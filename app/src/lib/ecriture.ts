/**
 * Lectures de l'Écriture : latin (Vulgate clémentine) et français (Crampon 1923), un fichier par livre dans
 * data/ecriture. Chacun garde sa numérotation (Crampon suit l'hébreu et le grec : psaumes, Siracide, Jn 6…) ;
 * une référence peut donc donner à part celle de la Vulgate : « Ps 51 | 50 », « Si 7, 36 | 7, 40 ».
 */
import { LIVRES } from './livres-bible.ts';
import { pas, uniteDe } from './roues-calcul.ts';
import type { ElementRoue, Pratique } from './types.ts';

export type Verset = [number, string];
export interface Chapitre {
	n: number;
	la: Verset[];
	fr: Verset[];
}
export interface Livre {
	id: string;
	abr: string;
	titre: string;
	chapitres: Chapitre[];
}
type Source = Record<'fr' | 'la', { ouvrage: string; edition?: string; url: string }>;

export { LIVRES };

interface Lieu {
	chapitre: number;
	de?: number;
	a?: number;
}
/** Lieu dans Crampon ; « la » : lieu dans la Vulgate quand la numérotation diffère. */
export interface Ref extends Lieu {
	livre: string;
	la?: Lieu;
}

const LIEU = /^(\d+)(?:\s*,\s*(\d+)(?:\s*-\s*(\d+))?)?$/;
function lireLieu(s: string): Lieu | undefined {
	const m = s.trim().match(LIEU);
	if (!m) return;
	const de = m[2] ? +m[2] : undefined;
	return { chapitre: +m[1], de, a: m[3] ? +m[3] : de };
}

/** « Mt 5 », « Mt 5, 3 », « 1 Co 13, 4-7 », « Ps 51 | 50 » ; undefined si le livre n'est pas connu. */
export function lireRef(s: string): Ref | undefined {
	const [fr, la] = s.split('|');
	const m = fr.trim().match(/^(.+?)\s+(\d.*)$/);
	if (!m || !LIVRES[m[1]]) return;
	const l = lireLieu(m[2]);
	if (!l) return;
	const v = la ? lireLieu(la) : undefined;
	return { livre: m[1], ...l, ...(v ? { la: v } : {}) };
}

const ecrireLieu = (r: Lieu) => `${r.chapitre}${r.de ? `, ${r.de}${r.a && r.a !== r.de ? `-${r.a}` : ''}` : ''}`;
export const ecrireRef = (r: Ref) => `${r.livre} ${ecrireLieu(r)}${r.la ? ` | ${ecrireLieu(r.la)}` : ''}`;

export function enClair(r: Ref): string {
	const l = LIVRES[r.livre];
	return `${l?.nom ?? r.livre}, ${r.livre === 'Ps' ? 'psaume' : 'chapitre'} ${r.chapitre}${r.la && r.la.chapitre !== r.chapitre ? ` (${r.la.chapitre})` : ''}${r.de ? `, ${r.a && r.a !== r.de ? `versets ${r.de} à ${r.a}` : `verset ${r.de}`}` : ''}`;
}

/**
 * Passage à lire pour l'élément du jour d'une roue. Un livre seul (roue des évangélistes) donne le chapitre suivant
 * de ce livre : chaque évangéliste garde son marque-page, qui avance d'un chapitre chaque fois que son tour revient.
 */
export function lectureDu(r: Pratique, date: string, e?: ElementRoue): Ref | undefined {
	if (!e?.lecture) return;
	const l = LIVRES[e.lecture.trim()];
	if (!l) return lireRef(e.lecture);
	const n = r.elements?.length ?? 1;
	const tour = Math.floor(pas(date, uniteDe(r)) / n);
	return { livre: e.lecture.trim(), chapitre: (tour % l.chapitres) + 1 };
}

const cache = new Map<string, Promise<unknown>>();
function charger<T>(chemin: string, fetchFn: typeof fetch): Promise<T | null> {
	if (!cache.has(chemin))
		cache.set(
			chemin,
			fetchFn(`/data/ecriture/${chemin}`)
				.then((r) => (r.ok ? r.json() : null))
				.catch(() => null)
		);
	return cache.get(chemin) as Promise<T | null>;
}

/** Le passage : versets latins et français retenus, et la source (chaque livre est un fichier, chargé à la demande). */
export async function passage(r: Ref, fetchFn: typeof fetch = fetch) {
	const id = LIVRES[r.livre]?.id;
	if (!id) return;
	const [l, source] = await Promise.all([charger<Livre>(`${id}.json`, fetchFn), charger<Source>('source.json', fetchFn)]);
	const c = l?.chapitres.find((x) => x.n === r.chapitre);
	const cl = r.la ? l?.chapitres.find((x) => x.n === r.la!.chapitre) : c;
	if (!c || !source) return;
	const dans = (x: Lieu) => (v: Verset) => !x.de || (v[0] >= x.de && v[0] <= (x.a ?? x.de));
	/** Numérotations différentes : le latin suit sa propre référence, et ne se lit pas verset contre verset. */
	return { la: cl?.la.filter(dans(r.la ?? r)) ?? [], fr: c.fr.filter(dans(r)), source, decale: !!r.la, titre: l!.titre };
}
