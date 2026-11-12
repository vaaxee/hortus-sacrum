<script lang="ts">
	import Badge from '#lib/Badge.svelte';
	import { db } from '#lib/db.ts';
	import { vivant } from '#lib/live.ts';
	import { nu, sansAccents } from '#lib/markup.ts';
	import type { Texte } from '#lib/types.ts';

	const textes = vivant(() => db.textes.orderBy('ordre').toArray(), [] as Texte[]);
	let recherche = $state('');
	let filtre: 'tous' | 'favoris' | 'personnel' = $state('tous');
	const filtres: ['tous' | 'favoris' | 'personnel', string][] = [
		['tous', 'Toutes'],
		['favoris', 'Favoris'],
		['personnel', 'Mes ajouts']
	];

	const visibles = $derived.by(() => {
		const q = sansAccents(recherche.trim());
		return $textes.filter((t) => {
			if (t.supprimeLe) return false;
			if (filtre === 'favoris' && !t.favori) return false;
			if (filtre === 'personnel' && t.origine !== 'personnel') return false;
			if (!q) return true;
			return sansAccents(`${t.titre} ${t.usage} ${nu(t.corps)} ${t.latin}`).includes(q);
		});
	});
	const groupes = $derived.by(() => {
		const g = new Map<string, Texte[]>();
		for (const t of visibles) {
			const k = t.partie || 'Sans partie';
			g.set(k, [...(g.get(k) ?? []), t]);
		}
		return [...g.entries()];
	});
</script>

<svelte:head><title>Prières — Hebdomada</title></svelte:head>

<main class="page">
	<div class="rangee">
		<h1>Prières</h1>
		<span class="espace"></span>
		<a class="bouton principal" href="/prieres/nouveau">Ajouter</a>
	</div>

	<div class="barre">
		<input type="search" placeholder="Chercher un titre, un mot…" bind:value={recherche} aria-label="Chercher une prière" />
		<div class="rangee" role="group" aria-label="Filtre">
			{#each filtres as [v, nom]}
				<button type="button" aria-pressed={filtre === v} onclick={() => (filtre = v)}>{nom}</button>
			{/each}
			<span class="petit">{visibles.length} pièce{visibles.length > 1 ? 's' : ''}</span>
		</div>
	</div>

	{#each groupes as [partie, liste]}
		<section>
			<h2>{partie}</h2>
			<ul>
				{#each liste as t (t.id)}
					<li>
						<a href="/prieres/{encodeURIComponent(t.id)}">
							<span class="titre">{t.favori ? '★ ' : ''}{t.titre}</span>
							{#if t.usage}<span class="petit">usage : {t.usage}</span>{/if}
						</a>
						<Badge objet={t} />
					</li>
				{/each}
			</ul>
		</section>
	{:else}
		<p class="petit vide">Aucune prière ne correspond.</p>
	{/each}
</main>

<style>
	.barre { display: grid; gap: 0.6rem; margin: 1rem 0 0.5rem; }
	.barre button[aria-pressed='true'] { border-color: var(--rubrique); color: var(--rubrique); }
	section { margin-top: 1.6rem; }
	ul { list-style: none; margin: 0.4rem 0 0; padding: 0; }
	li { display: flex; align-items: center; gap: 0.6rem; border-bottom: 1px solid var(--filet); }
	li a { flex: 1; min-width: 0; display: grid; padding: 0.6rem 0; text-decoration: none; }
	.titre { overflow-wrap: anywhere; }
	.vide { margin-top: 2rem; }
</style>
