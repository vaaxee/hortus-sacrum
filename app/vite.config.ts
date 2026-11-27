import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [
		sveltekit({
			// App entièrement statique (PWA) : les données vivent dans le navigateur.
			adapter: adapter({ fallback: 'index.html' }),
			// chemins absolus (/_app/…) : la page unique gardée hors ligne par le service worker sert toutes les adresses,
			// /lecture/doctrine comme /, et ne doit pas chercher ses fichiers dans /lecture/_app/
			paths: { relative: false }
		})
	],
	test: { include: ['src/**/*.test.ts'] }
});
