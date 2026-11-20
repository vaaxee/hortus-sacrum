/**
 * Tests de la matrice dévotionnelle (docs/conception/LOT_DIMENSIONS.md, § 5). Lot D1 : tests 1 et 2.
 * Ils décrivent et vérifient ; ils ne changent rien à la journée calculée.
 */
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CLE_DE_L_ETIQUETTE, dimensionsDevinees, ETIQUETTES } from '../etiquettes.ts';
import { textesDuProgramme } from './inventaire.ts';
import { DIMENSIONS, type ClassementTexte, type Vocabulaire } from './types.ts';
import { PROGRAMME, TEXTES } from './donnees-de-test.ts';

const lire = <T>(chemin: string): T => JSON.parse(readFileSync(new URL(`../../../../data/${chemin}`, import.meta.url), 'utf-8')) as T;
const VOCABULAIRE = lire<Vocabulaire>('programme/dimensions.json');
const CLASSEMENTS = lire<{ textes: Record<string, ClassementTexte> }>('prieres/dimensions-textes.json').textes;
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
