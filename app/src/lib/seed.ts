import { anneeLiturgique } from './calendrier.ts';
import { contenu, db, enregistrer } from './db.ts';
import { pratiquesDuPlan } from './plan.ts';
import { amorcerRoues } from './roues.ts';
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
	// à chaque lancement : n'ajoute que les textes sourcés jamais encore livrés (liste tenue dans meta « sources »)
	await amorcerSources(fetchFn);
	await amorcerLitanies();
	await amorcerDons();
	await fusionnerExamen();
	await amorcerDevotionsSemaine();
	await completerLitanies2();
	await amorcerRoues(fetchFn);
	await rouesDesLitanies();
	await litaniesDuLundi();
	await reparerLitanies();
	await rappelsDuProfil();
	await chapeletParLaRoue();
	await livrerElements();
	await renouvellementDuCordon();
}

/** Une seule fois (meta « profil-rappels ») : les anniversaires du profil spirituel déjà saisis reçoivent le rappel la veille. */
async function rappelsDuProfil(): Promise<void> {
	if (await db.meta.get('profil-rappels')) return;
	for (const f of await db.fetes.toArray()) {
		if (f.profil && !f.supprimeLe && !f.rappelVeille) await enregistrer('fetes', { ...f, rappelVeille: true });
	}
	await db.meta.put({ cle: 'profil-rappels', valeur: true });
}

/** Dédicace de chaque jour de la semaine et prières sourcées de l'app qui s'y rapportent. */
const DEVOTIONS_SEMAINE: [string, string[]][] = [
	['Dévotion du dimanche : la très sainte Trinité', ['fervent:litanies-sainte-trinite']],
	['Dévotion du lundi : les âmes du purgatoire', ['paroissien:de-profundis', 'beringer:chapelet-des-morts']],
	['Dévotion du mardi : les saints Anges', ['jardin:chapelet-de-saint-michel-archange', 'jardin:a-saint-gabriel-archange']],
	['Dévotion du mercredi : saint Joseph', ['beringer:litanies-saint-joseph', 'beringer:saint-joseph-purete']],
	['Dévotion du jeudi : le Saint-Sacrement', ['jardin:heure-sainte', 'jardin:acte-d-intention-de-communion-spirituelle-perpetuelle']],
	['Dévotion du vendredi : la Passion et le Sacré-Cœur', ['jardin:chaque-vendredi-devant-le-crucifix', 'beringer:litanies-sacre-coeur']],
	['Dévotion du samedi : la sainte Vierge', ['paroissien:litanies-sainte-vierge', 'beringer:coeur-afflige-de-marie']]
];

/** Une seule fois : « Dévotion du jour de la semaine » devient une ligne par jour, avec ses prières. */
export async function amorcerDevotionsSemaine(): Promise<void> {
	if (await db.meta.get('devotions-semaine')) return;
	for (const id of new Set(DEVOTIONS_SEMAINE.flatMap(([, t]) => t))) if (!(await db.textes.get(id))) return;
	const base = await db.liste.get('liste:8');
	if (base && base.titre === 'Dévotion du jour de la semaine' && !base.supprimeLe && !base.textes.length && base.original === contenu(base)) {
		for (let k = 0; k < 7; k++) {
			const [titre, textes] = DEVOTIONS_SEMAINE[k];
			const x = { ...base, id: k === 0 ? base.id : `liste:8-${k}`, titre, jours: jour(k), textes,
				...(k === 0 ? {} : { creeLe: DEPART, modifieLe: DEPART }) } as ElementListe;
			x.original = contenu(x);
			await db.liste.put(x);
		}
	}
	await db.meta.put({ cle: 'devotions-semaine', valeur: true });
}

/**
 * Une seule fois : « Examen de conscience » et « Prière du soir » ouvraient le même texte (l'examen est dans la prière
 * du soir du Paroissien) ; ils deviennent une seule ligne. Rien n'est touché si l'utilisateur a modifié ces lignes.
 */
export async function fusionnerExamen(): Promise<void> {
	if (await db.meta.get('examen-fusion-2')) return;
	const examen = await db.liste.get('liste:21');
	const soir = await db.liste.get('liste:22');
	// jamais modifiée par l'utilisateur : elle garde la date des données de départ
	const intact = (e?: ElementListe) => !!e && !e.supprimeLe && (e.modifieLe === DEPART || e.original === contenu(e));
	if (intact(examen) && intact(soir) && examen!.titre === 'Examen de conscience' && soir!.titre === 'Prière du soir') {
		await db.liste.delete('liste:21');
		const x = { ...soir!, titre: 'Prière du soir et examen de conscience', textes: ['paroissien:priere-du-soir'] } as ElementListe;
		x.original = contenu(x);
		await db.liste.put(x);
	}
	await db.meta.put({ cle: 'examen-fusion-2', valeur: true });
}

