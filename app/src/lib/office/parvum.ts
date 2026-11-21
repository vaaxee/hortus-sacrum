/**
 * Officium parvum Beatæ Mariæ Virginis (data/office/parvum.json, composé par engine/office/parvum.py depuis Divinum
 * Officium). Le fichier donne, pour chaque jour du calendrier, les huit heures du Petit Office ; ce module recompose
 * le texte d'un jour avec un titre de niveau 2 par heure, pour le composant Office (une heure à la fois).
 */

export interface DonneesParvum {
	titre: string;
	source: { depot: string; commit: string; version: string; fichiers: string[] };
	heures: { cle: string; nom: string; latin: string }[];
	/** Les temps du Petit Office (« adventus » → « Temps de l’Avent (Commune/C12A) »). */
	temps: Record<string, string>;
	jours: {
		debut: string;
		fin: string;
		chiffres: string;
		combinaisons: { temps: string; heures: string[] }[];
		/** Un caractère par jour depuis « debut » : le rang de la combinaison du jour dans l'alphabet « chiffres ». */
		suite: string;
	};
	textes: Record<string, { temps: string[]; paragraphes: number[] }>;
	paragraphes: string[];
}

export interface JourParvum {
	/** Le texte du jour : « ## Matines · Ad Matutinum », puis chaque heure. */
	corps: string;
	/** Le temps du jour (clé de « temps »). */
	temps: string;
	/** Son libellé. */
	nomDuTemps: string;
}

const JOUR = 86_400_000;
const utc = (iso: string) => Date.UTC(Number(iso.slice(0, 4)), Number(iso.slice(5, 7)) - 1, Number(iso.slice(8, 10)));

/** Le texte d'une heure, par son identifiant (« laudes.adventus »). */
export function texteDeLHeure(d: DonneesParvum, id: string): string {
	const t = d.textes[id];
	if (!t) throw new Error(`Officium parvum : texte inconnu « ${id} »`);
	return t.paragraphes.map((i) => d.paragraphes[i]).join('\n\n');
}

/** La combinaison du jour (AAAA-MM-JJ) : son temps et les huit heures ; undefined hors des années calculées. */
export function combinaisonDuJour(d: DonneesParvum, date: string): { temps: string; heures: string[] } | undefined {
	if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return undefined;
	const n = Math.round((utc(date) - utc(d.jours.debut)) / JOUR);
	if (n < 0 || n >= d.jours.suite.length) return undefined;
	return d.jours.combinaisons[d.jours.chiffres.indexOf(d.jours.suite[n])];
}

/** Le Petit Office d'un jour, prêt pour le composant Office ; undefined hors des années calculées. */
export function parvumDuJour(d: DonneesParvum, date: string): JourParvum | undefined {
	const c = combinaisonDuJour(d, date);
	if (!c) return undefined;
	const corps = d.heures.map((h, i) => `## ${h.nom} · ${h.latin}\n\n${texteDeLHeure(d, c.heures[i])}`).join('\n\n');
	return { corps, temps: c.temps, nomDuTemps: d.temps[c.temps] ?? c.temps };
}

let chargement: Promise<DonneesParvum | null> | undefined;

/** Les données de l'office (static/data/office/parvum.json), chargées une fois. */
export function chargerParvum(fetchFn: typeof fetch = fetch): Promise<DonneesParvum | null> {
	chargement ??= fetchFn('/data/office/parvum.json')
		.then((r) => (r.ok ? (r.json() as Promise<DonneesParvum>) : null))
		.catch(() => null);
	return chargement;
}
