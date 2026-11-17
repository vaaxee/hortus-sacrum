<script lang="ts">
	import { page } from '$app/state';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { rendre } from '#lib/markup.ts';
	import { chargerRecueil, type Recueil } from '#lib/meditations.ts';

	/** Bibliothèque des méditations : chaque recueil, sa table, et la lecture d'une entrée. */
	const RECUEILS: [string, string][] = [
		['hamon', 'Hamon — Méditations pour tous les jours de l’année'],
		['chaignon', 'Chaignon — La méditation, ou le fidèle sanctifié'],
		['mois-joseph', 'Lefebvre — Mois de saint Joseph (mars)'],
		['mois-marie', 'Lefebvre — Mois de Marie (mai)'],
		['mois-sacre-coeur', 'Lefebvre — Mois du Sacré-Cœur (juin)'],
		['mois-precieux-sang', 'Boylesve — Mois du Précieux Sang (juillet)'],
		['mois-purgatoire', 'Berlioux — Mois des âmes du purgatoire (novembre)'],
		['breviaire', 'Bréviaire romain — leçons du IIe nocturne'],
		['liguori-visites', 'S. Alphonse de Liguori — Visites au Saint-Sacrement et à la sainte Vierge (chaque jour du mois)']
	];
	const id = $derived(page.url.searchParams.get('r'));
	const n = $derived(page.url.searchParams.get('n'));
	let recueil = $state<Recueil | null>(null);
	let filtre = $state('');
	$effect(() => {
		const r = id;
		recueil = null;
		if (r) chargerRecueil(n === null ? `index/${r}` : r).then((x) => (recueil = x));
	});
	const entree = $derived(recueil && n !== null ? recueil.entrees[Number(n)] : undefined);
	const sansAccent = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
	const liste = $derived(
		(recueil?.entrees ?? []).map((e, i) => ({ e, i })).filter(({ e }) => !filtre || sansAccent(e.titre).includes(sansAccent(filtre)))
	);
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
			La méditation du jour est choisie d’elle-même (ligne « Méditation du jour » de la liste). Ici, on peut lire n’importe quel recueil.
		</p>
		<ul class="recueils">
			{#each RECUEILS as [r, nom]}<li><a href="/recueils?r={r}">{nom}</a></li>{/each}
		</ul>
	{:else if n === null}
		<a class="retour interface" href="/recueils"><Icone nom="retour" taille={16} /> Méditations</a>
		<div class="tete-page"><h1>{RECUEILS.find(([r]) => r === id)?.[1] ?? id}</h1></div>
		<input type="search" placeholder="Chercher un titre" bind:value={filtre} aria-label="Chercher un titre" />
		<ol class="table">
			{#each liste as { e, i }}<li>
					<a href="/recueils?r={id}&n={i}">{e.titre || '(sans titre)'}</a>{#if e.tome}<span class="petit">
							t. {e.tome}{e.page ? `, p. ${e.page}` : ''}</span
						>{/if}
				</li>{/each}
		</ol>
	{:else if entree}
		<a class="retour interface" href="/recueils?r={id}"><Icone nom="retour" taille={16} /> Table</a>
		<div class="tete-page">
			<h1>{entree.titre}</h1>
			<Ornement nom="fleuron" />
		</div>
		{#if entree.sommaire}<details class="sommaire">
				<summary class="pc">Sommaire pour la veille au soir</summary>
				<div class="lecture">{@html rendre(entree.sommaire)}</div>
			</details>{/if}
		<div class="lecture">{@html rendre(entree.corps)}</div>
		<p class="petit source">
			{recueil?.auteur}, <em>{recueil?.titre}</em>{#if entree.tome}, t. {entree.tome}{/if}{#if entree.page}, p. {entree.page}{/if}. {recueil?.provenance}.
		</p>
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
</style>
