<script lang="ts">
	import { page } from '$app/state';
	import { anneeLiturgique, iso, jourDu, type Jour } from '#lib/calendrier.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { rendre } from '#lib/markup.ts';
	import { chargerRecueil, choisir, type Choix, type Recueil } from '#lib/meditations.ts';

	/** Méditation du jour : Hamon les dimanches et aux temps forts, le parcours de Chaignon les jours ordinaires. */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const lendemain = $derived(iso(new Date(new Date(date + 'T12:00:00').getTime() + 864e5)));
	const veille = $derived(iso(new Date(new Date(date + 'T12:00:00').getTime() - 864e5)));

	let jour: Jour | undefined = $state();
	let jourDemain: Jour | undefined = $state();
	let hamon: Recueil | null = $state(null);
	let chaignon: Recueil | null = $state(null);
	let annee: Jour[] = $state([]);
	let charge = $state(false);
	$effect(() => {
		const d = date, l = lendemain, y = Number(d.slice(0, 4));
		charge = false;
		Promise.all([jourDu(d), jourDu(l), chargerRecueil('hamon'), chargerRecueil('chaignon'), anneeLiturgique(y - 1), anneeLiturgique(y)])
			.then(([j, jd, h, c, a1, a2]) => {
				jour = j; jourDemain = jd; hamon = h; chaignon = c;
				annee = [a1, a2].find((a) => a?.some((x) => x.date === d)) ?? [];
				charge = true;
			});
	});

	const entrees = $derived<Choix[]>(choisir(date, jour, annee, hamon, chaignon));
	const demain = $derived<Choix[]>(choisir(lendemain, jourDemain, annee, hamon, chaignon));
	let choix = $state(0);
	$effect(() => { void date; choix = 0; });
	const c = $derived(entrees[choix]);
	const m = $derived(c?.entree);
	const recueil = $derived(c?.recueil);
	const dateLongue = $derived(new Date(date + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' }));
	const edition = (x: Choix) => x.recueil.editions[String(x.entree.tome)] ?? '';
</script>

<svelte:head><title>Méditation — Hortus Sacrum</title></svelte:head>

<main class="ecran entree">
	<a class="retour interface" href="/?date={date}"><Icone nom="retour" taille={16} /> Aujourd’hui</a>

	<header>
		<p class="etiquette">Méditation · {dateLongue}</p>
		{#if m}
			<h1>{m.titre}</h1>
			{#if jour}<p class="usage"><em>{jour.office}</em></p>{/if}
		{:else if charge}
			<h1>Pas de méditation pour ce jour</h1>
		{/if}
		<nav class="jours interface" aria-label="Autres jours">
			<a href="/meditation?date={veille}">‹ veille</a>
			<a href="/meditation?date={lendemain}">lendemain ›</a>
		</nav>
		<Ornement nom="fleuron" />
	</header>

	{#if entrees.length > 1}
		<div class="choix interface" role="group" aria-label="Méditations de ce jour">
			{#each entrees as e, i}
				<button class="bouton" aria-pressed={choix === i} onclick={() => (choix = i)}>{e.recueil.id === 'chaignon' ? 'Chaignon' : 'Hamon'} · {e.entree.titre}</button>
			{/each}
		</div>
	{/if}

	{#if m}
		<div class="page">
			<article class="texte">
				{#if m.sommaire}
					<details class="sommaire">
						<summary class="pc">Sommaire pour la veille au soir</summary>
						<div class="lecture">{@html rendre(m.sommaire)}</div>
					</details>
				{/if}
				<div class="lecture">{@html rendre(m.corps)}</div>
			</article>

			<aside class="marge" aria-label="Source">
				<details open>
					<summary><span class="pc">Source</span></summary>
					<p class="imprime">
						{recueil?.auteur}, <em>{recueil?.titre}</em><br />{edition(c)}, t. {m.tome}{#if m.page}, p. {m.page}{/if}
					</p>
					<p>{recueil?.provenance}</p>
				</details>
				{#if demain.length}
					<details open>
						<summary><span class="pc">Pour demain</span></summary>
						<p><a href="/meditation?date={lendemain}">{demain[0].entree.titre}</a></p>
						{#if demain[0].entree.sommaire}<p class="petit">{demain[0].entree.sommaire}</p>{/if}
					</details>
				{/if}
			</aside>
		</div>
		<div class="cul"><Ornement nom="cherubin" taille={30} /></div>
	{/if}
</main>

<style>
	.ecran { max-width: 980px; margin: 0 auto; padding: var(--hs-e5) var(--hs-marge-mobile) var(--hs-e7); }
	.retour { display: inline-flex; align-items: center; gap: 4px; text-decoration: none; color: var(--hs-encre-douce); min-height: 44px; }
	header { text-align: center; display: grid; justify-items: center; gap: var(--hs-e3); margin: var(--hs-e6) auto; max-width: var(--hs-mesure); }
	header p { margin: 0; }
	h1 { font-size: var(--hs-t3); }
	.jours { display: flex; gap: var(--hs-e5); font-size: var(--hs-t0); }
	.choix { display: flex; flex-wrap: wrap; justify-content: center; gap: var(--hs-e2); margin: 0 auto var(--hs-e5); max-width: var(--hs-mesure); }
	.texte { max-width: var(--hs-mesure); margin-inline: auto; }
	.lecture :global(p) { text-align: justify; hyphens: auto; }
	.lecture :global(h2) { text-align: center; font-size: var(--hs-t1, 1.25rem); margin: var(--hs-e5) 0 var(--hs-e2); font-variant: small-caps; letter-spacing: 0.04em; }
	.sommaire { border-block: var(--hs-cheveu) solid var(--hs-filet); margin-bottom: var(--hs-e5); }
	.sommaire summary { padding: 10px 0; color: var(--hs-encre-douce); cursor: pointer; }
	.sommaire .lecture { font-size: 0.9375rem; color: var(--hs-encre-douce); }
	.marge { max-width: var(--hs-mesure); margin: var(--hs-e6) auto 0; border-top: var(--hs-cheveu) solid var(--hs-filet); }
	.marge details { border-bottom: var(--hs-cheveu) solid var(--hs-filet); }
	.marge summary { padding: 10px 0; color: var(--hs-encre-douce); }
	.marge p { margin: 0 0 12px; font-size: 0.9375rem; line-height: 1.45; color: var(--hs-encre-douce); }
	.marge .imprime { font-size: 1rem; }
	.marge .petit { font-size: 0.875rem; }
	.cul { text-align: center; color: var(--hs-or); margin-top: var(--hs-e7); }
	@media (min-width: 900px) {
		h1 { font-size: var(--hs-t4); }
		.page { display: grid; grid-template-columns: minmax(0, 1fr) 230px; gap: var(--hs-e6); align-items: start; }
		.marge { margin: 0; border-top: 0; position: sticky; top: var(--hs-e5); }
		.marge details { border-bottom: 0; border-left: var(--hs-cheveu) solid var(--hs-or-trait); padding-left: var(--hs-e4); margin-bottom: var(--hs-e5); }
	}
</style>
