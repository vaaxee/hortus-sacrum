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
