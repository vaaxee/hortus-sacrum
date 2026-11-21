/**
 * Compositeur d'ordo (LOT_DIMENSIONS § 6-7, lot D5) : critère du lot, sur l'Avent 2026 — aucun candidat n'est déjà dit
 * ce jour-là ; et chaque candidat est sourcé, porte la valeur manquante, n'est contenu dans aucun texte du jour.
 */
import { describe, expect, it } from 'vitest';
import { dimensionsEffectives } from '../dimensions.ts';
import { journee } from './journee.ts';
import { ordoDuJour, rapportOrdo } from './ordo.ts';
import { fragments, normaliser, partIncluse } from './texte.ts';
import { CALENDRIER, CLASSEMENTS, corps, CYCLES, dimensions, PLAN, PROGRAMME, TEXTES, VOCABULAIRE } from './donnees-de-test.ts';

const AVENT = CALENDRIER.filter((j) => j.date >= '2026-11-29' && j.date <= '2026-12-24');
const biblio = () => ({
	textes: TEXTES.values(),
	dimensions: (t: Parameters<typeof dimensionsEffectives>[0] & { id: string }) => dimensionsEffectives(t, CLASSEMENTS[t.id]),
	formules: PROGRAMME.formules
});
const JOURNEES = AVENT.map((jour) => ({
	jour,
	j: journee(PROGRAMME, { jour, pratiques: PLAN, corps, cycles: CYCLES, dimensions, vocabulaire: VOCABULAIRE })
}));
const ORDO = JOURNEES.map(({ jour, j }) => ({ j, o: ordoDuJour(j, jour.office, biblio()) }));
const FORMULES = PROGRAMME.formules.map(normaliser);

describe(`compositeur d'ordo sur l'Avent 2026 (${AVENT.length} jours)`, () => {
	it('propose des candidats (le rapport n’est pas vide)', () => {
		expect(ORDO.some(({ o }) => o.manques.some((m) => m.candidats.length))).toBe(true);
	});

	it('aucun candidat n’est déjà dit ce jour-là', () => {
		const deja = ORDO.flatMap(({ j, o }) =>
			o.manques.flatMap((m) => m.candidats.filter((c) => j.textes.has(c.texte)).map((c) => `${o.date} ${c.texte}`))
		);
		expect(deja).toEqual([]);
	});

	it('aucun candidat n’est contenu dans un texte du jour, ni ne le contient', () => {
		const inclus: string[] = [];
		for (const { j, o } of ORDO) {
			const dits = [...j.textes.keys()].map((id) => fragments(corps(id) ?? '', FORMULES));
			for (const c of new Set(o.manques.flatMap((m) => m.candidats.map((x) => x.texte)))) {
				const f = fragments(corps(c) ?? '', FORMULES);
				if (dits.some((g) => partIncluse(f, g) >= 1 / 3 || partIncluse(g, f) >= 1 / 3)) inclus.push(`${o.date} ${c}`);
			}
		}
		expect(inclus).toEqual([]);
	});

	it('chaque candidat est sourcé et porte la valeur manquante', () => {
		const fautes: string[] = [];
		for (const { o } of ORDO)
			for (const m of o.manques)
				for (const c of m.candidats) {
					const t = TEXTES.get(c.texte)!;
					if (!t.source?.ouvrage) fautes.push(`${c.texte} : sans source`);
					const d = dimensionsEffectives(t, CLASSEMENTS[t.id]).valeurs[m.dimension] ?? [];
					if (!d.includes(m.valeur)) fautes.push(`${c.texte} : ne porte pas ${m.dimension}:${m.valeur}`);
				}
		expect(fautes).toEqual([]);
	});

	it('chaque manque est une valeur du vocabulaire que la journée ne porte pas', () => {
		for (const { j, o } of ORDO)
			for (const m of o.manques) {
				expect(m.valeur in VOCABULAIRE.dimensions[m.dimension].valeurs).toBe(true);
				expect(j.couverture[m.dimension].some((c) => c.valeur === m.valeur)).toBe(false);
			}
	});

	it('déterministe : deux passages donnent le même rapport', () => {
		const libelle = (d: keyof typeof VOCABULAIRE.dimensions, v: string) => VOCABULAIRE.dimensions[d].valeurs[v] ?? v;
		const a = rapportOrdo(
			ORDO.map(({ o }) => o),
			libelle
		);
		const b = rapportOrdo(
			JOURNEES.map(({ jour, j }) => ordoDuJour(j, jour.office, biblio())),
			libelle
		);
		expect(a).toBe(b);
	});
});
