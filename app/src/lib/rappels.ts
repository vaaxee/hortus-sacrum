/**
 * Rappels (SPEC §7) : l'app calcule les rappels des jours qui viennent et les confie au serveur,
 * qui les envoie à l'heure dite à chaque appareil abonné (notifications push), même app fermée.
 */
import { iso, jourDu, type Jour } from './calendrier.ts';
import { SUPABASE_URL, VAPID_PUBLIC } from './config.ts';
import { db } from './db.ts';
import { occurrenceDu } from './pratiques.ts';
import { garde, rangElement } from './rangs.ts';
import type { ElementListe, FetePerso, Pratique } from './types.ts';

export interface ReglagesRappels {
	actif: boolean;
	/** Heures « HH:MM », ou '' pour ne pas recevoir ce rappel. */
	matin: string;
	soir: string;
	veille: string;
	/** Heures fixes des dévotions (Angélus, agonisants, 15 h le vendredi…) réglées dans la liste du jour. */
	heuresFixes: boolean;
	/** Les heures fixes ne sonnent que pour les dévotions de ce rang et au-dessus. */
	rangMini: 'praecipua' | 'pia' | 'supererogatoria';
	veilleFetes: boolean;
	veilleJeune: boolean;
	veillePratiques: boolean;
	premiersVendrediSamedi: boolean;
	fetesPerso: boolean;
}

export const REGLAGES_DEFAUT: ReglagesRappels = {
	actif: false, matin: '07:00', soir: '21:00', veille: '20:00', heuresFixes: true, rangMini: 'supererogatoria',
	veilleFetes: true, veilleJeune: true, veillePratiques: true, premiersVendrediSamedi: true, fetesPerso: true
};

export async function lireReglages(): Promise<ReglagesRappels> {
	const r = (await db.meta.get('rappels'))?.valeur as Partial<ReglagesRappels> | undefined;
	return { ...REGLAGES_DEFAUT, ...r };
}

export async function ecrireReglages(r: ReglagesRappels): Promise<void> {
	await db.meta.put({ cle: 'rappels', valeur: r });
}

export interface Rappel {
	quand: Date;
	titre: string;
	corps: string;
	url: string;
}

const a = (date: string, heure: string) => new Date(`${date}T${heure}:00`);
const longue = (date: string) => new Date(date + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });

/** Données nécessaires au calcul, lues une fois. */
export interface Contexte {
	liste: ElementListe[];
	pratiques: Pratique[];
	fetes: FetePerso[];
	titres: Record<string, string>;
	jour: (date: string) => Promise<Jour | undefined>;
}

/** Les rappels d'une journée (date AAAA-MM-JJ), dans l'ordre des heures. */
export async function rappelsDu(date: string, r: ReglagesRappels, ctx: Contexte): Promise<Rappel[]> {
	const out: Rappel[] = [];
	const d = new Date(date + 'T12:00:00');
	const j = await ctx.jour(date);
	const demain = iso(new Date(d.getTime() + 864e5));
	const jd = await ctx.jour(demain);
	const pratiques = ctx.pratiques.filter((p) => p.active && !p.supprimeLe).map((p) => ({ p, o: occurrenceDu(p, date) })).filter((x) => x.o);

	if (r.matin) {
		const morceaux = [j?.office, j?.jeune_abstinence?.libelle,
			...pratiques.map(({ p, o }) => (o!.total ? `${p.titre} ${o!.rang}/${o!.total}` : p.titre))].filter(Boolean);
		out.push({ quand: a(date, r.matin), titre: `Aujourd’hui, ${longue(date)}`, corps: morceaux.join(' — '), url: `/?date=${date}` });
	}
	if (r.heuresFixes) {
		for (const e of ctx.liste) {
			if (!e.actif || e.supprimeLe || !e.jours[d.getDay()] || !garde(rangElement(e), r.rangMini)) continue;
			for (const h of e.rappels) {
				out.push({ quand: a(date, h), titre: e.titre, corps: e.textes[0] ? ctx.titres[e.textes[0]] ?? '' : '', url: e.textes[0] ? `/prieres/${encodeURIComponent(e.textes[0])}` : `/?date=${date}` });
			}
		}
	}
	if (r.soir) out.push({ quand: a(date, r.soir), titre: 'Prière du soir', corps: 'Examen de conscience, prière du soir et ce qui reste de la liste du jour.', url: `/?date=${date}` });

	// la veille, pour demain
	if (r.veille && jd) {
		const veille: string[] = [];
		if (r.veilleFetes && /1re cl|2e cl/.test(jd.rang ?? '')) veille.push(`${jd.office} (${jd.rang})`);
		if (r.veilleJeune && jd.jeune_abstinence) veille.push(jd.jeune_abstinence.libelle);
		const dd = new Date(demain + 'T12:00:00');
		if (r.premiersVendrediSamedi && dd.getDate() <= 7 && (dd.getDay() === 5 || dd.getDay() === 6)) veille.push(dd.getDay() === 5 ? 'premier vendredi du mois' : 'premier samedi du mois');
		if (r.veillePratiques) {
			for (const p of ctx.pratiques.filter((p) => p.active && !p.supprimeLe)) {
				const o = occurrenceDu(p, demain);
				if (o && o.rang === 1) veille.push(`début : ${p.titre}`);
			}
		}
		if (r.fetesPerso) {
			for (const f of ctx.fetes.filter((f) => !f.supprimeLe && f.rappelVeille && f.mois === dd.getMonth() + 1 && f.jour === dd.getDate())) veille.push(f.titre);
		}
		if (veille.length) out.push({ quand: a(date, r.veille), titre: `Demain, ${longue(demain)}`, corps: veille.join(' — '), url: `/?date=${demain}` });
	}
	// le jour même des fêtes et anniversaires personnels
	if (r.fetesPerso && r.matin) {
		for (const f of ctx.fetes.filter((f) => !f.supprimeLe && f.mois === d.getMonth() + 1 && f.jour === d.getDate())) {
			out.push({ quand: a(date, r.matin), titre: f.titre, corps: f.genre === 'anniversaire' ? 'Anniversaire spirituel' : 'Fête', url: `/?date=${date}` });
		}
	}
	return out.sort((x, y) => x.quand.getTime() - y.quand.getTime());
}

