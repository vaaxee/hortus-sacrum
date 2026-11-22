/** Apparence choisie par l'utilisateur : thème (jour, nuit, automatique) et direction artistique. */
import { writable } from 'svelte/store';

export type Theme = 'auto' | 'jour' | 'nuit';
export type Direction = 'latine' | 'grecque';

export const theme = writable<Theme>('auto');
export const direction = writable<Direction>('latine');
/**
 * Mode église (décision du 22 nov.) : grand corps de texte et écran qui reste allumé, pour prier à l'église. Le choix
 * est gardé sur l'appareil ; il ne s'applique que sur les pages qui le proposent (pratique, office), par ModeEglise.svelte.
 */
export const eglise = writable(false);

/** L'appareil peut refuser le stockage (navigation privée, données bloquées) : l'app marche alors sans mémoire. */
function lire(cle: string): string | null {
	try {
		return localStorage.getItem(cle);
	} catch {
		return null;
	}
}
function garder(cle: string, valeur: string) {
	try {
		localStorage.setItem(cle, valeur);
	} catch {
		/* rien à garder */
	}
}

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
	let t = (lire('hs-theme') as Theme) ?? 'auto';
	let d = (lire('hs-da') as Direction) ?? 'latine';
	theme.set(t);
	direction.set(d);
	eglise.set(lire('hs-eglise') === 'oui');
	eglise.subscribe((v) => garder('hs-eglise', v ? 'oui' : 'non'));
	appliquer(t, d);
	theme.subscribe((v) => {
		t = v;
		garder('hs-theme', v);
		appliquer(t, d);
	});
	// thème automatique : la couleur suit aussi le passage jour / nuit du système
	matchMedia('(prefers-color-scheme: dark)').addEventListener('change', couleurDeLApp);
	direction.subscribe((v) => {
		d = v;
		garder('hs-da', v);
		appliquer(t, d);
	});
}
