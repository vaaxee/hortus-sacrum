import { redirect } from '@sveltejs/kit';

/** « Régler la liste » est devenu « Régler le programme » (refonte du 18 novembre). */
export function load() {
	redirect(308, '/programme');
}
