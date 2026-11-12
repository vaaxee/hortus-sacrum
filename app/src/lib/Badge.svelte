<script lang="ts">
	import { estModifie } from './db';
	import { ORIGINE_LIBELLE, type Base } from './types';

	let { objet }: { objet: Base } = $props();
</script>

<span class="badge {objet.origine}">{ORIGINE_LIBELLE[objet.origine]}</span>
{#if estModifie(objet)}<span class="badge modifie">modifié</span>{/if}
