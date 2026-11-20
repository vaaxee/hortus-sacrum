/**
 * Compte et synchronisation entre appareils.
 *
 * Principe : chaque appareil garde toutes ses données en local (IndexedDB) et fonctionne hors ligne.
 * Chaque écriture locale est notée dans une file d'envoi (« sortie »). Une synchronisation :
 *   1. reçoit ce qui a changé sur le serveur depuis la dernière fois, et l'applique s'il est plus récent ;
 *   2. envoie la file d'envoi ;
 * Conflits : le plus récent l'emporte (champ modifieLe). Les suppressions se propagent.
 */
import { createClient, type Session, type SupabaseClient } from '@supabase/supabase-js';
import type { Table } from 'dexie';
import { writable } from 'svelte/store';
import { SUPABASE_CLE, SUPABASE_URL } from './config.ts';
import { db } from './db.ts';

export const COLLECTIONS = [
	'textes',
	'pratiques',
	'liste',
	'programme',
	'recueils',
	'meditations',
	'fetes',
	'notes',
	'coches',
	'faits',
	'versions'
] as const;
export type Collection = (typeof COLLECTIONS)[number];

type Ligne = Record<string, unknown>;
/** Journaux à clé numérique locale : leur identité commune entre appareils est une clé naturelle. */
const NATURELLES: Partial<Record<Collection, (o: Ligne) => string>> = {
	coches: (o) => `${o.date}|${o.elementId}|${o.rang}`,
	faits: (o) => `${o.pratiqueId}|${o.date}`,
	versions: (o) => `${o.table}|${o.objetId}|${o.date}`
};
const cle = (c: Collection, o: Ligne) => NATURELLES[c]?.(o) ?? String(o.id);
const dateDe = (c: Collection, o: Ligne) => String(o.modifieLe ?? o.horodatage ?? o.date ?? new Date(0).toISOString());
const table = (c: Collection) => db[c] as unknown as Table<Ligne, string | number>;

// ------------------------------------------------------------------ file d'envoi (hooks Dexie)
let appliquantDistant = false;

function noter(c: Collection, o: Ligne | undefined, efface: boolean) {
	if (appliquantDistant || !o) return;
	const entree = { cle: `${c}:${cle(c, o)}`, collection: c, id: cle(c, o), efface, contenu: efface ? null : o };
	// hors de la transaction en cours : la file est écrite dès que l'écriture a réussi
	queueMicrotask(() => {
		db.sortie.put(entree).catch((e) => console.error(e));
		planifier();
	});
}

let hooksInstalles = false;
export function installerSuivi() {
	if (hooksInstalles) return;
	hooksInstalles = true;
	for (const c of COLLECTIONS) {
		const t = table(c);
		t.hook('creating', function (_k, obj) {
			this.onsuccess = (k) => noter(c, { ...obj, ...(NATURELLES[c] ? {} : { id: k }) }, false);
		});
		t.hook('updating', function (mods, _k, obj) {
			const apres = { ...obj } as Ligne;
			for (const [champ, v] of Object.entries(mods)) {
				if (v === undefined) delete apres[champ];
				else apres[champ] = v;
			}
			this.onsuccess = () => noter(c, apres, false);
		});
		t.hook('deleting', function (_k, obj) {
			this.onsuccess = () => noter(c, obj as Ligne, true);
		});
	}
}

// ------------------------------------------------------------------ compte
let client: SupabaseClient | undefined;
export function supabase(): SupabaseClient {
	client ??= createClient(SUPABASE_URL, SUPABASE_CLE, {
		auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: 'pkce' }
	});
	return client;
}

export type EtatSync =
	| { genre: 'deconnecte' }
	| { genre: 'en_cours'; courriel: string }
	| { genre: 'a_jour'; courriel: string; quand: string }
	| { genre: 'erreur'; courriel: string; message: string };

export const etatSync = writable<EtatSync>({ genre: 'deconnecte' });
let session: Session | null = null;

export async function initialiserCompte() {
	installerSuivi();
	const sb = supabase();
	const { data } = await sb.auth.getSession();
	session = data.session;
	sb.auth.onAuthStateChange((_evt, s) => {
		const nouvelle = !session && s;
		session = s;
		if (!s) etatSync.set({ genre: 'deconnecte' });
		// jamais d'appel à Supabase dans ce rappel : il garde le verrou de session, et la synchronisation
		// l'attendrait sans fin. On la lance juste après.
		else if (nouvelle) setTimeout(() => synchroniser(true), 0);
	});
	if (session) synchroniser();
	window.addEventListener('online', () => synchroniser());
	document.addEventListener('visibilitychange', () => {
		if (document.visibilityState === 'visible') synchroniser();
	});
}

/** Envoie le lien de connexion par courriel. */
export async function envoyerLien(courriel: string): Promise<string | null> {
	const { error } = await supabase().auth.signInWithOtp({
		email: courriel.trim(),
		options: { emailRedirectTo: `${location.origin}/reglages` }
	});
	return error ? error.message : null;
}

/**
 * Connexion par le code reçu dans le même courriel. Indispensable pour l'app installée sur l'écran d'accueil :
 * le lien s'ouvre dans le navigateur, qui ne partage pas sa session avec l'app installée.
 */
export async function verifierCode(courriel: string, code: string): Promise<string | null> {
	const { error } = await supabase().auth.verifyOtp({ email: courriel.trim(), token: code.replace(/\s/g, ''), type: 'email' });
	return error ? error.message : null;
}

