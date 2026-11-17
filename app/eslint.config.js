// Lint de l'app (plan général : rôle « Qualité »). Lancer : npm run lint
import js from '@eslint/js';
import prettier from 'eslint-config-prettier';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import ts from 'typescript-eslint';

export default ts.config(
	js.configs.recommended,
	...ts.configs.recommended,
	...svelte.configs['flat/recommended'],
	prettier,
	...svelte.configs['flat/prettier'],
	{ languageOptions: { globals: { ...globals.browser, ...globals.node } } },
	{ files: ['**/*.svelte', '**/*.svelte.ts'], languageOptions: { parserOptions: { parser: ts.parser } } },
	{
		rules: {
			'@typescript-eslint/no-unused-vars': [
				'error',
				{ argsIgnorePattern: '^_', varsIgnorePattern: '^_', destructuredArrayIgnorePattern: '^_', ignoreRestSiblings: true }
			],
			// app statique, sans chemin de base : les liens simples suffisent
			'svelte/no-navigation-without-resolve': 'off',
			// à reprendre peu à peu (rôle « Qualité ») : clés des boucles, Date/Map réactives
			'svelte/require-each-key': 'warn',
			'svelte/prefer-svelte-reactivity': 'warn',
			// le balisage des prières est produit par markup.ts à partir de textes sourcés, jamais d'une saisie extérieure
			'svelte/no-at-html-tags': 'off'
		}
	},
	{ ignores: ['build/', '.svelte-kit/', 'static/', 'node_modules/'] }
);
