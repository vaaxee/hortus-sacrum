import { elementDu } from './roues-calcul.ts';
import type { ElementListe, Pratique } from './types.ts';

/** Rang de la semaine dans le mois (1 à 5) : jours 1-7 → 1, 8-14 → 2, etc. `date` au format AAAA-MM-JJ. */
export function semaineDuMois(date: string): number {
	return Math.ceil(Number(date.slice(8, 10)) / 7);
}

/**
 * Prières à ouvrir ce jour-là pour un élément de la liste.
 * Élément « en alternance » : une seule prière, à tour de rôle selon la semaine du mois
 * (1re semaine → 1re prière, 2e → 2e…, et l'on recommence quand la liste est épuisée).
 */
export function textesDuJour(e: Pick<ElementListe, 'textes' | 'alterner' | 'roue'>, date: string, jour?: { temps: string; office: string }, roues: Pratique[] = []): string[] {
	// ligne « choisie par la roue » : la prière liée à l'élément du jour de la roue (rien si l'élément n'est qu'un thème)
	const r = e.roue ? roues.find((x) => x.id === e.roue && !x.supprimeLe) : undefined;
	if (r) {
		const el = elementDu(r, date);
		// la prière de l'élément du jour, puis les autres textes de la ligne (ex. la méthode de Montfort jointe au chapelet)
		return remplacementsDuTemps(el?.texte ? [el.texte, ...e.textes.slice(1)] : e.textes, jour);
	}
	const choisis = !e.alterner || e.textes.length < 2 ? e.textes : [e.textes[(semaineDuMois(date) - 1) % e.textes.length]];
	return remplacementsDuTemps(jaculatoiresDuJour(selonLeJour(choisis, date), date), jour);
}

/**
 * Lignes dont la prière change selon le jour de la semaine (dimanche → samedi) : un identifiant « du jour » remplacé par la page du jour.
 *  - Triple Couronne d'or : 1re lundi, mercredi, samedi ; 2e mardi, vendredi ; 3e jeudi, dimanche (Jardin, p. 21-25) ;
 *  - Chapelet : joyeux lundi et jeudi ; douloureux mardi et vendredi ; glorieux mercredi, samedi et dimanche ;
 *  - Petit bréviaire du Sacré-Cœur : un office par jour (Nancy, 1883).
 */
const TC = (n: number) => `hortus:triple-couronne-${n}`;
const CH = (n: string) => `hortus:chapelet-${n}`;
export const SELON_LE_JOUR: Record<string, string[]> = {
	'hortus:triple-couronne-du-jour': [TC(3), TC(1), TC(2), TC(1), TC(3), TC(2), TC(1)],
	'hortus:chapelet-du-jour': [CH('glorieux'), CH('joyeux'), CH('douloureux'), CH('glorieux'), CH('joyeux'), CH('douloureux'), CH('glorieux')],
	'hortus:petit-breviaire-du-jour': ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'].map((j) => `breviaire-sc:office-${j}`)
};
/** Libellés des identifiants « du jour » (éditeur de la liste). */
export const LIBELLES_DU_JOUR: Record<string, string> = {
	'hortus:triple-couronne-du-jour': 'Couronne du jour (selon le jour de la semaine)',
	'hortus:chapelet-du-jour': 'Chapelet du jour (selon le jour de la semaine)',
	'hortus:petit-breviaire-du-jour': 'Office du jour (selon le jour de la semaine)',
	'hortus:jaculatoires-du-jour': 'Dix jaculatoires, à tour de rôle'
};
/** Les trois chapelets, pour passer de l'un à l'autre (rosaire entier). */
export const CHAPELETS = [CH('joyeux'), CH('douloureux'), CH('glorieux')];
export function selonLeJour(ids: string[], date: string): string[] {
	const j = new Date(date + 'T12:00:00').getDay();
	return ids.map((id) => SELON_LE_JOUR[id]?.[j] ?? id);
}

/**
 * Ligne « Jaculatoires du jour » : 10 jaculatoires indulgenciées prises dans les 40 meilleures (rapport indulgence /
 * longueur, Thésaurisons 1941), à tour de rôle : on parcourt les 40 en 4 jours.
 */
export const JACULATOIRES_DU_JOUR = 'hortus:jaculatoires-du-jour';
export const JACULATOIRES = [
	'thesaurisons:jac-100',
	'thesaurisons:jac-44',
	'thesaurisons:jac-105',
	'thesaurisons:jac-19',
	'thesaurisons:jac-33',
	'thesaurisons:jac-57',
	'thesaurisons:jac-206',
	'thesaurisons:jac-71',
	'thesaurisons:jac-273',
	'thesaurisons:jac-199',
	'thesaurisons:jac-35',
	'thesaurisons:jac-37',
	'thesaurisons:jac-70',
	'thesaurisons:jac-90',
	'thesaurisons:jac-198',
	'thesaurisons:jac-207',
	'thesaurisons:jac-205',
	'thesaurisons:jac-72',
	'thesaurisons:jac-12',
	'thesaurisons:jac-204',
	'thesaurisons:jac-38',
	'thesaurisons:jac-87',
	'thesaurisons:jac-134',
	'thesaurisons:jac-244',
	'thesaurisons:jac-246',
	'thesaurisons:jac-275',
	'thesaurisons:jac-85',
	'thesaurisons:jac-7',
	'thesaurisons:jac-14',
	'thesaurisons:jac-39',
	'thesaurisons:jac-84',
	'thesaurisons:jac-232',
	'thesaurisons:jac-239',
	'thesaurisons:jac-242',
	'thesaurisons:jac-274',
	'thesaurisons:jac-132',
	'thesaurisons:jac-13',
	'thesaurisons:jac-108',
	'thesaurisons:jac-215',
	'thesaurisons:jac-491'
];
export function jaculatoiresDuJour(ids: string[], date: string): string[] {
	const i = ids.indexOf(JACULATOIRES_DU_JOUR);
	if (i < 0) return ids;
	const jourN = Math.floor(Date.parse(date + 'T12:00:00Z') / 86400000);
	const debut = ((jourN % 4) + 4) % 4 * 10;
	return [...ids.slice(0, i), ...JACULATOIRES.slice(debut, debut + 10), ...ids.slice(i + 1)];
}

/**
 * Au temps pascal, le Regina cæli remplace l'Angélus (Beringer 1925, n° 428).
 * Samedi saint : l'Angélus le matin, le Regina cæli à partir de midi — on montre les deux.
 */
const PASCAL: Record<string, string> = { 'paroissien:angelus': 'beringer:regina-caeli' };

export function remplacementsDuTemps(ids: string[], jour?: { temps: string; office: string }): string[] {
	if (!jour) return ids;
	if (jour.office === 'Samedi saint') return ids.flatMap((id) => (PASCAL[id] ? [id, PASCAL[id]] : [id]));
	if (jour.temps === 'Temps pascal') return ids.map((id) => PASCAL[id] ?? id);
	return ids;
}
