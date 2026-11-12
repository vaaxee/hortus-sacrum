/**
 * Balisage léger des textes :
 *   *italique*          → italique
 *   [r]texte[/r]        → rouge (rubrique)
 *   ℣. … / ℟. …         → verset et répons (le signe est en rouge)
 *   ## Titre            → intertitre
 *   ligne vide          → nouveau paragraphe ; retour simple → retour à la ligne
 */

function echapper(s: string): string {
	return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function enLigne(s: string): string {
	let h = echapper(s);
	h = h.replace(/\[r\]([\s\S]*?)\[\/r\]/g, '<span class="rub">$1</span>');
	h = h.replace(/\*([^*\n]+)\*/g, '<em>$1</em>');
	h = h.replace(/^(℣\.|℟\.)/gm, '<span class="vr">$1</span>');
	return h.replace(/\n/g, '<br>');
}

/** Rend le balisage en HTML sûr (tout le reste est échappé). */
export function rendre(corps: string): string {
	return corps
		.replace(/\r\n?/g, '\n')
		.split(/\n{2,}/)
		.map((p) => p.trim())
		.filter(Boolean)
		.map((p) => {
			if (p.startsWith('## ')) return `<h3>${enLigne(p.slice(3))}</h3>`;
			const cls = /^(℣\.|℟\.)/.test(p) ? ' class="verset"' : '';
			return `<p${cls}>${enLigne(p)}</p>`;
		})
		.join('\n');
}

/** Texte nu, pour la recherche. */
export function nu(corps: string): string {
	return corps.replace(/\[\/?r\]|\*|^## /gm, '');
}

export function sansAccents(s: string): string {
	return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
}

export interface Nettoyage {
	texte: string;
	/** Ce que le nettoyage a changé, pour l'aperçu. */
	rapport: string[];
}

/**
 * Nettoie un texte collé (page web, PDF, OCR) sans en changer les mots :
 * mots coupés en fin de ligne, sauts de ligne parasites, espaces doubles, ℣ et ℟.
 */
export function nettoyer(brut: string): Nettoyage {
	const rapport: string[] = [];
	let t = brut.replace(/\r\n?/g, '\n').replace(/­/g, '');

	const compter = (re: RegExp, s: string) => (s.match(re) ?? []).length;

	// ℣ et ℟ écrits V. / R. / V/ / R/ en début de ligne
	// Un « V. » n'est pris pour un verset que s'il est suivi d'un « R. » (sinon : chiffre romain V).
	const reV = /^[ \t]*(?:V\/|℣\.?|[Vv]\.)[ \t]*(?=\S)/;
	const reR = /^[ \t]*(?:R\/|℟\.?|[Rr]\.|R[xX]\.)[ \t]*(?=\S)/;
	const lignes0 = t.split('\n');
	let vr = 0;
	for (let i = 0; i < lignes0.length; i++) {
		if (!reV.test(lignes0[i])) continue;
		let j = i + 1;
		while (j < lignes0.length && j <= i + 4 && !reR.test(lignes0[j]) && !reV.test(lignes0[j])) j++;
		if (j < lignes0.length && reR.test(lignes0[j])) {
			lignes0[i] = lignes0[i].replace(reV, '℣. ');
			lignes0[j] = lignes0[j].replace(reR, '℟. ');
			vr += 2;
		}
	}
	t = lignes0.join('\n');
	if (vr) rapport.push(`${vr} verset(s) et répons reconnus (℣, ℟)`);

	// mots coupés en fin de ligne : « misé-\nricorde » → « miséricorde »
	const coupes = compter(/(\p{Ll})-\n[ \t]*(\p{Ll})/gu, t);
	t = t.replace(/(\p{Ll})-\n[ \t]*(\p{Ll})/gu, '$1$2');
	if (coupes) rapport.push(`${coupes} mot(s) coupé(s) en fin de ligne recollé(s)`);

	// paragraphes : une ligne vide sépare ; les retours simples à l'intérieur sont des coupures de mise en page
	const blocs = t.split(/\n[ \t]*\n+/);
	let joints = 0;
	const propres = blocs.map((b) => {
		const lignes = b.split('\n').map((l) => l.trim()).filter(Boolean);
		if (!lignes.length) return '';
		// vers, litanies, versets : lignes courtes ou commençant par ℣/℟ → on garde les retours
		const moy = lignes.reduce((n, l) => n + l.length, 0) / lignes.length;
		const liturgique = lignes.some((l) => /^(℣\.|℟\.)/.test(l));
		if (liturgique) {
			// on recolle seulement les lignes de suite (qui ne commencent pas par ℣/℟)
			const out: string[] = [];
			for (const l of lignes) {
				if (/^(℣\.|℟\.)/.test(l) || !out.length) out.push(l);
				else {
					out[out.length - 1] += ' ' + l;
					joints++;
				}
			}
			return out.join('\n');
		}
		if (moy < 45) return lignes.join('\n');
		// une première ligne courte, sans ponctuation de suite, devant un paragraphe : c'est un titre
		const max = Math.max(...lignes.map((l) => l.length));
		if (
			lignes.length > 2 &&
			lignes[0].length < 0.6 * max &&
			!/[,;:]$/.test(lignes[0]) &&
			/^\p{Lu}/u.test(lignes[1])
		) {
			joints += lignes.length - 2;
			return lignes[0] + '\n\n' + lignes.slice(1).join(' ');
		}
		joints += lignes.length - 1;
		return lignes.join(' ');
	});
	if (joints) rapport.push(`${joints} saut(s) de ligne parasite(s) retiré(s)`);
	t = propres.filter(Boolean).join('\n\n');

	const doubles = compter(/[ \t]{2,}/g, t);
	t = t.replace(/[ \t]{2,}/g, ' ');
	if (doubles) rapport.push(`${doubles} espace(s) double(s) réduit(s)`);

	// typographie française minimale, sans toucher aux mots
	t = t.replace(/ ([;:!?»])/g, ' $1').replace(/« /g, '« ').replace(/'/g, '’');

	return { texte: t.trim(), rapport };
}
