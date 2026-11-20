<script lang="ts">
	import { page } from '$app/state';
	import { iso } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { ecrireRef, enClair, lectureDu } from '#lib/ecriture.ts';
	import { SELON_LE_JOUR } from '#lib/liste.ts';
	import { elementDu } from '#lib/roues-calcul.ts';
	import type { Pratique, Texte } from '#lib/types.ts';

	/**
	 * Lecture (SPEC § 11) : ce qui se lit sort de la liste du jour. Quatre sections : Office, Écriture, Doctrine, Spirituel.
	 * Les contenus encore à venir (Bréviaire romain complet, Officium parvum, Somme théologique) sont annoncés comme tels.
	 */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const q = $derived(page.url.searchParams.get('date') ? `?date=${date}` : '');

	let office = $state<Texte | undefined>();
	let evangile = $state<{ href: string; libelle: string } | undefined>();
	$effect(() => {
		const d = date;
		const id = SELON_LE_JOUR['hortus:petit-breviaire-du-jour'][new Date(d + 'T12:00:00').getDay()];
		db.textes.get(id).then((t) => (office = t));
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
		<Ornement nom="fleuron" />
	</header>

	<section aria-labelledby="t-office">
		<h2 id="t-office" class="pc rub">Office</h2>
		<ul class="lectures">
			<li>
				<a href={office ? `/prieres/${encodeURIComponent(office.id)}` : '/prieres'}>
					<strong>Petit bréviaire du Sacré-Cœur</strong>
					<span>{office ? office.titre.replace('Petit bréviaire du Sacré-Cœur — ', '') : 'office du jour'}</span>
				</a>
			</li>
			<li>
				<a href="/saint{q}"><strong>Bréviaire romain</strong><span>leçons du jour et vie du saint</span></a>
				<p class="avenir">Heures complètes (rubriques d’avant 1955) : en préparation.</p>
			</li>
			<li class="avenir-ligne">
				<strong>Officium parvum de la sainte Vierge</strong>
				<p class="avenir">En préparation.</p>
			</li>
		</ul>
	</section>

	<section aria-labelledby="t-ecriture">
		<h2 id="t-ecriture" class="pc rub">Sainte Écriture</h2>
		<ul class="lectures">
			<li>
				<a href={evangile?.href ?? '/ecriture'}>
					<strong>Évangile</strong><span>{evangile?.libelle ?? 'les quatre Évangiles, à la suite'}</span>
				</a>
			</li>
		</ul>
	</section>

	<section aria-labelledby="t-doctrine">
		<h2 id="t-doctrine" class="pc rub">Doctrine</h2>
		<ul class="lectures">
			<li class="avenir-ligne">
				<strong>Somme théologique</strong>
				<p class="avenir">Un article par jour, traduction Lachat (1856), latin en regard : en préparation.</p>
			</li>
		</ul>
	</section>

	<section aria-labelledby="t-spirituel">
		<h2 id="t-spirituel" class="pc rub">Spirituel</h2>
		<ul class="lectures">
			<li><a href="/meditation{q}"><strong>Méditation du jour</strong><span>selon le mois et le temps</span></a></li>
			<li><a href="/saint{q}"><strong>Office et vie du saint</strong><span>avec la prière de sainte Gertrude</span></a></li>
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
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
	}
	.lectures a,
	.avenir-ligne {
		display: grid;
		gap: 2px;
		padding: 12px 4px;
		min-height: 44px;
		text-decoration: none;
		color: var(--hs-encre);
	}
	.lectures span {
		color: var(--hs-encre-douce);
		font-style: italic;
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
