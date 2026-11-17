import { describe, expect, it } from 'vitest';
import { semaineDuMois, textesDuJour } from './liste.ts';

describe('alternance par semaine du mois', () => {
	it('compte les semaines du mois', () => {
		expect(semaineDuMois('2026-11-01')).toBe(1);
		expect(semaineDuMois('2026-11-07')).toBe(1);
		expect(semaineDuMois('2026-11-08')).toBe(2);
		expect(semaineDuMois('2026-11-29')).toBe(5);
	});
	it('prend une prière à tour de rôle, et recommence à la 5e semaine', () => {
		const e = { textes: ['a', 'b'], alterner: true };
		expect(textesDuJour(e, '2026-11-01')).toEqual(['a']);
		expect(textesDuJour(e, '2026-11-08')).toEqual(['b']);
		expect(textesDuJour(e, '2026-11-15')).toEqual(['a']);
		expect(textesDuJour(e, '2026-11-29')).toEqual(['a']);
	});
	it('remplace l’Angélus par le Regina cæli au temps pascal, et montre les deux le samedi saint', () => {
		const e = { textes: ['paroissien:angelus'] };
		expect(textesDuJour(e, '2027-04-10', { temps: 'Temps pascal', office: 'x' })).toEqual(['beringer:regina-caeli']);
		expect(textesDuJour(e, '2027-03-27', { temps: 'Temps de la Passion', office: 'Samedi saint' })).toEqual(['paroissien:angelus', 'beringer:regina-caeli']);
		expect(textesDuJour(e, '2027-06-10', { temps: 'Temps après la Pentecôte', office: 'x' })).toEqual(['paroissien:angelus']);
	});
	it('laisse toutes les prières sans alternance, ou avec une seule prière', () => {
		expect(textesDuJour({ textes: ['a', 'b'] }, '2026-11-08')).toEqual(['a', 'b']);
		expect(textesDuJour({ textes: ['a'], alterner: true }, '2026-11-08')).toEqual(['a']);
	});
});

describe('petit bréviaire du Sacré-Cœur', () => {
	it("donne l'office du jour de la semaine", async () => {
		const { petitBreviaireDuJour, PETIT_BREVIAIRE_DU_JOUR } = await import('./liste');
		expect(petitBreviaireDuJour(['a', PETIT_BREVIAIRE_DU_JOUR, 'b'], '2026-11-20')).toEqual(['a', 'breviaire-sc:office-vendredi', 'b']);
		expect(petitBreviaireDuJour([PETIT_BREVIAIRE_DU_JOUR], '2026-11-22')).toEqual(['breviaire-sc:office-dimanche']);
		expect(petitBreviaireDuJour(['a'], '2026-11-22')).toEqual(['a']);
	});
});
