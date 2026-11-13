import type { ElementListe } from './types.ts';

/** Rang de la semaine dans le mois (1 à 5) : jours 1-7 → 1, 8-14 → 2, etc. `date` au format AAAA-MM-JJ. */
export function semaineDuMois(date: string): number {
	return Math.ceil(Number(date.slice(8, 10)) / 7);
}

/**
 * Prières à ouvrir ce jour-là pour un élément de la liste.
 * Élément « en alternance » : une seule prière, à tour de rôle selon la semaine du mois
 * (1re semaine → 1re prière, 2e → 2e…, et l'on recommence quand la liste est épuisée).
 */
export function textesDuJour(e: Pick<ElementListe, 'textes' | 'alterner'>, date: string): string[] {
	if (!e.alterner || e.textes.length < 2) return e.textes;
	return [e.textes[(semaineDuMois(date) - 1) % e.textes.length]];
}