/** Un don par jour (dim. sagesse … sam. crainte de Dieu), d'après le Cœur affligé de Marie (Beringer 1925, n° 450). */
const DONS_PAR_JOUR: [string, string][] = [
	['sagesse', 'sagesse'], ['intelligence', 'intelligence'], ['conseil', 'conseil'], ['force', 'force'],
	['science', 'science'], ['piete', 'piété'], ['crainte', 'crainte de Dieu']
];

/** Une seule fois : remplace « Demande d'un don du Saint-Esprit » par une ligne par jour, si l'utilisateur ne l'a pas modifiée. */
export async function amorcerDons(): Promise<void> {
	// correction : « don de intelligence » → « don d’intelligence » (lignes jamais modifiées)
	const lundi = await db.liste.get('liste:25-1');
	if (lundi && lundi.titre === 'Demande du don de intelligence' && lundi.modifieLe === DEPART) {
		const x = { ...lundi, titre: 'Demande du don d’intelligence' } as ElementListe;
		x.original = contenu(x);
		await db.liste.put(x);
	}
	if (await db.meta.get('dons')) return;
	for (const [cle] of DONS_PAR_JOUR) if (!(await db.textes.get(`beringer:don-${cle}`))) return;
	const base = await db.liste.get('liste:25');
	if (base && base.titre === 'Demande d’un don du Saint-Esprit' && !base.supprimeLe && !base.textes.length && base.original === contenu(base)) {
		for (let k = 0; k < 7; k++) {
			const [cle, nom] = DONS_PAR_JOUR[k];
			const x = {
				...base,
				id: k === 0 ? base.id : `liste:25-${k}`,
				titre: `Demande du don ${/^[aeiouéè]/i.test(nom) ? `d’${nom}` : `de ${nom}`}`,
				jours: jour(k),
				textes: [`beringer:don-${cle}`],
				...(k === 0 ? {} : { creeLe: DEPART, modifieLe: DEPART })
			} as ElementListe;
			x.original = contenu(x);
			await db.liste.put(x);
		}
	}
	await db.meta.put({ cle: 'dons', valeur: true });
}

/**
 * Litanies du jour (docs/LISTE_DU_JOUR.md) : une ligne par jour de la semaine, selon la dédicace du jour,
 * les litanies alternant d'une semaine du mois à l'autre. Jours sans litanie sourcée : ligne sans prière.
 */
const LITANIES_PAR_JOUR: string[][] = [
	['fervent:litanies-sainte-trinite', 'paroissien:litanies-saint-nom', 'paroissien:litanies-des-saints'], // dimanche : sainte Trinité
	['fsspx:litanies-delivrance-ames-purgatoire', 'salve-regina:litanies-fideles-defunts'], // lundi : âmes du purgatoire
	['fervent:litanies-ange-gardien', 'jardin:litanies-de-la-sainte-face'], // mardi : saints Anges
	['beringer:litanies-saint-joseph'], // mercredi : saint Joseph
	['fervent:litanies-saint-sacrement', 'paroissien:litanies-saint-nom'], // jeudi : Saint-Sacrement
	['beringer:litanies-sacre-coeur', 'jardin:litanies-de-notre-dame-des-sept-douleurs'], // vendredi : Passion, Sacré-Cœur
	['paroissien:litanies-sainte-vierge', 'jardin:litanies-de-notre-dame-des-sept-douleurs'] // samedi : sainte Vierge
];

/**
 * Une seule fois : remplace la ligne générique « Litanies du jour » par sept lignes (une par jour).
 * Ne touche à rien si l'utilisateur a modifié cette ligne. Attend que tous les textes soient livrés.
 */
export async function amorcerLitanies(): Promise<void> {
	for (const id of new Set(LITANIES_PAR_JOUR.flat())) if (!(await db.textes.get(id))) return;
	// la division en sept lignes passe d'abord : remplie avant, la ligne de départ n'était plus divisée
	if (!(await db.meta.get('litanies'))) await diviserLitanies();
	await completerLitanies();
}

