import { describe, expect, it } from 'vitest';
import { clesDuJour, entreesDuJour, type Recueil } from './meditations.ts';

const r: Recueil = {
	id: 'x', titre: '', auteur: '', editions: {}, provenance: '',
	entrees: [
		{ cle: 'T:Adv1-5', titre: 'Règne de Jésus-Christ en nous', tome: 1, page: 18, corps: '' },
		{ cle: 'D:12-08', titre: 'Immaculée Conception', tome: 1, page: 409, corps: '' },
		{ cle: 'T:Adv2-2', titre: 'Décret du mode', tome: 1, page: 30, corps: '' },
		{ cle: 'F:sacre-coeur', titre: 'Première méditation', tome: 2, page: 397, corps: '' },
		{ cle: 'F:sacre-coeur', titre: 'Deuxième méditation', tome: 2, page: 401, corps: '' }
	]
};

describe('méditation du jour', () => {
	it('prend le jour du temporal', () => {
		expect(entreesDuJour(r, '2026-12-04', { tempora: 'Adv1-5' }).map((e) => e.page)).toEqual([18]);
	});
	it('préfère la date fixe à la férie', () => {
		expect(entreesDuJour(r, '2026-12-08', { tempora: 'Adv2-2' }).map((e) => e.page)).toEqual([409]);
	});
	it('donne toutes les méditations d’une fête qui en a plusieurs', () => {
		expect(entreesDuJour(r, '2027-06-04', { tempora: 'Pent02-5' }).length).toBe(2);
	});
	it('compte les dimanches d’octobre', () => {
		expect(clesDuJour('2027-10-03', { tempora: 'Pent19-0' })[0]).toBe('O:10-1');
		expect(clesDuJour('2027-10-17', { tempora: 'Pent21-0' })[0]).toBe('O:10-3');
	});
});
