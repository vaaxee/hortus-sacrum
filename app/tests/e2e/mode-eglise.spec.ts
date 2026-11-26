// Mode église (décision du 22 nov.) : sur une pratique et sur l'office, un bouton pose <html data-eglise> (grand corps
// de lecture, barre d'onglets masquée) et garde l'écran allumé (Screen Wake Lock) ; le choix est gardé sur l'appareil.
// Ne vérifie aucun texte religieux.
import { expect, test, type Page } from '@playwright/test';

const PRATIQUE = '/pratique/' + encodeURIComponent('prog:priere-du-soir') + '?date=2026-11-23';

function surveiller(page: Page) {
	const erreurs: string[] = [];
	page.on('pageerror', (e) => erreurs.push(`exception : ${e.message}`));
	page.on('console', (m) => {
		if (m.type() === 'error') erreurs.push(`console : ${m.text()}`);
	});
	return erreurs;
}

/** Remplace l'API Screen Wake Lock par un double qui compte les demandes et les relâches. */
async function faussesVeilles(page: Page) {
	await page.addInitScript(() => {
		const w = window as unknown as { verrous: { demandes: number; actifs: number } };
		w.verrous = { demandes: 0, actifs: 0 };
		Object.defineProperty(navigator, 'wakeLock', {
			configurable: true,
			value: {
				request: async () => {
					w.verrous.demandes++;
					w.verrous.actifs++;
					let libre = false;
					return {
						get released() {
							return libre;
						},
						release: async () => {
							if (!libre) w.verrous.actifs--;
							libre = true;
						}
					};
				}
			}
		});
	});
}
const verrous = (page: Page) => page.evaluate(() => (window as unknown as { verrous: { demandes: number; actifs: number } }).verrous);

test('le mode église grossit le texte, masque les onglets, tient l’écran allumé et se garde', async ({ page }, info) => {
	const erreurs = surveiller(page);
	await faussesVeilles(page);
	await page.goto(PRATIQUE);
	const bouton = page.getByRole('button', { name: 'Mode église' });
	await expect(bouton).toHaveAttribute('aria-pressed', 'false');
	const box = await bouton.boundingBox();
	// 44 px CSS ; arrondi : la mesure peut tomber à 43,999996 selon la position de la page (sous-pixel)
	expect(Math.round(box!.width)).toBeGreaterThanOrEqual(44);
	expect(Math.round(box!.height)).toBeGreaterThanOrEqual(44);

	const lecture = page.locator('main .lecture').first();
	const taille = () => lecture.evaluate((e) => parseFloat(getComputedStyle(e).fontSize));
	const avant = await taille();
	if (info.project.name === 'telephone') await expect(page.locator('nav.onglets')).toBeVisible();

	await bouton.click();
	await expect(bouton).toHaveAttribute('aria-pressed', 'true');
	await expect(page.locator('html')).toHaveAttribute('data-eglise', '');
	await expect(page.locator('nav.onglets')).toBeHidden();
	expect(await taille()).toBeCloseTo(avant * 1.3, 0);
	await expect.poll(() => verrous(page)).toEqual({ demandes: 1, actifs: 1 });

	// gardé après rechargement
	await page.reload();
	await expect(page.getByRole('button', { name: 'Mode église' })).toHaveAttribute('aria-pressed', 'true');
	await expect(page.locator('html')).toHaveAttribute('data-eglise', '');
	await expect(page.locator('nav.onglets')).toBeHidden();
	await expect.poll(() => verrous(page)).toMatchObject({ actifs: 1 });

	if (info.project.name === 'telephone') {
		const deborde = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
		expect(deborde, 'défilement horizontal sur téléphone').toBe(false);
	}

	// coupé : tout revient, le verrou est relâché
	await page.getByRole('button', { name: 'Mode église' }).click();
	await expect(page.getByRole('button', { name: 'Mode église' })).toHaveAttribute('aria-pressed', 'false');
	await expect(page.locator('html')).not.toHaveAttribute('data-eglise');
	await expect.poll(() => verrous(page)).toMatchObject({ actifs: 0 });
	expect(await taille()).toBeCloseTo(avant, 0);
	if (info.project.name === 'telephone') await expect(page.locator('nav.onglets')).toBeVisible();
	await page.reload();
	await expect(page.getByRole('button', { name: 'Mode église' })).toHaveAttribute('aria-pressed', 'false');
	expect(erreurs, erreurs.join('\n')).toEqual([]);
});

test('le mode église suit sur l’office et ne s’applique pas hors des pages de prière', async ({ page }) => {
	const erreurs = surveiller(page);
	await page.goto(PRATIQUE);
	await page.getByRole('button', { name: 'Mode église' }).click();
	await expect(page.locator('html')).toHaveAttribute('data-eglise', '');

	await page.goto('/lecture/office');
	await expect(page.getByRole('button', { name: 'Mode église' })).toHaveAttribute('aria-pressed', 'true');
	await expect(page.locator('html')).toHaveAttribute('data-eglise', '');

	// le retour à la liste du jour quitte la page : la barre d'onglets revient, le choix reste gardé
	await page.getByRole('link', { name: 'Lecture' }).first().click();
	await expect(page).toHaveURL(/\/lecture$/);
	await expect(page.locator('html')).not.toHaveAttribute('data-eglise');
	expect(await page.evaluate(() => localStorage.getItem('hs-eglise'))).toBe('oui');
	expect(erreurs, erreurs.join('\n')).toEqual([]);
});

test('sans l’API Screen Wake Lock, le mode marche sans erreur', async ({ page }) => {
	const erreurs = surveiller(page);
	await page.addInitScript(() => {
		delete (Navigator.prototype as unknown as { wakeLock?: unknown }).wakeLock;
	});
	await page.goto(PRATIQUE);
	await page.getByRole('button', { name: 'Mode église' }).click();
	await expect(page.locator('html')).toHaveAttribute('data-eglise', '');
	await page.getByRole('button', { name: 'Mode église' }).click();
	await expect(page.locator('html')).not.toHaveAttribute('data-eglise');
	expect(erreurs, erreurs.join('\n')).toEqual([]);
});
