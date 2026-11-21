<script lang="ts">
	import Ornement from './Ornement.svelte';

	/**
	 * Case carrée à double filet (trait de couleur, puis filet d'or en retrait). Cochée, elle se remplit
	 * de vert et un petit brin s'y dessine (jamais une coche ordinaire).
	 */
	let { cochee = $bindable(false), libelle }: { cochee: boolean; libelle: string } = $props();
</script>

<button class="case brut" class:cochee role="checkbox" aria-checked={cochee} aria-label={libelle} onclick={() => (cochee = !cochee)}>
	{#if cochee}<Ornement nom="brin" taille={20} />{/if}
</button>

<style>
	.case {
		flex: none;
		width: 26px;
		height: 26px;
		padding: 0;
		display: grid;
		place-items: center;
		cursor: pointer;
		background: var(--hs-fond);
		border: var(--hs-trait) solid var(--hs-encre-douce);
		border-radius: 0;
		box-shadow:
			inset 0 0 0 2px var(--hs-fond),
			inset 0 0 0 2.75px var(--hs-or-trait);
		color: var(--hs-sur-lapis);
		position: relative;
		-webkit-tap-highlight-color: transparent;
		transition:
			border-color var(--hs-duree) var(--hs-courbe),
			background var(--hs-duree) var(--hs-courbe),
			box-shadow var(--hs-duree) var(--hs-courbe);
	}
	/* zone tactile de 44 px sans grossir la case */
	.case::after {
		content: '';
		position: absolute;
		inset: -9px;
	}
	.case:hover {
		box-shadow:
			inset 0 0 0 2px var(--hs-fond),
			inset 0 0 0 2.75px var(--hs-or);
	}
	.case:active {
		transform: scale(0.94);
	}
	.case:focus-visible {
		outline: 2px solid var(--hs-or-texte);
		outline-offset: 3px;
	}
	.case.cochee {
		border-color: var(--hs-vert);
		background: var(--hs-vert);
		box-shadow:
			inset 0 0 0 2px var(--hs-vert),
			inset 0 0 0 2.75px color-mix(in srgb, var(--hs-or) 70%, var(--hs-vert));
		color: var(--hs-fond);
		animation: sceller var(--hs-duree-lente) var(--hs-courbe);
	}
	@keyframes sceller {
		0% {
			transform: scale(0.82);
		}
		60% {
			transform: scale(1.06);
		}
		100% {
			transform: none;
		}
	}
	.case :global(.trace) {
		stroke-dasharray: 1;
		stroke-dashoffset: 1;
		animation: tracer var(--hs-duree) var(--hs-courbe) forwards;
	}
	.case :global(.trace:nth-child(2)) {
		animation-delay: 80ms;
	}
	.case :global(.trace:nth-child(3)) {
		animation-delay: 160ms;
	}
	@keyframes tracer {
		to {
			stroke-dashoffset: 0;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.case.cochee {
			animation: none;
		}
		.case :global(.trace) {
			animation: none;
			stroke-dashoffset: 0;
		}
		.case:active {
			transform: none;
		}
	}
</style>
