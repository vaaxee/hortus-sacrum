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
	/** Code du jour dans le temporal (champ `tempora` du calendrier : « Quadp3-2 » = mardi de la Quinquagésime). */
	code_tempora?: string[];
	/**
	 * Jours comptés à partir d'un jour d'ancrage (dévotions à jours comptés) : la date vaut si elle tombe entre
	 * `ancre + de` et `ancre + a` jours (compris), pour l'une des occurrences de l'ancre. L'ancre est une fête fixe
	 * (« MM-JJ », chaque année), un jour de chaque mois (`{ jour: 1 }`) ou le `rang`-ième jour de semaine de chaque mois
	 * (`{ rang: 1, jour_semaine: 5 }` = le premier vendredi). Exemples : neuvaine qui finit la veille du premier
	 * vendredi = `{ ancre: { rang: 1, jour_semaine: 5 }, de: -9, a: -1 }` ; « les cinq dimanches avant le 13 août » =
	 * `{ ancre: '08-13', de: -35, a: -1 }` avec `jours_semaine: [0]`.
	 */
	autour?: { ancre: string | AncreMensuelle; de: number; a: number };
	/** Au moins une des conditions. */
	ou?: Quand[];
	/** Exception. */
	sauf?: Quand;
}

/** Jour d'ancrage qui revient chaque mois : un jour du mois, ou le n-ième jour de semaine (0 = dimanche). */
export type AncreMensuelle = { jour: number } | { rang: number; jour_semaine: number };

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
	/** Paragraphes [début, fin) du passage retenu (après les ancres) : pour prendre un bloc précis d'un texte du livret. */
	paras?: [number, number?];
	/** Abaisse les titres de n niveaux (« ## » → « ### » pour n = 1), quand le texte entre dans une page composée. */
	niveau?: number;
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
			/** Suite d'un texte déjà commencé dans la page (page composée) : il n'est compté qu'une fois (indulgences). */
			suite?: boolean;
			/** Pratique du plan : seulement du n-ième au m-ième jour de la série (préparation de Montfort). */
			rangs?: [number, number];
	  }
	/** Rubrique, notice, mode d'emploi : repliée, jamais comptée comme prière dite. */
	| { notice: Choix; extrait?: Extrait; titre?: string; quand?: Quand }
	/** Point d'insertion nommé. */
	| { point: string; quand?: Quand }
	/** Champ libre (intentions particulières) : ni case ni durée. */
	| { champ: string; quand?: Quand }
	/**
	 * Titre ou consigne de mise en page d'une page composée (« ## Mystères », « *On peut dire…* ») : jamais une prière.
	 * C'est ce qu'écrivait engine/composer/composer.py entre les textes sourcés.
	 */
	| { editorial: string; quand?: Quand }
	/**
	 * Début d'une partie de la page (« Prière du matin », « Offrande de la journée ») : les sections qui suivent, jusqu'à la
	 * partie suivante, se replient sous ce titre de mise en page. `replie` : fermée à l'ouverture de la page. Jamais une prière.
	 */
	| { partie: string; replie?: boolean; quand?: Quand };

export type Moment = 'matin' | 'journee' | 'soir';

export interface Insertion {
	/** Entrée hôte (« prog:angelus ») et point d'insertion. */
	hote: string;
	point: string;
	/** Seulement à cette heure de l'hôte (Angélus de midi). */
	heure?: string;
	quand?: Quand;
	sections: Section[];
	/**
	 * Le point revient plusieurs fois (fin de chaque dizaine) : la k-ième section résolue va au k-ième passage, au lieu
	 * que toutes aillent à chacun (fruit propre de chaque mystère).
	 */
	repartir?: boolean;
}

export interface EntreeProgramme {
	id: string;
	titre: string;
	/** Révision de la donnée : une correction livrée incrémente ce nombre. */
	revision: number;
	quand?: Quand;
	rang?: 'praecipua' | 'pia' | 'supererogatoria';
	/** Pratique autonome : une ligne à cocher, qui ouvre sa page. */
	page?: {
		moment: Moment;
		ordre: number;
		heures?: string[];
		sections: Section[];
		/** Sous-titre de la ligne (la couronne ou les mystères du jour). */
		sous_titre?: string | { selon: 'jour_semaine'; valeurs: string[] };
	};
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
	/**
	 * Pourquoi l'entrée est là : sa fonction dans l'économie du jour (LOT_DIMENSIONS § 3.3, lot D4). Descriptif : ne filtre
	 * rien et ne change pas la journée. Un test vérifie que ses fins rejoignent celles de ses textes.
	 */
	motif?: Motif;
}

