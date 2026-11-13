import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import type { Jour } from './calendrier.ts';
import { pratiquesDuPlan } from './plan.ts';
import { occurrences } from './pratiques.ts';

const annee = JSON.parse(readFileSync('../data/calendar/2026-2027.json', 'utf-8')) as Jour[];
const pratiques = pratiquesDuPlan(annee, []);
const debut = annee[0].date;
const fin = annee[annee.length - 1].date;

/** Dates où le calendrier inscrit une dévotion dont le libellé commence par ce titre. */
const datesDuCalendrier = (prefixe: string) =>
	annee.filter((j) => j.devotions.some((d) => d.libelle.startsWith(prefixe))).map((j) => j.date);
const de = (titre: string) => pratiques.find((p) => p.titre === titre)!;
const dates = (titre: string) => occurrences(de(titre).regle, debut, fin).map((o) => o.date);

describe('pratiquesDuPlan (plan accepté 2026-2027)', () => {
	it('retrouve chaque série hebdomadaire aux mêmes dates que le calendrier papier', () => {
		for (const t of ['Sept dimanches de S. Joseph', 'Treize mardis de S. Antoine', 'Quinze samedis du Rosaire',
			'Treize vendredis de S. François de Paule', 'Dix dimanches de S. Ignace', 'Sept vendredis des Douleurs']) {
			expect(dates(t), t).toEqual(datesDuCalendrier(t));
		}
	});
	it('retrouve les neuvaines, fixes et mobiles', () => {
		for (const t of ['Neuvaine à l’Immaculée Conception', 'Neuvaine de Noël', 'Neuvaine au Saint-Esprit, avant la Pentecôte', 'Neuvaine au Sacré-Cœur']) {
			expect(dates(t), t).toEqual(datesDuCalendrier(t));
		}
	});
	it('préparation de Montfort : 33 jours du 3 mars au 4 avril 2027', () => {
		const d = dates('Préparation à la consécration de Montfort');
		expect(d).toHaveLength(33);
		expect([d[0], d[32]]).toEqual(['2027-03-03', '2027-04-04']);
	});
	it('neuf premiers vendredis et veille (Heure sainte)', () => {
		expect(dates('Neuf premiers vendredis du mois')).toEqual(datesDuCalendrier('Premier vendredi du mois —'));
		expect(dates('Heure sainte (veille du premier vendredi)')).toEqual(datesDuCalendrier('Heure sainte'));
	});
	it('identifiants uniques', () => {
		expect(new Set(pratiques.map((p) => p.id)).size).toBe(pratiques.length);
	});
});
