<script lang="ts">
	import { page } from '$app/state';
	import { introitVersCorps, iso, jourDu, MOIS_DEVOTION, RANG, teinte, type Jour } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Arche from '#lib/design/Arche.svelte';
	import Case from '#lib/design/Case.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { invocation, nomLatin, TOUS_LES_SAINTS } from '#lib/invocations.ts';
	import { textesDuJour } from '#lib/liste.ts';
	import { garde, rangElement, rangPratique, RANGS } from '#lib/rangs.ts';
	import { vivant } from '#lib/live.ts';
	import { rendre } from '#lib/markup.ts';
	import { creer, enregistrer } from '#lib/db.ts';
	import { occurrenceDu, type Occurrence } from '#lib/pratiques.ts';
	import { basculerFait } from '#lib/suivi.ts';
	import type { Coche, ElementListe, Fait, FetePerso, Moment, NoteJour, Pratique, Rang } from '#lib/types.ts';
	import Icone from '#lib/design/Icone.svelte';

	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	let jour: Jour | undefined = $state();
	$effect(() => {
		jourDu(date).then((j) => (jour = j));
	});

	const d = $derived(new Date(date + 'T12:00:00'));
	const dateLongue = $derived(d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }));
	const solennel = $derived(jour?.rang === '1re cl.' || jour?.rang === 'dim. 1re cl.');

	const liste = vivant(() => db.liste.orderBy('ordre').toArray(), [] as ElementListe[]);
	const titres = vivant(async () => Object.fromEntries((await db.textes.toArray()).map((t) => [t.id, t.titre])), {} as Record<string, string>);
	const MOMENTS: [Moment, string][] = [['matin', 'Matin'], ['propre', 'Propre du jour'], ['journee', 'Au fil du jour'], ['soir', 'Soir']];
	// pratiques du jour : elles remplacent les deux lignes génériques « dévotion en cours » et « neuvaine ou trentain »
	const pratiques = vivant(() => db.pratiques.toArray(), [] as Pratique[]);
	const faitsDuJour = $derived(vivant(() => db.faits.where('date').equals(date).toArray(), [] as Fait[]));
	const pratiquesDuJour = $derived(
		$pratiques
			.filter((p) => p.active && !p.supprimeLe)
			.map((p) => ({ p, o: occurrenceDu(p, date) }))
			.filter((x): x is { p: Pratique; o: Occurrence } => !!x.o)
	);
	const faite = (id: string) => $faitsDuJour.some((f) => f.pratiqueId === id);
	/** Pratiques rattachées à un élément générique de la liste, ou null si l'élément est ordinaire. */
	function pratiquesPour(e: ElementListe) {
		const gardees = pratiquesDuJour.filter((x) => garde(rangPratique(x.p), seuil));
		if (e.titre.startsWith('Dévotion à jours comptés')) return gardees.filter((x) => !['neuvaine', 'trentain'].includes(x.p.type));
		if (e.titre.startsWith('Neuvaine ou trentain')) return gardees.filter((x) => ['neuvaine', 'trentain'].includes(x.p.type));
		return null;
	}

	// jour chargé : on n'affiche que les dévotions du rang choisi et au-dessus (réglage gardé pour ce jour, sur cet appareil)
	let seuil = $state<Rang>('supererogatoria');
	$effect(() => {
		let v: string | null = null;
		try { v = localStorage.getItem(`seuil:${date}`); } catch { /* stockage indisponible */ }
		seuil = (v as Rang) || 'supererogatoria';
	});
	function regler(r: Rang) {
		seuil = r;
		try { localStorage.setItem(`seuil:${date}`, r); } catch { /* stockage indisponible */ }
	}
	const SEUILS: [Rang, string, string][] = [
		['supererogatoria', 'Omnia', 'tout afficher'],
		['pia', 'Sine supererogatoriis', 'laisser les dévotions surérogatoires'],
		['praecipua', 'Præcipua tantum', 'seulement les dévotions principales']
	];
	const ABREGE = Object.fromEntries(RANGS.map((r) => [r.cle, r]));
	const duJour = $derived(
		$liste.filter((e) => {
			if (!e.actif || e.supprimeLe || !e.jours[d.getDay()]) return false;
			const pp = pratiquesPour(e);
			return pp ? pp.length > 0 : garde(rangElement(e), seuil);
		})
	);
	const fini = (e: ElementListe) => {
		const pp = pratiquesPour(e);
		return pp ? pp.every((x) => faite(x.p.id)) : (coches[e.id] ?? 0) >= Math.max(1, e.rappels.length);
	};

	// fêtes et anniversaires personnels du jour
	const fetes = $derived(vivant(() => db.fetes.where('[mois+jour]').equals([d.getMonth() + 1, d.getDate()]).toArray(), [] as FetePerso[]));
	const fetesDuJour = $derived($fetes.filter((f) => !f.supprimeLe));
	const anniversaire = (f: FetePerso) => (f.annee && d.getFullYear() > f.annee ? `, ${d.getFullYear() - f.annee}${d.getFullYear() - f.annee === 1 ? 'er' : 'e'} anniversaire` : '');

	// note du jour
	const note = $derived(vivant(() => db.notes.get(`note:${date}`), undefined as NoteJour | undefined));
	async function noter(corps: string) {
		const existante = await db.notes.get(`note:${date}`);
		if (existante) await enregistrer('notes', { ...existante, corps });
		else if (corps.trim()) await creer<NoteJour>('notes', { id: `note:${date}`, origine: 'personnel', date, corps });
	}
	// coches du jour, enregistrées et horodatées
	const cochesDuJour = $derived(vivant(() => db.coches.where('date').equals(date).toArray(), [] as Coche[]));
	const coches = $derived.by(() => {
		const n: Record<string, number> = {};
		for (const c of $cochesDuJour) n[c.elementId] = (n[c.elementId] ?? 0) + 1;
		return n;
	});
	async function compter(e: ElementListe, total: number) {
		const fait = coches[e.id] ?? 0;
		if (fait >= total) await db.coches.where('[date+elementId]').equals([date, e.id]).delete();
		else await db.coches.add({ date, elementId: e.id, rang: fait, horodatage: new Date().toISOString() });
	}
	const decaler = (n: number) => {
		const x = new Date(d);
		x.setDate(x.getDate() + n);
		return iso(x);
	};
	const estAujourdhui = $derived(date === iso(new Date()));
	const faits = $derived(duJour.filter(fini).length);

	/** Sous-titre des éléments du propre, tiré du calendrier. */
	function precision(e: ElementListe): string {
		if (!jour) return '';
		if (e.titre.startsWith('Office du jour')) return jour.office;
		if (e.titre.startsWith('Dévotion du mois')) return MOIS_DEVOTION[d.getMonth() + 1].nom;
		return '';
	}
	const ROMAINS = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix'];
