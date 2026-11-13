<script lang="ts">
	import type { Snippet } from 'svelte';
	import Ornement from './Ornement.svelte';

	/**
	 * Cadre en arc plein cintre (arc roman) pour la fête du jour et les ouvertures de mois.
	 * « solennel » : double filet d'or et pièces d'angle, pour les grandes fêtes.
	 */
	let { solennel = false, children }: { solennel?: boolean; children: Snippet } = $props();
</script>

<div class="arche" class:solennel>
	<div class="interieur">{@render children()}</div>
	{#if solennel}
		<span class="coin bg"><Ornement nom="coin" taille={18} /></span>
		<span class="coin bd"><Ornement nom="coin" taille={18} /></span>
	{/if}
</div>

<style>
	.arche {
		position: relative; max-width: 26rem; margin-inline: auto;
		border: var(--hs-trait) solid var(--hs-or-trait); border-radius: 1000px 1000px 0 0;
		background: var(--hs-surface);
		padding: 0 var(--hs-e5) var(--hs-e6);
	}
	/* second filet, fin, à 3 px à l'intérieur */
	.arche::before {
		content: ''; position: absolute; inset: 4px; pointer-events: none;
		border: 0.5px solid var(--hs-or-trait); border-radius: 1000px 1000px 0 0;
	}
	.arche:not(.solennel)::before { display: none; }
	.interieur { padding-top: clamp(4.5rem, 24%, 6.5rem); text-align: center; display: grid; justify-items: center; gap: var(--hs-e3); }
	.coin { position: absolute; bottom: 9px; color: var(--hs-or); line-height: 0; }
	.coin.bg { left: 9px; transform: rotate(-90deg); }
	.coin.bd { right: 9px; transform: rotate(180deg); }
</style>