async function diviserLitanies(): Promise<void> {
	const base = await db.liste.get('liste:24');
	if (base && base.titre === 'Litanies du jour' && !base.supprimeLe && !base.textes.length && base.original === contenu(base)) {
		for (let k = 0; k < 7; k++) {
			const textes = LITANIES_PAR_JOUR[k];
			const x = {
				...base,
				id: k === 0 ? base.id : `liste:24-${k}`,
				jours: jour(k),
				textes,
				alterner: textes.length > 1,
				...(k === 0 ? {} : { creeLe: DEPART, modifieLe: DEPART })
			} as ElementListe;
			delete x.original;
			x.original = contenu(x);
			await db.liste.put(x);
		}
	}
	await db.meta.put({ cle: 'litanies', valeur: true });
}

/**
 * Réparation (meta « litanies-reparees ») : sur les installations où la ligne « Litanies du jour » a reçu les litanies
 * du dimanche avant d'être divisée, elle restait seule, tous les jours. Si elle n'a pas été modifiée, on la divise
 * en sept lignes, puis chaque jour reçoit ses litanies et sa roue.
 */
async function reparerLitanies(): Promise<void> {
	if (await db.meta.get('litanies-reparees')) return;
	for (const id of new Set(LITANIES_PAR_JOUR.flat())) if (!(await db.textes.get(id))) return;
	const base = await db.liste.get('liste:24');
	const intact = (e: ElementListe) => e.modifieLe === DEPART || e.original === contenu(e);
	if (base && base.titre === 'Litanies du jour' && !base.supprimeLe && intact(base) && base.jours.every(Boolean) && !(await db.liste.get('liste:24-1'))) {
		for (let k = 0; k < 7; k++) {
			const x = { ...base, id: k === 0 ? base.id : `liste:24-${k}`, jours: jour(k), textes: LITANIES_PAR_JOUR[k], alterner: false, creeLe: DEPART, modifieLe: DEPART } as ElementListe;
			delete x.roue;
			delete x.original;
			x.original = contenu(x);
			await db.liste.put(x);
		}
		for (let k = 0; k < 7; k++) await roueDesLitanies(k);
	}
	await db.meta.put({ cle: 'litanies-reparees', valeur: true });
}

/** Litanies trouvées après coup : remplit les lignes du jour restées vides et jamais modifiées par l'utilisateur. */
async function completerLitanies(): Promise<void> {
	for (let k = 0; k < 7; k++) {
		const e = await db.liste.get(k === 0 ? 'liste:24' : `liste:24-${k}`);
		const textes = LITANIES_PAR_JOUR[k];
		if (!e || e.supprimeLe || e.textes.length || !textes.length || e.original !== contenu(e) || !e.jours[k]) continue;
		const x = { ...e, textes, alterner: textes.length > 1 } as ElementListe;
		x.original = contenu(x);
		await db.liste.put(x);
	}
	await livrerElements();
}

/**
 * Une seule fois (meta « litanies-2 ») : les litanies trouvées dans le Fervent chrétien (1868) rejoignent les lignes
 * du dimanche, du mardi et du jeudi, et la dévotion du dimanche. Seulement les lignes jamais modifiées par l'utilisateur.
 */
async function completerLitanies2(): Promise<void> {
	if (await db.meta.get('litanies-2')) return;
	for (const id of ['fervent:litanies-sainte-trinite', 'fervent:litanies-ange-gardien', 'fervent:litanies-saint-sacrement']) if (!(await db.textes.get(id))) return;
	const intact = (e?: ElementListe) => !!e && !e.supprimeLe && (e.modifieLe === DEPART || e.original === contenu(e));
	for (const k of [0, 2, 4]) {
		const e = await db.liste.get(k === 0 ? 'liste:24' : `liste:24-${k}`);
		if (!intact(e) || !e!.jours[k]) continue;
		const textes = LITANIES_PAR_JOUR[k];
		const x = { ...e!, textes, alterner: textes.length > 1 } as ElementListe;
		x.original = contenu(x);
		await db.liste.put(x);
	}
	const dim = await db.liste.get('liste:8');
	if (intact(dim) && dim!.titre.startsWith('Dévotion du dimanche') && !dim!.textes.length) {
		const x = { ...dim!, textes: DEVOTIONS_SEMAINE[0][1] } as ElementListe;
		x.original = contenu(x);
		await db.liste.put(x);
	}
	await db.meta.put({ cle: 'litanies-2', valeur: true });
}

