// Tests de bout en bout (plan général : rôle « Qualité »). Lancer, après `npm run build` : npm run test:e2e
// Trois projets : bureau en clair, bureau en sombre (prefers-color-scheme), téléphone.
// Le navigateur est le Chromium installé avec Playwright ; la version de @playwright/test est fixée pour lui répondre.
import { defineConfig, devices } from '@playwright/test';

const PORT = 4180;

export default defineConfig({
	testDir: 'tests/e2e',
	fullyParallel: true,
	forbidOnly: !!process.env.CI,
	retries: 0,
	reporter: [['list']],
	use: {
		baseURL: `http://localhost:${PORT}`,
		locale: 'fr-FR',
		timezoneId: 'Europe/Paris',
		trace: 'off'
	},
	projects: [
		{ name: 'bureau-clair', use: { ...devices['Desktop Chrome'], colorScheme: 'light' } },
		{ name: 'bureau-sombre', use: { ...devices['Desktop Chrome'], colorScheme: 'dark' } },
		{ name: 'telephone', use: { ...devices['Pixel 7'] } }
	],
	webServer: {
		command: `npx vite preview --port ${PORT} --strictPort`,
		port: PORT,
		reuseExistingServer: !process.env.CI,
		timeout: 60_000
	}
});
