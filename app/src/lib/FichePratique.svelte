<script lang="ts">
	import { db } from './db.ts';
	import { vivant } from './live.ts';
	import { sansAccents } from './markup.ts';
	import { regleEnClair } from './pratiques.ts';
	import type { Pratique, Rang, Regle, Texte, TypePratique } from './types.ts';
	import { rangPratique, RANGS } from './rangs.ts';

	/** Formulaire d'une pratique : type, règle de dates, prières liées, promesses, indulgence, source. */
	let { pratique = $bindable() }: { pratique: Pratique } = $props();

	const textes = vivant(() => db.textes.orderBy('ordre').toArray(), [] as Texte[]);
	const titres = $derived(Object.fromEntries($textes.map((t) => [t.id, t.titre])));
	let recherche = $state('');
	const trouves = $derived.by(() => {
		const q = sansAccents(recherche.trim());
		if (q.length < 2) return [];
		return $textes.filter((t) => !t.supprimeLe && !pratique.textes.includes(t.id) && sansAccents(t.titre).includes(q)).slice(0, 6);
	});

	const TYPES: [TypePratique, string][] = [
		['jours_comptes', 'Dévotion à jours comptés'],
		['neuvaine', 'Neuvaine'],
		['trentain', 'Trentain'],
		['consecration', 'Consécration'],
		['mois', 'Dévotion du mois'],
		['jour_semaine', 'Dévotion du jour de la semaine']
	];
	const GENRES: [Regle['genre'], string][] = [
		['consecutifs', 'Des jours de suite, à partir d’une date'],
		['avant_fete', 'Les jours qui précèdent une fête'],
		['mensuel', 'Un jour de chaque mois (premier vendredi…)'],
		['fixe', 'Un jour fixe chaque année'],
		['mois_entier', 'Tous les jours d’un mois'],
		['hebdomadaire', 'Un jour de chaque semaine']
	];
	const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
	const MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
	const aujourdhui = new Date().toLocaleDateString('sv');

	/** Change de genre de règle en gardant ce qui peut l'être. */
	function changerGenre(g: Regle['genre']) {
		const r = pratique.regle as Record<string, unknown>;
		const nombre = (r.nombre as number) || 9;
		const jourSemaine = (r.jourSemaine as number | null) ?? null;
		const mois = (r.mois as number) || new Date().getMonth() + 1;
		const jour = (r.jour as number) || 1;
		const debut = (r.debut as string) || aujourdhui;
		pratique.regle =
			g === 'consecutifs'
				? { genre: g, nombre, jourSemaine, debut }
				: g === 'avant_fete'
					? { genre: g, nombre, jourSemaine, mois, jour }
					: g === 'mensuel'
						? { genre: g, rang: 1, jourSemaine: jourSemaine ?? 5 }
						: g === 'fixe'
							? { genre: g, mois, jour }
							: g === 'mois_entier'
								? { genre: g, mois }
								: g === 'roue'
									? { genre: g, unite: 'jour' }
									: { genre: g, jourSemaine: jourSemaine ?? 0 };
	}
	/** « chaque jour » (null) ou un jour de la semaine. */
	const lireJour = (v: string) => (v === '' ? null : Number(v));
</script>

