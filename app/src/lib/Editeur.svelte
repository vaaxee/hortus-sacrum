<script lang="ts">
	import { rendre } from './markup';

	let { corps = $bindable(''), latin = $bindable(''), lignes = 14 }: { corps: string; latin: string; lignes?: number } = $props();

	let zoneFr: HTMLTextAreaElement | undefined = $state();
	let zoneLa: HTMLTextAreaElement | undefined = $state();
	let derniere: 'fr' | 'la' = $state('fr');
	let avecLatin = $state(false);
	let apercu = $state(false);

	$effect(() => {
		if (latin.trim()) avecLatin = true;
	});

	function zone() {
		return derniere === 'la' && avecLatin ? zoneLa : zoneFr;
	}
	function ecrire(valeur: string, debut: number, fin: number) {
		const z = zone();
		if (!z) return;
		if (derniere === 'la' && avecLatin) latin = valeur;
		else corps = valeur;
		queueMicrotask(() => {
			z.focus();
			z.setSelectionRange(debut, fin);
		});
	}
	/** Entoure la sélection (italique, rouge). */
	function entourer(avant: string, apres: string) {
		const z = zone();
		if (!z) return;
		const { selectionStart: a, selectionEnd: b, value: v } = z;
		ecrire(v.slice(0, a) + avant + v.slice(a, b) + apres + v.slice(b), a + avant.length, b + avant.length);
	}
	/** Insère un signe à l'endroit du curseur. */
	function inserer(signe: string) {
		const z = zone();
		if (!z) return;
		const { selectionStart: a, selectionEnd: b, value: v } = z;
		ecrire(v.slice(0, a) + signe + v.slice(b), a + signe.length, a + signe.length);
	}
	/** Place un signe au début de la ligne courante (℣, ℟, intertitre). */
	function debutDeLigne(signe: string) {
		const z = zone();
		if (!z) return;
		const { selectionStart: a, value: v } = z;
		const d = v.lastIndexOf('\n', a - 1) + 1;
		const propre = v.slice(d).replace(/^(℣\. |℟\. |## )/, '');
		const neuf = v.slice(0, d) + signe + propre;
		const pos = a + signe.length - (v.length - d - propre.length);
		ecrire(neuf, pos, pos);
	}
</script>

<div class="editeur">
	<div class="outils" role="toolbar" aria-label="Mise en forme">
		<button type="button" onclick={() => debutDeLigne('℣. ')} title="Verset">℣</button>
		<button type="button" onclick={() => debutDeLigne('℟. ')} title="Répons">℟</button>
		<button type="button" class="rouge" onclick={() => inserer('✠ ')} title="Signe de croix">✠</button>
		<button type="button" class="rouge" onclick={() => entourer('[r]', '[/r]')} title="Rubrique, en rouge">Rouge</button>
		<button type="button" onclick={() => entourer('*', '*')} title="Italique"><em>Italique</em></button>
		<button type="button" onclick={() => debutDeLigne('## ')} title="Intertitre">Titre</button>
		<span class="espace"></span>
		<button type="button" aria-pressed={avecLatin} onclick={() => (avecLatin = !avecLatin)}>Colonne latine</button>
		<button type="button" aria-pressed={apercu} onclick={() => (apercu = !apercu)}>Aperçu</button>
	</div>

	<div class="colonnes" class:deux={avecLatin}>
		<label>
			<span>Texte français</span>
			<textarea bind:this={zoneFr} bind:value={corps} rows={lignes} onfocus={() => (derniere = 'fr')} lang="fr"></textarea>
		</label>
		{#if avecLatin}
			<label>
				<span>Texte latin</span>
				<textarea bind:this={zoneLa} bind:value={latin} rows={lignes} onfocus={() => (derniere = 'la')} lang="la"></textarea>
			</label>
		{/if}
	</div>

	{#if apercu}
		<div class="apercu epreuve" aria-label="Aperçu">
			<div class="priere">{@html rendre(corps)}</div>
			{#if avecLatin && latin.trim()}
				<hr class="filet" />
				<div class="priere" lang="la"><em>{@html rendre(latin)}</em></div>
			{/if}
		</div>
	{/if}
	<p class="petit">Ligne vide : nouveau paragraphe. Les boutons ℣ et ℟ marquent la ligne où se trouve le curseur.</p>
</div>

<style>
	.outils {
		display: flex;
		flex-wrap: wrap;
		gap: 0.35rem;
		margin-bottom: 0.5rem;
		position: sticky;
		top: 0;
		background: var(--hs-fond);
		padding: 0.3rem 0;
		z-index: 1;
	}
	.outils button {
		min-width: 44px;
		min-height: 40px;
		padding: 0 10px;
		text-transform: none;
		font-family: var(--hs-lecture);
		font-size: 1.0625rem;
		letter-spacing: 0;
		font-weight: 400;
	}
	.outils .rouge {
		color: var(--hs-rubrique);
	}
	.outils button[aria-pressed='true'] {
		border-color: var(--hs-rubrique);
		color: var(--hs-rubrique);
	}
	.colonnes {
		display: grid;
		gap: 0.75rem;
	}
	@media (min-width: 46rem) {
		.colonnes.deux {
			grid-template-columns: 1fr 1fr;
		}
	}
	.apercu {
		margin-top: var(--hs-e4);
	}
</style>
