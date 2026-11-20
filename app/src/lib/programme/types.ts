/**
 * Programme unique (SPEC § 11, principe 1 ; docs/conception/REFONTE_2026-11-18.md, § 2).
 * Chaque pratique est déclarée une seule fois dans data/programme/programme.json ; la journée est calculée par
 * journee() (journee.ts), sans rien stocker.
 */

/**
 * Quand une entrée ou une section vaut. Toutes les clés présentes doivent être vraies (ET) ; dans une liste, un seul
 * élément suffit (OU). Même vocabulaire que les fiches d'indulgence (mois, jours_semaine, dates, tempora).
 */
export interface Quand {
	/** 0 = dimanche … 6 = samedi. */
	jours_semaine?: number[];
	/** Rang de la semaine dans le mois : jours 1-7 → 1, 8-14 → 2… */
	semaines_du_mois?: number[];
	mois?: number[];
	/** Temps liturgique, tel que le calendrier l'écrit (« Temps pascal », « Temps du Carême »…). */
	tempora?: string[];
	/** « MM-JJ » (chaque année) ou « AAAA-MM-JJ ». */
	dates?: string[];
	/** Expression régulière sur l'office du jour (« ^Samedi saint$ »). */
	office?: string;
	/** Au moins une des conditions. */
	ou?: Quand[];
	/** Exception. */
	sauf?: Quand;
}

/** Choix d'un texte qui varie. Le résultat est un seul identifiant, ou rien (null). */
export type Choix =
	| string
	/** Sept valeurs, dimanche d'abord ; null : rien ce jour-là. */
	| { selon: 'jour_semaine'; valeurs: (string | null)[] }
	/** Roue (pratique de type roue, `roue:…`) : son élément du jour ; `parmi` sert si la roue n'est pas en base. */
	| { selon: 'rotation'; roue: string; parmi: string[]; unite: 'jour' | 'semaine' | 'mois' }
	| { selon: 'quand'; cas: { quand: Quand; texte: Choix }[]; sinon?: Choix }
	/** Prière de sainte Gertrude selon la catégorie du saint du jour (gertrude.ts). */
	| { selon: 'saint_du_jour' };

/**
 * Partie d'un texte. Les ancres sont des chaînes **exactes** du texte (une ligne de titre « ## … », une phrase) ;
 * un test vérifie qu'elles s'y trouvent.
 */
export interface Extrait {
	/** Section sous un titre (ligne exacte, « ## III. … ») jusqu'au titre suivant de même niveau ou plus haut. */
	section?: string;
	/** Début (compris) et fin (non comprise). */
	de?: string;
	a?: string;
	/** Une phrase exacte, seule. */
	phrase?: string;
	/** Paragraphes à retirer (texte exact du paragraphe), par exemple des invocations déjà dites ailleurs. */
	retirer?: string[];
	/** Le n-ième titre de ce niveau, n = rang du jour dans la série (neuvaine : « Premier jour »…). */
	rang_du_jour?: { niveau: number };
}

/** Coupe un texte hôte : un point d'insertion avant une ancre, ou après chaque partie dont le titre suit un motif. */
export interface Coupure {
	point: string;
	/** Ancre exacte : le point est placé juste avant. */
	avant?: string;
	/** Après chaque partie sous un titre de ce niveau dont le libellé suit le motif (fin de chaque dizaine). */
	apres_chaque?: { niveau: number; motif: string };
}

export type Section =
	| {
			texte: Choix;
			extrait?: Extrait;
			titre?: string;
			depliable?: boolean;
			quand?: Quand;
			coupures?: Coupure[];
			/** Pratique du plan : seulement du n-ième au m-ième jour de la série (préparation de Montfort). */
			rangs?: [number, number];
	  }
	/** Rubrique, notice, mode d'emploi : repliée, jamais comptée comme prière dite. */
	| { notice: Choix; extrait?: Extrait; titre?: string; quand?: Quand }
	/** Point d'insertion nommé. */
	| { point: string; quand?: Quand }
	/** Champ libre (intentions particulières) : ni case ni durée. */
	| { champ: string; quand?: Quand };

export type Moment = 'matin' | 'journee' | 'soir';

export interface Insertion {
	/** Entrée hôte (« prog:angelus ») et point d'insertion. */
	hote: string;
	point: string;
	/** Seulement à cette heure de l'hôte (Angélus de midi). */
	heure?: string;
	quand?: Quand;
	sections: Section[];
}

