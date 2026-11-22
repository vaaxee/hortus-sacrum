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
