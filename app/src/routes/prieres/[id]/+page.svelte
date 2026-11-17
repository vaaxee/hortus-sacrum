<script lang="ts">
	import { vivantSelon } from '#lib/vivant.svelte.ts';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import FicheTexte from '#lib/FicheTexte.svelte';
	import {
		db, dupliquer, enregistrer, estModifie, mettreALaCorbeille, restaurerOriginal, restaurerVersion,
		sortirDeLaCorbeille, versions
	} from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import { rendre } from '#lib/markup.ts';
	import { etiquetteSource } from '#lib/sources.ts';
	import type { Texte, Version } from '#lib/types.ts';
	import { iso, jourDu } from '#lib/calendrier.ts';
	import { CHAPELETS } from '#lib/liste.ts';
	import { chargerIndulgences, enClair, valeurDuJour, valeursDuJour, type Indulgences } from '#lib/indulgences.ts';


	const id = $derived(decodeURIComponent(page.params.id ?? ''));
	const texte = vivantSelon(() => { const k = id; return () => db.textes.get(k); }, undefined as Texte | undefined);
	let latin = $state(false);
	// indulgence (partielle) d'aujourd'hui, annoncée avant la prière, avec son intention éventuelle
	let ind = $state<Indulgences | null>(null);
	let tempora = $state<string | null>(null);
	const aujourdhui = iso(new Date());
	chargerIndulgences().then((x) => (ind = x));
	jourDu(aujourdhui).then((j) => (tempora = j?.tempora ?? null));
	const fiche = $derived(ind?.fiches[id]);
	// chapelet : passer aux autres mystères (rosaire entier)
	const autresChapelets = $derived(CHAPELETS.includes(id) ? CHAPELETS.filter((c) => c !== id) : []);
	const NOM_CHAPELET = (c: string) => `Mystères ${c.slice('hortus:chapelet-'.length)}`;
	const sansCompte = $derived(ind?.sans_compte[id]);
	const parties = vivant(
		async () => [...new Set((await db.textes.toArray()).map((t) => t.partie).filter(Boolean))],
		[] as string[]
	);
	let edition = $state(false);
	let brouillon: Texte | undefined = $state();
	let historique: Version[] = $state([]);
	let voirHistorique = $state(false);

	function modifier() {
		if (!texte.v) return;
		brouillon = structuredClone(texte.v);
		edition = true;
	}
	async function sauver() {
		if (!brouillon) return;
		await enregistrer('textes', $state.snapshot(brouillon) as Texte);
		edition = false;
	}
	async function ouvrirHistorique() {
		historique = await versions('textes', id);
		voirHistorique = !voirHistorique;
	}
	async function revenir(v: Version) {
		await restaurerVersion('textes', id, v);
		historique = await versions('textes', id);
	}
	async function copier() {
		const c = await dupliquer<Texte>('textes', id);
		if (c) goto(`/prieres/${encodeURIComponent(c.id)}`);
	}
	async function favori() {
		if (texte.v) await db.textes.update(id, { favori: !texte.v.favori });
	}
	async function jeter() {
		await mettreALaCorbeille('textes', id);
		goto('/prieres');
	}
	const dateFr = (iso: string) => new Date(iso).toLocaleString('fr-FR', { dateStyle: 'medium', timeStyle: 'short' });
	const titreVersion = (v: Version) => (JSON.parse(v.contenu) as Texte).titre;

	type Bloc = { genre: 'rubrique' | 'verset' | 'titre' | 'traduction' | 'texte'; fr: string; la?: string };

	/** Paragraphes du texte ; les strophes latines s'apparient à la suite de paragraphes simples de même longueur. */
	const blocs = $derived.by((): Bloc[] => {
		const t = texte.v;
		if (!t) return [];
		const genre = (p: string): Bloc['genre'] =>
			p.startsWith('[r]') && p.endsWith('[/r]') ? 'rubrique'
			: /^(℣\.|℟\.)/.test(p) ? 'verset'
			: p.startsWith('## ') || p.startsWith('### ') ? 'titre'
			: p.startsWith('[') ? 'traduction' : 'texte';
		const out: Bloc[] = t.corps.split(/\n{2,}/).filter(Boolean).map((p) => ({ genre: genre(p), fr: p }));
		const la = t.latin.split(/\n{2,}/).filter(Boolean);
		if (la.length) {
			for (let i = 0; i + la.length <= out.length; i++) {
				if (out.slice(i, i + la.length).every((b) => b.genre === 'texte' || b.genre === 'verset')) {
					la.forEach((l, k) => (out[i + k].la = l));
					break;
				}
			}
		}
		return out;
	});
	const aDuLatin = $derived(blocs.some((b) => b.la));
	const vers = $derived(blocs.some((b) => b.la && b.fr.includes('\n')));
	const ORIGINE = { livret: ['livret', 'Livret'], officielle: ['verifiee', 'Source vérifiée'], personnel: ['personnel', 'Ajout personnel'] } as const;
