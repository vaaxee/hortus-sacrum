/**
 * Roues symboliques : plusieurs cycles tournent ensemble sur les nombres de la tradition (1, 3, 4, 7, 12…).
 * Toutes partent alignées le premier dimanche de l'Avent ; chaque jour (ou semaine, ou mois), chaque roue avance d'un cran.
 * Les roues de départ viennent de data/roues.json ; ce sont des pratiques de type « roue », donc modifiables et synchronisées.
 */
import { contenu, db } from './db.ts';
import type { ElementRoue, Pratique, UniteRoue } from './types.ts';
import { SOURCE_VIDE } from './types.ts';

export * from './roues-calcul.ts';
import { elementDu } from './roues-calcul.ts';

interface RoueSource {
	id: string;
	nombre: number;
	titre: string;
	elements: ElementRoue[];
	source: Pratique['source'];
	verset?: { ref: string; la: string };
	actif: boolean;
	unite: UniteRoue;
	anneau?: number;
	liste?: boolean;
}

const DEPART = '2000-01-01T00:00:00.000Z';

/** Livre les roues de data/roues.json, chacune une seule fois (meta « roues ») ; ne touche jamais une roue existante. */
export async function amorcerRoues(fetchFn: typeof fetch = fetch): Promise<void> {
	const rep = await fetchFn('/data/roues.json');
	if (!rep.ok) return;
	const doc = (await rep.json()) as { roues: RoueSource[] };
	const livrees = new Set(((await db.meta.get('roues'))?.valeur as string[] | undefined) ?? []);
	const nouvelles = doc.roues.filter((r) => !livrees.has(r.id));
	for (const r of nouvelles) {
		livrees.add(r.id);
		const id = `roue:${r.id}`;
		if (await db.pratiques.get(id)) continue;
		const p = {
			id, origine: 'officielle', titre: r.titre, type: 'roue', regle: { genre: 'roue', unite: r.unite },
			textes: [...new Set(r.elements.map((e) => e.texte).filter(Boolean))] as string[],
			promesses: '', indulgence: '', source: { ...SOURCE_VIDE, ...r.source }, notes: '', active: r.actif,
			elements: r.elements, ...(r.verset ? { verset: r.verset } : {}), ...(r.anneau ? { anneau: r.anneau } : {}), ...(r.liste ? { liste: true } : {}),
			creeLe: DEPART, modifieLe: DEPART
		} as Pratique;
		p.original = contenu(p);
		await db.pratiques.put(p);
	}
	if (nouvelles.length) await db.meta.put({ cle: 'roues', valeur: [...livrees] });
	await completerElements(doc.roues);
}

const CHAMPS = ['lecture', 'texte'] as const;

/**
 * Champs ajoutés aux éléments après la livraison d'une roue (passage à lire, prière liée) : chacun n'est livré qu'une
 * fois (meta « roues-champs »), et seulement à un élément qui porte toujours le même nom et n'a rien à cette place.
 * Au premier passage, les prières déjà livrées avec les roues sont seulement notées (un lien retiré ne revient pas).
 */
async function completerElements(roues: RoueSource[]): Promise<void> {
	const meta = await db.meta.get('roues-champs');
	const livres = new Set((meta?.valeur as string[] | undefined) ?? []);
	const avant = livres.size;
	for (const r of roues) {
		const p = await db.pratiques.get(`roue:${r.id}`);
		let change = false;
		const elements = p?.elements?.map((e, k) => {
			const s = r.elements[k];
			if (!s) return e;
			let x = e;
			for (const c of CHAMPS) {
				const v = s[c];
				if (!v) continue;
				const cle = `${r.id}:${k}:${c}:${v}`;
				if (livres.has(cle)) continue;
				livres.add(cle);
				if (!meta && c === 'texte') continue;
				if (x.fr === s.fr && !x[c]) { x = { ...x, [c]: v }; change = true; }
			}
			return x;
		});
		if (p && elements && change) {
			const q = { ...p, elements, textes: [...new Set(elements.map((e) => e.texte).filter(Boolean))] as string[] };
			// une roue jamais modifiée le reste : son original suit
			if (p.modifieLe === DEPART || p.original === contenu(p)) q.original = contenu(q);
			await db.pratiques.put(q);
		}
	}
	if (livres.size !== avant || !meta) await db.meta.put({ cle: 'roues-champs', valeur: [...livres] });
}
