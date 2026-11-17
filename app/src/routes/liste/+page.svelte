<script lang="ts">
	import Badge from '#lib/Badge.svelte';
	import {
		creer, db, enregistrer, estModifie, mettreALaCorbeille, nouvelId, restaurerOriginal, sortirDeLaCorbeille,
		supprimerDefinitivement
	} from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import { sansAccents } from '#lib/markup.ts';
	import type { ElementListe, Moment, Pratique, Rang, Texte } from '#lib/types.ts';
	import { rangElement, RANGS } from '#lib/rangs.ts';
	import { LIBELLES_DU_JOUR } from '#lib/liste.ts';

	const liste = vivant(() => db.liste.orderBy('ordre').toArray(), [] as ElementListe[]);
	const textes = vivant(() => db.textes.orderBy('ordre').toArray(), [] as Texte[]);
	const MOMENTS: [Moment, string][] = [['matin', 'Matin'], ['propre', 'Propre du jour'], ['journee', 'Au fil du jour'], ['soir', 'Soir']];
	const JOURS = ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'];
	const JOURS_LONGS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];

	const actifs = $derived($liste.filter((e) => !e.supprimeLe));
	const corbeille = $derived($liste.filter((e) => e.supprimeLe));
	const roues = vivant(async () => (await db.pratiques.toArray()).filter((p) => p.type === 'roue' && !p.supprimeLe).sort((a, b) => a.titre.localeCompare(b.titre)), [] as Pratique[]);
	const titres = $derived(Object.fromEntries($textes.map((t) => [t.id, t.titre])));

	// ---- édition d'un élément ----
	let ouvert: string | undefined = $state();
	let brouillon: ElementListe | undefined = $state();
	let recherche = $state('');
	let nouvelleHeure = $state('');
	let aSupprimer: string | undefined = $state();

	function ouvrir(e: ElementListe) {
		if (ouvert === e.id) return fermer();
		ouvert = e.id;
		brouillon = structuredClone(e);
		recherche = '';
		nouvelleHeure = '';
	}
	function fermer() {
		ouvert = undefined;
		brouillon = undefined;
	}
	async function sauver() {
		if (!brouillon || !brouillon.titre.trim()) return;
		const b = $state.snapshot(brouillon) as ElementListe;
		b.rappels = [...b.rappels].sort();
		await enregistrer('liste', b);
		await renumeroter();
		fermer();
	}
	function ajouterHeure() {
		if (!brouillon || !nouvelleHeure || brouillon.rappels.includes(nouvelleHeure)) return;
		brouillon.rappels = [...brouillon.rappels, nouvelleHeure].sort();
		nouvelleHeure = '';
	}
	const trouves = $derived.by(() => {
		const q = sansAccents(recherche.trim());
		if (q.length < 2 || !brouillon) return [];
		return $textes.filter((t) => !t.supprimeLe && !brouillon!.textes.includes(t.id) && sansAccents(t.titre).includes(q)).slice(0, 6);
	});

	async function ajouter(moment: Moment) {
		const dernier = actifs.filter((e) => e.moment === moment).at(-1);
		const e = await creer<ElementListe>('liste', {
			id: nouvelId(),
			origine: 'personnel',
			titre: 'Nouvel élément',
			moment,
			etiquette: moment === 'propre' ? 'propre' : 'ordinaire',
			ordre: (dernier?.ordre ?? 0) + 1,
			jours: [true, true, true, true, true, true, true],
			rappels: [],
			textes: [],
			actif: true
		});
		await renumeroter();
		ouvrir(e);
	}
	async function basculer(e: ElementListe) {
		await enregistrer('liste', { ...e, actif: !e.actif });
	}
	async function jeter(e: ElementListe) {
		fermer();
		await mettreALaCorbeille('liste', e.id);
	}

	// ---- ordre : glisser-déposer au doigt ou à la souris, et boutons monter / descendre ----
	/** Réécrit l'ordre de toute la liste : moments dans l'ordre de la journée, puis rang dans le moment. */
	async function renumeroter(ordreLocal?: Record<Moment, string[]>) {
		const tous = await db.liste.toArray();
		let n = 0;
		await db.transaction('rw', db.liste, async () => {
			for (const [m] of MOMENTS) {
				const groupe = tous.filter((e) => e.moment === m).sort((a, b) => a.ordre - b.ordre);
				const ids = ordreLocal?.[m] ?? groupe.map((e) => e.id);
				const reste = groupe.map((e) => e.id).filter((id) => !ids.includes(id));
				for (const id of [...ids, ...reste]) await db.liste.update(id, { ordre: (n += 10) });
			}
		});
	}
	async function deplacer(e: ElementListe, pas: number) {
		const groupe = actifs.filter((x) => x.moment === e.moment).map((x) => x.id);
		const i = groupe.indexOf(e.id);
		const j = i + pas;
		if (j < 0 || j >= groupe.length) return;
		groupe.splice(j, 0, ...groupe.splice(i, 1));
		await renumeroter({ [e.moment]: groupe } as Record<Moment, string[]>);
	}

	let glisse: { id: string; moment: Moment; ids: string[] } | undefined = $state();
	function saisir(ev: PointerEvent, e: ElementListe) {
		(ev.currentTarget as HTMLElement).setPointerCapture(ev.pointerId);
		glisse = { id: e.id, moment: e.moment, ids: actifs.filter((x) => x.moment === e.moment).map((x) => x.id) };
		fermer();
	}
	function glisser(ev: PointerEvent) {
		if (!glisse) return;
		const lignes = [...document.querySelectorAll<HTMLElement>(`li[data-moment="${glisse.moment}"]`)];
		const cible = lignes.findIndex((l) => {
			const r = l.getBoundingClientRect();
			return ev.clientY >= r.top && ev.clientY <= r.bottom;
		});
		const de = glisse.ids.indexOf(glisse.id);
		if (cible < 0 || cible === de) return;
		const ids = [...glisse.ids];
		ids.splice(cible, 0, ...ids.splice(de, 1));
		glisse = { ...glisse, ids };
	}
	async function lacher() {
		if (!glisse) return;
		const g = glisse;
		glisse = undefined;
		await renumeroter({ [g.moment]: g.ids } as Record<Moment, string[]>);
	}
	/** Éléments d'un moment, dans l'ordre affiché (celui du glissement en cours, s'il y en a un). */
	function duMoment(m: Moment): ElementListe[] {
		const groupe = actifs.filter((e) => e.moment === m);
		if (glisse?.moment !== m) return groupe;
		return glisse.ids.map((id) => groupe.find((e) => e.id === id)).filter((e): e is ElementListe => !!e);
	}
	const resume = (e: ElementListe) => {
		const j = e.jours.every(Boolean) ? 'chaque jour' : e.jours.map((v, i) => (v ? JOURS[i] : '')).filter(Boolean).join(' ') || 'aucun jour';
		return e.rappels.length ? `${j}, ${e.rappels.join(', ')}` : j;
	};
