<script lang="ts">
	import '#lib/design/tokens.css';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';

	let { children } = $props();
	let theme: 'auto' | 'jour' | 'nuit' = $state('auto');
	let da: 'latine' | 'grecque' = $state('latine');

	onMount(() => {
		theme = (localStorage.getItem('hs-theme') as typeof theme) ?? 'auto';
		da = (localStorage.getItem('hs-da') as typeof da) ?? 'latine';
		appliquer();
		// le fond du document suit l'univers, pour les bords d'écran
		document.body.style.background = 'var(--hs-fond)';
		return () => {
			document.body.style.background = '';
			delete document.documentElement.dataset.theme;
			delete document.documentElement.dataset.da;
		};
	});
	function appliquer() {
		if (theme === 'auto') delete document.documentElement.dataset.theme;
		else document.documentElement.dataset.theme = theme;
		if (da === 'grecque') document.documentElement.dataset.da = 'grecque';
		else delete document.documentElement.dataset.da;
	}
	function choisirDa(d: typeof da) {
		da = d;
		localStorage.setItem('hs-da', d);
		appliquer();
	}
	function choisir(t: typeof theme) {
		theme = t;
		localStorage.setItem('hs-theme', t);
		appliquer();
	}

	const ecrans = [
		{ href: '/maquette', nom: 'Aujourd’hui' },
		{ href: '/maquette/priere', nom: 'Prière' },
		{ href: '/maquette/mois', nom: 'Ouverture du mois' }
	];
	const onglets = [
		{ icone: 'aujourdhui', nom: 'Aujourd’hui', href: '/maquette' },
		{ icone: 'calendrier', nom: 'Calendrier', href: '/maquette/mois' },
		{ icone: 'prieres', nom: 'Prières', href: '/maquette/priere' },
		{ icone: 'devotions', nom: 'Dévotions', href: '/maquette' },
		{ icone: 'profil', nom: 'Profil', href: '/maquette' }
	] as const;
	const chemin = $derived(page.url.pathname.replace(/\/$/, ''));
	const ongletActif = $derived(chemin === '/maquette/priere' ? 2 : chemin === '/maquette/mois' ? 1 : 0);
</script>

<div class="hs">
	<!-- barre de maquette : hors de l'identité, sert seulement à passer d'un écran et d'un thème à l'autre -->
	<div class="maquette interface" role="navigation" aria-label="Maquette">
		<span class="univers">Maquette</span>
		<span class="liens">
			{#each ecrans as e}
				<a href={e.href} aria-current={chemin === e.href ? 'page' : undefined}>{e.nom}</a>
			{/each}
		</span>
		<span class="themes" role="group" aria-label="Direction artistique">
			<button class:actif={da === 'latine'} onclick={() => choisirDa('latine')}>Latine</button>
			<button class:actif={da === 'grecque'} onclick={() => choisirDa('grecque')}>Grecque</button>
		</span>
		<span class="themes" role="group" aria-label="Thème">
			<button class:actif={theme === 'jour'} onclick={() => choisir('jour')}><Icone nom="jour" taille={16} /> Jour</button>
			<button class:actif={theme === 'nuit'} onclick={() => choisir('nuit')}><Icone nom="nuit" taille={16} /> Nuit</button>
			<button class:actif={theme === 'auto'} onclick={() => choisir('auto')}>Auto</button>
		</span>
	</div>

	{#if da === 'grecque'}<Ornement nom="mosaique" />{/if}
	<div class="cadre">
		<nav class="sommaire" aria-label="Navigation principale">
			<a class="marque" href="/maquette"><Ornement nom="chrisme" taille={22} /><span>Hortus Sacrum</span></a>
			{#each onglets as o, i}
				<a href={o.href} class:actif={i === ongletActif} aria-current={i === ongletActif ? 'page' : undefined}>
					<Icone nom={o.icone} taille={20} /><span>{o.nom}</span>
				</a>
			{/each}
		</nav>
		<div class="contenu">{@render children()}</div>
	</div>

	<nav class="onglets" aria-label="Navigation principale">
		{#each onglets as o, i}
			<a href={o.href} class:actif={i === ongletActif} aria-current={i === ongletActif ? 'page' : undefined}>
				<span class="palme">{#if i === ongletActif}<Ornement nom="palmette" taille={14} />{/if}</span>
				<Icone nom={o.icone} taille={22} />
				<span class="nom">{o.nom}</span>
			</a>
		{/each}
	</nav>
</div>

<style>
	.maquette {
		display: flex; flex-wrap: wrap; align-items: center; gap: 8px 20px; padding: 8px 16px;
		border-bottom: var(--hs-cheveu) dashed var(--hs-filet); color: var(--hs-encre-douce);
	}
	.univers { font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.6875rem; }
	.liens { display: flex; gap: 16px; flex: 1; flex-wrap: wrap; }
	.liens a { text-decoration: none; color: var(--hs-encre-douce); padding: 6px 0; border-bottom: var(--hs-trait) solid transparent; }
	.liens a[aria-current] { color: var(--hs-lapis); border-bottom-color: var(--hs-or); }
	.themes { display: flex; gap: 4px; }
	.themes button {
		display: inline-flex; align-items: center; gap: 4px; font: inherit; color: inherit; cursor: pointer;
		background: none; border: var(--hs-cheveu) solid var(--hs-filet); border-radius: var(--hs-rayon-tactile); padding: 5px 10px; min-height: 32px;
	}
	.themes button.actif { color: var(--hs-lapis); border-color: var(--hs-lapis); }

	.cadre { max-width: var(--hs-page); margin: 0 auto; }
	.contenu { padding-bottom: 96px; min-width: 0; }
	.sommaire { display: none; }

	/* barre d'onglets du téléphone : icônes au trait, petites capitales, palmette d'or sur l'onglet actif */
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
