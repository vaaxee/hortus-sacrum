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
		return remplacementsDuTemps(el?.texte ? [el.texte] : e.textes, jour);
	}
	const choisis = !e.alterner || e.textes.length < 2 ? e.textes : [e.textes[(semaineDuMois(date) - 1) % e.textes.length]];
	return remplacementsDuTemps(avecLePropre(choisis, date), jour);
}

/**
 * Triple Couronne d'or : l'ordinaire est suivi du propre de la couronne du jour (invocation et mystères) :
 * 1re lundi, mercredi, samedi ; 2e mardi, vendredi ; 3e jeudi, dimanche (Jardin, p. 21-25).
 */
const TRIPLE = 'jardin:la-triple-couronne-d-or-du-sacre-c-ur-de-jesus';
const COURONNES = [
	'jardin:troisieme-couronne-le-sacre-c-ur-de-jesus-dans-l-eucharistie', // dimanche
	'jardin:premiere-couronne-le-sacre-c-ur-de-jesus-dans-son-incarnatio', // lundi
	'jardin:deuxieme-couronne-le-sacre-c-ur-de-jesus-dans-sa-passion', // mardi
	'jardin:premiere-couronne-le-sacre-c-ur-de-jesus-dans-son-incarnatio', // mercredi
	'jardin:troisieme-couronne-le-sacre-c-ur-de-jesus-dans-l-eucharistie', // jeudi
	'jardin:deuxieme-couronne-le-sacre-c-ur-de-jesus-dans-sa-passion', // vendredi
	'jardin:premiere-couronne-le-sacre-c-ur-de-jesus-dans-son-incarnatio' // samedi
];
export function avecLePropre(ids: string[], date: string): string[] {
	const i = ids.indexOf(TRIPLE);
	if (i < 0) return ids;
	const propre = COURONNES[new Date(date + 'T12:00:00').getDay()];
	if (ids.includes(propre)) return ids;
	return [...ids.slice(0, i + 1), propre, ...ids.slice(i + 1)];
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
