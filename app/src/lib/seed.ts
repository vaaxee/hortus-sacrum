import { anneeLiturgique } from './calendrier.ts';
import { contenu, db } from './db.ts';
import { pratiquesDuPlan } from './plan.ts';
import type { ElementListe, Moment, Pratique, Texte } from './types.ts';
import { SOURCE_VIDE } from './types.ts';

/** Date des données de départ (livret, liste, plan) : plus ancienne que toute modification de l'utilisateur. */
const DEPART = '2000-01-01T00:00:00.000Z';

/** Conversion des pièces du livret (data/prieres/jardin.json) vers le balisage de l'app. */

interface Bloc {
	type: string;
	texte?: string;
	v?: string;
	r?: string;
	la?: string;
	fr?: string;
	items?: string[];
	numero?: string;
	fruit?: string;
	fruit_libelle?: string;
	titre?: string;
	note?: string;
}

interface Piece {
	id: string;
	ordre: number;
	titre: string;
	type: string;
	partie: { numero: string; titre: string } | null;
	jour_de_semaine: string | null;
	page_livret: number | null;
	usage: string | null;
	indulgence: string | null;
	source: string | null;
	blocs: Bloc[];
}

export function blocsVersCorps(blocs: Bloc[]): { corps: string; latin: string } {
	const fr: string[] = [];
	const la: string[] = [];
	for (const b of blocs) {
		switch (b.type) {
			case 'texte':
			case 'conclusion':
				fr.push(b.type === 'conclusion' ? `*${b.texte}*` : b.texte ?? '');
				break;
			case 'rubrique':
			case 'notice':
				fr.push(`[r]${(b.texte ?? '').replace(/\n+/g, ' ')}[/r]`);
				break;
			case 'intertitre':
				fr.push(`## ${b.texte}`);
				break;
			case 'traduction':
				fr.push(`[${b.texte}]`);
				break;
			case 'invocation':
				fr.push(b.texte ?? '');
				break;
			case 'verset':
				fr.push(`℣. ${b.v}\n℟. ${b.r}`);
				break;
			case 'strophe':
				fr.push(b.fr ?? '');
				la.push(b.la ?? '');
				break;
			case 'litanie':
				fr.push((b.items ?? []).join('\n'));
				break;
			case 'mystere':
				fr.push(`[r]${b.numero}[/r] ${b.texte}\n*${b.fruit_libelle}* ${b.fruit}`);
				break;
			case 'numero':
				fr.push(`[r]${b.numero}.[/r] ${b.texte}`);
				break;
			case 'fiche':
				fr.push(`[r]${b.titre}[/r] ${b.texte}. *${b.note}*`);
				break;
			default:
				if (b.texte) fr.push(b.texte);
		}
	}
	return { corps: fr.filter(Boolean).join('\n\n'), latin: la.filter(Boolean).join('\n\n') };
}

export function pieceVersTexte(p: Piece): Texte {
	const { corps, latin } = blocsVersCorps(p.blocs);
	const t: Texte = {
		id: `jardin:${p.id}`,
		origine: 'livret',
		titre: p.titre,
		partie: p.partie ? p.partie.titre : '',
		categorie: p.jour_de_semaine ?? '',
		corps,
		latin,
		usage: p.usage ?? '',
		indulgence: p.indulgence ?? '',
		source: {
			...SOURCE_VIDE,
			ouvrage: p.source ?? '',
			edition: 'Le Jardin de l’âme (livret)',
			page: p.page_livret ? String(p.page_livret) : ''
		},
		ordre: p.ordre,
		creeLe: '',
		modifieLe: ''
	};
	return t;
}

const TOUS = [true, true, true, true, true, true, true];
const jour = (...j: number[]) => TOUS.map((_, i) => j.includes(i));

