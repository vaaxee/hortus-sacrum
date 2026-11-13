/** Modèle de données : tout est modifiable par l'utilisateur (SPEC §9). */

export type Origine = 'livret' | 'officielle' | 'personnel';

export const ORIGINE_LIBELLE: Record<Origine, string> = {
	livret: 'Livret',
	officielle: 'Source officielle vérifiée',
	personnel: 'Ajout personnel'
};

export interface Source {
	ouvrage: string;
	edition: string;
	page: string;
	url: string;
}

/** Champs communs à tout objet modifiable. */
export interface Base {
	id: string;
	origine: Origine;
	/** Copie de l'état d'origine (livret ou source vérifiée), pour « Restaurer l'original ». */
	original?: string;
	creeLe: string;
	modifieLe: string;
	/** Corbeille : date de mise à la corbeille, sinon absent. */
	supprimeLe?: string;
}

/** Prière ou texte. Le corps utilise un balisage léger : voir markup.ts. */
export interface Texte extends Base {
	titre: string;
	partie: string;
	categorie: string;
	corps: string;
	latin: string;
	usage: string;
	indulgence: string;
	source: Source;
	favori?: boolean;
	ordre: number;
}

/** Version antérieure d'un objet (historique). */
export interface Version {
	id?: number;
	table: string;
	objetId: string;
	date: string;
	contenu: string;
}

export type TypePratique =
	| 'jours_comptes'
	| 'neuvaine'
	| 'trentain'
	| 'consecration'
	| 'mois'
	| 'jour_semaine';

/** Règle de dates d'une pratique. */
export type Regle =
	| { genre: 'avant_fete'; nombre: number; jourSemaine: number | null; mois: number; jour: number }
	| { genre: 'consecutifs'; nombre: number; jourSemaine: number | null; debut: string }
	| { genre: 'fixe'; mois: number; jour: number }
	/** Le rang-ième jour de semaine de chaque mois (ex. premier vendredi). nombre et debut : série comptée (9 premiers vendredis). decalage : en jours (−1 = la veille). */
	| { genre: 'mensuel'; rang: number; jourSemaine: number; nombre?: number; debut?: string; decalage?: number }
	| { genre: 'mois_entier'; mois: number }
	| { genre: 'hebdomadaire'; jourSemaine: number };

export interface Pratique extends Base {
	titre: string;
	type: TypePratique;
	regle: Regle;
	textes: string[];
	promesses: string;
	indulgence: string;
	source: Source;
	notes: string;
	active: boolean;
}

export type Moment = 'matin' | 'propre' | 'journee' | 'soir';

export interface ElementListe extends Base {
	titre: string;
	moment: Moment;
	etiquette: 'ordinaire' | 'propre';
	ordre: number;
	/** Jours actifs : index 0 = dimanche … 6 = samedi. */
	jours: boolean[];
	/** Heures de rappel (« HH:MM ») ; plusieurs heures = pièce répétée dans la journée. */
	rappels: string[];
	textes: string[];
	actif: boolean;
}

/** Une occurrence de pratique accomplie. */
export interface Fait {
	id?: number;
	pratiqueId: string;
	date: string;
	horodatage: string;
}

export interface Coche {
	id?: number;
	date: string;
	elementId: string;
	/** Rang de la récitation dans la journée (0, 1, 2…). */
	rang: number;
	horodatage: string;
}

export interface Recueil extends Base {
	titre: string;
	auteur: string;
	source: Source;
	/** Affectation : mois, temps liturgique, fête ou neuvaine. */
	affectation: { genre: 'mois' | 'temps' | 'fete' | 'neuvaine' | 'libre'; valeur: string };
}

export interface Meditation extends Base {
	recueilId: string;
	rang: number;
	titre: string;
	corps: string;
	pratique: string;
}

export interface FetePerso extends Base {
	titre: string;
	genre: 'fete' | 'saint' | 'anniversaire';
	mois: number;
	jour: number;
	annee?: number;
	rappelVeille: boolean;
	notes: string;
}

export interface NoteJour extends Base {
	date: string;
	corps: string;
}

export const SOURCE_VIDE: Source = { ouvrage: '', edition: '', page: '', url: '' };

export const TABLES = ['textes', 'pratiques', 'liste', 'recueils', 'meditations', 'fetes', 'notes'] as const;
export type NomTable = (typeof TABLES)[number];
