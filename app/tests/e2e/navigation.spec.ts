// Fumée de navigation : chaque onglet et le Profil s'ouvrent sans erreur de page ni erreur console,
// et, sur téléphone, sans défilement horizontal. Ne vérifie aucun texte religieux : seulement que l'app tient debout.
import { expect, test, type Page } from '@playwright/test';

const PAGES = [
	{ nom: 'Aujourd’hui', chemin: '/' },
	{ nom: 'Lecture', chemin: '/lecture' },
	{ nom: 'Prières', chemin: '/prieres' },
	{ nom: 'Dévotions', chemin: '/devotions' },
	{ nom: 'Calendrier', chemin: '/calendrier' },
	{ nom: 'Profil', chemin: '/profil' },
	{ nom: 'Historique', chemin: '/historique' },
	{ nom: 'Programme', chemin: '/programme' }
];

function surveiller(page: Page) {
	const erreurs: string[] = [];
	page.on('pageerror', (e) => erreurs.push(`exception : ${e.message}`));
	page.on('console', (m) => {
		if (m.type() === 'error') erreurs.push(`console : ${m.text()}`);
	});
	return erreurs;
}

for (const { nom, chemin } of PAGES) {
	test(`${nom} (${chemin}) s'ouvre sans erreur`, async ({ page }, info) => {
		const erreurs = surveiller(page);
		await page.goto(chemin);
		await page.waitForLoadState('networkidle');
		await expect(page.locator('body')).not.toContainText('Internal Error');
		expect(erreurs, erreurs.join('\n')).toEqual([]);
		if (info.project.name === 'telephone') {
			const deborde = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
			expect(deborde, 'défilement horizontal sur téléphone').toBe(false);
		}
	});
}

test('les onglets mènent à leur page', async ({ page }) => {
	await page.goto('/');
	await page.waitForLoadState('networkidle');
	// l'écran d'accueil masque la barre d'onglets jusqu'à « Entrer au jardin »
	await page.getByRole('button', { name: 'Entrer au jardin' }).click();
	for (const { nom, chemin } of PAGES.slice(1, 5)) {
		await page.getByRole('link', { name: nom, exact: true }).first().click();
		await expect(page).toHaveURL(new RegExp(`${chemin}$`));
	}
});
