/** Inventaire du programme : tous les textes qu'il peut donner, sans calculer de journée. */
import type { Choix, Programme, Section } from './types.ts';

/** Les cinq prières de sainte Gertrude au saint du jour (gertrude.ts). */
const GERTRUDE = [
	'gertrude:a-une-vierge',
	'gertrude:a-une-vierge-et-martyre',
	'gertrude:a-un-martyr',
	'gertrude:a-un-confesseur',
	'gertrude:saint-du-jour'
];

/** Tous les textes qu'un choix peut donner. */
export function candidats(c: Choix): string[] {
	if (typeof c === 'string') return [c];
	switch (c.selon) {
		case 'jour_semaine':
			return c.valeurs.filter((v): v is string => !!v);
		case 'rotation':
			return c.parmi;
		case 'quand':
			return [...c.cas.flatMap((x) => candidats(x.texte)), ...(c.sinon ? candidats(c.sinon) : [])];
		case 'saint_du_jour':
			return GERTRUDE;
	}
}

/** Toutes les sections du programme, avec l'entrée (ou la règle du plan) qui les déclare. */
export function sectionsDuProgramme(p: Programme): { ou: string; s: Section }[] {
	return [
		...p.entrees.flatMap((e) => [
			...(e.page?.sections ?? []).map((s) => ({ ou: e.id, s })),
			...(e.lecture?.sections ?? []).map((s) => ({ ou: e.id, s })),
			...(e.insertions ?? []).flatMap((i) => i.sections.map((s) => ({ ou: e.id, s })))
		]),
		...Object.entries(p.plan).flatMap(([cle, r]) => ('sections' in r ? r.sections.map((s) => ({ ou: `plan:${cle}`, s })) : []))
	];
}

/** Ensemble des textes (prières, non les notices) que le programme peut faire dire. */
export function textesDuProgramme(p: Programme): Set<string> {
	const out = new Set<string>();
	for (const { s } of sectionsDuProgramme(p)) if ('texte' in s) for (const id of candidats(s.texte)) out.add(id);
	return out;
}
