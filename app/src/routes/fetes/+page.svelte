<script lang="ts">
	import Badge from '#lib/Badge.svelte';
	import { creer, db, enregistrer, mettreALaCorbeille, nouvelId, sortirDeLaCorbeille, supprimerDefinitivement } from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import type { FetePerso } from '#lib/types.ts';

	/** Fêtes et saints personnels, anniversaires spirituels (baptême, confirmation, consécrations…). */
	const fetes = vivant(() => db.fetes.toArray(), [] as FetePerso[]);
	const MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
	const GENRES: [FetePerso['genre'], string][] = [
		['anniversaire', 'Anniversaires spirituels'],
		['saint', 'Saints favoris et fête patronale'],
		['fete', 'Fêtes locales et personnelles']
	];
	const EXEMPLES: Record<FetePerso['genre'], string> = {
		anniversaire: 'Baptême, confirmation, première communion, consécration…',
		saint: 'Saint patron, saints aimés : un rappel la veille de leur fête.',
		fete: 'Fête du diocèse, de la paroisse, d’un sanctuaire…'
	};

	const tri = (a: FetePerso, b: FetePerso) => a.mois - b.mois || a.jour - b.jour;
	const visibles = $derived($fetes.filter((f) => !f.supprimeLe).sort(tri));
	const corbeille = $derived($fetes.filter((f) => f.supprimeLe));

	let brouillon: FetePerso | undefined = $state();
	let estNouvelle = $state(false);
	let erreur = $state('');
	let aSupprimer: string | undefined = $state();

	function nouvelle(genre: FetePerso['genre']) {
		const d = new Date();
		brouillon = {
			id: nouvelId(),
			origine: 'personnel',
			titre: '',
			genre,
			mois: d.getMonth() + 1,
			jour: d.getDate(),
			rappelVeille: genre === 'saint',
			notes: '',
			creeLe: '',
			modifieLe: ''
		};
		estNouvelle = true;
		erreur = '';
	}
	function ouvrir(f: FetePerso) {
		brouillon = structuredClone(f);
		estNouvelle = false;
		erreur = '';
	}
	async function sauver() {
		if (!brouillon) return;
		if (!brouillon.titre.trim()) return (erreur = 'Donnez un nom à cette fête ou à cet anniversaire.');
		const max = new Date(2028, brouillon.mois, 0).getDate();
		if (brouillon.jour < 1 || brouillon.jour > max) return (erreur = `Le ${MOIS[brouillon.mois - 1]} compte ${max} jours.`);
		const b = $state.snapshot(brouillon) as FetePerso;
		if (!b.annee) delete b.annee;
		if (estNouvelle) {
			const { creeLe, modifieLe, ...reste } = b;
			await creer<FetePerso>('fetes', reste);
		} else await enregistrer('fetes', b);
		brouillon = undefined;
	}
	const date = (f: FetePerso) => `${f.jour === 1 ? '1er' : f.jour} ${MOIS[f.mois - 1]}${f.annee ? ` ${f.annee}` : ''}`;
</script>

