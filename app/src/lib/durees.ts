/**
 * Durée estimée de la prière : d'après la longueur du texte (récitation vocale posée), ou durée fixe pour ce qui ne
 * se mesure pas au texte (méditation, chapelet…). Chaque ligne peut porter sa propre durée, réglée à la main.
 */

/** Mots par minute en récitation vocale, posée (ni lue à voix basse ni chantée). */
export const MOTS_PAR_MINUTE = 120;

/** Lignes de la liste de départ dont la durée ne se déduit pas du texte (minutes). */
export const DUREES_FIXES: Record<string, number> = {
	'Méditation du jour': 15,
	Chapelet: 20,
	'Office du jour et vie du saint': 5,
	'Dévotion du mois': 5,
	'La roue du jour': 3,
	'Intentions particulières du jour': 1,
	'Dévotion du jour de la semaine': 5,
	'Triple Couronne d’or du Sacré-Cœur': 15,
	'Chapelet de saint Michel (couronne angélique)': 15,
	'Chapelet des Morts': 10
};

/** Minutes de récitation d'un texte (au moins une demi-minute ; les rubriques en italique ne se disent pas). */
export function minutesDuTexte(corps: string): number {
	const dit = corps.replace(/\*[^*\n]+\*/g, ' ').replace(/^#{2,3} .*$/gm, ' ');
	const mots = dit.split(/\s+/).filter((w) => /[\p{L}]/u.test(w)).length;
	return Math.max(0.5, mots / MOTS_PAR_MINUTE);
}

/** « 5 min », « 1 h 05 » ; arrondi à la minute (« < 1 min » pour moins d'une minute). */
export function enMinutes(m: number): string {
	const r = Math.round(m);
	if (r < 1) return '< 1 min';
	if (r < 60) return `${r} min`;
	return `${Math.floor(r / 60)} h ${String(r % 60).padStart(2, '0')}`;
}
