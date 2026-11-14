/**
 * Lectures de l'Écriture : les quatre Évangiles, latin (Vulgate clémentine) et français (Crampon 1923), dans
 * data/ecriture/evangiles.json. Chacun garde sa numérotation (Crampon suit le grec en Jn 6 et Mt 17).
 */
import { pas, uniteDe } from './roues-calcul.ts';
import type { ElementRoue, Pratique } from './types.ts';

export type Verset = [number, string];
export interface Chapitre { n: number; la: Verset[]; fr: Verset[] }
export interface Livre { id: string; titre: string; chapitres: Chapitre[] }
type Source = Record<'fr' | 'la', { ouvrage: string; edition?: string; url: string }>;

export const LIVRES: Record<string, { id: string; nom: string; chapitres: number }> = {
	Mt: { id: 'mt', nom: 'Saint Matthieu', chapitres: 28 },
	Mc: { id: 'mc', nom: 'Saint Marc', chapitres: 16 },
	Lc: { id: 'lc', nom: 'Saint Luc', chapitres: 24 },
	Jn: { id: 'jn', nom: 'Saint Jean', chapitres: 21 }
};

export interface Ref { livre: string; chapitre: number; de?: number; a?: number }

/** « Mt 5 », « Mt 5, 3 », « Mt 5, 3-10 » ; undefined si le livre n'est pas connu. */
export function lireRef(s: string): Ref | undefined {
	const m = s.trim().match(/^(\S+)\s+(\d+)(?:\s*,\s*(\d+)(?:\s*-\s*(\d+))?)?$/);
	if (!m || !LIVRES[m[1]]) return;
	const de = m[3] ? +m[3] : undefined;
	return { livre: m[1], chapitre: +m[2], de, a: m[4] ? +m[4] : de };
}

export const ecrireRef = (r: Ref) => `${r.livre} ${r.chapitre}${r.de ? `, ${r.de}${r.a && r.a !== r.de ? `-${r.a}` : ''}` : ''}`;

export function enClair(r: Ref): string {
	const l = LIVRES[r.livre];
	return `${l?.nom ?? r.livre}, chapitre ${r.chapitre}${r.de ? `, ${r.a && r.a !== r.de ? `versets ${r.de} à ${r.a}` : `verset ${r.de}`}` : ''}`;
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
	if (!cache.has(chemin)) cache.set(chemin, fetchFn(`/data/ecriture/${chemin}`).then((r) => (r.ok ? r.json() : null)).catch(() => null));
	return cache.get(chemin) as Promise<T | null>;
}

/** Le passage : versets latins et français retenus, et la source (chaque livre est un fichier, chargé à la demande). */
export async function passage(r: Ref, fetchFn: typeof fetch = fetch) {
	const id = LIVRES[r.livre]?.id;
	if (!id) return;
	const [l, source] = await Promise.all([charger<Livre>(`${id}.json`, fetchFn), charger<Source>('source.json', fetchFn)]);
	const c = l?.chapitres.find((x) => x.n === r.chapitre);
	if (!c || !source) return;
	const garde = (v: Verset) => !r.de || (v[0] >= r.de && v[0] <= (r.a ?? r.de));
	return { la: c.la.filter(garde), fr: c.fr.filter(garde), source };
}
