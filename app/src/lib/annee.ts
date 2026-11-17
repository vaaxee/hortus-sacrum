/**
 * Vue d'ensemble d'une année liturgique (du premier dimanche de l'Avent à la veille du suivant) :
 * temps liturgiques, dévotions de chaque mois, dévotions personnelles à jours comptés (en séries, rangées sur des
 * couloirs pour voir ce qui se suit et ce qui se superpose) et dates du profil spirituel.
 */
import type { Jour } from './calendrier.ts';
import { occurrences, versIso } from './pratiques.ts';
import type { FetePerso, Pratique } from './types.ts';

const J = 86400000;
const midi = (s: string) => new Date(s + 'T12:00:00');
export const ecart = (a: string, b: string) => Math.round((midi(b).getTime() - midi(a).getTime()) / J);
export const plusJours = (s: string, n: number) => versIso(new Date(midi(s).getTime() + n * J));

/** Couleur de chaque temps liturgique (le temps de la Passion garde le violet). */
const COULEUR_TEMPS: [RegExp, string][] = [
	[/Avent/, 'violet'],
	[/Noël/, 'blanc'],
	[/après l’Épiphanie/, 'vert'],
	[/Épiphanie/, 'blanc'],
	[/Septuagésime/, 'violet'],
	[/Carême|Passion/, 'violet'],
	[/pascal/, 'blanc'],
	[/Pentecôte/, 'vert']
];
export const couleurDuTemps = (temps: string) => COULEUR_TEMPS.find(([r]) => r.test(temps))?.[1] ?? 'vert';

export interface Segment {
	debut: string;
	fin: string;
	titre: string;
	couleur?: string;
}

/** Les temps liturgiques, en segments continus (le temps de l'Épiphanie qui revient pendant l'octave est fondu). */
export function temps(jours: Jour[]): Segment[] {
	const out: Segment[] = [];
	for (const j of jours) {
		const t = j.temps.replace(/^Temps de l’Épiphanie$/, 'Temps de l’Épiphanie');
		const der = out[out.length - 1];
		if (der && (der.titre === t || (/Épiphanie/.test(der.titre) && /Épiphanie/.test(t) && couleurDuTemps(der.titre) === couleurDuTemps(t))))
			der.fin = j.date;
		else out.push({ debut: j.date, fin: j.date, titre: t, couleur: couleurDuTemps(t) });
	}
	// un jour isolé du « temps après l'Épiphanie » au milieu de l'octave rejoint ses voisins
	return out
		.filter((s, i) => !(s.debut === s.fin && out[i - 1] && out[i + 1] && out[i - 1].titre === out[i + 1].titre))
		.reduce<Segment[]>((acc, s) => {
			const der = acc[acc.length - 1];
			if (der && der.titre === s.titre) der.fin = s.fin;
			else acc.push({ ...s });
			return acc;
		}, [])
		.map((s, i, a) => (a[i + 1] ? { ...s, fin: plusJours(a[i + 1].debut, -1) } : s));
}

/** Les mois civils de l'année liturgique, rognés à ses bornes. */
export function moisCivils(debut: string, fin: string): { an: number; mois: number; debut: string; fin: string }[] {
	const out = [];
	let d = midi(debut);
	while (versIso(d) <= fin) {
		const an = d.getFullYear(),
			mois = d.getMonth() + 1;
		const dernier = versIso(new Date(an, mois, 0, 12));
		out.push({ an, mois, debut: versIso(d), fin: dernier < fin ? dernier : fin });
		d = new Date(an, mois, 1, 12);
	}
	return out;
}

export interface Serie extends Segment {
	pratique: string;
	/** Dates de la série (une neuvaine de samedis n'occupe pas chaque jour entre son début et sa fin). */
	dates: string[];
	total: number;
	couloir: number;
}

/**
 * Séries des dévotions personnelles dans l'intervalle : chaque suite comptée (neuvaine, trentain, 33 jours, premiers
 * samedis…), le mois entier, ou une date fixe. Les pratiques de chaque semaine ou de chaque mois sans fin ne forment pas
 * de série : elles rempliraient l'année.
 */
export function series(pratiques: Pratique[], debut: string, fin: string): Serie[] {
	const out: Omit<Serie, 'couloir'>[] = [];
	for (const p of pratiques) {
		if (p.type === 'roue' || p.supprimeLe || !p.active) continue;
		const occ = occurrences(p.regle, debut, fin);
		const genre = p.regle.genre;
		if (genre === 'mois_entier' || genre === 'fixe') {
			if (occ.length)
				out.push({
					pratique: p.id,
					titre: p.titre,
					debut: occ[0].date,
					fin: occ[occ.length - 1].date,
					dates: occ.map((o) => o.date),
					total: occ.length
				});
			continue;
		}
		let s: (typeof out)[number] | null = null;
		for (const o of occ) {
			if (!o.total) continue;
			if (o.rang === 1 || !s) {
				s = { pratique: p.id, titre: p.titre, debut: o.date, fin: o.date, dates: [], total: o.total };
				out.push(s);
			}
			s.fin = o.date;
			s.dates.push(o.date);
		}
	}
	// couloirs : chaque série prend le premier couloir libre à sa date de début
	out.sort((a, b) => a.debut.localeCompare(b.debut) || b.fin.localeCompare(a.fin));
	const finsDesCouloirs: string[] = [];
	return out.map((s) => {
		let c = finsDesCouloirs.findIndex((f) => f < s.debut);
		if (c < 0) c = finsDesCouloirs.length;
		finsDesCouloirs[c] = s.fin;
		return { ...s, couloir: c };
	});
}

/** Jours où plusieurs séries se superposent. */
export function superpositions(s: Serie[]): Set<string> {
	const n = new Map<string, number>();
	for (const x of s) for (const d of x.dates) n.set(d, (n.get(d) ?? 0) + 1);
	return new Set([...n].filter(([, k]) => k > 1).map(([d]) => d));
}

export interface DatePerso {
	date: string;
	titre: string;
	profil?: string;
	id: string;
}

/** Les fêtes et anniversaires personnels, placés dans l'année liturgique. */
export function datesPerso(fetes: FetePerso[], debut: string, fin: string): DatePerso[] {
	const out: DatePerso[] = [];
	for (const f of fetes) {
		if (f.supprimeLe) continue;
		for (const an of [Number(debut.slice(0, 4)), Number(fin.slice(0, 4))]) {
			const d = `${an}-${String(f.mois).padStart(2, '0')}-${String(f.jour).padStart(2, '0')}`;
			if (d >= debut && d <= fin && !out.some((x) => x.id === f.id && x.date === d))
				out.push({ date: d, titre: f.titre, profil: f.profil, id: f.id });
		}
	}
	return out.sort((a, b) => a.date.localeCompare(b.date));
}
