/**
 * Parties de la bibliothèque (lot 7) : les parties qui se recouvraient (« Couronnes et chapelets », « Chapelet et
 * Rosaire », « Rosaire » ; « Prières à la Sainte Vierge », « Sainte Vierge », « Antiennes à la Sainte Vierge » ;
 * « Consécrations » et « Consécration à Jésus par Marie » ; « Prières à saint Joseph » et le cordon rangé sous
 * « Dévotions »…) sont réunies. La correspondance vaut pour les textes déjà en base et pour le livret, sans les modifier.
 */
import type { Texte } from './types.ts';

/** Partie d'origine (données, livret, réglage ancien) → partie affichée. */
export const PARTIE_REUNIE: Record<string, string> = {
	'Chapelet et Rosaire': 'Couronnes et chapelets',
	Rosaire: 'Couronnes et chapelets',
	'Sainte Vierge': 'Prières à la Sainte Vierge',
	'Antiennes à la Sainte Vierge': 'Prières à la Sainte Vierge',
	Consécrations: 'Consécration à Jésus par Marie',
	'Prières à saint Joseph': 'Saint Joseph',
	Passion: 'Passion et réparation',
	'Prières de réparation': 'Passion et réparation'
};

/** Pièces de l'ancienne partie « Dévotions » (fourre-tout) : chacune rejoint sa partie. */
const PAR_TEXTE: Record<string, string> = {
	'beringer:chapelet-des-morts': 'Couronnes et chapelets',
	'beringer:cordon-saint-joseph': 'Saint Joseph',
	'beringer:saint-joseph-purete': 'Saint Joseph',
	'beringer:coeur-afflige-de-marie': 'Prières à la Sainte Vierge'
};

/** Ordre d'affichage : la journée (matin, offrande), puis les grandes dévotions ; les autres parties suivent. */
export const ORDRE_DES_PARTIES = [
	'Prières du matin et du soir',
	'Offrande du matin',
	'Actes des devoirs de charité',
	'Apostolat de la prière',
	'Consécration à Jésus par Marie',
	'Prières à la Sainte Vierge',
	'Couronnes et chapelets',
	'Litanies',
	'Saint Joseph',
	'Passion et réparation',
	'Sainte Face',
	'Hymnes',
	'Dons du Saint-Esprit',
	'Neuvaines',
	'Dévotions à jours comptés',
	'Actions de grâces',
	'Petit bréviaire du Sacré-Cœur',
	'Prières de sainte Gertrude',
	'Jaculatoires indulgenciées'
];

export function partieDe(t: Pick<Texte, 'id' | 'partie'>): string {
	const p = t.partie?.trim() || 'Sans partie';
	if (p === 'Dévotions' && PAR_TEXTE[t.id]) return PAR_TEXTE[t.id];
	return PARTIE_REUNIE[p] ?? p;
}

export function rangDeLaPartie(p: string): number {
	const i = ORDRE_DES_PARTIES.indexOf(p);
	return i < 0 ? ORDRE_DES_PARTIES.length : i;
}
