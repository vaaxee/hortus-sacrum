<script lang="ts">
	import Ornement from './Ornement.svelte';

	/** Case carrée : cochée, un petit brin vert s'y dessine (jamais une coche ordinaire). */
	let { cochee = $bindable(false), libelle }: { cochee: boolean; libelle: string } = $props();
</script>

<button class="case brut" class:cochee role="checkbox" aria-checked={cochee} aria-label={libelle} onclick={() => (cochee = !cochee)}>
	{#if cochee}<Ornement nom="brin" taille={22} />{/if}
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
		color: var(--hs-vert);
		position: relative;
		transition: border-color var(--hs-duree) var(--hs-courbe);
	}
	/* zone tactile de 44 px sans grossir la case */
	.case::after {
		content: '';
		position: absolute;
		inset: -9px;
	}
	.case.cochee {
		border-color: var(--hs-vert);
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
</style>
