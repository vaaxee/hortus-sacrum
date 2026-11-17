/**
 * Import depuis un PDF ou une photo, entièrement dans le navigateur :
 * le fichier n'est envoyé nulle part. pdf.js lit le texte ; si la page est
 * scannée (ou si c'est une photo), Tesseract.js fait l'OCR en français et en latin.
 */
import { nettoyer } from './markup.ts';

export interface PageExtraite {
	page: number;
	texte: string;
	/** true si le texte vient de l'OCR (à relire de plus près). */
	ocr: boolean;
	/** Confiance moyenne de l'OCR, de 0 à 100. */
	confiance?: number;
}

export interface InfoPdf {
	pages: number;
	titre: string;
}

export type Progres = (message: string, fraction: number) => void;

/** En dessous de ce nombre de caractères, une page de PDF est tenue pour scannée. */
const SEUIL_TEXTE = 40;
const LANGUES = 'fra+lat';

type PdfDoc = import('pdfjs-dist').PDFDocumentProxy;

async function pdfjs() {
	const lib = await import('pdfjs-dist');
	const worker = (await import('pdfjs-dist/build/pdf.worker.min.mjs?url')).default;
	lib.GlobalWorkerOptions.workerSrc = worker;
	return lib;
}

export async function ouvrirPdf(fichier: File): Promise<{ doc: PdfDoc; info: InfoPdf }> {
	const lib = await pdfjs();
	const doc = await lib.getDocument({ data: await fichier.arrayBuffer() }).promise;
	let titre = '';
	try {
		const meta = await doc.getMetadata();
		titre = ((meta.info as Record<string, unknown>)?.Title as string) ?? '';
	} catch {
		/* pas de métadonnées */
	}
	return { doc, info: { pages: doc.numPages, titre: titre.trim() || fichier.name.replace(/\.pdf$/i, '') } };
}

/** Reconstitue les lignes d'une page d'après la position des fragments de texte. */
async function textePage(doc: PdfDoc, n: number): Promise<string> {
	const page = await doc.getPage(n);
	const contenu = await page.getTextContent();
	type Morceau = { x: number; y: number; h: number; s: string; w: number };
	const morceaux: Morceau[] = [];
	for (const it of contenu.items) {
		if (!('str' in it) || !it.str) continue;
		morceaux.push({ x: it.transform[4], y: it.transform[5], h: it.height || 10, s: it.str, w: it.width });
	}
	if (!morceaux.length) return '';
	const hauteurs = morceaux
		.filter((m) => m.s.trim())
		.map((m) => m.h)
		.sort((x, y) => x - y);
	const mediane = hauteurs[Math.floor(hauteurs.length / 2)] ?? 10;
	// lettrines : une ou deux lettres bien plus hautes que le texte courant
	const estLettrine = (m: Morceau) => m.h > mediane * 1.7 && m.s.trim().length <= 2 && /\p{L}/u.test(m.s);
	const lettrines = morceaux.filter(estLettrine);

	const lignes: { y: number; h: number; morceaux: Morceau[] }[] = [];
	for (const m of morceaux) {
		if (estLettrine(m)) continue;
		let ligne = lignes.find((l) => Math.abs(l.y - m.y) < Math.max(2, m.h * 0.4));
		if (!ligne) {
			ligne = { y: m.y, h: m.h, morceaux: [] };
			lignes.push(ligne);
		}
		ligne.morceaux.push(m);
		if (m.s.trim()) ligne.h = Math.max(ligne.h, m.h);
	}
	lignes.sort((a, b) => b.y - a.y);
	// la lettrine se rattache à la plus haute ligne qu'elle couvre
	const tete = new Map<(typeof lignes)[number], string>();
	for (const c of lettrines) {
		const couvertes = lignes.filter((l) => l.y >= c.y - 2 && l.y <= c.y + c.h && l.morceaux.some((m) => m.x > c.x));
		if (couvertes.length) tete.set(couvertes[0], (tete.get(couvertes[0]) ?? '') + c.s.trim());
	}
	const out: string[] = [];
	let precedente: (typeof lignes)[number] | undefined;
	for (const l of lignes) {
		l.morceaux.sort((a, b) => a.x - b.x);
		let s = '';
		let fin = -Infinity;
		for (const m of l.morceaux) {
			if (s && m.x - fin > l.h * 0.3 && !s.endsWith(' ') && !m.s.startsWith(' ')) s += ' ';
			s += m.s;
			fin = m.x + m.w;
		}
		s = (tete.get(l) ?? '') + s.trimEnd();
		if (!s.trim()) continue;
		// nouveau paragraphe : interligne nettement plus grand, ou changement de corps (titre, ligne « usage »)
		if (
			precedente &&
			(precedente.y - l.y > Math.max(precedente.h, l.h) * 1.9 || Math.abs(precedente.h - l.h) > Math.min(precedente.h, l.h) * 0.12)
		) {
			out.push('');
		}
		out.push(s);
		precedente = l;
	}
	// folio seul en tête ou en pied de page
	while (out.length && /^\d{1,4}$/.test(out[out.length - 1].trim() || '0')) out.pop();
	while (out.length && /^\d{1,4}$/.test(out[0].trim() || '0')) out.shift();
	return out.join('\n').trim();
}

