/**
 * Éditeur de recueils (REFONTE § 6, lot 11) : un recueil ajouté et affecté à un mois passe en tête ce mois-là ; une
 * surcharge remplace l'entrée livrée sans toucher au reste ; découpage d'un texte collé.
 */
import { describe, expect, it } from 'vitest';
import { choisirAvecMois, type Recueil as RecueilLu } from './meditations.ts';
import { avecSurcharges, choixPerso, cleValide, entreesDepuisTexte, recueilDuMoisPerso, versRecueil } from './recueils-perso.ts';
import type { Meditation, Recueil } from './types.ts';

const base = { origine: 'personnel' as const, creeLe: '2026-11-21T10:00:00Z', modifieLe: '2026-11-21T10:00:00Z' };
const source = { ouvrage: 'Mois de saint Michel', edition: 'Paris, 1880', page: '', url: '' };
const perso = (id: string, affectation: Recueil['affectation'], creeLe = base.creeLe): Recueil => ({
	...base,
	creeLe,
	id,
	titre: id,
	auteur: 'X',
	source,
	affectation
});
const med = (recueilId: string, rang: number, titre: string, extra: Partial<Meditation> = {}): Meditation => ({
	...base,
	id: `${recueilId}-${rang}`,
	recueilId,
	rang,
	titre,
	corps: `corps de ${titre}`,
	pratique: '',
	...extra
});

describe('recueil de l’utilisateur', () => {
	const r = perso('anges', { genre: 'mois', valeur: '9' });
	const meds = [med('anges', 1, 'Deuxième jour'), med('anges', 0, 'Premier jour', { pratique: 'Saluer son ange.' })];

	it('devient un recueil lisible, entrées dans l’ordre, clés J:n pour un mois', () => {
		const lu = versRecueil(r, meds);
		expect(lu.entrees.map((e) => [e.cle, e.titre])).toEqual([
			['J:1', 'Premier jour'],
			['J:2', 'Deuxième jour']
		]);
		expect(lu.entrees[0].pratique).toBe('Saluer son ange.');
		expect(lu.provenance).toBe('Paris, 1880');
	});

	it('affecté à un mois, il passe en tête ce mois-là', () => {
		const choisi = recueilDuMoisPerso([perso('autre', { genre: 'mois', valeur: '10' }), r], 9);
		expect(choisi?.id).toBe('anges');
		const lu = versRecueil(choisi!, meds);
		const hamon: RecueilLu = {
			id: 'hamon',
			titre: '',
			auteur: '',
			editions: {},
			provenance: '',
			entrees: [{ cle: 'D:09-01', titre: 'Hamon du jour', tome: 2, page: 1, corps: '' }]
		};
		const choix = choisirAvecMois('2027-09-01', { tempora: 'Pent14-3' }, [], hamon, null, lu);
		expect(choix.map((c) => c.entree.titre)).toEqual(['Premier jour', 'Hamon du jour']);
	});

	it('le plus récent l’emporte ; un recueil à la corbeille ne compte plus', () => {
		const neuf = perso('neuf', { genre: 'mois', valeur: '9' }, '2026-11-22T10:00:00Z');
		expect(recueilDuMoisPerso([r, neuf], 9)?.id).toBe('neuf');
		expect(recueilDuMoisPerso([r, { ...neuf, supprimeLe: '2026-11-23' }], 9)?.id).toBe('anges');
	});

	it('une entrée qui porte une clé est proposée ce jour-là', () => {
		const fete = versRecueil(perso('fete', { genre: 'fete', valeur: 'S. Michel' }), [med('fete', 0, 'Saint Michel', { cle: 'D:09-29' })]);
		expect(choixPerso([fete], '2027-09-29', { tempora: 'Pent18-3' }).map((c) => c.entree.titre)).toEqual(['Saint Michel']);
		expect(choixPerso([fete], '2027-09-30', { tempora: 'Pent18-4' })).toEqual([]);
	});
});

describe('surcharge d’un recueil livré', () => {
	const livre: RecueilLu = {
		id: 'hamon',
		titre: 'Méditations',
		auteur: 'Hamon',
		editions: {},
		provenance: '',
		entrees: [
			{ cle: 'D:12-08', titre: 'Immaculée Conception', tome: 1, page: 409, corps: 'texte livré, coquille' },
			{ cle: 'D:12-09', titre: 'Autre', tome: 1, page: 412, corps: 'intact' }
		]
	};

	it('remplace l’entrée corrigée et laisse les autres', () => {
		const r = avecSurcharges(livre, [med('hamon', 0, 'Immaculée Conception', { corps: 'texte corrigé' })]);
		expect(r.entrees[0]).toMatchObject({ corps: 'texte corrigé', cle: 'D:12-08', page: 409, corrige: true });
		expect(r.entrees[1]).toBe(livre.entrees[1]);
		expect(livre.entrees[0].corps).toBe('texte livré, coquille');
	});

	it('une surcharge à la corbeille rend le texte livré', () => {
		const r = avecSurcharges(livre, [med('hamon', 0, 'X', { corps: 'corrigé', supprimeLe: '2026-11-21' })]);
		expect(r).toBe(livre);
	});

	it('ne touche pas un autre recueil', () => {
		expect(avecSurcharges(livre, [med('chaignon', 0, 'X')])).toBe(livre);
	});
});

describe('saisie', () => {
	it('découpe un texte collé aux lignes « === Titre »', () => {
		const e = entreesDepuisTexte('=== Premier jour\nLe ciel.\n\n=== Deuxième jour\nLa terre.');
		expect(e.map((x) => [x.titre, x.corps])).toEqual([
			['Premier jour', 'Le ciel.'],
			['Deuxième jour', 'La terre.']
		]);
	});
	it('reconnaît les clés de meditations.ts', () => {
		for (const c of ['', 'D:12-08', 'T:Adv1-0', 'T:Pent24-6', 'F:sacre-coeur', 'O:10-3', 'J:31']) expect(cleValide(c), c).toBe(true);
		for (const c of ['12-08', 'D:1208', 'X:1', 'T:Adv']) expect(cleValide(c), c).toBe(false);
	});
});
