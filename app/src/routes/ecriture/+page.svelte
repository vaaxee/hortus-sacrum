<script lang="ts">
	import { page } from '$app/state';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { ecrireRef, enClair, LIVRES, lireRef, passage } from '#lib/ecriture.ts';
	import { iso } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import { vivant } from '#lib/live.ts';
	import type { Coche } from '#lib/types.ts';

	/** Lecture d'un passage des Évangiles : français de Crampon (1923), latin de la Vulgate en regard sur demande. */
	const ref = $derived(lireRef(page.url.searchParams.get('ref') ?? 'Mt 1') ?? { livre: 'Mt', chapitre: 1 });
	let texte = $state<Awaited<ReturnType<typeof passage>>>();
	let charge = $state(false);
	$effect(() => {
		const r = ref;
		charge = false;
		passage(r).then((p) => { texte = p; charge = true; });
	});

	let latin = $state(false);
	try { latin = localStorage.getItem('ecriture-latin') === '1'; } catch { /* rien */ }
	function basculer() {
		latin = !latin;
		try { localStorage.setItem('ecriture-latin', latin ? '1' : '0'); } catch { /* rien */ }
	}
	/** Versets français, avec le latin de même numéro ; quand les numérotations diffèrent, le latin vient à part. */
	const versets = $derived(texte ? texte.fr.map(([n, fr]) => ({ n, fr, la: texte!.decale ? '' : (texte!.la.find((v) => v[0] === n)?.[1] ?? '') })) : []);
	const livre = $derived(LIVRES[ref.livre]);
	/** « J'ai lu ce chapitre » : une coche « lecture:Mt 5 », qui compte pour les couronnes de lecture. */
	const cleLecture = $derived(`lecture:${ref.livre} ${ref.chapitre}`);
	const lectures = $derived(vivant(() => db.coches.where('date').above('').filter((c) => c.elementId === cleLecture).toArray(), [] as Coche[]));
	const luLe = $derived($lectures.map((c) => c.date).sort()[0]);
	async function marquerLu() {
		if (luLe) return;
		await db.coches.add({ date: iso(new Date()), elementId: cleLecture, rang: 0, horodatage: new Date().toISOString() });
	}
	const voisin = (d: number) => {
		const c = ref.chapitre + d;
		return c >= 1 && c <= livre.chapitres ? `/ecriture?ref=${encodeURIComponent(`${ref.livre} ${c}`)}` : '';
	};
</script>

<svelte:head><title>{ecrireRef(ref)} — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<p class="etiquette">Sacra Scriptura</p>
		<h1>{livre.nom}</h1>
		<p class="date pc chiffres-alignes">
			{#if voisin(-1)}<a class="pas" href={voisin(-1)} aria-label="Chapitre précédent"><Icone nom="retour" taille={16} /></a>{/if}
			{enClair(ref).replace(`${livre.nom}, `, '')}
			{#if voisin(1)}<a class="pas" href={voisin(1)} aria-label="Chapitre suivant"><Icone nom="chevron" taille={16} /></a>{/if}
		</p>
		<Ornement nom="fleuron" />
	</div>

	{#if texte && versets.length}
		<article class="texte" class:bilingue={latin}>
			<div class="bascule"><button class="bouton" aria-pressed={latin} onclick={basculer}>{latin ? 'Masquer le latin' : 'Latin'}</button></div>
			{#each versets as v, i (v.n)}
				<p class="verset" class:premier={i === 0 && !ref.de}>
					<span class="fr"><sup class="num rub">{v.n}</sup>{v.fr}</span>
					{#if latin && v.la}<span class="la" lang="la">{v.la}</span>{/if}
				</p>
			{/each}
			{#if latin && texte.decale && texte.la.length}
				<div class="latin-a-part" lang="la">
					<p class="pc rub">Vulgate</p>
					{#each texte.la as [n, la] (n)}<p class="verset"><span class="la"><sup class="num rub">{n}</sup>{la}</span></p>{/each}
				</div>
			{/if}
			{#if !ref.de && ['Mt', 'Mc', 'Lc', 'Jn'].includes(ref.livre)}
				<p class="lu">
					{#if luLe}<span class="petit">✠ Chapitre lu le {new Date(luLe + 'T12:00:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}</span>
					{:else}<button onclick={marquerLu}>J’ai lu ce chapitre</button>{/if}
				</p>
			{/if}
			<div class="cul"><Ornement nom="cherubin" taille={30} /></div>
			<p class="source petit">
				Traduction : <a href={texte.source.fr.url} rel="noopener" target="_blank">{texte.source.fr.ouvrage}</a>, {texte.source.fr.edition}.
				{#if latin}Latin : {texte.source.la.ouvrage}.{/if}
			</p>
			{#if ref.de}<p class="petit centre"><a href="/ecriture?ref={encodeURIComponent(`${ref.livre} ${ref.chapitre}`)}">Lire tout le chapitre</a></p>{/if}
		</article>
	{:else if charge}
		<p class="centre">Ce passage n’est pas dans l’app.</p>
	{/if}
</main>

<style>
	.tete-page { text-align: center; }
	.date { display: flex; justify-content: center; align-items: center; gap: var(--hs-e3); }
	.pas { display: inline-grid; place-items: center; width: 32px; height: 32px; color: var(--hs-or-texte); }
	.texte { max-width: var(--hs-mesure); margin: var(--hs-e5) auto 0; }
	.bascule { display: flex; justify-content: center; margin-bottom: var(--hs-e5); }
	.bascule .bouton { min-height: 36px; }
	.verset { margin: 0 0 var(--hs-e3); display: grid; gap: var(--hs-e1); text-align: justify; hyphens: auto; }
	.num { font-family: var(--hs-titre); font-size: 0.7em; margin-right: 0.35em; font-feature-settings: 'lnum'; }
	.premier .fr::first-letter { font-family: var(--hs-titre); font-size: 3.1em; float: left; line-height: 0.85; margin: 0.06em 0.08em 0 0; color: var(--hs-rubrique); }
	.premier .num { display: none; }
	.la { color: var(--hs-encre-douce); font-size: 0.95em; font-style: italic; padding-left: var(--hs-e4); border-left: var(--hs-cheveu) solid var(--hs-or-trait); }
	.latin-a-part { margin-top: var(--hs-e5); border-top: var(--hs-cheveu) solid var(--hs-or-trait); padding-top: var(--hs-e4); }
	.latin-a-part > .pc { text-align: center; margin: 0 0 var(--hs-e3); }
	.latin-a-part .la { border-left: 0; padding-left: 0; }
	.lu { text-align: center; margin: var(--hs-e5) 0 0; color: var(--hs-or-texte); }
	.cul { max-width: 90px; margin: var(--hs-e5) auto var(--hs-e3); }
	.source { text-align: center; color: var(--hs-encre-douce); }
	.centre { text-align: center; }
	@media (min-width: 720px) {
		.texte.bilingue { max-width: 52rem; }
		.bilingue .verset { grid-template-columns: 1fr 1fr; gap: var(--hs-e6); }
		.bilingue .la { order: -1; border-left: 0; padding-left: 0; font-style: normal; }
		.bilingue .fr { border-left: var(--hs-cheveu) solid var(--hs-or-trait); padding-left: var(--hs-e5); }
	}
</style>
