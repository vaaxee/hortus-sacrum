// Sans réseau (téléphone sans carte SIM, hors wifi) : une fois l'app ouverte une première fois, elle s'ouvre et
// se lit entièrement depuis l'appareil. Ne vérifie aucun texte religieux : seulement que l'app tient debout.
import { expect, test, type Page } from '@playwright/test';

/** Attend que le service worker contrôle la page et ait gardé la page unique de l'app. */
async function attendreLeCache(page: Page) {
	await page.evaluate(async () => {
		await navigator.serviceWorker.ready;
		if (!navigator.serviceWorker.controller)
			await new Promise((r) => navigator.serviceWorker.addEventListener('controllerchange', r, { once: true }));
	});
	await expect
		.poll(
			() =>
				page.evaluate(async () => {
					for (const nom of await caches.keys()) if (await (await caches.open(nom)).match('/')) return true;
					return false;
				}),
			{ timeout: 60_000 }
		)
		.toBe(true);
}

test('sans réseau, l’app s’ouvre et chaque onglet se lit', async ({ page, context }) => {
	test.setTimeout(120_000);
	await page.goto('/');
	await expect(page.getByRole('link', { name: 'Prières' }).first()).toBeVisible();
	await attendreLeCache(page);
	// recueils et jours du Bréviaire téléchargés d'avance (34 + 365 fichiers en 2026-2027)
	await expect
		.poll(() => page.evaluate(async () => (await (await caches.open('hortus-donnees')).keys()).length), { timeout: 90_000 })
		.toBeGreaterThan(390);

	await context.setOffline(true);
	for (const chemin of ['/', '/prieres', '/devotions', '/calendrier', '/lecture']) {
		await page.goto(chemin);
		await expect(page.getByRole('link', { name: 'Prières' }).first()).toBeVisible();
		await expect(page.locator('body')).not.toContainText('n’ont pas pu être chargées');
		expect(new URL(page.url()).pathname).toBe(chemin);
	}
	await context.setOffline(false);
});
