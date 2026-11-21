/**
 * Reproduction du bug « Internal Error » : passage de l'onglet Profil (/reglages) à l'Historique (/historique)
 * sur une base qui a des données (SPEC § 11). Une base neuve ne le montre pas, car rien n'y est coché.
 *
 * Lancer, après `npm run build` :   node tests/historique.e2e.mjs
 * (Playwright et Chromium doivent être installés ; le script lance lui-même `vite preview`.)
 * Sortie non nulle si l'Historique affiche une erreur ou si la page lève une exception.
 *
 * Cause principale constatée (19 nov. 2026) : les boucles `{#each … (r.titre)}` de l'Historique ont pour clé le titre.
 * Or plusieurs lignes portent le même titre (les sept « Litanies du jour », une par jour de la semaine ; les pratiques
 * du plan importées pour deux années liturgiques). Dès qu'il existe des coches sur plusieurs jours, deux lignes de même
 * titre ont des jours prévus, et Svelte lève `each_key_duplicate`, y compris en production.
 */
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const APP = fileURLToPath(new URL('..', import.meta.url));
const PORT = 4179;
const URL_APP = `http://localhost:${PORT}`;
const T = '2026-01-01T00:00:00.000Z';

/** Chaque scénario ajoute des données à une base fraîchement amorcée. `jours` : il y a n jours. */
const SCENARIOS = {
	'base neuve': { attendu: 'ok', ops: [] },
	'une coche aujourd’hui': { attendu: 'ok', ops: [{ op: 'cocher', jours: [0], id: 'liste:1' }] },
	'coches anciennes (plusieurs jours)': { attendu: 'ok', ops: [{ op: 'cocher', jours: [1, 2, 3, 8], id: 'liste:1' }] },
	'pratique sans règle': {
		attendu: 'ok',
		ops: [
			{ op: 'cocher', jours: [0], id: 'liste:1' },
			{ op: 'pratique', p: { id: 'test:sans-regle', titre: 'Pratique sans règle', type: 'neuvaine', active: true, textes: [] } }
		]
	},
	'élément sans jours ni rappels (ancienne version)': {
		attendu: 'ok',
		ops: [
			{ op: 'cocher', jours: [0], id: 'liste:1' },
			{
				op: 'element',
				e: { id: 'test:ancien', titre: 'Ancien élément', moment: 'matin', etiquette: 'ordinaire', ordre: 5, actif: true, textes: [] }
			}
		]
	}
};

async function fabriquer(page, ops) {
	await page.evaluate(
		async ({ ops, T }) => {
			const idb = await new Promise((ok, ko) => {
				const r = indexedDB.open('hebdomada');
				r.onsuccess = () => ok(r.result);
				r.onerror = () => ko(r.error);
			});
			const put = (store, v) =>
				new Promise((ok, ko) => {
					const t = idb.transaction(store, 'readwrite');
					t.objectStore(store).put(v);
					t.oncomplete = ok;
					t.onerror = () => ko(t.error);
				});
			const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
			for (const o of ops) {
				if (o.op === 'cocher')
					for (const n of o.jours) {
						const d = new Date(Date.now() - n * 86400000);
						await put('coches', { date: iso(d), elementId: o.id, rang: 0, horodatage: d.toISOString() });
					}
				if (o.op === 'pratique')
					await put('pratiques', { origine: 'personnel', promesses: '', indulgence: '', notes: '', creeLe: T, modifieLe: T, ...o.p });
				if (o.op === 'element') await put('liste', { origine: 'personnel', creeLe: T, modifieLe: T, ...o.e });
			}
			idb.close();
		},
		{ ops, T }
	);
}

async function attendreServeur() {
	for (let i = 0; i < 60; i++) {
		try {
			if ((await fetch(URL_APP)).ok) return;
		} catch {
			/* pas encore prêt */
		}
		await new Promise((r) => setTimeout(r, 500));
	}
	throw new Error('vite preview ne répond pas');
}

const serveur = spawn('npx', ['vite', 'preview', '--port', String(PORT), '--strictPort'], { cwd: APP, stdio: 'ignore' });
let echecs = 0;
try {
	await attendreServeur();
	const navigateur = await chromium.launch();
	for (const [nom, { ops }] of Object.entries(SCENARIOS)) {
		const ctx = await navigateur.newContext({
			viewport: { width: 390, height: 844 },
			deviceScaleFactor: 1,
			locale: 'fr-FR',
			timezoneId: 'Europe/Paris',
			serviceWorkers: 'block'
		});
		const page = await ctx.newPage();
		const erreurs = [];
		page.on('pageerror', (e) => erreurs.push(e.message.split('\n')[0]));
		page.on('console', (m) => m.type() === 'error' && erreurs.push(m.text().split('\n')[0]));
		await page.goto(URL_APP + '/');
		const entrer = page.getByText('Entrer au jardin');
		await page.waitForTimeout(800);
		if (await entrer.count()) await entrer.first().click();
		// amorçage : livret, sources, plan, roues
		await page.waitForFunction(
			() =>
				new Promise((ok) => {
					const r = indexedDB.open('hebdomada');
					r.onsuccess = () => {
						const q = r.result.transaction('meta').objectStore('meta').get('elements');
						q.onsuccess = () => ok(!!q.result);
						q.onerror = () => ok(false);
					};
					r.onerror = () => ok(false);
				}),
			null,
			{ timeout: 30000, polling: 500 }
		);
		await fabriquer(page, ops);
		await page.goto(URL_APP + '/profil');
		await page
			.getByRole('link', { name: /Historique/ })
			.first()
			.click();
		await page.waitForTimeout(2500);
		const texte = await page.evaluate(() => document.body.innerText);
		const ok = !/Internal Error/.test(texte) && /Historique/i.test(texte) && !erreurs.length;
		if (!ok) echecs++;
		console.log(`${ok ? 'ok   ' : 'ÉCHEC'} ${nom}${erreurs.length ? ` — ${erreurs.join(' ; ')}` : ''}`);
		await ctx.close();
	}
	await navigateur.close();
} finally {
	serveur.kill();
}
process.exit(echecs ? 1 : 0);
