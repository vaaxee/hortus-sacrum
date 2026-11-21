<script lang="ts">
	import '#lib/design/tokens.css';
	import '../app.css';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { direction, initialiserApparence } from '#lib/apparence.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { amorcer } from '#lib/seed.ts';
	import { initialiserCompte } from '#lib/sync.ts';
	import { lireReglages, planifier } from '#lib/rappels.ts';

	let { children } = $props();
	let pret = $state(false);
	let erreur = $state('');

	onMount(async () => {
		initialiserApparence();
		try {
			await amorcer();
			await initialiserCompte();
			// rappels : replanifier les 14 prochains jours à chaque ouverture (en arrière-plan)
			lireReglages()
				.then((r) => (r.actif ? planifier() : 0))
				.catch((e) => console.error('rappels', e));
		} catch (e) {
			erreur = 'Les prières du livret n’ont pas pu être chargées. Rechargez la page.';
			console.error(e);
		}
		pret = true;
	});

	const onglets = [
		{ icone: 'aujourdhui', nom: 'Aujourd’hui', href: '/' },
		{ icone: 'lecture', nom: 'Lecture', href: '/lecture' },
		{ icone: 'prieres', nom: 'Prières', href: '/prieres' },
		{ icone: 'devotions', nom: 'Dévotions', href: '/devotions' },
		{ icone: 'calendrier', nom: 'Calendrier', href: '/calendrier' }
	] as const;
	// le Profil n'est plus un onglet : une icône en haut à droite (SPEC § 11, navigation)
	const profilActif = $derived(['/reglages', '/profil', '/historique', '/fetes', '/imprimer'].some((h) => page.url.pathname.startsWith(h)));
	const actif = (href: string) => (href === '/' ? page.url.pathname === '/' : page.url.pathname.startsWith(href));
</script>

