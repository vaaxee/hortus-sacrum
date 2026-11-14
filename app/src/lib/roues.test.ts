import { describe, expect, it } from 'vitest';
import { debutAnnee, grandCycle, pas, position, premierDimancheAvent } from './roues.ts';
import type { Pratique } from './types.ts';

const iso = (d: Date) => d.toLocaleDateString('sv');
const roue = (n: number, unite: 'jour' | 'semaine' | 'mois' = 'jour') =>
	({ regle: { genre: 'roue', unite }, elements: Array.from({ length: n }, (_, i) => ({ fr: String(i) })) }) as unknown as Pratique;

describe('roues symboliques', () => {
	it('premier dimanche de l’Avent', () => {
		expect(iso(premierDimancheAvent(2024))).toBe('2024-12-01');
		expect(iso(premierDimancheAvent(2025))).toBe('2025-11-30');
		expect(iso(premierDimancheAvent(2026))).toBe('2026-11-29');
		expect(iso(premierDimancheAvent(2028))).toBe('2028-12-03');
	});
	it('l’année liturgique commence à l’Avent', () => {
		expect(iso(debutAnnee('2026-11-28'))).toBe('2025-11-30');
		expect(iso(debutAnnee('2026-11-29'))).toBe('2026-11-29');
	});
	it('toutes les roues sont alignées le premier jour, puis avancent d’un cran', () => {
		for (const n of [3, 4, 7, 12]) expect(position(roue(n), '2026-11-29')).toBe(0);
		expect(position(roue(3), '2026-11-30')).toBe(1);
		expect(position(roue(7), '2026-12-06')).toBe(0);
		expect(position(roue(4, 'semaine'), '2026-12-13')).toBe(2);
		expect(pas('2027-01-10', 'mois')).toBe(2);
	});
	it('grand cycle de 3, 4, 7 et 12 : 84 jours', () => {
		expect(grandCycle([3, 4, 7, 12])).toBe(84);
	});
});
