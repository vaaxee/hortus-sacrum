<script lang="ts">
	import { page } from '$app/state';
	import { introitVersCorps, iso, jourDu, MOIS_DEVOTION, RANG, teinte, type Jour } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Arche from '#lib/design/Arche.svelte';
	import Case from '#lib/design/Case.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { invocation, TOUS_LES_SAINTS } from '#lib/invocations.ts';
	import { vivant } from '#lib/live.ts';
	import { rendre } from '#lib/markup.ts';
	import type { ElementListe, Moment } from '#lib/types.ts';

	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	let jour: Jour | undefined = $state();
	$effect(() => {
		jourDu(date).then((j) => (jour = j));
	});

	const d = $derived(new Date(date + 'T12:00:00'));
	const dateLongue = $derived(d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }));
	const solennel = $derived(jour?.rang === '1re cl.' || jour?.rang === 'dim. 1re cl.');

	const liste = vivant(() => db.liste.orderBy('ordre').toArray(), [] as ElementListe[]);
	const MOMENTS: [Moment, string][] = [['matin', 'Matin'], ['propre', 'Propre du jour'], ['journee', 'Au fil du jour'], ['soir', 'Soir']];
	const duJour = $derived($liste.filter((e) => e.actif && !e.supprimeLe && e.jours[d.getDay()]));
	let coches: Record<string, number> = $state({});
	const faits = $derived(duJour.filter((e) => (coches[e.id] ?? 0) >= Math.max(1, e.rappels.length)).length);

	/** Sous-titre des éléments du propre, tiré du calendrier. */
	function precision(e: ElementListe): string {
		if (!jour) return '';
		if (e.titre.startsWith('Office du jour')) return jour.office;
		if (e.titre.startsWith('Dévotion du mois')) return MOIS_DEVOTION[d.getMonth() + 1].nom;
		if (e.titre.startsWith('Dévotion à jours comptés')) return jour.devotions.filter((x) => x.type !== 'neuvaine').map((x) => x.libelle).join(' ; ');
		if (e.titre.startsWith('Neuvaine')) return jour.devotions.filter((x) => x.type === 'neuvaine').map((x) => x.libelle).join(' ; ');
		return '';
	}
	const ROMAINS = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix'];
</script>

<svelte:head><title>Aujourd’hui — Hortus Sacrum</title></svelte:head>

