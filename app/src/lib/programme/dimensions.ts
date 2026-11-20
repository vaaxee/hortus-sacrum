/**
 * Dimensions des textes (lot « Dimensions ») : vocabulaire fermé et classement livré, chargés une fois.
 * Données : static/data/programme/dimensions.json et static/data/prieres/dimensions-textes.json (scripts/seed.mjs).
 */
import type { ClassementTexte, Vocabulaire } from './types.ts';

function charger<T>(chemin: string, fetchFn: typeof fetch): Promise<T | null> {
	return fetchFn(chemin)
		.then((r) => (r.ok ? (r.json() as Promise<T>) : null))
		.catch(() => null);
}

let vocabulaire: Promise<Vocabulaire | null> | undefined;
let classements: Promise<Record<string, ClassementTexte> | null> | undefined;

export function chargerVocabulaire(fetchFn: typeof fetch = fetch): Promise<Vocabulaire | null> {
	vocabulaire ??= charger<Vocabulaire>('/data/programme/dimensions.json', fetchFn).then((v) => {
		if (!v) vocabulaire = undefined; // hors ligne au premier lancement : on réessaiera
		return v;
	});
	return vocabulaire;
}

export function chargerClassements(fetchFn: typeof fetch = fetch): Promise<Record<string, ClassementTexte> | null> {
	classements ??= charger<{ textes: Record<string, ClassementTexte> }>('/data/prieres/dimensions-textes.json', fetchFn).then((c) => {
		if (!c) classements = undefined;
		return c?.textes ?? null;
	});
	return classements;
}
