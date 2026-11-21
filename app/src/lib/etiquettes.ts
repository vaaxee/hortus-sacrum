/**
 * Cadre pratique (SPEC § 10) : chaque prière porte des étiquettes (fins, objets, grâces, personnes, pratiques) ;
 * l'écran du jour en fait le bilan et propose une prière pour combler un manque.
 * Étiquettes par défaut : déduites du titre et du texte par mots-clés. L'utilisateur les corrige dans la fiche de la
 * prière (champ « étiquettes ») ; ses étiquettes remplacent alors celles qui sont déduites.
 */
import type { Dimension, Dimensions } from './programme/types.ts';
import type { Texte } from './types.ts';

/** Les cinq dimensions (lot « Dimensions ») ; l'ancienne catégorie « pratique » s'appelle désormais « forme ». */
export type Categorie = Dimension;

export const CATEGORIES: [Categorie, string][] = [
	['fin', 'Fins'],
	['objet', 'Objets'],
	['grace', 'Grâces demandées'],
	['personne', 'Personnes'],
	['forme', 'Formes']
];

/** Étiquette → [catégorie, motif cherché dans le titre et le texte (minuscules), clé du vocabulaire (dimensions.json)]. */
const CADRE: Record<string, [Categorie, RegExp, string]> = {
	adoration: ['fin', /\badore|adoration|\bgloire soit\b|gloria patri/, 'adoration'],
	'action de grâces': ['fin', /remerci|actions? de grâces|reconnaissance/, 'action-de-graces'],
	réparation: ['fin', /répar|amende honorable|outrage|blasphème/, 'reparation'],
	demande: ['fin', /accordez|donnez-(?:moi|nous)|faites que|je vous (?:en )?(?:prie|supplie|demande)|obtenez/, 'demande'],
	intercession: ['fin', /priez pour (?:nous|eux|moi)|ora pro|orate pro|intercession/, 'intercession'],
	Trinité: ['objet', /trinité|trinitas/, 'trinite'],
	'Jésus-Christ': ['objet', /jésus|jesu/, 'jesus-christ'],
	Eucharistie: ['objet', /saint[- ]sacrement|eucharist|hostie|communion/, 'eucharistie'],
	'Sacré-Cœur': ['objet', /sacré[- ]c(?:œ|oe)ur|c(?:œ|oe)ur de jésus|cor jesu/, 'sacre-coeur'],
	'sainte Vierge': ['objet', /\bmarie\b|vierge|\bave\b|maria/, 'sainte-vierge'],
	'Cœur immaculé': ['objet', /c(?:œ|oe)ur immaculé|c(?:œ|oe)ur de marie|cor mariæ/, 'coeur-immacule'],
	'saint Joseph': ['objet', /joseph/, 'saint-joseph'],
	'Saint-Esprit': ['objet', /saint[- ]esprit|esprit[- ]saint|sancte spiritus|veni creator/, 'saint-esprit'],
	anges: ['objet', /\bange|archange|michel|gabriel|raphaël/, 'anges'],
	'sainte Face': ['objet', /sainte face/, 'sainte-face'],
	'âmes du purgatoire': ['objet', /purgatoire|défunts|trépassés|requiem|de profundis/, 'ames-du-purgatoire'],
	salut: ['grace', /\bsalut\b|sauvez|damn/, 'salut'],
	'persévérance finale': ['grace', /persévérance|heure de (?:la|ma|notre) mort|bonne mort|derniers moments/, 'perseverance-finale'],
	sanctification: ['grace', /sanctifi|sainteté|perfection/, 'sanctification'],
	charité: ['grace', /charité|vous aimer|aimer davantage|de plus en plus/, 'charite'],
	vertus: ['grace', /humilité|patience|pureté|chasteté|douceur|obéissance|vertus?/, 'vertus'],
	'préservation du péché': ['grace', /tentation|éviter (?:le|tout) (?:péché|mal)|préserv/, 'preservation-du-peche'],
	'protection et santé': ['grace', /protection|protégez|santé|malades?|infirm|dangers/, 'protection-et-sante'],
	"devoir d'état": ['grace', /devoirs?\b|vocation/, 'devoir-d-etat'],
	'grâces temporelles': ['grace', /temporel|besoins|notre pain/, 'graces-temporelles'],
	'soi-même': ['personne', /\bmon âme\b|\bmoi\b/, 'soi-meme'],
	famille: ['personne', /famille|parents|foyers?|ancêtres/, 'famille'],
	amis: ['personne', /\bamis\b|bienfaiteurs/, 'amis'],
	ennemis: ['personne', /ennemis|persécut/, 'ennemis'],
	pécheurs: ['personne', /pécheurs|conversion/, 'pecheurs'],
	'Église et prêtres': ['personne', /\béglise\b|prêtres|pape|pontife|ministres/, 'eglise-et-pretres'],
	dirigeants: ['personne', /\brois?\b|chefs|patrie|france|princes/, 'dirigeants'],
	mourants: ['personne', /agonisants|mourants|à l'agonie/, 'mourants'],
	défunts: ['personne', /purgatoire|défunts|trépassés/, 'defunts'],
	chapelet: ['forme', /chapelet|rosaire|dizaine/, 'chapelet'],
	litanies: ['forme', /litanies/, 'litanie'],
	office: ['forme', /\boffice\b|bréviaire|matines|vêpres|complies/, 'office'],
	examen: ['forme', /examen/, 'examen'],
	méditation: ['forme', /méditation|méditer/, 'meditation'],
	jaculatoires: ['forme', /jaculatoire/, 'jaculatoire'],
	messe: ['forme', /\bmesse\b|saint sacrifice/, 'messe']
};

export const ETIQUETTES: Record<Categorie, string[]> = { fin: [], objet: [], grace: [], personne: [], forme: [] };
for (const [e, [c]] of Object.entries(CADRE)) ETIQUETTES[c].push(e);

/** Étiquettes d'une prière : celles de l'utilisateur, sinon celles déduites du titre et du texte. */
export function etiquettesDe(t: Pick<Texte, 'titre' | 'corps'> & { etiquettes?: string[] }): string[] {
	if (t.etiquettes) return t.etiquettes;
	const s = `${t.titre}\n${t.corps}`.toLowerCase();
	return Object.entries(CADRE)
		.filter(([, [, re]]) => re.test(s))
		.map(([e]) => e);
}

export interface Bilan {
	categorie: Categorie;
	libelle: string;
	couvertes: string[];
	manques: { etiquette: string; proposition?: Pick<Texte, 'id' | 'titre'> }[];
}

/**
 * Bilan du jour : pour chaque catégorie, les étiquettes couvertes par les prières du jour et celles qui manquent, avec,
 * pour chaque manque, la prière la plus courte de la bibliothèque qui le comble (praticité).
 */
export function bilanDuJour(duJour: string[], bibliotheque: (Texte & { etiquettes?: string[] })[]): Bilan[] {
	const par = new Map(bibliotheque.map((t) => [t.id, t]));
	const couvert = new Set(duJour.flatMap((id) => (par.get(id) ? etiquettesDe(par.get(id)!) : [])));
	const candidats = bibliotheque
		.filter((t) => !t.supprimeLe && !duJour.includes(t.id) && t.corps)
		.map((t) => ({ t, e: new Set(etiquettesDe(t)), n: t.corps.length }))
		.sort((a, b) => a.n - b.n);
	return CATEGORIES.map(([categorie, libelle]) => {
		const toutes = ETIQUETTES[categorie];
		const manques = toutes
			.filter((e) => !couvert.has(e))
			.map((etiquette) => {
				const c = candidats.find((x) => x.e.has(etiquette));
				return { etiquette, proposition: c ? { id: c.t.id, titre: c.t.titre } : undefined };
			});
		return { categorie, libelle, couvertes: toutes.filter((e) => couvert.has(e)), manques };
	});
}

// ------------------------------------------------------------------ dimensions (lot « Dimensions », brouillon)

/**
 * Motifs supplémentaires, pour les valeurs du vocabulaire qui n'ont pas d'étiquette du cadre pratique. Ils ne servent
 * qu'au brouillon des dimensions (`devinee`), jamais au bilan du jour.
 */
const DEVINE: [Dimension, RegExp, string][] = [
	['fin', /\blou(?:é|e|ange|ons)\b|béni soit|bénissons|hosanna|alléluia|magnificat|te deum/, 'louange'],
	['fin', /ayez pitié|miséricorde|pardonnez|soyez-(?:nous|moi) propice|miserere|propitia/, 'propitiation'],
	['objet', /passion|crucifi|\bcroix\b|plaies|calvaire|agonie de jésus/, 'passion'],
	['objet', /précieux sang|sang précieux|sang de jésus|sang de notre-seigneur/, 'precieux-sang'],
	['objet', /\bsaints\b|bienheureux|apôtres?\b|martyrs?\b/, 'saints'],
	['forme', /\boraison\b|\bprions\b|oremus/, 'oraison'],
	['forme', /\bacte d|\bactes d/, 'acte'],
	['forme', /\bhymne\b|te deum|magnificat|veni creator|stabat mater|ave maris stella/, 'hymne'],
	['forme', /neuvaine/, 'neuvaine']
];

/** Correspondance : étiquette du cadre pratique (réglages déjà saisis dans `Texte.etiquettes`) → dimension et clé. */
export const CLE_DE_L_ETIQUETTE: Record<string, [Dimension, string]> = Object.fromEntries(
	Object.entries(CADRE).map(([e, [c, , cle]]) => [e, [c, cle]])
);

const ajouterA = (d: Dimensions, dim: Dimension, cle: string) => {
	const v = (d[dim] ??= []);
	if (!v.includes(cle)) v.push(cle);
};

/** Dimensions déduites du titre et du texte (brouillon : chaque valeur reste « devinée » jusqu'à relecture). */
export function dimensionsDevinees(t: Pick<Texte, 'titre' | 'corps'>): Dimensions {
	const s = `${t.titre}\n${t.corps}`.toLowerCase();
	const d: Dimensions = {};
	for (const [, [c, re, cle]] of Object.entries(CADRE)) if (re.test(s)) ajouterA(d, c, cle);
	for (const [c, re, cle] of DEVINE) if (re.test(s)) ajouterA(d, c, cle);
	return d;
}

/** Les étiquettes réglées par l'utilisateur (ancien champ `Texte.etiquettes`), traduites en dimensions. */
export function depuisEtiquettes(etiquettes: string[]): Dimensions {
	const d: Dimensions = {};
	for (const e of etiquettes) {
		const c = CLE_DE_L_ETIQUETTE[e];
		if (c) ajouterA(d, c[0], c[1]);
	}
	return d;
}

// ------------------------------------------------------------------ type d'une prière (filtres de Prières, lot 7)

/** Les types montrés en filtre, chacun une valeur de la dimension « forme » (corrigeable dans la fiche). */
export const TYPES: [string, string][] = [
	['litanie', 'Litanies'],
	['chapelet', 'Chapelets et couronnes'],
	['office', 'Offices'],
	['neuvaine', 'Neuvaines'],
	['acte', 'Actes et offrandes'],
	['jaculatoire', 'Jaculatoires'],
	['hymne', 'Hymnes et antiennes'],
	['oraison', 'Autres prières']
];

/**
 * Type d'une prière, déduit de sa partie et de son titre (un seul) : sert aux filtres tant que la forme n'a pas été
 * réglée ou relue. L'ordre des règles compte : une neuvaine en litanies reste une neuvaine.
 */
export function typeDeduit(t: Pick<Texte, 'titre' | 'partie'>): string {
	const titre = t.titre.toLowerCase();
	const partie = (t.partie ?? '').toLowerCase();
	// d'abord le titre, qui dit ce qu'est la pièce ; puis la partie où le livre la range
	if (/jaculatoire/.test(partie)) return 'jaculatoire';
	if (/^neuvaine/.test(titre)) return 'neuvaine';
	if (/^litanies/.test(titre)) return 'litanie';
	if (
		/te deum|magnificat|veni creator|stabat|ave maris|salve regina|sub tuum|regina c|alma redemptoris|ave, regina|inviolata|o gloriosa|o quot undis|te, joseph|hymne/.test(
			titre
		)
	)
		return 'hymne';
	if (/chapelet|couronne|rosaire|dizaine/.test(titre)) return 'chapelet';
	if (/^(acte|actes|offrande|consécration|devoir|intention)\b/.test(titre)) return 'acte';
	if (/\boffice\b|bréviaire/.test(titre)) return 'office';
	if (/neuvaine/.test(partie)) return 'neuvaine';
	if (partie === 'litanies') return 'litanie';
	if (/hymne/.test(partie)) return 'hymne';
	if (/chapelet|couronne|rosaire/.test(partie)) return 'chapelet';
	if (/bréviaire|office/.test(partie)) return 'office';
	if (/offrande|devoir|consécration|apostolat/.test(partie)) return 'acte';
	return 'oraison';
}

/** Les types d'une prière : sa forme réglée ou relue si elle en a une parmi les types, sinon le type déduit. */
export function typesDe(t: Pick<Texte, 'titre' | 'partie'>, formeReglee?: string[]): string[] {
	const reglees = (formeReglee ?? []).filter((f) => TYPES.some(([k]) => k === f));
	return reglees.length ? reglees : [typeDeduit(t)];
}
