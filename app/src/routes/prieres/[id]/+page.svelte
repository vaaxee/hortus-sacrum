<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import Badge from '#lib/Badge.svelte';
	import FicheTexte from '#lib/FicheTexte.svelte';
	import {
		db, dupliquer, enregistrer, estModifie, mettreALaCorbeille, restaurerOriginal, restaurerVersion,
		sortirDeLaCorbeille, versions
	} from '#lib/db.ts';
	import { vivant } from '#lib/live.ts';
	import { rendre } from '#lib/markup.ts';
	import type { Texte, Version } from '#lib/types.ts';

	const id = $derived(decodeURIComponent(page.params.id ?? ''));
	const texte = $derived(vivant(() => db.textes.get(id), undefined as Texte | undefined));
	const parties = vivant(
		async () => [...new Set((await db.textes.toArray()).map((t) => t.partie).filter(Boolean))],
		[] as string[]
	);

	let edition = $state(false);
	let brouillon: Texte | undefined = $state();
	let historique: Version[] = $state([]);
	let voirHistorique = $state(false);
	let voirLatin = $state(false);
	let voirSource = $state(false);

	function modifier() {
		if (!$texte) return;
		brouillon = structuredClone($texte);
		edition = true;
	}
	async function sauver() {
		if (!brouillon) return;
		await enregistrer('textes', $state.snapshot(brouillon) as Texte);
		edition = false;
	}
	async function ouvrirHistorique() {
		historique = await versions('textes', id);
		voirHistorique = !voirHistorique;
	}
	async function revenir(v: Version) {
		await restaurerVersion('textes', id, v);
		historique = await versions('textes', id);
	}
	async function copier() {
		const c = await dupliquer<Texte>('textes', id);
		if (c) goto(`/prieres/${encodeURIComponent(c.id)}`);
	}
	async function favori() {
		if ($texte) await db.textes.update(id, { favori: !$texte.favori });
	}
	async function jeter() {
		await mettreALaCorbeille('textes', id);
		goto('/prieres');
	}
	const dateFr = (iso: string) => new Date(iso).toLocaleString('fr-FR', { dateStyle: 'medium', timeStyle: 'short' });
	const titreVersion = (v: Version) => (JSON.parse(v.contenu) as Texte).titre;
	const ligneSource = (t: Texte) =>
		[t.source.ouvrage, t.source.edition, t.source.page && `p. ${t.source.page}`].filter(Boolean).join(' — ');
</script>

<svelte:head><title>{$texte?.titre ?? 'Prière'} — Hebdomada</title></svelte:head>

<main class="page">
	<a class="petit" href="/prieres">← Prières</a>

	{#if !$texte}
		<p>Cette prière est introuvable.</p>
	{:else if edition && brouillon}
		<h1>Modifier</h1>
		<FicheTexte bind:texte={brouillon} parties={$parties} />
		<div class="rangee actions">
			<button class="principal" onclick={sauver}>Enregistrer</button>
			<button onclick={() => (edition = false)}>Annuler</button>
		</div>
	{:else}
		<header>
			<h1>{$texte.titre}</h1>
			<p class="rangee">
				<Badge objet={$texte} />
				{#if $texte.partie}<span class="petit">{$texte.partie}</span>{/if}
			</p>
			{#if $texte.usage}<p class="petit"><span class="rub">usage :</span> <em>{$texte.usage}</em></p>{/if}
		</header>

		{#if $texte.supprimeLe}
			<p class="corbeille">
				Cette prière est dans la corbeille.
				<button onclick={() => sortirDeLaCorbeille('textes', id)}>La rétablir</button>
			</p>
		{/if}

		<article class="priere">{@html rendre($texte.corps)}</article>

		{#if $texte.latin.trim()}
			<button class="discret" aria-expanded={voirLatin} onclick={() => (voirLatin = !voirLatin)}>
				{voirLatin ? '▾' : '▸'} Latin
			</button>
			{#if voirLatin}<article class="priere latin" lang="la">{@html rendre($texte.latin)}</article>{/if}
		{/if}

		{#if $texte.indulgence}
			<p class="indulgence"><span class="ind">Ind.</span> <em>{$texte.indulgence}</em></p>
		{/if}

		<button class="discret" aria-expanded={voirSource} onclick={() => (voirSource = !voirSource)}>
			{voirSource ? '▾' : '▸'} Source
		</button>
		{#if voirSource}
			<p class="petit source">
				{ligneSource($texte) || 'Aucune source indiquée.'}
				{#if $texte.source.url}<br /><a href={$texte.source.url} rel="noopener" target="_blank">{$texte.source.url}</a>{/if}
			</p>
		{/if}

		<hr class="filet" />
		<div class="rangee actions">
			<button class="principal" onclick={modifier}>Modifier</button>
			<button onclick={favori}>{$texte.favori ? '★ Favori' : '☆ Favori'}</button>
			<button onclick={copier}>Dupliquer</button>
			<button onclick={ouvrirHistorique}>Historique</button>
			{#if estModifie($texte)}
				<button onclick={() => restaurerOriginal('textes', id)}>Restaurer l’original</button>
			{/if}
			{#if !$texte.supprimeLe}
				<button onclick={jeter}>Mettre à la corbeille</button>
			{/if}
		</div>

		{#if voirHistorique}
			<section class="historique">
				<h2>Versions précédentes</h2>
				{#each historique as v (v.id)}
					<div class="rangee version">
						<span>{dateFr(v.date)} <span class="petit">— {titreVersion(v)}</span></span>
						<span class="espace"></span>
						<button onclick={() => revenir(v)}>Revenir à cette version</button>
					</div>
				{:else}
					<p class="petit">Aucune version précédente : ce texte n’a pas encore été modifié.</p>
				{/each}
			</section>
		{/if}
	{/if}
</main>

<style>
	header { margin: 0.6rem 0 1.2rem; }
	header p { margin: 0.35rem 0 0; }
	.latin { font-style: italic; padding-left: 0.8rem; border-left: 2px solid var(--filet); }
	.indulgence { font-size: 0.8rem; color: var(--encre-douce); margin: 1rem 0 0.4rem; }
	.ind { font-variant: small-caps; letter-spacing: 0.05em; }
	.source { margin: 0.2rem 0 0 0.6rem; overflow-wrap: anywhere; }
	.actions { margin-top: 1rem; }
	.corbeille { padding: 0.6rem 0.8rem; border: 1px dashed var(--rubrique); border-radius: 0.5rem; }
	.historique { margin-top: 1.4rem; }
	.version { padding: 0.5rem 0; border-bottom: 1px solid var(--filet); }
</style>