<svelte:head><title>Fêtes et anniversaires — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour" href="/reglages"><Icone nom="retour" taille={16} /> Profil</a>
	<div class="tete-page">
		<h1>Fêtes et anniversaires</h1>
		<Ornement nom="fleuron" />
		<p class="petit">Ils apparaissent sur l’écran Aujourd’hui et dans le calendrier.</p>
	</div>

	{#if brouillon}
		<section class="epreuve formulaire">
			<h2>{estNouvelle ? 'Ajouter' : 'Modifier'}</h2>
			<label><span>Nom</span><input type="text" bind:value={brouillon.titre} placeholder="Mon baptême, saint Louis…" /></label>
			<label>
				<span>Genre</span>
				<select bind:value={brouillon.genre}
					>{#each GENRES as [v, n]}<option value={v}>{n}</option>{/each}</select
				>
			</label>
			<div class="trois">
				<label><span>Jour</span><input type="number" min="1" max="31" bind:value={brouillon.jour} /></label>
				<label
					><span>Mois</span><select bind:value={brouillon.mois}
						>{#each MOIS as m, i}<option value={i + 1}>{m}</option>{/each}</select
					></label
				>
				<label><span>Année (facultatif)</span><input type="number" min="1900" max="2100" bind:value={brouillon.annee} /></label>
			</div>
			<label class="case"><input type="checkbox" bind:checked={brouillon.rappelVeille} /> Me le rappeler la veille</label>
			<label><span>Notes</span><textarea rows="2" bind:value={brouillon.notes}></textarea></label>
			{#if erreur}<p class="erreur" role="alert">{erreur}</p>{/if}
			<div class="rangee">
				<button class="principal" onclick={sauver}>Enregistrer</button>
				<button onclick={() => (brouillon = undefined)}>Annuler</button>
				{#if !estNouvelle}
					<button
						class="danger"
						onclick={async () => {
							await mettreALaCorbeille('fetes', brouillon!.id);
							brouillon = undefined;
						}}>Mettre à la corbeille</button
					>
				{/if}
			</div>
		</section>
	{/if}

	{#each GENRES as [genre, nom]}
		{@const groupe = visibles.filter((f) => f.genre === genre)}
		<section>
			<div class="tete-section">
				<Ornement nom="grecque" />
				<h2>{nom}</h2>
			</div>
			<ul class="reglee">
				{#each groupe as f (f.id)}
					<li>
						<button class="ligne brut" onclick={() => ouvrir(f)}>
							<span class="date pc chiffres-alignes">{date(f)}</span>
							<span class="titre"
								>{f.titre}{#if f.rappelVeille}<span class="rappel" title="Rappel la veille"> ✠</span>{/if}</span
							>
						</button>
					</li>
				{:else}
					<li class="vide petit">{EXEMPLES[genre]}</li>
				{/each}
			</ul>
			<button class="ajout" onclick={() => nouvelle(genre)}>Ajouter</button>
		</section>
	{/each}

	{#if corbeille.length}
		<section>
			<div class="tete-section">
				<Ornement nom="grecque" />
				<h2>Corbeille</h2>
			</div>
			<ul class="reglee">
				{#each corbeille as f (f.id)}
					<li class="jete">
						<span class="titre">{f.titre}</span><Badge objet={f} />
						<span class="espace"></span>
						<button onclick={() => sortirDeLaCorbeille('fetes', f.id)}>Rétablir</button>
						{#if aSupprimer === f.id}
							<button class="danger" onclick={() => supprimerDefinitivement('fetes', f.id)}>Confirmer la suppression</button>
						{:else}
							<button class="discret" onclick={() => (aSupprimer = f.id)}>Supprimer pour de bon</button>
						{/if}
					</li>
				{/each}
			</ul>
		</section>
	{/if}
</main>

<style>
	.tete-page :global(.filet) {
		max-width: 16rem;
	}
	.formulaire {
		display: grid;
		gap: var(--hs-e4);
		margin-bottom: var(--hs-e5);
	}
	.formulaire h2 {
		font-size: var(--hs-t2);
	}
	.trois {
		display: grid;
		grid-template-columns: 1fr 1.6fr 1.4fr;
		gap: var(--hs-e3);
	}
	.case {
		display: flex;
		gap: 8px;
		align-items: baseline;
	}
	.ligne {
		flex: 1;
		display: grid;
		grid-template-columns: 7.5rem 1fr;
		gap: var(--hs-e3);
		align-items: baseline;
		text-align: left;
		background: none;
		border: 0;
		padding: 12px 0;
		cursor: pointer;
		color: var(--hs-encre);
	}
	.date {
		color: var(--hs-encre-douce);
		font-size: 1.0625rem;
	}
	.titre {
		line-height: 1.3;
	}
	.rappel {
		color: var(--hs-rubrique);
		font-size: 0.8em;
	}
	li.vide {
		padding: 12px 0;
		font-style: italic;
	}
	li.jete {
		flex-wrap: wrap;
		padding: 8px 0;
	}
	.ajout {
		margin-top: var(--hs-e4);
		min-height: 40px;
	}
</style>
