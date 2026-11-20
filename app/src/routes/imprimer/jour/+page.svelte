<script lang="ts">
	import { page } from '$app/state';
	import { iso, jourDu, RANG, teinte, type Jour } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { invocation } from '#lib/invocations.ts';
	import { elementDu } from '#lib/roues.ts';
	import type { FetePerso, Pratique } from '#lib/types.ts';
	import type { Ligne, Moment } from '#lib/programme/types.ts';
	import { journeeVivante } from '#lib/programme/vivant.svelte.ts';

	/** Fiche du jour (A5) : propre, liste à cocher, roue, saints du martyrologe, place pour une note. */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const d = $derived(new Date(date + 'T12:00:00'));
	const dateLongue = $derived(d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }));

	let jour = $state<Jour | undefined>();
	const vie = journeeVivante(() => date);
	let pratiques = $state<Pratique[]>([]);
	let fetes = $state<FetePerso[]>([]);
	let titres = $state<Record<string, string>>({});
	$effect(() => {
		const dt = date,
			dd = d;
		jourDu(dt).then((j) => (jour = j));
		db.pratiques.toArray().then((p) => (pratiques = p.filter((x) => !x.supprimeLe && (x.active || x.type === 'roue'))));
		db.fetes
			.where('[mois+jour]')
			.equals([dd.getMonth() + 1, dd.getDate()])
			.toArray()
			.then((f) => (fetes = f.filter((x) => !x.supprimeLe)));
		db.textes.toArray().then((t) => (titres = Object.fromEntries(t.map((x) => [x.id, x.titre]))));
	});
	const MOMENTS: [Moment, string][] = [
		['matin', 'Matin'],
		['journee', 'Au fil du jour'],
		['soir', 'Soir']
	];
	/** Sous-titre : la prière du jour quand elle varie, et les pratiques du plan qui qualifient la ligne. */
	function sous(l: Ligne): string {
		const v = l.sections.find((x) => x.genre === 'texte' && x.origine === l.id && x.variante);
		return [v?.texte ? titres[v.texte] : '', ...l.annotations.map((a) => a.texte)].filter(Boolean).join(' · ');
	}
	const lectures = $derived((vie.jr?.lectures ?? []).filter((l) => l.compte));
	const roue = $derived(
		pratiques
			.filter((p) => p.type === 'roue' && p.active && !p.liste && (p.elements?.length ?? 0) > 1)
			.sort((a, b) => (a.elements?.length ?? 0) - (b.elements?.length ?? 0))
			.map((p) => ({ titre: p.titre, e: elementDu(p, date) }))
	);
</script>

<svelte:head>
	<title>Fiche du {date} — Hortus Sacrum</title>
	{@html `<style>@page { size: A5; margin: 11mm 12mm 12mm; }</style>`}
</svelte:head>

<div class="ecran-seul barre">
	<a href="/imprimer">Retour</a>
	<button class="principal" onclick={() => window.print()}>Imprimer ou enregistrer en PDF</button>
</div>

