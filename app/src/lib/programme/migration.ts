/**
 * Bascule de l'ancienne liste du jour (table `liste`) vers le programme unique (docs/conception/REFONTE_2026-11-18.md,
 * § 3). On garde les ajouts personnels, les durées et les rappels ; l'ancienne liste est archivée (versions et meta) ;
 * chaque changement est noté pour la page « Ce qui a changé », qui permet de revenir en arrière ligne par ligne.
 */
import type { ElementListe } from '../types.ts';
import { textesDuProgramme } from './inventaire.ts';
import type { EntreeProgramme, Moment, Programme, ReglageProgramme } from './types.ts';

const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];

/** Ancienne ligne livrée → entrée du programme qui la remplace (null : elle n'a plus de ligne, voir le motif). */
export const CORRESPONDANCE: Record<string, string | null> = {
	'liste:1': 'prog:priere-du-matin',
	'liste:2': 'prog:priere-du-matin',
	'liste:3': 'prog:salve-regina',
	'liste:4': 'prog:priere-du-matin',
	'liste:5': 'prog:cordon-gloria',
	'liste:6': 'lec:saint',
	'liste:7': 'lec:meditation',
	'liste:9': null,
	'liste:10': null,
	'liste:11': null,
	'liste:12': 'prog:angelus',
	'liste:13': 'prog:agonisants',
	'liste:14': 'prog:fleche-d-or',
	'liste:15': 'prog:chapelet',
	'liste:16': 'prog:triple-couronne',
	'liste:17': 'prog:devotion-mardi',
	'liste:18': 'prog:devotion-lundi',
	'liste:19': 'prog:brigitte',
	'liste:20': 'prog:devotion-vendredi',
	'liste:21': 'prog:priere-du-soir',
	'liste:22': 'prog:priere-du-soir',
	'liste:23': 'prog:priere-du-soir',
	'liste:roue': null,
	'liste:cordon-mercredi': 'prog:devotion-mercredi',
	'liste:scapulaire-jahenny': 'prog:scapulaire-jahenny',
	'liste:jaculatoires': null,
	'liste:petit-breviaire': 'lec:office',
	...Object.fromEntries(JOURS.flatMap((j, k) => [[k ? `liste:8-${k}` : 'liste:8', `prog:devotion-${j}`]])),
	...Object.fromEntries(JOURS.flatMap((j, k) => [[k ? `liste:24-${k}` : 'liste:24', `prog:devotion-${j}`]])),
	...Object.fromEntries(JOURS.map((_, k) => [k ? `liste:25-${k}` : 'liste:25', 'prog:don-du-jour']))
};

/** Pourquoi une ancienne ligne n'a plus de ligne propre. */
const MOTIF_SANS_LIGNE: Record<string, string> = {
	'liste:9': 'les dévotions à jours comptés du plan ont maintenant leur propre ligne, le jour venu',
	'liste:10': 'les neuvaines et trentains du plan ont maintenant leur propre ligne, le jour venu',
	'liste:11': 'la dévotion du mois se lit dans Lecture et s’ajoute aux pages du jour',
	'liste:roue': 'la roue se lit dans Lecture',
	'liste:jaculatoires': 'une jaculatoire s’affiche maintenant à chaque ouverture de l’écran du jour'
};

/** Ligne du jour qui porte une entrée (l'hôte, pour une petite pratique insérée). */
export function ligneDeLEntree(id: string, programme: Programme): string {
	const e = programme.entrees.find((x) => x.id === id);
	if (!e || e.page || e.lecture || !e.insertions?.length) return id;
	return e.insertions[0].hote;
}

/**
 * Coche d'une ancienne ligne → ligne du programme (Historique, couronnes). `personnels` : identifiants des anciens ajouts
 * personnels (archive), devenus « perso:… ». Les autres identifiants restent tels quels.
 */
export function traduireCoche(elementId: string, programme: Programme, personnels?: Set<string>): string {
	if (personnels?.has(elementId)) return `perso:${elementId}`;
	if (!(elementId in CORRESPONDANCE)) return elementId;
	const cible = CORRESPONDANCE[elementId];
	return cible ? ligneDeLEntree(cible, programme) : elementId;
}

