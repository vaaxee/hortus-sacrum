<script lang="ts">
	import Badge from '#lib/Badge.svelte';
	import { db } from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
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
	const vide = $derived(
		(filtre as string) === 'favoris'
			? 'Aucun favori pour l’instant. Ouvrez une prière et ajoutez-la aux favoris.'
			: (filtre as string) === 'personnel'
				? 'Vous n’avez encore rien ajouté. « Ajouter une prière » ouvre la saisie.'
				: 'Aucune prière ne contient ces mots.'
	);
</script>

<svelte:head><title>Prières — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<h1>Prières</h1>
		<Ornement nom="fleuron" />
	</div>

	<div class="barre">
		<input type="search" placeholder="Chercher un titre, un mot" bind:value={recherche} aria-label="Chercher une prière" />
		<div class="rangee" role="group" aria-label="Filtre">
			{#each filtres as [v, nom]}
				<button type="button" aria-pressed={filtre === v} onclick={() => (filtre = v)}>{nom}</button>
			{/each}
			<span class="espace"></span>
			<a class="bouton" href="/recueils">Méditations</a>
			<a class="bouton principal" href="/prieres/nouveau">Ajouter une prière</a>
		</div>
	</div>

	{#each groupes as [partie, liste]}
		<section>
			<div class="tete-section">
				<Ornement nom="grecque" />
				<h2>{partie}</h2>
			</div>
			<ul class="reglee">
				{#each liste as t (t.id)}
					<li>
						<a href="/prieres/{encodeURIComponent(t.id)}">
							<span class="titre">
								{#if t.favori}<span class="etoile" title="Favori"><Icone nom="etoile" taille={14} /></span>{/if}{t.titre}
							</span>
							{#if t.usage}<span class="usage"><span class="pc">usage :</span> <em>{t.usage}</em></span>{/if}
						</a>
						<Badge objet={t} />
					</li>
				{/each}
			</ul>
		</section>
	{:else}
		<p class="petit vide">{vide}</p>
	{/each}
</main>

<style>
	.tete-page :global(.filet) {
		max-width: 16rem;
	}
	.barre {
		display: grid;
		gap: var(--hs-e4);
	}
	.barre button {
		min-height: 36px;
	}
	li a {
		flex: 1;
		min-width: 0;
		display: grid;
		padding: 10px 0;
		text-decoration: none;
		color: var(--hs-encre);
	}
	.titre {
		overflow-wrap: anywhere;
		line-height: 1.3;
	}
	.etoile {
		color: var(--hs-or);
		margin-right: 6px;
		vertical-align: -1px;
	}
	.usage {
		font-size: 1rem;
		color: var(--hs-encre-douce);
		line-height: 1.35;
	}
	.usage .pc {
		color: var(--hs-rubrique);
	}
	.vide {
		margin-top: var(--hs-e6);
		text-align: center;
	}
</style>
