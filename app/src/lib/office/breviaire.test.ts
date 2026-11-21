/**
 * Bréviaire romain (lot 9) : le chargeur recompose chaque jour en huit heures que le composant Office sait découper.
 * Données réelles (data/office/breviaire/2026-2027) ; le contrôle complet de l'année est engine/office/test_breviaire.py.
 */
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { heuresDe } from '../programme/heures.ts';
import { breviaireDuJour, jourDuBreviaire, type CommunsBreviaire, type FichierJour } from './breviaire.ts';

const racine = new URL('../../../../data/office/breviaire/2026-2027/', import.meta.url);
const lire = <T>(f: string) => JSON.parse(readFileSync(new URL(f, racine), 'utf-8')) as T;
const communs = lire<CommunsBreviaire>('communs.json');
const fetchLocal = (async (url: string) => {
	const f = String(url).split('/').pop()!;
	try {
		return { ok: true, json: async () => lire(f) };
	} catch {
		return { ok: false, json: async () => null };
	}
}) as unknown as typeof fetch;

describe('Bréviaire romain 2026-2027', () => {
	it('déclare la version de 1954 et huit heures', () => {
		expect(communs.source.version).toBe('Divino Afflatu - 1954');
		expect(communs.heures.map((h) => h.cle)).toEqual(['matines', 'laudes', 'prime', 'tierce', 'sexte', 'none', 'vepres', 'complies']);
		expect(communs.jours).toEqual({ debut: '2026-11-29', fin: '2027-11-27' });
	});

	it('1er dimanche de l’Avent : huit heures, l’oraison « Excita » à Laudes', () => {
		const j = jourDuBreviaire(communs, lire<FichierJour>('11-29.json'));
		expect(j.office).toBe('Dominica I Adventus');
		const h = heuresDe(j.corps);
		expect(h.map((x) => x.titre.split(' · ')[0])).toEqual(['Matines', 'Laudes', 'Prime', 'Tierce', 'Sexte', 'None', 'Vêpres', 'Complies']);
		const laudes = j.corps.split('## Laudes')[1].split('## Prime')[0];
		expect(laudes).toContain('Excita, quǽsumus, Dómine, poténtiam tuam, et veni');
		expect(laudes).toContain('[r]Psalmus 92[/r]');
	});

	it('charge un jour à la demande, et rien hors de l’année calculée', async () => {
		expect((await breviaireDuJour('2026-12-25', fetchLocal))?.office).toMatch(/Nativitate/);
		expect(await breviaireDuJour('2026-11-28', fetchLocal)).toBeNull();
		expect(await breviaireDuJour('2030-01-01', fetchLocal)).toBeNull();
	});
});
