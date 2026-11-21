/**
 * Compositeur d'ordo (LOT_DIMENSIONS.md, § 6, lot D5) : pour une période, les manques de chaque journée et, pour chacun,
 * des textes candidats déjà sourcés dans la bibliothèque. Il **propose** : il n'écrit jamais dans les données, et la
 * journée reste celle que calcule `journee()` (on compose à la conception ; la journée reste fixe à l'exécution).
 *
 * Écart avec la conception (§ 6, « engine/ordo/composer.py ») : le compositeur est écrit en TypeScript pour réutiliser
 * `journee()`, `dimensionsEffectives()` et le contrôle d'inclusion du test d'unicité, au lieu d'en refaire une copie en
 * Python (CLAUDE.md § 3 et § 17 : pas de second moteur).
 */
import { minutesDuTexte } from '../durees.ts';
import type { DimensionsEffectives } from '../dimensions.ts';
import type { Texte } from '../types.ts';
import { fragments, normaliser, partIncluse } from './texte.ts';
import type { Dimension, Journee } from './types.ts';

export interface Candidat {
	texte: string;
	titre: string;
	/** Ouvrage et page : seuls les textes sourcés sont proposés. */
	source: string;
	/** Valeurs du candidat qui répondent aussi au contexte du jour ou à ses autres manques (« dimension:valeur »). */
	communs: string[];
	minutes: number;
	/** La valeur qui comble le manque est encore devinée (classement non relu, D2). */
	devine: boolean;
}

export interface ManqueDuJour {
	dimension: Dimension;
	valeur: string;
	/** Demandée par le contexte du jour, ou fin principale de la SPEC. */
	requis: boolean;
	candidats: Candidat[];
}

export interface OrdoDuJour {
	date: string;
	office: string;
	/** Contexte lisible : « objet:passion ← vendredi ». */
	contexte: string[];
	/** Toutes les valeurs du vocabulaire qu'aucune prière du jour ne porte, requises d'abord. */
	manques: ManqueDuJour[];
}

export interface Bibliotheque {
	textes: Iterable<Texte>;
	dimensions: (t: Texte) => DimensionsEffectives;
	/** Formules communes (programme.json › formules, non normalisées), écartées du contrôle d'inclusion. */
	formules?: string[];
}

/** Seuil du test d'unicité : un texte est « inclus » dans un autre si un tiers de ses fragments s'y retrouve. */
const INCLUSION = 1 / 3;

const sourceDe = (t: Texte): string | null => {
	const s = t.source;
	if (!s?.ouvrage) return null;
	return [s.ouvrage, s.edition, s.page && `p. ${s.page}`].filter(Boolean).join(', ');
};

/**
 * Manques d'une journée (requis d'abord) et leurs candidats. Un candidat : texte sourcé, porteur de la valeur manquante, qui n'est
 * pas déjà dit ce jour-là ni contenu dans un texte du jour (ni ne le contient). Classement : nombre de valeurs communes
 * avec le contexte et les autres manques, puis durée la plus courte, puis identifiant (déterministe).
 */
export function ordoDuJour(j: Journee, office: string, biblio: Bibliotheque, parManque = 3): OrdoDuJour {
	const tous = [...j.manques].sort((a, b) => Number(b.requis) - Number(a.requis));
	const dits = new Set(j.textes.keys());
	const textes = [...biblio.textes];
	const parId = new Map(textes.map((t) => [t.id, t]));
	const formules = (biblio.formules ?? []).map(normaliser);
	const fragmentsDits = [...dits].map((id) => fragments(parId.get(id)?.corps ?? '', formules));

	const voulues = new Set([
		...j.contexte.objets.map((v) => `objet:${v}`),
		...j.contexte.fins.map((v) => `fin:${v}`),
		...tous.filter((m) => m.requis).map((m) => `${m.dimension}:${m.valeur}`)
	]);

	const admissibles = textes
		.filter((t) => !dits.has(t.id) && t.corps?.trim() && sourceDe(t))
		.map((t) => ({ t, d: biblio.dimensions(t) }))
		.filter(({ t }) => {
			const f = fragments(t.corps, formules);
			return !fragmentsDits.some((g) => partIncluse(f, g) >= INCLUSION || partIncluse(g, f) >= INCLUSION);
		});

	const manques = tous.map((m) => {
		const candidats = admissibles
			.filter(({ d }) => d.valeurs[m.dimension]?.includes(m.valeur))
			.map(({ t, d }) => {
				const communs = Object.entries(d.valeurs)
					.flatMap(([dim, vs]) => (vs ?? []).map((v) => `${dim}:${v}`))
					.filter((k) => voulues.has(k) && k !== `${m.dimension}:${m.valeur}`);
				return {
					texte: t.id,
					titre: t.titre,
					source: sourceDe(t)!,
					communs,
					minutes: Math.max(1, Math.round(minutesDuTexte(t.corps))),
					devine: d.devinees.has(m.dimension)
				};
			})
			.sort((a, b) => b.communs.length - a.communs.length || a.minutes - b.minutes || a.texte.localeCompare(b.texte))
			.slice(0, parManque);
		return { dimension: m.dimension, valeur: m.valeur, requis: m.requis, candidats };
	});

	return {
		date: j.date,
		office,
		contexte: j.contexte.sources.map((s) => `${s.dimension}:${s.valeur} ← ${s.de}`),
		manques
	};
}

