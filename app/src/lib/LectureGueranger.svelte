<script lang="ts">
	import type { Jour } from './calendrier.ts';
	import { rendre } from './markup.ts';
	import { lecturesDuJour, type EntreeRecueil, type Recueil } from './meditations.ts';

	/** Lecture du jour tirée de Dom Guéranger, L'Année liturgique (repliée : les chapitres sont longs). */
	let { date, jour, titre = 'Lecture : Dom Guéranger, L’Année liturgique' }: { date: string; jour?: Jour; titre?: string } = $props();
	let res = $state<{ recueil: Omit<Recueil, 'entrees'>; entrees: EntreeRecueil[] } | null>(null);
	$effect(() => {
		const d = date, j = jour;
		res = null;
		lecturesDuJour(d, j).then((r) => (res = r));
	});
</script>

{#if res?.entrees.length}
	<section class="lecture-g" aria-label="Lecture du jour">
		<p class="pc rub centre">{titre}</p>
		{#each res.entrees as e}
			<details>
				<summary><span class="t">{e.titre || 'Lecture du jour'}</span> <span class="petit">t. {e.tome}</span></summary>
				<div class="lecture">{@html rendre(e.corps)}</div>
				<p class="source">{res.recueil.auteur}, <em>{res.recueil.titre}</em>, {res.recueil.editions[String(e.tome)]}. {res.recueil.provenance}.</p>
			</details>
		{/each}
	</section>
{/if}

<style>
	.lecture-g { max-width: var(--hs-mesure); margin: var(--hs-e7) auto 0; }
	.centre { text-align: center; }
	details { border-top: var(--hs-cheveu) solid var(--hs-filet); }
	details:last-child { border-bottom: var(--hs-cheveu) solid var(--hs-filet); }
	summary { padding: 12px 0; cursor: pointer; }
	.t { font-variant: small-caps; letter-spacing: 0.03em; }
	.petit { color: var(--hs-encre-douce); font-size: 0.875rem; }
	.lecture :global(p) { text-align: justify; hyphens: auto; }
	.source { font-size: 0.875rem; color: var(--hs-encre-douce); }
</style>
