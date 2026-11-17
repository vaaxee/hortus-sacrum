<script lang="ts">
	import { db } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import { etat, regleEnClair, versIso, type Etat } from '#lib/pratiques.ts';
	import { importerPlan } from '#lib/seed.ts';
	import type { Fait, Pratique } from '#lib/types.ts';

	// les roues symboliques ont leur page (/roue)
	const pratiques = vivant(async () => (await db.pratiques.toArray()).filter((p) => p.type !== 'roue'), [] as Pratique[]);
	const faits = vivant(() => db.faits.toArray(), [] as Fait[]);
	const aujourdhui = versIso(new Date());

	const parPratique = $derived.by(() => {
		const m = new Map<string, Set<string>>();
		for (const f of $faits) m.set(f.pratiqueId, (m.get(f.pratiqueId) ?? new Set()).add(f.date));
		return m;
	});
	const lignes = $derived(
		$pratiques
			.filter((p) => !p.supprimeLe && p.active)
			.map((p) => ({ p, e: etat(p, aujourdhui, parPratique.get(p.id) ?? new Set()) }))
			.sort((a, b) => (a.e.prochaine?.date ?? '9').localeCompare(b.e.prochaine?.date ?? '9'))
	);
	const GROUPES: [Etat['phase'], string, string][] = [
		['en_cours', 'En cours', 'Aucune série en cours. Ajoutez une neuvaine, un trentain ou une série.'],
		['a_venir', 'À venir', ''],
		['permanente', 'Chaque mois, chaque année', '']
	];
	const terminees = $derived(lignes.filter((l) => l.e.phase === 'terminee'));
	const masquees = $derived($pratiques.filter((p) => !p.supprimeLe && !p.active));
	const corbeille = $derived($pratiques.filter((p) => p.supprimeLe));

	const dateCourte = (s: string) =>
		new Date(s + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' });
	const quand = (e: Etat) =>
		!e.prochaine ? '' : e.prochaine.date === aujourdhui ? 'aujourd’hui' : `prochain jour : ${dateCourte(e.prochaine.date)}`;

	let message = $state('');
	async function reprendrePlan() {
		const n = await importerPlan();
		message = n
			? `${n} pratique${n > 1 ? 's ajoutées' : ' ajoutée'} depuis le plan de l’année.`
			: 'Toutes les pratiques du plan sont déjà là.';
	}
</script>

<svelte:head><title>Dévotions — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<h1>Dévotions</h1>
		<Ornement nom="fleuron" />
	</div>
	<div class="rangee">
		<a class="bouton principal" href="/devotions/nouvelle">Ajouter une pratique</a>
		<button onclick={reprendrePlan}>Reprendre le plan de l’année</button>
		<a class="bouton" href="/roue">La roue symbolique</a>
	</div>
	{#if message}<p class="petit" role="status">{message}</p>{/if}

	{#each GROUPES as [phase, nom, vide]}
		{@const groupe = lignes.filter((l) => l.e.phase === phase)}
		{#if groupe.length || vide}
			<section>
				<div class="tete-section">
					<Ornement nom="grecque" />
					<h2>{nom}</h2>
				</div>
				<ul class="reglee">
					{#each groupe as { p, e } (p.id)}
						<li>
							<a href="/devotions/{encodeURIComponent(p.id)}">
								<span class="titre">{p.titre}</span>
								<span class="detail">{regleEnClair(p.regle)}{quand(e) ? ` ; ${quand(e)}` : ''}</span>
								{#if e.manquees.length}
									<span class="alerte">Série interrompue : {e.manquees.length} jour{e.manquees.length > 1 ? 's' : ''} sans coche</span>
								{/if}
							</a>
							{#if e.serie.length}
								<span class="medaillon" class:plein={e.faites === e.serie.length} title="{e.faites} sur {e.serie.length}">
									<Ornement nom="medaillon" taille={40} />
									<span class="chiffres-alignes">{e.faites}<i>/</i>{e.serie.length}</span>
								</span>
							{/if}
						</li>
					{:else}
						<li class="vide petit">{vide}</li>
					{/each}
				</ul>
			</section>
		{/if}
	{/each}

	{#if terminees.length || masquees.length || corbeille.length}
		<details class="reste">
			<summary>Passées, masquées et corbeille ({terminees.length + masquees.length + corbeille.length})</summary>
			<ul class="reglee">
				{#each [...terminees.map((l) => l.p), ...masquees, ...corbeille] as p (p.id)}
					<li>
						<a href="/devotions/{encodeURIComponent(p.id)}">
							<span class="titre">{p.titre}</span>
							<span class="detail"
								>{p.supprimeLe
									? 'dans la corbeille'
									: !p.active
										? 'masquée'
										: parPratique.get(p.id)?.size
											? 'terminée'
											: 'passée, non commencée'}</span
							>
						</a>
					</li>
				{/each}
			</ul>
		</details>
	{/if}
</main>

<style>
	.tete-page :global(.filet) {
		max-width: 16rem;
	}
	li a {
		flex: 1;
		min-width: 0;
		display: grid;
		padding: 10px 0;
		text-decoration: none;
		color: var(--hs-encre);
	}
	.titre {
		line-height: 1.3;
		overflow-wrap: anywhere;
	}
	.detail {
		font-size: 1rem;
		font-style: italic;
		color: var(--hs-encre-douce);
		line-height: 1.35;
	}
	.alerte {
		font-size: 1rem;
		color: var(--hs-rubrique);
		font-variant-caps: all-small-caps;
		letter-spacing: var(--hs-chasse-petites-cap);
	}
	.medaillon {
		position: relative;
		flex: none;
		width: 40px;
		height: 40px;
		color: var(--hs-or);
		line-height: 0;
	}
	.medaillon span {
		position: absolute;
		inset: 0;
		display: grid;
		grid-auto-flow: column;
		place-items: center;
		justify-content: center;
		color: var(--hs-encre);
		font-family: var(--hs-interface);
		font-size: 0.6875rem;
		line-height: 1;
	}
	.medaillon i {
		font-style: normal;
		color: var(--hs-encre-douce);
		margin: 0 1px;
	}
	.medaillon.plein {
		color: var(--hs-vert);
	}
	li.vide {
		padding: 12px 0;
	}
	.reste {
		margin-top: var(--hs-e7);
		border-top: var(--hs-cheveu) solid var(--hs-filet);
	}
	.reste summary {
		padding: 12px 0;
		color: var(--hs-encre-douce);
		font-variant-caps: all-small-caps;
		letter-spacing: var(--hs-chasse-petites-cap);
	}
</style>
