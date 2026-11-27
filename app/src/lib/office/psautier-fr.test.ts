/**
 * Psautier de Fillion en regard du latin du Bréviaire romain : textes mot pour mot (copiés de l'édition de 1917, relus
 * sur le scan) et alignement sur les données réelles (data/office/breviaire/2026-2027, data/office/breviaire-fr).
 */
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { jourDuBreviaire, type CommunsBreviaire, type FichierJour } from './breviaire.ts';
import { aligner, etiquettesDeLaPartie, indexer, rendreAvecFillion, rendreParagraphe, type PsautierFr } from './psautier-fr.ts';

const data = new URL('../../../../data/office/', import.meta.url);
const lire = <T>(f: string) => JSON.parse(readFileSync(new URL(f, data), 'utf-8')) as T;
const fillion = lire<PsautierFr>('breviaire-fr/psautier-fillion.json');
const communs = lire<CommunsBreviaire>('breviaire/2026-2027/communs.json');
const idx = indexer(fillion);
const verset = (ps: number, n: number) => idx.psaumes.get(ps)!.versets.find((v) => v.n === n)!.fr;

describe('Psautier de Fillion : textes mot pour mot', () => {
	it('déclare son édition et son approbation', () => {
		expect(fillion.source.edition).toMatch(/^Septième édition soigneusement revue, Paris, Librairie Victor Lecoffre, J\. Gabalda/);
		expect(fillion.source.approbation).toContain('Imprimatur : Parisiis, die 4a junii 1912, P. Thomas');
		expect(fillion.psaumes).toHaveLength(150);
		expect(fillion.cantiques).toHaveLength(17);
	});

	it('Ps 1, 1 ; Ps 50, 3 ; Ps 109, 1 ; Ps 129, 1 ; Ps 150, 6', () => {
		// copiés de data/office/breviaire-fr/psautier-fillion.json
		expect(verset(1, 1)).toBe(
			"Heureux l'homme qui n'a point marché dans le conseil des impies, qui ne s'est pas arrêté dans la voie des pécheurs, et qui ne s'est point assis dans la chaire de pestilence ;"
		);
		expect(verset(50, 3)).toBe(
			'Ayez pitié de moi, ô Dieu, selon votre grande miséricorde, et selon la multitude de vos bontés, effacez mon iniquité.'
		);
		expect(verset(109, 1)).toBe(
			"Le Seigneur a dit à mon Seigneur : Asseyez-vous à ma droite, jusqu'à ce que je fasse de vos ennemis l'escabeau de vos pieds."
		);
		expect(verset(129, 1)).toBe('Du fond des abîmes je crie vers vous, Seigneur ;');
		expect(verset(150, 6)).toBe('Que tout ce qui respire loue le Seigneur.');
	});

	it('Ps 132 (jeudi, Vêpres) et le cantique de Zacharie, entiers', () => {
		expect(idx.psaumes.get(132)!.versets.map((v) => v.fr)).toEqual([
			"Ah ! qu'il est bon et agréable pour des frères d'habiter ensemble !",
			"C'est comme le parfum répandu sur la tête, qui descend sur la barbe, la barbe d'Aaron ; qui descend sur le bord de son vêtement.",
			"C'est comme la rosée de l'Hermon, qui descend sur la montagne de Sion ;",
			"Car c'est là que le Seigneur envoie la bénédiction, et la vie à tout jamais."
		]);
		const zacharie = idx.cantiques.get('Psalm231')!;
		expect(zacharie.versets[0].fr).toMatch(/^Béni soit le Seigneur, le Dieu d'Israël,/);
		expect(zacharie.versets).toHaveLength(12);
	});
});

describe('Alignement sur le latin du Bréviaire', () => {
	it('une partie « Psalmus N(a-b) » prend les étiquettes de Divinum Officium comprises entre a et b', () => {
		const labs = idx.psaumes.get(144)!.lignes_la!;
		expect(etiquettesDeLaPartie(labs, '1', '13a').at(-1)).toBe('13a');
		expect(etiquettesDeLaPartie(labs, '13b', '21')[0]).toBe('13b');
	});

	it('Ps 4 (Complies du dimanche) : chaque verset en face de sa ligne latine', () => {
		const p = communs.paragraphes.find((x) => x.startsWith('[r]Psalmus 4[/r]'))!;
		const latin = p
			.split('\n')
			.slice(1)
			.filter((l) => !/^(℣\.|℟\.)/.test(l));
		const blocs = aligner(idx.psaumes.get(4)!, latin)!;
		expect(blocs[0].la[0]).toMatch(/^Cum invocárem/);
		expect(blocs[0].fr).toBe(verset(4, 2));
		expect(blocs.at(-1)!.fr).toBe(verset(4, 10));
	});

	it('tous les psaumes de l’année calculée sont alignés, sauf l’invitatoire', () => {
		const sans: string[] = [];
		let n = 0;
		for (const p of communs.paragraphes) {
			const m = /^\[r\]Psalmus (\d+)/m.exec(p);
			if (!m) continue;
			n++;
			const h = rendreParagraphe(p, idx);
			if (!h.includes('class="strophe"') && !h.includes('class="fr-bloc"')) sans.push(m[0]);
		}
		expect(n).toBeGreaterThan(400);
		expect(sans).toEqual([]);
	});

	it('un cantique coupé autrement que chez Fillion : le français en un bloc, après le latin', () => {
		const p = communs.paragraphes.find((x) => x.includes('[r]Exod. 15:1-22[/r]'))!;
		const h = rendreParagraphe(p, idx);
		expect(h).not.toContain('class="strophe"');
		expect(h.indexOf('Cantémus Dómino')).toBeLessThan(h.indexOf('class="fr-bloc"'));
		expect(h).toContain('Cantique de Moïse. Exod. xv, 1-19');
		expect(h).toContain('Chantons au Seigneur, car il a fait éclater sa gloire ; il a précipité dans la mer le cheval et le cavalier.');
	});

	it('1er dimanche de l’Avent, Laudes : le Ps 92 en regard, le Gloria en latin seul', () => {
		const j = jourDuBreviaire(communs, lire<FichierJour>('breviaire/2026-2027/11-29.json'));
		const laudes = j.corps.split('## Laudes')[1].split('## Prime')[0];
		const h = rendreAvecFillion(laudes, fillion);
		expect(h).toContain("Le Seigneur a régné, et s'est revêtu de gloire : le Seigneur s'est revêtu et s'est ceint de force.");
		expect(h).toContain('Dóminus regnávit');
		expect(h).toContain('Glória Patri');
		expect(h).not.toContain('[r]');
	});
});