</script>

<svelte:head><title>{texte.v?.titre ?? 'Prière'} — Hortus Sacrum</title></svelte:head>

{#if !texte.v}
	<main class="page"><a class="retour" href="/prieres"><Icone nom="retour" taille={16} /> Prières</a><p>Cette prière est introuvable.</p></main>
{:else if edition && brouillon}
	<main class="page">
		<a class="retour" href="/prieres"><Icone nom="retour" taille={16} /> Prières</a>
		<div class="tete-page"><h1>Modifier</h1></div>
		<FicheTexte bind:texte={brouillon} parties={$parties} />
		<div class="rangee actions-edition">
			<button class="principal" onclick={sauver}>Enregistrer</button>
			<button onclick={() => (edition = false)}>Annuler</button>
		</div>
	</main>
{:else}
	{@const t = texte.v}
	<main class="ecran entree">
		<a class="retour interface" href="/prieres"><Icone nom="retour" taille={16} /> {texte.v.partie || 'Prières'}</a>

		<header>
			<h1>{t.titre}</h1>
			<p class="marques">
				<span class="cartouche {ORIGINE[t.origine][0]}">{etiquetteSource(t)}</span>
				{#if estModifie(t)}<span class="cartouche personnel">modifié</span>{/if}
			</p>
			{#if t.supprimeLe}
				<p class="corbeille">Cette prière est dans la corbeille. <button onclick={() => sortirDeLaCorbeille('textes', id)}>La rétablir</button></p>
			{/if}
			{#if t.usage}<p class="usage"><span class="pc rub">usage :</span> <em>{t.usage}</em></p>{/if}
			{#if fiche}
				<aside class="indulgence-jour">
					{#if fiche.intention}<p><span class="pc rub">intention :</span> <em>{fiche.intention}</em></p>{/if}
					<p><span class="pc rub">aujourd’hui :</span> {enClair(valeurDuJour(fiche, aujourdhui, tempora))}
						<span class="detail">({valeursDuJour(fiche, aujourdhui, tempora).map((p) => p.texte).join(' + ')})</span></p>
					{#if fiche.partielles.some((p) => p.quand)}
						<p class="detail">Selon le jour : {fiche.partielles.filter((p) => p.quand).map((p) => p.texte).join(' ; ')}.</p>
					{/if}
					{#if fiche.note}<p class="detail">{fiche.note}</p>{/if}
					<p class="detail source">{fiche.ref}</p>
				</aside>
			{:else if sansCompte}
				<aside class="indulgence-jour"><p class="detail">{sansCompte}</p></aside>
			{/if}
			{#if autresChapelets.length}
				<nav class="autres-chapelets" aria-label="Autres mystères du Rosaire">
					{#each autresChapelets as c}<a class="bouton" href={`/prieres/${encodeURIComponent(c)}`}>{NOM_CHAPELET(c)}</a>{/each}
				</nav>
			{/if}
			<Ornement nom="fleuron" />
		</header>

		<div class="page">
			<article class="texte" class:vers class:bilingue={latin && aDuLatin}>
				{#if aDuLatin}
					<div class="bascule">
						<button class="bouton" aria-pressed={latin} onclick={() => (latin = !latin)}>{latin ? 'Masquer le latin' : 'Latin'}</button>
					</div>
				{/if}
				{#each blocs as b}
					{#if b.genre === 'rubrique'}
						<p class="rubrique rub">{@html rendre(b.fr.slice(3, -4)).replace(/^<p>|<\/p>$/g, '')}</p>
					{:else if b.la}
						<div class="strophe">
							{#if latin}<div class="la lecture" lang="la">{@html rendre(b.la)}</div>{/if}
							<div class="fr lecture">{@html rendre(b.fr)}</div>
						</div>
					{:else}
						<div class="lecture {b.genre}">{@html rendre(b.fr)}</div>
					{/if}
				{/each}
				{#if autresChapelets.length}
					<nav class="autres-chapelets" aria-label="Autres mystères du Rosaire">
						{#each autresChapelets as c}<a class="bouton" href={`/prieres/${encodeURIComponent(c)}`}>{NOM_CHAPELET(c)}</a>{/each}
					</nav>
				{/if}
			</article>

			<aside class="marge" aria-label="Indulgence et source">
				{#if t.indulgence}
					<details open>
						<summary><span class="cartouche ind">Ind.</span></summary>
						<p>{t.indulgence}</p>
					</details>
				{/if}
				<details open>
					<summary><span class="pc">Source</span></summary>
					<p class="imprime">
						{t.source.ouvrage}{#if t.source.edition}<br /><em>{t.source.edition}</em>{/if}{#if t.source.page}, p. {t.source.page}{/if}
					</p>
				</details>
			</aside>
		</div>

		<div class="cul"><Ornement nom="cherubin" taille={30} /></div>
		<div class="actions">
			<button class="principal" onclick={modifier}>Modifier</button>
			<button onclick={favori} aria-pressed={!!t.favori}>{t.favori ? 'Retirer des favoris' : 'Ajouter aux favoris'}</button>
			<button onclick={copier}>Dupliquer</button>
			<button onclick={ouvrirHistorique} aria-expanded={voirHistorique}>Historique</button>
			{#if estModifie(t)}<button onclick={() => restaurerOriginal('textes', id)}>Restaurer l’original</button>{/if}
			{#if !t.supprimeLe}<button class="danger" onclick={jeter}>Mettre à la corbeille</button>{/if}
		</div>
		{#if voirHistorique}
			<section class="historique">
				<h3>Versions précédentes</h3>
				{#each historique as v (v.id)}
					<div class="rangee version">
						<span>{dateFr(v.date)} <span class="petit">{titreVersion(v)}</span></span>
						<span class="espace"></span>
						<button onclick={() => revenir(v)}>Revenir à cette version</button>
					</div>
				{:else}
					<p class="petit">Ce texte n’a pas encore été modifié.</p>
				{/each}
			</section>
		{/if}
		<div hidden>
		</div>
	</main>
{/if}

<style>
	.autres-chapelets { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0; }
	.indulgence-jour { max-width: 34rem; margin: var(--hs-e3) auto 0; padding: var(--hs-e2) var(--hs-e4); border: var(--hs-cheveu) solid var(--hs-or-trait); text-align: center; }
	.indulgence-jour p { margin: 2px 0; }
	.indulgence-jour .detail { font-size: 0.9375rem; color: var(--hs-encre-douce); font-style: italic; }
	.ecran { max-width: 980px; margin: 0 auto; padding: var(--hs-e5) var(--hs-marge-mobile) 0; }
	.retour { display: inline-flex; align-items: center; gap: 4px; text-decoration: none; color: var(--hs-encre-douce); min-height: 44px; }
	header { text-align: center; display: grid; justify-items: center; gap: var(--hs-e3); margin: var(--hs-e6) auto var(--hs-e6); max-width: var(--hs-mesure); }
	header p { margin: 0; }
	h1 { font-size: var(--hs-t3); }
	.usage { font-size: 1.0625rem; }
	.marques { display: flex; gap: 8px; }
	header :global(.filet) { margin-top: var(--hs-e3); max-width: 18rem; }

	.texte { max-width: var(--hs-mesure); margin-inline: auto; }
	.rubrique { font-style: italic; text-align: center; font-size: 1.0625rem; margin: 0 auto var(--hs-ligne); max-width: 28rem; text-wrap: balance; }
	.bascule { display: flex; justify-content: center; margin-bottom: var(--hs-e5); }
	.bascule .bouton { min-height: 36px; }
	.strophe { margin-bottom: var(--hs-ligne); display: grid; gap: var(--hs-e2); }
	.texte .strophe :global(p) { margin: 0; text-align: left; hyphens: manual; }
	.vers .strophe { justify-content: center; }
	.strophe .la { color: var(--hs-encre-douce); font-size: 1.0625rem; padding-left: var(--hs-e4); border-left: var(--hs-cheveu) solid var(--hs-or-trait); order: 2; }
	.lecture.verset, .lecture.traduction { margin-top: var(--hs-ligne); }
	.lecture.verset :global(p), .lecture.traduction :global(p) { text-align: center; }
	.lecture.traduction { font-size: 1.0625rem; color: var(--hs-encre-douce); margin-top: 0; }

	/* marginalia : sous le texte au téléphone, dans la marge à l'ordinateur */
	.marge { max-width: var(--hs-mesure); margin: var(--hs-e6) auto 0; border-top: var(--hs-cheveu) solid var(--hs-filet); }
	.marge details { border-bottom: var(--hs-cheveu) solid var(--hs-filet); }
	.marge summary { padding: 10px 0; color: var(--hs-encre-douce); }
	.marge p { margin: 0 0 12px; font-size: 0.9375rem; line-height: 1.45; color: var(--hs-encre-douce); }
	.marge .imprime { font-size: 1rem; }

	.cul { text-align: center; color: var(--hs-or); margin-top: var(--hs-e7); }
	.actions-edition { margin-top: var(--hs-e5); }
	.corbeille { font-size: 1rem; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: center; color: var(--hs-rubrique); }
	.historique { max-width: var(--hs-mesure); margin: var(--hs-e6) auto 0; }
	.historique h3 { color: var(--hs-rubrique); text-align: center; margin-bottom: var(--hs-e3); }
	.version { padding: 8px 0; border-bottom: var(--hs-cheveu) solid var(--hs-filet); font-size: 1.0625rem; }
	.actions { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: var(--hs-e6); }

	@media (min-width: 640px) {
		h1 { font-size: var(--hs-t4); }
		.texte.bilingue { max-width: 46rem; }
		.bilingue .strophe { grid-template-columns: 1fr 1fr; gap: var(--hs-e6); justify-content: stretch; }
		.bilingue .strophe .la { order: 0; border-left: 0; padding-left: 0; text-align: right; font-size: inherit; }
		.bilingue .strophe .la :global(p) { text-align: right; }
		.bilingue .strophe .fr { border-left: var(--hs-cheveu) solid var(--hs-or-trait); padding-left: var(--hs-e6); }
	}
	@media (min-width: 1280px) {
		.page { display: grid; grid-template-columns: minmax(0, 1fr) 210px; gap: var(--hs-e6); align-items: start; }
		.marge { margin: 0; border-top: 0; position: sticky; top: var(--hs-e5); padding-top: 4.5rem; }
		.marge details { border-bottom: 0; border-left: var(--hs-cheveu) solid var(--hs-or-trait); padding-left: var(--hs-e4); margin-bottom: var(--hs-e5); }
		.marge summary { padding: 0 0 6px; pointer-events: none; }
	}
</style>
