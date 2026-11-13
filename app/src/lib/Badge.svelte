<script lang="ts">
	import { estModifie } from './db.ts';
	import type { Base } from './types.ts';
	import { etiquetteSource } from './sources.ts';

	/** Cartouche d'origine : « Livret » (or), le manuel ou l'auteur pour un texte sourcé (vert), « Ajout personnel » (lapis). */
	let { objet }: { objet: Base & { source?: { ouvrage?: string; edition?: string } } } = $props();
	const CLASSE = { livret: 'livret', officielle: 'verifiee', personnel: 'personnel' } as const;
</script>

<span class="cartouche {CLASSE[objet.origine]}">{etiquetteSource(objet)}</span>
{#if estModifie(objet)}<span class="cartouche personnel">modifié</span>{/if}
