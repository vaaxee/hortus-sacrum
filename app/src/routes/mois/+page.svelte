<script lang="ts">
	import { page } from '$app/state';
	import { iso, MOIS_DEVOTION } from '#lib/calendrier.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { rendre } from '#lib/markup.ts';
	import { chargerRecueil, NOM_COURT, RECUEIL_DU_MOIS, type EntreeRecueil, type Recueil } from '#lib/meditations.ts';

	/** Dévotion du mois : son nom, son indulgence (Ench. 1952), et la page du jour du recueil du mois s'il y en a un. */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const mois = $derived(Number(date.slice(5, 7)));
	const jourDuMois = $derived(Number(date.slice(8, 10)));
	const dev = $derived(MOIS_DEVOTION[mois]);
	let recueil = $state<Recueil | null>(null);
	$effect(() => {
		const id = RECUEIL_DU_MOIS[mois];
		recueil = null;
		if (id) chargerRecueil(id).then((r) => (recueil = r));
	});
	const entree = $derived<EntreeRecueil | undefined>(recueil?.entrees.find((e) => e.cle === `J:${jourDuMois}`));
	/** Prière, exemple et conseils pratiques du jour, quand le recueil les donne (Berlioux, mois des âmes). */
	const pratique = $derived.by(() => {
		if (!entree) return '';
		const ps = entree.corps.split('\n\n');
		const i = ps.findIndex((p) => /^\W*(PRIÈRE|PRIERE|CONSEILS PRATIQUES|PRATIQUE|RÉSOLUTION)\b/.test(p));
		return i >= 0 ? ps.slice(i).join('\n\n') : '';
	});
</script>

<svelte:head><title>{dev?.nom ?? 'Dévotion du mois'} — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour interface" href="/?date={date}"><Icone nom="retour" taille={16} /> Aujourd’hui</a>
	<div class="tete-page"><h1>{dev?.nom}</h1><Ornement nom="fleuron" /></div>
	<p class="petit">Indulgence : {dev?.reference}.</p>
	{#if entree}
		<p>Aujourd’hui, {NOM_COURT[recueil?.id ?? ''] ?? ''} : <a href="/meditation?date={date}">{entree.titre}</a></p>
		{#if pratique}
			<h2>Pour la pratique de ce jour</h2>
			<div class="lecture">{@html rendre(pratique)}</div>
			<p class="petit source">{recueil?.auteur}, <em>{recueil?.titre}</em>, {recueil?.editions['1']}.</p>
		{/if}
	{:else}
		<p class="petit">Pas encore de recueil ancien pour ce mois dans l’app : la méditation du jour suit Hamon ou Chaignon.</p>
	{/if}
</main>

<style>
	.retour { display: inline-flex; align-items: center; gap: 4px; text-decoration: none; color: var(--hs-encre-douce); min-height: 44px; }
	.lecture :global(p) { text-align: justify; hyphens: auto; }
	.source { color: var(--hs-encre-douce); }
</style>