export type Annulation = { reactiver: string } | { retirer: { id: string; champ: 'duree' | 'heures' | 'quand' } } | { supprimer: string };

export interface Changement {
	/** Anciennes lignes en cause. */
	anciens: string[];
	titre: string;
	texte: string;
	annuler?: Annulation;
}

export interface PlanDeMigration {
	reglages: ReglageProgramme[];
	changements: Changement[];
}

const MOMENT: Record<string, Moment> = { matin: 'matin', propre: 'journee', journee: 'journee', soir: 'soir' };
const tousLesJours = (j?: boolean[]) => !j || j.every(Boolean);
const joursDe = (j: boolean[]) => j.flatMap((v, k) => (v ? [k] : []));
const enClair = (j: boolean[]) =>
	joursDe(j)
		.map((k) => JOURS[k])
		.join(', ');

function original(e: ElementListe): Partial<ElementListe> | null {
	if (!e.original) return null;
	try {
		return JSON.parse(e.original) as Partial<ElementListe>;
	} catch {
		return null;
	}
}

/** Entrée personnelle tirée d'une ancienne ligne (ajout personnel, ou ligne livrée que l'on reprend telle quelle). */
export function entreeDe(e: ElementListe, id: string, titre = e.titre): EntreeProgramme {
	return {
		id,
		titre,
		revision: 1,
		source: `ancienne liste du jour (${e.id})`,
		...(!tousLesJours(e.jours) && { quand: { jours_semaine: joursDe(e.jours) } }),
		...(e.duree !== undefined && { duree: e.duree }),
		page: {
			moment: MOMENT[e.moment] ?? 'journee',
			ordre: 100 + (e.ordre ?? 0),
			...(e.rappels?.length && { heures: [...e.rappels] }),
			sections: (e.textes ?? []).map((t) => ({ texte: t }))
		}
	};
}

