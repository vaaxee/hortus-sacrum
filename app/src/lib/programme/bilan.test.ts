import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { enJours, type Indulgences } from '../indulgences.ts';
import { JACULATOIRES } from '../liste.ts';
import {
	ficheValable,
	indulgencesDuJour,
	jaculatoireAOuvrir,
	jaculatoiresPermises,
	minutesDeLaLigne,
	minutesDUneRecitation,
	texteDeLaJournee
} from './bilan.ts';
import { journee } from './journee.ts';
import { CALENDRIER, corps, PLAN, PROGRAMME, TEXTES } from './donnees-de-test.ts';

const IND = JSON.parse(readFileSync(new URL('../../../../data/prieres/indulgences.json', import.meta.url), 'utf-8')) as Indulgences;
const jr = journee(PROGRAMME, { jour: CALENDRIER.find((j) => j.date === '2026-12-01')!, pratiques: PLAN, corps });
const ligne = (id: string) => jr.lignes.find((l) => l.id === id)!;

describe('durées d’après les pages composées', () => {
	it('la durée réglée prime ; elle compte chaque récitation', () => {
		expect(minutesDeLaLigne(ligne('prog:chapelet'), corps)).toBe(20);
	});
	it('Angélus : trois récitations, les agonisants une fois (à midi)', () => {
		const l = ligne('prog:angelus');
		const total = minutesDeLaLigne(l, corps);
		expect(total).toBeGreaterThan(3 * minutesDUneRecitation({ ...l, sections: l.sections.filter((s) => !s.heure) }, corps) - 0.01);
		expect(total).toBeLessThan(3 * minutesDUneRecitation(l, corps) + 0.01);
	});
	it('la journée de semaine dure entre une heure et deux heures', () => {
		const total = jr.lignes.reduce((a, l) => a + minutesDeLaLigne(l, corps), 0);
		expect(total).toBeGreaterThan(60);
		expect(total).toBeLessThan(120);
	});
});

describe('indulgences', () => {
	it('seulement les fiches de l’Enchiridion de 1952, avec traduction approuvée hors du français', () => {
		expect(ficheValable({ ref: 'Beringer 1925, n° 1', frequence: 'chaque fois', partielles: [] })).toBe(false);
		expect(ficheValable({ ref: 'Ench. 1952, n° 1', frequence: 'chaque fois', partielles: [], langue: 'latin' })).toBe(false);
		expect(
			ficheValable({ ref: 'Ench. 1952, n° 1', frequence: 'chaque fois', partielles: [], langue: 'latin', traduction: 'Thésaurisons' })
		).toBe(true);
	});
	it('rien de gagné sans coche ; une jaculatoire dite compte', () => {
		const rien = indulgencesDuJour(jr, () => 0, new Map(), IND);
		expect(enJours(rien.gagnees)).toBe(0);
		expect(enJours(rien.possibles)).toBeGreaterThan(0);
		const jac = jaculatoiresPermises(JACULATOIRES, IND, (id) => TEXTES.has(id))[0];
		const une = indulgencesDuJour(jr, () => 0, new Map([[jac, 1]]), IND);
		expect(enJours(une.gagnees)).toBeGreaterThan(0);
	});
	it('n° 250 : la neuvaine du premier vendredi compte, une seule fois le jour où tombe aussi celle de S. Alphonse', () => {
		const jour = (date: string) => journee(PROGRAMME, { jour: CALENDRIER.find((j) => j.date === date)!, pratiques: PLAN, corps });
		const sans = { ...IND, fiches: { ...IND.fiches } };
		delete sans.fiches['breviaire-sc:neuvaine'];
		const possibles = (date: string, ind: Indulgences) => enJours(indulgencesDuJour(jour(date), () => 0, new Map(), ind).possibles);
		// lecture stricte (décision du 26 nov.) : seule la neuvaine du premier vendredi de décembre compte
		const comptes = CALENDRIER.map((j) => j.date).filter((d) => possibles(d, IND) !== possibles(d, sans));
		expect(comptes).toEqual([
			'2026-11-29',
			'2026-11-30',
			'2026-12-01',
			'2026-12-02',
			'2026-12-03',
			'2027-11-24',
			'2027-11-25',
			'2027-11-26',
			'2027-11-27'
		]);
		// les autres neuvaines du mois restent au programme, sans indulgence
		expect(jour('2027-02-01').textes.has('breviaire-sc:neuvaine')).toBe(true);
		// 28 mai 2027 : la neuvaine avant la fête est comptée sur celle de S. Alphonse, une seule fois
		const j = jour('2027-05-28');
		expect(j.textes.has('breviaire-sc:neuvaine') && j.textes.has('liguori:neuvaine-sacre-coeur')).toBe(true);
		const sansLiguori = { ...IND, fiches: { ...IND.fiches } };
		delete sansLiguori.fiches['liguori:neuvaine-sacre-coeur'];
		expect(possibles('2027-05-28', IND) - possibles('2027-05-28', sansLiguori)).toBe(7 * 365);
		// le même jour en décembre, deux textes à n° 250 ne comptent qu'une fois
		const deux = { ...IND, fiches: { ...IND.fiches, 'liguori:neuvaine-sacre-coeur': IND.fiches['breviaire-sc:neuvaine'] } };
		expect(possibles('2026-12-01', deux)).toBe(possibles('2026-12-01', IND));
	});
	it('tout coché : gagné = possible', () => {
		const tout = indulgencesDuJour(jr, (l) => l.heures?.length ?? 1, new Map(), IND);
		expect(tout.gagnees).toEqual(tout.possibles);
	});
});

describe('jaculatoire d’ouverture', () => {
	const permises = jaculatoiresPermises(JACULATOIRES, IND, (id) => TEXTES.has(id));
	const texte = texteDeLaJournee([...jr.lignes, ...jr.lectures], corps);
	it('écarte celles qui sont déjà dans les pages du jour', () => {
		// « Mon Jésus, miséricorde » est dans la Triple Couronne
		expect(texte).toContain(' mon jesus misericorde ');
		for (let k = 0; k < 50; k++)
			expect(jaculatoireAOuvrir(permises, corps, texte, undefined, () => k / 50)).not.toBe('thesaurisons:jac-33');
	});
	it('jamais deux fois de suite la même', () => {
		const a = jaculatoireAOuvrir(permises, corps, texte, undefined, () => 0)!;
		expect(jaculatoireAOuvrir(permises, corps, texte, a, () => 0)).not.toBe(a);
	});
});
