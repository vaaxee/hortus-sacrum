<script lang="ts">
	import CarteCouronne from '#lib/design/CarteCouronne.svelte';
	import { couronnesDeLaBase, type Couronne } from '#lib/couronnes.ts';
	import { iso } from '#lib/calendrier.ts';
	import { creer, db, enregistrer, mettreALaCorbeille, nouvelId } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import type { FetePerso } from '#lib/types.ts';
	import Reglages from '#lib/Reglages.svelte';

	/**
	 * Le Profil, une seule page (REFONTE § 4.1) : profil spirituel en tête, puis les entrées (Historique, Couronnes,
	 * Fêtes personnelles, Imprimer), puis les réglages techniques. L'ancienne adresse /reglages mène à « #reglages ».
	 * Profil spirituel : sacrements reçus, consécrations, saint patron et saints aimés.
	 * Chaque ligne est une fête personnelle (même table que /fetes) : anniversaire rappelé, saint rappelé la veille.
	 */
	const fetes = vivant(async () => (await db.fetes.toArray()).filter((f) => !f.supprimeLe), [] as FetePerso[]);
	const SACREMENTS: [string, string][] = [
		['bapteme', 'Baptême'],
		['confirmation', 'Confirmation'],
		['communion', 'Première communion'],
		['mariage', 'Mariage'],
		['ordre', 'Ordination ou profession religieuse']
	];
	const TITRES: Record<string, string> = {
		bapteme: 'Anniversaire de mon baptême',
		confirmation: 'Anniversaire de ma confirmation',
		communion: 'Anniversaire de ma première communion',
		mariage: 'Anniversaire de mon mariage',
		ordre: 'Anniversaire de mon ordination ou de ma profession'
	};
	const du = (cle: string) => $fetes.filter((f) => f.profil === cle).sort((a, b) => a.mois - b.mois || a.jour - b.jour);
	const versDate = (f: FetePerso) => (f.annee ? `${f.annee}-${String(f.mois).padStart(2, '0')}-${String(f.jour).padStart(2, '0')}` : '');
	const auj = new Date();
	function depuis(f: FetePerso): string {
		if (!f.annee) return '';
		const n =
			auj.getFullYear() - f.annee - (auj.getMonth() + 1 < f.mois || (auj.getMonth() + 1 === f.mois && auj.getDate() < f.jour) ? 1 : 0);
		return n > 0 ? `il y a ${n} an${n > 1 ? 's' : ''}` : 'cette année';
	}
	const dateFr = (f: FetePerso) =>
		new Date(f.annee ?? 2000, f.mois - 1, f.jour).toLocaleDateString(
			'fr-FR',
			f.annee ? { day: 'numeric', month: 'long', year: 'numeric' } : { day: 'numeric', month: 'long' }
		);

	/** Enregistre la date d'un sacrement (une seule ligne par sacrement). */
	async function sacrement(cle: string, nom: string, valeur: string) {
		const existant = du(cle)[0];
		if (!valeur) return existant && mettreALaCorbeille('fetes', existant.id);
		const [a, m, j] = valeur.split('-').map(Number);
		const titre = TITRES[cle] ?? `Anniversaire : ${nom}`;
		if (existant) await enregistrer('fetes', { ...existant, annee: a, mois: m, jour: j });
		else
			await creer<FetePerso>('fetes', {
				id: nouvelId(),
				origine: 'personnel',
				titre,
				genre: 'anniversaire',
				mois: m,
				jour: j,
				annee: a,
				rappelVeille: true,
				notes: '',
				profil: cle
			});
	}

	let nouveau = $state<{ cle: string; titre: string; date: string } | null>(null);
	function ajouter(cle: string) {
		nouveau = { cle, titre: '', date: '' };
	}
	async function valider() {
		if (!nouveau || !nouveau.titre.trim() || !nouveau.date) return;
		const [a, m, j] = nouveau.date.split('-').map(Number);
		const saint = nouveau.cle !== 'consecration';
		await creer<FetePerso>('fetes', {
			id: nouvelId(),
			origine: 'personnel',
			titre: nouveau.titre.trim(),
			genre: saint ? 'saint' : 'anniversaire',
			mois: m,
			jour: j,
			...(saint ? {} : { annee: a }),
			rappelVeille: true,
			notes: '',
			profil: nouveau.cle
		});
		nouveau = null;
	}
	let tresor = $state<Couronne[]>([]);
	$effect(() => {
		couronnesDeLaBase(iso(new Date())).then((c) => (tresor = c));
	});
	let ouverte = $state('');
	const GENRES: [Couronne['genre'], string][] = [
		['serie', 'Séries accomplies'],
		['mois', 'Mois entiers'],
		['constance', 'Constance'],
		['lecture', 'Lectures']
	];
	const RUBRIQUES: [string, string, string, string][] = [
		[
			'consecration',
			'Consécrations',
			'Ex. : consécration à Jésus par Marie, cordon de saint Joseph, scapulaire…',
			'Date de la consécration'
		],
		[
			'patron',
			'Saint patron et fête patronale',
			'Le saint dont vous portez le nom : un rappel la veille de sa fête.',
			'Jour de sa fête (l’année ne compte pas)'
		],
		['saint', 'Saints aimés', 'Un rappel la veille de leur fête.', 'Jour de sa fête (l’année ne compte pas)']
	];
