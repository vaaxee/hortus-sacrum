<script lang="ts">
	import { page } from '$app/state';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { db } from '#lib/db.ts';
	import { rendre } from '#lib/markup.ts';
	import { chargerRecueil, type Recueil } from '#lib/meditations.ts';
	import {
		avecSurcharges,
		corrigerEntree,
		estLivre,
		masquerRecueil,
		RECUEILS_LIVRES,
		recueilsMasques,
		recueilsPerso,
		retablirEntree,
		toutesLesMeditations,
		versRecueil
	} from '#lib/recueils-perso.ts';
	import type { Recueil as RecueilPerso } from '#lib/types.ts';

	/**
	 * Bibliothèque des méditations : recueils livrés et recueils de l'utilisateur, leur table, la lecture d'une entrée.
	 * Éditeur (lot 11) : ajouter un recueil (/recueils/editer), corriger une entrée livrée (surcharge locale, le fichier
	 * livré n'est jamais touché), masquer un recueil livré.
	 */
	const id = $derived(page.url.searchParams.get('r'));
	const n = $derived(page.url.searchParams.get('n'));
	let version = $state(0);
	let recueil = $state<Recueil | null>(null);
	let perso = $state<RecueilPerso[]>([]);
	let masques = $state<string[]>([]);
	let filtre = $state('');
	$effect(() => {
		void version;
		Promise.all([recueilsPerso(), recueilsMasques()]).then(([p, m]) => {
			perso = p;
			masques = m;
		});
	});
	$effect(() => {
		const r = id,
			k = n;
		void version;
		recueil = null;
		if (!r) return;
		(async () => {
			const meds = await toutesLesMeditations();
			if (estLivre(r)) {
				const x = await chargerRecueil(k === null ? `index/${r}` : r);
				recueil = x && avecSurcharges(x, meds);
			} else {
				const p = await db.recueils.get(r);
				recueil = p && !p.supprimeLe ? versRecueil(p, meds) : null;
			}
		})();
	});
	const livre = $derived(!!id && estLivre(id));
	const nom = $derived(id ? (RECUEILS_LIVRES.find(([r]) => r === id)?.[1] ?? recueil?.titre ?? '') : '');
	const entree = $derived(recueil && n !== null ? recueil.entrees[Number(n)] : undefined);
	const sansAccent = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
	const liste = $derived(
		(recueil?.entrees ?? []).map((e, i) => ({ e, i })).filter(({ e }) => !filtre || sansAccent(e.titre).includes(sansAccent(filtre)))
	);

	// correction d'une entrée livrée
	let edition = $state<{ titre: string; corps: string; pratique: string } | null>(null);
	$effect(() => {
		void entree;
		edition = null;
	});
	async function corriger() {
		if (!id || n === null || !edition) return;
		const brut = await chargerRecueil(id);
		const origine = brut?.entrees[Number(n)];
		if (!origine) return;
		await corrigerEntree(id, Number(n), origine, edition);
		edition = null;
		version++;
	}
	async function retablir() {
		if (!id || n === null) return;
		await retablirEntree(id, Number(n));
		version++;
	}
	async function basculer(r: string, masquer: boolean) {
		await masquerRecueil(r, masquer);
		version++;
	}
</script>