<div class="hs">
	<!-- bandeau du haut, sous la zone de l'encoche ; propre à chaque direction artistique -->
	<div class="bandeau-haut" aria-hidden="true">
		{#if $direction === 'grecque'}<Ornement nom="mosaique" />{:else}<Ornement nom="grecque" />{/if}
	</div>

	<div class="cadre">
		<nav class="sommaire" aria-label="Navigation principale">
			<a class="marque" href="/"><Ornement nom="chrisme" taille={22} /><span>Hortus Sacrum</span></a>
			{#each onglets as o}
				<a href={o.href} class:actif={actif(o.href)} aria-current={actif(o.href) ? 'page' : undefined}>
					<Icone nom={o.icone} taille={20} /><span>{o.nom}</span>
				</a>
			{/each}
			<a href="/profil" class:actif={profilActif} aria-current={profilActif ? 'page' : undefined}>
				<Icone nom="profil" taille={20} /><span>Profil</span>
			</a>
		</nav>
		<a class="profil-haut" href="/profil" aria-label="Profil et réglages" class:actif={profilActif}><Icone nom="profil" taille={22} /></a>
		<div class="contenu">
			{#if erreur}<p class="page erreur" role="alert">{erreur}</p>{/if}
			{#if pret}{@render children()}{/if}
		</div>
	</div>

	<!-- la barre d'état du téléphone est transparente : le texte qui défile ne passe pas sous l'heure -->
	<div class="barre-etat" aria-hidden="true"></div>

	<nav class="onglets" aria-label="Navigation principale">
		{#each onglets as o}
			<a href={o.href} class:actif={actif(o.href)} aria-current={actif(o.href) ? 'page' : undefined}>
				<!-- l'onglet actif se loge dans une niche, une croisette d'or à la clef -->
				<span class="niche" aria-hidden="true">
					<svg viewBox="0 0 46 40" width="46" height="40">
						<path class="arc" d="M3 40V21a20 17 0 0 1 40 0v19" />
						<path class="clef" d="M23 1v6.500M20.300 3.600h5.400" />
					</svg>
				</span>
				<span class="icone"><Icone nom={o.icone} taille={22} /></span>
				<span class="nom">{o.nom}</span>
			</a>
		{/each}
	</nav>
</div>

<style>
	.barre-etat {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		height: env(safe-area-inset-top);
		background: var(--hs-fond);
		z-index: 15;
		pointer-events: none;
	}
	.bandeau-haut {
		padding-top: calc(env(safe-area-inset-top) + 6px);
		color: var(--hs-or);
		line-height: 0;
	}
	.profil-haut {
		position: absolute;
		top: 4px;
		right: max(12px, env(safe-area-inset-right));
		z-index: 16;
		display: grid;
		place-items: center;
		width: 44px;
		height: 44px;
		border-radius: 50%;
		color: var(--hs-encre-douce);
	}
	.profil-haut.actif {
		color: var(--hs-or);
	}
	.cadre {
		position: relative;
		max-width: var(--hs-page);
		margin: 0 auto;
	}
	.contenu {
		padding-bottom: calc(96px + env(safe-area-inset-bottom));
		min-width: 0;
	}
	.sommaire {
		display: none;
	}

	/* téléphone : barre d'onglets ; double filet en tête (or, puis pierre), grain de papier,
	   l'onglet actif logé dans une niche d'or. La zone de l'indicateur d'accueil (iOS) reste dégagée. */
	.onglets {
		position: fixed;
		inset: auto 0 0 0;
		z-index: 5;
		display: flex;
		justify-content: space-around;
		background: color-mix(in srgb, var(--hs-surface-douce) 55%, var(--hs-fond));
		border-top: var(--hs-cheveu) solid var(--hs-or-trait);
		box-shadow: 0 -6px 14px -12px color-mix(in srgb, var(--hs-encre) 40%, transparent);
		padding: 5px max(4px, env(safe-area-inset-right)) calc(4px + env(safe-area-inset-bottom)) max(4px, env(safe-area-inset-left));
	}
	/* second filet, de pierre, à 3 px sous le filet d'or */
	.onglets::before {
		content: '';
		position: absolute;
		inset: 3px 0 auto;
		border-top: var(--hs-cheveu) solid var(--hs-filet);
		pointer-events: none;
	}
	/* grain de papier propre à la barre (le grain de la page passe dessous) */
	.onglets::after {
		content: '';
		position: absolute;
		inset: 0;
		pointer-events: none;
		opacity: calc(var(--hs-grain) * 2.2);
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .5 0 0 0 0 .45 0 0 0 0 .35 0 0 0 1 0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23g)'/%3E%3C/svg%3E");
	}
	.onglets a {
		flex: 1;
		position: relative;
		z-index: 1;
		display: grid;
		justify-items: center;
		align-content: start;
		gap: 3px;
		min-height: 58px;
		padding: 12px 0 4px;
		text-decoration: none;
		color: var(--hs-encre-douce);
		min-width: 0;
		-webkit-tap-highlight-color: transparent;
	}
	.onglets a:focus-visible {
		outline: 2px solid var(--hs-or-texte);
		outline-offset: -2px;
	}
	.onglets .icone {
		display: grid;
		place-items: center;
		height: 26px;
		line-height: 0;
		transition: transform 120ms var(--hs-courbe);
	}
	.onglets a:active .icone {
		transform: translateY(1px) scale(0.96);
	}
	.niche {
		position: absolute;
		top: 2px;
		left: 50%;
		width: 46px;
		height: 40px;
		margin-left: -23px;
		line-height: 0;
		opacity: 0;
		transform: scaleY(0.6);
		transform-origin: 50% 100%;
		transition:
			opacity var(--hs-duree) var(--hs-courbe),
			transform var(--hs-duree) var(--hs-courbe);
		pointer-events: none;
	}
	.niche svg {
		display: block;
		overflow: visible;
	}
	.niche .arc {
		fill: color-mix(in srgb, var(--hs-lapis) 9%, transparent);
		stroke: var(--hs-or);
		stroke-width: 1;
	}
	.niche .clef {
		fill: none;
		stroke: var(--hs-or);
		stroke-width: 1.2;
		stroke-linecap: round;
	}
	.onglets a.actif {
		color: var(--hs-lapis);
	}
	.onglets a.actif .niche {
		opacity: 1;
		transform: none;
	}
	.onglets .nom {
		font-family: var(--hs-lecture);
		font-variant-caps: all-small-caps;
		letter-spacing: 0.03em;
		font-size: 0.875rem;
		line-height: 1.1;
		white-space: nowrap;
		position: relative;
	}
	.onglets a.actif .nom {
		font-weight: 600;
	}
	@media (max-width: 359px) {
		.onglets .nom {
			font-size: 0.8125rem;
			letter-spacing: 0.02em;
		}
	}

	/* ordinateur : colonne de gauche, comme la table d'un beau livre */
	@media (min-width: 900px) {
		.onglets,
		.profil-haut {
			display: none;
		}
		.cadre {
			display: grid;
			grid-template-columns: 220px minmax(0, 1fr);
			gap: 24px;
			padding: 0 24px;
		}
		.contenu {
			padding-bottom: var(--hs-e9);
		}
		.sommaire {
			display: flex;
			flex-direction: column;
			gap: 2px;
			position: sticky;
			top: 0;
			align-self: start;
			padding: var(--hs-e7) 0 var(--hs-e6);
			border-right: var(--hs-cheveu) solid var(--hs-filet);
			min-height: 100dvh;
		}
		.sommaire a {
			display: flex;
			align-items: center;
			gap: 12px;
			padding: 9px 16px 9px 14px;
			text-decoration: none;
			color: var(--hs-encre-douce);
			border-left: 2px solid transparent;
			font-family: var(--hs-lecture);
			font-variant-caps: all-small-caps;
			letter-spacing: var(--hs-chasse-petites-cap);
			font-size: 1.0625rem;
		}
		.sommaire a.actif {
			color: var(--hs-lapis);
			border-left-color: var(--hs-or);
		}
		.sommaire .marque {
			color: var(--hs-encre);
			font-family: var(--hs-accent);
			font-variant-caps: normal;
			letter-spacing: 0.02em;
			font-size: 1.25rem;
			margin-bottom: var(--hs-e6);
			border-left-color: transparent;
		}
		.sommaire .marque :global(svg) {
			color: var(--hs-rubrique);
		}
	}
</style>
