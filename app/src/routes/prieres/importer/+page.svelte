<script lang="ts">
	import { goto } from '$app/navigation';
	import { onDestroy } from 'svelte';
	import { creer, db, nouvelId } from '#lib/db.ts';
	import { arreterOcr, assembler, decouper, extraireImage, extrairePdf, ouvrirPdf, type PageExtraite } from '#lib/importer.ts';
	import { rendre } from '#lib/markup.ts';
	import { SOURCE_VIDE, type Texte } from '#lib/types.ts';

	type Doc = Awaited<ReturnType<typeof ouvrirPdf>>['doc'];

	let fichier: File | undefined = $state();
	let doc: Doc | undefined;
	let estPdf = $state(false);
	let nbPages = $state(0);
	let de = $state(1);
	let a = $state(1);
	let forcerOcr = $state(false);

	let etape: 'choix' | 'extraction' | 'correction' = $state('choix');
	let message = $state('');
	let fraction = $state(0);
	let erreur = $state('');

	let pages: PageExtraite[] = $state([]);
	let texte = $state('');
	let ouvrage = $state('');
	let edition = $state('');
	let partie = $state('');
	let zone: HTMLTextAreaElement | undefined = $state();
	let apercu: number | undefined = $state();

	const pieces = $derived(decouper(texte, ouvrage));
	const pagesOcr = $derived(pages.filter((p) => p.ocr));
	const MAX_PAGES = 40;

	onDestroy(() => {
		arreterOcr();
		doc?.cleanup();
	});

	async function choisir(e: Event) {
		erreur = '';
		const f = (e.currentTarget as HTMLInputElement).files?.[0];
		if (!f) return;
		fichier = f;
		estPdf = f.type === 'application/pdf' || /\.pdf$/i.test(f.name);
		if (estPdf) {
			try {
				const r = await ouvrirPdf(f);
				doc = r.doc;
				nbPages = r.info.pages;
				ouvrage = r.info.titre;
				de = 1;
				a = Math.min(nbPages, 1);
			} catch (err) {
				console.error(err);
				erreur = 'Ce PDF n’a pas pu être ouvert (fichier abîmé ou protégé par mot de passe).';
				fichier = undefined;
			}
		} else {
			ouvrage = f.name.replace(/\.[a-z0-9]+$/i, '');
		}
	}

	async function extraire() {
		if (!fichier) return;
		erreur = '';
		if (estPdf) {
			if (!(de >= 1 && a >= de && a <= nbPages)) return (erreur = `Choisissez des pages entre 1 et ${nbPages}.`);
			if (a - de + 1 > MAX_PAGES) return (erreur = `Prenez ${MAX_PAGES} pages au plus à la fois.`);
		}
		etape = 'extraction';
		try {
			const suivre = (m: string, f: number) => {
				message = m;
				fraction = f;
			};
			pages = estPdf && doc ? await extrairePdf(doc, de, a, suivre, forcerOcr) : await extraireImage(fichier, suivre);
			texte = assembler(pages);
			etape = 'correction';
		} catch (err) {
			console.error(err);
			erreur = 'L’extraction a échoué. Pour un PDF scanné, la reconnaissance de texte a besoin d’Internet la première fois.';
			etape = 'choix';
		}
	}

	/** Insère une marque de nouvelle pièce au début de la ligne du curseur. */
	function couperIci() {
		if (!zone) return;
		const pos = zone.selectionStart;
		const debut = texte.lastIndexOf('\n', pos - 1) + 1;
		texte = texte.slice(0, debut) + '=== \n' + texte.slice(debut);
		queueMicrotask(() => {
			zone?.focus();
			zone?.setSelectionRange(debut + 4, debut + 4);
		});
	}

	async function enregistrer() {
		erreur = '';
		if (!pieces.length) return (erreur = 'Il n’y a aucun texte à enregistrer.');
		if (pieces.some((p) => !p.titre.trim())) return (erreur = 'Donnez un titre à chaque pièce (ligne « === Titre »).');
		const dernier = await db.textes.orderBy('ordre').last();
		let ordre = dernier?.ordre ?? 0;
		for (const p of pieces) {
			await creer<Texte>('textes', {
				id: nouvelId(),
				origine: 'personnel',
				titre: p.titre,
				partie,
				categorie: '',
				corps: p.corps,
				latin: '',
				usage: '',
				indulgence: '',
				source: { ...SOURCE_VIDE, ouvrage, edition, page: p.pages },
				ordre: ++ordre
			});
		}
		goto('/prieres');
	}
</script>