<svelte:head><title>Méditations — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	{#if !id}
		<a class="retour interface" href="/prieres"><Icone nom="retour" taille={16} /> Prières</a>
		<div class="tete-page">
			<h1>Méditations</h1>
			<Ornement nom="fleuron" />
		</div>
		<p class="petit">
			La méditation du jour est choisie d’elle-même (ligne « Méditation du jour » de la liste). Ici, on peut lire n’importe quel recueil, en
			ajouter un, ou corriger une entrée.
		</p>
		<ul class="recueils">
			{#each RECUEILS_LIVRES.filter(([r]) => !masques.includes(r)) as [r, titre] (r)}
				<li>
					<a href="/recueils?r={r}">{titre}</a>
					<button class="brut petit masquer" onclick={() => basculer(r, true)} aria-label="Masquer {titre}">masquer</button>
				</li>
			{/each}
		</ul>
		<h2 class="pc">Mes recueils</h2>
		{#if perso.length}
			<ul class="recueils">
				{#each perso as r (r.id)}
					<li>
						<a href="/recueils?r={r.id}">{r.titre}</a>{#if r.auteur}<span class="petit"> — {r.auteur}</span>{/if}
						<a class="petit modifier" href="/recueils/editer?id={r.id}">modifier</a>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="petit">Aucun recueil ajouté.</p>
		{/if}
		<p><a class="bouton" href="/recueils/editer">Ajouter un recueil</a></p>
		{#if masques.length}
			<details class="masques">
				<summary class="petit">Recueils masqués ({masques.length})</summary>
				<ul class="recueils">
					{#each RECUEILS_LIVRES.filter(([r]) => masques.includes(r)) as [r, titre] (r)}
						<li>{titre} <button class="brut petit masquer" onclick={() => basculer(r, false)}>afficher</button></li>
					{/each}
				</ul>
			</details>
		{/if}
	{:else if n === null}
		<a class="retour interface" href="/recueils"><Icone nom="retour" taille={16} /> Méditations</a>
		<div class="tete-page"><h1>{nom || id}</h1></div>
		{#if !livre && recueil}<p><a class="petit" href="/recueils/editer?id={id}">Modifier ce recueil</a></p>{/if}
		<input type="search" placeholder="Chercher un titre" bind:value={filtre} aria-label="Chercher un titre" />
		<ol class="table">
			{#each liste as { e, i } (i)}<li>
					<a href="/recueils?r={id}&n={i}">{e.titre || '(sans titre)'}</a>{#if e.tome}<span class="petit">
							t. {e.tome}{e.page ? `, p. ${e.page}` : ''}</span
						>{/if}{#if e.corrige}<span class="petit"> · corrigée</span>{/if}
				</li>{/each}
		</ol>
	{:else if entree}
		<a class="retour interface" href="/recueils?r={id}"><Icone nom="retour" taille={16} /> Table</a>
		<div class="tete-page">
			<h1>{entree.titre}</h1>
			<Ornement nom="fleuron" />
		</div>
		{#if edition}
			<form
				class="edition"
				onsubmit={(ev) => {
					ev.preventDefault();
					corriger();
				}}
			>
				<p class="petit">
					La correction reste sur vos appareils ; le texte livré n’est pas modifié et peut être rétabli. Recopier le texte de l’édition
					ancienne, sans le réécrire.
				</p>
				<label>Titre <input bind:value={edition.titre} /></label>
				<label>Texte <textarea rows="16" bind:value={edition.corps}></textarea></label>
				<label>Pratique ou résolution <textarea rows="3" bind:value={edition.pratique}></textarea></label>
				<div class="actions">
					<button class="bouton" type="submit">Enregistrer la correction</button>
					<button class="brut" type="button" onclick={() => (edition = null)}>Annuler</button>
				</div>
			</form>
		{:else}
			{#if entree.sommaire}<details class="sommaire">
					<summary class="pc">Sommaire pour la veille au soir</summary>
					<div class="lecture">{@html rendre(entree.sommaire)}</div>
				</details>{/if}
			<div class="lecture">{@html rendre(entree.corps)}</div>
			{#if entree.pratique}
				<h2 class="pc">Pratique</h2>
				<div class="lecture">{@html rendre(entree.pratique)}</div>
			{/if}
			<p class="petit source">
				{recueil?.auteur}, <em>{recueil?.titre}</em>{#if entree.tome}, t. {entree.tome}{/if}{#if entree.page}, p. {entree.page}{/if}. {recueil?.provenance}.
			</p>
			{#if livre}
				<p class="interface actions">
					<button
						class="brut petit"
						onclick={() => (edition = { titre: entree.titre, corps: entree.corps, pratique: entree.pratique ?? '' })}
						>Corriger cette entrée</button
					>
					{#if entree.corrige}<span class="petit">Corrigée par vous.</span>
						<button class="brut petit" onclick={retablir}>Rétablir le texte livré</button>{/if}
				</p>
			{/if}
		{/if}
		<nav class="suite interface">
			{#if Number(n) > 0}<a href="/recueils?r={id}&n={Number(n) - 1}">‹ précédente</a>{/if}
			{#if recueil && Number(n) < recueil.entrees.length - 1}<a href="/recueils?r={id}&n={Number(n) + 1}">suivante ›</a>{/if}
		</nav>
	{/if}
</main>

<style>
	.retour {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		text-decoration: none;
		color: var(--hs-encre-douce);
		min-height: 44px;
	}
	.recueils,
	.table {
		padding-left: 1.2rem;
	}
	.recueils li,
	.table li {
		margin: 0.5rem 0;
	}
	.lecture :global(p) {
		text-align: justify;
		hyphens: auto;
	}
	.lecture :global(h2) {
		text-align: center;
		font-variant: small-caps;
		letter-spacing: 0.04em;
		font-size: 1.15rem;
	}
	.sommaire {
		border-block: var(--hs-cheveu) solid var(--hs-filet);
		margin-bottom: var(--hs-e5);
	}
	.sommaire summary {
		padding: 10px 0;
		color: var(--hs-encre-douce);
		cursor: pointer;
	}
	.source {
		margin-top: var(--hs-e6);
		color: var(--hs-encre-douce);
	}
	.suite {
		display: flex;
		justify-content: space-between;
		margin-top: var(--hs-e5);
	}
	input[type='search'] {
		width: 100%;
		margin: var(--hs-e3) 0;
	}
	.masquer,
	.modifier {
		margin-left: var(--hs-e2);
		color: var(--hs-encre-douce);
	}
	.masques {
		margin-top: var(--hs-e5);
	}
	.edition {
		display: grid;
		gap: var(--hs-e3);
	}
	.edition label {
		display: grid;
		gap: var(--hs-e1, 4px);
	}
	.edition input,
	.edition textarea {
		width: 100%;
		font: inherit;
	}
	.actions {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--hs-e3);
	}
</style>
