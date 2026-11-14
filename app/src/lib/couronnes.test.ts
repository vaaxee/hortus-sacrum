import { describe, expect, it } from 'vitest';
import { couronnes } from './couronnes.ts';
import type { Coche, ElementListe, Fait, Pratique } from './types.ts';

const samedis = { id: 's', titre: 'Premiers samedis du mois', type: 'jours_comptes', promesses: '', active: true,
	regle: { genre: 'mensuel', rang: 1, jourSemaine: 6, nombre: 5, debut: '2027-01-01' } } as unknown as Pratique;
const fait = (date: string, pratiqueId = 's') => ({ pratiqueId, date, horodatage: '' }) as Fait;
const PREMIERS = ['2027-01-02', '2027-02-06', '2027-03-06', '2027-04-03', '2027-05-01'];

describe('couronnes', () => {
	it('une série achevée sans manquer de jour donne une couronne, avec la grâce attachée', () => {
		const c = couronnes({ pratiques: [samedis], faits: PREMIERS.map((d) => fait(d)), liste: [], coches: [], aujourdhui: '2027-06-01' });
		expect(c).toHaveLength(1);
		expect(c[0].titre).toBe('Enfant du Cœur Immaculé');
		expect(c[0].date).toBe('2027-05-01');
		expect(c[0].quete).toBe('Premiers samedis du mois, 5 sur 5');
		expect(c[0].promesse).toMatch(/Pontevedra, 10 décembre 1925/); // cinq samedis : la promesse de Fatima
	});
	it('un jour manqué : pas de couronne', () => {
		const c = couronnes({ pratiques: [samedis], faits: PREMIERS.filter((d) => d !== '2027-03-06').map((d) => fait(d)), liste: [], coches: [], aujourdhui: '2027-06-01' });
		expect(c).toHaveLength(0);
	});
	it('la promesse inscrite dans la pratique passe avant', () => {
		const c = couronnes({ pratiques: [{ ...samedis, promesses: 'Ma promesse.' }], faits: PREMIERS.map((d) => fait(d)), liste: [], coches: [], aujourdhui: '2027-06-01' });
		expect(c[0].promesse).toBe('Ma promesse.');
	});
	it('mois entier et constance', () => {
		const mois = { id: 'm', titre: 'Dévotion du mois', jours: Array(7).fill(true) } as ElementListe;
		const jours: Coche[] = [];
		for (let k = 0; k < 45; k++) {
			const d = new Date(2027, 4, 1 + k, 12);
			jours.push({ elementId: 'm', date: `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`, rang: 0, horodatage: '' });
		}
		const c = couronnes({ pratiques: [], faits: [], liste: [mois], coches: jours, aujourdhui: '2027-07-01' });
		expect(c.map((x) => x.titre).sort()).toEqual(['Compagnon du désert', 'Fleur du mois de Marie']);
	});
	it('un Évangile lu en entier', () => {
		const coches = Array.from({ length: 16 }, (_, i) => ({ elementId: `lecture:Mc ${i + 1}`, date: '2027-01-0' + ((i % 9) + 1), rang: 0, horodatage: '' }));
		const c = couronnes({ pratiques: [], faits: [], liste: [], coches, aujourdhui: '2027-02-01' });
		expect(c.map((x) => x.titre)).toEqual(['Disciple de saint Marc']);
	});
});
