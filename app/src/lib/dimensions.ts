/**
 * Dimensions d'un texte (lot « Dimensions », D2) : ce qui compte, dimension par dimension.
 * Ordre de priorité : réglage de l'utilisateur (`Texte.dimensions`) > ses anciennes étiquettes (`Texte.etiquettes`,
 * réglage antérieur qui remplaçait tout) > classement livré (data/prieres/dimensions-textes.json) > motifs du texte.
 * Une valeur est « devinée » tant que ni l'utilisateur ni une relecture livrée ne l'a confirmée.
 */
import { depuisEtiquettes, dimensionsDevinees } from './etiquettes.ts';
import { DIMENSIONS, type ClassementTexte, type Dimension, type Dimensions } from './programme/types.ts';
import type { Texte } from './types.ts';

export interface DimensionsEffectives {
	valeurs: Dimensions;
	/** Dimensions encore devinées (affichées en gris). */
	devinees: Set<Dimension>;
	/** Date de relecture (de l'utilisateur, ou du classement livré). */
	releve?: string;
}

export function dimensionsEffectives(
	t: Pick<Texte, 'titre' | 'corps' | 'etiquettes' | 'dimensions'>,
	livre?: ClassementTexte
): DimensionsEffectives {
	const valeurs: Dimensions = {};
	const devinees = new Set<Dimension>();
	const anciennes = t.etiquettes ? depuisEtiquettes(t.etiquettes) : null;
	let motifs: Dimensions | undefined;
	for (const d of DIMENSIONS) {
		const perso = t.dimensions?.[d];
		if (perso !== undefined) valeurs[d] = [...perso];
		else if (anciennes) valeurs[d] = anciennes[d] ?? [];
		else if (livre) {
			// un classement livré vaut pour toutes les dimensions : une dimension absente n'a aucune valeur
			valeurs[d] = [...(livre[d] ?? [])];
			if (!livre.releve || livre.devinee?.includes(d)) devinees.add(d);
		} else {
			motifs ??= dimensionsDevinees(t);
			valeurs[d] = motifs[d] ?? [];
			devinees.add(d);
		}
	}
	const releve = t.dimensions?.releve ?? livre?.releve;
	if (t.dimensions?.releve) devinees.clear();
	return { valeurs, devinees, ...(releve && { releve }) };
}

/** Bascule une valeur : le réglage de l'utilisateur remplace, pour cette dimension seulement, ce qui était affiché. */
export function basculerValeur(
	t: Pick<Texte, 'titre' | 'corps' | 'etiquettes' | 'dimensions'>,
	livre: ClassementTexte | undefined,
	d: Dimension,
	v: string
): NonNullable<Texte['dimensions']> {
	const actuelles = dimensionsEffectives(t, livre).valeurs[d] ?? [];
	const nouvelles = actuelles.includes(v) ? actuelles.filter((x) => x !== v) : [...actuelles, v];
	return { ...t.dimensions, [d]: nouvelles };
}

/** « Relu » : toutes les valeurs affichées deviennent celles de l'utilisateur, datées. */
export function marquerRelu(
	t: Pick<Texte, 'titre' | 'corps' | 'etiquettes' | 'dimensions'>,
	livre: ClassementTexte | undefined,
	date: string
): NonNullable<Texte['dimensions']> {
	return { ...dimensionsEffectives(t, livre).valeurs, releve: date };
}
