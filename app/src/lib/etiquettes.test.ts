import { describe, expect, it } from 'vitest';
import { bilanDuJour, etiquettesDe } from './etiquettes.ts';
import type { Texte } from './types.ts';

const t = (id: string, titre: string, corps: string, etiquettes?: string[]) =>
	({
		id,
		titre,
		corps,
		etiquettes,
		partie: '',
		categorie: '',
		latin: '',
		usage: '',
		indulgence: '',
		ordre: 0,
		creeLe: '',
		modifieLe: ''
	}) as unknown as Texte;

describe('cadre pratique', () => {
	it('déduit les étiquettes du texte', () => {
		const e = etiquettesDe(
			t(
				'a',
				'Prière pour les agonisants',
				'Ô très miséricordieux Jésus… purifiez dans votre sang les pécheurs du monde entier qui sont à l’agonie'
			)
		);
		expect(e).toContain('Jésus-Christ');
		expect(e).toContain('pécheurs');
		expect(e).toContain('mourants');
	});
	it('les étiquettes de l’utilisateur remplacent celles qui sont déduites', () => {
		expect(etiquettesDe(t('a', 'Litanies', 'priez pour nous', ['famille']))).toEqual(['famille']);
	});
	it('fait le bilan du jour et propose la prière la plus courte pour un manque', () => {
		const bib = [
			t('a', 'Acte d’adoration', 'Je vous adore'),
			t('b', 'Pour les défunts', 'Requiem pour les défunts du purgatoire, longue prière'),
			t('c', 'Défunts', 'De profundis, défunts')
		];
		const b = bilanDuJour(['a'], bib);
		const fins = b.find((x) => x.categorie === 'fin')!;
		expect(fins.couvertes).toEqual(['adoration']);
		const pers = b.find((x) => x.categorie === 'personne')!;
		expect(pers.manques.find((m) => m.etiquette === 'défunts')?.proposition?.id).toBe('c');
	});
});
