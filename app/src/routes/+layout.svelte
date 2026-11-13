<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { amorcer } from '#lib/seed.ts';

	let { children } = $props();
	let pret = $state(false);
	let erreur = $state('');

	onMount(async () => {
		try {
			await amorcer();
		} catch (e) {
			erreur = 'Les données de départ n’ont pas pu être chargées.';
			console.error(e);
		}
		pret = true;
	});

	const onglets = [
		{ href: '/', nom: 'Aujourd’hui' },
		{ href: '/prieres', nom: 'Prières' },
		{ href: '/reglages', nom: 'Réglages' }
	];
	const actif = (href: string) =>
		href === '/' ? page.url.pathname === '/' : page.url.pathname.startsWith(href);
</script>

{#if erreur}<p class="page petit" role="alert">{erreur}</p>{/if}
{#if pret}{@render children()}{/if}

{#if !page.url.pathname.startsWith('/maquette')}
<nav aria-label="Navigation principale">
	{#each onglets as o}
		<a href={o.href} aria-current={actif(o.href) ? 'page' : undefined}>{o.nom}</a>
	{/each}
</nav>
{/if}

<style>
	nav {
		position: fixed; inset: auto 0 0 0;
		display: flex; justify-content: center; gap: 0.25rem;
		padding: 0.4rem 0.5rem calc(0.4rem + env(safe-area-inset-bottom));
		background: color-mix(in srgb, var(--papier) 92%, transparent);
		backdrop-filter: blur(8px);
		border-top: 1px solid var(--filet);
	}
	nav a {
		flex: 1; max-width: 11rem; text-align: center; text-decoration: none;
		padding: 0.5rem 0.25rem; border-radius: 0.5rem;
		font-variant: small-caps; letter-spacing: 0.05em; color: var(--encre-douce);
	}
	nav a[aria-current='page'] { color: var(--rubrique); background: var(--carte); }
</style>
