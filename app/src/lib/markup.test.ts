import { describe, expect, it } from 'vitest';
import { nettoyer, rendre } from './markup';

describe('rendre', () => {
	it('échappe le HTML et rend le balisage', () => {
		const h = rendre('[r]Rubrique.[/r]\n\n℣. Verset <b>\n℟. *Répons*');
		expect(h).toContain('<span class="rub">Rubrique.</span>');
		expect(h).toContain('&lt;b&gt;');
		expect(h).toContain('<span class="vr">℣.</span>');
		expect(h).toContain('<em>Répons</em>');
	});
});

describe('nettoyer', () => {
	it('recolle les mots coupés et les lignes d’un paragraphe', () => {
		const brut =
			'Mon Dieu, je vous offre toutes les œuvres de cette jour-\nnée, dans l’intention de vous glorifier, de réparer mes\npéchés  et de satisfaire pour les âmes du purgatoire.';
		const { texte, rapport } = nettoyer(brut);
		expect(texte).toBe(
			'Mon Dieu, je vous offre toutes les œuvres de cette journée, dans l’intention de vous glorifier, de réparer mes péchés et de satisfaire pour les âmes du purgatoire.'
		);
		expect(rapport.length).toBeGreaterThan(0);
	});

	it('reconnaît ℣ et ℟ et garde une ligne par verset', () => {
		const { texte } = nettoyer('V. Priez pour nous, sainte Mère de Dieu.\nR. Afin que nous devenions dignes\ndes promesses de Jésus-Christ.');
		expect(texte).toBe('℣. Priez pour nous, sainte Mère de Dieu.\n℟. Afin que nous devenions dignes des promesses de Jésus-Christ.');
	});

	it('garde les vers et les litanies ligne à ligne', () => {
		const { texte } = nettoyer('Ave, maris stella,\nDei Mater alma,\natque semper Virgo,\nfelix cæli porta.');
		expect(texte.split('\n')).toHaveLength(4);
	});

	it('détache une ligne de titre collée au paragraphe', () => {
		const { texte } = nettoyer(
			'Essai de collage\nCeci est un texte d’essai, coupé en fin de li-\ngne comme dans un PDF, avec des retours parasites\nau milieu des phrases, sur plusieurs lignes.'
		);
		expect(texte.split('\n\n')[0]).toBe('Essai de collage');
	});

	it('un V. seul reste un chiffre romain', () => {
		const { texte } = nettoyer('V. Cinquième point de la liste.\nVI. Sixième point de la liste.');
		expect(texte).not.toContain('℣');
	});

	it('ne change aucun mot', () => {
		const brut = 'Ô Jésus ! vraie joie des Anges, Paradis de délices.';
		expect(nettoyer(brut).texte.replace(/ /g, ' ')).toBe(brut);
	});
});
