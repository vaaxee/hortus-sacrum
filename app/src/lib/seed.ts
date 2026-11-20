import { anneeLiturgique } from './calendrier.ts';
import { contenu, db, enregistrer } from './db.ts';
import { pratiquesDuPlan } from './plan.ts';
import { basculer } from './programme/bascule.ts';
import { chargerProgramme } from './programme/charger.ts';
import { amorcerRoues } from './roues.ts';
import type { Pratique, Texte } from './types.ts';
import { SOURCE_VIDE } from './types.ts';

/** Date des données de départ (livret, liste, plan) : plus ancienne que toute modification de l'utilisateur. */
const DEPART = '2000-01-01T00:00:00.000Z';

/** Conversion des pièces du livret (data/prieres/jardin.json) vers le balisage de l'app. */

interface Bloc {
	type: string;
	texte?: string;
	v?: string;
	r?: string;
	la?: string;
	fr?: string;
	items?: string[];
	numero?: string;
	fruit?: string;
	fruit_libelle?: string;
	titre?: string;
	note?: string;
}

interface Piece {
	id: string;
	ordre: number;
	titre: string;
	type: string;
	partie: { numero: string; titre: string } | null;
	jour_de_semaine: string | null;
	page_livret: number | null;
	usage: string | null;
	indulgence: string | null;
	source: string | null;
	blocs: Bloc[];
}

export function blocsVersCorps(blocs: Bloc[]): { corps: string; latin: string } {
	const fr: string[] = [];
	const la: string[] = [];
	for (const b of blocs) {
		switch (b.type) {
			case 'texte':
			case 'conclusion':
				fr.push(b.type === 'conclusion' ? `*${b.texte}*` : (b.texte ?? ''));
				break;
			case 'rubrique':
			case 'notice':
				fr.push(`[r]${(b.texte ?? '').replace(/\n+/g, ' ')}[/r]`);
				break;
			case 'intertitre':
				fr.push(`## ${b.texte}`);
				break;
			case 'traduction':
				fr.push(`[${b.texte}]`);
				break;
			case 'invocation':
				fr.push(b.texte ?? '');
				break;
			case 'verset':
				fr.push(`℣. ${b.v}\n℟. ${b.r}`);
				break;
			case 'strophe':
				fr.push(b.fr ?? '');
				la.push(b.la ?? '');
				break;
			case 'litanie':
				fr.push((b.items ?? []).join('\n'));
				break;
			case 'mystere':
				fr.push(`[r]${b.numero}[/r] ${b.texte}\n*${b.fruit_libelle}* ${b.fruit}`);
				break;
			case 'numero':
				fr.push(`[r]${b.numero}.[/r] ${b.texte}`);
				break;
			case 'fiche':
				fr.push(`[r]${b.titre}[/r] ${b.texte}. *${b.note}*`);
				break;
			default:
				if (b.texte) fr.push(b.texte);
		}
	}
	return { corps: fr.filter(Boolean).join('\n\n'), latin: la.filter(Boolean).join('\n\n') };
}

export function pieceVersTexte(p: Piece): Texte {
	const { corps, latin } = blocsVersCorps(p.blocs);
	const t: Texte = {
		id: `jardin:${p.id}`,
		origine: 'livret',
		titre: p.titre,
		partie: p.partie ? p.partie.titre : '',
		categorie: p.jour_de_semaine ?? '',
		corps,
		latin,
		usage: p.usage ?? '',
		indulgence: p.indulgence ?? '',
		source: {
			...SOURCE_VIDE,
			ouvrage: p.source ?? '',
			edition: 'Le Jardin de l’âme (livret)',
			page: p.page_livret ? String(p.page_livret) : ''
		},
		ordre: p.ordre,
		creeLe: '',
		modifieLe: ''
	};
	return t;
}

/**
 * À chaque lancement : livre le livret (premier lancement), le plan de l'année, les textes sourcés jamais encore livrés,
 * les roues ; puis, une seule fois, archive l'ancienne liste du jour et la remplace par le programme unique (SPEC § 11).
 * Ne touche jamais à ce que l'utilisateur a modifié. La liste du jour n'est plus amorcée : elle est calculée
 * (app/src/lib/programme).
 */
export async function amorcer(fetchFn: typeof fetch = fetch): Promise<void> {
	const fait = await db.meta.get('amorce');
	const niveau = (fait?.valeur as number) ?? 0;
	if (niveau < 1) await amorcerLivret(fetchFn);
	if (niveau < 2) await importerPlan(fetchFn);
	if (niveau < 2) await db.meta.put({ cle: 'amorce', valeur: 2 });
	await amorcerSources(fetchFn);
	await amorcerRoues(fetchFn);
	await rouesDesLitanies();
	await retirerRoueDesChapelets();
	await rappelsDuProfil();
	await textesDesDevotions();
	const programme = await chargerProgramme(fetchFn);
	if (programme) await basculer(programme);
}

