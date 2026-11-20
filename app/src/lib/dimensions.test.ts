import { describe, expect, it } from 'vitest';
import { contenu } from './db.ts';
import { basculerValeur, dimensionsEffectives, marquerRelu } from './dimensions.ts';
import type { ClassementTexte } from './programme/types.ts';
import type { Texte } from './types.ts';

const texte = (x: Partial<Texte> = {}) =>
	({ id: 't', titre: 'Litanies de saint Joseph', corps: 'Joseph très chaste, priez pour nous.', ...x }) as Texte;
const LIVRE: ClassementTexte = { fin: ['louange'], objet: ['saint-joseph'], forme: ['litanie'], devinee: ['fin', 'objet', 'forme'] };

describe('dimensions d’un texte', () => {
	it('sans classement livré : les motifs du texte, tous devinés', () => {
		const e = dimensionsEffectives(texte());
		expect(e.valeurs.objet).toContain('saint-joseph');
		expect(e.devinees.has('objet')).toBe(true);
	});
	it('classement livré non relu : ses valeurs, devinées', () => {
		const e = dimensionsEffectives(texte(), LIVRE);
		expect(e.valeurs.fin).toEqual(['louange']);
		expect([...e.devinees].sort()).toEqual(['fin', 'forme', 'grace', 'objet', 'personne']);
		expect(e.valeurs.grace).toEqual([]);
	});
	it('classement livré relu : plus rien de deviné pour les dimensions relues', () => {
		const e = dimensionsEffectives(texte(), { ...LIVRE, releve: '2026-11-21', devinee: [] });
		expect(e.devinees.size).toBe(0);
		expect(e.releve).toBe('2026-11-21');
	});
	it('le réglage de l’utilisateur prime, dimension par dimension', () => {
		const t = texte({ dimensions: { fin: ['demande'] } });
		const e = dimensionsEffectives(t, LIVRE);
		expect(e.valeurs.fin).toEqual(['demande']);
		expect(e.devinees.has('fin')).toBe(false);
		expect(e.valeurs.objet).toEqual(['saint-joseph']); // pas réglée : la donnée livrée
		expect(e.devinees.has('objet')).toBe(true);
	});
	it('les anciennes étiquettes de l’utilisateur remplacent tout le classement livré', () => {
		const e = dimensionsEffectives(texte({ etiquettes: ['famille', 'litanies'] }), LIVRE);
		expect(e.valeurs).toMatchObject({ personne: ['famille'], forme: ['litanie'], fin: [] });
		expect(e.devinees.size).toBe(0);
	});
	it('basculer une valeur, puis marquer relu', () => {
		const t = texte();
		t.dimensions = basculerValeur(t, LIVRE, 'fin', 'demande');
		expect(dimensionsEffectives(t, LIVRE).valeurs.fin).toEqual(['louange', 'demande']);
		t.dimensions = marquerRelu(t, LIVRE, '2026-11-21');
		const e = dimensionsEffectives(t, LIVRE);
		expect(e.devinees.size).toBe(0);
		expect(e.valeurs.forme).toEqual(['litanie']);
	});
	it('classer un texte ne le rend pas « modifié » (il garde les corrections livrées)', () => {
		const t = { ...texte(), origine: 'officielle', creeLe: '', modifieLe: '' } as Texte;
		expect(contenu({ ...t, dimensions: { fin: ['demande'] }, etiquettes: ['famille'] })).toBe(contenu(t));
	});
});
