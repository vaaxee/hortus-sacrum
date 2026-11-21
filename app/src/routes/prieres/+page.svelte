<script lang="ts">
	import Badge from '#lib/Badge.svelte';
	import { db } from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { dimensionsEffectives } from '#lib/dimensions.ts';
	import { TYPES, typesDe } from '#lib/etiquettes.ts';
	import { vivant } from '#lib/live.ts';
	import { nu, sansAccents } from '#lib/markup.ts';
	import { partieDe, rangDeLaPartie } from '#lib/parties.ts';
	import { chargerClassements, chargerVocabulaire } from '#lib/programme/dimensions.ts';
	import type { ClassementTexte, Vocabulaire } from '#lib/programme/types.ts';
	import type { Texte } from '#lib/types.ts';

	/**
	 * Prières (REFONTE § 4.5) : recherche ; filtres par thème (objets) et par type (forme), corrigeables dans la fiche de
	 * chaque prière ; parties repliées, avec leur nombre, rendues seulement une fois ouvertes.
	 */
	const textes = vivant(() => db.textes.orderBy('ordre').toArray(), [] as Texte[]);
	let vocabulaire = $state.raw<Vocabulaire | null>(null);
	let classements = $state.raw<Record<string, ClassementTexte> | null>(null);
	chargerVocabulaire().then((v) => (vocabulaire = v));
	chargerClassements().then((c) => (classements = c));

	let recherche = $state('');
	let filtre: 'tous' | 'favoris' | 'personnel' = $state('tous');
	const filtres: ['tous' | 'favoris' | 'personnel', string][] = [
		['tous', 'Toutes'],
		['favoris', 'Favoris'],
		['personnel', 'Mes ajouts']
	];
	const THEMES = [
		'trinite',
		'jesus-christ',
		'eucharistie',
		'sacre-coeur',
		'passion',
		'sainte-vierge',
		'saint-joseph',
		'anges',
		'saints',
		'ames-du-purgatoire',
		'sainte-face'
	];
	let theme = $state<string | null>(null);
	let type = $state<string | null>(null);

	/** Thèmes et types de chaque prière (dimensions effectives : réglage, relecture, classement livré, motifs). */
	const classement = $derived(
		new Map(
			$textes.map((t) => {
				const e = dimensionsEffectives(t, classements?.[t.id]);
				const forme = e.devinees.has('forme') ? undefined : e.valeurs.forme;
				return [t.id, { objets: new Set(e.valeurs.objet ?? []), types: new Set(typesDe(t, forme)) }];
			})
		)
	);

	const visibles = $derived.by(() => {
		const q = sansAccents(recherche.trim());
		return $textes.filter((t) => {
			if (t.supprimeLe) return false;
			if (filtre === 'favoris' && !t.favori) return false;
			if (filtre === 'personnel' && t.origine !== 'personnel') return false;
			const c = classement.get(t.id);
			if (theme && !c?.objets.has(theme)) return false;
			if (type && !c?.types.has(type)) return false;
			if (!q) return true;
			return sansAccents(`${t.titre} ${t.usage} ${nu(t.corps)} ${t.latin}`).includes(q);
		});
	});
	const groupes = $derived.by(() => {
		const g = new Map<string, Texte[]>();
		for (const t of visibles) {
			const k = partieDe(t);
			g.set(k, [...(g.get(k) ?? []), t]);
		}
		return [...g.entries()].sort((a, b) => rangDeLaPartie(a[0]) - rangDeLaPartie(b[0]) || a[0].localeCompare(b[0]));
	});
	/** Une recherche ou un filtre ouvre les parties ; sinon elles sont repliées et ne s'ouvrent qu'au toucher. */
	const tout = $derived(!!recherche.trim() || !!theme || !!type || filtre !== 'tous');
	let ouvertes = $state<Record<string, boolean>>({});
	const ouverte = (p: string) => tout || !!ouvertes[p];
	const vide = $derived(
		(filtre as string) === 'favoris'
			? 'Aucun favori pour l’instant. Ouvrez une prière et ajoutez-la aux favoris.'
			: (filtre as string) === 'personnel'
				? 'Vous n’avez encore rien ajouté. « Ajouter une prière » ouvre la saisie.'
				: 'Aucune prière ne répond à cette recherche.'
	);
	const libelleObjet = (v: string) => vocabulaire?.dimensions.objet.valeurs[v] ?? v;
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
			<span class="segments">
				{#each filtres as [v, nom] (v)}
					<button type="button" aria-pressed={filtre === v} onclick={() => (filtre = v)}>{nom}</button>
				{/each}
			</span>
			<span class="espace"></span>
			<a class="bouton principal" href="/prieres/nouveau">Ajouter une prière</a>
		</div>
		<div class="pastilles" role="group" aria-label="Thème">
			<span class="etiquette">Thème</span>
			{#each THEMES as v (v)}
				<button type="button" class="brut puce" aria-pressed={theme === v} onclick={() => (theme = theme === v ? null : v)}
					>{libelleObjet(v)}</button
				>
			{/each}
		</div>
		<div class="pastilles" role="group" aria-label="Type">
			<span class="etiquette">Type</span>
			{#each TYPES as [v, nom] (v)}
				<button type="button" class="brut puce" aria-pressed={type === v} onclick={() => (type = type === v ? null : v)}
					>{nom}</button
				>
			{/each}
		</div>
		<p class="petit compte">
			{visibles.length} prière{visibles.length > 1 ? 's' : ''}{tout ? '' : ` en ${groupes.length} parties`} ; les méditations sont dans
			<a href="/lecture/spirituel">Lecture</a>.
		</p>
	</div>

	{#each groupes as [partie, liste] (partie)}
		<details class="partie" open={ouverte(partie)} ontoggle={(e) => (ouvertes[partie] = e.currentTarget.open)}>
			<summary>
				<span class="nom">{partie}</span>
				<span class="nombre chiffres-alignes">{liste.length}</span>
			</summary>
			{#if ouverte(partie)}
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
			{/if}
		</details>
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
		gap: var(--hs-e3);
	}
	/* une rangée de pastilles qui défile horizontalement, sans élargir la page */
	.pastilles {
		display: flex;
		gap: 6px;
		align-items: center;
		overflow-x: auto;
		padding: 5px 4px;
		margin-inline: -4px;
		scrollbar-width: none;
		/* la rangée s'efface au bord droit : on devine qu'elle continue */
		mask-image: linear-gradient(to right, #000 calc(100% - 28px), transparent);
	}
	.pastilles .etiquette {
		flex: none;
		margin-right: 4px;
	}
	.compte {
		margin: 0;
	}
	.partie {
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
	}
	.partie:first-of-type {
		margin-top: var(--hs-e5);
		border-top: var(--hs-cheveu) solid var(--hs-filet);
	}
	.partie summary {
		display: flex;
		align-items: baseline;
		gap: 12px;
		padding: 12px 0;
		min-height: 44px;
		cursor: pointer;
	}
	.partie .nom {
		flex: 1;
		font-size: 1.125rem;
	}
	.partie .nombre {
		color: var(--hs-encre-douce);
		font-size: 0.875rem;
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