{#if jour}
	<article class="fiche">
		<header>
			<p class="date pc">{dateLongue}</p>
			<p class="temps">{jour.temps}</p>
			<h1><span class="pastille" style="--p: {teinte(jour)}"></span>{jour.office}</h1>
			<p class="rang">
				{RANG[jour.rang] ?? jour.rang}{#if jour.commemoraisons.length}
					— comm. {jour.commemoraisons.join(' ; ')}{/if}
			</p>
			{#if jour.jeune_abstinence}<p class="rub">{jour.jeune_abstinence.libelle}</p>{/if}
			{#each fetes as f}<p class="rub">✠ {f.titre}</p>{/each}
			{#if jour.introit_incipit}<p class="introit">
					<span class="pc">Introït</span> <em lang="la">{jour.introit_incipit}</em>{#if jour.station}
						· {jour.station}{/if}
				</p>{/if}
		</header>

		{#each MOMENTS as [m, nom] (m)}
			{@const el = (vie.jr?.lignes ?? []).filter((l) => l.moment === m)}
			{#if el.length}
				<h2>{nom}</h2>
				<ul>
					{#each el as l (l.id)}
						<li>
							<span class="case"></span>{l.titre}{#if sous(l)}
								<em>— {sous(l)}</em>{/if}{#if (l.heures?.length ?? 0) > 1}
								<span class="fois">({l.heures!.join(', ')})</span>{/if}
						</li>
					{/each}
					{#if m === 'journee'}
						{#if lectures.length}
							<li><span class="case"></span>Lectures du jour : {lectures.map((l) => l.titre).join(' · ')}</li>
						{/if}
						{#if roue.length}
							<li class="roue">
								<span class="case"></span>La roue du jour : {roue
									.map((r) => r.e?.fr)
									.filter(Boolean)
									.join(' · ')}
							</li>
						{/if}
					{/if}
				</ul>
			{/if}
		{/each}

		<h2>Martyrologe</h2>
		<p class="saints">
			{jour.martyrologe
				.map((x) => invocation(x.texte)?.texte)
				.filter(Boolean)
				.join(' — ')}
		</p>

		<h2>Note</h2>
		<div class="lignes"></div>
		<div class="cul"><Ornement nom="fleuron" /></div>
	</article>
{/if}

<style>
	.barre {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 12px;
		max-width: 148mm;
		margin: 24px auto 12px;
		padding: 0 12px;
	}
	.fiche {
		max-width: 148mm;
		margin: 0 auto;
		padding: 0 12px 120px;
		font-size: 10pt;
		line-height: 1.4;
	}
	header {
		text-align: center;
		border-bottom: 0.6pt solid var(--hs-or);
		padding-bottom: 6pt;
	}
	.date {
		margin: 0;
		color: var(--hs-encre-douce);
		font-size: 10pt;
	}
	.temps {
		margin: 0;
		font-style: italic;
		color: var(--hs-encre-douce);
		font-size: 9pt;
	}
	h1 {
		font-size: 15pt;
		margin: 4pt 0 2pt;
		display: flex;
		gap: 8px;
		align-items: center;
		justify-content: center;
	}
	.pastille {
		width: 9pt;
		height: 9pt;
		border-radius: 50%;
		background: var(--p);
		border: 0.5pt solid var(--hs-or);
		flex: none;
	}
	.rang,
	.introit,
	.rub {
		margin: 1pt 0;
		font-size: 9pt;
	}
	.rub {
		color: var(--hs-rubrique);
	}
	h2 {
		font-family: var(--hs-titre);
		font-style: italic;
		font-size: 12pt;
		color: var(--hs-rubrique);
		margin: 8pt 0 2pt;
	}
	ul {
		list-style: none;
		margin: 0;
		padding: 0;
		columns: 2;
		column-gap: 8mm;
	}
	li {
		break-inside: avoid;
		padding: 1.5pt 0;
		display: flex;
		gap: 6px;
		align-items: baseline;
	}
	li em {
		color: var(--hs-encre-douce);
	}
	li.roue {
		column-span: all;
	}
	.case {
		flex: none;
		width: 7pt;
		height: 7pt;
		border: 0.6pt solid var(--hs-encre);
		transform: translateY(1pt);
	}
	.fois {
		color: var(--hs-encre-douce);
		font-size: 8pt;
	}
	.saints {
		margin: 0;
		font-size: 9pt;
		font-style: italic;
	}
	.lignes {
		height: 22mm;
		background: repeating-linear-gradient(transparent 0 6.5mm, var(--hs-filet) 6.5mm calc(6.5mm + 0.5pt));
	}
	.cul {
		max-width: 40mm;
		margin: 6pt auto 0;
	}
	@media print {
		.fiche {
			max-width: none;
			padding: 0;
		}
	}
</style>