/** Le plan de la bascule, sans rien écrire : calculé à partir de l'ancienne liste et du programme livré. */
export function planifierMigration(liste: ElementListe[], programme: Programme, maintenant: string): PlanDeMigration {
	const reglages = new Map<string, ReglageProgramme>();
	const changements: Changement[] = [];
	const regler = (id: string) => {
		let r = reglages.get(id);
		if (!r) reglages.set(id, (r = { id, modifieLe: maintenant }));
		return r;
	};
	const entree = (id: string) => programme.entrees.find((e) => e.id === id);
	const dansLeProgramme = textesDuProgramme(programme);
	const actif = (e: ElementListe) => e.actif !== false && !e.supprimeLe;

	// 1. ajouts personnels : gardés tels quels
	for (const e of liste) {
		if (e.origine !== 'personnel' || e.supprimeLe) continue;
		const id = `perso:${e.id}`;
		reglages.set(id, { id, entree: entreeDe(e, id), ...(e.actif === false && { actif: false }), modifieLe: maintenant });
		changements.push({ anciens: [e.id], titre: e.titre, texte: 'Ajout personnel gardé.', annuler: { supprimer: id } });
	}

	// 2. lignes livrées : regroupées par entrée cible
	const parCible = new Map<string, ElementListe[]>();
	for (const e of liste) {
		if (e.origine === 'personnel') continue;
		if (!(e.id in CORRESPONDANCE)) {
			// ligne livrée inconnue (version intermédiaire) : reprise telle quelle si elle a des prières
			if (actif(e) && e.textes?.length) {
				const id = `perso:${e.id}`;
				reglages.set(id, { id, entree: entreeDe(e, id), modifieLe: maintenant });
				changements.push({ anciens: [e.id], titre: e.titre, texte: 'Ligne reprise telle quelle.', annuler: { supprimer: id } });
			}
			continue;
		}
		const cible = CORRESPONDANCE[e.id];
		if (!cible) {
			if (actif(e)) changements.push({ anciens: [e.id], titre: e.titre, texte: `Plus de ligne propre : ${MOTIF_SANS_LIGNE[e.id]}.` });
			continue;
		}
		parCible.set(cible, [...(parCible.get(cible) ?? []), e]);
	}

	for (const [cible, sources] of parCible) {
		const ent = entree(cible);
		if (!ent) continue;
		const titres = [...new Set(sources.map((s) => s.titre))];
		const nom = ent.titre;
		const porteLigne = !!(ent.page || ent.lecture);

		// désactivée : seulement si toutes les anciennes lignes qui y mènent l'étaient
		if (sources.every((s) => !actif(s))) {
			regler(cible).actif = false;
			changements.push({
				anciens: sources.map((s) => s.id),
				titre: nom,
				texte: `Désactivée, comme ${titres.length > 1 ? 'les anciennes lignes' : 'l’ancienne ligne'} « ${titres.join(' », « ')} ».`,
				annuler: { reactiver: cible }
			});
			continue;
		} else if (sources.some((s) => !actif(s))) {
			const eteintes = sources.filter((s) => !actif(s)).map((s) => s.titre);
			changements.push({
				anciens: sources.filter((s) => !actif(s)).map((s) => s.id),
				titre: nom,
				texte: `« ${[...new Set(eteintes)].join(' », « ')} » était désactivé ; c’est maintenant une partie de « ${nom} », gardée.`
			});
		}

		// durée réglée à la main
		const durees = sources.map((s) => s.duree).filter((d): d is number => d !== undefined);
		if (durees.length && porteLigne) {
			regler(cible).duree = Math.max(...durees);
			changements.push({
				anciens: sources.filter((s) => s.duree !== undefined).map((s) => s.id),
				titre: nom,
				texte: `Durée réglée à la main gardée : ${Math.max(...durees)} min.`,
				annuler: { retirer: { id: cible, champ: 'duree' } }
			});
		}

		// rappels changés (une seule ancienne ligne, qui porte une ligne)
		if (sources.length === 1) {
			const s = sources[0];
			const o = original(s);
			const avant = o?.rappels ?? [];
			const apres = s.rappels ?? [];
			if (o && avant.join() !== apres.join()) {
				if (porteLigne && ent.page) {
					regler(cible).heures = apres;
					changements.push({
						anciens: [s.id],
						titre: nom,
						texte: apres.length ? `Rappels gardés : ${apres.join(', ')}.` : 'Rappels retirés, comme dans l’ancienne liste.',
						annuler: { retirer: { id: cible, champ: 'heures' } }
					});
				} else
					changements.push({
						anciens: [s.id],
						titre: nom,
						texte: `Rappels (${apres.join(', ') || 'aucun'}) non repris : « ${nom} » se dit maintenant dans une autre page.`
					});
			}
			// jours changés
			if (o?.jours && s.jours && o.jours.join() !== s.jours.join() && !ent.quand && porteLigne) {
				regler(cible).quand = { jours_semaine: joursDe(s.jours) };
				changements.push({
					anciens: [s.id],
					titre: nom,
					texte: `Seulement le ${enClair(s.jours)}, comme dans l’ancienne liste.`,
					annuler: { retirer: { id: cible, champ: 'quand' } }
				});
			}
		}

		// prières changées par l'utilisateur : celles que le programme ne dit pas deviennent un ajout personnel
		for (const s of sources) {
			const o = original(s);
			if (!o || !actif(s) || (o.textes ?? []).join() === (s.textes ?? []).join()) continue;
			const nouvelles = (s.textes ?? []).filter((t) => !dansLeProgramme.has(t));
			if (!nouvelles.length) continue;
			const id = `perso:${s.id}`;
			reglages.set(id, {
				id,
				entree: entreeDe({ ...s, textes: nouvelles }, id, `${s.titre} (repris de l’ancienne liste)`),
				modifieLe: maintenant
			});
			changements.push({
				anciens: [s.id],
				titre: s.titre,
				texte: 'Vous aviez changé les prières de cette ligne : celles que le programme ne dit pas sont gardées comme ajout personnel.',
				annuler: { supprimer: id }
			});
		}
	}
	return { reglages: [...reglages.values()], changements };
}
