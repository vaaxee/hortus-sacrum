<script lang="ts">
	import { page } from '$app/state';
	import { iso, jourDu, RANG, teinte, type Jour } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import { occurrenceDu } from '#lib/pratiques.ts';
	import type { FetePerso, Pratique } from '#lib/types.ts';

	/** Semaine liturgique, du dimanche au samedi, comme le calendrier papier. */
	const ref = $derived(new Date((page.url.searchParams.get('d') ?? iso(new Date())) + 'T12:00:00'));
	const dimanche = $derived(new Date(ref.getFullYear(), ref.getMonth(), ref.getDate() - ref.getDay(), 12));
	const dates = $derived(Array.from({ length: 7 }, (_, i) => iso(new Date(dimanche.getFullYear(), dimanche.getMonth(), dimanche.getDate() + i, 12))));
	const decaler = (n: number) => iso(new Date(dimanche.getFullYear(), dimanche.getMonth(), dimanche.getDate() + 7 * n, 12));

	let jours: (Jour | undefined)[] = $state([]);
	$effect(() => {
		Promise.all(dates.map((d) => jourDu(d))).then((j) => (jours = j));
	});
	const pratiques = vivant(() => db.pratiques.toArray(), [] as Pratique[]);
	const fetes = vivant(() => db.fetes.toArray(), [] as FetePerso[]);

	// filtres (SPEC §1) : ce que l'on veut voir sous chaque jour
	let voir = $state({ fetes: true, jeunes: true, devotions: true, perso: true });
	const FILTRES: [keyof typeof voir, string][] = [['fetes', 'Fêtes'], ['jeunes', 'Jeûnes'], ['devotions', 'Dévotions'], ['perso', 'Mes fêtes']];

	const duJour = (d: string) =>
		$pratiques.filter((p) => p.active && !p.supprimeLe).map((p) => ({ p, o: occurrenceDu(p, d) })).filter((x) => x.o);
	const persoDu = (d: string) => {
		const x = new Date(d + 'T12:00:00');
		return $fetes.filter((f) => !f.supprimeLe && f.mois === x.getMonth() + 1 && f.jour === x.getDate());
	};
	const GRANDS = ['1re cl.', '2e cl.', 'dim. 1re cl.', 'dim. 2e cl.', 'dim.'];
	const titreSemaine = $derived.by(() => {
		const f = (s: string, mois = true) => new Date(s + 'T12:00:00').toLocaleDateString('fr-FR', mois ? { day: 'numeric', month: 'long' } : { day: 'numeric' });
		return `Du ${f(dates[0])} au ${f(dates[6])}`;
	});
	const aujourdhui = iso(new Date());
</script>