export async function deconnecter() {
	await supabase().auth.signOut();
	await db.meta.delete('sync-curseur');
	etatSync.set({ genre: 'deconnecte' });
}

// ------------------------------------------------------------------ synchronisation
let minuterie: ReturnType<typeof setTimeout> | undefined;
/** Regroupe les écritures rapprochées : une synchronisation deux secondes après la dernière. */
function planifier() {
	if (!session) return;
	clearTimeout(minuterie);
	minuterie = setTimeout(() => synchroniser(), 2000);
}

let enCours: Promise<void> | undefined;
export function synchroniser(premiere = false): Promise<void> {
	if (!session) return Promise.resolve();
	enCours ??= executer(premiere).finally(() => (enCours = undefined));
	return enCours;
}

async function executer(premiere: boolean) {
	const courriel = session?.user.email ?? '';
	etatSync.set({ genre: 'en_cours', courriel });
	try {
		// premier passage sur cet appareil avec ce compte : tout ce qui est local part au serveur
		const deja = await db.meta.get(`sync-compte:${session!.user.id}`);
		if (premiere || !deja) await toutMettreEnFile();
		await recevoir();
		await envoyer();
		await db.meta.put({ cle: `sync-compte:${session!.user.id}`, valeur: true });
		etatSync.set({ genre: 'a_jour', courriel, quand: new Date().toISOString() });
	} catch (e) {
		console.error(e);
		etatSync.set({ genre: 'erreur', courriel, message: e instanceof Error ? e.message : String(e) });
	}
}

async function toutMettreEnFile() {
	for (const c of COLLECTIONS) {
		const lignes = await table(c).toArray();
		await db.sortie.bulkPut(lignes.map((o) => ({ cle: `${c}:${cle(c, o)}`, collection: c, id: cle(c, o), efface: false, contenu: o })));
	}
}

/** Contenu envoyé au serveur : sans la clé numérique locale des journaux. */
function nettoyer(c: Collection, o: Ligne): Ligne {
	if (!NATURELLES[c]) return o;
	const { id: _id, ...reste } = o;
	return reste;
}

async function envoyer() {
	const file = await db.sortie.toArray();
	const user_id = session!.user.id;
	for (let i = 0; i < file.length; i += 200) {
		const lot = file.slice(i, i + 200);
		const lignes = lot.map((e) => ({
			user_id,
			collection: e.collection,
			id: e.id,
			contenu: e.efface ? {} : nettoyer(e.collection as Collection, e.contenu as Ligne),
			modifie_le: e.efface ? new Date().toISOString() : dateDe(e.collection as Collection, e.contenu as Ligne),
			efface: e.efface
		}));
		const { error } = await supabase().from('documents').upsert(lignes, { onConflict: 'user_id,collection,id' });
		if (error) throw new Error(error.message);
		// on ne retire de la file que ce qui n'a pas été réécrit entre-temps
		for (const e of lot) {
			const actuel = await db.sortie.get(e.cle);
			if (actuel && JSON.stringify(actuel) === JSON.stringify(e)) await db.sortie.delete(e.cle);
		}
	}
}

async function recevoir() {
	const curseur = ((await db.meta.get('sync-curseur'))?.valeur as string) ?? '1970-01-01T00:00:00Z';
	// pages successives d'une même requête (beaucoup de documents peuvent porter le même instant serveur) ;
	// le curseur n'avance qu'une fois tout reçu
	let dernier = curseur;
	for (let debut = 0; ; debut += 500) {
		const { data, error } = await supabase()
			.from('documents')
			.select('collection,id,contenu,modifie_le,efface,maj_serveur')
			.gt('maj_serveur', curseur)
			.order('maj_serveur', { ascending: true })
			.order('collection', { ascending: true })
			.order('id', { ascending: true })
			.range(debut, debut + 499);
		if (error) throw new Error(error.message);
		if (!data?.length) break;
		await appliquer(data as Distant[]);
		dernier = data[data.length - 1].maj_serveur as string;
		if (data.length < 500) break;
	}
	if (dernier !== curseur) await db.meta.put({ cle: 'sync-curseur', valeur: dernier });
}

interface Distant {
	collection: Collection;
	id: string;
	contenu: Ligne;
	modifie_le: string;
	efface: boolean;
}

async function appliquer(lignes: Distant[]) {
	appliquantDistant = true;
	try {
		for (const r of lignes) {
			if (!COLLECTIONS.includes(r.collection)) continue;
			const t = table(r.collection);
			// une écriture locale en attente plus récente l'emporte
			const attente = await db.sortie.get(`${r.collection}:${r.id}`);
			if (attente && !attente.efface && dateDe(r.collection, attente.contenu as Ligne) > r.modifie_le) continue;
			const naturelle = NATURELLES[r.collection];
			if (naturelle) {
				const locales = (await t.toArray()).filter((o) => naturelle(o) === r.id);
				if (r.efface) await t.bulkDelete(locales.map((o) => o.id as number));
				else if (!locales.length) await t.add(r.contenu);
				continue;
			}
			const local = await t.get(r.id);
			if (r.efface) {
				if (local) await t.delete(r.id);
			} else if (!local || dateDe(r.collection, local) <= r.modifie_le) {
				await t.put({ ...r.contenu, id: r.id });
			}
		}
	} finally {
		appliquantDistant = false;
	}
}
