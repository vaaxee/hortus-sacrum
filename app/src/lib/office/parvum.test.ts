import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { rendre } from '../markup.ts';
import { heuresDe } from '../programme/heures.ts';
import { extraire } from '../programme/texte.ts';
import { combinaisonDuJour, parvumDuJour, texteDeLHeure, type DonneesParvum } from './parvum.ts';

const DONNEES = JSON.parse(readFileSync(new URL('../../../../data/office/parvum.json', import.meta.url), 'utf-8')) as DonneesParvum;

/** Le texte d'une heure d'un jour, tel que le composant Office l'affiche. */
function heure(date: string, cle: string): string {
	const jour = parvumDuJour(DONNEES, date)!;
	const h = heuresDe(jour.corps).find((x) => x.cle === cle)!;
	return extraire(jour.corps, h.extrait) ?? '';
}

describe('Officium parvum', () => {
	it('chaque jour a ses huit heures canoniales, dans l’ordre, chacune avec son texte', () => {
		const jour = parvumDuJour(DONNEES, '2026-11-24')!;
		const heures = heuresDe(jour.corps);
		expect(heures.map((h) => h.cle)).toEqual(['matines', 'laudes', 'prime', 'tierce', 'sexte', 'none', 'vepres', 'complies']);
		expect(heures.every((h) => h.canoniale)).toBe(true);
		for (const h of heures) expect((extraire(jour.corps, h.extrait) ?? '').length).toBeGreaterThan(500);
	});

	it('tous les jours des années calculées se recomposent sans trou', () => {
		const { debut, suite } = DONNEES.jours;
		const t0 = Date.UTC(Number(debut.slice(0, 4)), Number(debut.slice(5, 7)) - 1, Number(debut.slice(8, 10)));
		for (let n = 0; n < suite.length; n++) {
			const date = new Date(t0 + n * 86_400_000).toISOString().slice(0, 10);
			const c = combinaisonDuJour(DONNEES, date);
			expect(c?.heures).toHaveLength(8);
			for (const id of c!.heures) expect(texteDeLHeure(DONNEES, id).trim()).not.toBe('');
		}
		expect(combinaisonDuJour(DONNEES, '1999-01-01')).toBeUndefined();
		expect(parvumDuJour(DONNEES, '2099-01-01')).toBeUndefined();
	});

	it('aucune section vide, aucun renvoi de Divinum Officium laissé tel quel', () => {
		for (const [id, t] of Object.entries(DONNEES.textes)) {
			const texte = texteDeLHeure(DONNEES, id);
			expect(texte, id).not.toMatch(/^[@$&]|\bmissing\b|est absente/m);
			const blocs = texte.split('\n\n');
			blocs.forEach((b, i) => {
				if (b.startsWith('### ')) expect(blocs[i + 1] ?? '', `${id} : ${b}`).not.toMatch(/^(### |$)/);
			});
			expect(t.temps.length).toBeGreaterThan(0);
		}
	});

	it('trois temps témoins : Avent, Noël, reste de l’année', () => {
		// Avent (Commune/C12A) : Alma Redemptoris avec le verset de l'Annonciation ; antiennes de Sancti/03-25
		expect(parvumDuJour(DONNEES, '2026-12-02')!.temps).toBe('adventus');
		expect(heure('2026-12-02', 'complies')).toContain('Alma Redemptóris Mater');
		expect(heure('2026-12-02', 'complies')).toContain('Ángelus Dómini nuntiávit Maríæ');
		expect(heure('2026-12-02', 'vepres')).toContain('Missus est Gábriel Angelus');
		// Noël (Commune/C12N) : antiennes de la Circoncision (Sancti/01-01), oraison « Deus, qui salútis ætérnæ »
		expect(parvumDuJour(DONNEES, '2026-12-28')!.temps).toBe('nativitatis');
		expect(heure('2026-12-28', 'prime')).toContain('O admirábile commércium');
		expect(heure('2026-12-28', 'complies')).toContain('Deus, qui salútis ætérnæ');
		// Reste de l'année (Commune/C12) : « Assúmpta est María », Te Deum, Salve Regina
		expect(parvumDuJour(DONNEES, '2026-11-24')!.temps).toBe('post-pentecosten');
		expect(heure('2026-11-24', 'laudes')).toContain('Assúmpta est María in cælum');
		expect(heure('2026-11-24', 'matines')).toContain('Te Deum laudámus');
		expect(heure('2026-11-24', 'complies')).toContain('Salve, Regína');
	});

	it('Septuagésime et temps pascal', () => {
		expect(heure('2027-02-10', 'prime')).toContain('Laus tibi, Dómine');
		expect(heure('2027-02-10', 'matines')).not.toContain('Te Deum laudámus');
		expect(heure('2027-02-10', 'complies')).toContain('Ave, Regína cælórum');
		expect(heure('2026-04-20', 'complies')).toContain('Regína cæli');
	});

	it('les psaumes de Matines suivent le jour (lundi, mardi, mercredi)', () => {
		expect(heure('2026-11-23', 'matines')).toContain('Psalmus 8');
		expect(heure('2026-11-24', 'matines')).toContain('Psalmus 44');
		expect(heure('2026-11-25', 'matines')).toContain('Psalmus 95');
		expect(heure('2026-11-26', 'matines')).toBe(heure('2026-11-23', 'matines'));
	});

	it('le balisage passe par rendre() sans italique parasite (l’astérisque de médiante reste un astérisque)', () => {
		for (const id of Object.keys(DONNEES.textes)) expect(rendre(texteDeLHeure(DONNEES, id)), id).not.toContain('<em>');
		const html = rendre(heure('2026-11-24', 'laudes'));
		expect(html).toContain('<h4>Psalmi</h4>');
		expect(html).toContain('Dóminus regnávit, decórem indútus est: * indútus est Dóminus fortitúdinem');
	});
});