export interface EntreeProgramme {
	id: string;
	titre: string;
	/** Révision de la donnée : une correction livrée incrémente ce nombre. */
	revision: number;
	quand?: Quand;
	rang?: 'praecipua' | 'pia' | 'supererogatoria';
	/** Pratique autonome : une ligne à cocher, qui ouvre sa page. */
	page?: { moment: Moment; ordre: number; heures?: string[]; sections: Section[] };
	/** Petite pratique placée dans d'autres pages ; cochée avec elles. */
	insertions?: Insertion[];
	/** Ce qui se lit (onglet Lecture). `compte` : compté dans « Lectures du jour ». */
	lecture?: {
		section: 'office' | 'ecriture' | 'doctrine' | 'spirituel';
		route: string;
		ordre: number;
		compte: boolean;
		sections?: Section[];
	};
	/** Page explicative (onglet Dévotions), jamais dans la journée. */
	explication?: string[];
	/** Durée en minutes quand l'estimation par le texte est fausse. */
	duree?: number;
	/** Décision, audit ou source qui justifie l'entrée. */
	source: string;
}

/** Pratique du plan (table `pratiques`) : ce qu'elle fait dans la journée, selon son identifiant sans l'année. */
export type RegleDuPlan =
	/** Elle demande ce que la journée fait déjà : une note sur la ligne hôte, sans ligne de plus. */
	| { annote: string; note?: string }
	/** Elle apporte un texte propre : une ligne, avec la partie du jour. */
	| { moment: Moment; ordre: number; sections: Section[] };

export interface AFournir {
	quoi: string;
	/** Où le texte ira quand il sera transcrit. */
	ou: string;
	quand?: Quand;
}

export interface Programme {
	version: number;
	entrees: EntreeProgramme[];
	plan: Record<string, RegleDuPlan>;
	/** Formules communes (Pater, Ave, Gloria…), écartées du test d'inclusion : elles structurent les prières. */
	formules: string[];
	a_fournir: AFournir[];
}

/** Surcouche de l'utilisateur (lot 4) : ce qu'il change à une entrée livrée, ou un ajout personnel. */
export interface ReglageProgramme {
	id: string;
	actif?: boolean;
	ordre?: number;
	duree?: number;
	heures?: string[];
	quand?: Quand;
	entree?: EntreeProgramme;
}

// ------------------------------------------------------------------ résultat

export interface SectionResolue {
	genre: 'texte' | 'notice' | 'champ';
	/** Identifiant du texte (absent pour un champ). */
	texte?: string;
	extrait?: Extrait;
	titre?: string;
	depliable?: boolean;
	/** Entrée qui a apporté la section (la ligne elle-même, ou un invité). */
	origine: string;
	/** Seulement à cette heure de la ligne. */
	heure?: string;
	/** Nom du saint à mettre à la place de « N. » (prière de sainte Gertrude). */
	nom?: string;
	/** Libellé du champ libre. */
	champ?: string;
	/** Rang du jour dans une série (neuvaine), pour un extrait `rang_du_jour`. */
	rang?: number;
}

export interface Annotation {
	/** Pratique du plan ou entrée qui annote. */
	source: string;
	texte: string;
}

export interface Ligne {
	/** Identifiant de l'entrée : clé des coches, de l'historique et des boucles d'affichage. */
	id: string;
	titre: string;
	moment: Moment;
	ordre: number;
	heures?: string[];
	sections: SectionResolue[];
	/** Entrées insérées dans la page, cochées avec elle. */
	invites: string[];
	annotations: Annotation[];
	rang?: EntreeProgramme['rang'];
	duree?: number;
}

export interface Lecture {
	id: string;
	titre: string;
	section: 'office' | 'ecriture' | 'doctrine' | 'spirituel';
	route: string;
	ordre: number;
	compte: boolean;
	sections: SectionResolue[];
	invites: string[];
}

export interface Journee {
	date: string;
	lignes: Ligne[];
	lectures: Lecture[];
	/** Texte → entrées qui l'apportent ce jour-là. */
	textes: Map<string, string[]>;
	/** Textes d'une pratique du plan déjà dits dans la journée : la pratique annote la ligne qui les a. */
	fusions: { texte: string; de: string; vers: string }[];
	/** Textes en double entre entrées du programme, retirés par la garde : doit rester vide (test d'unicité). */
	conflits: { texte: string; garde: string; retire: string }[];
	a_fournir: AFournir[];
}
