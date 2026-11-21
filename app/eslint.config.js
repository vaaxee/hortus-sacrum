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
			// toute boucle a sa clé (une clé en double fait planter Svelte : clé d'identifiant seulement quand elle est unique)
			'svelte/require-each-key': 'error',
			// les Map, Set et Date signalés sont des valeurs locales, construites dans un $derived ou une fonction et rendues
			// sans être modifiées ensuite : des versions réactives (SvelteMap…) n'y apporteraient rien
			'svelte/prefer-svelte-reactivity': 'off',
			// le balisage des prières est produit par markup.ts à partir de textes sourcés, jamais d'une saisie extérieure
			'svelte/no-at-html-tags': 'off'
		}
	},
	{ ignores: ['build/', '.svelte-kit/', 'static/', 'node_modules/'] }
);
