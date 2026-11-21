<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { db } from '#lib/db.ts';
	import { nettoyer } from '#lib/markup.ts';
	import {
		cleValide,
		entreesDepuisTexte,
		GENRES,
		meditationsDe,
		sauverRecueil,
		supprimerRecueil,
		type Affectation
	} from '#lib/recueils-perso.ts';

	/**
	 * Ajouter ou modifier un recueil de méditations (SPEC § 9 ; REFONTE § 6, lot 11) : saisie au clavier, copier-coller
	 * nettoyé (markup.ts › nettoyer) ou fichier texte ; découpage en entrées aux lignes « === Titre » ; affectation du
	 * recueil (mois, temps, fête, neuvaine, libre) et clé de jour de chaque entrée.
	 */
	const id = $derived(page.url.searchParams.get('id'));
	let titre = $state('');
	let auteur = $state('');
	let source = $state({ ouvrage: '', edition: '', page: '', url: '' });
	let affectation = $state<Affectation>({ genre: 'libre', valeur: '' });
	let entrees = $state<{ titre: string; corps: string; pratique: string; cle: string }[]>([]);
	let brut = $state('');
	let rapport = $state<string[]>([]);
	let erreur = $state('');
	let charge = $state(false);

	$effect(() => {
		const r = id;
		if (!r) {
			charge = true;
			return;
		}
		Promise.all([db.recueils.get(r), meditationsDe(r)]).then(([x, meds]) => {
			if (x && !x.supprimeLe) {
				titre = x.titre;
				auteur = x.auteur;
				source = { ...x.source };
				affectation = { ...x.affectation };
				entrees = meds
					.sort((a, b) => a.rang - b.rang)
					.map((m) => ({ titre: m.titre, corps: m.corps, pratique: m.pratique ?? '', cle: m.cle ?? '' }));
			}
			charge = true;
		});
	});

	const aide = $derived(GENRES.find((g) => g.genre === affectation.genre)?.aide ?? '');
	const clesFausses = $derived(entrees.map((e, i) => (cleValide(e.cle.trim()) ? -1 : i)).filter((i) => i >= 0));

	async function lireFichier(ev: Event) {
		const f = (ev.currentTarget as HTMLInputElement).files?.[0];
		if (f) brut = await f.text();
	}
	function nettoyerTexte() {
		const n = nettoyer(brut);
		brut = n.texte;
		rapport = n.rapport;
	}
	function decouperTexte() {
		const e = entreesDepuisTexte(brut);
		if (!e.length) {
			erreur = 'Aucun texte à découper.';
			return;
		}
		erreur = '';
		entrees = [...entrees, ...e];
		brut = '';
		rapport = [];
	}
	function deplacer(i: number, d: -1 | 1) {
		const j = i + d;
		if (j < 0 || j >= entrees.length) return;
		const copie = [...entrees];
		[copie[i], copie[j]] = [copie[j], copie[i]];
		entrees = copie;
	}
	async function enregistrer() {
		erreur = '';
		if (!titre.trim()) return (erreur = 'Le recueil a besoin d’un titre.');
		if (!entrees.length) return (erreur = 'Le recueil n’a encore aucune entrée.');
		if (clesFausses.length) return (erreur = `Clé de jour non reconnue : entrée ${clesFausses.map((i) => i + 1).join(', ')}.`);
		if (affectation.genre === 'mois' && !(Number(affectation.valeur) >= 1 && Number(affectation.valeur) <= 12))
			return (erreur = 'Choisir le mois (1 à 12).');
		const r = await sauverRecueil(
			{
				...(id && { id }),
				titre: titre.trim(),
				auteur: auteur.trim(),
				source: { ...source, ouvrage: source.ouvrage.trim() || titre.trim() },
				affectation: { ...affectation }
			},
			entrees.map((e) => ({ ...e, cle: e.cle.trim() }))
		);
		goto(`/recueils?r=${r}`);
	}
	async function supprimer() {
		if (!id || !confirm('Mettre ce recueil à la corbeille ?')) return;
		await supprimerRecueil(id);
		goto('/recueils');
	}
</script>

