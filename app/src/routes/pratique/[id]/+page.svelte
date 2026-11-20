<script lang="ts">
	import { page } from '$app/state';
	import { iso } from '#lib/calendrier.ts';
	import { creer, db, enregistrer } from '#lib/db.ts';
	import Case from '#lib/design/Case.svelte';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { enMinutes } from '#lib/durees.ts';
	import { avecLeNom } from '#lib/gertrude.ts';
	import { rendre } from '#lib/markup.ts';
	import { contenuDe, minutesDUneRecitation, recitations } from '#lib/programme/bilan.ts';
	import { cocher } from '#lib/programme/suivi.ts';
	import type { Ligne, SectionResolue } from '#lib/programme/types.ts';
	import { journeeVivante } from '#lib/programme/vivant.svelte.ts';
	import type { Coche, Fait, NoteJour } from '#lib/types.ts';
	import { vivantSelon } from '#lib/vivant.svelte.ts';

	/**
	 * Page d'une pratique du jour (SPEC § 11, principe 4) : ses prières à la suite, composées à l'affichage à partir des
	 * textes sourcés ; les petites pratiques insérées à leur place ; notices et heures repliées.
	 */
	const id = $derived(decodeURIComponent(page.params.id ?? ''));
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const vie = journeeVivante(() => date);
	const ligne = $derived(vie.jr?.lignes.find((l) => l.id === id));
	const lecture = $derived(vie.jr?.lectures.find((l) => l.id === id));
	const sections = $derived(ligne?.sections ?? lecture?.sections ?? []);
	const titre = $derived(ligne?.titre ?? lecture?.titre ?? '');

	const coches = vivantSelon(() => {
		const k = date;
		return () => db.coches.where('date').equals(k).toArray();
	}, [] as Coche[]);
	const faits = vivantSelon(() => {
		const k = date;
		return () => db.faits.where('date').equals(k).toArray();
	}, [] as Fait[]);
	const idsPratiques = $derived(new Set(vie.pratiques.map((p) => p.id)));
	const faites = (l: Ligne) =>
		idsPratiques.has(l.id) ? (faits.v.some((f) => f.pratiqueId === l.id) ? 1 : 0) : coches.v.filter((c) => c.elementId === l.id).length;

	/** Le texte d'une section, prêt à afficher (nom du saint à la place de « N. »). */
	function html(s: SectionResolue): string {
		const t = contenuDe(s, vie.corps);
		return rendre(s.nom ? avecLeNom(t, s.nom) : t);
	}
	const titreDe = (s: SectionResolue) => s.titre ?? (s.texte ? vie.textes.get(s.texte)?.titre : '') ?? '';
	/** Le titre d'un texte ne se répète pas : texte coupé en morceaux, invité dit à chaque dizaine. */
	const dernierMorceau = (k: number) =>
		!sections.slice(k + 1).some((x) => x.texte === sections[k].texte && x.origine === sections[k].origine);
	const nouveauTexte = (k: number) => !sections.slice(0, k).some((x) => x.texte === sections[k].texte && x.origine === sections[k].origine);

	// champ libre (intentions particulières) : une note du jour à part
	const intentions = vivantSelon(
		() => {
			const k = `intentions:${date}`;
			return () => db.notes.get(k);
		},
		undefined as NoteJour | undefined
	);
	async function noterIntentions(corps: string) {
		const k = `intentions:${date}`;
		const existante = await db.notes.get(k);
		if (existante) await enregistrer('notes', { ...existante, corps });
		else if (corps.trim()) await creer<NoteJour>('notes', { id: k, origine: 'personnel', date, corps });
	}
	const dateFr = $derived(new Date(date + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' }));
</script>

<svelte:head><title>{titre || 'Pratique'} — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour" href="/{date === iso(new Date()) ? '' : `?date=${date}`}"><Icone nom="retour" taille={16} /> Aujourd’hui</a>
	{#if !vie.jr}
		<p class="aide">Préparation de la page…</p>
	{:else if !ligne && !lecture}
		<p>Cette pratique n’est pas au programme du {dateFr}.</p>
	{:else}
		<div class="tete-page">
			<p class="etiquette">{dateFr}</p>
			<h1>{titre}</h1>
			{#if ligne?.heures?.length}<p class="petit">{ligne.heures.join(' · ')}</p>{/if}
			{#if ligne && minutesDUneRecitation(ligne, vie.corps) > 0}<p class="petit">
					≈ {enMinutes(minutesDUneRecitation(ligne, vie.corps))}
				</p>{/if}
			<Ornement nom="fleuron" />
		</div>
		{#each ligne?.annotations ?? [] as a (a.source)}
			<p class="annotation"><span class="rub">✠</span> {a.texte}</p>
		{/each}

		{#each sections as s, k (k)}
			{#if s.genre === 'champ'}
				<section class="champ">
					<h2 class="pc">{s.champ}</h2>
					<textarea rows="3" aria-label={s.champ} value={intentions.v?.corps ?? ''} onblur={(ev) => noterIntentions(ev.currentTarget.value)}
					></textarea>
				</section>
			{:else if s.genre === 'notice'}
				<details class="notice">
					<summary class="pc">{titreDe(s) || 'Notice'}</summary>
					<div class="lecture">{@html html(s)}</div>
				</details>
			{:else if s.depliable}
				<details class="depliable">
					<summary>{titreDe(s)}</summary>
					<div class="lecture">{@html html(s)}</div>
				</details>
			{:else}
				<section class="priere" class:invite={ligne && s.origine !== ligne.id}>
					{#if nouveauTexte(k)}
						<h2>
							{titreDe(s)}
							{#if s.heure}<span class="heure interface">à {s.heure}</span>{/if}
						</h2>
					{/if}
					<div class="lecture">{@html html(s)}</div>
					{#if s.texte && dernierMorceau(k)}
						<p class="seule"><a href="/prieres/{encodeURIComponent(s.texte)}">la prière seule, sa source et son indulgence</a></p>
					{/if}
				</section>
			{/if}
		{/each}

		{#if ligne}
			{@const n = recitations(ligne)}
			{@const f = faites(ligne)}
			<div class="fait">
				<Case libelle="{ligne.titre} : fait" bind:cochee={() => f >= n, () => cocher(ligne, date, f, idsPratiques)} />
				<span>{n > 1 ? `Récitations faites : ${f} sur ${n}` : f ? 'Fait' : 'Marquer comme fait'}</span>
			</div>
		{/if}
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
	.annotation {
		font-style: italic;
		color: var(--hs-encre-douce);
		margin: var(--hs-e2) 0;
	}
	.priere {
		margin-top: var(--hs-e5);
	}
	.priere.invite {
		padding-left: var(--hs-e3);
		border-left: var(--hs-cheveu) solid var(--hs-or-trait);
	}
	.priere h2 {
		font-size: var(--hs-t2);
		margin-bottom: var(--hs-e2);
	}
	.heure {
		font-size: var(--hs-t0);
		color: var(--hs-encre-douce);
		margin-left: 8px;
	}
	.seule {
		margin: var(--hs-e2) 0 0;
		font-size: 0.875rem;
		text-align: right;
	}
	.notice,
	.depliable {
		margin-top: var(--hs-e4);
		border-block: var(--hs-cheveu) solid var(--hs-filet);
	}
	.notice summary,
	.depliable summary {
		padding: 12px 0;
		cursor: pointer;
		color: var(--hs-encre-douce);
	}
	.champ {
		margin-top: var(--hs-e5);
	}
	.champ h2 {
		font-size: var(--hs-t1, 1rem);
		color: var(--hs-encre-douce);
	}
	.fait {
		display: flex;
		align-items: center;
		gap: 14px;
		margin: var(--hs-e7) 0 var(--hs-e5);
		padding-top: var(--hs-e4);
		border-top: var(--hs-cheveu) solid var(--hs-or-trait);
	}
</style>