async function rendrePage(doc: PdfDoc, n: number, echelle = 2.5): Promise<HTMLCanvasElement> {
	const page = await doc.getPage(n);
	const vue = page.getViewport({ scale: echelle });
	const canvas = document.createElement('canvas');
	canvas.width = Math.ceil(vue.width);
	canvas.height = Math.ceil(vue.height);
	await page.render({ canvas, viewport: vue }).promise;
	return canvas;
}

type Ouvrier = import('tesseract.js').Worker;
let ouvrier: Promise<Ouvrier> | undefined;

/** Lance (une seule fois) le moteur d'OCR ; les modèles de langue se téléchargent au premier usage. */
function moteurOcr(progres?: Progres): Promise<Ouvrier> {
	ouvrier ??= (async () => {
		const { createWorker } = await import('tesseract.js');
		return createWorker(LANGUES, 1, {
			logger: (m: { status: string; progress: number }) => {
				if (m.status.startsWith('loading') || m.status.startsWith('initializ')) {
					progres?.('Préparation de la reconnaissance de texte…', m.progress);
				}
			}
		});
	})();
	return ouvrier;
}

export async function arreterOcr(): Promise<void> {
	if (!ouvrier) return;
	const o = await ouvrier;
	ouvrier = undefined;
	await o.terminate();
}

interface MotOcr {
	text: string;
	confidence: number;
	bbox?: { x0: number; x1: number };
}
interface LigneOcr {
	words: MotOcr[];
}
interface BlocOcr {
	paragraphs: { lines: LigneOcr[] }[];
}