<label><span>Titre</span><input type="text" bind:value={pratique.titre} /></label>
<label>
	<span>Genre de pratique</span>
	<select bind:value={pratique.type}>
		{#each TYPES as [v, n]}<option value={v}>{n}</option>{/each}
	</select>
</label>
<label>
	<span>Rang</span>
	<select bind:value={() => rangPratique(pratique), (v: Rang) => (pratique.rang = v)}>
		{#each RANGS as r}<option value={r.cle} title={r.aide}>{r.latin} ({r.fr})</option>{/each}
	</select>
</label>

<fieldset>
	<legend>Quand</legend>
	<label>
		<span>Règle</span>
		<select value={pratique.regle.genre} onchange={(e) => changerGenre(e.currentTarget.value as Regle['genre'])}>
			{#each GENRES as [v, n]}<option value={v}>{n}</option>{/each}
		</select>
	</label>

	{#if pratique.regle.genre === 'consecutifs' || pratique.regle.genre === 'avant_fete'}
		{@const r = pratique.regle}
		<div class="deux">
			<label><span>Combien</span><input type="number" min="1" max="366" bind:value={r.nombre} /></label>
			<label>
				<span>Lesquels</span>
				<select
					value={r.jourSemaine === null ? '' : String(r.jourSemaine)}
					onchange={(e) => (r.jourSemaine = lireJour(e.currentTarget.value))}
				>
					<option value="">tous les jours</option>
					{#each JOURS as j, i}<option value={String(i)}>les {j}s</option>{/each}
				</select>
			</label>
		</div>
	{/if}
	{#if pratique.regle.genre === 'consecutifs'}
		<label><span>À partir du</span><input type="date" bind:value={pratique.regle.debut} /></label>
	{/if}
	{#if pratique.regle.genre === 'avant_fete' || pratique.regle.genre === 'fixe'}
		{@const r = pratique.regle}
		<div class="deux">
			<label><span>{r.genre === 'fixe' ? 'Le' : 'Avant le'}</span><input type="number" min="1" max="31" bind:value={r.jour} /></label>
			<label>
				<span>Mois</span>
				<select bind:value={r.mois}
					>{#each MOIS as m, i}<option value={i + 1}>{m}</option>{/each}</select
				>
			</label>
		</div>
	{/if}
	{#if pratique.regle.genre === 'mensuel'}
		{@const r = pratique.regle}
		<div class="deux">
			<label>
				<span>Rang dans le mois</span>
				<select bind:value={r.rang}>
					{#each ['premier', 'deuxième', 'troisième', 'quatrième'] as n, i}<option value={i + 1}>{n}</option>{/each}
				</select>
			</label>
			<label>
				<span>Jour</span>
				<select bind:value={r.jourSemaine}
					>{#each JOURS as j, i}<option value={i}>{j}</option>{/each}</select
				>
			</label>
		</div>
		<div class="deux">
			<label><span>Mois de suite (vide : sans fin)</span><input type="number" min="1" max="60" bind:value={r.nombre} /></label>
			<label><span>À partir du</span><input type="date" bind:value={r.debut} /></label>
		</div>
		<label class="case"
			><input type="checkbox" checked={r.decalage === -1} onchange={(e) => (r.decalage = e.currentTarget.checked ? -1 : 0)} /> La veille de ce
			jour</label
		>
	{/if}
	{#if pratique.regle.genre === 'mois_entier'}
		<label>
			<span>Mois</span>
			<select bind:value={pratique.regle.mois}
				>{#each MOIS as m, i}<option value={i + 1}>{m}</option>{/each}</select
			>
		</label>
	{/if}
	{#if pratique.regle.genre === 'hebdomadaire'}
		<label>
			<span>Jour</span>
			<select bind:value={pratique.regle.jourSemaine}
				>{#each JOURS as j, i}<option value={i}>{j}</option>{/each}</select
			>
		</label>
	{/if}
	<p class="clair">{regleEnClair(pratique.regle)}</p>
</fieldset>

<fieldset>
	<legend>Prières liées</legend>
	{#each pratique.textes as id}
		<div class="liee">
			<span>{titres[id] ?? 'Prière introuvable'}</span>
			<button
				class="brut"
				type="button"
				aria-label="Retirer cette prière"
				onclick={() => (pratique.textes = pratique.textes.filter((x) => x !== id))}>×</button
			>
		</div>
	{/each}
	<input type="search" placeholder="Chercher une prière à lier" bind:value={recherche} aria-label="Chercher une prière à lier" />
	{#each trouves as t}
		<button
			class="trouve brut"
			type="button"
			onclick={() => {
				pratique.textes = [...pratique.textes, t.id];
				recherche = '';
			}}
		>
			{t.titre} <span class="petit">{t.partie}</span>
		</button>
	{/each}
</fieldset>

<label><span>Intention ou notes</span><textarea rows="2" bind:value={pratique.notes}></textarea></label>
<label><span>Promesses (seulement d’une source sûre)</span><textarea rows="3" bind:value={pratique.promesses}></textarea></label>
<label><span>Indulgence</span><textarea rows="2" bind:value={pratique.indulgence}></textarea></label>

<fieldset>
	<legend>Source</legend>
	<label><span>Ouvrage</span><input type="text" bind:value={pratique.source.ouvrage} /></label>
	<div class="deux">
		<label><span>Édition</span><input type="text" bind:value={pratique.source.edition} /></label>
		<label><span>Page ou numéro</span><input type="text" bind:value={pratique.source.page} /></label>
	</div>
</fieldset>

<style>
	label,
	fieldset {
		margin-top: var(--hs-e4);
	}
	.deux {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--hs-e4);
	}
	input[type='date'] {
		width: 100%;
		padding: 9px 2px;
		font: inherit;
		color: var(--hs-encre);
		background: transparent;
		border: 0;
		border-bottom: var(--hs-trait) solid var(--hs-filet);
	}
	.case {
		display: flex;
		gap: 8px;
		align-items: baseline;
		font-size: 1rem;
	}
	.clair {
		margin: var(--hs-e4) 0 0;
		font-style: italic;
		color: var(--hs-rubrique);
	}
	.liee {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 8px;
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
		padding: 2px 0;
	}
	.liee button {
		width: 32px;
		height: 32px;
		background: none;
		border: 0;
		cursor: pointer;
		color: var(--hs-rubrique);
		font-size: 1.125rem;
	}
	.trouve {
		display: block;
		width: 100%;
		text-align: left;
		background: none;
		border: 0;
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
		padding: 8px 0;
		cursor: pointer;
		color: var(--hs-lapis);
	}
</style>