/** Intention de l'auteur du programme pour une entrée : valeurs du vocabulaire (dimensions.json) et note libre. */
export interface Motif {
	fins?: string[];
	objets?: string[];
	note?: string;
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
	/** Date de la dernière modification (synchronisation : le plus récent l'emporte). */
	modifieLe: string;
}

// ------------------------------------------------------------------ résultat

export interface SectionResolue {
	genre: 'texte' | 'notice' | 'champ' | 'editorial' | 'partie';
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
	/** Le texte varie (jour de la semaine, roue, temps) : son titre se montre sous celui de la ligne. */
	variante?: boolean;
	/** Suite d'un texte déjà commencé dans la page : compté une seule fois. */
	suite?: boolean;
	/** Titre ou consigne de mise en page (genre « editorial »), titre de la partie (genre « partie »). */
	contenu?: string;
	/** Partie fermée à l'ouverture de la page (genre « partie »). */
	replie?: boolean;
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
	/** La couronne, les mystères du jour… */
	sousTitre?: string;
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
	/** Contexte dévotionnel (cycles du jour). Descriptif : il ne change pas les lignes. */
	contexte: ContexteDevotionnel;
	/** Valeurs de chaque dimension couvertes par les prières du jour (lignes, invités compris). */
	couverture: Record<Dimension, Couverture[]>;
	/** Valeurs non couvertes ; `requis` : demandée par le contexte du jour (ou fin principale de la SPEC). */
	manques: { dimension: Dimension; valeur: string; requis: boolean }[];
}

// ------------------------------------------------------------------ dimensions (lot « Dimensions », LOT_DIMENSIONS.md)

/** Les cinq dimensions d'une prière : ce qu'elle fait, à qui, ce qu'elle demande, pour qui, sous quelle forme. */
export type Dimension = 'fin' | 'objet' | 'grace' | 'personne' | 'forme';
export const DIMENSIONS: Dimension[] = ['fin', 'objet', 'grace', 'personne', 'forme'];
/** Classement d'un texte : valeurs du vocabulaire (data/programme/dimensions.json), par dimension. */
export type Dimensions = Partial<Record<Dimension, string[]>>;

/** Vocabulaire fermé (data/programme/dimensions.json). */
export interface Vocabulaire {
	dimensions: Record<Dimension, { libelle: string; aide: string; valeurs: Record<string, string> }>;
	/** Les cinq fins de la SPEC (§ 10), seules comptées pour la couverture de la semaine. */
	fins_principales: string[];
}

/** Ce qu'un cycle apporte au contexte du jour. */
export interface Qualification {
	objets?: string[];
	fins?: string[];
	note?: string;
}

/** Cycles dévotionnels (data/programme/cycles.json) : ils qualifient le jour, sans rien ajouter ni retirer. */
export interface Cycles {
	jour_semaine: Record<string, Qualification>;
	mois: Record<string, Qualification>;
	/** Thème de la semaine du mois : vide tant qu'il n'est pas adopté (question 1). */
	semaine_du_mois: Record<string, Qualification>;
	/** Temps liturgique (libellé du calendrier). */
	temps: Record<string, Qualification>;
	/** Fêtes, par expression régulière sur l'office du jour. */
	fetes: (Qualification & { office: string })[];
}

/** Contexte dévotionnel du jour (LOT_DIMENSIONS.md, § 4.1) : affiché, testé ; ne filtre rien. */
export interface ContexteDevotionnel {
	temps: string;
	/** Office du saint du jour, quand c'est une fête du sanctoral. */
	sanctoral?: string;
	objets: string[];
	fins: string[];
	/** Traçabilité : « passion ← vendredi ». */
	sources: { dimension: Dimension; valeur: string; de: string }[];
}

/** Valeur couverte par les lignes du jour. */
export interface Couverture {
	valeur: string;
	/** Identifiants des lignes qui la portent. */
	par: string[];
}

/** Classement livré d'un texte (data/prieres/dimensions-textes.json). */
export interface ClassementTexte extends Dimensions {
	/** Date de relecture humaine ; sans elle, toutes les valeurs comptent comme devinées. */
	releve?: string;
	/** Dimensions encore issues des motifs de etiquettes.ts. */
	devinee?: Dimension[];
}
