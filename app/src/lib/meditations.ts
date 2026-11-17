import type { Jour } from './calendrier.ts';

/** Une méditation ou une lecture d'un recueil ancien, rattachée à un jour par une clé. */
export interface EntreeRecueil {
	/** T:<temporal> (Adv1-0…), D:<MM-JJ> (date fixe), F:<fête mobile>, O:10-<n> (n-ième dimanche d'octobre). */
	cle: string | null;
	titre: string;
	tome: number;
	page: number;
	sommaire?: string;
	corps: string;
}

export interface Recueil {
	id: string;
	titre: string;
	auteur: string;
	editions: Record<string, string>;
	provenance: string;
	entrees: EntreeRecueil[];
}

const cache = new Map<string, Promise<Recueil | null>>();

export function chargerRecueil(id: string, fetchFn: typeof fetch = fetch): Promise<Recueil | null> {
	if (!cache.has(id)) {
		cache.set(
			id,
			fetchFn(`/data/recueils/${id}.json`)
				.then((r) => (r.ok ? (r.json() as Promise<Recueil>) : null))
				.catch(() => null)
		);
	}
	return cache.get(id)!;
}

/**
 * Clés à essayer pour un jour, de la plus propre à la plus générale :
 * fête mobile, dimanche d'octobre, date fixe, puis jour du temporal.
 */
export function clesDuJour(date: string, jour?: Pick<Jour, 'tempora'> | null): string[] {
	const d = new Date(date + 'T12:00:00');
	const md = date.slice(5);
	const cles: string[] = [];
	const t = jour?.tempora ?? null;
	if (t === 'Pent02-5') cles.push('F:sacre-coeur');
	if (d.getMonth() === 9 && d.getDay() === 0) cles.push(`O:10-${Math.ceil(d.getDate() / 7)}`);
	cles.push(`D:${md}`);
	if (t) cles.push(`T:${t}`);
	// 12 et 13 janvier, sans clé du temporal : semaine après le premier dimanche de l'Épiphanie
	else if (md === '01-12' || md === '01-13') cles.push(`T:Epi1-${d.getDay()}`);
	return cles;
}

/** Jour « ordinaire » : férie hors dimanche, au temps après l'Épiphanie ou après la Pentecôte. */
export function estOrdinaire(date: string, jour?: Pick<Jour, 'tempora'> | null): boolean {
	const t = jour?.tempora;
	return !!t && /^(Epi|Pent)\d+-[1-6]$/.test(t) && new Date(date + 'T12:00:00').getDay() !== 0;
}

/**
 * Rang du jour dans le parcours de Chaignon : on suit ses méditations dans l'ordre, un jour ordinaire après l'autre,
 * depuis le début de l'année liturgique (et l'on recommence au début quand le parcours est fini).
 */
export function rangParcours(date: string, annee: Pick<Jour, 'date' | 'tempora'>[], taille: number): number {
	const n = annee.filter((j) => j.date <= date && estOrdinaire(j.date, j)).length;
	return taille ? ((Math.max(1, n) - 1) % taille) + 1 : 0;
}

export interface Choix {
	recueil: Recueil;
	entree: EntreeRecueil;
}

/**
 * Méditations du jour, la principale d'abord.
 * Dimanches et temps forts : Hamon. Jours ordinaires : le parcours de Chaignon (« le fidèle sanctifié »).
 * Les autres méditations propres au jour (fête dans l'un ou l'autre recueil) suivent, au choix.
 */
/** Recueil propre à chaque mois de dévotion (mois → identifiant). */
export const RECUEIL_DU_MOIS: Record<number, string> = {
	3: 'mois-joseph',
	5: 'mois-marie',
	6: 'mois-sacre-coeur',
	7: 'mois-precieux-sang',
	11: 'mois-purgatoire'
};

/** Nom court d'un recueil, pour les boutons de choix. */
export const NOM_COURT: Record<string, string> = {
	'index/hamon': 'Hamon',
	'index/chaignon': 'Chaignon',
	'index/mois-joseph': 'Mois de saint Joseph',
	'index/mois-marie': 'Mois de Marie',
	'index/mois-sacre-coeur': 'Mois du Sacré-Cœur',
	'index/mois-precieux-sang': 'Mois du Précieux Sang',
	'index/mois-purgatoire': 'Mois des âmes',
	hamon: 'Hamon',
	chaignon: 'Chaignon',
	'mois-joseph': 'Mois de saint Joseph',
	'mois-marie': 'Mois de Marie',
	'mois-sacre-coeur': 'Mois du Sacré-Cœur',
	'mois-precieux-sang': 'Mois du Précieux Sang',
	'mois-purgatoire': 'Mois des âmes'
};