<svelte:head><title>Importer un PDF ou une photo — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour" href="/prieres/nouveau">‹ Ajouter une prière</a>
	<div class="tete-page"><h1>Importer un PDF ou une photo</h1></div>

	{#if etape === 'choix'}
		<p class="petit">
			Le fichier reste sur cet appareil : rien n’est envoyé. Pour une page scannée ou une photo, le texte est reconnu en français et en
			latin ; la première fois, l’outil de reconnaissance se télécharge (connexion nécessaire).
		</p>
		<label class="bouton fichier">
			{fichier ? 'Changer de fichier' : 'Choisir un PDF ou une photo'}
			<input type="file" accept="application/pdf,.pdf,image/*" onchange={choisir} />
		</label>

		{#if fichier}
			<p class="nom">
				{fichier.name}{#if estPdf}
					<span class="petit">— {nbPages} page{nbPages > 1 ? 's' : ''}</span>{/if}
			</p>
			{#if estPdf}
				<div class="grille">
					<label><span>De la page</span><input type="number" min="1" max={nbPages} bind:value={de} /></label>
					<label><span>À la page</span><input type="number" min="1" max={nbPages} bind:value={a} /></label>
				</div>
				<p class="petit">Ce sont les pages du fichier, pas la numérotation imprimée du livre : vous corrigerez la page citée ensuite.</p>
				<label class="case"
					><input type="checkbox" bind:checked={forcerOcr} /> Reconnaître le texte sur l’image, même si le PDF contient déjà du texte (PDF scanné
					mal lu)</label
				>
			{/if}
			<div class="rangee actions">
				<button class="principal" onclick={extraire}>Extraire le texte</button>
			</div>
		{/if}
	{:else if etape === 'extraction'}
		<p role="status">{message}</p>
		<progress max="1" value={fraction}></progress>
	{:else}
		{#if pagesOcr.length}
			<p class="alerte">
				{pagesOcr.length} page{pagesOcr.length > 1 ? 's ont été lues' : ' a été lue'} par reconnaissance de texte ({pagesOcr
					.map((p) => `p. ${p.page} : ${p.confiance} %`)
					.join(' ; ')}). Relisez-{pagesOcr.length > 1 ? 'les' : 'la'}
				contre l’original : une lettre peut être fausse.
			</p>
		{/if}

		<fieldset>
			<legend>Source commune</legend>
			<label><span>Ouvrage</span><input type="text" bind:value={ouvrage} /></label>
			<div class="grille">
				<label><span>Édition (lieu, éditeur, année)</span><input type="text" bind:value={edition} /></label>
				<label><span>Partie de la bibliothèque</span><input type="text" bind:value={partie} /></label>
			</div>
		</fieldset>

		<div class="rangee outils">
			<button type="button" onclick={couperIci}>Couper ici : nouvelle pièce</button>
			<span class="petit">Placez le curseur sur la première ligne d’une prière, puis coupez. Écrivez son titre après « === ».</span>
		</div>
		<label>
			<span>Texte extrait, à corriger</span>
			<textarea bind:this={zone} bind:value={texte} rows="18"></textarea>
		</label>
		<p class="petit">
			Les marques ⟦p. N⟧ indiquent le début de chaque page ; elles servent à remplir la source et ne seront pas enregistrées.
		</p>

		<h2>{pieces.length} pièce{pieces.length > 1 ? 's' : ''} à enregistrer</h2>
		<ul class="pieces">
			{#each pieces as p, i (i)}
				<li>
					<button class="discret ligne" aria-expanded={apercu === i} onclick={() => (apercu = apercu === i ? undefined : i)}>
						<span>{apercu === i ? '▾' : '▸'} {p.titre || 'Sans titre'}</span>
						<span class="petit">{p.pages ? `p. ${p.pages}` : ''} · {p.corps.length} caractères</span>
					</button>
					{#if apercu === i}<div class="priere apercu">{@html rendre(p.corps)}</div>{/if}
				</li>
			{/each}
		</ul>

		{#if erreur}<p class="erreur" role="alert">{erreur}</p>{/if}
		<div class="rangee actions">
			<button class="principal" onclick={enregistrer}>Enregistrer {pieces.length > 1 ? `les ${pieces.length} pièces` : 'la pièce'}</button>
			<button onclick={() => (etape = 'choix')}>Revenir au choix des pages</button>
		</div>
		<p class="petit">Les pièces seront marquées « Ajout personnel ». Vous pourrez ensuite compléter chacune (latin, usage, indulgence).</p>
	{/if}
	{#if erreur && etape === 'choix'}<p class="erreur" role="alert">{erreur}</p>{/if}
</main>

<style>
	.fichier {
		position: relative;
		overflow: hidden;
		margin-top: 0.5rem;
	}
	.fichier input {
		position: absolute;
		inset: 0;
		opacity: 0;
		cursor: pointer;
	}
	.nom {
		margin: 0.8rem 0 0.4rem;
		overflow-wrap: anywhere;
	}
	.grille {
		display: grid;
		gap: 0.75rem;
		grid-template-columns: 1fr 1fr;
	}
	input[type='number'] {
		width: 100%;
		padding: 0.5rem 0.65rem;
		background: var(--hs-surface);
		border: 1px solid var(--hs-filet);
		border-radius: 0;
		font: inherit;
		color: inherit;
	}
	.case {
		display: flex;
		gap: 0.5rem;
		align-items: baseline;
		margin-top: 0.6rem;
		font-size: 0.9rem;
	}
	.actions {
		margin-top: 1.2rem;
	}
	progress {
		width: 100%;
		accent-color: var(--hs-rubrique);
	}
	.alerte {
		padding: 0.6rem 0.9rem;
		border: 1px dashed var(--hs-rubrique);
		border-radius: 0;
		font-size: 0.9rem;
	}
	fieldset {
		border: 1px solid var(--hs-filet);
		border-radius: 0;
		padding: 0.2rem 0.8rem 0.8rem;
		margin-top: 0.8rem;
	}
	fieldset label {
		margin-top: 0.6rem;
	}
	legend {
		font-variant: small-caps;
		letter-spacing: 0.05em;
		color: var(--hs-rubrique);
		padding: 0 0.3rem;
	}
	.outils {
		margin: 1rem 0 0.4rem;
	}
	h2 {
		margin-top: 1.4rem;
	}
	.pieces {
		list-style: none;
		margin: 0.4rem 0 0;
		padding: 0;
	}
	.pieces li {
		border-bottom: 1px solid var(--hs-filet);
	}
	.ligne {
		width: 100%;
		justify-content: space-between;
		text-align: left;
		color: var(--hs-encre);
		flex-wrap: wrap;
	}
	.apercu {
		padding: 0.4rem 0.8rem 0.8rem;
	}
	.erreur {
		color: var(--hs-rubrique);
	}
</style>
