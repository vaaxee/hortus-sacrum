/**
 * Éditeur de recueils (SPEC § 9 ; REFONTE § 6, lot 11). Les recueils livrés (data/recueils) restent des fichiers en
 * lecture seule ; l'utilisateur, dans la base (tables `recueils` et `meditations`, déjà synchronisées) :
 * - ajoute ses propres recueils, découpés en entrées et affectés (mois, temps, fête, neuvaine, libre) ;
 * - corrige une entrée d'un recueil livré par une **surcharge** (une `Meditation` qui porte l'identifiant du recueil
 *   livré et le rang de l'entrée) : le fichier d'origine n'est jamais touché, et « Rétablir » remet le texte livré ;
 * - masque un recueil livré (réglage de l'appareil).
 * Fonctions pures d'abord (testées), accès à la base ensuite.
 */
import { contenu, creer, db, enregistrer, mettreALaCorbeille, nouvelId } from './db.ts';
import { decouper } from './importer.ts';
import { clesDuJour, entreesDuJour, type Choix, type EntreeRecueil, type Recueil as RecueilLu } from './meditations.ts';
import type { Jour } from './calendrier.ts';
import type { Meditation, Recueil as RecueilPerso, Source } from './types.ts';

/** Recueils livrés, dans l'ordre de la bibliothèque. */
export const RECUEILS_LIVRES: [string, string][] = [
	['hamon', 'Hamon — Méditations pour tous les jours de l’année'],
	['chaignon', 'Chaignon — La méditation, ou le fidèle sanctifié'],
	['mois-joseph', 'Lefebvre — Mois de saint Joseph (mars)'],
	['mois-marie', 'Lefebvre — Mois de Marie (mai)'],
	['mois-sacre-coeur', 'Lefebvre — Mois du Sacré-Cœur (juin)'],
	['mois-precieux-sang', 'Boylesve — Mois du Précieux Sang (juillet)'],
	['mois-purgatoire', 'Berlioux — Mois des âmes du purgatoire (novembre)'],
	['breviaire', 'Bréviaire romain — leçons du IIe nocturne'],
	['liguori-visites', 'S. Alphonse de Liguori — Visites au Saint-Sacrement et à la sainte Vierge (chaque jour du mois)']
];
export const estLivre = (id: string) => RECUEILS_LIVRES.some(([r]) => r === id);

export type Affectation = RecueilPerso['affectation'];
export const GENRES: { genre: Affectation['genre']; nom: string; aide: string }[] = [
	{ genre: 'mois', nom: 'Un mois', aide: 'numéro du mois (1 à 12) : une entrée par jour, dans l’ordre, en tête de la méditation' },
	{ genre: 'temps', nom: 'Un temps liturgique', aide: 'ex. « Temps de l’Avent » ; chaque entrée porte sa clé de jour' },
	{ genre: 'fete', nom: 'Une fête', aide: 'nom de la fête ; chaque entrée porte sa clé de jour (D:MM-JJ, F:…)' },
	{ genre: 'neuvaine', nom: 'Une neuvaine', aide: 'nom de la neuvaine ; chaque entrée porte sa clé de jour' },
	{
		genre: 'libre',
		nom: 'Aucune (lecture libre)',
		aide: 'lisible dans la bibliothèque ; une entrée qui porte une clé est proposée ce jour-là'
	}
];

/** Identifiant d'une surcharge : un seul par entrée livrée. */
export const idSurcharge = (recueil: string, rang: number) => `surcharge:${recueil}:${rang}`;

/** Clé d'une entrée d'un recueil affecté à un mois : son rang (1 = premier jour du mois). */
const cleDeMois = (rang: number) => `J:${rang}`;

/** Un recueil de l'utilisateur, sous la forme d'un recueil livré (pour la lecture et la méditation du jour). */
export function versRecueil(r: RecueilPerso, meditations: Meditation[]): RecueilLu {
	const entrees: EntreeRecueil[] = meditations
		.filter((m) => m.recueilId === r.id && !m.supprimeLe)
		.sort((a, b) => a.rang - b.rang)
		.map((m, i) => ({
			cle: m.cle || (r.affectation.genre === 'mois' ? cleDeMois(i + 1) : null),
			titre: m.titre,
			tome: 0,
			page: 0,
			corps: m.corps,
			...(m.pratique?.trim() && { pratique: m.pratique })
		}));
	const s = r.source;
	return {
		id: r.id,
		titre: r.titre,
		auteur: r.auteur,
		editions: {},
		provenance: [s.edition, s.page && `p. ${s.page}`, s.url].filter(Boolean).join(', ') || 'ajout personnel',
		entrees
	};
}

/** Un recueil livré, avec les corrections de l'utilisateur à la place des entrées corrigées. */
export function avecSurcharges(livre: RecueilLu, meditations: Meditation[]): RecueilLu {
	const parRang = new Map(meditations.filter((m) => m.recueilId === livre.id && !m.supprimeLe).map((m) => [m.rang, m]));
	if (!parRang.size) return livre;
	return {
		...livre,
		entrees: livre.entrees.map((e, i) => {
			const m = parRang.get(i);
			return m ? { ...e, titre: m.titre, corps: m.corps, ...(m.pratique?.trim() && { pratique: m.pratique }), corrige: true } : e;
		})
	};
}

/** Recueil de l'utilisateur affecté à ce mois (le plus récent), s'il y en a un : il passe avant le recueil livré. */
export function recueilDuMoisPerso(recueils: RecueilPerso[], mois: number): RecueilPerso | undefined {
	return recueils
		.filter((r) => !r.supprimeLe && r.affectation.genre === 'mois' && Number(r.affectation.valeur) === mois)
		.sort((a, b) => b.creeLe.localeCompare(a.creeLe))[0];
}

