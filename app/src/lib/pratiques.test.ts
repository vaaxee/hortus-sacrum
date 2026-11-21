import { describe, expect, it } from 'vitest';
import { etat, occurrences, recommencer, regleEnClair } from './pratiques.ts';
import type { Pratique, Regle } from './types.ts';

const dates = (r: Regle, de: string, a: string) => occurrences(r, de, a).map((o) => o.date);
const pratique = (regle: Regle): Pratique => ({
	id: 'p',
	origine: 'personnel',
	titre: 'Essai',
	type: 'jours_comptes',
	regle,
	textes: [],
	promesses: '',
	indulgence: '',
	source: { ouvrage: '', edition: '', page: '', url: '' },
	notes: '',
	active: true,
	creeLe: '',
	modifieLe: ''
});

describe('occurrences', () => {
	it('sept dimanches avant le 19 mars 2027 (plan accepté : 31 janv. – 14 mars)', () => {
		const r: Regle = { genre: 'avant_fete', nombre: 7, jourSemaine: 0, mois: 3, jour: 19 };
		const d = dates(r, '2027-01-01', '2027-12-31');
		expect(d[0]).toBe('2027-01-31');
		expect(d[6]).toBe('2027-03-14');
		expect(d).toHaveLength(7);
	});
	it('neuvaine : les neuf jours avant le 8 décembre', () => {
		const r: Regle = { genre: 'avant_fete', nombre: 9, jourSemaine: null, mois: 12, jour: 8 };
		expect(dates(r, '2026-11-01', '2026-12-31')).toEqual([
			'2026-11-29',
			'2026-11-30',
			'2026-12-01',
			'2026-12-02',
			'2026-12-03',
			'2026-12-04',
			'2026-12-05',
			'2026-12-06',
			'2026-12-07'
		]);
	});
	it('treize mardis de suite à partir du 16 mars 2027 (finit le 8 juin)', () => {
		const r: Regle = { genre: 'consecutifs', nombre: 13, jourSemaine: 2, debut: '2027-03-16' };
		const o = occurrences(r, '2027-01-01', '2027-12-31');
		expect(o[0]).toEqual({ date: '2027-03-16', rang: 1, total: 13 });
		expect(o[12].date).toBe('2027-06-08');
	});
	it('neuf premiers vendredis à partir de décembre 2026', () => {
		const r: Regle = { genre: 'mensuel', rang: 1, jourSemaine: 5, nombre: 9, debut: '2026-12-04' };
		const d = dates(r, '2026-11-01', '2027-12-31');
		expect(d.slice(0, 3)).toEqual(['2026-12-04', '2027-01-01', '2027-02-05']);
		expect(d).toHaveLength(9);
		expect(d[8]).toBe('2027-08-06');
	});
	it('veille du premier vendredi (Heure sainte)', () => {
		const r: Regle = { genre: 'mensuel', rang: 1, jourSemaine: 5, decalage: -1 };
		// le 31 décembre est la veille du premier vendredi de janvier 2027
		expect(dates(r, '2026-12-01', '2026-12-31')).toEqual(['2026-12-03', '2026-12-31']);
	});
	it('trentain : trente jours de suite', () => {
		const r: Regle = { genre: 'consecutifs', nombre: 30, jourSemaine: null, debut: '2026-11-13' };
		const o = occurrences(r, '2026-11-01', '2026-12-31');
		expect(o).toHaveLength(30);
		expect(o[29]).toEqual({ date: '2026-12-12', rang: 30, total: 30 });
	});
});

describe('etat', () => {
	const r: Regle = { genre: 'consecutifs', nombre: 9, jourSemaine: null, debut: '2026-11-10' };
	it('compte les jours faits et repère les jours manqués', () => {
		const e = etat(pratique(r), '2026-11-13', new Set(['2026-11-10', '2026-11-12']));
		expect(e.phase).toBe('en_cours');
		expect(e.faites).toBe(2);
		expect(e.manquees.map((o) => o.date)).toEqual(['2026-11-11']);
		expect(e.prochaine?.rang).toBe(4);
	});
	it('pas de jour manqué avant le premier jour coché', () => {
		expect(etat(pratique(r), '2026-11-13', new Set()).manquees).toEqual([]);
		expect(etat(pratique(r), '2026-11-13', new Set(['2026-11-11'])).manquees.map((o) => o.date)).toEqual(['2026-11-12']);
	});
	it('série à venir, puis terminée', () => {
		expect(etat(pratique(r), '2026-11-01', new Set()).phase).toBe('a_venir');
		expect(etat(pratique(r), '2026-11-10', new Set()).phase).toBe('en_cours'); // premier jour : encore à temps
		expect(etat(pratique(r), '2026-12-01', new Set()).phase).toBe('terminee');
	});
	it('recommencer repart d’aujourd’hui', () => {
		const n = recommencer(r, '2026-11-13');
		expect(occurrences(n, '2026-11-01', '2026-12-31')[0].date).toBe('2026-11-13');
	});
});

describe('regleEnClair', () => {
	it('dit la règle en français', () => {
		expect(regleEnClair({ genre: 'avant_fete', nombre: 7, jourSemaine: 0, mois: 3, jour: 19 })).toBe('les 7 dimanches avant le 19 mars');
		expect(regleEnClair({ genre: 'mensuel', rang: 1, jourSemaine: 5 })).toBe('le premier vendredi de chaque mois');
	});
});

describe('données anciennes ou incomplètes', () => {
	it('une règle absente ou sans jour de semaine valide ne plante ni ne boucle', async () => {
		const { occurrences } = await import('./pratiques.ts');
		expect(occurrences(undefined, '2026-01-01', '2026-12-31')).toEqual([]);
		const r = { genre: 'avant_fete', mois: 12, jour: 8, nombre: 9 } as unknown as Parameters<typeof occurrences>[0];
		expect(() => occurrences(r, '2026-01-01', '2026-12-31')).not.toThrow();
	});
});

describe('série jamais commencée (audit du 20 nov.)', () => {
	// « Douze samedis avant l'Immaculée Conception » : la série du plan s'ouvre le 19 septembre 2026
	const r: Regle = { genre: 'avant_fete', nombre: 12, jourSemaine: 6, mois: 12, jour: 8 };
	it('ouverte depuis septembre, aucune coche : non commencée, pas en cours', () => {
		const e = etat(pratique(r), '2026-11-20', new Set());
		expect(e.serie[0].date).toBe('2026-09-19');
		expect(e.faites).toBe(0);
		expect(e.phase).toBe('non_commencee');
		expect(e.manquees).toEqual([]);
	});
	it('un seul samedi coché suffit : en cours', () => {
		expect(etat(pratique(r), '2026-11-20', new Set(['2026-11-14'])).phase).toBe('en_cours');
	});
	it('le premier jour, rien n’est encore manqué : en cours', () => {
		expect(etat(pratique(r), '2026-09-19', new Set()).phase).toBe('en_cours');
	});
});
