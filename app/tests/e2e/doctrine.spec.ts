// Doctrine (lot 10) : la Somme s'ouvre sur l'article du jour, le latin se montre en regard, « J'ai lu cet article »
// avance le marque-page et coche la lecture. Ne vérifie aucun texte religieux mot pour mot (test des données à part).
import { expect, test } from '@playwright/test';

test('Somme théologique : article du jour, latin, marque-page', async ({ page }, info) => {
	const erreurs: string[] = [];
	page.on('pageerror', (e) => erreurs.push(`exception : ${e.message}`));
	page.on('console', (m) => {
		if (m.type() === 'error') erreurs.push(`console : ${m.text()}`);
	});
	await page.goto('/lecture/doctrine?date=2026-11-22');
	await expect(page.locator('.date')).toContainText('Iª q. 1 a. 1');
	await expect(page.getByRole('heading', { name: 'Article I' })).toBeVisible();
	await expect(page.locator('[lang="la"]')).toHaveCount(0);
	await page.getByRole('button', { name: 'Latin' }).click();
	await expect(page.locator('[lang="la"]').first()).toBeVisible();
	await page.getByRole('button', { name: 'J’ai lu cet article' }).click();
	await expect(page.getByText('Article lu aujourd’hui')).toBeVisible();
	// le lendemain, l'article suivant
	await page.goto('/lecture/doctrine?date=2026-11-23');
	await expect(page.locator('.date')).toContainText('Iª q. 1 a. 2');
	// Lecture : la ligne de la Somme mène à la page
	await page.goto('/lecture?date=2026-11-23');
	await expect(page.getByRole('link', { name: /Somme théologique/ })).toContainText('Iª q. 1 a. 2');
	if (info.project.name === 'telephone') {
		await page.goto('/lecture/doctrine?date=2026-11-23');
		const deborde = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
		expect(deborde, 'défilement horizontal sur téléphone').toBe(false);
	}
	expect(erreurs, erreurs.join('\n')).toEqual([]);
});
