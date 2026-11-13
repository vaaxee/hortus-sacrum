/// <reference types="@sveltejs/kit" />
/// <reference no-default-lib="true"/>
/// <reference lib="esnext" />
/// <reference lib="webworker" />
/**
 * Hors ligne : l'app, ses fichiers et les données (calendrier, livret) sont gardés sur l'appareil.
 * Les données de l'utilisateur sont déjà en local (IndexedDB) ; le serveur ne sert qu'à synchroniser.
 */
import { version } from '$app/env';
import { assets, immutable } from '$app/manifest';

const sw = self as unknown as ServiceWorkerGlobalScope;
const CACHE = `hortus-${version}`;
// les données d'essai et les modèles d'OCR (téléchargés à la demande) ne sont pas préchargés
// chemins relatifs à la racine du site (base vide)
const A_GARDER = [...immutable, ...assets].map((f) => '/' + String(f.path).replace(/^\//, '')).filter((f) => !f.includes('/essai/'));

sw.addEventListener('install', (e) => {
	e.waitUntil(caches.open(CACHE).then((c) => c.addAll(A_GARDER)).then(() => sw.skipWaiting()));
});

sw.addEventListener('activate', (e) => {
	e.waitUntil(
		caches.keys()
			.then((cles) => Promise.all(cles.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
			.then(() => sw.clients.claim())
	);
});

sw.addEventListener('fetch', (e) => {
	const req = e.request;
	if (req.method !== 'GET') return;
	const url = new URL(req.url);
	// le serveur de synchronisation n'est jamais mis en cache
	if (url.hostname.endsWith('supabase.co')) return;

	e.respondWith(
		(async () => {
			const cache = await caches.open(CACHE);
			// fichiers de l'app : d'abord le cache
			if (url.origin === sw.location.origin && A_GARDER.includes(url.pathname)) {
				const enCache = await cache.match(url.pathname);
				if (enCache) return enCache;
			}
			try {
				const rep = await fetch(req);
				// polices et pages : gardées pour la prochaine fois sans réseau
				if (rep.ok && (url.origin === sw.location.origin || url.hostname.includes('fonts.g'))) cache.put(req, rep.clone());
				return rep;
			} catch {
				const enCache = (await cache.match(req)) ?? (req.mode === 'navigate' ? await cache.match('/') : undefined);
				if (enCache) return enCache;
				throw new Error('hors ligne');
			}
		})()
	);
});
