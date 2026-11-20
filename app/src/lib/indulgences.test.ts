import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { mentionDuTexte, noteDeTraduction, type Fiche, type Indulgences } from './indulgences.ts';
import { JACULATOIRES } from './liste.ts';

const donnees = JSON.parse(readFileSync(new URL('../../../data/prieres/indulgences.json', import.meta.url), 'utf8')) as Indulgences;

describe('indulgences : Enchiridion de 1952 seulement', () => {
	it('chaque fiche comptée cite l’Enchiridion de 1952', () => {
		for (const [id, f] of Object.entries(donnees.fiches)) expect(f.ref, id).toMatch(/Ench\. 1952/);
	});
	it('les concessions absentes de l’Enchiridion ne sont plus comptées', () => {
		for (const id of ['jardin:chapelet-de-saint-michel-archange']) {
			expect(donnees.fiches[id], id).toBeUndefined();
			expect(donnees.sans_compte[id], id).toMatch(/abrogée/);
		}
	});
	it('les œuvres reprises en 1952 sous un autre numéro restent comptées', () => {
		expect(donnees.fiches['thesaurisons:jac-244']?.ref).toMatch(/n° 234/);
		expect(donnees.fiches['thesaurisons:jac-232']?.ref).toMatch(/n° 199/);
		expect(donnees.fiches['beringer:coeur-afflige-de-marie']?.ref).toMatch(/n° 383/);
	});
	it('chaque fiche indique la langue de la concession', () => {
		for (const [id, f] of Object.entries(donnees.fiches)) expect(f.langue, id).toBeTruthy();
	});
	it('les jaculatoires du jour sont toutes indulgenciées en 1952', () => {
		for (const id of JACULATOIRES) expect(donnees.fiches[id]?.ref, id).toMatch(/Ench\. 1952/);
	});
	it('une mention recopiée d’un manuel antérieur n’est pas montrée ; celle de l’utilisateur l’est', () => {
		const ancien = { indulgence: '300 jours. — Pie VII, 1815.' };
		expect(mentionDuTexte({ ...ancien, original: JSON.stringify(ancien) })).toBeNull();
		expect(mentionDuTexte({ indulgence: '500 jours (Ench. 1952, n° 20)', original: '{}' })).not.toBeNull();
		expect(mentionDuTexte({ indulgence: 'ma note', original: JSON.stringify(ancien) })).toBe('ma note');
	});
	it('rappelle la règle des traductions (can. 934 § 2)', () => {
		const f: Fiche = { ref: 'Ench. 1952, n° 1', frequence: 'chaque fois', partielles: [] };
		expect(noteDeTraduction({ ...f, langue: 'français' })).toBeNull();
		expect(noteDeTraduction({ ...f, langue: 'latin', traduction: 'Thésaurisons' })).toMatch(/approuvée/);
		expect(noteDeTraduction(f)).toMatch(/934/);
	});
});
