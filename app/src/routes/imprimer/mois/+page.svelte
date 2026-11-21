<script lang="ts">
	import { page } from '$app/state';
	import { iso, MOIS_DEVOTION, moisDu, NOMS_MOIS, teinte, type Jour } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { occurrences } from '#lib/pratiques.ts';
	import type { FetePerso, Pratique } from '#lib/types.ts';

	/** Calendrier d'un mois (A4 en largeur) : office, couleur, jeûne, fêtes personnelles et pratiques de chaque jour. */
	const m = $derived(page.url.searchParams.get('m') ?? iso(new Date()).slice(0, 7));
	const an = $derived(Number(m.slice(0, 4)));
	const mois = $derived(Number(m.slice(5, 7)));
	let jours = $state<Jour[]>([]);
	let fetes = $state<FetePerso[]>([]);
	let pratiques = $state<Pratique[]>([]);
	$effect(() => {
		const a = an,
			mo = mois;
		moisDu(a, mo).then((j) => (jours = j));
		db.fetes.toArray().then((f) => (fetes = f.filter((x) => !x.supprimeLe && x.mois === mo)));
		db.pratiques.toArray().then((p) => (pratiques = p.filter((x) => x.active && !x.supprimeLe && x.type !== 'roue')));
	});
	const fin = $derived(new Date(an, mois, 0).getDate());
	const decalage = $derived((new Date(an, mois - 1, 1).getDay() + 6) % 7); // semaine commençant le lundi
	const cases = $derived([...Array(decalage).fill(null), ...Array.from({ length: fin }, (_, i) => i + 1)]);
	const cle = (j: number) => `${m}-${String(j).padStart(2, '0')}`;
	const parDate = $derived(Object.fromEntries(jours.map((j) => [j.date, j])));
	const pratiquesDu = $derived.by(() => {
		const out: Record<string, string[]> = {};
		for (const p of pratiques) {
			for (const o of occurrences(p.regle, `${m}-01`, cle(fin)))
				(out[o.date] ??= []).push(o.total ? `${p.titre} ${o.rang}/${o.total}` : p.titre);
		}
		return out;
	});
	const JOURS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];
</script>

<svelte:head>
	<title>{NOMS_MOIS[mois]} {an} — Hortus Sacrum</title>
	{@html `<style>@page { size: A4 landscape; margin: 9mm 10mm; }</style>`}
</svelte:head>

<div class="ecran-seul barre">
	<a href="/imprimer">Retour</a>
	<button class="principal" onclick={() => window.print()}>Imprimer ou enregistrer en PDF</button>
</div>

<article class="cal">
	<header>
		<h1>{NOMS_MOIS[mois]} {an}</h1>
		<p class="devotion">{MOIS_DEVOTION[mois]?.nom}</p>
	</header>
	<div class="grille">
		{#each JOURS as j, i (i)}<div class="entete pc">{j}</div>{/each}
		{#each cases as n, i (i)}
			{#if n === null}<div class="vide"></div>
			{:else}
				{@const jr = parDate[cle(n)]}
				<div class="case" class:dimanche={i % 7 === 6}>
					<p class="num chiffres-alignes">
						{#if jr}<span class="pastille" style="--p: {teinte(jr)}"></span>{/if}{n}
					</p>
					{#if jr}<p class="office">{jr.office}</p>{/if}
					{#if jr?.jeune_abstinence}<p class="jeune">{jr.jeune_abstinence.libelle}</p>{/if}
					{#each fetes.filter((f) => f.jour === n) as f, i (i)}<p class="perso">✠ {f.titre}</p>{/each}
					{#each pratiquesDu[cle(n)] ?? [] as p, i (i)}<p class="prat">{p}</p>{/each}
				</div>
			{/if}
		{/each}
	</div>
	<div class="cul"><Ornement nom="fleuron" /></div>
</article>

<style>
	.barre {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 12px;
		max-width: 277mm;
		margin: 24px auto 12px;
		padding: 0 12px;
	}
	.cal {
		max-width: 277mm;
		margin: 0 auto;
		padding: 0 12px 120px;
		font-size: 7.5pt;
		line-height: 1.25;
	}
	header {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		border-bottom: 0.6pt solid var(--hs-or);
		margin-bottom: 4pt;
	}
	h1 {
		font-size: 18pt;
	}
	.devotion {
		margin: 0;
		font-family: var(--hs-titre);
		font-style: italic;
		font-size: 12pt;
		color: var(--hs-rubrique);
	}
	.grille {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		border-left: 0.5pt solid var(--hs-filet);
		border-top: 0.5pt solid var(--hs-filet);
	}
	.entete {
		text-align: center;
		padding: 2pt;
		font-size: 8pt;
		border-right: 0.5pt solid var(--hs-filet);
		border-bottom: 0.5pt solid var(--hs-filet);
		color: var(--hs-encre-douce);
	}
	.case,
	.vide {
		min-height: 27mm;
		padding: 2pt 3pt;
		border-right: 0.5pt solid var(--hs-filet);
		border-bottom: 0.5pt solid var(--hs-filet);
		overflow: hidden;
	}
	.case p {
		margin: 0 0 1pt;
	}
	.num {
		font-size: 10pt;
		display: flex;
		align-items: center;
		gap: 4px;
	}
	.dimanche .num {
		color: var(--hs-rubrique);
	}
	.pastille {
		width: 6pt;
		height: 6pt;
		border-radius: 50%;
		background: var(--p);
		border: 0.4pt solid var(--hs-or);
	}
	.office {
		font-family: var(--hs-lecture);
	}
	.jeune,
	.perso {
		color: var(--hs-rubrique);
	}
	.prat {
		color: var(--hs-encre-douce);
		font-style: italic;
	}
	.cul {
		max-width: 40mm;
		margin: 6pt auto 0;
	}
	@media print {
		.cal {
			max-width: none;
			padding: 0;
		}
		.case,
		.vide {
			min-height: 0;
			height: 30mm;
		}
	}
</style>
