<script lang="ts">
	import '#lib/design/tokens.css';
	import '../app.css';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { direction, initialiserApparence } from '#lib/apparence.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { amorcer } from '#lib/seed.ts';

	let { children } = $props();
	let pret = $state(false);
	let erreur = $state('');

	onMount(async () => {
		initialiserApparence();
		try {
			await amorcer();
		} catch (e) {
			erreur = 'Les prières du livret n’ont pas pu être chargées. Rechargez la page.';
			console.error(e);
		}
		pret = true;
	});

	const onglets = [
		{ icone: 'aujourdhui', nom: 'Aujourd’hui', href: '/' },
		{ icone: 'calendrier', nom: 'Calendrier', href: '/calendrier' },
		{ icone: 'prieres', nom: 'Prières', href: '/prieres' },
		{ icone: 'devotions', nom: 'Dévotions', href: '/devotions' },
		{ icone: 'profil', nom: 'Profil', href: '/reglages' }
	] as const;
	const actif = (href: string) => (href === '/' ? page.url.pathname === '/' : page.url.pathname.startsWith(href));
</script>

<div class="hs">
	{#if $direction === 'grecque'}<Ornement nom="mosaique" />{/if}

	<div class="cadre">
		<nav class="sommaire" aria-label="Navigation principale">
			<a class="marque" href="/"><Ornement nom="chrisme" taille={22} /><span>Hortus Sacrum</span></a>
			{#each onglets as o}
				<a href={o.href} class:actif={actif(o.href)} aria-current={actif(o.href) ? 'page' : undefined}>
					<Icone nom={o.icone} taille={20} /><span>{o.nom}</span>
				</a>
			{/each}
		</nav>
		<div class="contenu">
			{#if erreur}<p class="page erreur" role="alert">{erreur}</p>{/if}
			{#if pret}{@render children()}{/if}
		</div>
	</div>

	<nav class="onglets" aria-label="Navigation principale">
		{#each onglets as o}
			<a href={o.href} class:actif={actif(o.href)} aria-current={actif(o.href) ? 'page' : undefined}>
				<span class="palme">{#if actif(o.href)}<Ornement nom="palmette" taille={14} />{/if}</span>
				<Icone nom={o.icone} taille={22} />
				<span class="nom">{o.nom}</span>
			</a>
		{/each}
	</nav>
</div>

<style>
	.cadre { max-width: var(--hs-page); margin: 0 auto; }
	.contenu { padding-bottom: 104px; min-width: 0; }
	.sommaire { display: none; }

	/* téléphone : barre d'onglets, icônes au trait, palmette d'or sur l'onglet actif */
	.onglets {
		position: fixed; inset: auto 0 0 0; z-index: 5; display: flex; justify-content: space-around;
		background: var(--hs-fond); border-top: var(--hs-cheveu) solid var(--hs-filet);
		padding: 2px 4px calc(6px + env(safe-area-inset-bottom));
	}
	.onglets a {
		flex: 1; display: grid; justify-items: center; gap: 1px; padding: 2px 0 4px; text-decoration: none;
		color: var(--hs-encre-douce); min-width: 0;
	}
	.onglets a.actif { color: var(--hs-lapis); }
	.palme { height: 14px; color: var(--hs-or); display: block; line-height: 0; }
	.onglets .nom {
		font-family: var(--hs-lecture); font-variant-caps: all-small-caps; letter-spacing: var(--hs-chasse-petites-cap);
		font-size: 0.8125rem; line-height: 1.1; white-space: nowrap;
	}

	/* ordinateur : colonne de gauche, comme la table d'un beau livre */
	@media (min-width: 900px) {
		.onglets { display: none; }
		.cadre { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 24px; padding: 0 24px; }
		.contenu { padding-bottom: var(--hs-e9); }
		.sommaire {
			display: flex; flex-direction: column; gap: 2px; position: sticky; top: 0; align-self: start;
			padding: var(--hs-e7) 0 var(--hs-e6); border-right: var(--hs-cheveu) solid var(--hs-filet); min-height: 100dvh;
		}
		.sommaire a {
			display: flex; align-items: center; gap: 12px; padding: 9px 16px 9px 14px; text-decoration: none;
			color: var(--hs-encre-douce); border-left: 2px solid transparent;
			font-family: var(--hs-lecture); font-variant-caps: all-small-caps; letter-spacing: var(--hs-chasse-petites-cap); font-size: 1.0625rem;
		}
		.sommaire a.actif { color: var(--hs-lapis); border-left-color: var(--hs-or); }
		.sommaire .marque {
			color: var(--hs-encre); font-family: var(--hs-accent); font-variant-caps: normal; letter-spacing: 0.02em;
			font-size: 1.25rem; margin-bottom: var(--hs-e6); border-left-color: transparent;
		}
		.sommaire .marque :global(svg) { color: var(--hs-rubrique); }
	}
</style>
