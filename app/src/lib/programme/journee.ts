/**
 * La journée calculée à partir du programme unique (docs/conception/REFONTE_2026-11-18.md, § 2.6). Fonction pure :
 * rien n'est lu en base ni stocké ; le contexte apporte le jour liturgique, les pratiques (plan et roues) et, pour
 * couper les pages hôtes aux points d'insertion, le corps des textes.
 */
import { priereDuSaint } from '../gertrude.ts';
import { occurrenceDu } from '../pratiques.ts';
import { elementDu, pas } from '../roues-calcul.ts';
import type { Pratique } from '../types.ts';
import { vaut, type JourDuProgramme } from './quand.ts';
import { contexteDevotionnel, couvertureDe, manquesDe } from './contexte.ts';
import { couper } from './texte.ts';
import type {
	Choix,
	Cycles,
	Dimensions,
	EntreeProgramme,
	Journee,
	Lecture,
	Ligne,
	Moment,
	Programme,
	ReglageProgramme,
	Section,
	SectionResolue,
	Vocabulaire
} from './types.ts';

export interface Contexte {
	jour: JourDuProgramme;
	/** Table `pratiques` : plan de l'année, pratiques personnelles et roues. */
	pratiques?: Pratique[];
	/** Corps d'un texte (pour couper un hôte aux points d'insertion) ; sans lui, les invités vont à la fin de l'hôte. */
	corps?: (id: string) => string | undefined;
	/** Surcouche de l'utilisateur (lot 4). */
	reglages?: ReglageProgramme[];
	/** Lot « Dimensions » (descriptif seulement : rien n'y change les lignes). Cycles dévotionnels du jour. */
	cycles?: Cycles | null;
	/** Dimensions d'un texte (dimensions.ts : réglage de l'utilisateur, classement livré, motifs). */
	dimensions?: (id: string) => Dimensions | undefined;
	vocabulaire?: Vocabulaire | null;
}

type Bloc = SectionResolue | { point: string };
const estPoint = (b: Bloc): b is { point: string } => 'point' in b;
const ORDRE_MOMENTS: Record<Moment, number> = { matin: 0, journee: 1, soir: 2 };

/** Identifiant d'une pratique du plan sans l'année : « plan:2026:treize-mardis-de-s-antoine » → « treize-mardis-de-s-antoine ». */
export const cleDuPlan = (id: string) => id.replace(/^plan:(\d{4}:)?/, '');

/** Entrées livrées, modifiées par les réglages de l'utilisateur, plus ses ajouts. */
export function appliquerReglages(entrees: EntreeProgramme[], reglages: ReglageProgramme[] = []): EntreeProgramme[] {
	const parId = new Map(reglages.map((r) => [r.id, r]));
	const out: EntreeProgramme[] = [];
	for (const e of entrees) {
		const r = parId.get(e.id);
		if (r?.actif === false) continue;
		let x = r?.entree ?? e;
		if (r && x.page)
			x = { ...x, page: { ...x.page, ...(r.ordre !== undefined && { ordre: r.ordre }), ...(r.heures && { heures: r.heures }) } };
		if (r?.quand) x = { ...x, quand: r.quand };
		if (r?.duree !== undefined) x = { ...x, duree: r.duree };
		out.push(x);
	}
	const livres = new Set(entrees.map((e) => e.id));
	for (const r of reglages) if (r.entree && !livres.has(r.id) && r.actif !== false) out.push(r.entree);
	return out;
}

