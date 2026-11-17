<script lang="ts">
	import { goto } from '$app/navigation';
	import FicheTexte from '#lib/FicheTexte.svelte';
	import { creer, db, nouvelId } from '#lib/db.ts';
	import { vivant } from '#lib/live.ts';
	import { nettoyer } from '#lib/markup.ts';
	import { SOURCE_VIDE, type Texte } from '#lib/types.ts';

	const parties = vivant(async () => [...new Set((await db.textes.toArray()).map((t) => t.partie).filter(Boolean))], [] as string[]);

	let mode: 'clavier' | 'coller' = $state('clavier');
	let brut = $state('');
	let rapport: string[] = $state([]);
	let nettoye = $state(false);
	let erreur = $state('');

	let texte: Texte = $state({
		id: nouvelId(),
		origine: 'personnel',
		titre: '',
		partie: '',
		categorie: '',
		corps: '',
		latin: '',
		usage: '',
		indulgence: '',
		source: { ...SOURCE_VIDE },
		ordre: 0,
		creeLe: '',
		modifieLe: ''
	});

	function passerAuNettoyage() {
		const r = nettoyer(brut);
		texte.corps = r.texte;
		rapport = r.rapport;
		nettoye = true;
		// première ligne courte : proposée comme titre
		const premiere = r.texte.split('\n')[0] ?? '';
		if (!texte.titre && premiere.length <= 80 && r.texte.startsWith(premiere + '\n\n')) {
			texte.titre = premiere.replace(/[.:]$/, '');
			texte.corps = r.texte.slice(premiere.length).trim();
		}
	}

	async function enregistrer() {
		erreur = '';
		if (!texte.titre.trim()) return (erreur = 'Donnez un titre à cette prière.');
		if (!texte.corps.trim()) return (erreur = 'Le texte est vide.');
		const dernier = await db.textes.orderBy('ordre').last();
		const t = $state.snapshot(texte) as Texte;
		t.ordre = (dernier?.ordre ?? 0) + 1;
		const { creeLe, modifieLe, ...reste } = t;
		await creer<Texte>('textes', reste);
		goto(`/prieres/${encodeURIComponent(t.id)}`);
	}
</script>

<svelte:head><title>Ajouter une prière — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour" href="/prieres">‹ Prières</a>
	<div class="tete-page"><h1>Ajouter une prière</h1></div>

	<div class="rangee modes" role="group" aria-label="Façon de saisir">
		<button aria-pressed={mode === 'clavier'} onclick={() => (mode = 'clavier')}>Au clavier</button>
		<button aria-pressed={mode === 'coller'} onclick={() => (mode = 'coller')}>Copier-coller</button>
		<a class="bouton" href="/prieres/importer">PDF ou photo</a>
	</div>

	{#if mode === 'coller' && !nettoye}
		<label>
			<span>Collez le texte ici</span>
			<textarea rows="12" bind:value={brut} placeholder="Texte copié d’une page, d’un PDF…"></textarea>
		</label>
		<p class="petit">
			Le nettoyage recolle les mots coupés en fin de ligne, retire les sauts de ligne parasites et les espaces doubles, et reconnaît les ℣
			et ℟. Il ne change aucun mot. Vous corrigez ensuite dans l’aperçu.
		</p>
		<button class="principal" disabled={!brut.trim()} onclick={passerAuNettoyage}>Nettoyer et prévisualiser</button>
	{:else}
		{#if mode === 'coller'}
			<div class="rapport epreuve">
				<strong>Nettoyage :</strong>
				{#if rapport.length}
					<ul>
						{#each rapport as r}<li>{r}</li>{/each}
					</ul>
				{:else}
					rien à corriger.
				{/if}
				<button class="discret" onclick={() => (nettoye = false)}>Revenir au texte collé</button>
			</div>
		{/if}
		<FicheTexte bind:texte parties={$parties} />
		{#if erreur}<p class="erreur" role="alert">{erreur}</p>{/if}
		<div class="rangee actions">
			<button class="principal" onclick={enregistrer}>Enregistrer</button>
			<a class="bouton" href="/prieres">Annuler</a>
		</div>
		<p class="petit">Cette prière sera marquée « Ajout personnel ».</p>
	{/if}
</main>

<style>
	.modes {
		margin: 1rem 0;
	}
	.modes button[aria-pressed='true'] {
		border-color: var(--hs-rubrique);
		color: var(--hs-rubrique);
	}
	.rapport {
		font-size: 1rem;
		margin-bottom: var(--hs-e4);
		padding: var(--hs-e4);
	}
	.rapport ul {
		margin: 0.3rem 0;
		padding-left: 1.2rem;
	}
	.actions {
		margin-top: 1.2rem;
	}
	.erreur {
		color: var(--hs-rubrique);
	}
</style>