/** Textes sourcés trouvés pour des dévotions du plan restées sans texte (titre de la dévotion → texte). */
const TEXTES_DES_DEVOTIONS: Record<string, string | [string[], string]> = {
	'Neuvaine à l’Immaculée Conception': 'weber:neuvaine-immaculee-conception',
	'Neuvaine au Sacré-Cœur': 'liguori:neuvaine-sacre-coeur',
	'Neuvaine de la Nativité de Notre-Dame': 'neuvaines-1886:nativite',
	'Neuvaine de l’Assomption': 'neuvaines-1886:assomption',
	'Neuvaine de Noël': 'liguori:neuvaine-de-noel',
	// pas de neuvaine propre trouvée : l'Enchiridion indulgencie toute prière faite neuf jours de suite en l'honneur du mystère
	'Neuvaine du Rosaire': [
		['sambucy:chapelet-saint-dominique', 'paroissien:litanies-sainte-vierge'],
		'Chaque jour : le chapelet et les litanies de la sainte Vierge, avec le propos de prier ainsi neuf jours de suite. Toute prière en l’honneur de Notre-Dame du Rosaire faite ainsi : 5 ans une fois le jour ; plénière à la fin, aux conditions ordinaires (Ench. 1952, n° 396).'
	],
	'Neuvaine de la Toussaint': [['paroissien:litanies-des-saints'], 'Chaque jour : les litanies des saints (5 ans ; Ench. 1952, n° 687).']
};

/** Relie chaque texte une seule fois (meta « devotions-textes ») aux dévotions de ce titre, vides et jamais modifiées. */
async function textesDesDevotions(): Promise<void> {
	const livres = new Set(((await db.meta.get('devotions-textes'))?.valeur as string[] | undefined) ?? []);
	let change = false;
	for (const [titre, v] of Object.entries(TEXTES_DES_DEVOTIONS)) {
		const [ids, note] = typeof v === 'string' ? [[v], ''] : v;
		const id = ids.join('+');
		if (livres.has(id)) continue;
		let manque = false;
		for (const t of ids) if (!(await db.textes.get(t))) manque = true;
		if (manque) continue;
		for (const p of await db.pratiques.toArray()) {
			if (p.titre !== titre || p.supprimeLe || p.textes.length || !(p.modifieLe === DEPART || p.original === contenu(p))) continue;
			const q = { ...p, textes: ids, ...(note && !p.notes ? { notes: note } : {}) } as Pratique;
			q.original = contenu(q);
			await db.pratiques.put(q);
		}
		livres.add(id);
		change = true;
	}
	if (change) await db.meta.put({ cle: 'devotions-textes', valeur: [...livres] });
}

/** Une seule fois (meta « profil-rappels ») : les anniversaires du profil spirituel déjà saisis reçoivent le rappel la veille. */
async function rappelsDuProfil(): Promise<void> {
	if (await db.meta.get('profil-rappels')) return;
	for (const f of await db.fetes.toArray()) {
		if (f.profil && !f.supprimeLe && !f.rappelVeille) await enregistrer('fetes', { ...f, rappelVeille: true });
	}
	await db.meta.put({ cle: 'profil-rappels', valeur: true });
}

/**
 * Litanies du jour (docs/LISTE_DU_JOUR.md) : une ligne par jour de la semaine, selon la dédicace du jour,
 * les litanies alternant d'une semaine du mois à l'autre. Jours sans litanie sourcée : ligne sans prière.
 */
const LITANIES_PAR_JOUR: string[][] = [
	['fervent:litanies-sainte-trinite', 'paroissien:litanies-saint-nom', 'paroissien:litanies-des-saints'], // dimanche : sainte Trinité
	['fsspx:litanies-delivrance-ames-purgatoire', 'salve-regina:litanies-fideles-defunts'], // lundi : âmes du purgatoire
	['fervent:litanies-ange-gardien', 'jardin:litanies-de-la-sainte-face'], // mardi : saints Anges
	['beringer:litanies-saint-joseph'], // mercredi : saint Joseph
	['fervent:litanies-saint-sacrement', 'paroissien:litanies-saint-nom'], // jeudi : Saint-Sacrement
	['beringer:litanies-sacre-coeur', 'jardin:litanies-de-notre-dame-des-sept-douleurs'], // vendredi : Passion, Sacré-Cœur
	['paroissien:litanies-sainte-vierge', 'jardin:litanies-de-notre-dame-des-sept-douleurs'] // samedi : sainte Vierge
];

const JOURS_NOMS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];

/**
 * Roues des litanies (une par jour qui en a plusieurs) : la litanie du jour avance d'un cran chaque semaine depuis le
 * premier dimanche de l'Avent. Hors de la rosace (champ « liste »), modifiables ; le programme lit leur élément du jour.
 */