{#if jour}
	<div class="bandeau" style="background: {teinte(jour)}"></div>
	<main class="ecran entree">
		<header class="jour">
			<p class="date pc chiffres-alignes">{dateLongue}</p>
			<p class="temps etiquette">{jour.temps}</p>

			<Arche {solennel}>
				<span class="pastille" style="--pastille: {teinte(jour)}" title="Couleur liturgique : {jour.couleur}"></span>
				<h1 class:fete={solennel}>{jour.office}</h1>
				<p class="rang pc">{RANG[jour.rang] ?? jour.rang}</p>
				{#if jour.commemoraisons.length}
					<p class="comm"><span class="pc">Comm.</span> {jour.commemoraisons.join(' ; ')}</p>
				{/if}
				{#if jour.jeune_abstinence}<p class="jeune rub pc">{jour.jeune_abstinence.libelle}</p>{/if}
			</Arche>

			{#if jour.introit_incipit}
				<details class="introit">
					<summary>
						<span class="pc rub">Introït</span>
						<em lang="la">{jour.introit_incipit}</em>
						{#if jour.station}<span class="station imprime">{jour.station}</span>{/if}
					</summary>
					{#if jour.introit}
						<div class="colonnes">
							<div class="lecture" lang="la">{@html rendre(introitVersCorps(jour.introit.la))}</div>
							{#if jour.introit.fr}<div class="lecture">{@html rendre(introitVersCorps(jour.introit.fr))}</div>{/if}
						</div>
						<p class="source imprime">Missel romain, d’après Divinum Officium.</p>
					{/if}
				</details>
			{/if}
		</header>

		<section class="liste" aria-label="Liste du jour">
			<div class="avancement interface">
				<span class="etiquette">Le jardin du jour</span>
				<span class="trait"><span style="width: {duJour.length ? (100 * faits) / duJour.length : 0}%"></span></span>
				<span class="chiffres-alignes">{faits} / {duJour.length}</span>
			</div>

			{#each MOMENTS as [moment, nom]}
				{@const elements = duJour.filter((e) => e.moment === moment)}
				{#if elements.length}
					<div class="tete">
						<Ornement nom="grecque" />
						<h2>{nom}</h2>
					</div>
					<ul>
						{#each elements as e (e.id)}
							{@const total = Math.max(1, e.rappels.length)}
							{@const fait = coches[e.id] ?? 0}
							{@const sous = precision(e)}
							<li class:fini={fait >= total}>
								<Case
									libelle={e.titre}
									bind:cochee={() => fait >= total, (v) => (coches[e.id] = v ? Math.min(total, fait + 1) : 0)}
								/>
								<div class="corps">
									<span class="titre">{e.titre}</span>
									{#if sous}<span class="sous">{sous}</span>{/if}
									{#if e.rappels.length}<span class="heures interface">{e.rappels.join(', ')}</span>{/if}
								</div>
								{#if total > 1}
									<button class="medaillon" onclick={() => (coches[e.id] = (fait + 1) % (total + 1))}
										aria-label="{fait} sur {total} : compter une récitation de plus">
										<Ornement nom="medaillon" taille={34} />
										<span class="pc">{ROMAINS[fait] || '·'}<i>/</i>{ROMAINS[total]}</span>
									</button>
								{/if}
								<span class="genre pc" class:propre={e.etiquette === 'propre'}>{e.etiquette === 'propre' ? 'propre' : 'ord.'}</span>
							</li>
						{/each}
					</ul>
				{/if}
			{/each}
		</section>

		<section class="martyrologe" aria-label="Martyrologe">
			<div class="tete">
				<Ornement nom="grecque" />
				<h2>Martyrologe</h2>
				<p class="etiquette">Les saints de ce jour</p>
			</div>
			{#each jour.martyrologe.slice(0, 6) as m}
				{@const inv = invocation(m.texte)}
				<details class="eloge">
					<summary>
						{#if inv}<span class="invocation">{inv.texte}</span>{:else}<span class="invocation sans">{m.texte.split(/[.,]/)[0]}…</span>{/if}
					</summary>
					<p class="texte">{m.texte}</p>
					{#if m.texte_la}<p class="texte" lang="la">{m.texte_la}</p>{/if}
				</details>
			{/each}
			<p class="tous"><span class="rub">✠</span> {TOUS_LES_SAINTS}</p>
			<p class="source imprime">Martyrologe romain, traduction française donnée par Divinum Officium.</p>
		</section>

		<div class="cul"><Ornement nom="fleuron" /></div>
	</main>
{/if}

<style>
	.bandeau { height: 5px; border-bottom: var(--hs-cheveu) solid var(--hs-or-trait); }
	.ecran { max-width: var(--hs-colonne); margin: 0 auto; padding: var(--hs-e6) var(--hs-marge-mobile) 0; }
	.jour { text-align: center; }
	.date { margin: 0; font-size: 1.0625rem; color: var(--hs-encre-douce); }
	.temps { margin: 2px 0 var(--hs-e5); }
	h1 { font-size: var(--hs-t3); }
	h1.fete { color: var(--hs-rubrique); }
	.rang { margin: 0; color: var(--hs-encre-douce); font-size: 1.0625rem; }
	.comm { margin: 0; font-size: 1rem; font-style: italic; line-height: 1.4; text-wrap: balance; }
	.comm .pc { font-style: normal; color: var(--hs-encre-douce); }
	.jeune { margin: var(--hs-e2) 0 0; font-size: 1.0625rem; }

	.introit { margin-top: var(--hs-e5); border-block: var(--hs-cheveu) solid var(--hs-filet); text-align: left; }
	.introit summary { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: center; gap: 4px 12px; padding: var(--hs-e3) 0; }
	.station { font-size: 0.9375rem; color: var(--hs-encre-douce); font-style: italic; flex-basis: 100%; text-align: center; }
	.colonnes { display: grid; gap: var(--hs-e5); padding: var(--hs-e2) 0 var(--hs-e4); }
	.colonnes :global(.lecture p) { text-align: left; font-size: 1.0625rem; }
	.source { font-size: 0.875rem; color: var(--hs-encre-douce); font-style: italic; text-align: center; margin: 0 0 var(--hs-e4); }

	.liste { margin-top: var(--hs-e7); }
	.avancement { display: flex; align-items: center; gap: 12px; color: var(--hs-encre-douce); }
	.trait { flex: 1; height: 1px; background: var(--hs-filet); position: relative; }
	.trait span { position: absolute; inset: -1px auto -1px 0; background: var(--hs-vert); transition: width var(--hs-duree-lente) var(--hs-courbe); }

	.tete { margin-top: var(--hs-e7); text-align: center; display: grid; gap: var(--hs-e3); }
	.tete h2 { font-size: var(--hs-t2); }
	.tete .etiquette { margin: -6px 0 0; }
	ul { list-style: none; margin: var(--hs-e3) 0 0; padding: 0; }
	li { display: flex; align-items: center; gap: 14px; padding: 11px 0; border-bottom: var(--hs-cheveu) solid var(--hs-filet); min-height: 56px; }
	.corps { flex: 1; min-width: 0; display: grid; }
	.titre { line-height: 1.3; transition: color var(--hs-duree) var(--hs-courbe); }
	li.fini .titre { color: var(--hs-encre-douce); }
	.sous { font-style: italic; font-size: 1rem; line-height: 1.35; color: var(--hs-encre-douce); }
	.heures { color: var(--hs-encre-douce); font-size: 0.75rem; margin-top: 2px; }
	.genre { font-size: 0.9375rem; color: var(--hs-encre-douce); width: 3.2rem; text-align: right; flex: none; }
	.genre.propre { color: var(--hs-rubrique); }
	.medaillon { position: relative; flex: none; width: 34px; height: 34px; padding: 0; border: 0; background: none; color: var(--hs-or); cursor: pointer; line-height: 0; }
	.medaillon span { position: absolute; inset: 0; display: grid; place-items: center; grid-auto-flow: column; justify-content: center; color: var(--hs-encre); font-size: 0.8125rem; line-height: 1; }
	.medaillon i { font-style: normal; color: var(--hs-encre-douce); margin: 0 1px; }
	li.fini .medaillon { color: var(--hs-vert); }

	.eloge { border-bottom: var(--hs-cheveu) solid var(--hs-filet); }
	.eloge summary { padding: 10px 0; }
	.invocation::before { content: '✠'; color: var(--hs-rubrique); margin-right: 10px; font-size: 0.8em; }
	.invocation.sans { color: var(--hs-encre-douce); font-style: italic; }
	.invocation.sans::before { content: '·'; }
	.texte { margin: 0 0 12px 1.5rem; font-size: 1.0625rem; text-align: justify; hyphens: auto; }
	.tous { text-align: center; margin: var(--hs-e5) 0 var(--hs-e2); font-style: italic; }
	.martyrologe .tete { margin-bottom: var(--hs-e3); }
	.cul { margin: var(--hs-e7) auto 0; max-width: 16rem; }

	@media (min-width: 700px) {
		h1 { font-size: var(--hs-t4); }
		.colonnes { grid-template-columns: 1fr 1fr; }
	}
</style>
