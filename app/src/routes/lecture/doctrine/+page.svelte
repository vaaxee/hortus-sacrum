<script lang="ts">
	import { page } from '$app/state';
	import { iso } from '#lib/calendrier.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { rendre } from '#lib/markup.ts';
	import {
		articleDuJour,
		chargerIndex,
		chargerQuestion,
		lireMarque,
		marquerLu,
		voisins,
		type Article,
		type IndexSomme,
		type Marque,
		type Question
	} from '#lib/somme.ts';

	/**
	 * Doctrine (lot 10 ; SPEC § 11, REFONTE § 5.6) : la Somme théologique, un article par jour à la suite. Français de
	 * Lachat, latin léonin en regard sur demande (comme l'Évangile). « ?ref=Iª q. 2 a. 3 » ouvre un article précis.
	 */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const demande = $derived(page.url.searchParams.get('ref'));

	let index = $state<IndexSomme | null>(null);
	let marque = $state<Marque | undefined>();
	let question = $state<Question | null>(null);
	let charge = $state(false);

	$effect(() => {
		chargerIndex().then((i) => (index = i));
		lireMarque().then((m) => (marque = m));
	});
	const duJour = $derived(index && index.articles.length ? articleDuJour(index, marque, date) : null);
	const entree = $derived(index ? (demande && index.articles.find((a) => a.ref === demande)) || duJour?.entree : undefined);
	$effect(() => {
		const e = entree;
		if (!e) return;
		charge = false;
		chargerQuestion(e.fichier).then((q) => {
			question = q;
			charge = true;
		});
	});
	const article = $derived<Article | undefined>(question?.articles.find((a) => a.ref === entree?.ref));
	const proches = $derived(index && entree ? voisins(index, entree.ref) : {});
	const premierDeLaQuestion = $derived(entree?.article === 1);
	const luCeJour = $derived(!!marque && marque.ref === entree?.ref && marque.date === date);
	const estDuJour = $derived(entree?.ref === duJour?.entree.ref);

	let latin = $state(false);
	try {
		latin = localStorage.getItem('somme-latin') === '1';
	} catch {
		/* rien */
	}
	function basculer() {
		latin = !latin;
		try {
			localStorage.setItem('somme-latin', latin ? '1' : '0');
		} catch {
			/* rien */
		}
	}
	async function lu() {
		if (!entree) return;
		await marquerLu(entree.ref, date);
		marque = await lireMarque();
	}
	const lien = (ref: string) => `/lecture/doctrine?ref=${encodeURIComponent(ref)}`;
	const romain = (n: number) =>
		['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV'][n] ?? String(n);
</script>

