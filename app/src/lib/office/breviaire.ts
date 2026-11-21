/**
 * Bréviaire romain, heures complètes, rubriques d'avant 1955 (REFONTE § 5, lot 9), latin seul.
 * Données produites par engine/office/breviaire.py, qui exécute hors ligne le moteur de Divinum Officium :
 * data/office/breviaire/<AAAA-AAAA>/communs.json (paragraphes communs à plusieurs jours) et MM-JJ.json (plan du jour et
 * paragraphes propres). Les jours sont chargés à la demande (puis gardés par le service worker) ; ce module recompose
 * le texte d'un jour avec un titre de niveau 2 par heure, pour le composant Office (une heure à la fois).
 */

export interface CommunsBreviaire {
	titre: string;
	source: { depot: string; commit: string; version: string; langue: string; note: string };
	heures: { cle: string; nom: string; latin: string }[];
	jours: { debut: string; fin: string };
	paragraphes: string[];
}

export interface FichierJour {
	date: string;
	office: string;
	/** Huit heures ; réf. >= 0 : paragraphe commun ; réf. < 0 : propres[-réf - 1]. */
	heures: number[][];
	propres: string[];
}

export interface JourBreviaire {
	date: string;
	/** L'office du jour selon Divinum Officium (« Dominica I Adventus »). */
	office: string;
	/** « ## Matines · Ad Matutinum », puis chaque heure. */
	corps: string;
}

/** Années liturgiques calculées (année du premier dimanche de l'Avent). */
export const ANNEES_CALCULEES = [2026];

export function paragraphe(c: CommunsBreviaire, j: FichierJour, ref: number): string {
	const p = ref >= 0 ? c.paragraphes[ref] : j.propres[-ref - 1];
	if (p === undefined) throw new Error(`Bréviaire ${j.date} : paragraphe ${ref} introuvable`);
	return p;
}

export function jourDuBreviaire(c: CommunsBreviaire, j: FichierJour): JourBreviaire {
	const corps = c.heures
		.map((h, i) => `## ${h.nom} · ${h.latin}\n\n${(j.heures[i] ?? []).map((r) => paragraphe(c, j, r)).join('\n\n')}`)
		.join('\n\n');
	return { date: j.date, office: j.office, corps };
}

const dossier = (annee: number) => `/data/office/breviaire/${annee}-${annee + 1}`;
const communs = new Map<number, Promise<CommunsBreviaire | null>>();
const lire = <T>(url: string, fetchFn: typeof fetch) =>
	fetchFn(url)
		.then((r) => (r.ok ? (r.json() as Promise<T>) : null))
		.catch(() => null);

export function chargerCommuns(annee: number, fetchFn: typeof fetch = fetch): Promise<CommunsBreviaire | null> {
	if (!communs.has(annee)) {
		const p = lire<CommunsBreviaire>(`${dossier(annee)}/communs.json`, fetchFn);
		communs.set(annee, p);
		// un échec passager (hors ligne) n'est pas gardé : la prochaine demande réessaie
		void p.then((c) => {
			if (!c) communs.delete(annee);
		});
	}
	return communs.get(annee)!;
}

/** L'office d'un jour (AAAA-MM-JJ), ou null hors des années calculées. */
export async function breviaireDuJour(date: string, fetchFn: typeof fetch = fetch): Promise<JourBreviaire | null> {
	if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return null;
	for (const annee of ANNEES_CALCULEES) {
		const c = await chargerCommuns(annee, fetchFn);
		if (!c || date < c.jours.debut || date > c.jours.fin) continue;
		const j = await lire<FichierJour>(`${dossier(annee)}/${date.slice(5)}.json`, fetchFn);
		return j ? jourDuBreviaire(c, j) : null;
	}
	return null;
}

/** Précharge les jours qui suivent (le service worker les garde pour la lecture hors ligne). */
export function prechargerSemaine(date: string, jours = 7, fetchFn: typeof fetch = fetch): void {
	const d = new Date(date + 'T12:00:00');
	for (let i = 1; i <= jours; i++) {
		const x = new Date(d.getTime() + i * 864e5).toISOString().slice(0, 10);
		void breviaireDuJour(x, fetchFn);
	}
}