<svelte:head><title>Semaine — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="vues rangee" role="group" aria-label="Vue">
		<a class="bouton" href="/calendrier?m={dates[3].slice(0, 7)}">Mois</a>
		<span class="bouton actif" aria-current="page">Semaine</span>
		<a class="bouton" href="/calendrier/annee">Année</a>
	</div>

	<div class="tete-page">
		<div class="titre-semaine">
			<a class="pas" href="/calendrier/semaine?d={decaler(-1)}" aria-label="Semaine précédente"><Icone nom="retour" taille={20} /></a>
			<h1>{titreSemaine}</h1>
			<a class="pas" href="/calendrier/semaine?d={decaler(1)}" aria-label="Semaine suivante"><Icone nom="chevron" taille={20} /></a>
		</div>
		{#if jours[0]}<p class="petit">{jours[0].temps}</p>{/if}
	</div>

	<div class="filtres rangee" role="group" aria-label="Afficher">
		{#each FILTRES as [k, nom]}
			<button aria-pressed={voir[k]} onclick={() => (voir[k] = !voir[k])}>{nom}</button>
		{/each}
	</div>

	<table class="ordo">
		<tbody>
			{#each dates as d, i (d)}
				{@const j = jours[i]}
				{@const x = new Date(d + 'T12:00:00')}
				<tr class:auj={d === aujourdhui} class:dimanche={x.getDay() === 0}>
					<td class="p">{#if j}<span class="pastille" style="--pastille: {teinte(j)}" title={j.couleur}></span>{/if}</td>
					<td class="d pc chiffres-alignes">
						<a href="/?date={d}">{x.toLocaleDateString('fr-FR', { weekday: 'short' })}<br /><span class="n">{x.getDate()}</span></a>
					</td>
					<td class="o">
						{#if j}
							<a href="/?date={d}" class="office" class:fete={voir.fetes && (j.est_fete_sanctorale || GRANDS.includes(j.rang)) && GRANDS.slice(0, 2).includes(j.rang)}>{j.office}</a>
							<span class="r pc">{RANG[j.rang] ?? j.rang}</span>
							{#if voir.fetes && j.commemoraisons.length}<span class="ligne">Comm. {j.commemoraisons.join(' ; ')}</span>{/if}
							{#if voir.jeunes && j.jeune_abstinence}<span class="ligne jeune">{j.jeune_abstinence.libelle}</span>{/if}
							{#if voir.devotions}
								{#each duJour(d) as { p, o } (p.id)}
									<a class="ligne devotion" href="/devotions/{encodeURIComponent(p.id)}">❧ {p.titre}{o?.total ? `, ${o.rang}/${o.total}` : ''}</a>
								{/each}
							{/if}
							{#if voir.perso}
								{#each persoDu(d) as f (f.id)}<span class="ligne perso">✠ {f.titre}</span>{/each}
							{/if}
						{:else}
							<span class="petit">Calendrier non généré pour ce jour.</span>
						{/if}
					</td>
				</tr>
			{/each}
		</tbody>
	</table>

	<div class="cul"><Ornement nom="fleuron" /></div>
</main>

<style>
	.vues { justify-content: center; margin-bottom: var(--hs-e5); gap: 0; }
	.vues .bouton { min-height: 36px; border-radius: 0; }
	.vues .actif { background: color-mix(in srgb, var(--hs-lapis) 14%, transparent); border-color: var(--hs-or); }
	.titre-semaine { display: flex; align-items: center; justify-content: center; gap: var(--hs-e2); }
	.titre-semaine h1 { font-size: var(--hs-t2); }
	.pas { display: inline-grid; place-items: center; width: 44px; height: 44px; color: var(--hs-encre-douce); flex: none; }
	.filtres { justify-content: center; gap: 6px; margin-bottom: var(--hs-e4); }
	.filtres button { min-height: 34px; padding: 0 12px; }
	.filtres button[aria-pressed='false'] { border-color: var(--hs-filet); color: var(--hs-encre-douce); }

	.ordo { width: 100%; border-collapse: collapse; }
	.ordo td { padding: 10px 0; border-bottom: var(--hs-cheveu) solid var(--hs-filet); vertical-align: top; }
	.ordo tr:first-child td { border-top: var(--hs-cheveu) solid var(--hs-filet); }
	tr.auj td { background: color-mix(in srgb, var(--hs-or) 10%, transparent); }
	.p { width: 22px; padding-top: 16px !important; }
	.d { width: 3.6rem; font-size: 1rem; line-height: 1.1; }
	.d a { color: var(--hs-encre-douce); text-decoration: none; }
	.d .n { font-size: 1.375rem; color: var(--hs-encre); }
	tr.dimanche .d .n, tr.dimanche .office { color: var(--hs-rubrique); }
	.o { line-height: 1.3; }
	.office { color: var(--hs-encre); text-decoration: none; }
	.office.fete { color: var(--hs-rubrique); }
	.r { display: block; font-size: 0.9375rem; color: var(--hs-encre-douce); }
	.ligne { display: block; font-size: 1rem; margin-top: 3px; color: var(--hs-encre-douce); text-decoration: none; }
	.jeune { color: var(--hs-rubrique); font-style: italic; }
	.devotion { color: var(--hs-lapis); }
	.perso { color: var(--hs-encre); font-style: italic; }
	.cul { margin: var(--hs-e7) auto 0; max-width: 16rem; }
</style>
