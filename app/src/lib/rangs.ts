import type { ElementListe, Pratique, Rang } from './types.ts';

/** Les trois rangs d'une dévotion, du plus nécessaire au plus libre. */
export const RANGS: { cle: Rang; latin: string; abrege: string; fr: string; aide: string }[] = [
	{ cle: 'praecipua', latin: 'Præcipua', abrege: 'Præc.', fr: 'principale', aide: 'Dévotions suivies et prières quotidiennes centrales : à garder même un jour chargé.' },
	{ cle: 'pia', latin: 'Pia', abrege: 'Pia', fr: 'pieuse', aide: 'Bonne et recommandée : à dire si le temps le permet.' },
	{ cle: 'supererogatoria', latin: 'Supererogatoria', abrege: 'Super.', fr: 'surérogatoire', aide: 'Par surcroît : la première à laisser un jour chargé.' }
];

export const ORDRE_RANG: Record<Rang, number> = { praecipua: 0, pia: 1, supererogatoria: 2 };

/** Rangs de départ des éléments de la liste du jour (par titre). Tout ce qui n'y est pas est « pia ». */
const RANG_DE_DEPART: Record<string, Rang> = {
	'Offrande du matin': 'praecipua',
	'Prière du matin': 'praecipua',
	'Méditation du jour': 'praecipua',
	'Dévotion à jours comptés en cours': 'praecipua',
	'Neuvaine ou trentain en cours': 'praecipua',
	'Angélus': 'praecipua',
	'Chapelet': 'praecipua',
	'Quinze oraisons de sainte Brigitte': 'praecipua',
	'Examen de conscience': 'praecipua',
	'Prière du soir': 'praecipua',
	'Prière du soir et examen de conscience': 'praecipua',
	'Cordon de saint Joseph : sept Gloria Patri': 'supererogatoria',
	'Cordon de saint Joseph : prière pour la pureté': 'supererogatoria'
};

export function rangElement(e: Pick<ElementListe, 'titre' | 'rang'>): Rang {
	return e.rang ?? RANG_DE_DEPART[e.titre] ?? 'pia';
}

/** Une pratique suivie (neuvaine, jours comptés, série) est principale, sauf choix contraire. */
export function rangPratique(p: Pick<Pratique, 'rang'>): Rang {
	return p.rang ?? 'praecipua';
}

/** Filtre « jour chargé » : rang le plus bas encore affiché. */
export type Seuil = Rang;
export const garde = (r: Rang, seuil: Seuil) => ORDRE_RANG[r] <= ORDRE_RANG[seuil];
