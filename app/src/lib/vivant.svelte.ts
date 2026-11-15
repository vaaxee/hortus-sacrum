import { liveQuery } from 'dexie';

/**
 * Requête vivante Dexie qui suit ses paramètres : `fabrique` lit les valeurs réactives (date, id…) et rend la requête.
 * Quand l'une change, l'abonnement est refait ; quand la base change, la valeur se met à jour.
 * (Un store `vivant()` placé dans un `$derived` gardait l'abonnement du premier jour affiché.)
 * À appeler pendant l'initialisation d'un composant.
 */
export function vivantSelon<T>(fabrique: () => () => Promise<T>, initial: T): { readonly v: T } {
	let v = $state.raw(initial);
	$effect(() => {
		const requete = fabrique();
		v = initial;
		const abo = liveQuery(requete).subscribe({ next: (x) => (v = x), error: (e) => console.error(e) });
		return () => abo.unsubscribe();
	});
	return {
		get v() {
			return v;
		}
	};
}
