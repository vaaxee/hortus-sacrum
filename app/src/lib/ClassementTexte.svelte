<script lang="ts">
	import { basculerValeur, dimensionsEffectives, marquerRelu } from './dimensions.ts';
	import { chargerClassements, chargerVocabulaire } from './programme/dimensions.ts';
	import { DIMENSIONS, type ClassementTexte, type Vocabulaire } from './programme/types.ts';
	import type { Texte } from './types.ts';

	/**
	 * Relecture du classement d'une prière (lot « Dimensions », D2) : cinq rangées de pastilles (fins, objets, grâces,
	 * personnes, formes). Les valeurs encore devinées sont en gris ; « Relu » les confirme toutes.
	 */
	let { texte = $bindable() }: { texte: Texte } = $props();
	let vocabulaire = $state.raw<Vocabulaire | null>(null);
	let livre = $state.raw<ClassementTexte | undefined>();
	chargerVocabulaire().then((v) => (vocabulaire = v));
	$effect(() => {
		const id = texte.id;
		chargerClassements().then((c) => (livre = c?.[id]));
	});
	const effectives = $derived(dimensionsEffectives(texte, livre));
	const aujourdhui = () => new Date().toISOString().slice(0, 10);
	const dateFr = (d: string) => new Date(d + 'T12:00:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
</script>

{#if vocabulaire}
	<fieldset class="classement">
		<legend>Classement</legend>
		<p class="aide">
			{#if effectives.devinees.size}
				En gris : valeurs devinées d’après le texte, à relire. Touchez une valeur pour l’ajouter ou la retirer.
			{:else if effectives.releve}
				Relu le {dateFr(effectives.releve)}.
			{:else}
				Réglé à la main.
			{/if}
		</p>
		{#each DIMENSIONS as d (d)}
			{@const dim = vocabulaire.dimensions[d]}
			<div class="rangee" role="group" aria-label={dim.libelle}>
				<span class="nom pc" title={dim.aide}>{dim.libelle}</span>
				{#each Object.entries(dim.valeurs) as [v, libelle] (v)}
					{@const choisie = effectives.valeurs[d]?.includes(v) ?? false}
					<button
						type="button"
						class="valeur brut"
						class:choisie
						class:devinee={choisie && effectives.devinees.has(d)}
						aria-pressed={choisie}
						onclick={() => (texte.dimensions = basculerValeur(texte, livre, d, v))}>{libelle}</button
					>
				{/each}
			</div>
		{/each}
		{#if effectives.devinees.size}
			<button type="button" class="relu" onclick={() => (texte.dimensions = marquerRelu(texte, livre, aujourdhui()))}>Relu</button>
		{/if}
	</fieldset>
{/if}

<style>
	.classement {
		display: grid;
		gap: 0.5rem;
	}
	.rangee {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0.3rem;
	}
	.nom {
		flex-basis: 100%;
		font-size: 0.8125rem;
		color: var(--hs-encre-douce);
	}
	.rangee .valeur {
		flex: none;
		white-space: nowrap;
		padding: 4px 10px;
		min-height: 30px;
		border: var(--hs-cheveu) solid var(--hs-filet);
		border-radius: 999px;
		background: none;
		color: var(--hs-encre-douce);
		font-family: var(--hs-interface);
		font-size: 0.8125rem;
		line-height: 1.2;
		cursor: pointer;
	}
	.rangee .valeur.choisie {
		border-color: var(--hs-or-trait);
		background: color-mix(in srgb, var(--hs-or) 18%, var(--hs-fond));
		color: var(--hs-encre);
	}
	.rangee .valeur.devinee {
		background: var(--hs-surface-douce);
		color: var(--hs-encre-douce);
		border-style: dashed;
	}
	.relu {
		justify-self: start;
	}
</style>
