/**
 * Psautier du Bréviaire romain en français : L.-Cl. Fillion, *Le nouveau psautier du Bréviaire romain*, 7e éd., Paris,
 * Lecoffre-Gabalda, 1917 (*imprimatur* Paris, 4 juin 1912), traduit de la Vulgate ; transcrit sur le scan
 * (data/office/breviaire-fr/psautier-fillion.json, chaîne engine/recueils/relecture/fillion, contrôle
 * engine/office/test_psautier_fr.py). Décision de l'utilisateur du 22 nov. 2026 : Fillion pour les psaumes, Hugueny pour
 * le reste (REFONTE § 5.5).
 *
 * Le latin reste le texte de l'office (CLAUDE.md § 15) : ce module ne change pas le corps de l'heure, il le rend en HTML
 * en plaçant le français en regard de chaque psaume. Un verset français est mis en face des lignes latines où il commence
 * (`ligne_la`, étiquettes de Divinum Officium : « 2a », « 2b »…) jusqu'à la ligne où commence le verset suivant. Un
 * cantique (ou le psaume invitatoire) que Fillion coupe autrement que Divinum Officium n'a pas d'étiquettes : le
 * français est alors donné en un bloc, après le latin. Si le nombre de lignes latines ne correspond pas aux étiquettes,
 * le latin est rendu seul (jamais un français en face du mauvais latin).
 */
import { rendre } from '../markup.ts';

export interface VersetFr {
	n: number;
	fr: string;
	page: number;
	/** Étiquette de la ligne latine (Divinum Officium) où le verset commence. */
	ligne_la?: string;
	lecture?: string[];
}

export interface PieceFr {
	/** Numéro du psaume (Vulgate) ; absent pour un cantique. */
	numero?: number;
	/** Fichier de Divinum Officium d'un cantique (« Psalm231 »). */
	do?: string;
	titre: string;
	reference?: string;
	versets: VersetFr[];
	/** Étiquettes des lignes latines de Divinum Officium ; absentes quand l'alignement ligne à ligne n'est pas possible. */
	lignes_la?: string[];
	note?: string;
	pages: number[];
}

export interface PsautierFr {
	titre: string;
	source: { ouvrage: string; auteur: string; edition: string; approbation: string; url: string; page: string };
	psaumes: PieceFr[];
	cantiques: PieceFr[];
}

/** Référence imprimée par Divinum Officium sous « Canticum … » → fichier Psalterium/Psalmorum/PsalmNNN.txt. */
const CANTIQUES: Record<string, string> = {
	'Dan 3:57-88,56': 'Psalm210',
	'1 Par. 29:10-13': 'Psalm211',
	'Tob. 13:1-11': 'Psalm212',
	'Judith 16:15-22': 'Psalm213',
	'Jer 31:10-18': 'Psalm214',
	'Isa 45:15-30': 'Psalm215',
	'Sir 36:1-16': 'Psalm216',
	'Dan 3:52-57': 'Psalm220',
	'Isa 12:1-7': 'Psalm221',
	'Isa 38:10-24': 'Psalm222',
	'3 Reg 2:1-16': 'Psalm223',
	'Exod. 15:1-22': 'Psalm224',
	'Hab 3:2-19': 'Psalm225',
	'Deut 32:1-65': 'Psalm226',
	'Luc. 1:68-79': 'Psalm231',
	'Luc. 1:46-55': 'Psalm232',
	'Luc. 2:29-32': 'Psalm233'
};

