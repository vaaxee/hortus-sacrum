import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [
		sveltekit({
			// App entièrement statique (PWA) : les données vivent dans le navigateur.
			adapter: adapter({ fallback: 'index.html' })
		})
	],
	test: { include: ['src/**/*.test.ts'] }
});
