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

export const estRoue = (p: Pratique) => p.type === 'roue';

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
	if (!nouvelles.length) return;
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
	await db.meta.put({ cle: 'roues', valeur: [...livrees] });
}
