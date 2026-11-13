<script lang="ts">
	import { onMount } from 'svelte';
	import { iso, jourDu, type Jour } from '#lib/calendrier.ts';
	import Ornement from '#lib/design/Ornement.svelte';

	/** Dévotions des trente prochains jours, d'après le plan de l'année (calendrier). */
	let jours: Jour[] = $state([]);
	let charge = $state(false);

	onMount(async () => {
		const d = new Date();
		const out: Jour[] = [];
		for (let i = 0; i < 30; i++) {
			const j = await jourDu(iso(d));
			if (j?.devotions.length) out.push(j);
			d.setDate(d.getDate() + 1);
		}
		jours = out;
		charge = true;
	});

	const dateCourte = (s: string) =>
		new Date(s + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' });
</script>

<svelte:head><title>Dévotions — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<h1>Dévotions</h1>
		<Ornement nom="fleuron" />
		<p class="petit">Les trente prochains jours, d’après le plan de l’année.</p>
	</div>

	{#if jours.length}
		<table class="ordo">
			<tbody>
				{#each jours as j}
					<tr>
						<td class="d pc chiffres-alignes"><a href="/?date={j.date}">{dateCourte(j.date)}</a></td>
						<td>
							{#each j.devotions as dv}
								<p class:neuvaine={dv.type === 'neuvaine'}>
									{dv.libelle}{#if dv.page_jardin}<span class="ref imprime">Jardin, p. {dv.page_jardin}</span>{/if}
								</p>
							{/each}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{:else if charge}
		<p class="petit vide">Aucune dévotion à jours comptés ni neuvaine dans les trente prochains jours.</p>
	{/if}

	<p class="aide suite">
		Les compteurs, les séries interrompues et l’édition de vos propres pratiques arrivent à l’étape suivante.
	</p>
</main>

<style>
	.tete-page :global(.filet) { max-width: 16rem; }
	.ordo { width: 100%; border-collapse: collapse; }
	.ordo td { padding: 9px 0; border-bottom: var(--hs-cheveu) solid var(--hs-filet); vertical-align: baseline; }
	.ordo tr:first-child td { border-top: var(--hs-cheveu) solid var(--hs-filet); }
	.d { width: 6.2rem; white-space: nowrap; font-size: 1.0625rem; }
	.d a { color: var(--hs-encre-douce); text-decoration: none; }
	.ordo p { margin: 0; line-height: 1.35; }
	.ordo p + p { margin-top: 4px; }
	.neuvaine { font-style: italic; color: var(--hs-encre-douce); }
	.ref { margin-left: 0.5em; font-size: 0.9375rem; color: var(--hs-encre-douce); font-style: italic; }
	.vide { text-align: center; }
	.suite { margin-top: var(--hs-e6); text-align: center; }
</style>