const JOURS_NOMS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
/**
 * Une seule fois (meta « roues-litanies ») : les litanies du jour ne tournent plus selon la semaine du mois mais sur une
 * roue par jour, qui avance d'un cran chaque semaine depuis le premier dimanche de l'Avent. Les roues sont hors de la
 * rosace (champ « liste ») et restent modifiables ; seules les lignes jamais modifiées sont reliées.
 */
async function rouesDesLitanies(): Promise<void> {
	if (await db.meta.get('roues-litanies')) return;
	for (const id of new Set(LITANIES_PAR_JOUR.flat())) if (!(await db.textes.get(id))) return;
	for (let k = 0; k < 7; k++) if (k !== 1) await roueDesLitanies(k);
	await db.meta.put({ cle: 'roues-litanies', valeur: true });
}

/** Une seule fois (meta « roues-litanies-lundi ») : les litanies des défunts trouvées pour le lundi tournent elles aussi. */
async function litaniesDuLundi(): Promise<void> {
	if (await db.meta.get('roues-litanies-lundi')) return;
	for (const id of LITANIES_PAR_JOUR[1]) if (!(await db.textes.get(id))) return;
	await roueDesLitanies(1);
	await db.meta.put({ cle: 'roues-litanies-lundi', valeur: true });
}

async function roueDesLitanies(k: number): Promise<void> {
	const intact = (e?: ElementListe) => !!e && !e.supprimeLe && (e.modifieLe === DEPART || e.original === contenu(e));
	{
		const ids = LITANIES_PAR_JOUR[k];
		if (ids.length < 2) return;
		const id = `roue:litanies-${k}`;
		if (!(await db.pratiques.get(id))) {
			const elements = [];
			for (const t of ids) elements.push({ fr: (await db.textes.get(t))?.titre ?? t, texte: t });
			const r = {
				id, origine: 'officielle', titre: `Litanies du ${JOURS_NOMS[k]}`, type: 'roue', regle: { genre: 'roue', unite: 'semaine' },
				textes: ids, promesses: '', indulgence: '', source: { ...SOURCE_VIDE }, notes: '', active: true, liste: true, elements,
				creeLe: DEPART, modifieLe: DEPART
			} as Pratique;
			r.original = contenu(r);
			await db.pratiques.put(r);
		}
		const e = await db.liste.get(k === 0 ? 'liste:24' : `liste:24-${k}`);
		if (intact(e) && e!.jours[k] && (!e!.textes.length || e!.textes.every((t) => ids.includes(t)))) {
			const x = { ...e!, textes: ids, roue: id, alterner: false } as ElementListe;
			x.original = contenu(x);
			await db.liste.put(x);
		}
	}
}

/** Une seule fois : la ligne « Chapelet » ouvre le chapelet de saint Dominique et suit la roue des trois chapelets. */
async function chapeletParLaRoue(): Promise<void> {
	if (await db.meta.get('chapelet-roue')) return;
	if (!(await db.textes.get('sambucy:chapelet-saint-dominique')) || !(await db.pratiques.get('roue:chapelets-rosaire'))) return;
	const e = (await db.liste.toArray()).find((x) => x.titre === 'Chapelet' && !x.supprimeLe);
	if (e && (e.modifieLe === DEPART || e.original === contenu(e)) && !e.textes.length) {
		const x = { ...e, roue: 'roue:chapelets-rosaire', textes: ['sambucy:chapelet-saint-dominique'] } as ElementListe;
		x.original = contenu(x);
		await db.liste.put(x);
	}
	await db.meta.put({ cle: 'chapelet-roue', valeur: true });
}

const CORDON_TITRE = 'Cordon de saint Joseph : renouvellement et prière pour la pureté';
const CORDON_TEXTES = ['hortus:renouvellement-cordon-saint-joseph', 'beringer:saint-joseph-purete'];

/** Une seule fois (meta « cordon-renouvellement ») : la ligne du mercredi reçoit la formule de renouvellement, si jamais modifiée. */
async function renouvellementDuCordon(): Promise<void> {
	if (await db.meta.get('cordon-renouvellement')) return;
	if (!(await db.textes.get(CORDON_TEXTES[0]))) return;
	const e = await db.liste.get('liste:cordon-mercredi');
	if (e && !e.supprimeLe && (e.modifieLe === DEPART || e.original === contenu(e)) && e.textes.join() === 'beringer:saint-joseph-purete') {
		const x = { ...e, titre: CORDON_TITRE, textes: CORDON_TEXTES } as ElementListe;
		x.original = contenu(x);
		await db.liste.put(x);
	}
	await db.meta.put({ cle: 'cordon-renouvellement', valeur: true });
}