</script>

<svelte:head><title>Aujourd’hui — Hortus Sacrum</title></svelte:head>

{#if jour}
	<div class="bandeau" style="background: {teinte(jour)}"></div>
	<main class="ecran entree">
		<header class="jour">
			<p class="date pc chiffres-alignes">
				<a class="pas" href="/?date={decaler(-1)}" aria-label="Jour précédent"><Icone nom="retour" taille={16} /></a>
				{dateLongue}
				<a class="pas" href="/?date={decaler(1)}" aria-label="Jour suivant"><Icone nom="chevron" taille={16} /></a>
			</p>
			{#if !estAujourdhui}<p class="revenir"><a href="/">Revenir à aujourd’hui</a></p>{/if}
			<p class="temps etiquette">{jour.temps}</p>

			<Arche {solennel}>
				<span class="pastille" style="--pastille: {teinte(jour)}" title="Couleur liturgique : {jour.couleur}"></span>
				<h1 class:fete={solennel}>{jour.office}</h1>
				<p class="rang pc">{RANG[jour.rang] ?? jour.rang}</p>
				{#if jour.commemoraisons.length}
					<p class="comm"><span class="pc">Comm.</span> {jour.commemoraisons.join(' ; ')}</p>
				{/if}
				{#if jour.jeune_abstinence}<p class="jeune rub pc">{jour.jeune_abstinence.libelle}</p>{/if}
			</Arche>

			{#each fetesDuJour as f (f.id)}
				<p class="perso"><span class="rub">✠</span> {f.titre}{anniversaire(f)}</p>
			{/each}

			{#if jour.introit_incipit}
				<details class="introit">
					<summary>
						<span class="pc rub">Introït</span>
						<em lang="la">{jour.introit_incipit}</em>
						{#if jour.station}<span class="station imprime">{jour.station}</span>{/if}
					</summary>
					{#if jour.introit}
						<div class="colonnes">
							<div class="lecture" lang="la">{@html rendre(introitVersCorps(jour.introit.la))}</div>
							{#if jour.introit.fr}<div class="lecture">{@html rendre(introitVersCorps(jour.introit.fr))}</div>{/if}
						</div>
						<p class="source imprime">Missel romain, d’après Divinum Officium.</p>
					{/if}
				</details>
			{/if}
		</header>

		<section class="liste" aria-label="Liste du jour">
			<div class="avancement interface">
				<span class="etiquette">Le jardin du jour</span>
				<span class="trait"><span style="width: {duJour.length ? (100 * faits) / duJour.length : 0}%"></span></span>
				<span class="chiffres-alignes">{faits} / {duJour.length}</span>
			</div>
			<p class="regler"><a href="/liste">Régler la liste</a></p>
			<div class="seuils interface" role="group" aria-label="Jour chargé : quelles dévotions afficher">
				{#each SEUILS as [r, latin, fr]}
					<button class="brut" aria-pressed={seuil === r} title={fr} onclick={() => regler(r)}>{latin}</button>
				{/each}
			</div>

			{#each MOMENTS as [moment, nom]}
				{@const elements = duJour.filter((e) => e.moment === moment)}
				{#if elements.length}
					<div class="tete">
						<Ornement nom="grecque" />
						<h2>{nom}</h2>
					</div>
					<ul>
						{#each elements as e (e.id)}
							{@const total = Math.max(1, e.rappels.length)}
							{@const fait = coches[e.id] ?? 0}
							{@const sous = precision(e)}
							{@const pp = pratiquesPour(e)}
							{@const tx = textesDuJour(e, date, jour)}
							{#if pp}
								{#each pp as { p, o } (p.id)}
									<li class:fini={faite(p.id)}>
										<Case libelle={p.titre} bind:cochee={() => faite(p.id), () => basculerFait(p.id, date)} />
										<div class="corps">
											<a class="titre" href="/devotions/{encodeURIComponent(p.id)}">{p.titre}</a>
											{#if p.notes}<span class="sous">{p.notes}</span>{/if}
										</div>
										{#if o.total}
											<span class="medaillon fixe" title="{o.rang} sur {o.total}">
												<Ornement nom="medaillon" taille={34} />
												<span class="chiffres-alignes petit-chiffre">{o.rang}<i>/</i>{o.total}</span>
											</span>
										{/if}
										<span class="genre pc propre">propre</span>
									</li>
								{/each}
							{:else}
							<li class:fini={fait >= total}>
								<Case
									libelle={e.titre}
									bind:cochee={() => fait >= total, () => compter(e, total)}
								/>
								<div class="corps">
									{#if tx.length === 1}
										<a class="titre" href="/prieres/{encodeURIComponent(tx[0])}">{e.titre}</a>
										{#if (e.alterner && e.textes.length > 1) || !e.textes.includes(tx[0])}<span class="sous">{$titres[tx[0]] ?? ''}</span>{/if}
									{:else if tx.length > 1}
										<details class="plusieurs">
											<summary class="titre">{e.titre}</summary>
											{#each tx as id}
												<a href="/prieres/{encodeURIComponent(id)}">{$titres[id] ?? id}</a>
											{/each}
										</details>
									{:else if e.titre === 'Méditation du jour'}
										<a class="titre" href="/meditation?date={date}">{e.titre}</a>
									{:else}
										<span class="titre">{e.titre}</span>
									{/if}
									{#if sous}<span class="sous">{sous}</span>{/if}
									{#if e.rappels.length}<span class="heures interface">{e.rappels.join(', ')}</span>{/if}
								</div>
								{#if total > 1}
									<button class="medaillon brut" onclick={() => compter(e, total)}
										aria-label="{fait} sur {total} : compter une récitation de plus">
										<Ornement nom="medaillon" taille={34} />
										<span class="pc">{ROMAINS[fait] || '·'}<i>/</i>{ROMAINS[total]}</span>
									</button>
								{/if}
								<span class="genre pc" class:propre={e.etiquette === 'propre'}>{e.etiquette === 'propre' ? 'propre' : 'ord.'}<br /><span class="rang rang-{rangElement(e)}" title={ABREGE[rangElement(e)].latin + ' : ' + ABREGE[rangElement(e)].fr}>{ABREGE[rangElement(e)].abrege}</span></span>
							</li>
							{/if}
						{/each}
					</ul>
				{/if}
			{/each}
		</section>

		<details class="note-jour" open={!!$note?.corps}>
			<summary class="pc">Note du jour</summary>
			<textarea rows="3" aria-label="Note du jour" value={$note?.corps ?? ''} onblur={(ev) => noter(ev.currentTarget.value)} placeholder="Une intention, une résolution, une grâce reçue"></textarea>
		</details>

		<section class="martyrologe" aria-label="Martyrologe">
			<div class="tete">
				<Ornement nom="grecque" />
				<h2>Martyrologe</h2>
				<p class="etiquette">Les saints de ce jour</p>
			</div>
			{#each jour.martyrologe as m}
				{@const inv = invocation(m.texte)}
				{@const la = nomLatin(m.texte_la)}
				<details class="eloge">
					<summary>
						{#if inv}<span class="invocation">{inv.texte}</span>{:else}<span class="invocation sans">{m.texte.split(/[.,]/)[0]}…</span>{/if}
						{#if la}<span class="nom-latin" lang="la">{la}</span>{/if}
					</summary>
					<p class="texte">{m.texte}</p>
					{#if m.texte_la}<p class="texte" lang="la">{m.texte_la}</p>{/if}
				</details>
			{/each}
			<p class="tous"><span class="rub">✠</span> {TOUS_LES_SAINTS}</p>
			<p class="source imprime">Martyrologe romain, traduction française donnée par Divinum Officium.</p>
		</section>

		<div class="cul"><Ornement nom="fleuron" /></div>
	</main>
{/if}

<style>
	.bandeau { height: 5px; border-bottom: var(--hs-cheveu) solid var(--hs-or-trait); }
	.ecran { max-width: var(--hs-colonne); margin: 0 auto; padding: var(--hs-e6) var(--hs-marge-mobile) 0; }
	.jour { text-align: center; }
	.date { margin: 0; font-size: 1.0625rem; color: var(--hs-encre-douce); display: flex; align-items: center; justify-content: center; gap: 4px; }
	.pas { display: inline-grid; place-items: center; width: 40px; height: 40px; color: var(--hs-encre-douce); }
	.revenir { margin: 0; font-size: 1rem; }
	a.titre, .plusieurs summary { color: var(--hs-encre); text-decoration: none; }
	.plusieurs a { display: block; padding: 6px 0 6px 12px; font-size: 1.0625rem; text-decoration: none; border-left: var(--hs-cheveu) solid var(--hs-or-trait); margin: 2px 0; }
	.temps { margin: 2px 0 var(--hs-e5); }
	h1 { font-size: var(--hs-t3); }
	h1.fete { color: var(--hs-rubrique); }
	.rang { margin: 0; color: var(--hs-encre-douce); font-size: 1.0625rem; }
	.comm { margin: 0; font-size: 1rem; font-style: italic; line-height: 1.4; text-wrap: balance; }
	.comm .pc { font-style: normal; color: var(--hs-encre-douce); }
	.jeune { margin: var(--hs-e2) 0 0; font-size: 1.0625rem; }

	.introit { margin-top: var(--hs-e5); border-block: var(--hs-cheveu) solid var(--hs-filet); text-align: left; }
	.introit summary { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: center; gap: 4px 12px; padding: var(--hs-e3) 0; }
	.station { font-size: 0.9375rem; color: var(--hs-encre-douce); font-style: italic; flex-basis: 100%; text-align: center; }
	.colonnes { display: grid; gap: var(--hs-e5); padding: var(--hs-e2) 0 var(--hs-e4); }
	.colonnes :global(.lecture p) { text-align: left; font-size: 1.0625rem; }
	.source { font-size: 0.875rem; color: var(--hs-encre-douce); font-style: italic; text-align: center; margin: 0 0 var(--hs-e4); }

	.liste { margin-top: var(--hs-e7); }
	.avancement { display: flex; align-items: center; gap: 12px; color: var(--hs-encre-douce); }
	.trait { flex: 1; height: 1px; background: var(--hs-filet); position: relative; }
	.trait span { position: absolute; inset: -1px auto -1px 0; background: var(--hs-vert); transition: width var(--hs-duree-lente) var(--hs-courbe); }

	.perso { margin: var(--hs-e3) 0 0; font-style: italic; }
	.note-jour { margin-top: var(--hs-e6); border-block: var(--hs-cheveu) solid var(--hs-filet); }
	.note-jour summary { padding: 12px 0; color: var(--hs-encre-douce); }
	.note-jour textarea { margin-bottom: var(--hs-e4); }
	.medaillon.fixe { cursor: default; }
	.petit-chiffre { font-family: var(--hs-interface); font-size: 0.625rem !important; }
	.regler { margin: var(--hs-e2) 0 0; text-align: right; font-family: var(--hs-interface); font-size: var(--hs-t0); letter-spacing: var(--hs-chasse-interface); }
	.tete { margin-top: var(--hs-e7); text-align: center; display: grid; gap: var(--hs-e3); }
	.tete h2 { font-size: var(--hs-t2); }
	.tete .etiquette { margin: -6px 0 0; }
	ul { list-style: none; margin: var(--hs-e3) 0 0; padding: 0; }
	li { display: flex; align-items: center; gap: 14px; padding: 11px 0; border-bottom: var(--hs-cheveu) solid var(--hs-filet); min-height: 56px; }
	.corps { flex: 1; min-width: 0; display: grid; }
	.titre { line-height: 1.3; transition: color var(--hs-duree) var(--hs-courbe); }
	li.fini .titre { color: var(--hs-encre-douce); }
	.sous { font-style: italic; font-size: 1rem; line-height: 1.35; color: var(--hs-encre-douce); }
	.heures { color: var(--hs-encre-douce); font-size: 0.75rem; margin-top: 2px; }
	.genre { font-size: 0.9375rem; color: var(--hs-encre-douce); width: 3.2rem; text-align: right; flex: none; }
	.genre.propre { color: var(--hs-rubrique); }
	.genre .rang { font-size: 0.75rem; letter-spacing: 0.04em; color: var(--hs-encre-douce); }
	.genre .rang-praecipua { color: var(--hs-or-texte); }
	.genre .rang-supererogatoria { font-style: italic; }
	.seuils { display: flex; justify-content: flex-end; flex-wrap: wrap; gap: var(--hs-e1, 6px) var(--hs-e2); margin: var(--hs-e1, 6px) 0 0; font-size: var(--hs-t0); letter-spacing: var(--hs-chasse-interface); }
	.seuils button { color: var(--hs-encre-douce); padding: 2px 0; min-height: 0; background: none; border: 0; border-bottom: 1px solid transparent; font: inherit; letter-spacing: inherit; cursor: pointer; }
	.seuils button[aria-pressed='true'] { color: var(--hs-encre); border-bottom-color: currentColor; }
	.medaillon { position: relative; flex: none; width: 34px; height: 34px; padding: 0; border: 0; background: none; color: var(--hs-or); cursor: pointer; line-height: 0; }
	.medaillon span { position: absolute; inset: 0; display: grid; place-items: center; grid-auto-flow: column; justify-content: center; color: var(--hs-encre); font-size: 0.8125rem; line-height: 1; }
	.medaillon i { font-style: normal; color: var(--hs-encre-douce); margin: 0 1px; }
	li.fini .medaillon { color: var(--hs-vert); }

	.eloge { border-bottom: var(--hs-cheveu) solid var(--hs-filet); }
	.eloge summary { padding: 10px 0; }
	.invocation::before { content: '✠'; color: var(--hs-rubrique); margin-right: 10px; font-size: 0.8em; }
	.invocation.sans { color: var(--hs-encre-douce); font-style: italic; }
	.invocation.sans::before { content: '·'; }
	.nom-latin { display: block; margin-left: 1.55rem; font-size: 1rem; font-style: italic; color: var(--hs-encre-douce); line-height: 1.35; }
	.texte { margin: 0 0 12px 1.5rem; font-size: 1.0625rem; text-align: justify; hyphens: auto; }
	.tous { text-align: center; margin: var(--hs-e5) 0 var(--hs-e2); font-style: italic; }
	.martyrologe .tete { margin-bottom: var(--hs-e3); }
	.cul { margin: var(--hs-e7) auto 0; max-width: 16rem; }

	@media (min-width: 700px) {
		h1 { font-size: var(--hs-t4); }
		.colonnes { grid-template-columns: 1fr 1fr; }
	}
</style>