/** Un mot est tenu pour un parasite (ornement, bord de page) s'il est peu sûr et ne ressemble pas à un mot. */
function parasite(m: MotOcr): boolean {
	if (m.confidence >= 60) return false;
	const lettres = (m.text.match(/\p{L}/gu) ?? []).length;
	const vraiMot = /^[\p{L}’'-]{3,}[.,;:!?»]*$/u.test(m.text) && /\p{Ll}/u.test(m.text);
	return m.confidence < 35 || !vraiMot || lettres < m.text.length * 0.6;
}

/**
 * Recompose le texte reconnu en écartant les ornements : lignes dont la confiance
 * moyenne est basse, et mots parasites en début ou en fin de ligne.
 * On ne retire jamais un mot au milieu d'une ligne.
 */
export function filtrerOcr(blocs: BlocOcr[]): string {
	const paragraphes: string[] = [];
	for (const bloc of blocs) {
		for (const par of bloc.paragraphs) {
			const lignes: string[] = [];
			for (const l of par.lines) {
				const mots = l.words.filter((m) => m.text.trim());
				if (!mots.length) continue;
				const moyenne = mots.reduce((n, m) => n + m.confidence, 0) / mots.length;
				if (moyenne < 50) continue;
				let d = 0;
				let f = mots.length;
				while (d < f && parasite(mots[d])) d++;
				while (f > d && parasite(mots[f - 1])) f--;
				// en bord de ligne : un signe isolé, séparé du texte par un grand blanc, est un ornement
				const ecart = (i: number) => (mots[i].bbox && mots[i - 1].bbox ? mots[i].bbox!.x0 - mots[i - 1].bbox!.x1 : 0);
				const ecarts = mots
					.slice(1)
					.map((_, i) => ecart(i + 1))
					.filter((e) => e > 0)
					.sort((a, b) => a - b);
				const normal = ecarts[Math.floor(ecarts.length / 2)] ?? 0;
				const signe = (m: MotOcr) => !/\p{Ll}{2,}/u.test(m.text);
				if (normal > 0) {
					let coupe = -1;
					for (let i = Math.max(d + 1, f - 3); i < f; i++) {
						if (ecart(i) > normal * 1.8 && mots.slice(i, f).every(signe)) {
							coupe = i;
							break;
						}
					}
					if (coupe > 0) f = coupe;
					let debut = -1;
					for (let i = Math.min(f - 1, d + 3); i > d; i--) {
						if (ecart(i) > normal * 1.8 && mots.slice(d, i).every(signe)) {
							debut = i;
							break;
						}
					}
					if (debut > 0) d = debut;
				}
				const texte = mots
					.slice(d, f)
					.map((m) => m.text)
					.join(' ');
				if (texte.trim()) lignes.push(texte);
			}
			if (lignes.length) paragraphes.push(lignes.join('\n'));
		}
	}
	return paragraphes.join('\n\n');
}

async function ocr(image: HTMLCanvasElement | File | Blob, progres?: Progres): Promise<{ texte: string; confiance: number }> {
	const o = await moteurOcr(progres);
	const r = await o.recognize(image, {}, { text: true, blocks: true });
	const blocs = r.data.blocks as unknown as BlocOcr[] | null;
	const texte = blocs?.length ? filtrerOcr(blocs) : r.data.text.trim();
	return { texte, confiance: Math.round(r.data.confidence) };
}

/** Extrait les pages de..a d'un PDF ; passe à l'OCR page par page si le texte manque. */
export async function extrairePdf(
	doc: PdfDoc,
	de: number,
	a: number,
	progres: Progres = () => {},
	forcerOcr = false
): Promise<PageExtraite[]> {
	const out: PageExtraite[] = [];
	const total = a - de + 1;
	for (let n = de; n <= a; n++) {
		const fait = (n - de) / total;
		progres(`Lecture de la page ${n}…`, fait);
		const texte = forcerOcr ? '' : await textePage(doc, n);
		if (texte.replace(/\s/g, '').length >= SEUIL_TEXTE) {
			out.push({ page: n, texte: nettoyer(texte).texte, ocr: false });
			continue;
		}
		progres(`Page ${n} scannée : reconnaissance du texte…`, fait);
		const canvas = await rendrePage(doc, n);
		const r = await ocr(canvas, progres);
		canvas.width = canvas.height = 0;
		out.push({ page: n, texte: nettoyer(r.texte).texte, ocr: true, confiance: r.confiance });
	}
	progres('Terminé.', 1);
	return out;
}

/** Photo de page (JPEG, PNG…) : même chemin d'OCR. */
export async function extraireImage(fichier: File, progres: Progres = () => {}): Promise<PageExtraite[]> {
	progres('Reconnaissance du texte de la photo…', 0.1);
	const r = await ocr(fichier, progres);
	progres('Terminé.', 1);
	return [{ page: 1, texte: nettoyer(r.texte).texte, ocr: true, confiance: r.confiance }];
}

// ------------------------------------------------------------------ découpage
export const MARQUE_PAGE = /^⟦p\. (\d+)⟧$/;
export const MARQUE_PIECE = /^===\s*(.*)$/;

/** Assemble les pages en un seul texte à corriger ; chaque page commence par « ⟦p. N⟧ ». */
export function assembler(pages: PageExtraite[]): string {
	return pages.map((p) => `⟦p. ${p.page}⟧\n${p.texte}`).join('\n\n');
}

export interface PieceDecoupee {
	titre: string;
	corps: string;
	/** Pages couvertes, ex. « 12 » ou « 12-13 ». */
	pages: string;
}

/**
 * Découpe le texte corrigé en pièces. Une ligne « === Titre » commence une nouvelle pièce.
 * Les marques de page servent à remplir la source, puis disparaissent du texte.
 */
export function decouper(texte: string, titreParDefaut = ''): PieceDecoupee[] {
	const pieces: { titre: string; lignes: string[]; pages: number[] }[] = [];
	let cur: (typeof pieces)[number] | undefined;
	let page: number | undefined;
	for (const ligne of texte.replace(/\r\n?/g, '\n').split('\n')) {
		const mp = ligne.trim().match(MARQUE_PAGE);
		if (mp) {
			page = Number(mp[1]);
			if (cur) cur.lignes.push('');
			continue;
		}
		const mt = ligne.match(MARQUE_PIECE);
		if (mt) {
			cur = { titre: mt[1].trim(), lignes: [], pages: [] };
			pieces.push(cur);
			continue;
		}
		if (!cur) {
			if (!ligne.trim()) continue;
			cur = { titre: '', lignes: [], pages: [] };
			pieces.push(cur);
		}
		cur.lignes.push(ligne);
		if (ligne.trim() && page !== undefined && !cur.pages.includes(page)) cur.pages.push(page);
	}
	return pieces
		.map((p, i) => {
			let corps = p.lignes
				.join('\n')
				.replace(/\n{3,}/g, '\n\n')
				.trim();
			let titre = p.titre;
			if (!titre) {
				// sans titre donné : une première ligne courte suivie d'une ligne vide sert de titre
				const m = corps.match(/^([^\n]{1,80})\n\n/);
				if (m) {
					titre = m[1].replace(/[.:]$/, '');
					corps = corps.slice(m[0].length).trim();
				} else titre = pieces.length > 1 ? `${titreParDefaut} (${i + 1})`.trim() : titreParDefaut;
			}
			const pp = p.pages;
			const pages = pp.length ? (pp.length > 1 ? `${pp[0]}-${pp[pp.length - 1]}` : String(pp[0])) : '';
			return { titre, corps, pages };
		})
		.filter((p) => p.corps);
}
