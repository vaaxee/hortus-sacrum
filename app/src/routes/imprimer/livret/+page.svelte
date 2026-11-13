<script lang="ts">
	import { page } from '$app/state';
	import { db } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { rendre } from '#lib/markup.ts';
	import type { Texte } from '#lib/types.ts';

	/** Livret de poche, 110 × 170 mm : page de titre, table, puis chaque prière avec son indulgence et sa source. */
	const ids = $derived((page.url.searchParams.get('t') ?? '').split(',').filter(Boolean));
	const titre = $derived(page.url.searchParams.get('titre') || 'Livret de prières');
	let textes = $state<Texte[]>([]);
	$effect(() => {
		const liste = ids;
		db.textes.bulkGet(liste).then((t) => (textes = t.filter((x): x is Texte => !!x)));
	});
	const ref = (t: Texte) => [t.source.ouvrage, t.source.edition, t.source.page ? `p. ${t.source.page}` : ''].filter(Boolean).join(', ');
</script>

<svelte:head>
	<title>{titre} — Hortus Sacrum</title>
	{@html `<style>@page { size: 110mm 170mm; margin: 13mm 11mm 15mm; }</style>`}
</svelte:head>

<div class="ecran-seul barre">
	<a href="/imprimer">Retour</a>
	<button class="principal" onclick={() => window.print()}>Imprimer ou enregistrer en PDF</button>
</div>

<article class="livret">
	<section class="couverture">
		<Ornement nom="chrisme" taille={42} />
		<h1>{titre}</h1>
		<Ornement nom="fleuron" />
		<p class="sous">Hortus Sacrum</p>
	</section>

	<section class="table">
		<h2>Table</h2>
		<ol>{#each textes as t (t.id)}<li>{t.titre}</li>{/each}</ol>
	</section>

	{#each textes as t (t.id)}
		<section class="piece">
			<h2>{t.titre}</h2>
			{#if t.usage}<p class="usage">{t.usage}</p>{/if}
			<div class="lecture">{@html rendre(t.corps)}</div>
			{#if t.latin}<div class="lecture latin" lang="la">{@html rendre(t.latin)}</div>{/if}
			{#if t.indulgence}<p class="note"><span class="pc">Indulgence.</span> {t.indulgence}</p>{/if}
			{#if ref(t)}<p class="note source">{ref(t)}</p>{/if}
		</section>
	{/each}
</article>

<style>
	.barre { display: flex; justify-content: space-between; align-items: center; gap: 12px; max-width: 110mm; margin: 24px auto 12px; padding: 0 12px; }
	.livret { max-width: 110mm; margin: 0 auto; padding: 0 12px 120px; font-size: 10.5pt; line-height: 1.42; hyphens: auto; }
	.couverture { min-height: 140mm; display: grid; place-content: center; justify-items: center; gap: 14px; text-align: center; color: var(--hs-or-texte); break-after: page; }
	.couverture h1 { color: var(--hs-encre); font-size: 20pt; }
	.sous { font-family: var(--hs-titre); font-style: italic; color: var(--hs-encre-douce); margin: 0; }
	.table { break-after: page; }
	.table h2, .piece h2 { font-size: 14pt; text-align: center; color: var(--hs-rubrique); margin: 0 0 8pt; }
	.table ol { padding-left: 1.2em; font-size: 10pt; }
	.piece { break-before: page; }
	.piece :global(p) { margin: 0 0 5pt; text-align: justify; }
	.piece :global(h3) { font-size: 10.5pt; color: var(--hs-rubrique); text-align: center; margin: 8pt 0 4pt; }
	.usage { font-style: italic; font-size: 9pt; color: var(--hs-encre-douce); text-align: center; }
	.latin { margin-top: 8pt; font-style: italic; color: var(--hs-encre-douce); }
	.note { font-size: 8.5pt; color: var(--hs-encre-douce); margin: 8pt 0 0; border-top: 0.5pt solid var(--hs-filet); padding-top: 4pt; }
	.source { font-style: italic; border: 0; padding: 0; margin-top: 3pt; }
	@media print {
		.livret { max-width: none; padding: 0; }
		.couverture { min-height: 130mm; }
	}
</style>