</script>

<svelte:head><title>Profil — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<h1>Profil</h1>
		<Ornement nom="fleuron" />
		<p class="petit">
			Les grâces reçues et les protecteurs choisis ; leurs anniversaires et leurs fêtes reviennent dans la journée et dans les rappels.
		</p>
	</div>

	<section>
		<h2>Sacrements reçus</h2>
		{#each SACREMENTS as [cle, nom] (cle)}
			{@const f = du(cle)[0]}
			<div class="ligne">
				<label
					><span>{nom}</span><input
						type="date"
						value={f ? versDate(f) : ''}
						onchange={(ev) => sacrement(cle, nom, ev.currentTarget.value)}
					/></label
				>
				{#if f}<p class="depuis">{depuis(f)}</p>{/if}
			</div>
		{/each}
	</section>

	{#each RUBRIQUES as [cle, nom, aide, libelleDate] (cle)}
		<section>
			<h2>{nom}</h2>
			<p class="aide">{aide}</p>
			<ul>
				{#each du(cle) as f (f.id)}
					<li>
						<span class="nom">{f.titre}</span>
						<span class="quand"
							>{dateFr(f)}{#if f.annee}
								· {depuis(f)}{/if}{#if f.rappelVeille}
								· rappel la veille{/if}</span
						>
						<button class="discret" onclick={() => mettreALaCorbeille('fetes', f.id)} aria-label="Retirer {f.titre}">retirer</button>
					</li>
				{/each}
			</ul>
			{#if nouveau?.cle === cle}
				<div class="ajout">
					<label><span>{cle === 'consecration' ? 'Consécration' : 'Saint'}</span><input type="text" bind:value={nouveau.titre} /></label>
					<label><span>{libelleDate}</span><input type="date" bind:value={nouveau.date} /></label>
					<div class="rangee">
						<button class="principal" onclick={valider}>Ajouter</button><button class="discret" onclick={() => (nouveau = null)}
							>Annuler</button
						>
					</div>
				</div>
			{:else}
				<button onclick={() => ajouter(cle)}>Ajouter</button>
			{/if}
		</section>
	{/each}

	<p class="petit fin">Toutes ces dates se retrouvent, modifiables, dans <a href="/fetes">les fêtes personnelles</a>.</p>

	<nav class="portes" aria-label="Profil">
		<a href="/historique"><span class="pc">Historique</span><em>régularité et constance</em></a>
		<a href="#couronnes"><span class="pc">Couronnes</span><em>les quêtes achevées</em></a>
		<a href="/fetes"><span class="pc">Fêtes personnelles</span><em>anniversaires et saints aimés</em></a>
		<a href="/imprimer"><span class="pc">Imprimer</span><em>livret, fiche du jour, calendrier</em></a>
		<a href="#reglages"><span class="pc">Réglages</span><em>compte, rappels, apparence, sauvegarde, corbeille</em></a>
	</nav>

	<section class="tresor" id="couronnes">
		<h2>Couronnes</h2>
		<p class="aide">
			Les quêtes achevées sans manquer de jour : séries à jours comptés, mois entiers, constance, lectures. Un jour manqué fait recommencer
			la série.
		</p>
		{#if tresor.length}
			{#each GENRES as [g, nom] (g)}
				{@const cs = tresor.filter((c) => c.genre === g)}
				{#if cs.length}
					<h3 class="pc">{nom}</h3>
					<ul>
						{#each cs as c (c.id)}
							<li class="couronne">
								<button
									class="brut ligne-couronne"
									onclick={() => (ouverte = ouverte === c.id ? '' : c.id)}
									aria-expanded={ouverte === c.id}
								>
									<span class="nom"
										>✠ {c.titre}{#if c.fois > 1}
											<span class="fois">({c.fois}e fois)</span>{/if}</span
									>
									<span class="quand"
										>{new Date(c.date + 'T12:00:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}</span
									>
								</button>
								{#if ouverte === c.id}<CarteCouronne {c} />{/if}
							</li>
						{/each}
					</ul>
				{/if}
			{/each}
		{:else}
			<p class="vide">Aucune couronne encore. La première viendra avec la première série menée jusqu’au bout.</p>
		{/if}
	</section>

	<hr class="filet" />

	<section id="reglages">
		<h2>Réglages</h2>
		<Reglages />
	</section>
</main>

<style>
	.portes {
		display: grid;
		gap: 0;
		margin-top: var(--hs-e4);
		border-top: var(--hs-cheveu) solid var(--hs-filet);
	}
	.portes a {
		display: grid;
		padding: 12px 0;
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
		text-decoration: none;
		color: var(--hs-encre);
	}
	.portes em {
		font-size: 1rem;
		color: var(--hs-encre-douce);
	}
	@media (min-width: 640px) {
		.portes {
			grid-template-columns: 1fr 1fr;
			column-gap: var(--hs-e5);
		}
	}
	section {
		margin-top: var(--hs-e6);
	}
	section h2 {
		font-size: var(--hs-t2);
		margin-bottom: var(--hs-e2);
	}
	.ligne {
		display: flex;
		align-items: flex-end;
		gap: var(--hs-e3);
		flex-wrap: wrap;
		margin: var(--hs-e2) 0;
	}
	.ligne label {
		flex: 1 1 14rem;
	}
	.depuis {
		margin: 0 0 8px;
		font-style: italic;
		color: var(--hs-encre-douce);
	}
	ul {
		list-style: none;
		padding: 0;
		margin: 0 0 var(--hs-e3);
	}
	li {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 4px 12px;
		padding: 8px 0;
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
	}
	.nom {
		flex: 1 1 12rem;
	}
	.quand {
		color: var(--hs-encre-douce);
		font-style: italic;
		font-size: 1rem;
	}
	.ajout {
		display: grid;
		gap: var(--hs-e3);
		margin: var(--hs-e3) 0;
	}
	.tresor h3 {
		font-size: 0.8rem;
		margin: var(--hs-e4) 0 var(--hs-e2);
		color: var(--hs-or-texte);
	}
	.couronne {
		display: block;
	}
	.ligne-couronne {
		background: none;
		border: 0;
		color: inherit;
		font: inherit;
		display: flex;
		flex-wrap: wrap;
		gap: 4px 12px;
		align-items: baseline;
		width: 100%;
		text-align: left;
		cursor: pointer;
		padding: 0;
	}
	.fois {
		color: var(--hs-encre-douce);
		font-size: 0.9em;
	}
	.vide {
		font-style: italic;
		color: var(--hs-encre-douce);
	}
	.fin {
		margin-top: var(--hs-e6);
		text-align: center;
	}
</style>
