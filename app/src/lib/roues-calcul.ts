/** Calculs des roues symboliques, sans accès à la base (utilisables partout, y compris dans les tests). */
import type { ElementRoue, Pratique, UniteRoue } from './types.ts';

const J = 86400000;
const midi = (s: string) => new Date(s + 'T12:00:00');

/** Premier dimanche de l'Avent de l'année civile a (dimanche du 27 novembre au 3 décembre). */
export function premierDimancheAvent(a: number): Date {
	const noel = new Date(a, 11, 25, 12);
	// quatrième dimanche avant Noël : le dimanche qui précède Noël (Noël exclu), moins trois semaines
	const recul = noel.getDay() === 0 ? 7 : noel.getDay();
	return new Date(noel.getTime() - (recul + 21) * J);
}

/** Début de l'année liturgique qui contient la date (AAAA-MM-JJ). */
export function debutAnnee(date: string): Date {
	const d = midi(date);
	const a = premierDimancheAvent(d.getFullYear());
	return d >= a ? a : premierDimancheAvent(d.getFullYear() - 1);
}

/** Rang (à partir de 0) de la période en cours depuis le début de l'année liturgique. */
export function pas(date: string, unite: UniteRoue): number {
	const d = midi(date);
	const a = debutAnnee(date);
	const jours = Math.round((d.getTime() - a.getTime()) / J);
	if (unite === 'semaine') return Math.floor(jours / 7);
	if (unite === 'mois') return (d.getFullYear() - a.getFullYear()) * 12 + d.getMonth() - a.getMonth();
	return jours;
}

export const uniteDe = (r: Pratique): UniteRoue => (r.regle.genre === 'roue' ? r.regle.unite : 'jour');

/** Position (à partir de 0) de la roue à cette date. */
export function position(r: Pratique, date: string): number {
	const n = r.elements?.length ?? 0;
	return n ? pas(date, uniteDe(r)) % n : 0;
}

export function elementDu(r: Pratique, date: string): ElementRoue | undefined {
	return r.elements?.[position(r, date)];
}

/** Nombre de jours avant que toutes les roues quotidiennes données retrouvent ensemble leur position. */
export function grandCycle(nombres: number[]): number {
	const pgcd = (a: number, b: number): number => (b ? pgcd(b, a % b) : a);
	return nombres.filter((n) => n > 0).reduce((m, n) => (m * n) / pgcd(m, n), 1);
}