export async function contexte(): Promise<Contexte> {
	const [liste, pratiques, fetes, textes] = await Promise.all([db.liste.toArray(), db.pratiques.toArray(), db.fetes.toArray(), db.textes.toArray()]);
	return { liste, pratiques, fetes, titres: Object.fromEntries(textes.map((t) => [t.id, t.titre])), jour: (dt) => jourDu(dt) };
}

/** Rappels des `jours` prochains jours à partir de maintenant. */
export async function prochains(r: ReglagesRappels, jours = 14): Promise<Rappel[]> {
	const ctx = await contexte();
	const maintenant = new Date();
	const out: Rappel[] = [];
	for (let k = 0; k < jours; k++) {
		out.push(...(await rappelsDu(iso(new Date(maintenant.getTime() + k * 864e5)), r, ctx)));
	}
	return out.filter((x) => x.quand > maintenant);
}

// ------------------------------------------------------------------ abonnement et envoi au serveur
// Sans compte : l'appareil est désigné par un identifiant aléatoire gardé sur lui ; la fonction
// « rappels-appareil » enregistre son abonnement et ses rappels, « envoyer-rappels » les envoie à l'heure dite.

const FONCTION = `${SUPABASE_URL}/functions/v1/rappels-appareil`;

export const pushPossible = () =>
	typeof window !== 'undefined' && 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;

async function appareil(): Promise<string> {
	const deja = (await db.meta.get('appareil'))?.valeur as string | undefined;
	if (deja) return deja;
	const octets = crypto.getRandomValues(new Uint8Array(24));
	const id = btoa(String.fromCharCode(...octets)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
	await db.meta.put({ cle: 'appareil', valeur: id });
	return id;
}

async function appeler(action: string, donnees: Record<string, unknown> = {}): Promise<{ ok?: boolean; erreur?: string; rappels?: number }> {
	const rep = await fetch(FONCTION, {
		method: 'POST',
		headers: { 'content-type': 'application/json' },
		body: JSON.stringify({ action, appareil: await appareil(), ...donnees })
	});
	return rep.json().catch(() => ({ erreur: `réponse ${rep.status}` }));
}

function cleBinaire(b64: string): Uint8Array {
	const p = '='.repeat((4 - (b64.length % 4)) % 4);
	const s = atob((b64 + p).replace(/-/g, '+').replace(/_/g, '/'));
	return Uint8Array.from(s, (c) => c.charCodeAt(0));
}

/** Demande l'autorisation, abonne cet appareil et l'enregistre sur le serveur. Renvoie un message d'erreur, ou null. */
export async function abonner(): Promise<string | null> {
	if (!pushPossible()) return 'Ce navigateur ne permet pas les notifications. Sur iPhone, ajoutez d’abord l’app à l’écran d’accueil et ouvrez-la depuis l’icône.';
	const permission = await Notification.requestPermission();
	if (permission !== 'granted') return 'Les notifications ont été refusées. Autorisez-les dans les réglages du téléphone (Notifications → Hortus Sacrum).';
	const reg = await navigator.serviceWorker.ready;
	const abo = (await reg.pushManager.getSubscription()) ??
		(await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: cleBinaire(VAPID_PUBLIC) as BufferSource }));
	const r = await appeler('abonner', { abonnement: abo.toJSON() });
	return r.ok ? null : `L’abonnement n’a pas pu être enregistré : ${r.erreur}`;
}

/** Désabonne cet appareil et efface ses rappels à venir. */
export async function desabonner(): Promise<void> {
	await appeler('desabonner');
	if (pushPossible()) {
		const abo = await (await navigator.serviceWorker.ready).pushManager.getSubscription();
		await abo?.unsubscribe();
	}
}

/**
 * Remplace sur le serveur les rappels à venir de cet appareil par ceux calculés maintenant (14 jours).
 * Appelé à l'ouverture de l'app et après un changement de réglage.
 */
export async function planifier(): Promise<number> {
	const r = await lireReglages();
	const liste = r.actif ? await prochains(r) : [];
	const rep = await appeler('planifier', { rappels: liste.map((x) => ({ quand: x.quand.toISOString(), titre: x.titre, corps: x.corps, url: x.url })) });
	if (!rep.ok) throw new Error(rep.erreur ?? 'erreur du serveur');
	await db.meta.put({ cle: 'rappels-planifies', valeur: new Date().toISOString() });
	return rep.rappels ?? 0;
}

/** Envoie une notification d'essai à cet appareil (via le serveur, dans la minute). */
export async function essai(): Promise<string | null> {
	const r = await appeler('essai');
	return r.ok ? null : (r.erreur ?? 'erreur du serveur');
}
