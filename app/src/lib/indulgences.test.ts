import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { latinEnPremier, mentionDuTexte, noteDeTraduction, type Fiche, type Indulgences } from './indulgences.ts';
import { JACULATOIRES } from './liste.ts';
import { revisionsDuLivret, type Piece } from './livret.ts';

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
	it('ouvre sur le latin quand aucune traduction n’est approuvée', () => {
		const f: Fiche = { ref: 'Ench. 1952, n° 1', frequence: 'chaque fois', partielles: [] };
		expect(latinEnPremier({ ...f, langue: 'latin' })).toBe(true);
		expect(latinEnPremier({ ...f, langue: 'italien' })).toBe(true);
		expect(latinEnPremier({ ...f, langue: 'latin', traduction: 'Thésaurisons' })).toBe(false);
		expect(latinEnPremier({ ...f, langue: 'français' })).toBe(false);
		expect(latinEnPremier(undefined)).toBe(false);
	});
	it('les traductions de Beringer (1925) et les Pater, Ave, Gloria usuels ouvrent sur le français', () => {
		const beringer = Object.entries(donnees.fiches).filter(([, f]) => f.traduction?.startsWith('Beringer'));
		expect(beringer.map(([id]) => id).sort()).toEqual(
			[
				'paroissien:angelus',
				'beringer:regina-caeli',
				'paroissien:de-profundis',
				'jardin:magnificat',
				'jardin:chaque-vendredi-devant-le-crucifix',
				'beringer:coeur-afflige-de-marie',
				'jardin:les-sept-douleurs-de-marie',
				'weber:trois-prieres-perpetuel-secours',
				'paroissien:litanies-saint-nom',
				'paroissien:litanies-sainte-vierge'
			].sort()
		);
		for (const [id, f] of beringer) {
			expect(f.traduction, id).toMatch(/11 juillet 1925/);
			expect(latinEnPremier(f), id).toBe(false);
		}
		// les pages du chapelet sont composées à l'affichage (lot 6) : la fiche est celle de Sambucy
		for (const id of ['sambucy:chapelet-saint-dominique']) {
			expect(donnees.fiches[id]?.traduction, id).toMatch(/L’Ami du clergé, 9 avril 1931/);
			expect(latinEnPremier(donnees.fiches[id]), id).toBe(false);
		}
	});
	it('les hymnes en vers et les textes de Beringer qui ne suivent pas la formule de 1952 restent en latin d’abord', () => {
		for (const id of ['jardin:veni-creator-spiritus', 'jardin:ave-maris-stella', 'weber:stabat-mater'])
			expect(latinEnPremier(donnees.fiches[id]), id).toBe(true);
	});
	it('les textes remplacés par ceux de Beringer portent une révision', () => {
		const sources = JSON.parse(readFileSync(new URL('../../../data/prieres/sources.json', import.meta.url), 'utf8')) as {
			pieces: { id: string; corps: string; revision?: number }[];
		};
		const p = (id: string) => sources.pieces.find((x) => x.id === id);
		expect(p('paroissien:angelus')?.corps).toContain('par la voix de l’Ange');
		expect(p('paroissien:de-profundis')?.corps).toContain('Des profondeurs de l’abîme');
		expect(p('weber:trois-prieres-perpetuel-secours')?.corps).toContain('Voici à vos pieds, ô Mère du Perpétuel Secours');
		const lorette = p('paroissien:litanies-sainte-vierge')?.corps ?? '';
		const ordre = [
			'Mère admirable',
			'Mère du bon conseil',
			'Mère du Créateur',
			'péché originel',
			'Regina in caelum assumpta',
			'très saint Rosaire',
			'Reine de la paix'
		];
		expect(ordre.map((x) => lorette.indexOf(x))).toEqual(ordre.map((x) => lorette.indexOf(x)).sort((a, b) => a - b));
		expect(ordre.every((x) => lorette.includes(x))).toBe(true);
		expect(p('paroissien:litanies-saint-nom')?.corps).toContain('Par votre institution de la très sainte Eucharistie');
		expect(p('weber:trois-prieres-perpetuel-secours')?.corps.match(/Trois \*Ave Maria\*/g)).toHaveLength(3);
		for (const id of [
			'paroissien:angelus',
			'paroissien:de-profundis',
			'weber:trois-prieres-perpetuel-secours',
			'paroissien:litanies-saint-nom',
			'paroissien:litanies-sainte-vierge'
		])
			expect(p(id)?.revision ?? 0, id).toBeGreaterThan(0);
	});
	it('les traductions certifiées de Thésaurisons sont reportées dans le livret (n° 82, 150, 498)', () => {
		const jardin = JSON.parse(readFileSync(new URL('../../../data/prieres/jardin.json', import.meta.url), 'utf8')) as {
			pieces: Piece[];
		};
		const revs = new Map(revisionsDuLivret(jardin.pieces).map((r) => [r.id, r]));
		const couronne = revs.get('jardin:la-triple-couronne-d-or-du-sacre-c-ur-de-jesus')?.corps ?? '';
		expect(couronne).toContain('Doux Cœur de mon Jésus, faites que je vous aime de plus en plus.');
		expect(couronne).not.toContain('toujours de plus en plus');
		expect(revs.get('jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph')?.corps).toContain(
			'nous vivions uniquement pour eux et mourions dans la joie de leur amour'
		);
		expect(revs.get('jardin:priere-pour-les-agonisants')?.corps).toContain('qui sont en ce moment à l’agonie');
		for (const id of ['jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph', 'jardin:priere-pour-les-agonisants']) {
			expect(donnees.fiches[id]?.traduction, id).toMatch(/Thésaurisons/);
			expect(latinEnPremier(donnees.fiches[id]), id).toBe(false);
		}
		// la Triple Couronne est composée à l'affichage depuis le livret (lot 6) : la fiche est celle du livret
		expect(donnees.fiches['jardin:la-triple-couronne-d-or-du-sacre-c-ur-de-jesus']?.traduction).toMatch(/n° 82/);
		expect(donnees.fiches['hortus:triple-couronne-1']).toBeUndefined();
	});
	it('rappelle la règle des traductions (can. 934 § 2)', () => {
		const f: Fiche = { ref: 'Ench. 1952, n° 1', frequence: 'chaque fois', partielles: [] };
		expect(noteDeTraduction({ ...f, langue: 'français' })).toBeNull();
		expect(noteDeTraduction({ ...f, langue: 'latin', traduction: 'Thésaurisons' })).toMatch(/approuvée/);
		expect(noteDeTraduction(f)).toMatch(/934/);
	});
});