/** Éléments ajoutés à la liste de départ après sa création ; chacun n'est livré qu'une fois (meta « elements »). */
const NOUVEAUX_ELEMENTS: Omit<ElementListe, 'creeLe' | 'modifieLe'>[] = [
	{
		id: 'liste:cordon-mercredi', origine: 'officielle', titre: CORDON_TITRE,
		moment: 'matin', etiquette: 'ordinaire', jours: jour(3), rappels: [], textes: CORDON_TEXTES, ordre: 51, actif: true
	},
	{
		id: 'liste:roue', origine: 'officielle', titre: 'La roue du jour',
		moment: 'propre', etiquette: 'propre', jours: TOUS, rappels: [], textes: [], ordre: 75, actif: true
	}
];

async function livrerElements(): Promise<void> {
	const livres = new Set(((await db.meta.get('elements'))?.valeur as string[] | undefined) ?? []);
	const nouveaux = NOUVEAUX_ELEMENTS.filter((e) => !livres.has(e.id));
	if (!nouveaux.length) return;
	for (const e of nouveaux) {
		livres.add(e.id);
		if (await db.liste.get(e.id)) continue;
		const x = { ...e, creeLe: DEPART, modifieLe: DEPART } as ElementListe;
		x.original = contenu(x);
		await db.liste.put(x);
	}
	await db.meta.put({ cle: 'elements', valeur: [...livres] });
}

/** Liens par défaut entre éléments de la liste du jour et textes sourcés (titre de l'élément → identifiants). */
const LIENS_SOURCES: Record<string, string[]> = {
	'Prière du matin': ['paroissien:priere-du-matin'],
	'Prière du soir': ['paroissien:priere-du-soir'],
	'Examen de conscience': ['paroissien:priere-du-soir'],
	'Angélus': ['paroissien:angelus'],
	'Salve Regina, avec ses versets': ['beringer:salve-regina'],
	'Sub tuum, avec ses versets': ['beringer:sub-tuum'],
	'Chapelet des Morts': ['beringer:chapelet-des-morts', 'paroissien:de-profundis'],
	'Cordon de saint Joseph : sept Gloria Patri': ['beringer:cordon-saint-joseph']
};

/**
 * Textes recopiés d'éditions anciennes (data/prieres/sources.json), marqués « Source vérifiée ».
 * Chaque texte n'est livré qu'une fois : supprimé ou modifié par l'utilisateur, il n'est jamais remis ni remplacé.
 * Un élément de liste n'est relié qu'au moment de la livraison, et seulement s'il n'a encore aucune prière.
 */
export async function amorcerSources(fetchFn: typeof fetch = fetch): Promise<void> {
	const rep = await fetchFn('/data/prieres/sources.json');
	if (!rep.ok) return;
	const doc = (await rep.json()) as { pieces: Omit<Texte, 'origine' | 'ordre' | 'creeLe' | 'modifieLe'>[] };
	const livres = new Set(((await db.meta.get('sources'))?.valeur as string[] | undefined) ?? []);
	const nouveaux = doc.pieces.filter((p) => !livres.has(p.id));
	if (!nouveaux.length) return;
	const dernier = await db.textes.orderBy('ordre').last();
	let ordre = (dernier?.ordre ?? 0) + 1;
	for (const brut of nouveaux) {
		livres.add(brut.id);
		if (await db.textes.get(brut.id)) continue;
		const x = { ...brut, origine: 'officielle', ordre: ordre++, creeLe: DEPART, modifieLe: DEPART } as Texte;
		x.original = contenu(x);
		await db.textes.put(x);
	}
	for (const e of await db.liste.toArray()) {
		const ids = LIENS_SOURCES[e.titre]?.filter((id) => nouveaux.some((p) => p.id === id));
		if (!ids?.length || e.textes.length) continue;
		// mise à jour de la liste de départ : l'original suit, pour que l'élément ne paraisse pas « modifié »
		const neuf = { ...e, textes: ids };
		const intact = e.original && e.original === contenu(e);
		await db.liste.put(intact ? { ...neuf, original: contenu(neuf) } : neuf);
	}
	await db.meta.put({ cle: 'sources', valeur: [...livres] });
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
