import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { TYPES, typeDeduit, typesDe } from './etiquettes.ts';
import { pieceVersTexte, type Piece } from './livret.ts';
import { partieDe, rangDeLaPartie } from './parties.ts';
import type { Texte } from './types.ts';

const lire = <T>(c: string): T => JSON.parse(readFileSync(new URL(`../../../data/${c}`, import.meta.url), 'utf-8')) as T;
const TEXTES: Texte[] = [
	...lire<{ pieces: Piece[] }>('prieres/jardin.json').pieces.map(pieceVersTexte),
	...lire<{ pieces: Texte[] }>('prieres/sources.json').pieces
];
const t = (titre: string, partie = '') => ({ titre, partie });

describe('parties de la bibliothèque (lot 7)', () => {
	const parties = new Set(TEXTES.map(partieDe));
	it('les parties qui se recouvraient sont réunies', () => {
		for (const ancienne of [
			'Chapelet et Rosaire',
			'Rosaire',
			'Sainte Vierge',
			'Antiennes à la Sainte Vierge',
			'Consécrations',
			'Dévotions',
			'Passion'
		])
			expect(parties.has(ancienne), ancienne).toBe(false);
		expect(partieDe({ id: 'x', partie: 'Rosaire' })).toBe('Couronnes et chapelets');
		expect(partieDe({ id: 'jardin:la-fleche-d-or', partie: 'Prières de réparation' })).toBe('Passion et réparation');
		expect(partieDe({ id: 'beringer:cordon-saint-joseph', partie: 'Dévotions' })).toBe('Saint Joseph');
	});
	it('aucune partie n’en double une autre (même nom aux accents et à la casse près)', () => {
		const cle = (p: string) => p.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
		const vus = new Map<string, string>();
		for (const p of parties) {
			expect(vus.get(cle(p)), p).toBeUndefined();
			vus.set(cle(p), p);
		}
	});
	it('chaque partie livrée a son rang d’affichage', () => {
		for (const p of parties) expect(rangDeLaPartie(p), p).toBeLessThan(99);
	});
});

describe('type d’une prière (filtres)', () => {
	it('déduit du titre d’abord, puis de la partie', () => {
		expect(typeDeduit(t('Litanies de saint Joseph', 'Saint Joseph'))).toBe('litanie');
		expect(typeDeduit(t('Neuvaine au Sacré-Cœur de Jésus', 'Neuvaines'))).toBe('neuvaine');
		expect(typeDeduit(t('Le chapelet de saint Dominique', 'Couronnes et chapelets'))).toBe('chapelet');
		expect(typeDeduit(t('Sub tuum, avec ses versets'))).toBe('hymne');
		expect(typeDeduit(t('Acte de foi', 'Prières du matin et du soir'))).toBe('acte');
		expect(typeDeduit(t('Petit bréviaire du Sacré-Cœur — office du lundi', 'Petit bréviaire du Sacré-Cœur'))).toBe('office');
		expect(typeDeduit(t('Mon Jésus, miséricorde', 'Jaculatoires indulgenciées'))).toBe('jaculatoire');
		expect(typeDeduit(t('Prière du matin', 'Prières du matin et du soir'))).toBe('oraison');
	});
	it('la forme réglée ou relue dans la fiche prime', () => {
		expect(typesDe(t('Prière du matin'), ['examen', 'litanie'])).toEqual(['litanie']);
		expect(typesDe(t('Prière du matin'), [])).toEqual(['oraison']);
	});
	it('chaque prière livrée a un type parmi les filtres', () => {
		for (const x of TEXTES)
			expect(
				TYPES.some(([k]) => k === typeDeduit(x)),
				x.id
			).toBe(true);
	});
});