/** Rapport Markdown d'une période (docs/audits/ORDO_<début>_<fin>.md). */
export function rapportOrdo(jours: OrdoDuJour[], libelle: (dimension: Dimension, valeur: string) => string): string {
	const debut = jours[0]?.date ?? '';
	const fin = jours.at(-1)?.date ?? '';
	const L: string[] = [];
	L.push(`# Ordo du ${debut} au ${fin} : manques et candidats`, '');
	L.push(
		'Rapport du compositeur d’ordo (`docs/conception/LOT_DIMENSIONS.md`, § 6 ; `app/src/lib/programme/ordo.ts`), produit par',
		`\`npm run ordo -- ${debut} ${fin}\` dans \`app/\`. Il **propose** et n’écrit rien : un candidat retenu entre dans`,
		'`data/programme/programme.json` à la main, avec `source: "ordo <date> : …"`, puis passe les tests d’unicité et de',
		'matrice.',
		'',
		'- **Manque** : valeur du vocabulaire (`dimensions.json`) qu’aucune prière du jour ne porte. Il est **requis** quand',
		'  le contexte du jour le demande (jour de la semaine, mois, temps) ou que c’est une des cinq fins principales de la',
		'  SPEC ; les autres manques sont des pistes, non des obligations.',
		'- **Candidat** : texte **déjà sourcé** de la bibliothèque, porteur de la valeur manquante, ni dit ce jour-là, ni',
		'  contenu dans un texte du jour, ni le contenant (contrôle d’inclusion du test d’unicité). Classés par valeurs',
		'  communes avec le contexte du jour, puis par durée.',
		'- « (deviné) » : la valeur vient encore des motifs de `etiquettes.ts` ; le classement n’est pas relu (D2).',
		''
	);

	const parManque = new Map<string, { requis: number; jours: number; candidats: Map<string, { c: Candidat; n: number }> }>();
	for (const j of jours)
		for (const m of j.manques) {
			const k = `${m.dimension}:${m.valeur}`;
			const e = parManque.get(k) ?? { requis: 0, jours: 0, candidats: new Map() };
			e.jours++;
			if (m.requis) e.requis++;
			for (const c of m.candidats) {
				const x = e.candidats.get(c.texte) ?? { c, n: 0 };
				x.n++;
				e.candidats.set(c.texte, x);
			}
			parManque.set(k, e);
		}

	const requis = [...parManque].filter(([, e]) => e.requis);
	L.push('## Manques requis', '');
	if (!requis.length)
		L.push(
			`Aucun sur les ${jours.length} jours : chaque jour couvre les objets de son contexte, et chaque fin principale est`,
			'dite au moins une fois (tests 3 et 4 de la matrice).',
			''
		);
	else {
		for (const j of jours) {
			const m = j.manques.filter((x) => x.requis);
			if (!m.length) continue;
			L.push(`### ${j.date} — ${j.office}`, '');
			if (j.contexte.length) L.push(`Contexte : ${j.contexte.join(' ; ')}.`, '');
			for (const x of m) {
				L.push(`- **${libelle(x.dimension, x.valeur)}** (${x.dimension})`);
				if (!x.candidats.length) L.push('  - aucun texte sourcé ne la porte : à chercher (A_FOURNIR.md)');
				for (const c of x.candidats)
					L.push(
						`  - ${c.titre} — \`${c.texte}\` — ${c.source} — ${c.minutes} min` +
							(c.communs.length ? ` — rejoint aussi : ${c.communs.join(', ')}` : '') +
							(c.devine ? ' (deviné)' : '')
					);
			}
			L.push('');
		}
	}

	L.push('## Autres manques de la période', '');
	L.push('Valeurs jamais ou rarement portées par la journée. Colonne « Jours » : jours de la période où la valeur manque.', '');
	L.push('| Dimension | Valeur | Jours | Candidats les plus fréquents |', '|---|---|---|---|');
	for (const [k, e] of [...parManque]
		.filter(([, e]) => !e.requis)
		.sort((a, b) => a[0].split(':')[0].localeCompare(b[0].split(':')[0]) || b[1].jours - a[1].jours || a[0].localeCompare(b[0]))) {
		const [dim, val] = k.split(':') as [Dimension, string];
		const meilleurs = [...e.candidats.values()]
			.sort((a, b) => b.n - a.n || a.c.minutes - b.c.minutes || a.c.texte.localeCompare(b.c.texte))
			.slice(0, 3)
			.map(({ c }) => `${c.titre} (\`${c.texte}\`, ${c.minutes} min${c.devine ? ', deviné' : ''})`)
			.join(' ; ');
		L.push(`| ${dim} | ${libelle(dim, val)} | ${e.jours} / ${jours.length} | ${meilleurs || '*aucun texte sourcé*'} |`);
	}
	L.push('');
	return L.join('\n') + '\n';
}
