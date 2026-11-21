/**
 * Opérations sur le corps d'un texte (balisage de markup.ts) : extraits par ancres, coupures pour les points
 * d'insertion, et recherche d'un texte contenu dans un autre (test d'unicité). Fonctions pures.
 */
import type { Coupure, Extrait } from './types.ts';

const niveauDe = (ligne: string) => /^(#{1,6}) /.exec(ligne)?.[1].length ?? 0;

/** Position de fin d'une section commencée à `debut` (titre de niveau n) : titre suivant de niveau ≤ n, ou la fin. */
function finDeSection(corps: string, debut: number, niveau: number): number {
	const re = /^(#{1,6}) /gm;
	re.lastIndex = corps.indexOf('\n', debut) + 1 || corps.length;
	for (let m = re.exec(corps); m; m = re.exec(corps)) if (m[1].length <= niveau) return m.index;
	return corps.length;
}

/** Début de la ligne exacte `ligne` (ligne entière), ou -1. */
function ligneExacte(corps: string, ligne: string): number {
	let i = corps.indexOf(ligne);
	while (i >= 0) {
		const debut = i === 0 || corps[i - 1] === '\n';
		const fin = i + ligne.length === corps.length || corps[i + ligne.length] === '\n';
		if (debut && fin) return i;
		i = corps.indexOf(ligne, i + 1);
	}
	return -1;
}

/**
 * La partie du corps désignée par l'extrait, ou null si une ancre manque (le texte a changé : on ne devine pas).
 * `rang` : rang du jour dans une série (pour `rang_du_jour`).
 */
export function extraire(corps: string, ex: Extrait | undefined, rang = 0): string | null {
	if (!ex) return corps;
	let t = corps;
	if (ex.section !== undefined) {
		const i = ligneExacte(t, ex.section);
		if (i < 0) return null;
		t = t.slice(i, finDeSection(t, i, niveauDe(ex.section)));
	}
	if (ex.rang_du_jour) {
		const n = ex.rang_du_jour.niveau;
		const titres = [...t.matchAll(new RegExp(`^#{${n}} .*$`, 'gm'))];
		const m = titres[rang - 1];
		if (!m || m.index === undefined) return null;
		t = t.slice(m.index, finDeSection(t, m.index, n));
	}
	if (ex.de !== undefined) {
		const i = t.indexOf(ex.de);
		if (i < 0) return null;
		t = t.slice(i);
	}
	if (ex.a !== undefined) {
		const i = t.indexOf(ex.a);
		if (i < 0) return null;
		t = t.slice(0, i);
	}
	if (ex.phrase !== undefined) {
		if (!t.includes(ex.phrase)) return null;
		t = ex.phrase;
	}
	if (ex.paras) {
		t = t
			.split(/\n\s*\n/)
			.slice(ex.paras[0], ex.paras[1])
			.join('\n\n');
	}
	if (ex.retirer?.length) {
		const paras = t.split(/\n\s*\n/);
		if (!ex.retirer.every((r) => paras.some((p) => p.trim() === r))) return null;
		t = paras.filter((p) => !ex.retirer!.includes(p.trim())).join('\n\n');
	}
	if (ex.niveau) t = t.replace(/^## /gm, `${'#'.repeat(2 + ex.niveau)} `);
	return t.trim();
}

/** Une partie d'un texte hôte coupé, suivie des points d'insertion qui viennent après elle. */
export interface Morceau {
	/** Absent : le texte entier. */
	extrait?: Extrait;
	/** Morceau sans texte (points placés au tout début). */
	vide?: true;
	points: string[];
}

/**
 * Coupe un texte aux points d'insertion. Chaque morceau est désigné par des ancres (`de`, `a`) prises dans le texte,
 * pour que la page se compose à l'affichage sans recopier le texte. Renvoie null si une ancre manque.
 */
export function couper(corps: string, coupures: Coupure[]): Morceau[] | null {
	// coupes : position, ancre qui commence le morceau suivant, points placés avant
	const coupes: { pos: number; ancre: string; points: string[] }[] = [];
	const finale: string[] = [];
	const ajouter = (pos: number, point: string) => {
		if (pos >= corps.length) return void finale.push(point);
		const c = coupes.find((x) => x.pos === pos);
		if (c) c.points.push(point);
		else {
			const finLigne = corps.indexOf('\n', pos);
			coupes.push({ pos, ancre: corps.slice(pos, finLigne < 0 ? corps.length : finLigne), points: [point] });
		}
	};
	for (const c of coupures) {
		if (c.avant !== undefined) {
			const i = corps.indexOf(c.avant);
			if (i < 0) return null;
			ajouter(i, c.point);
		}
		if (c.apres_chaque) {
			const { niveau, motif } = c.apres_chaque;
			const re = new RegExp(`^#{${niveau}} (.*)$`, 'gm');
			let n = 0;
			for (const m of corps.matchAll(re)) {
				if (!new RegExp(motif, 'u').test(m[1]) || m.index === undefined) continue;
				ajouter(finDeSection(corps, m.index, niveau), c.point);
				n++;
			}
			if (!n) return null;
		}
	}
	coupes.sort((a, b) => a.pos - b.pos);
	if (!coupes.length) return [{ points: finale }];
	const morceaux: Morceau[] = [];
	// avant la première coupe : le début du texte, ou rien si la coupe est au tout début
	morceaux.push(
		coupes[0].pos > 0 ? { extrait: { a: coupes[0].ancre }, points: coupes[0].points } : { vide: true, points: coupes[0].points }
	);
	for (let k = 1; k < coupes.length; k++) {
		morceaux.push({ extrait: { de: coupes[k - 1].ancre, a: coupes[k].ancre }, points: coupes[k].points });
	}
	morceaux.push({ extrait: { de: coupes[coupes.length - 1].ancre }, points: finale });
	return morceaux;
}

// ------------------------------------------------------------------ inclusion

/** Texte réduit aux mots : sans rubriques, balisage, accents ni ponctuation ; en minuscules. */
export function normaliser(s: string): string {
	return s
		.replace(/\[r\][\s\S]*?\[\/r\]/g, ' ')
		.replace(/^#{1,6} .*$/gm, ' ')
		.replace(/[*_]/g, ' ')
		.normalize('NFD')
		.replace(/[̀-ͯ]/g, '')
		.toLowerCase()
		.replace(/æ/g, 'ae')
		.replace(/œ/g, 'oe')
		.replace(/[^a-z0-9]+/g, ' ')
		.trim();
}

/** Longueur des fragments comparés (en mots). */
export const FRAGMENT = 8;

/** Fragments de FRAGMENT mots consécutifs, après retrait des formules communes (déjà normalisées). */
export function fragments(s: string, formules: string[] = []): Set<string> {
	let n = ` ${normaliser(s)} `;
	for (const f of formules) if (f) n = n.split(` ${f} `).join(' | ');
	const out = new Set<string>();
	for (const morceau of n.split('|')) {
		const mots = morceau.split(' ').filter(Boolean);
		for (let i = 0; i + FRAGMENT <= mots.length; i++) out.add(mots.slice(i, i + FRAGMENT).join(' '));
	}
	return out;
}

/** Part des fragments de `a` qu'on retrouve dans `b` (0 si `a` est trop court pour être comparé). */
export function partIncluse(a: Set<string>, b: Set<string>): number {
	if (!a.size) return 0;
	let n = 0;
	for (const f of a) if (b.has(f)) n++;
	return n / a.size;
}
