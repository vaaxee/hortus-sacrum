/**
 * Indulgences partielles : valeur de chaque prière à une date donnée (selon le mois, le jour de la semaine, une fête,
 * un jour du temporal) et total des prières cochées. Données : data/prieres/indulgences.json.
 * Les indulgences plénières et celles réservées aux confréries ne sont pas comptées.
 */
export interface Valeur {
	ans: number;
	jours: number;
}
export interface Partielle extends Partial<Valeur> {
	texte: string;
	quand?: { mois?: number[]; jours_semaine?: number[]; dates?: string[]; tempora?: string[] };
	/** Indice de la valeur ordinaire que celle-ci remplace aux jours indiqués. */
	remplace?: number;
	/** Nombre de fois que l'invocation indulgenciée est dite dans la prière (5 mystères → 5) ; 1 par défaut. */
	repetitions?: number;
}
export interface Fiche {
	ref: string;
	frequence: 'chaque fois' | 'une fois le jour';
	partielles: Partielle[];
	intention?: string;
	note?: string;
	/** Langue de la concession (Ench. 1952, Praenotanda 3). */
	langue?: 'latin' | 'italien' | 'français';
	/** Traduction française approuvée selon le can. 934 § 2, quand la concession n'est pas en français. */
	traduction?: string;
}

/**
 * Seules comptent les œuvres de l'Enchiridion indulgentiarum de 1952 (décret du 3 mars 1952) : la mention d'indulgence
 * d'un texte (souvent recopiée d'un manuel antérieur, Beringer, Raccolta…) n'est montrée que si elle cite l'Enchiridion,
 * ou si l'utilisateur l'a écrite lui-même. La fiche d'indulgence, elle, fait foi.
 */
export function mentionEnMarge(indulgence: string | undefined, modifieParUtilisateur: boolean): string | null {
	if (!indulgence?.trim()) return null;
	return modifieParUtilisateur || /Ench/.test(indulgence) ? indulgence : null;
}

/** Mention d'indulgence à montrer pour un texte (null si elle vient d'un manuel antérieur abrogé). */
export function mentionDuTexte(t: { indulgence?: string; original?: string }): string | null {
	let deLUtilisateur = !t.original;
	if (t.original) {
		try {
			deLUtilisateur = (JSON.parse(t.original) as { indulgence?: string }).indulgence !== t.indulgence;
		} catch {
			deLUtilisateur = false;
		}
	}
	return mentionEnMarge(t.indulgence, deLUtilisateur);
}

/** Note sur la langue (can. 934 § 2) : l'indulgence d'une prière concédée en latin ou en italien suit sa traduction approuvée. */
export function noteDeTraduction(f: Fiche): string | null {
	if (f.langue === 'français') return null;
	if (f.traduction) return `Traduction approuvée : ${f.traduction}.`;
	return "En français, l'indulgence n'est gagnée qu'avec une traduction approuvée (can. 934 § 2) ; sinon, dire la formule de la concession.";
}
export interface Indulgences {
	fiches: Record<string, Fiche>;
	sans_compte: Record<string, string>;
}

let cache: Promise<Indulgences | null> | null = null;
export function chargerIndulgences(fetchFn: typeof fetch = fetch): Promise<Indulgences | null> {
	cache ??= fetchFn('/data/prieres/indulgences.json')
		.then((r) => (r.ok ? (r.json() as Promise<Indulgences>) : null))
		.catch(() => null);
	return cache;
}

/** La condition de calendrier d'une valeur est-elle remplie à cette date ? */
export function sApplique(p: Partielle, date: string, tempora?: string | null): boolean {
	const q = p.quand;
	if (!q) return true;
	const d = new Date(date + 'T12:00:00');
	return (
		!!q.mois?.includes(d.getMonth() + 1) ||
		!!q.jours_semaine?.includes(d.getDay()) ||
		!!q.dates?.includes(date.slice(5)) ||
		(!!tempora && !!q.tempora?.includes(tempora))
	);
}

/** Valeurs retenues à cette date : les valeurs saisonnières remplacent la valeur ordinaire qu'elles désignent. */
export function valeursDuJour(f: Fiche, date: string, tempora?: string | null): Partielle[] {
	const actives = f.partielles.filter((p) => p.quand && sApplique(p, date, tempora));
	const remplacees = new Set(actives.map((p) => p.remplace).filter((x): x is number => x !== undefined));
	return f.partielles.filter((p, i) => (p.quand ? actives.includes(p) : !remplacees.has(i)));
}

export function valeurDuJour(f: Fiche, date: string, tempora?: string | null): Valeur {
	return somme(valeursDuJour(f, date, tempora).map((p) => fois({ ans: p.ans ?? 0, jours: p.jours ?? 0 }, p.repetitions ?? 1)));
}

export function somme(vs: Valeur[]): Valeur {
	return vs.reduce((a, v) => ({ ans: a.ans + v.ans, jours: a.jours + v.jours }), { ans: 0, jours: 0 });
}

export function fois(v: Valeur, n: number): Valeur {
	return { ans: v.ans * n, jours: v.jours * n };
}

/** « 12 ans et 300 jours » ; les jours ne sont pas convertis en années (l'usage des recueils). */
export function enClair(v: Valeur): string {
	const a = v.ans ? `${v.ans} an${v.ans > 1 ? 's' : ''}` : '';
	const j = v.jours ? `${v.jours} jour${v.jours > 1 ? 's' : ''}` : '';
	return [a, j].filter(Boolean).join(' et ') || '—';
}

/** Valeur ramenée en jours, seulement pour comparer et dessiner la barre (1 an = 365 jours). */
export const enJours = (v: Valeur) => v.ans * 365 + v.jours;
