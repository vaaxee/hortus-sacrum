// Bréviaire romain (REFONTE § 5, lot 9) : Lecture › Office › Bréviaire romain affiche l'office du jour, heure par heure.
import { expect, test } from '@playwright/test';

test('le 1er dimanche de l’Avent, les huit heures du Bréviaire romain', async ({ page }) => {
	const erreurs: string[] = [];
	page.on('pageerror', (e) => erreurs.push(e.message));
	await page.goto('/lecture/office?breviaire=romain&date=2026-11-29');
	// exact : à l'heure des Vêpres, la commémoraison du dimanche porte aussi ce nom
	await expect(page.getByText('Dominica I Adventus', { exact: true })).toBeVisible();
	for (const h of ['Matines', 'Laudes', 'Prime', 'Tierce', 'Sexte', 'None', 'Vêpres', 'Complies'])
		await expect(page.getByRole('tab', { name: h, exact: true })).toBeVisible();
	await page.getByRole('tab', { name: 'Laudes', exact: true }).first().click();
	await expect(page.getByText('Excita, quǽsumus, Dómine, poténtiam tuam', { exact: false }).first()).toBeVisible();
	expect(erreurs).toEqual([]);
});

test('hors de l’année calculée, un message et le renvoi vers les leçons du jour', async ({ page }) => {
	await page.goto('/lecture/office?breviaire=romain&date=2030-01-01');
	await expect(page.getByText('n’est calculé que pour l’année liturgique 2026-2027')).toBeVisible();
});

test('les psaumes du Bréviaire romain en français de Fillion, en regard du latin', async ({ page }) => {
	const erreurs: string[] = [];
	page.on('pageerror', (e) => erreurs.push(e.message));
	await page.goto('/lecture/office?breviaire=romain&date=2026-11-29');
	await page.getByRole('tab', { name: 'Laudes', exact: true }).first().click();
	// Ps 92, 1 : le latin d'abord, le français de Fillion en face (data/office/breviaire-fr/psautier-fillion.json)
	const strophe = page.locator('.strophe', { hasText: 'Dóminus regnávit' }).first();
	await expect(strophe.locator('[lang="la"]')).toContainText('Dóminus regnávit');
	await expect(strophe.locator('[lang="fr"]')).toHaveText(
		"Le Seigneur a régné, et s'est revêtu de gloire : le Seigneur s'est revêtu et s'est ceint de force."
	);
	await expect(page.getByText('Le nouveau psautier du Bréviaire romain')).toBeVisible();
	// latin seul sur demande
	await page.getByRole('button', { name: 'Latin seul' }).click();
	await expect(page.locator('.strophe')).toHaveCount(0);
	await expect(page.getByText('Dóminus regnávit', { exact: false }).first()).toBeVisible();
	await page.getByRole('button', { name: 'Psaumes en français' }).click();
	await expect(page.locator('.strophe').first()).toBeVisible();
	expect(erreurs).toEqual([]);
});