/** Liste du jour de départ (docs/LISTE_DU_JOUR.md). Les éléments sans texte en base attendent leur source. */
function listeParDefaut(): Omit<ElementListe, 'creeLe' | 'modifieLe'>[] {
	const L: [string, Moment, 'ordinaire' | 'propre', boolean[], string[], string[]][] = [
		['Offrande du matin', 'matin', 'ordinaire', TOUS, [], ['jardin:intention-d-indulgences', 'jardin:acte-de-soumission-a-la-volonte-de-dieu', 'jardin:acte-d-intention-de-communion-spirituelle-perpetuelle', 'jardin:acte-de-recommandation-des-ames-rencontrees']],
		['Prière du matin', 'matin', 'ordinaire', TOUS, [], []],
		['Salve Regina, avec ses versets', 'matin', 'ordinaire', TOUS, [], []],
		['Intentions particulières du jour', 'matin', 'ordinaire', TOUS, [], []],
		['Cordon de saint Joseph : sept Gloria Patri', 'matin', 'ordinaire', TOUS, [], []],
		['Office du jour et vie du saint', 'propre', 'propre', TOUS, [], []],
		['Méditation du jour', 'propre', 'propre', TOUS, [], []],
		['Dévotion du jour de la semaine', 'propre', 'propre', TOUS, [], []],
		['Dévotion à jours comptés en cours', 'propre', 'propre', TOUS, [], []],
		['Neuvaine ou trentain en cours', 'propre', 'propre', TOUS, [], []],
		['Dévotion du mois', 'propre', 'propre', TOUS, [], []],
		['Angélus', 'journee', 'ordinaire', TOUS, ['06:00', '12:00', '18:00'], []],
		['Prière pour les agonisants', 'journee', 'ordinaire', TOUS, ['07:00', '12:00', '21:00'], ['jardin:priere-pour-les-agonisants']],
		['La Flèche d’or', 'journee', 'ordinaire', TOUS, ['07:00', '12:00', '21:00'], ['jardin:la-fleche-d-or']],
		['Chapelet', 'journee', 'ordinaire', TOUS, [], []],
		['Triple Couronne d’or du Sacré-Cœur', 'journee', 'ordinaire', TOUS, [], ['jardin:la-triple-couronne-d-or-du-sacre-c-ur-de-jesus']],
		['Chapelet de saint Michel (couronne angélique)', 'journee', 'ordinaire', jour(2), [], ['jardin:chapelet-de-saint-michel-archange']],
		['Chapelet des Morts', 'journee', 'ordinaire', jour(1), [], []],
		['Quinze oraisons de sainte Brigitte', 'journee', 'ordinaire', TOUS, [], ['jardin:les-quinze-oraisons-de-sainte-brigitte']],
		['Devant le Crucifix', 'journee', 'propre', jour(5), ['15:00'], ['jardin:chaque-vendredi-devant-le-crucifix']],
		['Examen de conscience', 'soir', 'ordinaire', TOUS, [], []],
		['Prière du soir', 'soir', 'ordinaire', TOUS, [], []],
		['Sub tuum, avec ses versets', 'soir', 'ordinaire', TOUS, [], []],
		['Litanies du jour', 'soir', 'propre', TOUS, [], []],
		['Demande d’un don du Saint-Esprit', 'soir', 'ordinaire', TOUS, [], []]
	];
	return L.map(([titre, moment, etiquette, jours, rappels, textes], i) => ({
		id: `liste:${i + 1}`,
		origine: 'officielle' as const,
		titre, moment, etiquette, jours, rappels, textes,
		ordre: (i + 1) * 10,
		actif: true
	}));
}

/** Premier lancement : charge le livret et la liste de départ. Ne touche jamais à ce qui existe déjà. */
export async function amorcer(fetchFn: typeof fetch = fetch): Promise<void> {
	const fait = await db.meta.get('amorce');
	const niveau = (fait?.valeur as number) ?? 0;
	if (niveau < 1) await amorcerLivret(fetchFn);
	if (niveau < 2) await importerPlan(fetchFn);
	if (niveau < 2) await db.meta.put({ cle: 'amorce', valeur: 2 });
	if (niveau < 3) {
		await amorcerSources(fetchFn);
		await db.meta.put({ cle: 'amorce', valeur: 3 });
	}
}

