<script lang="ts">
	import Editeur from './Editeur.svelte';
	import type { Texte } from './types';

	/** Formulaire complet d'une prière : texte, latin, usage, indulgence, source, classement. */
	let { texte = $bindable(), parties = [] }: { texte: Texte; parties?: string[] } = $props();
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
	label, fieldset { margin-top: 0.8rem; }
	.grille { display: grid; gap: 0.75rem; grid-template-columns: 1fr 1fr; }
	fieldset { border: 1px solid var(--hs-filet); border-radius: 0; padding: 0.2rem 0.8rem 0.8rem; }
	legend { font-variant: small-caps; letter-spacing: 0.05em; color: var(--hs-rubrique); padding: 0 0.3rem; }
</style>
