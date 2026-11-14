<script lang="ts">
	import { goto } from '$app/navigation';
	import { iso } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import type { Texte } from '#lib/types.ts';

	/** Impressions : livret de prières (110 × 170 mm), fiche du jour, calendrier du mois. « Enregistrer en PDF » se fait depuis l'impression. */
	const textes = vivant(async () => (await db.textes.orderBy('ordre').toArray()).filter((t) => !t.supprimeLe), [] as Texte[]);
	const parties = $derived.by(() => {
		const m = new Map<string, Texte[]>();
		for (const t of $textes) m.set(t.partie || 'Autres prières', [...(m.get(t.partie || 'Autres prières') ?? []), t]);
		return [...m.entries()];
	});
	let choisis = $state<string[]>([]);
	let filtre = $state('');
	const basculer = (id: string) => (choisis = choisis.includes(id) ? choisis.filter((x) => x !== id) : [...choisis, id]);
	const visible = (t: Texte) => !filtre.trim() || t.titre.toLowerCase().includes(filtre.trim().toLowerCase());
	let titreLivret = $state('Mon livret de prières');

	let date = $state(iso(new Date()));
	let mois = $state(iso(new Date()).slice(0, 7));

	function composer() {
		const q = new URLSearchParams({ t: choisis.join(','), titre: titreLivret });
		goto(`/imprimer/livret?${q}`);
	}
</script>

<svelte:head><title>Imprimer — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<h1>Imprimer</h1>
		<Ornement nom="fleuron" />
		<p class="petit">Chaque page s’imprime, ou s’enregistre en PDF depuis la fenêtre d’impression de l’appareil.</p>
	</div>

	<section>
		<h2>Fiche du jour</h2>
		<p class="petit">Le propre du jour, la liste à cocher, la roue, les saints du martyrologe : une feuille A5.</p>
		<div class="rangee">
			<input type="date" bind:value={date} aria-label="Date de la fiche" />
			<a class="bouton principal" href="/imprimer/jour?date={date}">Préparer la fiche</a>
		</div>
	</section>

	<section>
		<h2>Calendrier du mois</h2>
		<p class="petit">Offices, couleurs, jeûnes, fêtes personnelles et dévotions du mois : une feuille A4 en largeur.</p>
		<div class="rangee">
			<input type="month" bind:value={mois} aria-label="Mois du calendrier" />
			<a class="bouton principal" href="/imprimer/mois?m={mois}">Préparer le calendrier</a>
		</div>
	</section>

	<section>
		<h2>Livret de prières</h2>
		<p class="petit">Format de poche, 110 × 170 mm. Cochez les prières dans l’ordre où elles doivent paraître.</p>
		<label><span>Titre du livret</span><input type="text" bind:value={titreLivret} /></label>
		<label><span>Chercher une prière</span><input type="search" bind:value={filtre} /></label>
		{#each parties as [partie, liste]}
			{@const vues = liste.filter(visible)}
			{#if vues.length}
				<fieldset>
					<legend>{partie}</legend>
					{#each vues as t (t.id)}
						<label class="case">
							<input type="checkbox" checked={choisis.includes(t.id)} onchange={() => basculer(t.id)} />
							<span class="nom">{t.titre}</span>
							{#if choisis.includes(t.id)}<span class="ordre chiffres-alignes">{choisis.indexOf(t.id) + 1}</span>{/if}
						</label>
					{/each}
				</fieldset>
			{/if}
		{/each}
		<div class="rangee bas">
			<button class="principal" disabled={!choisis.length} onclick={composer}>Composer le livret ({choisis.length})</button>
			{#if choisis.length}<button class="discret" onclick={() => (choisis = [])}>Tout décocher</button>{/if}
		</div>
	</section>
</main>

<style>
	section { margin-top: var(--hs-e6); }
	section h2 { font-size: var(--hs-t2); }
	.case { display: flex; align-items: baseline; gap: 10px; padding: 4px 0; }
	.case .nom { flex: 1; font-variant-caps: normal; letter-spacing: 0; font-size: 1.0625rem; color: var(--hs-encre); font-family: var(--hs-lecture); }
	.ordre { color: var(--hs-or-texte); font-size: 0.9375rem; }
	.bas { position: sticky; bottom: 96px; padding: var(--hs-e3) 0; background: var(--hs-fond); }
</style>
