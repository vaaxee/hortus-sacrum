<script lang="ts">
	import { page } from '$app/state';
	import { iso } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Case from '#lib/design/Case.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { ecrireRef, enClair, lectureDu } from '#lib/ecriture.ts';
	import { etatDesLectures } from '#lib/programme/lectures.ts';
	import { journeeVivante } from '#lib/programme/vivant.svelte.ts';
	import { elementDu } from '#lib/roues-calcul.ts';
	import type { Coche, Pratique } from '#lib/types.ts';
	import { vivantSelon } from '#lib/vivant.svelte.ts';

	/**
	 * Lecture (SPEC § 11) : ce qui se lit sort de la liste du jour. Quatre sections : Office, Écriture, Doctrine, Spirituel.
	 * « Lectures du jour (n/N) » se calcule ici comme sur Aujourd'hui (programme/lectures.ts) ; chaque lecture se coche,
	 * l'office heure par heure.
	 */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const q = $derived(page.url.searchParams.get('date') ? `?date=${date}` : '');
	const vie = journeeVivante(() => date);

	const cochesDuJour = vivantSelon(() => {
		const k = date;
		return () => db.coches.where('date').equals(k).toArray();
	}, [] as Coche[]);
	const coches = $derived.by(() => {
		const n: Record<string, number> = {};
		for (const c of cochesDuJour.v) n[c.elementId] = (n[c.elementId] ?? 0) + 1;
		return n;
	});
	const etat = $derived(vie.jr ? etatDesLectures(vie.jr, coches, vie.corps) : null);
	const de = (id: string) => etat?.lectures.find((x) => x.lecture.id === id);
	async function lire(id: string) {
		if (coches[id]) await db.coches.where('[date+elementId]').equals([date, id]).delete();
		else await db.coches.add({ date, elementId: id, rang: 0, horodatage: new Date().toISOString() });
	}

	const office = $derived.by(() => {
		const id = vie.jr?.lectures.find((l) => l.id === 'lec:office')?.sections.find((s) => s.texte)?.texte;
		return id ? vie.textes.get(id) : undefined;
	});
	let evangile = $state<{ href: string; libelle: string } | undefined>();
	$effect(() => {
		const d = date;
		db.pratiques.get('roue:lecture-evangiles').then((r: Pratique | undefined) => {
			const ref = r && !r.supprimeLe ? lectureDu(r, d, elementDu(r, d)) : undefined;
			evangile = ref ? { href: `/ecriture?ref=${encodeURIComponent(ecrireRef(ref))}`, libelle: enClair(ref) } : undefined;
		});
	});
</script>

<svelte:head><title>Lecture — Hortus Sacrum</title></svelte:head>

<main class="ecran entree">
	<header>
		<p class="etiquette">Lecture</p>
		<h1>Lectures du jour</h1>
		{#if etat}<p class="compte pc chiffres-alignes">{etat.lues} / {etat.total}</p>{/if}
		<Ornement nom="fleuron" />
	</header>

	<section aria-labelledby="t-office">
		<h2 id="t-office" class="pc rub">Office</h2>
		<ul class="lectures">
			<li class:lu={de('lec:office')?.lu}>
				<span class="avancement pc chiffres-alignes" aria-hidden="true">{de('lec:office')?.faites ?? 0}/{de('lec:office')?.total ?? 8}</span
				>
				<a href="/lecture/office{q}">
					<strong>Petit bréviaire du Sacré-Cœur</strong>
					<span
						>{office ? office.titre.replace('Petit bréviaire du Sacré-Cœur — ', '') : 'office du jour'} · une heure à la fois ; {de(
							'lec:office'
						)?.faites ?? 0} heure{(de('lec:office')?.faites ?? 0) > 1 ? 's' : ''} dite{(de('lec:office')?.faites ?? 0) > 1 ? 's' : ''}</span
					>
				</a>
			</li>
			<li class="sans-case">
				<a href="/lecture/office{q}"><strong>Bréviaire romain</strong><span>heures complètes en préparation ; leçons du jour</span></a>
			</li>
			<li class="sans-case">
				<a href="/lecture/office{q}"><strong>Officium parvum de la sainte Vierge</strong><span>en préparation</span></a>
			</li>
		</ul>
	</section>

	<section aria-labelledby="t-ecriture">
		<h2 id="t-ecriture" class="pc rub">Sainte Écriture</h2>
		<ul class="lectures">
			<li class:lu={de('lec:ecriture')?.lu}>
				<Case libelle="Évangile : lu" bind:cochee={() => !!de('lec:ecriture')?.lu, () => lire('lec:ecriture')} />
				<a href={evangile?.href ?? '/ecriture'}>
					<strong>Évangile</strong><span>{evangile?.libelle ?? 'les quatre Évangiles, à la suite'}</span>
				</a>
			</li>
		</ul>
	</section>

	<section aria-labelledby="t-doctrine">
		<h2 id="t-doctrine" class="pc rub">Doctrine</h2>
		<ul class="lectures">
			<li class="sans-case avenir-ligne">
				<strong>Somme théologique</strong>
				<p class="avenir">Un article par jour, traduction Lachat (1856), latin en regard : en préparation.</p>
			</li>
		</ul>
	</section>

	<section aria-labelledby="t-spirituel">
		<h2 id="t-spirituel" class="pc rub">Spirituel</h2>
		<ul class="lectures">
			<li class:lu={de('lec:meditation')?.lu}>
				<Case libelle="Méditation du jour : lue" bind:cochee={() => !!de('lec:meditation')?.lu, () => lire('lec:meditation')} />
				<a href="/meditation{q}"><strong>Méditation du jour</strong><span>selon le mois et le temps</span></a>
			</li>
			<li class="sans-case">
				<a href="/lecture/spirituel{q}"><strong>Tout le spirituel du jour</strong><span>office et vie du saint, Guéranger, roues</span></a>
			</li>
		</ul>
	</section>
</main>

<style>
	.ecran {
		max-width: 760px;
		margin: 0 auto;
		padding: var(--hs-e5) var(--hs-marge-mobile) var(--hs-e7);
	}
	header {
		text-align: center;
		margin-bottom: var(--hs-e5);
	}
	.compte {
		margin: 0;
		color: var(--hs-encre-douce);
	}
	section {
		margin-top: var(--hs-e5);
	}
	h2 {
		margin: 0 0 var(--hs-e2);
	}
	.lectures {
		list-style: none;
		margin: 0;
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
	.lectures li.avenir-ligne {
		display: grid;
	}
	.lectures a,
	.avenir-ligne {
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
	.avancement {
		flex: none;
		width: 26px;
		text-align: center;
		font-size: 0.8125rem;
		color: var(--hs-or-texte);
	}
	.lectures li.lu .avancement {
		color: var(--hs-vert);
	}
	.avenir {
		margin: 0 4px 10px;
		font-size: 0.9em;
		color: var(--hs-encre-douce);
	}
	.avenir-ligne .avenir {
		margin: 0;
	}
</style>