</script>

<svelte:head><title>Liste du jour — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour" href="/"><Icone nom="retour" taille={16} /> Aujourd’hui</a>
	<div class="tete-page">
		<h1>Liste du jour</h1>
		<Ornement nom="fleuron" />
		<p class="petit">Glissez la poignée pour changer l’ordre. Touchez un élément pour le régler.</p>
	</div>

	{#each MOMENTS as [moment, nom]}
		<section>
			<div class="tete-section">
				<Ornement nom="grecque" />
				<h2>{nom}</h2>
			</div>
			<ul class="reglee">
				{#each duMoment(moment) as e, i (e.id)}
					<li data-moment={moment} class:inactif={!e.actif} class:glisse={glisse?.id === e.id} class:ouvert={ouvert === e.id}>
						<div class="ligne">
							<button
								class="poignee brut" aria-label="Déplacer « {e.titre} »"
								onpointerdown={(ev) => saisir(ev, e)} onpointermove={glisser} onpointerup={lacher} onpointercancel={lacher}
							>
								<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M3 5.500h12M3 9h12M3 12.500h12" stroke="currentColor" stroke-width="1.250" fill="none" stroke-linecap="round" /></svg>
							</button>
							<button class="resume brut" aria-expanded={ouvert === e.id} onclick={() => ouvrir(e)}>
								<span class="titre">{e.titre}</span>
								<span class="detail">{resume(e)}{e.textes.length ? `, ${e.textes.length} prière${e.textes.length > 1 ? 's' : ''}${e.alterner && e.textes.length > 1 ? ' en alternance' : ''}{e.roue ? ', par la roue' : ''}` : ''}{e.actif ? '' : ', masqué'}</span>
							</button>
							<span class="fleches">
								<button class="brut" aria-label="Monter" disabled={i === 0} onclick={() => deplacer(e, -1)}><Icone nom="retour" taille={16} /></button>
								<button class="brut" aria-label="Descendre" disabled={i === duMoment(moment).length - 1} onclick={() => deplacer(e, 1)}><Icone nom="chevron" taille={16} /></button>
							</span>
						</div>

						{#if ouvert === e.id && brouillon}
							<div class="reglage epreuve">
								<label><span>Titre</span><input type="text" bind:value={brouillon.titre} /></label>
								<div class="deux">
									<label>
										<span>Moment</span>
										<select bind:value={brouillon.moment}>
											{#each MOMENTS as [m, n]}<option value={m}>{n}</option>{/each}
										</select>
									</label>
									<label>
										<span>Genre</span>
										<select bind:value={brouillon.etiquette}>
											<option value="ordinaire">Ordinaire</option>
											<option value="propre">Propre</option>
										</select>
									</label>
									<label>
										<span>Rang</span>
										<select bind:value={() => rangElement(brouillon!), (v: Rang) => (brouillon!.rang = v)}>
											{#each RANGS as r}<option value={r.cle} title={r.aide}>{r.latin} ({r.fr})</option>{/each}
										</select>
									</label>
								</div>

								<p class="aide">Jours où il apparaît</p>
								<div class="jours" role="group" aria-label="Jours de la semaine">
									{#each JOURS as j, k}
										<button aria-pressed={brouillon.jours[k]} aria-label={JOURS_LONGS[k]} onclick={() => (brouillon!.jours[k] = !brouillon!.jours[k])}>{j}</button>
									{/each}
								</div>

								<p class="aide">Heures de rappel. Plusieurs heures : la prière se compte plusieurs fois dans la journée.</p>
								<div class="rangee">
									{#each brouillon.rappels as h}
										<span class="heure">{h}<button class="brut" aria-label="Retirer {h}" onclick={() => (brouillon!.rappels = brouillon!.rappels.filter((x) => x !== h))}>×</button></span>
									{/each}
									<input class="temps" type="time" bind:value={nouvelleHeure} aria-label="Nouvelle heure" />
									<button disabled={!nouvelleHeure} onclick={ajouterHeure}>Ajouter l’heure</button>
								</div>

								<label><span>Durée d’une récitation (minutes)</span>
									<input type="number" min="0" step="1" inputmode="numeric" placeholder="estimée d’après le texte"
										value={brouillon.duree ?? ''}
										oninput={(ev) => (brouillon!.duree = ev.currentTarget.value === '' ? undefined : Number(ev.currentTarget.value))} />
								</label>

								<label><span>Choix de la prière</span>
									<select value={brouillon.roue ?? ''} onchange={(ev) => (brouillon!.roue = ev.currentTarget.value || undefined)}>
										<option value="">Fixe : les prières ci-dessous</option>
										{#each $roues as r (r.id)}<option value={r.id}>Par la roue : {r.titre} ({r.elements?.length ?? 0})</option>{/each}
									</select>
								</label>
								{#if brouillon.roue}<p class="aide">Chaque jour, la prière liée à l’élément du jour de cette roue ; un élément sans prière s’affiche comme thème. Les roues se règlent sur la page <a href="/roue">La roue</a>.</p>{/if}
								<p class="aide">Prières ouvertes par cet élément{brouillon.roue ? ' (quand la roue n’en donne pas)' : ''}</p>
								{#each brouillon.textes as id}
									<div class="liee">
										<span>{titres[id] ?? LIBELLES_DU_JOUR[id] ?? 'Prière introuvable'}</span>
										<button class="brut" aria-label="Retirer cette prière" onclick={() => (brouillon!.textes = brouillon!.textes.filter((x) => x !== id))}>×</button>
									</div>
								{/each}
								<input type="search" placeholder="Chercher une prière à lier" bind:value={recherche} aria-label="Chercher une prière à lier" />
								{#each trouves as t}
									<button class="trouve brut" onclick={() => { brouillon!.textes = [...brouillon!.textes, t.id]; recherche = ''; }}>
										{t.titre} <span class="petit">{t.partie}</span>
									</button>
								{/each}
								{#if brouillon.textes.length > 1}
									<label class="case"><input type="checkbox" bind:checked={brouillon.alterner} /> Une seule prière par jour, à tour de rôle selon la semaine du mois (1re semaine : la première, 2e : la deuxième…)</label>
								{/if}

								<div class="rangee actions">
									<button class="principal" disabled={!brouillon.titre.trim()} onclick={sauver}>Enregistrer</button>
									<button onclick={fermer}>Annuler</button>
									<button onclick={() => basculer(e)}>{e.actif ? 'Masquer' : 'Afficher'}</button>
									{#if estModifie(e)}<button onclick={async () => { await restaurerOriginal('liste', e.id); fermer(); }}>Restaurer l’original</button>{/if}
									<button class="danger" onclick={() => jeter(e)}>Mettre à la corbeille</button>
								</div>
								<p class="origine"><Badge objet={e} /></p>
							</div>
						{/if}
					</li>
				{:else}
					<li class="vide petit">Rien pour ce moment.</li>
				{/each}
			</ul>
			<button class="ajout" onclick={() => ajouter(moment)}>Ajouter un élément</button>
		</section>
	{/each}

	{#if corbeille.length}
		<section>
			<div class="tete-section"><Ornement nom="grecque" /><h2>Corbeille</h2></div>
			<ul class="reglee">
				{#each corbeille as e (e.id)}
					<li class="jete">
						<span class="titre">{e.titre}</span>
						<span class="espace"></span>
						<button onclick={() => sortirDeLaCorbeille('liste', e.id)}>Rétablir</button>
						{#if aSupprimer === e.id}
							<button class="danger" onclick={() => supprimerDefinitivement('liste', e.id)}>Confirmer la suppression</button>
						{:else}
							<button class="discret" onclick={() => (aSupprimer = e.id)}>Supprimer pour de bon</button>
						{/if}
					</li>
				{/each}
			</ul>
		</section>
	{/if}
</main>

<style>
	.tete-page :global(.filet) { max-width: 16rem; }
	li { display: block !important; min-height: 0 !important; transition: background var(--hs-duree-vive) var(--hs-courbe); }
	li.glisse { background: var(--hs-surface); }
	li.inactif .titre { color: var(--hs-encre-douce); text-decoration: line-through; text-decoration-thickness: var(--hs-cheveu); }
	.ligne { display: flex; align-items: center; gap: var(--hs-e2); min-height: 56px; }
	.poignee { flex: none; width: 40px; height: 44px; display: grid; place-items: center; background: none; border: 0; cursor: grab; color: var(--hs-encre-douce); touch-action: none; }
	.poignee:active { cursor: grabbing; color: var(--hs-lapis); }
	.resume { flex: 1; min-width: 0; display: grid; text-align: left; background: none; border: 0; padding: 8px 0; cursor: pointer; }
	.titre { line-height: 1.3; overflow-wrap: anywhere; }
	.detail { font-family: var(--hs-interface); font-size: 0.75rem; letter-spacing: var(--hs-chasse-interface); color: var(--hs-encre-douce); line-height: 1.4; }
	.fleches { display: flex; flex: none; }
	.fleches button { width: 36px; height: 44px; display: grid; place-items: center; background: none; border: 0; cursor: pointer; color: var(--hs-encre-douce); transform: rotate(90deg); }
	.fleches button:disabled { opacity: 0.25; cursor: default; }

	.reglage { margin: 0 0 var(--hs-e4); padding: var(--hs-e4); display: grid; gap: var(--hs-e3); }
	.deux { display: grid; grid-template-columns: 1fr 1fr; gap: var(--hs-e4); }
	.aide { margin: var(--hs-e2) 0 0; }
	.jours { display: flex; flex-wrap: wrap; gap: 6px; }
	.jours button { min-height: 40px; padding: 0 10px; text-transform: none; font-family: var(--hs-lecture); font-size: 1.0625rem; font-weight: 400; letter-spacing: 0; font-variant-caps: all-small-caps; }
	.jours button[aria-pressed='false'] { border-color: var(--hs-filet); color: var(--hs-encre-douce); }
	.heure { display: inline-flex; align-items: center; gap: 4px; padding: 4px 4px 4px 10px; border: var(--hs-cheveu) solid var(--hs-filet); font-family: var(--hs-interface); font-size: var(--hs-t0); font-variant-numeric: lining-nums; }
	.heure button, .liee button { width: 32px; height: 32px; background: none; border: 0; cursor: pointer; color: var(--hs-rubrique); font-size: 1.125rem; line-height: 1; }
	.temps { width: 7.5rem !important; }
	.liee { display: flex; align-items: center; justify-content: space-between; gap: 8px; border-bottom: var(--hs-cheveu) solid var(--hs-filet); padding: 2px 0; }
	.trouve { display: block; width: 100%; text-align: left; background: none; border: 0; border-bottom: var(--hs-cheveu) solid var(--hs-filet); padding: 8px 0; cursor: pointer; color: var(--hs-lapis); }
	.actions { margin-top: var(--hs-e3); }
	.origine { margin: 0; }
	.ajout { margin-top: var(--hs-e4); min-height: 40px; }
	li.vide { padding: 12px 0; }
	li.jete { display: flex !important; align-items: center; gap: var(--hs-e3); flex-wrap: wrap; padding: 8px 0; }
</style>
