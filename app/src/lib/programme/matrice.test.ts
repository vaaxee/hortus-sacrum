/**
 * Tests de la matrice dévotionnelle (docs/conception/LOT_DIMENSIONS.md, § 5) : tests 1 et 2 (D1), 3 à 5 (D3). Le test 6
 * (thème de la semaine du mois) reste désactivé : le thème n'est pas adopté.
 * Ils décrivent et vérifient ; ils ne changent rien à la journée calculée.
 */
import { describe, expect, it } from 'vitest';
import { CLE_DE_L_ETIQUETTE, dimensionsDevinees, ETIQUETTES } from '../etiquettes.ts';
import { textesDuProgramme } from './inventaire.ts';
import { DIMENSIONS } from './types.ts';
import { journee } from './journee.ts';
import { CALENDRIER, CLASSEMENTS, corps, CYCLES, dimensions, PLAN, PROGRAMME, TEXTES, VOCABULAIRE } from './donnees-de-test.ts';

const admise = (dim: (typeof DIMENSIONS)[number], v: string) => v in VOCABULAIRE.dimensions[dim].valeurs;

describe('vocabulaire', () => {
	it('déclare les cinq dimensions, et les cinq fins de la SPEC parmi les fins', () => {
		expect(Object.keys(VOCABULAIRE.dimensions).sort()).toEqual([...DIMENSIONS].sort());
		for (const f of VOCABULAIRE.fins_principales) expect(admise('fin', f), f).toBe(true);
		expect(VOCABULAIRE.fins_principales).toHaveLength(5);
	});
	it('chaque étiquette du cadre pratique a sa clé dans le vocabulaire (réglages déjà saisis)', () => {
		for (const [cat, etiquettes] of Object.entries(ETIQUETTES))
			for (const e of etiquettes) {
				const [dim, cle] = CLE_DE_L_ETIQUETTE[e];
				expect(dim, e).toBe(cat);
				expect(admise(dim, cle), `${e} → ${dim}:${cle}`).toBe(true);
			}
	});
	it('les motifs ne devinent que des valeurs du vocabulaire', () => {
		for (const t of TEXTES.values()) {
			const d = dimensionsDevinees(t);
			for (const dim of DIMENSIONS) for (const v of d[dim] ?? []) expect(admise(dim, v), `${t.id} → ${dim}:${v}`).toBe(true);
		}
	});
});

describe('classement des textes du programme', () => {
	const ids = [...textesDuProgramme(PROGRAMME)].filter((id) => TEXTES.has(id));

	it('test 1 : chaque texte du programme a des dimensions déclarées (avertit tant qu’il n’est pas relu)', () => {
		const sans = ids.filter((id) => !DIMENSIONS.some((d) => CLASSEMENTS[id]?.[d]?.length));
		expect(sans).toEqual([]);
		const nonRelus = ids.filter((id) => !CLASSEMENTS[id]?.releve);
		if (nonRelus.length) console.warn(`matrice : ${nonRelus.length} textes du programme sur ${ids.length} restent à relire (D2).`);
	});

	it('test 2 : chaque valeur citée existe dans le vocabulaire', () => {
		const inconnues: string[] = [];
		for (const [id, c] of Object.entries(CLASSEMENTS)) {
			for (const dim of DIMENSIONS) for (const v of c[dim] ?? []) if (!admise(dim, v)) inconnues.push(`${id} → ${dim}:${v}`);
			for (const dim of c.devinee ?? []) if (!DIMENSIONS.includes(dim)) inconnues.push(`${id} → devinee:${dim}`);
		}
		expect(inconnues).toEqual([]);
	});
});

// ------------------------------------------------------------------ tests 3 à 5 (D3) : ils signalent, ils ne modifient rien

const ANNEE = CALENDRIER.map((jour) =>
	journee(PROGRAMME, { jour, pratiques: PLAN, corps, cycles: CYCLES, dimensions, vocabulaire: VOCABULAIRE })
);

describe(`matrice sur ${ANNEE.length} jours`, () => {
	it('la matrice ne change aucune ligne : la journée est la même avec ou sans dimensions', () => {
		for (const j of ANNEE.filter((_, i) => i % 7 === 0)) {
			const sans = journee(PROGRAMME, { jour: CALENDRIER.find((x) => x.date === j.date)!, pratiques: PLAN, corps });
			expect(j.lignes, j.date).toEqual(sans.lignes);
			expect(j.lectures, j.date).toEqual(sans.lectures);
		}
	});

	it('test 3 : chaque jour, les objets du contexte sont couverts par au moins une ligne', () => {
		const trous = ANNEE.flatMap((j) =>
			j.contexte.objets
				.filter((o) => !j.couverture.objet.some((c) => c.valeur === o))
				.map((o) => `${j.date} ${o} ← ${j.contexte.sources.find((s) => s.valeur === o)?.de}`)
		);
		expect(trous).toEqual([]);
	});

	it('test 4 : chaque semaine couvre les cinq fins principales de la SPEC', () => {
		const trous: string[] = [];
		for (let i = 0; i + 7 <= ANNEE.length; i += 7) {
			const semaine = ANNEE.slice(i, i + 7);
			const fins = new Set(semaine.flatMap((j) => j.couverture.fin.map((c) => c.valeur)));
			for (const f of VOCABULAIRE.fins_principales) if (!fins.has(f)) trous.push(`semaine du ${semaine[0].date} : ${f}`);
		}
		expect(trous).toEqual([]);
	});

	it('test 5 : le motif d’une entrée a au moins une fin commune avec ses textes', () => {
		const contradictions: string[] = [];
		for (const e of PROGRAMME.entrees as ((typeof PROGRAMME.entrees)[number] & { motif?: { fins?: string[] } })[]) {
			if (!e.motif?.fins?.length) continue;
			// les fins des textes que l'entrée apporte elle-même (dans sa page ou chez son hôte)
			const fins = new Set(
				ANNEE.flatMap((j) =>
					[...j.lignes, ...j.lectures].flatMap((l) =>
						l.sections.filter((s) => s.origine === e.id && s.texte).flatMap((s) => dimensions(s.texte!)?.fin ?? [])
					)
				)
			);
			if (!e.motif.fins.some((f) => fins.has(f))) contradictions.push(`${e.id} : ${e.motif.fins.join(', ')}`);
		}
		expect(contradictions).toEqual([]);
	});
});
