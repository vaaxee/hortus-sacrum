// Éditeur de recueils (REFONTE § 6, lot 11) : ajout par copier-coller, découpage, affectation à un mois, puis
// méditation du jour ; correction d'une entrée d'un recueil livré, puis retour au texte livré.
import { expect, test } from '@playwright/test';

test('un recueil collé, découpé et affecté à décembre donne la méditation du 5 décembre', async ({ page }) => {
	const erreurs: string[] = [];
	page.on('pageerror', (e) => erreurs.push(e.message));
	await page.goto('/recueils/editer');
	await page.getByLabel('Titre', { exact: true }).fill('Mois de l’Avent (essai)');
	await page.getByLabel('Le recueil sert pour').selectOption('mois');
	await page.getByRole('combobox', { name: /^Mois/ }).selectOption('12');
	const texte = [1, 2, 3, 4, 5, 6].map((n) => `=== Jour ${n} de l’essai\nTexte du jour ${n}.`).join('\n\n');
	await page.getByLabel('Texte à découper').fill(texte);
	await page.getByRole('button', { name: 'Découper en entrées' }).click();
	await expect(page.getByText('Entrées (6)')).toBeVisible();
	await page.getByRole('button', { name: 'Enregistrer le recueil' }).click();
	await expect(page).toHaveURL(/\/recueils\?r=/);
	await expect(page.getByRole('link', { name: 'Jour 5 de l’essai' })).toBeVisible();

	await page.goto('/meditation?date=2026-12-05');
	await expect(page.getByRole('heading', { level: 1 })).toHaveText('Jour 5 de l’essai');
	await expect(page.getByText('Texte du jour 5.')).toBeVisible();

	await page.goto('/recueils');
	await expect(page.getByRole('link', { name: 'Mois de l’Avent (essai)' })).toBeVisible();
	expect(erreurs).toEqual([]);
});

test('corriger une entrée livrée, puis rétablir le texte livré', async ({ page }) => {
	await page.goto('/recueils?r=mois-purgatoire&n=0');
	const titre = page.getByRole('heading', { level: 1 });
	await expect(titre).not.toBeEmpty();
	const livre = await titre.textContent();
	await page.getByRole('button', { name: 'Corriger cette entrée' }).click();
	await page.getByLabel('Titre').fill(`${livre} (corrigé)`);
	await page.getByRole('button', { name: 'Enregistrer la correction' }).click();
	await expect(titre).toHaveText(`${livre} (corrigé)`);
	await expect(page.getByText('Corrigée par vous.')).toBeVisible();
	await page.getByRole('button', { name: 'Rétablir le texte livré' }).click();
	await expect(titre).toHaveText(livre!);
});