/** Pendant un mois de dévotion, la méditation du recueil du mois passe en tête ; les autres restent au choix. */
export function choisirAvecMois(
	date: string,
	jour: Pick<Jour, 'tempora'> | undefined | null,
	annee: Pick<Jour, 'date' | 'tempora'>[],
	hamon: Recueil | null,
	chaignon: Recueil | null,
	mois: Recueil | null
): Choix[] {
	const base = choisir(date, jour, annee, hamon, chaignon);
	const e = mois?.entrees.find((x) => x.cle === `J:${Number(date.slice(8, 10))}`);
	return mois && e ? [{ recueil: mois, entree: e }, ...base] : base;
}

export function choisir(
	date: string,
	jour: Pick<Jour, 'tempora'> | undefined | null,
	annee: Pick<Jour, 'date' | 'tempora'>[],
	hamon: Recueil | null,
	chaignon: Recueil | null
): Choix[] {
	const h = hamon ? entreesDuJour(hamon, date, jour).map((entree) => ({ recueil: hamon, entree })) : [];
	const cPropres = chaignon
		? entreesDuJour({ ...chaignon, entrees: chaignon.entrees.filter((e) => !e.cle?.startsWith('S:')) }, date, jour).map((entree) => ({
				recueil: chaignon,
				entree
			}))
		: [];
	const fete = h.some((x) => x.entree.cle?.startsWith('D:') || x.entree.cle?.startsWith('F:'));
	if (chaignon && estOrdinaire(date, jour) && !fete) {
		const parcours = chaignon.entrees.filter((e) => e.cle?.startsWith('S:'));
		const n = rangParcours(date, annee, parcours.length);
		const p = parcours.find((e) => e.cle === `S:${n}`);
		if (p) return [{ recueil: chaignon, entree: p }, ...cPropres, ...h];
	}
	return [...h, ...cPropres];
}

/** Guéranger, L'Année liturgique : un index (clé → volume, rang) et un fichier par volume, chargé à la demande. */
interface IndexGueranger extends Omit<Recueil, 'entrees'> {
	index: Record<string, [number, number][]>;
}
let indexG: Promise<IndexGueranger | null> | null = null;
const volumesG = new Map<number, Promise<EntreeRecueil[]>>();

export async function lecturesDuJour(
	date: string,
	jour?: Pick<Jour, 'tempora'> | null,
	fetchFn: typeof fetch = fetch
): Promise<{ recueil: Omit<Recueil, 'entrees'>; entrees: EntreeRecueil[] }> {
	indexG ??= fetchFn('/data/recueils/gueranger/index.json')
		.then((r) => (r.ok ? r.json() : null))
		.catch(() => null);
	const ix = await indexG;
	if (!ix) return { recueil: { id: 'gueranger', titre: '', auteur: '', editions: {}, provenance: '' }, entrees: [] };
	const { index, ...recueil } = ix;
	for (const c of clesDuJour(date, jour)) {
		const refs = index[c];
		if (!refs?.length) continue;
		const entrees: EntreeRecueil[] = [];
		for (const [v, r] of refs) {
			if (!volumesG.has(v)) {
				volumesG.set(
					v,
					fetchFn(`/data/recueils/gueranger/v${String(v).padStart(2, '0')}.json`)
						.then((x) => (x.ok ? x.json() : { entrees: [] }))
						.then((d) => d.entrees as EntreeRecueil[])
						.catch(() => [])
				);
			}
			const e = (await volumesG.get(v)!)[r];
			if (e) entrees.push(e);
		}
		return { recueil, entrees };
	}
	return { recueil, entrees: [] };
}

/** Les méditations du recueil pour ce jour (plusieurs quand une fête en a plusieurs), dans l'ordre du livre. */
export function entreesDuJour(r: Recueil, date: string, jour?: Pick<Jour, 'tempora'> | null): EntreeRecueil[] {
	for (const c of clesDuJour(date, jour)) {
		const trouvees = r.entrees.filter((e) => e.cle === c);
		if (trouvees.length) return trouvees;
	}
	return [];
}
