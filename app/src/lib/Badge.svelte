<script lang="ts">
	import { estModifie } from './db.ts';
	import type { Base } from './types.ts';

	/** Cartouche d'origine : « Livret » (or), « Source vérifiée » (vert), « Ajout personnel » (lapis). */
	let { objet }: { objet: Base } = $props();
	const ORIGINE = {
		livret: ['livret', 'Livret'],
		officielle: ['verifiee', 'Source vérifiée'],
		personnel: ['personnel', 'Ajout personnel']
	} as const;
</script>

<span class="cartouche {ORIGINE[objet.origine][0]}">{ORIGINE[objet.origine][1]}</span>
{#if estModifie(objet)}<span class="cartouche personnel">modifié</span>{/if}
