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
	it('laisse toutes les prières sans alternance, ou avec une seule prière', () => {
		expect(textesDuJour({ textes: ['a', 'b'] }, '2026-11-08')).toEqual(['a', 'b']);
		expect(textesDuJour({ textes: ['a'], alterner: true }, '2026-11-08')).toEqual(['a']);
	});
});
