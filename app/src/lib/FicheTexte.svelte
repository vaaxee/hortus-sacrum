<script lang="ts">
	import Editeur from './Editeur.svelte';
	import { ETIQUETTES, etiquettesDe } from './etiquettes.ts';
	import type { Texte } from './types';

	/** Formulaire complet d'une prière : texte, latin, usage, indulgence, source, classement. */
	let { texte = $bindable(), parties = [] }: { texte: Texte; parties?: string[] } = $props();
	// étiquettes du cadre pratique : déduites du texte tant que l'utilisateur ne les a pas réglées
	const toutes = Object.values(ETIQUETTES).flat();
	function basculer(e: string) {
		const cur = etiquettesDe(texte);
		texte.etiquettes = cur.includes(e) ? cur.filter((x) => x !== e) : [...cur, e];
	}
</script>

<label>
	<span>Titre</span>
	<input type="text" bind:value={texte.titre} />
</label>

<Editeur bind:corps={texte.corps} bind:latin={texte.latin} />

<div class="grille">
	<label>
		<span>Partie</span>
		<input type="text" bind:value={texte.partie} list="parties" />
		<datalist id="parties">{#each parties as p}<option value={p}></option>{/each}</datalist>
	</label>
	<label>
		<span>Catégorie</span>
		<input type="text" bind:value={texte.categorie} />
	</label>
</div>
<label>
	<span>Usage (jour ou moment recommandé)</span>
	<input type="text" bind:value={texte.usage} />
</label>
<fieldset class="etiquettes">
	<legend>Étiquettes (cadre pratique){texte.etiquettes ? '' : ' — déduites du texte'}</legend>
	{#each toutes as e}
		<label class="case"><input type="checkbox" checked={etiquettesDe(texte).includes(e)} onchange={() => basculer(e)} /> {e}</label>
	{/each}
</fieldset>
<label>
	<span>Indulgence</span>
	<textarea rows="2" bind:value={texte.indulgence}></textarea>
</label>

<fieldset>
	<legend>Source</legend>
	<label><span>Ouvrage</span><input type="text" bind:value={texte.source.ouvrage} /></label>
	<div class="grille">
		<label><span>Édition</span><input type="text" bind:value={texte.source.edition} /></label>
		<label><span>Page ou numéro</span><input type="text" bind:value={texte.source.page} /></label>
	</div>
	<label><span>Adresse (URL)</span><input type="url" bind:value={texte.source.url} /></label>
</fieldset>

<style>
	.etiquettes { display: flex; flex-wrap: wrap; gap: 0.25rem 0.75rem; }
	.etiquettes .case { display: inline-flex; align-items: center; gap: 0.25rem; }
	label, fieldset { margin-top: 0.8rem; }
	.grille { display: grid; gap: 0.75rem; grid-template-columns: 1fr 1fr; }
	fieldset { border: 1px solid var(--hs-filet); border-radius: 0; padding: 0.2rem 0.8rem 0.8rem; }
	legend { font-variant: small-caps; letter-spacing: 0.05em; color: var(--hs-rubrique); padding: 0 0.3rem; }
</style>
