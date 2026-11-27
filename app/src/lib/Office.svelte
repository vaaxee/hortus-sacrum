<script lang="ts">
	import { db } from './db.ts';
	import Case from './design/Case.svelte';
	import { rendre } from './markup.ts';
	import { cocheDeLHeure, heureCourante, type Heure } from './programme/heures.ts';
	import { extraire } from './programme/texte.ts';

	/**
	 * Un office à plusieurs heures (Petit bréviaire du Sacré-Cœur ; plus tard le Bréviaire romain et l'Officium parvum) :
	 * une rangée de boutons, une heure à la fois, l'heure courante choisie à l'ouverture. Chaque heure se coche à part
	 * (coche « <ligne>:<heure> ») ; l'office est lu quand toutes ses heures canoniales le sont.
	 */
	let {
		corps,
		heures,
		ligne,
		date,
		coches,
		maintenant = new Date(),
		rendu = rendre
	}: {
		corps: string;
		heures: Heure[];
		/** Identifiant de la lecture ou de la ligne (« lec:office »). */
		ligne: string;
		date: string;
		/** Coches du jour, par identifiant. */
		coches: Record<string, number>;
		maintenant?: Date;
		/** Rendu HTML d'une heure (par défaut le balisage léger ; le Bréviaire romain y met le français de Fillion en regard). */
		rendu?: (texte: string) => string;
	} = $props();

	let choisie = $state<string | undefined>();
	const heure = $derived(heures.find((h) => h.cle === choisie) ?? heureCourante(heures, maintenant) ?? heures[0]);
	const dite = (h: Heure) => (coches[cocheDeLHeure(ligne, h.cle)] ?? 0) > 0;
	async function basculer(h: Heure) {
		const id = cocheDeLHeure(ligne, h.cle);
		if (dite(h)) await db.coches.where('[date+elementId]').equals([date, id]).delete();
		else await db.coches.add({ date, elementId: id, rang: 0, horodatage: new Date().toISOString() });
	}
	const canoniales = $derived(heures.filter((h) => h.canoniale));
	const faites = $derived(canoniales.filter(dite).length);
</script>

<div class="office">
	<div class="heures" role="tablist" aria-label="Heures de l’office">
		{#each heures as h (h.cle)}
			<button
				class="heure brut"
				class:dite={dite(h)}
				class:annexe={!h.canoniale}
				role="tab"
				aria-selected={heure?.cle === h.cle}
				onclick={() => (choisie = h.cle)}
				>{h.nom}{#if dite(h)}<span class="signe" aria-label="dite"> ✓</span>{/if}</button
			>
		{/each}
	</div>
	<p class="avancement interface">{faites} / {canoniales.length} heures dites</p>

	{#if heure}
		<div class="texte-heure" role="tabpanel" aria-label={heure.titre}>
			<div class="lecture">{@html rendu(extraire(corps, heure.extrait) ?? '')}</div>
			<div class="dire">
				<Case libelle="{heure.nom} : dite" bind:cochee={() => dite(heure), () => basculer(heure)} />
				<span>{dite(heure) ? `${heure.nom} : dite` : `Marquer ${heure.nom.toLowerCase()} comme dite`}</span>
			</div>
		</div>
	{/if}
</div>

<style>
	.heures {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		margin: var(--hs-e3) 0 var(--hs-e2);
	}
	.heures .heure {
		flex: none;
		min-height: 36px;
		padding: 4px 12px;
		border: var(--hs-cheveu) solid var(--hs-filet);
		border-radius: 999px;
		background: none;
		color: var(--hs-encre-douce);
		font-family: var(--hs-interface);
		font-size: 0.875rem;
		line-height: 1.2;
		cursor: pointer;
	}
	.heures .heure.annexe {
		font-style: italic;
	}
	.heures .heure.dite {
		color: var(--hs-vert);
		border-color: color-mix(in srgb, var(--hs-vert) 50%, var(--hs-filet));
	}
	.heures .heure[aria-selected='true'] {
		color: var(--hs-encre);
		border-color: var(--hs-or-trait);
		background: color-mix(in srgb, var(--hs-or) 18%, var(--hs-fond));
		font-weight: 600;
	}
	.avancement {
		margin: 0 0 var(--hs-e4);
		font-size: var(--hs-t0);
		color: var(--hs-encre-douce);
	}
	/* psaumes du Bréviaire romain : latin, et le français de Fillion en regard (même disposition que les prières bilingues) */
	.lecture :global(.psaume) {
		margin-bottom: var(--hs-ligne);
	}
	.lecture :global(.strophe) {
		display: grid;
		gap: var(--hs-e1);
		margin-bottom: var(--hs-e2);
	}
	.lecture :global(.strophe p) {
		margin: 0;
		text-align: left;
		hyphens: manual;
	}
	/* le latin est le texte de l'office : même allure que le reste de l'heure (pas l'italique du latin « en regard ») */
	.lecture :global(.strophe .la) {
		font-style: normal;
	}
	.lecture :global(.strophe .fr),
	.lecture :global(.fr-bloc) {
		color: var(--hs-encre-douce);
		padding-left: var(--hs-e4);
		border-left: var(--hs-cheveu) solid var(--hs-or-trait);
	}
	.lecture :global(.fr-bloc) {
		margin-bottom: var(--hs-ligne);
	}
	.lecture :global(.fr-bloc p) {
		text-align: left;
	}
	@media (min-width: 900px) {
		.lecture :global(.strophe) {
			grid-template-columns: 1fr 1fr;
			gap: var(--hs-e6);
		}
		.lecture :global(.strophe .fr) {
			padding-left: var(--hs-e6);
		}
	}
	.dire {
		display: flex;
		align-items: center;
		gap: 14px;
		margin: var(--hs-e6) 0 var(--hs-e4);
		padding-top: var(--hs-e4);
		border-top: var(--hs-cheveu) solid var(--hs-or-trait);
	}
</style>
