<script lang="ts">
	import { db } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import { etat, regleEnClair, versIso, type Etat } from '#lib/pratiques.ts';
	import { importerPlan } from '#lib/seed.ts';
	import { chargerProgramme } from '#lib/programme/charger.ts';
	import type { Programme } from '#lib/programme/types.ts';
	import type { Fait, Pratique, Texte } from '#lib/types.ts';

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
	// En cours ; ce mois-ci (prochain jour avant la fin du mois) ; plus tard, groupé par mois (REFONTE § 4.6)
	const finDuMois = aujourdhui.slice(0, 8) + '31';
	const enCours = $derived(lignes.filter((l) => l.e.phase === 'en_cours'));
	// ouvertes à une date passée sans aucune coche : pas « en cours » (audit du 20 nov.)
	const nonCommencees = $derived(lignes.filter((l) => l.e.phase === 'non_commencee'));
	const aVenir = $derived(lignes.filter((l) => (l.e.phase === 'a_venir' || l.e.phase === 'permanente') && l.e.prochaine));
	const ceMois = $derived(aVenir.filter((l) => l.e.prochaine!.date <= finDuMois));
	const plusTard = $derived.by(() => {
		const m = new Map<string, typeof lignes>();
		for (const l of aVenir.filter((x) => x.e.prochaine!.date > finDuMois)) {
			const k = l.e.prochaine!.date.slice(0, 7);
			m.set(k, [...(m.get(k) ?? []), l]);
		}
		return [...m.entries()];
	});
	const nomDuMois = (k: string) => new Date(k + '-15T12:00:00').toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' });

	// pages explicatives : pratiques qui se lisent (règles, port d'un scapulaire, confréries) et non des prières du jour
	let programme = $state.raw<Programme | null>(null);
	chargerProgramme().then((x) => (programme = x));
	const textes = vivant(() => db.textes.toArray(), [] as Texte[]);
	const EXPLICATIVES = [
		'beringer:cordon-saint-joseph',
		'jardin:heure-sainte',
		'jardin:offrandes-de-la-garde-d-honneur',
		'jardin:priere-de-la-milice-angelique',
		'jardin:acte-heroique-de-charite',
		'jardin:premiers-vendredis-du-mois',
		'jardin:premiers-samedis-du-mois',
		'jardin:treize-mardis-de-saint-antoine',
		'jardin:quinze-mardis-de-saint-dominique',
		'jardin:sept-dimanches-de-saint-joseph',
		'jardin:douze-samedis-avant-l-immaculee-conception',
		'jardin:quinze-samedis-du-rosaire'
	];
	const explicatives = $derived.by(() => {
		const ids = [...new Set([...(programme?.entrees.flatMap((e) => e.explication ?? []) ?? []), ...EXPLICATIVES])];
		const par = new Map($textes.filter((t) => !t.supprimeLe).map((t) => [t.id, t]));
		return ids.flatMap((id) => (par.get(id) ? [par.get(id)!] : []));
	});
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
	{#snippet ligne(p: Pratique, e: Etat)}
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
	{/snippet}

	<section>
		<div class="tete-section">
			<Ornement nom="grecque" />
			<h2>En cours</h2>
		</div>
		<ul class="reglee">
			{#each enCours as { p, e } (p.id)}
				{@render ligne(p, e)}
			{:else}
				<li class="vide petit">Aucune série en cours.</li>
			{/each}
		</ul>
	</section>

	{#if nonCommencees.length}
		<section>
			<div class="tete-section">
				<Ornement nom="grecque" />
				<h2>Ouvertes, pas commencées</h2>
			</div>
			<p class="petit">Ces séries ont commencé sans vous : rien n’est coché. Vous pouvez les commencer aujourd’hui.</p>
			<ul class="reglee">
				{#each nonCommencees as { p, e } (p.id)}
					{@render ligne(p, e)}
				{/each}
			</ul>
		</section>
	{/if}

	<section>
		<div class="tete-section">
			<Ornement nom="grecque" />
			<h2>Ce mois-ci</h2>
		</div>
		<ul class="reglee">
			{#each ceMois as { p, e } (p.id)}
				{@render ligne(p, e)}
			{:else}
				<li class="vide petit">Rien d’autre ce mois-ci.</li>
			{/each}
		</ul>
	</section>

	{#if plusTard.length}
		<details class="reste">
			<summary>Plus tard ({plusTard.reduce((a, [, l]) => a + l.length, 0)})</summary>
			{#each plusTard as [mois, groupe] (mois)}
				<h3 class="mois">{nomDuMois(mois)}</h3>
				<ul class="reglee">
					{#each groupe as { p, e } (p.id)}
						{@render ligne(p, e)}
					{/each}
				</ul>
			{/each}
		</details>
	{/if}

	{#if explicatives.length}
		<details class="reste">
			<summary>Pages explicatives ({explicatives.length})</summary>
			<p class="petit">
				Ce qui se lit et se règle une fois : conditions des séries, scapulaire, confréries. Ce ne sont pas des prières du jour.
			</p>
			<ul class="reglee">
				{#each explicatives as t (t.id)}
					<li>
						<a href="/prieres/{encodeURIComponent(t.id)}"><span class="titre">{t.titre}</span></a>
					</li>
				{/each}
			</ul>
		</details>
	{/if}

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

	<div class="rangee administration">
		<a class="bouton principal" href="/devotions/nouvelle">Ajouter une pratique</a>
		<button onclick={reprendrePlan}>Reprendre le plan de l’année</button>
		<a class="bouton" href="/roue">La roue symbolique</a>
	</div>
	{#if message}<p class="petit" role="status">{message}</p>{/if}
</main>

<style>
	.administration {
		margin-top: var(--hs-e6);
	}
	.mois {
		margin: var(--hs-e4) 0 0;
		font-size: var(--hs-t1, 1rem);
		color: var(--hs-encre-douce);
		text-transform: capitalize;
	}
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