/** Entrées des recueils de l'utilisateur (hors mois) qui portent une clé de ce jour : proposées après les autres. */
export function choixPerso(recueils: RecueilLu[], date: string, jour?: Pick<Jour, 'tempora'> | null): Choix[] {
	return recueils.flatMap((recueil) => entreesDuJour(recueil, date, jour).map((entree) => ({ recueil, entree })));
}

/** Découpe un texte (saisi, collé ou lu d'un fichier) en entrées : une ligne « === Titre » ouvre une entrée. */
export function entreesDepuisTexte(texte: string): { titre: string; corps: string; pratique: string; cle: string }[] {
	return decouper(texte).map((p, i) => ({ titre: p.titre || `Entrée ${i + 1}`, corps: p.corps, pratique: '', cle: '' }));
}

/** Clés admises pour une entrée (meditations.ts) ; vide = selon l'affectation du recueil. */
export function cleValide(cle: string): boolean {
	return !cle || /^(T:[A-Za-z]+\d*-\d|D:\d\d-\d\d|F:[a-z0-9-]+|O:10-[1-5]|J:\d{1,2})$/.test(cle);
}

/** Exemples de clés pour un jour, à afficher comme aide (« D:12-08 ; T:Adv2-2 »). */
export const clesExemple = (date: string, jour?: Pick<Jour, 'tempora'> | null) => clesDuJour(date, jour).join(' ; ');

// ------------------------------------------------------------------ base

/** Masquage des recueils livrés : réglage de l'appareil (meta), non synchronisé. */
const MASQUES = 'recueils-masques';
export async function recueilsMasques(): Promise<string[]> {
	return ((await db.meta.get(MASQUES))?.valeur as string[] | undefined) ?? [];
}
export async function masquerRecueil(id: string, masquer: boolean): Promise<void> {
	const m = new Set(await recueilsMasques());
	if (masquer) m.add(id);
	else m.delete(id);
	await db.meta.put({ cle: MASQUES, valeur: [...m] });
}

export async function recueilsPerso(): Promise<RecueilPerso[]> {
	return (await db.recueils.toArray()).filter((r) => !r.supprimeLe).sort((a, b) => a.titre.localeCompare(b.titre, 'fr'));
}

export async function meditationsDe(recueilId: string): Promise<Meditation[]> {
	return (await db.meditations.where('recueilId').equals(recueilId).toArray()).filter((m) => !m.supprimeLe);
}

/** Enregistre un recueil de l'utilisateur et ses entrées (création ou modification complète). */
export async function sauverRecueil(
	r: { id?: string; titre: string; auteur: string; source: Source; affectation: Affectation },
	entrees: { titre: string; corps: string; pratique: string; cle: string }[]
): Promise<string> {
	const id = r.id ?? nouvelId();
	const avant = await db.recueils.get(id);
	const base = { id, origine: 'personnel' as const, titre: r.titre, auteur: r.auteur, source: r.source, affectation: r.affectation };
	if (avant) await enregistrer<RecueilPerso>('recueils', { ...avant, ...base });
	else await creer<RecueilPerso>('recueils', base);
	const anciennes = await meditationsDe(id);
	for (const [rang, e] of entrees.entries()) {
		const existante = anciennes.find((m) => m.rang === rang);
		const m = { recueilId: id, rang, titre: e.titre, corps: e.corps, pratique: e.pratique, ...(e.cle && { cle: e.cle }) };
		if (existante) {
			const { cle: _c, ...sansCle } = existante;
			await enregistrer<Meditation>('meditations', { ...sansCle, ...m });
		} else await creer<Meditation>('meditations', { id: nouvelId(), origine: 'personnel', ...m });
	}
	for (const m of anciennes.filter((x) => x.rang >= entrees.length)) await mettreALaCorbeille('meditations', m.id);
	return id;
}

export async function supprimerRecueil(id: string): Promise<void> {
	await mettreALaCorbeille('recueils', id);
	for (const m of await meditationsDe(id)) await mettreALaCorbeille('meditations', m.id);
}

/**
 * Corrige une entrée d'un recueil livré. La première correction crée la surcharge avec le texte livré pour original
 * (« Restaurer l'original » et l'historique des versions fonctionnent comme pour les prières), puis l'enregistre.
 */
export async function corrigerEntree(
	recueil: string,
	rang: number,
	livre: EntreeRecueil,
	correction: { titre: string; corps: string; pratique: string }
): Promise<void> {
	const id = idSurcharge(recueil, rang);
	let m = await db.meditations.get(id);
	if (!m || m.supprimeLe) {
		if (m) await db.meditations.delete(id);
		m = await creer<Meditation>('meditations', {
			id,
			origine: 'officielle',
			recueilId: recueil,
			rang,
			titre: livre.titre,
			corps: livre.corps,
			pratique: livre.pratique ?? ''
		});
	}
	if (contenu({ ...m, ...correction }) !== contenu(m)) await enregistrer<Meditation>('meditations', { ...m, ...correction });
}

/** Rétablit le texte livré : la surcharge va à la corbeille (restaurable). */
export async function retablirEntree(recueil: string, rang: number): Promise<void> {
	await mettreALaCorbeille('meditations', idSurcharge(recueil, rang));
}

/** Toutes les surcharges et entrées de l'utilisateur, pour la lecture et la méditation du jour. */
export async function toutesLesMeditations(): Promise<Meditation[]> {
	return (await db.meditations.toArray()).filter((m) => !m.supprimeLe);
}
