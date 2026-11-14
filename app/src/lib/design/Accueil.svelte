<script lang="ts">
	/**
	 * Écran d'accueil, avant « Aujourd'hui » : le nom de l'app, la Vierge gravée à l'or (d'après le Couronnement de la Vierge
	 * de Velázquez, v. 1635, Prado, domaine public), l'introït du jour, une invocation et l'avancement du jour en trois fleurons.
	 */
	import Ornement from './Ornement.svelte';
	let {
		introit = '', introitFr = '', invocation = '', avancement = 0, entrer
	}: { introit?: string; introitFr?: string; invocation?: string; avancement?: number; entrer: () => void } = $props();
	let traduction = $state(false);
	// image d'accueil : le tableau (par défaut) ou sa gravure à l'or ; réglage gardé sur l'appareil
	let image = $state<'tableau' | 'gravure'>('tableau');
	$effect(() => {
		try { image = (localStorage.getItem('accueil-image') as 'tableau' | 'gravure') || 'tableau'; } catch { /* stockage indisponible */ }
	});
	// pendant l'accueil, la barre d'onglets est masquée
	$effect(() => {
		document.documentElement.classList.add('accueil-ouvert');
		return () => document.documentElement.classList.remove('accueil-ouvert');
	});
	// trois fleurons : matin, jour, soir ; chacun s'allume quand un tiers de la liste est faite
	const allumes = $derived(Math.min(3, Math.floor(avancement * 3 + 0.0001)));
</script>

<div class="accueil" role="dialog" aria-label="Accueil">
	<p class="nom">Hortus Sacrum</p>
	<div class="arche" aria-hidden="true">
		{#if image === 'gravure'}<div class="gravure"></div>{:else}<img class="tableau" src="/accueil/velazquez.jpg" alt="" />{/if}
	</div>
	{#if introit}
		<button class="brut introit" onclick={() => (traduction = !traduction)} aria-label="Introït du jour : afficher la traduction">
			<span class="pc">Introït</span>
			<em lang={traduction ? 'fr' : 'la'}>{traduction && introitFr ? introitFr : introit}</em>
		</button>
	{/if}
	{#if invocation}<p class="invocation">{invocation}</p>{/if}
	<div class="fleurons" role="img" aria-label="Jardin du jour : {allumes} sur 3">
		{#each [0, 1, 2] as i}<span class:allume={i < allumes}><Ornement nom="lis" taille={18} /></span>{/each}
	</div>
	<button class="entrer" onclick={entrer}>Entrer au jardin</button>
	<p class="credit">{image === 'gravure' ? 'D’après ' : ''}Velázquez, <em>Le Couronnement de la Vierge</em>, v. 1635</p>
</div>

<style>
	.accueil {
		position: fixed; inset: 0; z-index: 20; overflow-y: auto; background: var(--hs-fond);
		display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--hs-e4);
		padding: calc(var(--hs-e6) + env(safe-area-inset-top)) var(--hs-marge-mobile) calc(var(--hs-e6) + env(safe-area-inset-bottom));
		text-align: center; animation: venir 900ms var(--hs-courbe);
	}
	.nom { margin: 0; font-family: var(--hs-titre); font-size: var(--hs-t3); letter-spacing: 0.18em; text-transform: uppercase; color: var(--hs-or-texte); }
	.arche {
		width: min(72vw, 21rem); aspect-ratio: 3 / 4; padding: 10px; border: var(--hs-trait) solid var(--hs-or-trait);
		border-radius: 50% 50% 0 0 / 34% 34% 0 0;
	}
	.gravure {
		width: 100%; height: 100%; border-radius: 50% 50% 0 0 / 34% 34% 0 0;
		background: var(--hs-or-texte); /* or sombre le jour, or clair la nuit */
		-webkit-mask: url('/accueil/vierge.png') center 12% / cover no-repeat;
		mask: url('/accueil/vierge.png') center 12% / cover no-repeat;
	}
	.tableau {
		width: 100%; height: 100%; object-fit: cover; object-position: center 12%; display: block;
		border-radius: 50% 50% 0 0 / 34% 34% 0 0; box-shadow: inset 0 0 0 1px var(--hs-or-trait);
	}
	.introit { background: none; border: 0; padding: 4px 8px; display: grid; gap: 2px; max-width: 26rem; cursor: pointer; color: var(--hs-encre); }
	.introit .pc { color: var(--hs-rubrique); font-size: 0.9375rem; }
	.introit em { font-size: 1.125rem; line-height: 1.4; }
	.invocation { margin: 0; font-style: italic; color: var(--hs-encre-douce); font-size: 1.0625rem; max-width: 24rem; }
	.invocation::before { content: '✠ '; color: var(--hs-rubrique); font-style: normal; }
	.fleurons { display: flex; gap: 14px; color: var(--hs-filet); }
	.fleurons .allume { color: var(--hs-or); }
	.entrer { margin-top: var(--hs-e2); }
	.credit { margin: 0; font-size: 0.75rem; color: var(--hs-encre-douce); opacity: 0.7; }
	@keyframes venir { from { opacity: 0; } to { opacity: 1; } }
	@media (prefers-reduced-motion: reduce) { .accueil { animation: none; } }
</style>
