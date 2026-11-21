<script lang="ts">
	import { page } from '$app/state';
	import { iso } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import Office from '#lib/Office.svelte';
	import { heuresDeLaLecture } from '#lib/programme/lectures.ts';
	import { journeeVivante } from '#lib/programme/vivant.svelte.ts';
	import type { Coche } from '#lib/types.ts';
	import { vivantSelon } from '#lib/vivant.svelte.ts';

	/**
	 * Lecture › Office (REFONTE § 4.4) : le bréviaire du jour, une heure à la fois. Le Petit bréviaire du Sacré-Cœur est
	 * l'office compté dans « Lectures du jour » ; le Bréviaire romain et l'Officium parvum viendront dans le même cadre.
	 */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const q = $derived(page.url.searchParams.get('date') ? `?date=${date}` : '');
	const vie = journeeVivante(() => date);
	const lecture = $derived(vie.jr?.lectures.find((l) => l.id === 'lec:office'));
	const texte = $derived.by(() => {
		const id = lecture?.sections.find((s) => s.texte)?.texte;
		return id ? vie.textes.get(id) : undefined;
	});
	const heures = $derived(lecture ? heuresDeLaLecture(lecture, vie.corps) : []);
	const cochesDuJour = vivantSelon(() => {
		const k = date;
		return () => db.coches.where('date').equals(k).toArray();
	}, [] as Coche[]);
	const coches = $derived.by(() => {
		const n: Record<string, number> = {};
		for (const c of cochesDuJour.v) n[c.elementId] = (n[c.elementId] ?? 0) + 1;
		return n;
	});
	const BREVIAIRES = [
		{ cle: 'sacre-coeur', nom: 'Petit bréviaire du Sacré-Cœur' },
		{ cle: 'romain', nom: 'Bréviaire romain' },
		{ cle: 'parvum', nom: 'Officium parvum' }
	] as const;
	let breviaire = $state<(typeof BREVIAIRES)[number]['cle']>('sacre-coeur');
	const jourFr = $derived(new Date(date + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' }));
</script>

<svelte:head><title>Office — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour" href="/lecture{q}"><Icone nom="retour" taille={16} /> Lecture</a>
	<div class="tete-page">
		<p class="etiquette">Office · {jourFr}</p>
		<h1>{BREVIAIRES.find((b) => b.cle === breviaire)?.nom}</h1>
		<Ornement nom="fleuron" />
	</div>

	<div class="breviaires" role="group" aria-label="Bréviaire">
		{#each BREVIAIRES as b (b.cle)}
			<button class="brut" aria-pressed={breviaire === b.cle} onclick={() => (breviaire = b.cle)}>{b.nom}</button>
		{/each}
	</div>

	{#if breviaire === 'sacre-coeur'}
		{#if texte && heures.length}
			<p class="petit">{texte.titre.replace('Petit bréviaire du Sacré-Cœur — ', '')}</p>
			<Office corps={texte.corps} {heures} ligne="lec:office" {date} {coches} />
			<p class="source"><a href="/prieres/{encodeURIComponent(texte.id)}">L’office entier, sa source</a></p>
		{:else if vie.jr}
			<p class="aide">L’office du jour n’est pas dans la bibliothèque.</p>
		{:else}
			<p class="aide">Préparation de l’office…</p>
		{/if}
	{:else if breviaire === 'romain'}
		<p>
			Les heures complètes, selon les rubriques d’avant 1955, sont en préparation (latin seul, d’après Divinum Officium). En attendant : <a
				href="/saint{q}">les leçons du jour et la vie du saint</a
			>.
		</p>
	{:else}
		<p>L’Officium parvum de la sainte Vierge est en préparation ; il s’affichera ici, une heure à la fois.</p>
	{/if}
</main>

<style>
	.retour {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		text-decoration: none;
		font-family: var(--hs-interface);
		font-size: var(--hs-t0);
	}
	.breviaires {
		display: flex;
		flex-wrap: wrap;
		gap: 4px 14px;
		margin: var(--hs-e3) 0;
		font-family: var(--hs-interface);
		font-size: var(--hs-t0);
	}
	.breviaires button {
		padding: 6px 0;
		min-height: 36px;
		background: none;
		border: 0;
		border-bottom: 1px solid transparent;
		color: var(--hs-encre-douce);
		cursor: pointer;
	}
	.breviaires button[aria-pressed='true'] {
		color: var(--hs-encre);
		border-bottom-color: currentColor;
	}
	.source {
		text-align: right;
		font-size: 0.875rem;
	}
</style>
