/**
 * Garantie d'unicité (SPEC § 11, principe 1) : sur toute l'année liturgique 2026-2027, aucun texte ne paraît deux fois
 * dans une journée, ni en entier ni contenu dans un autre ; chaque identifiant existe ; chaque ancre se trouve dans
 * son texte.
 */
import { describe, expect, it } from 'vitest';
import { journee } from './journee.ts';
import { couper, extraire, fragments, normaliser, partIncluse } from './texte.ts';
import { candidats, sectionsDuProgramme } from './inventaire.ts';
import type { Section } from './types.ts';
import { CALENDRIER, corps, PLAN, PROGRAMME, TEXTES } from './donnees-de-test.ts';

const toutesLesSections = sectionsDuProgramme(PROGRAMME);

const FORMULES = PROGRAMME.formules.map(normaliser);

describe('données du programme', () => {
	it('chaque identifiant de texte existe', () => {
		const manquants: string[] = [];
		for (const { ou, s } of toutesLesSections) {
			const c = 'texte' in s ? s.texte : 'notice' in s ? s.notice : null;
			if (c) for (const id of candidats(c)) if (!TEXTES.has(id)) manquants.push(`${ou} → ${id}`);
		}
		for (const e of PROGRAMME.entrees) for (const id of e.explication ?? []) if (!TEXTES.has(id)) manquants.push(`${e.id} → ${id}`);
		expect(manquants).toEqual([]);
	});

	it('chaque ancre se trouve dans son texte, et une page coupée se recompose à l’identique', () => {
		const fautes: string[] = [];
		for (const { ou, s } of toutesLesSections) {
			if (!('texte' in s) && !('notice' in s)) continue;
			const c = 'texte' in s ? s.texte : s.notice;
			for (const id of candidats(c)) {
				const t = corps(id);
				if (!t) continue;
				if (s.extrait && !s.extrait.rang_du_jour && extraire(t, s.extrait) === null) fautes.push(`${ou} : extrait absent de ${id}`);
				if (s.extrait?.rang_du_jour && extraire(t, s.extrait, 1) === null) fautes.push(`${ou} : pas de 1er jour dans ${id}`);
				if ('coupures' in s && s.coupures) {
					const m = couper(t, s.coupures);
					if (!m) {
						fautes.push(`${ou} : coupure impossible dans ${id}`);
						continue;
					}
					const recompose = m
						.filter((x) => !x.vide)
						.map((x) => extraire(t, x.extrait))
						.join('\n\n');
					if (normaliser(recompose) !== normaliser(t)) fautes.push(`${ou} : ${id} ne se recompose pas`);
				}
			}
		}
		expect(fautes).toEqual([]);
	});

	it('chaque invité a un hôte déclaré qui porte le point demandé', () => {
		const fautes: string[] = [];
		const points = (sections: Section[]) =>
			sections.flatMap((s) => ('point' in s ? [s.point] : 'coupures' in s && s.coupures ? s.coupures.map((c) => c.point) : []));
		for (const e of PROGRAMME.entrees)
			for (const i of e.insertions ?? []) {
				const h = PROGRAMME.entrees.find((x) => x.id === i.hote);
				const p = points([...(h?.page?.sections ?? []), ...(h?.lecture?.sections ?? [])]);
				if (!p.includes(i.point)) fautes.push(`${e.id} → ${i.hote}:${i.point}`);
			}
		for (const [cle, r] of Object.entries(PROGRAMME.plan))
			if ('annote' in r && !PROGRAMME.entrees.some((e) => e.id === r.annote)) fautes.push(`plan:${cle} → ${r.annote}`);
		expect(fautes).toEqual([]);
	});

	it('chaque pratique du plan importé a sa règle dans le programme', () => {
		const sans = PLAN.map((p) => p.id.replace(/^plan:(\d{4}:)?/, '')).filter((c) => !(c in PROGRAMME.plan));
		expect(sans).toEqual([]);
	});
});

// ------------------------------------------------------------------ l'année entière

/** Contenu réel de chaque section du jour, pour chercher un texte contenu dans un autre. */
const cache = new Map<string, Set<string>>();
function fragmentsDe(id: string, extrait: Parameters<typeof extraire>[1], rang = 0): Set<string> {
	const cle = `${id}|${JSON.stringify(extrait ?? null)}|${rang}`;
	let f = cache.get(cle);
	if (!f) {
		const t = corps(id);
		f = fragments(t ? (extraire(t, extrait, rang) ?? '') : '', FORMULES);
		cache.set(cle, f);
	}
	return f;
}

const JOURS = CALENDRIER.map((j) => journee(PROGRAMME, { jour: j, pratiques: PLAN, corps }));

describe(`unicité sur ${CALENDRIER.length} jours (${CALENDRIER[0].date} → ${CALENDRIER.at(-1)!.date})`, () => {
	it('aucun texte apporté par deux entrées le même jour (garde jamais déclenchée)', () => {
		const conflits = JOURS.flatMap((j) => j.conflits.map((c) => `${j.date} ${c.texte} : ${c.garde} et ${c.retire}`));
		expect(conflits).toEqual([]);
		const doubles = JOURS.flatMap((j) => [...j.textes].filter(([, o]) => o.length > 1).map(([t, o]) => `${j.date} ${t} : ${o.join(', ')}`));
		expect(doubles).toEqual([]);
	});

	it('aucun texte du jour n’est contenu dans un autre texte du même jour', () => {
		const inclus = new Set<string>();
		// Fragments mis en cache : le calcul est quadratique et passait la limite de 5 s quand la suite tourne en parallèle.
		const cache = new Map<string, ReturnType<typeof fragmentsDe>>();
		const frag = (s: (typeof JOURS)[number]['lignes'][number]['sections'][number]) => {
			const cle = `${s.texte}|${JSON.stringify(s.extrait ?? null)}|${s.rang ?? ''}`;
			let f = cache.get(cle);
			if (!f) cache.set(cle, (f = fragmentsDe(s.texte!, s.extrait, s.rang)));
			return f;
		};
		for (const j of JOURS) {
			const sections = [...j.lignes, ...j.lectures].flatMap((l) => l.sections.filter((s) => s.texte && s.genre === 'texte'));
			for (const a of sections)
				for (const b of sections) {
					if (a === b || a.origine === b.origine) continue;
					const fa = frag(a);
					if (fa.size < 2) continue;
					const part = partIncluse(fa, frag(b));
					if (part >= 1 / 3) inclus.add(`${a.texte} (${a.origine}) ⊂ ${b.texte} (${b.origine}) : ${Math.round(part * 100)} %`);
				}
		}
		expect([...inclus]).toEqual([]);
	}, 30_000);

	it('chaque jour a sa prière du matin, son chapelet, sa prière du soir et une seule litanie', () => {
		const LITANIES = /litanies/;
		for (const j of JOURS) {
			const ids = j.lignes.map((l) => l.id);
			expect(ids, j.date).toEqual(expect.arrayContaining(['prog:priere-du-matin', 'prog:chapelet', 'prog:priere-du-soir', 'prog:angelus']));
			// les litanies d'une neuvaine du plan s'ajoutent à celle du jour : on ne compte que le programme
			const litanies = [...j.textes].filter(([t, o]) => LITANIES.test(t) && o.some((x) => x.startsWith('prog:'))).map(([t]) => t);
			expect(litanies.length, `${j.date} : ${litanies.join(', ')}`).toBeLessThanOrEqual(1);
		}
	});
});
