/**
 * Cadre pratique (SPEC § 10) : chaque prière porte des étiquettes (fins, objets, grâces, personnes, pratiques) ;
 * l'écran du jour en fait le bilan et propose une prière pour combler un manque.
 * Étiquettes par défaut : déduites du titre et du texte par mots-clés. L'utilisateur les corrige dans la fiche de la
 * prière (champ « étiquettes ») ; ses étiquettes remplacent alors celles qui sont déduites.
 */
import type { Texte } from './types.ts';

export type Categorie = 'fin' | 'objet' | 'grace' | 'personne' | 'pratique';

export const CATEGORIES: [Categorie, string][] = [
	['fin', 'Fins'],
	['objet', 'Objets'],
	['grace', 'Grâces demandées'],
	['personne', 'Personnes'],
	['pratique', 'Pratiques']
];

/** Étiquette → [catégorie, motif cherché dans le titre et le texte (minuscules)]. */
const CADRE: Record<string, [Categorie, RegExp]> = {
	adoration: ['fin', /\badore|adoration|\bgloire soit\b|gloria patri/],
	'action de grâces': ['fin', /remerci|actions? de grâces|reconnaissance/],
	réparation: ['fin', /répar|amende honorable|outrage|blasphème/],
	demande: ['fin', /accordez|donnez-(?:moi|nous)|faites que|je vous (?:en )?(?:prie|supplie|demande)|obtenez/],
	intercession: ['fin', /priez pour (?:nous|eux|moi)|ora pro|orate pro|intercession/],
	Trinité: ['objet', /trinité|trinitas/],
	'Jésus-Christ': ['objet', /jésus|jesu/],
	Eucharistie: ['objet', /saint[- ]sacrement|eucharist|hostie|communion/],
	'Sacré-Cœur': ['objet', /sacré[- ]c(?:œ|oe)ur|c(?:œ|oe)ur de jésus|cor jesu/],
	'sainte Vierge': ['objet', /\bmarie\b|vierge|\bave\b|maria/],
	'Cœur immaculé': ['objet', /c(?:œ|oe)ur immaculé|c(?:œ|oe)ur de marie|cor mariæ/],
	'saint Joseph': ['objet', /joseph/],
	'Saint-Esprit': ['objet', /saint[- ]esprit|esprit[- ]saint|sancte spiritus|veni creator/],
	anges: ['objet', /\bange|archange|michel|gabriel|raphaël/],
	'sainte Face': ['objet', /sainte face/],
	'âmes du purgatoire': ['objet', /purgatoire|défunts|trépassés|requiem|de profundis/],
	salut: ['grace', /\bsalut\b|sauvez|damn/],
	'persévérance finale': ['grace', /persévérance|heure de (?:la|ma|notre) mort|bonne mort|derniers moments/],
	sanctification: ['grace', /sanctifi|sainteté|perfection/],
	charité: ['grace', /charité|vous aimer|aimer davantage|de plus en plus/],
	vertus: ['grace', /humilité|patience|pureté|chasteté|douceur|obéissance|vertus?/],
	'préservation du péché': ['grace', /tentation|éviter (?:le|tout) (?:péché|mal)|préserv/],
	'protection et santé': ['grace', /protection|protégez|santé|malades?|infirm|dangers/],
	"devoir d'état": ['grace', /devoirs?\b|vocation/],
	'grâces temporelles': ['grace', /temporel|besoins|notre pain/],
	'soi-même': ['personne', /\bmon âme\b|\bmoi\b/],
	famille: ['personne', /famille|parents|foyers?|ancêtres/],
	amis: ['personne', /\bamis\b|bienfaiteurs/],
	ennemis: ['personne', /ennemis|persécut/],
	pécheurs: ['personne', /pécheurs|conversion/],
	'Église et prêtres': ['personne', /\béglise\b|prêtres|pape|pontife|ministres/],
	dirigeants: ['personne', /\brois?\b|chefs|patrie|france|princes/],
	mourants: ['personne', /agonisants|mourants|à l'agonie/],
	défunts: ['personne', /purgatoire|défunts|trépassés/],
	chapelet: ['pratique', /chapelet|rosaire|dizaine/],
	litanies: ['pratique', /litanies/],
	office: ['pratique', /\boffice\b|bréviaire|matines|vêpres|complies/],
	examen: ['pratique', /examen/],
	méditation: ['pratique', /méditation|méditer/],
	jaculatoires: ['pratique', /jaculatoire/],
	messe: ['pratique', /\bmesse\b|saint sacrifice/]
};

export const ETIQUETTES: Record<Categorie, string[]> = { fin: [], objet: [], grace: [], personne: [], pratique: [] };
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
