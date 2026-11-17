import { describe, expect, it } from 'vitest';
import { ecrireRef, enClair, lectureDu, lireRef } from './ecriture.ts';
import type { Pratique } from './types.ts';

describe('références', () => {
	it('lit et récrit', () => {
		expect(lireRef('Mt 5, 3-10')).toEqual({ livre: 'Mt', chapitre: 5, de: 3, a: 10 });
		expect(lireRef('Jn 1')).toEqual({ livre: 'Jn', chapitre: 1, de: undefined, a: undefined });
		expect(lireRef('Xy 20')).toBeUndefined();
		expect(ecrireRef(lireRef('Lc 2, 14')!)).toBe('Lc 2, 14');
		expect(enClair(lireRef('Mt 5, 3-10')!)).toBe('Saint Matthieu, chapitre 5, versets 3 à 10');
		expect(lireRef('1 Co 13, 13')).toEqual({ livre: '1 Co', chapitre: 13, de: 13, a: 13 });
		expect(lireRef('Ps 51 | 50')).toEqual({
			livre: 'Ps',
			chapitre: 51,
			de: undefined,
			a: undefined,
			la: { chapitre: 50, de: undefined, a: undefined }
		});
		expect(ecrireRef(lireRef('Si 7, 36 | 7, 40')!)).toBe('Si 7, 36 | 7, 40');
		expect(enClair(lireRef('Ps 51 | 50')!)).toBe('Les Psaumes, psaume 51 (50)');
	});
});

describe('roue des évangélistes', () => {
	const r = {
		type: 'roue',
		regle: { genre: 'roue', unite: 'jour' },
		elements: [
			{ fr: 'Mt', lecture: 'Mt' },
			{ fr: 'Mc', lecture: 'Mc' },
			{ fr: 'Lc', lecture: 'Lc' },
			{ fr: 'Jn', lecture: 'Jn' }
		]
	} as unknown as Pratique;
	it('chaque évangéliste avance d’un chapitre à chacun de ses tours', () => {
		// premier dimanche de l'Avent 2026 : 29 novembre
		expect(lectureDu(r, '2026-11-29', r.elements![0])).toEqual({ livre: 'Mt', chapitre: 1 });
		expect(lectureDu(r, '2026-12-02', r.elements![3])).toEqual({ livre: 'Jn', chapitre: 1 });
		expect(lectureDu(r, '2026-12-03', r.elements![0])).toEqual({ livre: 'Mt', chapitre: 2 });
		// Marc (16 chapitres) recommence après son 16e tour : jour 1 + 4 × 16 = 65 jours après le départ
		expect(lectureDu(r, '2027-02-02', r.elements![1])).toEqual({ livre: 'Mc', chapitre: 1 });
	});
});
