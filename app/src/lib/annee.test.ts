import { describe, expect, it } from 'vitest';
import { datesPerso, moisCivils, series, superpositions, temps } from './annee.ts';
import type { Jour } from './calendrier.ts';
import type { FetePerso, Pratique } from './types.ts';

const p = (id: string, regle: Pratique['regle']) => ({ id, titre: id, type: 'devotion', regle, active: true }) as unknown as Pratique;

describe('année liturgique', () => {
	it('découpe les mois civils', () => {
		const m = moisCivils('2026-11-29', '2027-11-27');
		expect(m.length).toBe(13);
		expect(m[0]).toEqual({ an: 2026, mois: 11, debut: '2026-11-29', fin: '2026-11-30' });
		expect(m[12].fin).toBe('2027-11-27');
	});
	it('fond les temps en segments continus', () => {
		const j = (date: string, t: string) => ({ date, temps: t }) as Jour;
		const s = temps([j('2026-12-24', 'Temps de l’Avent'), j('2026-12-25', 'Temps de Noël'), j('2026-12-26', 'Temps de Noël'), j('2027-01-06', 'Temps de l’Épiphanie')]);
		expect(s.map((x) => [x.titre, x.debut, x.fin, x.couleur])).toEqual([
			['Temps de l’Avent', '2026-12-24', '2026-12-24', 'violet'],
			['Temps de Noël', '2026-12-25', '2027-01-05', 'blanc'],
			['Temps de l’Épiphanie', '2027-01-06', '2027-01-06', 'blanc']
		]);
	});
	it('range les séries sur des couloirs et repère les superpositions', () => {
		const neuvaine = p('n', { genre: 'consecutifs', nombre: 9, jourSemaine: null, debut: '2026-12-01' });
		const trentain = p('t', { genre: 'consecutifs', nombre: 30, jourSemaine: null, debut: '2026-12-05' });
		const apres = p('a', { genre: 'consecutifs', nombre: 3, jourSemaine: null, debut: '2026-12-20' });
		const chaqueLundi = p('l', { genre: 'hebdomadaire', jourSemaine: 1 });
		const s = series([neuvaine, trentain, apres, chaqueLundi], '2026-11-29', '2027-11-27');
		expect(s.map((x) => [x.pratique, x.couloir, x.dates.length])).toEqual([['n', 0, 9], ['t', 1, 30], ['a', 0, 3]]);
		const sup = superpositions(s);
		expect(sup.has('2026-12-05')).toBe(true);
		expect(sup.has('2026-12-04')).toBe(false);
		expect(sup.has('2026-12-20')).toBe(true);
	});
	it('place les dates personnelles', () => {
		const f = { id: 'b', titre: 'Baptême', mois: 1, jour: 12, profil: 'bapteme' } as FetePerso;
		expect(datesPerso([f], '2026-11-29', '2027-11-27').map((x) => x.date)).toEqual(['2027-01-12']);
	});
});
