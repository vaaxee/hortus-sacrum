/**
 * Constantes de l'ancienne liste du jour encore utilisées : pages « du jour », chapelets, jaculatoires.
 * La liste du jour est désormais calculée par le programme unique (programme/journee.ts).
 */

/**
 * Pages dont la prière change selon le jour de la semaine (dimanche → samedi) :
 *  - Triple Couronne d'or : 1re lundi, mercredi, samedi ; 2e mardi, vendredi ; 3e jeudi, dimanche (Jardin, p. 21-25) ;
 *  - Chapelet : joyeux lundi et jeudi ; douloureux mardi et vendredi ; glorieux mercredi, samedi et dimanche ;
 *  - Petit bréviaire du Sacré-Cœur : un office par jour (Nancy, 1883).
 */
const TC = (n: number) => `hortus:triple-couronne-${n}`;
const CH = (n: string) => `hortus:chapelet-${n}`;
export const SELON_LE_JOUR: Record<string, string[]> = {
	'hortus:triple-couronne-du-jour': [TC(3), TC(1), TC(2), TC(1), TC(3), TC(2), TC(1)],
	'hortus:chapelet-du-jour': [
		CH('glorieux'),
		CH('joyeux'),
		CH('douloureux'),
		CH('glorieux'),
		CH('joyeux'),
		CH('douloureux'),
		CH('glorieux')
	],
	'hortus:petit-breviaire-du-jour': ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'].map(
		(j) => `breviaire-sc:office-${j}`
	)
};
/** Les trois chapelets, pour passer de l'un à l'autre (rosaire entier). */
export const CHAPELETS = [CH('joyeux'), CH('douloureux'), CH('glorieux')];

/**
 * Jaculatoires de Thésaurisons pour le ciel (1941), parmi lesquelles se tire la jaculatoire d'ouverture de l'écran du jour
 * (programme/bilan.ts : seulement celles de l'Enchiridion de 1952, avec une traduction approuvée).
 */
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