export function journee(programme: Programme, ctx: Contexte): Journee {
	const j = ctx.jour;
	const date = j.date;
	const pratiques = (ctx.pratiques ?? []).filter((p) => !p.supprimeLe);

	function choisir(c: Choix): { id: string; nom?: string } | null {
		if (typeof c === 'string') return { id: c };
		switch (c.selon) {
			case 'jour_semaine': {
				const v = c.valeurs[new Date(date + 'T12:00:00').getDay()];
				return v ? { id: v } : null;
			}
			case 'rotation': {
				const r = pratiques.find((p) => p.id === c.roue);
				if (r?.elements?.length) {
					const t = elementDu(r, date)?.texte;
					return t ? { id: t } : null;
				}
				return c.parmi.length ? { id: c.parmi[pas(date, c.unite) % c.parmi.length] } : null;
			}
			case 'quand': {
				const cas = c.cas.find((x) => vaut(x.quand, j));
				if (cas) return choisir(cas.texte);
				return c.sinon === undefined ? null : choisir(c.sinon);
			}
			case 'saint_du_jour': {
				const p = j.office ? priereDuSaint(j.office, !!j.est_fete_sanctorale) : null;
				return p ? { id: p.id, ...(p.nom && { nom: p.nom }) } : null;
			}
		}
	}

	function resoudre(sections: Section[], origine: string, rang = 0): Bloc[] {
		const out: Bloc[] = [];
		for (const s of sections) {
			if (!vaut(s.quand, j)) continue;
			if ('point' in s) out.push({ point: s.point });
			else if ('champ' in s) out.push({ genre: 'champ', champ: s.champ, origine });
			else if ('notice' in s) {
				const c = choisir(s.notice);
				if (c)
					out.push({ genre: 'notice', texte: c.id, origine, ...(s.extrait && { extrait: s.extrait }), ...(s.titre && { titre: s.titre }) });
			} else {
				if (s.rangs && (rang < s.rangs[0] || rang > s.rangs[1])) continue;
				const c = choisir(s.texte);
				if (!c) continue;
				const base: SectionResolue = {
					genre: 'texte',
					texte: c.id,
					origine,
					...(s.titre && { titre: s.titre }),
					...(s.depliable && { depliable: true }),
					...(c.nom && { nom: c.nom }),
					...(typeof s.texte !== 'string' && { variante: true }),
					...(s.extrait && { extrait: s.extrait }),
					...(s.extrait?.rang_du_jour && { rang })
				};
				if (!s.coupures?.length) {
					out.push(base);
					continue;
				}
				const corps = ctx.corps?.(c.id);
				const morceaux = corps ? couper(corps, s.coupures) : null;
				if (!morceaux) {
					// texte inconnu ou ancre absente : le texte entier, puis les points (le test des ancres le signale)
					out.push(base, ...s.coupures.map((x) => ({ point: x.point })));
					continue;
				}
				morceaux.forEach((m, k) => {
					if (!m.vide) out.push({ ...base, ...(m.extrait && { extrait: m.extrait }), ...(k > 0 && { titre: undefined }) });
					for (const p of m.points) out.push({ point: p });
				});
			}
		}
		return out.map((b) => (estPoint(b) ? b : (Object.fromEntries(Object.entries(b).filter(([, v]) => v !== undefined)) as SectionResolue)));
	}

	// 1. entrées du jour
	const entrees = appliquerReglages(programme.entrees, ctx.reglages);
	const parId = new Map(entrees.map((e) => [e.id, e]));
	const actives = entrees.filter((e) => vaut(e.quand, j));

	// 2. pages et lectures, avec leurs points d'insertion
	type Hote = { blocs: Bloc[]; invites: string[] };
	const lignes = new Map<string, Ligne & Hote>();
	const lectures = new Map<string, Lecture & Hote>();
	for (const e of actives) {
		if (e.page) {
			lignes.set(e.id, {
				id: e.id,
				titre: e.titre,
				moment: e.page.moment,
				ordre: e.page.ordre,
				...(e.page.heures && { heures: e.page.heures }),
				sections: [],
				blocs: resoudre(e.page.sections, e.id),
				invites: [],
				annotations: [],
				...(e.rang && { rang: e.rang }),
				...(e.duree !== undefined && { duree: e.duree })
			});
		}
		if (e.lecture) {
			lectures.set(e.id, {
				id: e.id,
				titre: e.titre,
				section: e.lecture.section,
				route: e.lecture.route,
				ordre: e.lecture.ordre,
				compte: e.lecture.compte,
				sections: [],
				blocs: resoudre(e.lecture.sections ?? [], e.id),
				invites: []
			});
		}
	}

	// 3. insertions : chaque invité va au point de son hôte ; sans hôte ce jour-là, il devient une ligne à part
	const dejaPlaces = new WeakMap<{ point: string }, number>();
	for (const e of actives) {
		for (const ins of e.insertions ?? []) {
			if (!vaut(ins.quand, j)) continue;
			const blocs = resoudre(ins.sections, e.id).filter((b): b is SectionResolue => !estPoint(b));
			if (!blocs.length) continue;
			const avecHeure = ins.heure ? blocs.map((b) => ({ ...b, heure: ins.heure })) : blocs;
			const hote = lignes.get(ins.hote) ?? lectures.get(ins.hote);
			if (hote) {
				const places: number[] = [];
				hote.blocs.forEach((b, k) => estPoint(b) && b.point === ins.point && places.push(k));
				if (!places.length) hote.blocs.push(...avecHeure);
				// à un même point, les invités se suivent dans l'ordre du programme
				for (const k of places.reverse()) {
					const marque = hote.blocs[k] as { point: string };
					const deja = dejaPlaces.get(marque) ?? 0;
					hote.blocs.splice(k + 1 + deja, 0, ...avecHeure);
					dejaPlaces.set(marque, deja + avecHeure.length);
				}
				if (!hote.invites.includes(e.id)) hote.invites.push(e.id);
				continue;
			}
			const page = parId.get(ins.hote)?.page;
			const seule = lignes.get(e.id);
			if (seule) seule.blocs.push(...avecHeure);
			else
				lignes.set(e.id, {
					id: e.id,
					titre: e.titre,
					moment: page?.moment ?? 'journee',
					ordre: (page?.ordre ?? 50) + 1,
					sections: [],
					blocs: avecHeure,
					invites: [],
					annotations: []
				});
		}
	}

	// 4. pratiques du plan : annotation de la ligne hôte, ou ligne propre avec la partie du jour
	const planLignes: (Ligne & Hote)[] = [];
	const vus = new Set<string>();
	for (const p of pratiques) {
		if (p.type === 'roue' || !p.active) continue;
		const o = occurrenceDu(p, date);
		if (!o) continue;
		const cle = cleDuPlan(p.id);
		if (vus.has(cle)) continue;
		vus.add(cle);
		const regle = programme.plan[cle];
		const compteur = o.total ? ` — ${o.rang}/${o.total}` : '';
		if (regle && 'annote' in regle) {
			const hote = lignes.get(regle.annote);
			if (hote) {
				hote.annotations.push({ source: p.id, texte: `${p.titre}${compteur}${regle.note ? ` : ${regle.note}` : ''}` });
				continue;
			}
		}
		const blocs: Bloc[] =
			regle && 'sections' in regle
				? resoudre(regle.sections, p.id, o.rang)
				: (p.textes ?? []).map((t) => ({ genre: 'texte' as const, texte: t, origine: p.id }));
		planLignes.push({
			id: p.id,
			titre: `${p.titre}${compteur}`,
			moment: regle && 'moment' in regle ? regle.moment : 'journee',
			ordre: regle && 'ordre' in regle ? regle.ordre : 75,
			sections: [],
			blocs,
			invites: [],
			annotations: []
		});
	}

	// 5. ordre d'affichage, puis garde d'unicité
	const tri = (a: Ligne, b: Ligne) => ORDRE_MOMENTS[a.moment] - ORDRE_MOMENTS[b.moment] || a.ordre - b.ordre;
	const ordonnees = [...lignes.values()].sort(tri);
	const lues = [...lectures.values()].sort((a, b) => a.ordre - b.ordre);
	const porteur = new Map<string, { origine: string; hote: Ligne | Lecture }>();
	const conflits: Journee['conflits'] = [];
	for (const h of [...ordonnees, ...lues]) {
		h.blocs = h.blocs.filter((b) => {
			if (estPoint(b) || b.genre !== 'texte' || !b.texte) return true;
			const deja = porteur.get(b.texte);
			if (!deja) {
				porteur.set(b.texte, { origine: b.origine, hote: h });
				return true;
			}
			if (deja.origine === b.origine) return true; // même pratique, dite à plusieurs heures ou à chaque dizaine
			conflits.push({ texte: b.texte, garde: deja.origine, retire: b.origine });
			return false;
		});
	}
	// une pratique du plan qui demande un texte déjà dit dans la journée annote la ligne qui le porte
	const fusions: Journee['fusions'] = [];
	for (const l of planLignes) {
		l.blocs = l.blocs.filter((b) => {
			if (estPoint(b) || b.genre !== 'texte' || !b.texte) return true;
			const deja = porteur.get(b.texte);
			if (!deja) {
				porteur.set(b.texte, { origine: b.origine, hote: l });
				return true;
			}
			if (deja.origine === b.origine) return true;
			fusions.push({ texte: b.texte, de: l.id, vers: deja.hote.id });
			if ('annotations' in deja.hote && !deja.hote.annotations.some((a) => a.source === l.id))
				deja.hote.annotations.push({ source: l.id, texte: l.titre });
			return false;
		});
		if (l.blocs.some((b) => !estPoint(b) && b.genre === 'texte')) ordonnees.push(l);
	}
	ordonnees.sort(tri);

	const textes = new Map<string, string[]>();
	const fermer = <T extends Hote & { sections: SectionResolue[] }>(h: T) => {
		h.sections = h.blocs.filter((b): b is SectionResolue => !estPoint(b));
		for (const s of h.sections) {
			if (s.genre !== 'texte' || !s.texte) continue;
			const o = textes.get(s.texte) ?? [];
			if (!o.includes(s.origine)) o.push(s.origine);
			textes.set(s.texte, o);
		}
		const { blocs: _b, ...reste } = h;
		return reste;
	};
	const lignesFinales = ordonnees.map(fermer);
	// lot « Dimensions » : décrire la journée déjà fixée (contexte, couverture, manques), sans rien y changer
	const contexte = contexteDevotionnel(j, ctx.cycles);
	const couverture = couvertureDe(lignesFinales, ctx.dimensions ?? (() => undefined));
	return {
		date,
		lignes: lignesFinales,
		lectures: lues.map(fermer),
		textes,
		fusions,
		conflits,
		a_fournir: programme.a_fournir.filter((a) => vaut(a.quand, j)),
		contexte,
		couverture,
		manques: manquesDe(couverture, contexte, ctx.vocabulaire)
	};
}
