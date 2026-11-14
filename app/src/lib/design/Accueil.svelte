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
	<!-- cadre : frises en haut et en bas, quarts de rosace aux angles -->
	<div class="frise haut" aria-hidden="true"><Ornement nom="grecque" /></div>
	<div class="frise bas" aria-hidden="true"><Ornement nom="grecque" /></div>
	{#each ['hg', 'hd', 'bg', 'bd'] as c}<span class="coin {c}" aria-hidden="true"><Ornement nom="coin" taille={30} /></span>{/each}

	<p class="nom">Hortus Sacrum</p>
	<div class="filet-titre" aria-hidden="true"><Ornement nom="fleuron" /></div>
	<div class="niche" aria-hidden="true">
		<span class="cle"><Ornement nom="croix-pattee" taille={22} /></span>
		<span class="cherub g"><Ornement nom="cherubin" taille={18} /></span>
		<span class="cherub d"><Ornement nom="cherubin" taille={18} /></span>
	<div class="arche" aria-hidden="true">
		{#if image === 'gravure'}<div class="gravure"></div>{:else}<img class="tableau" src="/accueil/velazquez.jpg" alt="" />{/if}
	</div>
		<div class="socle"><Ornement nom="perles" /></div>
	</div>
	{#if introit}
		<button class="brut introit" onclick={() => (traduction = !traduction)} aria-label="Introït du jour : afficher la traduction">
			<span class="pc">Introït</span>
			<em lang={traduction ? 'fr' : 'la'}>{traduction && introitFr ? introitFr : introit}</em>
		</button>
	{/if}
	<div class="filet-milieu" aria-hidden="true"><Ornement nom="laurier" /></div>
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
	.frise { position: fixed; left: 0; right: 0; color: var(--hs-or); opacity: 0.85; line-height: 0; }
	.frise.haut { top: env(safe-area-inset-top); }
	.frise.bas { bottom: env(safe-area-inset-bottom); }
	.coin { position: fixed; color: var(--hs-or); opacity: 0.8; line-height: 0; }
	.coin.hg { top: calc(18px + env(safe-area-inset-top)); left: 10px; }
	.coin.hd { top: calc(18px + env(safe-area-inset-top)); right: 10px; transform: scaleX(-1); }
	.coin.bg { bottom: calc(18px + env(safe-area-inset-bottom)); left: 10px; transform: scaleY(-1); }
	.coin.bd { bottom: calc(18px + env(safe-area-inset-bottom)); right: 10px; transform: scale(-1, -1); }
	.filet-titre { width: min(60vw, 16rem); color: var(--hs-or); margin-top: -10px; }
	.filet-milieu { width: min(50vw, 12rem); color: var(--hs-or-trait); }
	.niche { position: relative; display: grid; justify-items: center; }
	.cle { position: absolute; top: -13px; left: 50%; transform: translateX(-50%); z-index: 1; color: var(--hs-rubrique); background: var(--hs-fond); padding: 0 4px; line-height: 0; }
	.cherub { position: absolute; top: 34%; color: var(--hs-or); line-height: 0; }
	.cherub.g { left: -34px; }
	.cherub.d { right: -34px; transform: scaleX(-1); }
	.socle { width: calc(100% + 24px); color: var(--hs-or); margin-top: 6px; line-height: 0; }
	@media (max-width: 380px) { .cherub { display: none; } }
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
