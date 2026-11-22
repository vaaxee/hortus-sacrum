// Décisions du 22 nov. : « Fait » en bas d'une pratique ramène à la liste, à cette ligne ; la couleur de l'app suit la
// direction et le thème choisis.
import { expect, test } from '@playwright/test';

test('« Fait » ramène à la liste du jour, à la ligne cochée', async ({ page }) => {
	await page.goto('/pratique/' + encodeURIComponent('prog:priere-du-soir') + '?date=2026-11-23');
	await page.getByRole('checkbox', { name: /Prière du soir.*: fait/ }).click();
	await expect(page).toHaveURL(/\/\?date=2026-11-23#ligne-prog:priere-du-soir$/);
	const ligne = page.locator('[id="ligne-prog:priere-du-soir"]');
	await expect(ligne).toBeInViewport();
	await expect(ligne).toHaveClass(/fini/);
});

test('la couleur de l’app suit la direction choisie', async ({ page }) => {
	await page.goto('/');
	const couleur = () => page.locator('meta[name="theme-color"]').first().getAttribute('content');
	await expect(page.locator('meta[name="theme-color"]')).toHaveCount(1);
	const avant = await couleur();
	await page.evaluate(() => localStorage.setItem('hs-da', 'grecque'));
	await page.reload();
	await expect.poll(couleur).not.toBe(avant);
});
