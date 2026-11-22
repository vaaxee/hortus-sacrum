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
