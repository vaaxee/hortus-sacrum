import { liveQuery } from 'dexie';
import { readable, type Readable } from 'svelte/store';

/** Requête vivante Dexie exposée comme store Svelte : l'écran se met à jour dès que la base change. */
export function vivant<T>(requete: () => Promise<T>, initial: T): Readable<T> {
	return readable(initial, (set) => {
		const abo = liveQuery(requete).subscribe({ next: set, error: (e) => console.error(e) });
		return () => abo.unsubscribe();
	});
}