<svelte:head><title>{id ? 'Modifier un recueil' : 'Ajouter un recueil'} — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour interface" href={id ? `/recueils?r=${id}` : '/recueils'}><Icone nom="retour" taille={16} /> Méditations</a>
	<div class="tete-page">
		<h1>{id ? 'Modifier le recueil' : 'Ajouter un recueil'}</h1>
		<Ornement nom="fleuron" />
	</div>

	{#if charge}
		<form
			onsubmit={(ev) => {
				ev.preventDefault();
				enregistrer();
			}}
		>
			<fieldset>
				<legend class="pc">Recueil</legend>
				<label>Titre <input bind:value={titre} required /></label>
				<label>Auteur <input bind:value={auteur} /></label>
				<label>Ouvrage <input bind:value={source.ouvrage} placeholder="titre de l’édition, si différent" /></label>
				<label>Édition <input bind:value={source.edition} placeholder="lieu, éditeur, année" /></label>
				<label>Page ou volume <input bind:value={source.page} /></label>
				<label>Lien (archive.org, Gallica…) <input type="url" bind:value={source.url} /></label>
			</fieldset>

			<fieldset>
				<legend class="pc">Affectation</legend>
				<label
					>Le recueil sert pour
					<select bind:value={affectation.genre}>
						{#each GENRES as g (g.genre)}<option value={g.genre}>{g.nom}</option>{/each}
					</select>
				</label>
				{#if affectation.genre === 'mois'}
					<label
						>Mois
						<select bind:value={affectation.valeur}>
							<option value="">—</option>
							{#each ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'] as m, i (m)}
								<option value={String(i + 1)}>{m}</option>
							{/each}
						</select>
					</label>
				{:else if affectation.genre !== 'libre'}
					<label>Lequel <input bind:value={affectation.valeur} /></label>
				{/if}
				<p class="petit">{aide}</p>
			</fieldset>

			<fieldset>
				<legend class="pc">Ajouter des entrées</legend>
				<p class="petit">
					Taper ou coller le texte, ou ouvrir un fichier texte. Une ligne « === Titre » commence une entrée. Le nettoyage recolle les mots
					coupés et les lignes brisées, sans changer les mots.
				</p>
				<label>Fichier texte <input type="file" accept=".txt,text/plain" onchange={lireFichier} /></label>
				<textarea rows="10" bind:value={brut} aria-label="Texte à découper"></textarea>
				<div class="actions">
					<button class="brut" type="button" onclick={nettoyerTexte} disabled={!brut.trim()}>Nettoyer</button>
					<button class="bouton" type="button" onclick={decouperTexte} disabled={!brut.trim()}>Découper en entrées</button>
				</div>
				{#if rapport.length}<ul class="petit">
						{#each rapport as r, i (i)}<li>{r}</li>{/each}
					</ul>{/if}
			</fieldset>

			<fieldset>
				<legend class="pc">Entrées ({entrees.length})</legend>
				<p class="petit">
					Clé de jour (facultative) : « D:12-08 » (date fixe), « T:Adv1-0 » (jour du temporal), « F:sacre-coeur » (fête mobile), « J:5 » (5e
					jour du mois). Dans un recueil affecté à un mois, les entrées sans clé suivent les jours du mois dans l’ordre.
				</p>
				<ol class="entrees">
					{#each entrees as e, i (i)}
						<li>
							<label>Titre <input bind:value={e.titre} /></label>
							<label
								>Clé de jour <input
									bind:value={e.cle}
									aria-invalid={clesFausses.includes(i)}
									placeholder={affectation.genre === 'mois' ? `J:${i + 1}` : ''}
								/></label
							>
							<details>
								<summary class="petit">Texte ({e.corps.length} signes)</summary>
								<textarea rows="10" bind:value={e.corps} aria-label="Texte de l’entrée {i + 1}"></textarea>
							</details>
							<label>Pratique ou résolution <textarea rows="2" bind:value={e.pratique}></textarea></label>
							<div class="actions">
								<button class="brut petit" type="button" onclick={() => deplacer(i, -1)} disabled={i === 0}>monter</button>
								<button class="brut petit" type="button" onclick={() => deplacer(i, 1)} disabled={i === entrees.length - 1}
									>descendre</button
								>
								<button class="brut petit" type="button" onclick={() => (entrees = entrees.filter((_, j) => j !== i))}>retirer</button>
							</div>
						</li>
					{/each}
				</ol>
				<button
					class="brut"
					type="button"
					onclick={() => (entrees = [...entrees, { titre: `Entrée ${entrees.length + 1}`, corps: '', pratique: '', cle: '' }])}
					>Ajouter une entrée vide</button
				>
			</fieldset>

			{#if erreur}<p class="erreur" role="alert">{erreur}</p>{/if}
			<div class="actions">
				<button class="bouton" type="submit">Enregistrer le recueil</button>
				{#if id}<button class="brut" type="button" onclick={supprimer}>Mettre à la corbeille</button>{/if}
			</div>
		</form>
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
	form {
		display: grid;
		gap: var(--hs-e5);
	}
	fieldset {
		display: grid;
		gap: var(--hs-e3);
		border: var(--hs-cheveu) solid var(--hs-filet);
		padding: var(--hs-e4, 16px);
		margin: 0;
		min-width: 0;
	}
	label {
		display: grid;
		gap: 4px;
	}
	input,
	select,
	textarea {
		width: 100%;
		font: inherit;
		box-sizing: border-box;
	}
	input[type='file'] {
		width: auto;
		max-width: 100%;
	}
	.entrees {
		display: grid;
		gap: var(--hs-e4, 16px);
		padding-left: 1.2rem;
		margin: 0;
	}
	.entrees li {
		display: grid;
		gap: var(--hs-e2);
	}
	.actions {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--hs-e3);
	}
	[aria-invalid='true'] {
		outline: 2px solid var(--hs-rubis, #7a1f2b);
	}
	.erreur {
		color: var(--hs-rubis, #7a1f2b);
	}
</style>