<svelte:head><title>{entree?.ref ?? 'Somme théologique'} — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<p class="etiquette">Summa theologiae</p>
		<h1>Somme théologique</h1>
		{#if entree}
			<p class="date pc chiffres-alignes">
				{#if proches.avant}<a class="pas" href={lien(proches.avant.ref)} aria-label="Article précédent"
						><Icone nom="retour" taille={16} /></a
					>{/if}
				{entree.ref}
				{#if proches.apres}<a class="pas" href={lien(proches.apres.ref)} aria-label="Article suivant"><Icone nom="chevron" taille={16} /></a
					>{/if}
			</p>
		{/if}
		<Ornement nom="fleuron" />
	</div>

	{#if question && article && entree}
		<article class="texte" class:bilingue={latin}>
			<div class="bascule">
				<button class="bouton" aria-pressed={latin} onclick={basculer}>{latin ? 'Masquer le latin' : 'Latin'}</button>
			</div>

			<header class="intitule">
				<p class="pc rub">Question {romain(question.question)}. {question.titre.fr.replace(/\.$/, '')}</p>
				{#if latin}<p class="la" lang="la">{question.titre.la}</p>{/if}
			</header>

			{#if premierDeLaQuestion}
				<section class="bloc prologue" aria-label="Prologue de la question">
					<div class="fr">{@html rendre(question.prooemium.fr)}</div>
					{#if latin}<div class="la" lang="la">{@html rendre(question.prooemium.la)}</div>{/if}
				</section>
			{/if}

			<header class="intitule">
				<h2 class="pc">Article {romain(entree.article)}</h2>
				<p class="titre-article">{article.titre.fr}</p>
				{#if latin}<p class="la" lang="la">{article.titre.la}</p>{/if}
			</header>

			{#each article.objections as o, i (i)}
				<section class="bloc">
					<div class="fr">{@html rendre(o.fr)}</div>
					{#if latin}<div class="la" lang="la">{@html rendre(o.la)}</div>{/if}
				</section>
			{/each}
			<section class="bloc">
				{#if article.sed_contra.fr}<div class="fr">{@html rendre(article.sed_contra.fr)}</div>{/if}
				{#if latin || !article.sed_contra.fr}<div class="la" lang="la">{@html rendre(article.sed_contra.la)}</div>{/if}
			</section>
			<section class="bloc corps">
				<div class="fr">{@html rendre(article.respondeo.fr)}</div>
				{#if latin}<div class="la" lang="la">{@html rendre(article.respondeo.la)}</div>{/if}
			</section>
			{#each article.reponses as r, i (i)}
				<section class="bloc">
					<div class="fr">{@html rendre(r.fr)}</div>
					{#if latin}<div class="la" lang="la">{@html rendre(r.la)}</div>{/if}
				</section>
			{/each}
			{#each article.notes ?? [] as n (n)}<p class="note petit">{n}</p>{/each}

			<p class="lu">
				{#if luCeJour}<span class="petit">✠ Article lu aujourd’hui</span>
				{:else if estDuJour}<button onclick={lu}>J’ai lu cet article</button>
				{:else if duJour}<a class="petit" href="/lecture/doctrine">Article du jour : {duJour.entree.ref}</a>{/if}
			</p>
			{#if duJour?.fin && estDuJour}<p class="petit centre">Les articles suivants ne sont pas encore dans l’app.</p>{/if}
			<div class="cul"><Ornement nom="cherubin" taille={30} /></div>
			<p class="source petit">
				Traduction : <a href={question.source.fr.url} rel="noopener" target="_blank">{question.source.fr.ouvrage}</a>, {question.source.fr
					.edition}, p. {article.pages.fr[0]}{article.pages.fr[1] !== article.pages.fr[0] ? `-${article.pages.fr[1]}` : ''}.
				{#if latin}Latin : <a href={question.source.la.url} rel="noopener" target="_blank">{question.source.la.ouvrage}</a>, {question
						.source.la.edition}.{/if}
			</p>
		</article>
	{:else if charge || (index && !index.articles.length)}
		<p class="centre">Cet article n’est pas dans l’app.</p>
	{/if}
</main>

<style>
	.tete-page {
		text-align: center;
	}
	.date {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--hs-e3);
	}
	.pas {
		display: inline-grid;
		place-items: center;
		width: 32px;
		height: 32px;
		color: var(--hs-or-texte);
	}
	.texte {
		max-width: var(--hs-mesure);
		margin: var(--hs-e5) auto 0;
	}
	.bascule {
		display: flex;
		justify-content: center;
		margin-bottom: var(--hs-e5);
	}
	.bascule .bouton {
		min-height: 36px;
	}
	.intitule {
		text-align: center;
		margin: var(--hs-e5) 0 var(--hs-e4);
	}
	.intitule p,
	.intitule h2 {
		margin: 0 0 var(--hs-e1);
	}
	.titre-article {
		font-style: italic;
	}
	.bloc {
		margin: 0 0 var(--hs-e4);
		display: grid;
		gap: var(--hs-e2);
		text-align: justify;
		hyphens: auto;
	}
	.bloc :global(p) {
		margin: 0 0 var(--hs-e2);
	}
	.la {
		color: var(--hs-encre-douce);
		font-size: 0.95em;
		font-style: italic;
		padding-left: var(--hs-e4);
		border-left: var(--hs-cheveu) solid var(--hs-or-trait);
	}
	.intitule .la {
		border-left: 0;
		padding-left: 0;
	}
	.note {
		color: var(--hs-encre-douce);
		font-style: italic;
	}
	.lu {
		text-align: center;
		margin: var(--hs-e5) 0 0;
		color: var(--hs-or-texte);
	}
	.cul {
		max-width: 90px;
		margin: var(--hs-e5) auto var(--hs-e3);
	}
	.source {
		text-align: center;
		color: var(--hs-encre-douce);
	}
	.centre {
		text-align: center;
	}
	@media (min-width: 720px) {
		.texte.bilingue {
			max-width: 52rem;
		}
		.bilingue .bloc {
			grid-template-columns: 1fr 1fr;
			gap: var(--hs-e6);
		}
		.bilingue .bloc .la {
			order: -1;
			border-left: 0;
			padding-left: 0;
			font-style: normal;
		}
		.bilingue .bloc .fr {
			border-left: var(--hs-cheveu) solid var(--hs-or-trait);
			padding-left: var(--hs-e5);
		}
	}
</style>
