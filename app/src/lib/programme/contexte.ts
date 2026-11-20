/**
 * Contexte dévotionnel du jour et couverture des dimensions (LOT_DIMENSIONS.md, § 4-5). Fonctions pures.
 * Principe : on compose à la conception ; la journée reste fixe à l'exécution. Rien ici n'ajoute ni ne retire une ligne :
 * le contexte et la couverture décrivent la journée, pour l'afficher et pour les tests.
 */
import type { JourDuProgramme } from './quand.ts';
import {
	DIMENSIONS,
	type ContexteDevotionnel,
	type Couverture,
	type Cycles,
	type Dimension,
	type Dimensions,
	type Ligne,
	type Qualification,
	type Vocabulaire
} from './types.ts';

const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
const MOIS = ['', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];

export function contexteDevotionnel(j: JourDuProgramme, cycles?: Cycles | null): ContexteDevotionnel {
	const d = new Date(j.date + 'T12:00:00');
	const objets: string[] = [];
	const fins: string[] = [];
	const sources: ContexteDevotionnel['sources'] = [];
	const ajouter = (q: Qualification | undefined, de: string) => {
		for (const v of q?.objets ?? []) {
			if (!objets.includes(v)) objets.push(v);
			sources.push({ dimension: 'objet', valeur: v, de });
		}
		for (const v of q?.fins ?? []) {
			if (!fins.includes(v)) fins.push(v);
			sources.push({ dimension: 'fin', valeur: v, de });
		}
	};
	if (cycles) {
		ajouter(cycles.jour_semaine[String(d.getDay())], JOURS[d.getDay()]);
		ajouter(cycles.mois[String(d.getMonth() + 1)], `mois de ${MOIS[d.getMonth() + 1]}`);
		const semaine = Math.ceil(d.getDate() / 7);
		ajouter(cycles.semaine_du_mois[String(semaine)], `${semaine}e semaine du mois`);
		if (j.temps) ajouter(cycles.temps[j.temps], j.temps);
		if (j.office) for (const f of cycles.fetes) if (new RegExp(f.office, 'u').test(j.office)) ajouter(f, j.office);
	}
	return {
		temps: j.temps ?? '',
		...(j.est_fete_sanctorale && j.office && { sanctoral: j.office }),
		objets,
		fins,
		sources
	};
}

/** Valeurs couvertes par les prières dites dans les lignes du jour (notices et champs exclus). */
export function couvertureDe(lignes: Ligne[], dimensions: (id: string) => Dimensions | undefined): Record<Dimension, Couverture[]> {
	const par = Object.fromEntries(DIMENSIONS.map((d) => [d, new Map<string, string[]>()])) as Record<Dimension, Map<string, string[]>>;
	for (const l of lignes) {
		for (const s of l.sections) {
			if (s.genre !== 'texte' || !s.texte) continue;
			const dims = dimensions(s.texte);
			if (!dims) continue;
			for (const d of DIMENSIONS)
				for (const v of dims[d] ?? []) {
					const ids = par[d].get(v) ?? [];
					if (!ids.includes(l.id)) ids.push(l.id);
					par[d].set(v, ids);
				}
		}
	}
	return Object.fromEntries(DIMENSIONS.map((d) => [d, [...par[d]].map(([valeur, ids]) => ({ valeur, par: ids }))])) as Record<
		Dimension,
		Couverture[]
	>;
}

/**
 * Ce qui manque : les valeurs du vocabulaire qu'aucune prière du jour ne porte (toutes, si le vocabulaire est connu ;
 * sinon seulement celles que le contexte demande). `requis` : demandée par le contexte, ou fin principale de la SPEC.
 */
export function manquesDe(
	couverture: Record<Dimension, Couverture[]>,
	contexte: ContexteDevotionnel,
	vocabulaire?: Vocabulaire | null
): { dimension: Dimension; valeur: string; requis: boolean }[] {
	const requis = new Set([
		...contexte.objets.map((v) => `objet:${v}`),
		...contexte.fins.map((v) => `fin:${v}`),
		...(vocabulaire?.fins_principales ?? []).map((v) => `fin:${v}`)
	]);
	const out: { dimension: Dimension; valeur: string; requis: boolean }[] = [];
	for (const d of DIMENSIONS) {
		const couvertes = new Set(couverture[d].map((c) => c.valeur));
		const candidates = vocabulaire
			? Object.keys(vocabulaire.dimensions[d].valeurs)
			: [...requis].filter((r) => r.startsWith(`${d}:`)).map((r) => r.slice(d.length + 1));
		for (const v of candidates) if (!couvertes.has(v)) out.push({ dimension: d, valeur: v, requis: requis.has(`${d}:${v}`) });
	}
	return out;
}
