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
// les recueils de méditations et de lectures (~20 Mo) ne sont pas préchargés : chaque fichier est gardé dès sa première lecture
const A_GARDER = [...immutable, ...assets]
	.map((f) => '/' + String(f.path).replace(/^\//, ''))
	.filter((f) => !f.includes('/essai/') && !f.startsWith('/data/recueils/'));

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

// rappels : notification envoyée par le serveur (fonction envoyer-rappels)
sw.addEventListener('push', (e) => {
	let m: { titre?: string; corps?: string; url?: string; tag?: string } = {};
	try { m = e.data?.json() ?? {}; } catch { m = { titre: 'Hortus Sacrum', corps: e.data?.text() }; }
	e.waitUntil(sw.registration.showNotification(m.titre ?? 'Hortus Sacrum', {
		body: m.corps ?? '', tag: m.tag, icon: '/icon-192.png', badge: '/icon-192.png', data: { url: m.url ?? '/' }
	}));
});

sw.addEventListener('notificationclick', (e) => {
	e.notification.close();
	const url = (e.notification.data?.url as string) ?? '/';
	e.waitUntil((async () => {
		const fenetres = await sw.clients.matchAll({ type: 'window', includeUncontrolled: true });
		const f = fenetres[0] as WindowClient | undefined;
		if (f) { await f.focus(); await f.navigate(url); } else await sw.clients.openWindow(url);
	})());
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
