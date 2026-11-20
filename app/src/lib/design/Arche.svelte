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
	<div class="interieur">
		{@render children()}
		<!-- rameau de laurier sous le nom, dans les deux directions -->
		<span class="rameau" aria-hidden="true"><Ornement nom="laurier" /></span>
	</div>
	<!-- grecque : chrisme à la clé, palmettes aux angles, filet intérieur de tesselles -->
	<span class="cle da-grecque"><Ornement nom="chrisme" taille={22} /></span>
	<span class="pattee g da-grecque"><Ornement nom="palmette" taille={16} /></span>
	<span class="pattee d da-grecque"><Ornement nom="palmette" taille={16} /></span>
	<span class="filet-interieur da-grecque" aria-hidden="true"></span>
	<!-- latine : fleur de lys à la clé de l'arche, croix pattées aux angles -->
	<span class="cle da-latine"><Ornement nom="lis" taille={22} /></span>
	<span class="pattee g da-latine"><Ornement nom="croix-pattee" taille={14} /></span>
	<span class="pattee d da-latine"><Ornement nom="croix-pattee" taille={14} /></span>
	{#if solennel}
		<span class="coin bg"><Ornement nom="coin" taille={18} /></span>
		<span class="coin bd"><Ornement nom="coin" taille={18} /></span>
	{/if}
</div>

<style>
	.arche {
		position: relative;
		max-width: 26rem;
		margin-inline: auto;
		border: var(--hs-trait) solid var(--hs-arche-filet);
		border-radius: 1000px 1000px 0 0;
		background: var(--hs-arche-fond);
		color: var(--hs-arche-encre);
		/* à l'intérieur de l'arche, les rôles suivent le fond de l'arche */
		--hs-encre: var(--hs-arche-encre);
		--hs-encre-douce: var(--hs-arche-encre-douce);
		--hs-rubrique: var(--hs-arche-accent);
		padding: 0 var(--hs-e5) var(--hs-e6);
	}
	/* second filet, fin, à 3 px à l'intérieur */
	.arche::before {
		content: '';
		position: absolute;
		inset: 4px;
		pointer-events: none;
		border: 0.5px solid var(--hs-arche-filet);
		border-radius: 1000px 1000px 0 0;
	}
	.arche:not(.solennel)::before {
		display: none;
	}
	.interieur {
		padding-top: clamp(4.5rem, 24%, 6.5rem);
		text-align: center;
		display: grid;
		justify-items: center;
		gap: var(--hs-e3);
	}
	.cle {
		position: absolute;
		top: 10px;
		left: 50%;
		transform: translateX(-50%);
		color: var(--hs-arche-filet);
		line-height: 0;
	}
	.pattee {
		position: absolute;
		bottom: 12px;
		color: var(--hs-arche-filet);
		line-height: 0;
	}
	.pattee.g {
		left: 12px;
	}
	.pattee.d {
		right: 12px;
	}
	.solennel .pattee {
		bottom: 34px;
	}
	.rameau {
		display: block;
		width: min(60%, 12rem);
		color: var(--hs-arche-filet);
		opacity: 0.85;
		line-height: 0;
	}
	/* filet intérieur pointillé, à 6 px du bord : l'arche paraît sertie */
	.filet-interieur {
		position: absolute;
		inset: 6px;
		pointer-events: none;
		border: 1px dotted var(--hs-arche-filet);
		border-bottom: 0;
		border-radius: 1000px 1000px 0 0;
		opacity: 0.7;
	}
	.coin {
		position: absolute;
		bottom: 9px;
		color: var(--hs-arche-filet);
		line-height: 0;
	}
	.coin.bg {
		left: 9px;
		transform: rotate(-90deg);
	}
	.coin.bd {
		right: 9px;
		transform: rotate(180deg);
	}
</style>
