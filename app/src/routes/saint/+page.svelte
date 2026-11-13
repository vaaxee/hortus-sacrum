<script lang="ts">
	import { page } from '$app/state';
	import { iso, jourDu, type Jour } from '#lib/calendrier.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { rendre } from '#lib/markup.ts';
	import { chargerRecueil, type EntreeRecueil, type Recueil } from '#lib/meditations.ts';

	/** Office du jour et vie du saint : leçons du IIe nocturne du Bréviaire (Divino Afflatu), français et latin. */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	let jour: Jour | undefined = $state();
	let breviaire = $state<Recueil | null>(null);
	let charge = $state(false);
	let latin = $state(false);
	$effect(() => {
		const d = date;
		charge = false;
		Promise.all([jourDu(d), chargerRecueil('breviaire')]).then(([j, b]) => { jour = j; breviaire = b; charge = true; });
	});
	const fichier = $derived((jour as (Jour & { fichier_divinum_officium?: string | null }) | undefined)?.fichier_divinum_officium ?? null);
	const lecons = $derived<EntreeRecueil | undefined>(
		breviaire && fichier ? breviaire.entrees.find((e) => e.cle === `O:${fichier}`) : undefined
	);
	const dateLongue = $derived(new Date(date + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' }));
</script>

<svelte:head><title>Office du jour — Hortus Sacrum</title></svelte:head>

<main class="ecran entree">
	<a class="retour interface" href="/?date={date}"><Icone nom="retour" taille={16} /> Aujourd’hui</a>
	<header>
		<p class="etiquette">Office du jour · {dateLongue}</p>
		{#if jour}
			<h1>{jour.office}</h1>
			<p class="usage"><em>{jour.rang}{jour.commemoraisons.length ? ` ; mémoire : ${jour.commemoraisons.join(', ')}` : ''}</em></p>
		{/if}
		<Ornement nom="fleuron" />
	</header>

	{#if lecons}
		<div class="page">
			<article class="texte">
				<p class="pc rub centre">Leçons du IIe nocturne</p>
				{#if (lecons as EntreeRecueil & { latin?: string }).latin}
					<div class="bascule"><button class="bouton" aria-pressed={latin} onclick={() => (latin = !latin)}>{latin ? 'Français' : 'Latin'}</button></div>
				{/if}
				<div class="lecture" lang={latin ? 'la' : 'fr'}>{@html rendre(latin ? (lecons as EntreeRecueil & { latin?: string }).latin ?? '' : lecons.corps)}</div>
			</article>
			<aside class="marge" aria-label="Source">
				<details open>
					<summary><span class="pc">Source</span></summary>
					<p class="imprime"><em>Breviarium Romanum</em>, rubriques de 1911 (Divino Afflatu), {fichier}</p>
					<p>{breviaire?.provenance}</p>
				</details>
			</aside>
		</div>
		<div class="cul"><Ornement nom="cherubin" taille={30} /></div>
	{:else if charge}
		<p class="centre">Pas de leçons propres pour l’office de ce jour (férie ou dimanche : voir la méditation du jour).</p>
	{/if}
</main>

<style>
	.ecran { max-width: 980px; margin: 0 auto; padding: var(--hs-e5) var(--hs-marge-mobile) var(--hs-e7); }
	.retour { display: inline-flex; align-items: center; gap: 4px; text-decoration: none; color: var(--hs-encre-douce); min-height: 44px; }
	header { text-align: center; display: grid; justify-items: center; gap: var(--hs-e3); margin: var(--hs-e6) auto; max-width: var(--hs-mesure); }
	header p { margin: 0; }
	h1 { font-size: var(--hs-t3); }
	.centre { text-align: center; }
	.bascule { text-align: center; margin: var(--hs-e2) 0 var(--hs-e4); }
	.texte { max-width: var(--hs-mesure); margin-inline: auto; }
	.lecture :global(p) { text-align: justify; hyphens: auto; }
	.lecture :global(h2) { text-align: center; font-size: var(--hs-t1, 1.25rem); margin: var(--hs-e5) 0 var(--hs-e2); font-variant: small-caps; letter-spacing: 0.04em; }
	.marge { max-width: var(--hs-mesure); margin: var(--hs-e6) auto 0; border-top: var(--hs-cheveu) solid var(--hs-filet); }
	.marge details { border-bottom: var(--hs-cheveu) solid var(--hs-filet); }
	.marge summary { padding: 10px 0; color: var(--hs-encre-douce); }
	.marge p { margin: 0 0 12px; font-size: 0.9375rem; line-height: 1.45; color: var(--hs-encre-douce); }
	.cul { text-align: center; color: var(--hs-or); margin-top: var(--hs-e7); }
	@media (min-width: 900px) {
		h1 { font-size: var(--hs-t4); }
		.page { display: grid; grid-template-columns: minmax(0, 1fr) 230px; gap: var(--hs-e6); align-items: start; }
		.marge { margin: 0; border-top: 0; position: sticky; top: var(--hs-e5); }
		.marge details { border-bottom: 0; border-left: var(--hs-cheveu) solid var(--hs-or-trait); padding-left: var(--hs-e4); margin-bottom: var(--hs-e5); }
	}
</style>
