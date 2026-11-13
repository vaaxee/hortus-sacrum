/** Lecture du calendrier généré par le moteur (static/data/calendar/AAAA-AAAA.json). */

export interface Jour {
	date: string;
	jour: string;
	temps: string;
	/** Clé du temporal (Adv1-0, Epi3-2, Quad5-0, Pasc7-6, Pent05-3…), null pendant le temps de Noël. */
	tempora?: string | null;
	office: string;
	rang: string;
	couleur: string;
	commemoraisons: string[];
	est_fete_sanctorale: boolean;
	introit_incipit: string | null;
	introit: { la: string[]; fr: string[] | null } | null;
	station: string | null;
	notice_martyrologe: string | null;
	jeune_abstinence: { code: string; libelle: string } | null;
	devotions: { type: string; cle?: string; libelle: string; page_jardin: number | null }[];
	martyrologe: { cle: string; texte: string; texte_la?: string | null }[];
}

const cache = new Map<number, Promise<Jour[] | null>>();

function annee(a: number, fetchFn: typeof fetch): Promise<Jour[] | null> {
	if (!cache.has(a)) {
		cache.set(
			a,
			fetchFn(`/data/calendar/${a}-${a + 1}.json`)
				.then((r) => (r.ok ? (r.json() as Promise<Jour[]>) : null))
				.catch(() => null)
		);
	}
	return cache.get(a)!;
}

/** Tous les jours de l'année liturgique qui commence à l'Avent de l'année a (ou null si elle n'est pas générée). */
export function anneeLiturgique(a: number, fetchFn: typeof fetch = fetch): Promise<Jour[] | null> {
	return annee(a, fetchFn);
}

export function iso(d: Date): string {
	return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

/** Le jour liturgique d'une date (AAAA-MM-JJ), ou undefined si l'année n'est pas générée. */
export async function jourDu(date: string, fetchFn: typeof fetch = fetch): Promise<Jour | undefined> {
	const y = Number(date.slice(0, 4));
	for (const a of [y - 1, y]) {
		const trouve = (await annee(a, fetchFn))?.find((j) => j.date === date);
		if (trouve) return trouve;
	}
}

/** Tous les jours d'un mois civil. */
export async function moisDu(an: number, mois: number, fetchFn: typeof fetch = fetch): Promise<Jour[]> {
	const prefixe = `${an}-${String(mois).padStart(2, '0')}-`;
	const out: Jour[] = [];
	for (const a of [an - 1, an]) {
		for (const j of (await annee(a, fetchFn)) ?? []) if (j.date.startsWith(prefixe)) out.push(j);
	}
	return out;
}

/** Couleur liturgique → variable CSS de la pastille et du bandeau. Or pour les fêtes de 1re classe en blanc. */
export function teinte(j: Pick<Jour, 'couleur' | 'rang'>): string {
	if (j.couleur === 'blanc' && j.rang === '1re cl.') return 'var(--hs-lit-or)';
	return `var(--hs-lit-${j.couleur})`;
}

/** Rang abrégé du calendrier → libellé en clair. */
export const RANG: Record<string, string> = {
	'1re cl.': 'double de 1re classe',
	'2e cl.': 'double de 2e classe',
	'dbl maj.': 'double majeur',
	dbl: 'double',
	'semi-dbl': 'semi-double',
	simple: 'simple',
	vigile: 'vigile',
	'vigile 1re cl.': 'vigile de 1re classe',
	'vigile 2e cl.': 'vigile de 2e classe',
	'fér. maj.': 'férie majeure',
	'fér. priv.': 'férie privilégiée',
	férie: 'férie',
	'dim.': 'dimanche',
	'dim. 1re cl.': 'dimanche de 1re classe',
	'dim. 2e cl.': 'dimanche de 2e classe'
};

/**
 * Dévotion de chaque mois (SPEC §3 et décisions du 12 novembre 2026) :
 * pieux exercices indulgenciés de l'Enchiridion de 1952, sauf février (coutume).
 */
export const MOIS_DEVOTION: Record<number, { nom: string; reference: string }> = {
	1: { nom: 'Mois du saint Nom de Jésus', reference: 'Ench. 1952, n° 118' },
	2: { nom: 'Mois de la Sainte Famille', reference: 'coutume ; aucune indulgence propre au mois dans l’Enchiridion de 1952' },
	3: { nom: 'Mois de saint Joseph', reference: 'Ench. 1952, n° 466' },
	4: { nom: 'Mois eucharistique', reference: 'Ench. 1952, n° 175' },
	5: { nom: 'Mois de Marie', reference: 'Ench. 1952, n° 325' },
	6: { nom: 'Mois du Sacré-Cœur', reference: 'Ench. 1952, n° 253' },
	7: { nom: 'Mois du Précieux Sang', reference: 'Ench. 1952, n° 217' },
	8: { nom: 'Mois du Cœur Immaculé de Marie', reference: 'Ench. 1952, n° 389' },
	9: { nom: 'Mois de Notre-Dame des Sept Douleurs', reference: 'Ench. 1952, n° 381' },
	10: { nom: 'Mois du Rosaire', reference: 'Ench. 1952, n° 398' },
	11: { nom: 'Mois des fidèles trépassés', reference: 'Ench. 1952, n° 589' },
	12: { nom: 'Mois de l’Immaculée Conception', reference: 'Ench. 1952, n° 364' }
};

export const NOMS_MOIS = ['', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];

/** Lignes d'Introït de DO → balisage de l'app (« !Ps 24:1 » = référence, « v. » = antienne, « &Gloria »). */
export function introitVersCorps(lignes: string[]): string {
	return lignes
		.map((l) => {
			if (l.startsWith('!')) return `[r]${l.slice(1).replace(/\.$/, '')}[/r]`;
			if (l.startsWith('&Gloria')) return '[r]℣. Gloria Patri.[/r]';
			return l.replace(/^v\.\s*/, '');
		})
		.join('\n\n');
}
