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
	couleurDeLApp();
}

/**
 * Couleur de l'app installée (barre d'état, écran du lancement) : celle du fond de la direction et du thème choisis
 * (décision du 22 nov.). Une seule balise theme-color, recalculée à chaque changement.
 */
function couleurDeLApp() {
	const fond = getComputedStyle(document.body).backgroundColor;
	if (!fond) return;
	const metas = [...document.querySelectorAll<HTMLMetaElement>('meta[name="theme-color"]')];
	const m = metas.shift() ?? document.head.appendChild(Object.assign(document.createElement('meta'), { name: 'theme-color' }));
	for (const x of metas) x.remove();
	m.removeAttribute('media');
	m.content = fond;
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
	// thème automatique : la couleur suit aussi le passage jour / nuit du système
	matchMedia('(prefers-color-scheme: dark)').addEventListener('change', couleurDeLApp);
	direction.subscribe((v) => {
		d = v;
		localStorage.setItem('hs-da', v);
		appliquer(t, d);
	});
}
