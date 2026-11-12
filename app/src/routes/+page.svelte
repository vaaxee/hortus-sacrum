<script lang="ts">
	import { onMount } from 'svelte';

	interface Jour {
		date: string;
		jour: string;
		temps: string;
		office: string;
		rang: string;
		couleur: string;
		commemoraisons: string[];
		introit_incipit: string | null;
		station: string | null;
		jeune_abstinence: { code: string; libelle: string } | null;
		devotions: { type: string; libelle: string; page_jardin: number | null }[];
	}

	let jour: Jour | undefined = $state();
	let charge = $state(false);
	const aujourdhui = new Date();
	const iso = `${aujourdhui.getFullYear()}-${String(aujourdhui.getMonth() + 1).padStart(2, '0')}-${String(aujourdhui.getDate()).padStart(2, '0')}`;

	onMount(async () => {
		const y = aujourdhui.getFullYear();
		for (const a of [y - 1, y]) {
			try {
				const r = await fetch(`/data/calendar/${a}-${a + 1}.json`);
				if (!r.ok) continue;
				const trouve = ((await r.json()) as Jour[]).find((j) => j.date === iso);
				if (trouve) {
					jour = trouve;
					break;
				}
			} catch {
				/* année non générée */
			}
		}
		charge = true;
	});

	const dateLongue = aujourdhui.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
</script>

<svelte:head><title>Aujourd’hui — Hebdomada</title></svelte:head>

<main class="page">
	<p class="petit date">{dateLongue}</p>
	{#if jour}
		<p class="petit temps">{jour.temps}</p>
		<h1><span class="pastille {jour.couleur}" title="Couleur : {jour.couleur}"></span>{jour.office}</h1>
		<p class="rang">{jour.rang}</p>
		{#if jour.commemoraisons.length}<p class="petit">Comm. {jour.commemoraisons.join(' ; ')}</p>{/if}
		{#if jour.introit_incipit}
			<p class="petit">Intr. <em>{jour.introit_incipit}</em>{#if jour.station} · <em>{jour.station}</em>{/if}</p>
		{/if}
		{#if jour.jeune_abstinence}<p class="jeune">{jour.jeune_abstinence.libelle}</p>{/if}
		{#each jour.devotions as d}
			<p class="petit">{d.type === 'neuvaine' ? '◦' : '❧'} {d.libelle}{#if d.page_jardin} — <em>Jardin</em>, p. {d.page_jardin}{/if}</p>
		{/each}
	{:else if charge}
		<h1>Hebdomada in Dei servitio</h1>
		<p class="petit">Le calendrier de cette année n’est pas encore généré.</p>
	{/if}

	<hr class="filet" />
	<p class="petit">
		La liste du jour, le martyrologe et les suivis arrivent aux étapes suivantes. La bibliothèque de prières est déjà
		entièrement modifiable : <a href="/prieres">ouvrir les prières</a>.
	</p>
</main>

<style>
	.date { text-transform: capitalize; margin: 0; }
	.temps { margin: 0.2rem 0 0.6rem; font-variant: small-caps; letter-spacing: 0.05em; }
	.rang { margin: 0.2rem 0 0.5rem; font-style: italic; }
	.jeune { color: var(--rubrique); font-style: italic; margin: 0.4rem 0; }
	.pastille { display: inline-block; width: 0.7rem; height: 0.7rem; border-radius: 50%; margin-right: 0.5rem; vertical-align: 0.1rem; border: 1px solid var(--encre-douce); }
	.pastille.violet { background: var(--violet); }
	.pastille.rouge { background: var(--rouge); }
	.pastille.vert { background: var(--vert); }
	.pastille.rose { background: var(--rose); }
	.pastille.noir { background: #000; }
	.pastille.blanc { background: #fff; }
</style>
