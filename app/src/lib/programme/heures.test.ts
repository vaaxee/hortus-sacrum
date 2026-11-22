import { describe, expect, it } from 'vitest';
import { cocheDeLHeure, heureCourante, heuresDe } from './heures.ts';
import { journee } from './journee.ts';
import { etatDesLectures } from './lectures.ts';
import { extraire, normaliser } from './texte.ts';
import { CALENDRIER, corps, PLAN, PROGRAMME } from './donnees-de-test.ts';

const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
const a = (h: number) => new Date(2026, 10, 21, h, 30);

describe('heures du Petit bréviaire du Sacré-Cœur', () => {
	it('chaque office a ses huit heures, dans l’ordre du livre, et la Recommandation à part', () => {
		for (const j of JOURS) {
			const h = heuresDe(corps(`breviaire-sc:office-${j}`)!);
			expect(
				h.filter((x) => x.canoniale).map((x) => x.cle),
				j
			).toEqual(['matines', 'laudes', 'prime', 'tierce', 'sexte', 'none', 'vepres', 'complies']);
			expect(
				h.filter((x) => !x.canoniale).map((x) => x.nom),
				j
			).toEqual(['Recommandation']);
		}
	});

	it('les heures, mises bout à bout, redonnent l’office entier', () => {
		const t = corps('breviaire-sc:office-lundi')!;
		const recompose = heuresDe(t)
			.map((h) => extraire(t, h.extrait))
			.join('\n\n');
		expect(normaliser(recompose)).toBe(normaliser(t));
	});

	it('à l’ouverture, l’heure courante', () => {
		const h = heuresDe(corps('breviaire-sc:office-lundi')!);
		expect(heureCourante(h, a(3))?.cle).toBe('matines');
		expect(heureCourante(h, a(6))?.cle).toBe('laudes');
		expect(heureCourante(h, a(10))?.cle).toBe('tierce');
		expect(heureCourante(h, a(13))?.cle).toBe('sexte');
		expect(heureCourante(h, a(16))?.cle).toBe('none');
		expect(heureCourante(h, a(19))?.cle).toBe('vepres');
		expect(heureCourante(h, a(22))?.cle).toBe('complies');
	});

	it('un texte sans heures n’est pas un office', () => {
		expect(heuresDe(corps('paroissien:priere-du-matin')!)).toEqual([]);
	});
});

describe('« Lectures du jour » : un seul calcul', () => {
	const jr = journee(PROGRAMME, { jour: CALENDRIER.find((j) => j.date === '2026-12-01')!, pratiques: PLAN, corps });
	it('l’office est lu quand chaque heure canoniale est cochée', () => {
		const coches: Record<string, number> = {};
		const avant = etatDesLectures(jr, coches, corps);
		const office = avant.lectures.find((x) => x.lecture.id === 'lec:office')!;
		expect(office).toMatchObject({ lu: false, faites: 0, total: 8 });
		for (const h of office.heures!.filter((x) => x.canoniale)) coches[cocheDeLHeure('lec:office', h.cle)] = 1;
		const apres = etatDesLectures(jr, coches, corps);
		expect(apres.lectures.find((x) => x.lecture.id === 'lec:office')).toMatchObject({ lu: true, faites: 8 });
		expect(apres.lues).toBe(avant.lues + 1);
	});
	it('l’Évangile est lu par sa case ou par « J’ai lu ce chapitre »', () => {
		expect(etatDesLectures(jr, { 'lecture:Mt 5': 1 }, corps).lectures.find((x) => x.lecture.id === 'lec:ecriture')?.lu).toBe(true);
		expect(etatDesLectures(jr, { 'lec:ecriture': 1 }, corps).lectures.find((x) => x.lecture.id === 'lec:ecriture')?.lu).toBe(true);
	});
	it('N = les lectures comptées (office, Évangile, Somme, méditation)', () => {
		expect(etatDesLectures(jr, {}, corps).total).toBe(4);
	});
});
