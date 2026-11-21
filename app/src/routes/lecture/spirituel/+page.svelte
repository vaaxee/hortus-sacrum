<script lang="ts">
	import { page } from '$app/state';
	import { iso } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Case from '#lib/design/Case.svelte';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { priereDuSaint } from '#lib/gertrude.ts';
	import { journeeVivante } from '#lib/programme/vivant.svelte.ts';
	import type { Coche } from '#lib/types.ts';
	import { vivantSelon } from '#lib/vivant.svelte.ts';

	/**
	 * Lecture › Spirituel (REFONTE § 4.4) : la méditation du jour (comptée dans « Lectures du jour »), l'office et la vie du
	 * saint avec la prière de sainte Gertrude à la fin, Guéranger, le verset des roues ; les Visites en avril.
	 */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const q = $derived(page.url.searchParams.get('date') ? `?date=${date}` : '');
	const vie = journeeVivante(() => date);
	const cochesDuJour = vivantSelon(() => {
		const k = date;
		return () => db.coches.where('date').equals(k).toArray();
	}, [] as Coche[]);
	const lu = (id: string) => cochesDuJour.v.some((c) => c.elementId === id);
	async function lire(id: string) {
		if (lu(id)) await db.coches.where('[date+elementId]').equals([date, id]).delete();
		else await db.coches.add({ date, elementId: id, rang: 0, horodatage: new Date().toISOString() });
	}
	const gertrude = $derived(vie.jour ? priereDuSaint(vie.jour.office, vie.jour.est_fete_sanctorale) : null);
	const avril = $derived(date.slice(5, 7) === '04');
	const jourDuMois = $derived(Number(date.slice(8, 10)));
</script>

<svelte:head><title>Spirituel — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour" href="/lecture{q}"><Icone nom="retour" taille={16} /> Lecture</a>
	<div class="tete-page">
		<p class="etiquette">Lecture</p>
		<h1>Spirituel</h1>
		<Ornement nom="fleuron" />
	</div>

	<ul class="lectures">
		<li class:lu={lu('lec:meditation')}>
			<Case libelle="Méditation du jour : lue" bind:cochee={() => lu('lec:meditation'), () => lire('lec:meditation')} />
			<a href="/meditation{q}"><strong>Méditation du jour</strong><span>le livre du mois, sinon Hamon ou Chaignon ; Guéranger</span></a>
		</li>
		<li class:lu={lu('lec:saint')}>
			<Case libelle="Office et vie du saint : lus" bind:cochee={() => lu('lec:saint'), () => lire('lec:saint')} />
			<a href="/saint{q}">
				<strong>Office et vie du saint</strong>
				<span
					>{vie.jour?.office ?? 'le saint du jour'}{gertrude
						? ` ; à la fin, la prière de sainte Gertrude${gertrude.nom ? ` à ${gertrude.nom}` : ''}`
						: ''}</span
				>
			</a>
		</li>
		<li class="sans-case">
			<a href="/roue{q}"><strong>Les roues du jour</strong><span>le verset de chaque roue, et ce qu’il ouvre</span></a>
		</li>
		<li class="sans-case">
			<a href="/recueils"
				><strong>Bibliothèque des méditations</strong><span>Hamon, Chaignon, les livres des mois, Guéranger, les leçons du Bréviaire</span
				></a
			>
		</li>
		{#if avril}
			<li class="sans-case">
				<a href="/recueils?r=liguori-visites"
					><strong>Visites au Saint-Sacrement</strong><span>mois eucharistique : la visite du {jourDuMois}</span></a
				>
			</li>
		{/if}
	</ul>
	<p class="aide">Seule la méditation compte dans « Lectures du jour » ; le reste se lit à volonté.</p>
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
	.lectures {
		list-style: none;
		margin: var(--hs-e4) 0 0;
		padding: 0;
		border-top: var(--hs-cheveu) solid var(--hs-filet);
	}
	.lectures li {
		display: flex;
		align-items: center;
		gap: 14px;
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
	}
	.lectures li.sans-case {
		padding-left: 40px;
	}
	.lectures a {
		flex: 1;
		display: grid;
		gap: 2px;
		padding: 12px 4px;
		min-height: 44px;
		text-decoration: none;
		color: var(--hs-encre);
	}
	.lectures li.lu strong {
		color: var(--hs-encre-douce);
	}
	.lectures span {
		color: var(--hs-encre-douce);
		font-style: italic;
	}
</style>
