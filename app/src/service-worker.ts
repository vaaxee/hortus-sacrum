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
// Données lues à la demande (recueils, jours du Bréviaire, polices) : un cache à part, gardé d'une version à
// l'autre. Sans lui, chaque mise à jour de l'app effaçait ce qui avait été lu, et l'appareil sans réseau (sans
// carte SIM, hors wifi) ne retrouvait plus ses méditations.
const DONNEES = 'hortus-donnees';
// La page unique de l'app (adapter-static, fallback index.html, servie à « / ») : toute navigation la reçoit, depuis le cache.
const PAGE = '/';
// les données d'essai et les modèles d'OCR (téléchargés à la demande) ne sont pas préchargés
// chemins relatifs à la racine du site (base vide)
// les recueils de méditations et de lectures (~20 Mo) et les jours du Bréviaire romain ne sont pas préchargés : chaque
// fichier est gardé dès sa première lecture (la page Office précharge la semaine qui vient)
const A_GARDER = [PAGE, ...[...immutable, ...assets].map((f) => '/' + String(f.path).replace(/^\//, ''))].filter(
	(f) => !f.includes('/essai/') && !f.startsWith('/data/recueils/') && !f.startsWith('/data/office/breviaire/')
);
// Ces mêmes fichiers (~26 Mo) sont téléchargés d'avance, en arrière-plan, quand la page le demande (au premier
// lancement avec réseau, puis à chaque ouverture : seuls les fichiers manquants sont pris) : sur un appareil sans
// carte SIM, l'app doit tout avoir avant de quitter le wifi.
const D_AVANCE = assets
	.map((f) => '/' + String(f.path).replace(/^\//, ''))
	.filter((f) => f.startsWith('/data/recueils/') || f.startsWith('/data/office/breviaire/'));
const A_LA_DEMANDE = (url: URL) =>
	(url.origin === sw.location.origin && url.pathname.startsWith('/data/')) || /^fonts\.g(oogleapis|static)\.com$/.test(url.hostname);

/** Le réseau, mais pas plus de `ms` : un réseau lent ou absent ne doit jamais bloquer la prière. */
function reseau(req: Request, ms: number): Promise<Response> {
	return new Promise((resoudre, rejeter) => {
		const minuterie = setTimeout(() => rejeter(new Error('réseau trop lent')), ms);
		fetch(req).then(
			(r) => (clearTimeout(minuterie), resoudre(r)),
			(e) => (clearTimeout(minuterie), rejeter(e))
		);
	});
}

async function toutGarder() {
	const donnees = await caches.open(DONNEES);
	for (const f of D_AVANCE) {
		if (await donnees.match(f)) continue;
		try {
			const rep = await fetch(f);
			if (rep.ok) await donnees.put(f, rep);
		} catch {
			return; // plus de réseau : on reprendra à la prochaine ouverture
		}
	}
}

sw.addEventListener('message', (e) => {
	if (e.data === 'tout-garder') e.waitUntil(toutGarder());
});

sw.addEventListener('install', (e) => {
	e.waitUntil(
		caches
			.open(CACHE)
			.then((c) => c.addAll(A_GARDER))
			.then(() => sw.skipWaiting())
	);
});

sw.addEventListener('activate', (e) => {
	e.waitUntil(
		caches
			.keys()
			.then((cles) => Promise.all(cles.filter((k) => k !== CACHE && k !== DONNEES).map((k) => caches.delete(k))))
			.then(() => sw.clients.claim())
	);
});

// rappels : notification envoyée par le serveur (fonction envoyer-rappels)
sw.addEventListener('push', (e) => {
	let m: { titre?: string; corps?: string; url?: string; tag?: string } = {};
	try {
		m = e.data?.json() ?? {};
	} catch {
		m = { titre: 'Hortus Sacrum', corps: e.data?.text() };
	}
	e.waitUntil(
		sw.registration.showNotification(m.titre ?? 'Hortus Sacrum', {
			body: m.corps ?? '',
			tag: m.tag,
			icon: '/icon-192.png',
			badge: '/icon-192.png',
			data: { url: m.url ?? '/' }
		})
	);
});

sw.addEventListener('notificationclick', (e) => {
	e.notification.close();
	const url = (e.notification.data?.url as string) ?? '/';
	e.waitUntil(
		(async () => {
			const fenetres = await sw.clients.matchAll({ type: 'window', includeUncontrolled: true });
			const f = fenetres[0] as WindowClient | undefined;
			if (f) {
				await f.focus();
				await f.navigate(url);
			} else await sw.clients.openWindow(url);
		})()
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
			// ouverture de l'app ou d'une de ses pages : la page unique de cette version, sans attendre le réseau
			if (req.mode === 'navigate' && url.origin === sw.location.origin) {
				const page = await cache.match(PAGE);
				if (page) return page;
			}
			// fichiers de l'app : d'abord le cache
			if (url.origin === sw.location.origin && A_GARDER.includes(url.pathname)) {
				const enCache = await cache.match(url.pathname);
				if (enCache) return enCache;
			}
			// données lues à la demande et polices : le cache s'il les a (rafraîchi en arrière-plan), sinon le réseau
			if (A_LA_DEMANDE(url)) {
				const donnees = await caches.open(DONNEES);
				const garde = await donnees.match(req);
				const frais = fetch(req).then((rep) => {
					// opaque : feuille de style des polices chargée sans CORS
					if (rep.ok || rep.type === 'opaque') donnees.put(req, rep.clone());
					return rep;
				});
				if (garde) {
					e.waitUntil(frais.catch(() => undefined));
					return garde;
				}
				return frais;
			}
			try {
				const rep = await reseau(req, 8000);
				if (rep.ok && url.origin === sw.location.origin) cache.put(req, rep.clone());
				return rep;
			} catch {
				const enCache = (await cache.match(req)) ?? (req.mode === 'navigate' ? await cache.match(PAGE) : undefined);
				if (enCache) return enCache;
				return Response.error();
			}
		})()
	);
});
