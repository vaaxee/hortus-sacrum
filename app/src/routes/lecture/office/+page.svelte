<script lang="ts">
	import { page } from '$app/state';
	import { iso } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import ModeEglise from '#lib/ModeEglise.svelte';
	import Office from '#lib/Office.svelte';
	import { breviaireDuJour, chargerCommuns, prechargerSemaine, type JourBreviaire } from '#lib/office/breviaire.ts';
	import { chargerParvum, parvumDuJour, type DonneesParvum } from '#lib/office/parvum.ts';
	import { chargerPsautierFr, rendreAvecFillion, type PsautierFr } from '#lib/office/psautier-fr.ts';
	import { heuresDe } from '#lib/programme/heures.ts';
	import { heuresDeLaLecture } from '#lib/programme/lectures.ts';
	import { journeeVivante } from '#lib/programme/vivant.svelte.ts';
	import type { Coche } from '#lib/types.ts';
	import { vivantSelon } from '#lib/vivant.svelte.ts';

	/**
	 * Lecture › Office (REFONTE § 4.4) : le bréviaire du jour, une heure à la fois. Le Petit bréviaire du Sacré-Cœur est
	 * l'office compté dans « Lectures du jour ». L'Officium parvum (latin, d'après Divinum Officium) s'affiche dans le
	 * même composant, ses heures cochées à part (« lec:parvum:<heure> ») ; le Bréviaire romain aussi (« lec:romain:<heure> »,
	 * heures complètes d'après le moteur de Divinum Officium, lot 9), le français de Fillion (1917) en regard des psaumes
	 * et des cantiques, sur demande ; le latin reste le texte de l'office (CLAUDE.md § 15).
	 */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const q = $derived(page.url.searchParams.get('date') ? `?date=${date}` : '');
	const vie = journeeVivante(() => date);
	const lecture = $derived(vie.jr?.lectures.find((l) => l.id === 'lec:office'));
	const texte = $derived.by(() => {
		const id = lecture?.sections.find((s) => s.texte)?.texte;
		return id ? vie.textes.get(id) : undefined;
	});
	const heures = $derived(lecture ? heuresDeLaLecture(lecture, vie.corps) : []);
	const cochesDuJour = vivantSelon(() => {
		const k = date;
		return () => db.coches.where('date').equals(k).toArray();
	}, [] as Coche[]);
	const coches = $derived.by(() => {
		const n: Record<string, number> = {};
		for (const c of cochesDuJour.v) n[c.elementId] = (n[c.elementId] ?? 0) + 1;
		return n;
	});
	const BREVIAIRES = [
		{ cle: 'sacre-coeur', nom: 'Petit bréviaire du Sacré-Cœur' },
		{ cle: 'romain', nom: 'Bréviaire romain' },
		{ cle: 'parvum', nom: 'Officium parvum' }
	] as const;
	type Cle = (typeof BREVIAIRES)[number]['cle'];
	const demande = page.url.searchParams.get('breviaire');
	let breviaire = $state<Cle>(BREVIAIRES.find((b) => b.cle === demande)?.cle ?? 'sacre-coeur');
	let parvum = $state<DonneesParvum | null | undefined>();
	$effect(() => {
		if (breviaire === 'parvum' && parvum === undefined) chargerParvum().then((d) => (parvum = d));
	});
	// Bréviaire romain (lot 9) : un fichier par jour, chargé à la demande ; la semaine qui vient est préchargée
	let romain = $state<JourBreviaire | null | undefined>();
	let sourceRomain = $state('');
	$effect(() => {
		if (breviaire !== 'romain') return;
		const d = date;
		romain = undefined;
		breviaireDuJour(d).then((j) => {
			if (d !== date) return;
			romain = j;
			if (j) prechargerSemaine(d);
		});
		chargerCommuns(2026).then((c) => (sourceRomain = c?.source.depot ?? ''));
	});
	const heuresRomain = $derived(romain ? heuresDe(romain.corps) : []);
	// psautier de Fillion en regard (préférence gardée sur l'appareil ; affiché par défaut)
	let fillion = $state<PsautierFr | null | undefined>();
	let francais = $state(true);
	$effect(() => {
		try {
			francais = localStorage.getItem('breviaire-francais') !== '0';
		} catch {
			/* stockage indisponible : réglage par défaut */
		}
	});
	$effect(() => {
		if (breviaire === 'romain' && francais && fillion === undefined) chargerPsautierFr().then((d) => (fillion = d));
	});
	function basculerFrancais() {
		francais = !francais;
		try {
			localStorage.setItem('breviaire-francais', francais ? '1' : '0');
		} catch {
			/* stockage indisponible */
		}
	}
	const renduRomain = $derived(francais && fillion ? (t: string) => rendreAvecFillion(t, fillion!) : undefined);
	const jourParvum = $derived(parvum ? parvumDuJour(parvum, date) : undefined);
	const heuresParvum = $derived(jourParvum ? heuresDe(jourParvum.corps) : []);
	const jourFr = $derived(new Date(date + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' }));
</script>

<svelte:head><title>Office — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="barre-page">
		<a class="retour" href="/lecture{q}"><Icone nom="retour" taille={16} /> Lecture</a>
		<ModeEglise />
	</div>
	<div class="tete-page">
		<p class="etiquette">Office · {jourFr}</p>
		<h1>{BREVIAIRES.find((b) => b.cle === breviaire)?.nom}</h1>
		<Ornement nom="fleuron" />
	</div>

	<div class="breviaires" role="group" aria-label="Bréviaire">
		{#each BREVIAIRES as b (b.cle)}
			<button class="brut" aria-pressed={breviaire === b.cle} onclick={() => (breviaire = b.cle)}>{b.nom}</button>
		{/each}
	</div>

	{#if breviaire === 'sacre-coeur'}
		{#if texte && heures.length}
			<p class="petit">{texte.titre.replace('Petit bréviaire du Sacré-Cœur — ', '')}</p>
			<Office corps={texte.corps} {heures} ligne="lec:office" {date} {coches} />
			<p class="source"><a href="/prieres/{encodeURIComponent(texte.id)}">L’office entier, sa source</a></p>
		{:else if vie.jr}
			<p class="aide">L’office du jour n’est pas dans la bibliothèque.</p>
		{:else}
			<p class="aide">Préparation de l’office…</p>
		{/if}
	{:else if breviaire === 'romain'}
		{#if romain && heuresRomain.length}
			<div class="bascule-fr">
				<p class="petit"><em lang="la">{romain.office}</em> · latin{francais ? ', psaumes en regard' : ''}</p>
				<button class="bouton" aria-pressed={francais} onclick={basculerFrancais}>{francais ? 'Latin seul' : 'Psaumes en français'}</button>
			</div>
			<Office corps={romain.corps} heures={heuresRomain} ligne="lec:romain" {date} {coches} rendu={renduRomain} />
			<p class="source">
				Texte de <a href={sourceRomain}>Divinum Officium</a>, rubriques de 1954 (<em>Divino afflatu</em>).{#if francais && fillion}
					Psaumes et cantiques en français : L.-Cl. Fillion, <a href={fillion.source.url}
						><em>Le nouveau psautier du Bréviaire romain</em></a
					>, 7<sup>e</sup> éd., Paris, Lecoffre-Gabalda, 1917 (<em>imprimatur</em> Paris, 1912).{/if} La traduction des leçons est sur
				<a href="/saint{q}">la page du saint</a>.
			</p>
		{:else if romain === null}
			<p class="aide">
				Le Bréviaire romain n’est calculé que pour l’année liturgique 2026-2027. <a href="/saint{q}"
					>Les leçons du jour et la vie du saint</a
				>.
			</p>
		{:else}
			<p class="aide">Préparation de l’office…</p>
		{/if}
	{:else if jourParvum && heuresParvum.length}
		<p class="petit">{jourParvum.nomDuTemps.replace(/\s*\(.*\)$/, '')} · latin</p>
		<Office corps={jourParvum.corps} heures={heuresParvum} ligne="lec:parvum" {date} {coches} />
		<p class="source">
			Texte de <a href={parvum?.source.depot}>Divinum Officium</a>, rubriques de 1954 ({jourParvum.nomDuTemps.match(/\((.*)\)$/)?.[1] ??
				'Commune/C12'})
		</p>
	{:else if parvum === null || parvum}
		<p class="aide">L’Officium parvum n’est pas calculé pour ce jour.</p>
	{:else}
		<p class="aide">Préparation de l’office…</p>
	{/if}
</main>

<style>
	.retour {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		text-decoration: none;
		font-family: var(--hs-interface);
		font-size: var(--hs-t0);
	}
	.breviaires {
		display: flex;
		flex-wrap: wrap;
		gap: 4px 14px;
		margin: var(--hs-e3) 0;
		font-family: var(--hs-interface);
		font-size: var(--hs-t0);
	}
	.breviaires button {
		padding: 6px 0;
		min-height: 36px;
		background: none;
		border: 0;
		border-bottom: 1px solid transparent;
		color: var(--hs-encre-douce);
		cursor: pointer;
	}
	.breviaires button[aria-pressed='true'] {
		color: var(--hs-encre);
		border-bottom-color: currentColor;
	}
	.bascule-fr {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 4px 14px;
	}
	.bascule-fr .petit {
		margin: 0;
	}
	.source {
		text-align: right;
		font-size: 0.875rem;
	}
</style>