/** Liens par défaut entre éléments de la liste du jour et textes sourcés (titre de l'élément → identifiants). */
const LIENS_SOURCES: Record<string, string[]> = {
	'Prière du matin': ['paroissien:priere-du-matin'],
	'Prière du soir': ['paroissien:priere-du-soir'],
	'Examen de conscience': ['paroissien:priere-du-soir'],
	'Angélus': ['paroissien:angelus']
};

/**
 * Textes recopiés d'éditions anciennes (data/prieres/sources.json), marqués « Source vérifiée ».
 * Un texte déjà présent n'est jamais remplacé ; un élément de liste n'est relié que s'il n'a encore aucune prière.
 */
export async function amorcerSources(fetchFn: typeof fetch = fetch): Promise<void> {
	const rep = await fetchFn('/data/prieres/sources.json');
	if (!rep.ok) return;
	const doc = (await rep.json()) as { pieces: Omit<Texte, 'origine' | 'ordre' | 'creeLe' | 'modifieLe'>[] };
	const dernier = await db.textes.orderBy('ordre').last();
	let ordre = (dernier?.ordre ?? 0) + 1;
	for (const brut of doc.pieces) {
		if (await db.textes.get(brut.id)) continue;
		const x = { ...brut, origine: 'officielle', ordre: ordre++, creeLe: DEPART, modifieLe: DEPART } as Texte;
		x.original = contenu(x);
		await db.textes.put(x);
	}
	for (const e of await db.liste.toArray()) {
		const ids = LIENS_SOURCES[e.titre];
		if (!ids || e.textes.length) continue;
		// mise à jour de la liste de départ : l'original suit, pour que l'élément ne paraisse pas « modifié »
		const neuf = { ...e, textes: ids };
		const intact = e.original && e.original === contenu(e);
		await db.liste.put(intact ? { ...neuf, original: contenu(neuf) } : neuf);
	}
}

/**
 * Importe le plan des dévotions (année liturgique en cours et suivante) comme pratiques modifiables.
 * N'écrase jamais une pratique existante. Renvoie le nombre de pratiques ajoutées.
 */
export async function importerPlan(fetchFn: typeof fetch = fetch): Promise<number> {
	const y = new Date().getFullYear();
	const textes = await db.textes.toArray();
	const t = DEPART;
	let n = 0;
	for (const a of [y - 1, y]) {
		const annee = await anneeLiturgique(a, fetchFn);
		if (!annee) continue;
		for (const b of pratiquesDuPlan(annee, textes)) {
			if (await db.pratiques.get(b.id)) continue;
			const p = { ...b, creeLe: t, modifieLe: t } as Pratique;
			p.original = contenu(p);
			await db.pratiques.put(p);
			n++;
		}
	}
	return n;
}

async function amorcerLivret(fetchFn: typeof fetch): Promise<void> {
	const rep = await fetchFn('/data/prieres/jardin.json');
	const doc = (await rep.json()) as { pieces: Piece[] };
	const t = DEPART;
	const textes = doc.pieces.map((p) => {
		const x = pieceVersTexte(p);
		x.creeLe = x.modifieLe = t;
		x.original = contenu(x);
		return x;
	});
	const liste = listeParDefaut().map((e) => {
		const x = { ...e, creeLe: t, modifieLe: t } as ElementListe;
		x.original = contenu(x);
		return x;
	});
	await db.transaction('rw', db.textes, db.liste, db.meta, async () => {
		for (const x of textes) if (!(await db.textes.get(x.id))) await db.textes.put(x);
		for (const x of liste) if (!(await db.liste.get(x.id))) await db.liste.put(x);
	});
}