const TETE_PSAUME = /^\[r\]Psalmus (\d+)(?:\((\d+[a-z]?)-(\d+[a-z]?)\))?\[\/r\]$/;
const TETE_CANTIQUE = /^\[r\]Canticum [^[]*\[\/r\]$/;
const REF = /^\[r\](.*)\[\/r\]$/;
/** Lignes du psaume qui ne sont pas du texte chanté : rubriques, Gloria (℣. ℟.), renvois. */
const horsTexte = (l: string) => !l.trim() || /^(\[r\]|℣\.|℟\.|&|\$)/.test(l);

type Cle = [number, string];
const cle = (lab: string): Cle => {
	const m = /^(\d+)([a-z]?)$/.exec(lab);
	return m ? [Number(m[1]), m[2]] : [1e6, ''];
};
const avant = (x: Cle, y: Cle) => x[0] < y[0] || (x[0] === y[0] && x[1] < y[1]);

/** Les étiquettes d'une partie de psaume « Psalmus N(a-b) » (même règle que engine/office/test_psautier_fr.py). */
export function etiquettesDeLaPartie(labs: string[], de?: string, a?: string): string[] {
	const tous = labs.filter((l) => l !== 'doxologie');
	if (!de || !a) return tous;
	const d = cle(de);
	const f = cle(a);
	let sel = tous.filter((l) => {
		const c = cle(l);
		return !avant(c, d) && (c[0] < f[0] || (c[0] === f[0] && (!f[1] || c[1] <= f[1])));
	});
	if (f[1] === 'a') sel = sel.filter((l) => !(cle(l)[0] === f[0] && cle(l)[1] === ''));
	return sel;
}

/** Index des pièces : psaumes par numéro, cantiques par fichier de Divinum Officium. */
export function indexer(p: PsautierFr): { psaumes: Map<number, PieceFr>; cantiques: Map<string, PieceFr> } {
	return {
		psaumes: new Map(p.psaumes.map((x) => [x.numero!, x])),
		cantiques: new Map(p.cantiques.map((x) => [x.do!, x]))
	};
}

export interface Bloc {
	/** Lignes latines (balisage du Bréviaire). */
	la: string[];
	/** Le français en regard (un ou plusieurs versets), ou rien. */
	fr?: string;
}

/**
 * Aligne les lignes latines d'un psaume (ou d'une partie) sur les versets de Fillion : une suite de blocs latin/français,
 * ou null si l'alignement n'est pas possible (pas d'étiquettes, nombre de lignes différent).
 */
export function aligner(piece: PieceFr, latin: string[], de?: string, a?: string): Bloc[] | null {
	if (!piece.lignes_la) return null;
	const sel = etiquettesDeLaPartie(piece.lignes_la, de, a);
	if (sel.length !== latin.length || !sel.length) return null;
	const debuts = new Map<number, string[]>();
	for (const v of piece.versets) {
		const i = v.ligne_la === undefined ? -1 : sel.indexOf(v.ligne_la);
		if (i < 0) continue;
		debuts.set(i, [...(debuts.get(i) ?? []), v.fr]);
	}
	const blocs: Bloc[] = [];
	latin.forEach((l, i) => {
		const fr = debuts.get(i);
		if (fr || !blocs.length) blocs.push({ la: [l], fr: fr?.join(' ') });
		else blocs[blocs.length - 1].la.push(l);
	});
	return blocs;
}

const html = (latin: string) => rendre(latin).replace(/^<p>|<\/p>$/g, '');

function strophe(b: Bloc): string {
	const fr = b.fr ? `<div class="fr" lang="fr"><p>${html(b.fr)}</p></div>` : '<div class="fr"></div>';
	return `<div class="strophe"><div class="la" lang="la"><p>${html(b.la.join('\n'))}</p></div>${fr}</div>`;
}

function blocFrancais(piece: PieceFr): string {
	const tete = piece.reference ? `${piece.titre}. ${piece.reference}` : piece.titre;
	const vs = piece.versets.map((v) => html(v.fr)).join('<br>');
	return `<div class="fr-bloc" lang="fr"><p class="rub">${html(tete)}</p><p>${vs}</p></div>`;
}

/** Un paragraphe du Bréviaire en HTML, le français de Fillion en regard s'il porte un psaume ou un cantique. */
export function rendreParagraphe(p: string, idx: ReturnType<typeof indexer>): string {
	const lignes = p.split('\n');
	const t = lignes.findIndex((l) => TETE_PSAUME.test(l.trim()) || TETE_CANTIQUE.test(l.trim()));
	if (t < 0) return rendre(p);
	let piece: PieceFr | undefined;
	let de: string | undefined;
	let a: string | undefined;
	let corps = t + 1;
	const m = TETE_PSAUME.exec(lignes[t].trim());
	if (m) {
		piece = idx.psaumes.get(Number(m[1]));
		[de, a] = [m[2], m[3]];
	} else {
		const ref = REF.exec((lignes[t + 1] ?? '').trim());
		piece = ref ? idx.cantiques.get(CANTIQUES[ref[1]] ?? '') : undefined;
		corps = t + 2;
	}
	if (!piece) return rendre(p);
	// le texte chanté : lignes suivies jusqu'à la première ligne hors texte (Gloria, rubrique)
	let fin = corps;
	while (fin < lignes.length && !horsTexte(lignes[fin])) fin++;
	const latin = lignes.slice(corps, fin);
	const tete = lignes.slice(0, corps).join('\n');
	const queue = lignes.slice(fin).join('\n');
	const blocs = aligner(piece, latin, de, a);
	// sans alignement : le paragraphe latin entier (antiennes intercalées comprises), puis le français en un bloc
	if (!blocs) return `${rendre(p)}${blocFrancais(piece)}`;
	const milieu = `<div class="psaume bilingue">${blocs.map(strophe).join('')}</div>`;
	return `${rendre(tete)}${milieu}${queue.trim() ? rendre(queue) : ''}`;
}

/** Le corps d'une heure en HTML (comme `rendre`), le français de Fillion en regard des psaumes et cantiques. */
export function rendreAvecFillion(corps: string, p: PsautierFr): string {
	const idx = indexer(p);
	return corps
		.replace(/\r\n?/g, '\n')
		.split(/\n{2,}/)
		.map((x) => x.trim())
		.filter(Boolean)
		.map((x) => rendreParagraphe(x, idx))
		.join('\n');
}

let chargement: Promise<PsautierFr | null> | undefined;

/** Le psautier de Fillion (static/data/office/breviaire-fr/psautier-fillion.json), chargé une fois. */
export function chargerPsautierFr(fetchFn: typeof fetch = fetch): Promise<PsautierFr | null> {
	chargement ??= fetchFn('/data/office/breviaire-fr/psautier-fillion.json')
		.then((r) => (r.ok ? (r.json() as Promise<PsautierFr>) : null))
		.catch(() => null);
	void chargement.then((d) => {
		if (!d) chargement = undefined;
	});
	return chargement;
}
