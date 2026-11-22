/**
 * Somme théologique (lot 10 ; SPEC § 11, REFONTE § 5.6) : un article par jour, à la suite depuis la Iª pars, q. 1, a. 1.
 * Français de Lachat (Vivès), latin de l'édition léonine en regard ; données data/somme (engine/somme/construire.py).
 *
 * Marque-page : meta « marque-somme » = { ref, date } du dernier article lu (réglage de l'appareil, comme les
 * recueils masqués). L'article du jour est celui qui suit le marque-page ; lu aujourd'hui, il reste celui du jour.
 */
import { db } from './db.ts';

export interface Bilingue {
	la: string;
	fr: string;
}
export interface Article {
	ref: string;
	titre: Bilingue;
	objections: Bilingue[];
	sed_contra: Bilingue;
	respondeo: Bilingue;
	reponses: Bilingue[];
	pages: { fr: [number, number] };
	/** Manques de l'édition (ex. « Sed contra » non traduit par Lachat). */
	notes?: string[];
}
interface SourceEdition {
	ouvrage: string;
	edition: string;
	url: string;
	relecture?: string;
}
export interface Question {
	ref: string;
	partie: string;
	question: number;
	titre: Bilingue;
	prooemium: Bilingue;
	articles: Article[];
	source: { fr: SourceEdition; la: SourceEdition; pages_fr: [number, number] };
	revision: number;
}
export interface EntreeIndex {
	ref: string;
	fichier: string;
	question: number;
	article: number;
}
export interface IndexSomme {
	note: string;
	articles: EntreeIndex[];
}
export interface Marque {
	ref: string;
	date: string;
}

export const CLE_MARQUE = 'marque-somme';
/** Coche de la lecture du jour (programme : lec:doctrine). */
export const LECTURE = 'lec:doctrine';

/**
 * L'article du jour d'après le marque-page : le suivant du dernier lu ; le même s'il a été lu ce jour-là ; le premier
 * sans marque-page. « fin » : tous les articles livrés sont lus (le dernier reste affiché).
 */
export function articleDuJour(index: IndexSomme, marque: Marque | undefined, date: string): { entree: EntreeIndex; fin: boolean } {
	const a = index.articles;
	if (!marque) return { entree: a[0], fin: false };
	const i = a.findIndex((x) => x.ref === marque.ref);
	if (i < 0) return { entree: a[0], fin: false };
	if (marque.date === date) return { entree: a[i], fin: false };
	if (i + 1 >= a.length) return { entree: a[i], fin: true };
	return { entree: a[i + 1], fin: false };
}

/** Article précédent et suivant dans l'ordre de lecture. */
export function voisins(index: IndexSomme, ref: string): { avant?: EntreeIndex; apres?: EntreeIndex } {
	const i = index.articles.findIndex((x) => x.ref === ref);
	return i < 0 ? {} : { avant: index.articles[i - 1], apres: index.articles[i + 1] };
}

const caches = new Map<string, Promise<unknown>>();
function charger<T>(chemin: string, fetchFn: typeof fetch): Promise<T | null> {
	let p = caches.get(chemin);
	if (!p) {
		p = fetchFn(`/data/somme/${chemin}`)
			.then((r) => (r.ok ? r.json() : null))
			.catch(() => null);
		caches.set(chemin, p);
	}
	return p as Promise<T | null>;
}
export const chargerIndex = (fetchFn: typeof fetch = fetch) => charger<IndexSomme>('index.json', fetchFn);
export const chargerQuestion = (fichier: string, fetchFn: typeof fetch = fetch) => charger<Question>(fichier, fetchFn);

export async function lireMarque(): Promise<Marque | undefined> {
	return (await db.meta.get(CLE_MARQUE))?.valeur as Marque | undefined;
}

/** « J'ai lu cet article » : le marque-page avance et la lecture du jour est cochée. */
export async function marquerLu(ref: string, date: string): Promise<void> {
	await db.meta.put({ cle: CLE_MARQUE, valeur: { ref, date } satisfies Marque });
	const deja = await db.coches.where('[date+elementId]').equals([date, LECTURE]).count();
	if (!deja) await db.coches.add({ date, elementId: LECTURE, rang: 0, horodatage: new Date().toISOString() });
}
