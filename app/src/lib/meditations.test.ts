import { describe, expect, it } from 'vitest';
import { choisir, clesDuJour, entreesDuJour, rangParcours, type Recueil } from './meditations.ts';

const r: Recueil = {
	id: 'x',
	titre: '',
	auteur: '',
	editions: {},
	provenance: '',
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
	it('jours ordinaires : parcours de Chaignon dans l’ordre ; dimanches et temps forts : Hamon', () => {
		const ch: Recueil = {
			...r,
			id: 'chaignon',
			entrees: [
				{ cle: 'S:1', titre: 'La fin de l’homme', tome: 1, page: 0, corps: '' },
				{ cle: 'S:2', titre: 'Les créatures', tome: 1, page: 0, corps: '' }
			]
		};
		const ham: Recueil = {
			...r,
			entrees: [
				{ cle: 'T:Pent03-2', titre: 'H', tome: 2, page: 1, corps: '' },
				{ cle: 'T:Pent03-0', titre: 'Dim', tome: 2, page: 1, corps: '' }
			]
		};
		const annee = [
			{ date: '2027-06-13', tempora: 'Pent03-0' },
			{ date: '2027-06-14', tempora: 'Pent03-1' },
			{ date: '2027-06-15', tempora: 'Pent03-2' },
			{ date: '2027-06-16', tempora: 'Pent03-3' }
		];
		const mardi = choisir('2027-06-15', { tempora: 'Pent03-2' }, annee, ham, ch);
		expect(mardi[0].entree.titre).toBe('Les créatures');
		expect(mardi.map((x) => x.entree.titre)).toContain('H');
		expect(choisir('2027-06-13', { tempora: 'Pent03-0' }, annee, ham, ch)[0].entree.titre).toBe('Dim');
		expect(rangParcours('2027-06-16', annee, 2)).toBe(1);
	});
	it('compte les dimanches d’octobre', () => {
		expect(clesDuJour('2027-10-03', { tempora: 'Pent19-0' })[0]).toBe('O:10-1');
		expect(clesDuJour('2027-10-17', { tempora: 'Pent21-0' })[0]).toBe('O:10-3');
	});
});
