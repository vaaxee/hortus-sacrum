<script lang="ts">
	import { db } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { ancienneListe, annuler, META_BASCULE, reprendreTelleQuelle, type EtatBascule } from '#lib/programme/bascule.ts';
	import type { ElementListe } from '#lib/types.ts';
	import { vivantSelon } from '#lib/vivant.svelte.ts';

	/**
	 * Ce qui a changé à la refonte (décisions du 20 nov.) : la liste du jour a été remplacée par le programme unique. Chaque
	 * changement se défait ici ; chaque ancienne ligne peut être reprise telle qu'elle était, comme ajout personnel.
	 */
	const etat = vivantSelon(
		() => () => db.meta.get(META_BASCULE).then((m) => m?.valeur as EtatBascule | undefined),
		undefined as EtatBascule | undefined
	);
	let anciennes = $state<ElementListe[]>([]);
	ancienneListe().then((l) => (anciennes = l.filter((e) => !e.supprimeLe).sort((a, b) => a.ordre - b.ordre)));
	const reprises = vivantSelon(() => () => db.programme.toArray().then((r) => new Set(r.map((x) => x.id))), new Set<string>());
	const date = $derived(
		etat.v ? new Date(etat.v.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : ''
	);
	const JOURS = ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'];
	const jours = (e: ElementListe) =>
		e.jours?.every(Boolean) ? 'chaque jour' : (e.jours ?? []).flatMap((v, k) => (v ? [JOURS[k]] : [])).join(' ');
</script>

<svelte:head><title>Ce qui a changé — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<p class="etiquette"><a href="/programme">Régler le programme</a></p>
		<h1>Ce qui a changé</h1>
		<Ornement nom="fleuron" />
		<p class="petit">
			La liste du jour a été remplacée par le programme unique{date ? ` le ${date}` : ''} : chaque prière n’y paraît qu’une fois par jour, et
			les petites prières se disent à l’intérieur d’une autre page. Vos ajouts, vos durées et vos rappels ont été gardés. L’ancienne liste reste
			dans l’historique des versions.
		</p>
	</div>

	{#if etat.v?.changements.length}
		<section>
			<h2>Changements</h2>
			<ul>
				{#each etat.v.changements as c, i (i)}
					<li class:annule={c.annule}>
						<strong>{c.titre}</strong>
						<span>{c.texte}</span>
						{#if c.annuler && !c.annule}
							<button class="brut" onclick={() => annuler(c.annuler!, i)}>Annuler</button>
						{:else if c.annule}<span class="aide">Annulé.</span>{/if}
					</li>
				{/each}
			</ul>
		</section>
	{:else}
		<p class="aide">Aucun changement à signaler : cette installation n’avait pas d’ancienne liste.</p>
	{/if}

	{#if anciennes.length}
		<section>
			<h2>L’ancienne liste</h2>
			<p class="aide">Reprendre une ligne telle qu’elle était l’ajoute au programme comme prière personnelle.</p>
			<ul>
				{#each anciennes as e (e.id)}
					<li>
						<strong>{e.titre}</strong>
						<span class="aide"
							>{jours(e)}{e.rappels?.length ? ` · ${e.rappels.join(', ')}` : ''}{e.actif === false ? ' · désactivée' : ''}</span
						>
						{#if reprises.v.has(`perso:${e.id}:reprise`)}
							<span class="aide">Reprise.</span>
						{:else}
							<button class="brut" onclick={() => reprendreTelleQuelle($state.snapshot(e) as ElementListe)}>Reprendre telle quelle</button>
						{/if}
					</li>
				{/each}
			</ul>
		</section>
	{/if}
</main>

<style>
	section {
		margin-top: var(--hs-e6);
	}
	h2 {
		font-size: var(--hs-t2);
	}
	ul {
		list-style: none;
		padding: 0;
	}
	li {
		display: grid;
		gap: 4px;
		padding: 10px 0;
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
	}
	li.annule span:not(.aide) {
		text-decoration: line-through;
		color: var(--hs-encre-douce);
	}
	button {
		justify-self: start;
		background: none;
		border: 0;
		padding: 4px 0;
		color: var(--hs-rubrique);
		text-decoration: underline;
		font: inherit;
		cursor: pointer;
	}
</style>
