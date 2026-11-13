/** Apparence choisie par l'utilisateur : thème (jour, nuit, automatique) et direction artistique. */
import { writable } from 'svelte/store';

export type Theme = 'auto' | 'jour' | 'nuit';
export type Direction = 'latine' | 'grecque';

export const theme = writable<Theme>('auto');
export const direction = writable<Direction>('latine');

function appliquer(t: Theme, d: Direction) {
	const html = document.documentElement;
	if (t === 'auto') delete html.dataset.theme;
	else html.dataset.theme = t;
	if (d === 'grecque') html.dataset.da = 'grecque';
	else delete html.dataset.da;
}

/** À appeler une fois au démarrage : relit les choix gardés sur l'appareil et les applique. */
export function initialiserApparence() {
	let t = (localStorage.getItem('hs-theme') as Theme) ?? 'auto';
	let d = (localStorage.getItem('hs-da') as Direction) ?? 'latine';
	theme.set(t);
	direction.set(d);
	appliquer(t, d);
	theme.subscribe((v) => {
		t = v;
		localStorage.setItem('hs-theme', v);
		appliquer(t, d);
	});
	direction.subscribe((v) => {
		d = v;
		localStorage.setItem('hs-da', v);
		appliquer(t, d);
	});
}
