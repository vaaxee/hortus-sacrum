// Prière du matin et du soir en parties titrées et repliables (demande du 22 nov.) : on peut s'arrêter et reprendre ;
// les actes des devoirs de charité sont repliés à l'ouverture.
import { expect, test } from '@playwright/test';

test('la prière du matin se lit par parties, les devoirs de charité repliés', async ({ page }) => {
	const erreurs: string[] = [];
	page.on('pageerror', (e) => erreurs.push(e.message));
	await page.goto('/pratique/' + encodeURIComponent('prog:priere-du-matin') + '?date=2026-11-23');
	const partie = (nom: string) => page.locator('details.partie').filter({ has: page.getByRole('heading', { name: nom, exact: true }) });
	await expect(partie('Prière du matin')).toHaveAttribute('open', '');
	await expect(partie('Offrande de la journée')).toHaveAttribute('open', '');
	const devoirs = partie('Actes des devoirs de charité');
	await expect(devoirs).not.toHaveAttribute('open', '');
	await devoirs.locator('> summary').click();
	await expect(devoirs).toHaveAttribute('open', '');
	await partie('Prière du matin').locator('> summary').click();
	await expect(partie('Prière du matin')).not.toHaveAttribute('open', '');
	expect(erreurs).toEqual([]);
});

test('la prière du soir se lit par parties', async ({ page }) => {
	await page.goto('/pratique/' + encodeURIComponent('prog:priere-du-soir') + '?date=2026-11-23');
	for (const nom of ['Don du Saint-Esprit du jour', 'Prière du soir', 'Recommandations du soir'])
		await expect(page.getByRole('heading', { name: nom, exact: true })).toBeVisible();
});

// Décisions du 26 nov. (docs/audits/PRIERES_OBLIGATOIRES_2026-11-26.md) : textes indulgenciés ou prescrits à la place
// des textes sans titre, trois Ave de saint Alphonse le soir, ouverture du chapelet aux intentions du Souverain Pontife.
test('prières obligatoires : remplaçants du matin, trois Ave du soir, intentions du Pape au chapelet', async ({ page }) => {
	const erreurs: string[] = [];
	page.on('pageerror', (e) => erreurs.push(e.message));
	await page.goto('/pratique/' + encodeURIComponent('prog:priere-du-matin') + '?date=2026-11-23');
	await expect(page.getByText('qui nous avez fait parvenir au commencement de ce jour').first()).toBeVisible();
	await expect(page.getByText('Recevez, Seigneur, toute ma liberté').first()).toBeVisible();
	await expect(page.getByText('Entre vos mains, Seigneur, et entre les mains de vos Anges').first()).toBeVisible();
	await expect(page.getByText('je vous remercie très humblement')).toHaveCount(0);
	await page.goto('/pratique/' + encodeURIComponent('prog:priere-du-soir') + '?date=2026-11-23');
	await expect(page.getByText('Par votre Immaculée Conception, ô Marie').first()).toBeVisible();
	await page.goto('/pratique/' + encodeURIComponent('prog:chapelet') + '?date=2026-11-23');
	await expect(page.getByText('se disent aux intentions du Souverain Pontife').first()).toBeVisible();
	expect(erreurs).toEqual([]);
});
