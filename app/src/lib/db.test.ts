import { describe, expect, it } from 'vitest';
import { contenu, estModifie } from './db.ts';
import type { ElementListe } from './types.ts';

const base: ElementListe = {
	id: 'liste:1', origine: 'officielle', titre: 'Offrande du matin', moment: 'matin', etiquette: 'ordinaire',
	ordre: 10, jours: [true, true, true, true, true, true, true], rappels: [], textes: [], actif: true,
	creeLe: '2026-11-12', modifieLe: '2026-11-12'
};

describe('estModifie', () => {
	it('un changement de rang ne compte pas', () => {
		const o = { ...base, original: contenu(base), ordre: 40 };
		expect(estModifie(o)).toBe(false);
	});
	it('un changement de titre compte', () => {
		const o = { ...base, original: contenu(base), titre: 'Autre titre' };
		expect(estModifie(o)).toBe(true);
	});
	it('un ajout personnel n’a pas d’original', () => {
		expect(estModifie({ ...base, origine: 'personnel' })).toBe(false);
	});
});
