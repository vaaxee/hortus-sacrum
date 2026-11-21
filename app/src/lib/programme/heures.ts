/**
 * Heures d'un office (Petit bréviaire du Sacré-Cœur aujourd'hui ; Bréviaire romain et Officium parvum plus tard) :
 * le texte est découpé selon ses propres titres de niveau 2 (« ## À Matines »…), une heure à la fois à l'écran
 * (SPEC § 11, principe 4 ; REFONTE § 4.3-4.4). Fonctions pures.
 */
import type { Extrait } from './types.ts';
import { normaliser } from './texte.ts';

/** Les heures canoniales, dans l'ordre, avec l'heure du jour à partir de laquelle chacune est proposée à l'ouverture. */
export const HEURES_CANONIALES: { cle: string; nom: string; des: number }[] = [
	{ cle: 'matines', nom: 'Matines', des: 0 },
	{ cle: 'laudes', nom: 'Laudes', des: 6 },
	{ cle: 'prime', nom: 'Prime', des: 7 },
	{ cle: 'tierce', nom: 'Tierce', des: 9 },
	{ cle: 'sexte', nom: 'Sexte', des: 12 },
	{ cle: 'none', nom: 'None', des: 15 },
	{ cle: 'vepres', nom: 'Vêpres', des: 18 },
	{ cle: 'complies', nom: 'Complies', des: 21 }
];

export interface Heure {
	/** « matines »… ; pour une partie qui n'est pas une heure (Recommandation), une clé tirée de son titre. */
	cle: string;
	/** Libellé du bouton (« Matines », « Recommandation »). */
	nom: string;
	/** Le titre tel que le livre l'écrit (« À Matines »). */
	titre: string;
	extrait: Extrait;
	/** Heure canoniale (comptée pour l'office), ou autre partie du texte. */
	canoniale: boolean;
}

/** Les parties d'un office, d'après ses titres de niveau 2. Moins de deux heures canoniales : ce n'est pas un office. */
export function heuresDe(corps: string): Heure[] {
	const out: Heure[] = [];
	for (const m of corps.matchAll(/^## (.+)$/gm)) {
		const titre = m[1].trim();
		const mots = normaliser(titre).split(' ');
		const h = HEURES_CANONIALES.find((x) => mots.includes(normaliser(x.nom)));
		out.push({
			cle: h?.cle ?? mots.join('-'),
			nom: h?.nom ?? titre,
			titre,
			extrait: { section: m[0] },
			canoniale: !!h
		});
	}
	return out.filter((h) => h.canoniale).length >= 2 ? out : [];
}

/** L'heure proposée à l'ouverture : la dernière heure canoniale déjà commencée à cette heure du jour. */
export function heureCourante(heures: Heure[], maintenant: Date): Heure | undefined {
	const h = maintenant.getHours();
	const canoniales = heures.filter((x) => x.canoniale);
	let choisie = canoniales[0];
	for (const x of canoniales) {
		const c = HEURES_CANONIALES.find((y) => y.cle === x.cle);
		if (c && c.des <= h) choisie = x;
	}
	return choisie;
}

/** Identifiant de coche d'une heure : « lec:office:matines ». */
export const cocheDeLHeure = (ligne: string, heure: string) => `${ligne}:${heure}`;