async function rouesDesLitanies(): Promise<void> {
	for (let k = 0; k < 7; k++) {
		const ids = LITANIES_PAR_JOUR[k];
		const id = `roue:litanies-${k}`;
		if (ids.length < 2 || (await db.pratiques.get(id))) continue;
		const textes = await Promise.all(ids.map((t) => db.textes.get(t)));
		if (!textes.every(Boolean)) continue;
		const r = {
			id,
			origine: 'officielle',
			titre: `Litanies du ${JOURS_NOMS[k]}`,
			type: 'roue',
			regle: { genre: 'roue', unite: 'semaine' },
			textes: ids,
			promesses: '',
			indulgence: '',
			source: { ...SOURCE_VIDE },
			notes: '',
			active: true,
			liste: true,
			elements: ids.map((t, i) => ({ fr: textes[i]?.titre ?? t, texte: t })),
			creeLe: DEPART,
			modifieLe: DEPART
		} as Pratique;
		r.original = contenu(r);
		await db.pratiques.put(r);
	}
}

/** Une seule fois : la roue des trois chapelets n'a plus d'usage (chapelet du jour), écartée si elle n'a pas été modifiée. */
async function retirerRoueDesChapelets(): Promise<void> {
	if (await db.meta.get('roue-chapelets-retiree')) return;
	const r = await db.pratiques.get('roue:chapelets-rosaire');
	if (r && !r.supprimeLe && r.original === contenu(r)) await db.pratiques.put({ ...r, supprimeLe: new Date().toISOString() });
	await db.meta.put({ cle: 'roue-chapelets-retiree', valeur: true });
}

/**
 * Textes recopiés d'éditions anciennes (data/prieres/sources.json), marqués « Source vérifiée ».
 * Chaque texte n'est livré qu'une fois : supprimé ou modifié par l'utilisateur, il n'est jamais remis ni remplacé.
 */
export async function amorcerSources(fetchFn: typeof fetch = fetch): Promise<void> {
	const rep = await fetchFn('/data/prieres/sources.json');
	if (!rep.ok) return;
	const doc = (await rep.json()) as { pieces: Omit<Texte, 'origine' | 'ordre' | 'creeLe' | 'modifieLe'>[] };
	const livres = new Set(((await db.meta.get('sources'))?.valeur as string[] | undefined) ?? []);
	await reviser(doc.pieces as (Texte & { revision?: number })[]);
	const nouveaux = doc.pieces.filter((p) => !livres.has(p.id));
	if (!nouveaux.length) return;
	const dernier = await db.textes.orderBy('ordre').last();
	let ordre = (dernier?.ordre ?? 0) + 1;
	for (const brut of nouveaux) {
		livres.add(brut.id);
		if (await db.textes.get(brut.id)) continue;
		const x = { ...brut, origine: 'officielle', ordre: ordre++, creeLe: DEPART, modifieLe: DEPART } as Texte;
		x.original = contenu(x);
		await db.textes.put(x);
	}
	await db.meta.put({ cle: 'sources', valeur: [...livres] });
}

/**
 * Corrections des textes déjà livrés : une pièce dont la `revision` (data) dépasse celle déjà appliquée remplace le texte
 * en base, seulement si l'utilisateur ne l'a pas modifié (meta « revisions » : id → révision appliquée).
 */
async function reviser(pieces: (Texte & { revision?: number })[]): Promise<void> {
	const faites = ((await db.meta.get('revisions'))?.valeur as Record<string, number> | undefined) ?? {};
	let change = false;
	for (const p of pieces) {
		if (!p.revision || (faites[p.id] ?? 0) >= p.revision) continue;
		faites[p.id] = p.revision;
		change = true;
		const t = await db.textes.get(p.id);
		if (!t || !(t.modifieLe === DEPART || t.original === contenu(t))) continue;
		const { revision: _r, ...brut } = p;
		const x = { ...t, ...brut } as Texte;
		x.original = contenu(x);
		await db.textes.put(x);
	}
	if (change) await db.meta.put({ cle: 'revisions', valeur: faites });
}

/**
 * Importe le plan des dévotions (année liturgique en cours et suivante) comme pratiques modifiables.
 * N'écrase jamais une pratique existante. Renvoie le nombre de pratiques ajoutées.
 */
export async function importerPlan(fetchFn: typeof fetch = fetch): Promise<number> {
	const y = new Date().getFullYear();
	const textes = await db.textes.toArray();
	const t = DEPART;
	let n = 0;
	for (const a of [y - 1, y]) {
		const annee = await anneeLiturgique(a, fetchFn);
		if (!annee) continue;
		for (const b of pratiquesDuPlan(annee, textes)) {
			if (await db.pratiques.get(b.id)) continue;
			const p = { ...b, creeLe: t, modifieLe: t } as Pratique;
			p.original = contenu(p);
			await db.pratiques.put(p);
			n++;
		}
	}
	return n;
}
async function amorcerLivret(fetchFn: typeof fetch): Promise<void> {
	const rep = await fetchFn('/data/prieres/jardin.json');
	const doc = (await rep.json()) as { pieces: Piece[] };
	const textes = doc.pieces.map((p) => {
		const x = pieceVersTexte(p);
		x.creeLe = x.modifieLe = DEPART;
		x.original = contenu(x);
		return x;
	});
	await db.transaction('rw', db.textes, async () => {
		for (const x of textes) if (!(await db.textes.get(x.id))) await db.textes.put(x);
	});
}
