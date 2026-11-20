/** Chargement du programme livré (static/data/programme/programme.json, copié par scripts/seed.mjs). */
import type { Programme } from './types.ts';

let cache: Promise<Programme | null> | undefined;

export function chargerProgramme(fetchFn: typeof fetch = fetch): Promise<Programme | null> {
	cache ??= fetchFn('/data/programme/programme.json')
		.then((r) => (r.ok ? (r.json() as Promise<Programme>) : null))
		.catch(() => null)
		.then((p) => {
			if (!p) cache = undefined; // échec (hors ligne au premier lancement) : on réessaiera
			return p;
		});
	return cache;
}
