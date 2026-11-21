<script lang="ts">
	import { vivantSelon } from '#lib/vivant.svelte.ts';
	import { page } from '$app/state';
	import { introitVersCorps, iso, RANG, teinte } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Arche from '#lib/design/Arche.svelte';
	import Case from '#lib/design/Case.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { invocation, nomLatin, TOUS_LES_SAINTS } from '#lib/invocations.ts';
	import { invocationLatine } from '#lib/invocations-latines.ts';
	import { JACULATOIRES } from '#lib/liste.ts';
	import { indexDesValeurs } from '#lib/dimensions.ts';
	import { garde, rangPratique } from '#lib/rangs.ts';
	import { rendre } from '#lib/markup.ts';
	import { creer, enregistrer } from '#lib/db.ts';
	import { occurrenceDu } from '#lib/pratiques.ts';
	import type { Coche, Fait, FetePerso, NoteJour, Rang } from '#lib/types.ts';
	import Icone from '#lib/design/Icone.svelte';
	import { actionsDeGraces } from '#lib/anniversaires.ts';
	import Accueil from '#lib/design/Accueil.svelte';
	import CarteCouronne from '#lib/design/CarteCouronne.svelte';
	import { couronnesDeLaBase, marquerVue, vues, type Couronne } from '#lib/couronnes.ts';
	import { enMinutes } from '#lib/durees.ts';
	import { chargerIndulgences, enClair, enJours, type Indulgences } from '#lib/indulgences.ts';
	import {
		indulgencesDuJour,
		jaculatoireAOuvrir,
		jaculatoiresPermises,
		minutesDeLaLigne,
		minutesDUneRecitation,
		recitations,
		texteDeLaJournee
	} from '#lib/programme/bilan.ts';
	import { etatDesLectures } from '#lib/programme/lectures.ts';
	import { cocher, direJaculatoire } from '#lib/programme/suivi.ts';
	import { journeeVivante } from '#lib/programme/vivant.svelte.ts';
	import { DIMENSIONS, type Ligne, type Moment } from '#lib/programme/types.ts';

	/**
	 * Aujourd'hui (SPEC § 11) : la journée calculée par le programme unique. Une page par pratique, une seule fois par
	 * jour ; ce qui se lit est résumé en une ligne ; jauges et bilan derrière un bouton ; une jaculatoire à chaque ouverture.
	 */
	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const vie = journeeVivante(() => date);
	const jour = $derived(vie.jour);
	const jr = $derived(vie.jr);

	const d = $derived(new Date(date + 'T12:00:00'));
	const dateLongue = $derived(d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }));
	const solennel = $derived(jour?.rang === '1re cl.' || jour?.rang === 'dim. 1re cl.');
	const MOMENTS: [Moment, string][] = [
		['matin', 'Matin'],
		['journee', 'Au fil du jour'],
		['soir', 'Soir']
	];

	// coches et faits du jour
	const cochesDuJour = vivantSelon(() => {
		const k = date;
		return () => db.coches.where('date').equals(k).toArray();
	}, [] as Coche[]);
	const faitsDuJour = vivantSelon(() => {
		const k = date;
		return () => db.faits.where('date').equals(k).toArray();
	}, [] as Fait[]);
	const coches = $derived.by(() => {
		const n: Record<string, number> = {};
		for (const c of cochesDuJour.v) n[c.elementId] = (n[c.elementId] ?? 0) + 1;
		return n;
	});
	const idsPratiques = $derived(new Set(vie.pratiques.map((p) => p.id)));
	/** Récitations faites d'une ligne (une pratique du plan se suit dans `faits`). */
	const faites = (l: Ligne) => (idsPratiques.has(l.id) ? (faitsDuJour.v.some((f) => f.pratiqueId === l.id) ? 1 : 0) : (coches[l.id] ?? 0));
	const finie = (l: Ligne) => faites(l) >= recitations(l);

	// jour chargé : seules les pratiques du rang choisi et au-dessus (réglage gardé pour ce jour, sur cet appareil)
	let seuil = $state<Rang>('supererogatoria');
	$effect(() => {
		let v: string | null = null;
		try {
			v = localStorage.getItem(`seuil:${date}`);
		} catch {
			/* stockage indisponible */
		}
		seuil = (v as Rang) || 'supererogatoria';
	});
	function regler(r: Rang) {
		seuil = r;
		try {
			localStorage.setItem(`seuil:${date}`, r);
		} catch {
			/* stockage indisponible */
		}
	}
	const SEUILS: [Rang, string, string][] = [
		['supererogatoria', 'Omnia', 'tout afficher'],
		['pia', 'Sine supererogatoriis', 'laisser les dévotions surérogatoires'],
		['praecipua', 'Præcipua tantum', 'seulement les dévotions principales']
	];
	const rangDe = (l: Ligne): Rang => {
		const p = vie.pratiques.find((x) => x.id === l.id);
		return p ? rangPratique(p) : (l.rang ?? 'pia');
	};
	const lignes = $derived((jr?.lignes ?? []).filter((l) => garde(rangDe(l), seuil)));

	// lectures du jour : une ligne qui les résume (n/N), cochées une à une
	const etatLectures = $derived(jr ? etatDesLectures(jr, coches, vie.corps) : null);
	const lectures = $derived(etatLectures?.lectures ?? []);
	const lues = $derived(etatLectures?.lues ?? 0);
	async function lire(id: string) {
		if (coches[id]) await db.coches.where('[date+elementId]').equals([date, id]).delete();
		else await db.coches.add({ date, elementId: id, rang: 0, horodatage: new Date().toISOString() });
	}

	// avancement : chaque ligne compte pour une, et « Lectures du jour » pour une
	const total = $derived(lignes.length + (lectures.length ? 1 : 0));
	const faits = $derived(lignes.filter(finie).length + (lectures.length && lues === lectures.length ? 1 : 0));

	// durées d'après les pages composées
	const minutes = $derived.by(() => {
		let tout = 0,
			fait = 0;
		for (const l of lignes) {
			const m = minutesDeLaLigne(l, vie.corps);
			tout += m;
			fait += (m * Math.min(faites(l), recitations(l))) / recitations(l);
		}
		return { tout, fait };
	});

	// indulgences : seulement les fiches de l'Enchiridion de 1952 (traduction approuvée)
	let ind = $state<Indulgences | null>(null);
	chargerIndulgences().then((x) => (ind = x));
	const jaculatoiresDites = $derived(
		new Map(
			Object.entries(coches)
				.filter(([k]) => k.startsWith('jac:'))
				.map(([k, n]) => [k.slice(4), n])
		)
	);
	const indulgences = $derived(ind && jr ? indulgencesDuJour({ ...jr, lignes }, faites, jaculatoiresDites, ind, jour?.tempora) : null);

	// jaculatoire d'ouverture : une autre à chaque ouverture, jamais une de celles que disent déjà les pages du jour
	let jaculatoire = $state<string | undefined>();
	let ditePourCetteOuverture = $state(false);
	$effect(() => {
		if (jaculatoire || !jr || !ind) return;
		let derniere: string | undefined;
		try {
			derniere = localStorage.getItem('jaculatoire-derniere') ?? undefined;
		} catch {
			/* stockage indisponible */
		}
		const permises = jaculatoiresPermises(JACULATOIRES, ind, (id) => vie.textes.has(id));
		jaculatoire = jaculatoireAOuvrir(permises, vie.corps, texteDeLaJournee([...jr.lignes, ...jr.lectures], vie.corps), derniere);
		try {
			if (jaculatoire) localStorage.setItem('jaculatoire-derniere', jaculatoire);
		} catch {
			/* stockage indisponible */
		}
	});
	async function dire() {
		if (!jaculatoire || ditePourCetteOuverture) return;
		ditePourCetteOuverture = true;
		await direJaculatoire(jaculatoire, date);
	}
	const valeurJaculatoire = $derived(jaculatoire && ind?.fiches[jaculatoire]?.partielles.map((p) => p.texte).join(' ; '));

	// lot « Dimensions » : le contexte du jour et ce que couvrent ses prières, calculés par journee() ; ils décrivent la
	// journée, ils ne la changent pas
	const libelle = (d: string, v: string) =>
		vie.vocabulaire?.dimensions[d as keyof NonNullable<typeof vie.vocabulaire>['dimensions']]?.valeurs[v] ?? v;
	const ligneDeContexte = $derived(
		jr
			? [...jr.contexte.objets.map((o) => libelle('objet', o)), ...jr.contexte.fins.map((f) => `temps de ${libelle('fin', f)}`)].join(' · ')
			: ''
	);
	const sourcesDuContexte = $derived(jr ? jr.contexte.sources.map((s) => `${libelle(s.dimension, s.valeur)} ← ${s.de}`).join(' ; ') : '');
	const index = $derived(indexDesValeurs(vie.textes.values(), vie.classements));
	/** Une prière de la bibliothèque, la plus courte, qui porte la valeur et n'est pas déjà dite ce jour-là. */
	const propositionPour = (d: string, v: string) => index.get(`${d}:${v}`)?.find((t) => !jr?.textes.has(t.id));
	const manquesRequis = $derived((jr?.manques ?? []).filter((m) => m.requis));
	// promesses attachées aux pratiques du jour
	const promesses = $derived(
		vie.pratiques
			.filter((p) => p.active && !p.supprimeLe && p.promesses?.trim())
			.map((p) => ({ p, o: occurrenceDu(p, date) }))
			.filter((x) => x.o)
	);

	/** Sous-titre d'une ligne : la prière du jour quand elle change (chapelet, couronne), et les pratiques du plan. */
	function sousTitre(l: Ligne): string {
		const premier = l.sections.find((s) => s.genre === 'texte' && s.texte && s.origine === l.id);
		const variante = l.sousTitre || (premier?.variante && premier.texte ? (vie.textes.get(premier.texte)?.titre ?? '') : '');
		return [variante, ...l.annotations.map((a) => a.texte)].filter(Boolean).join(' · ');
	}
	const ROMAINS = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix'];

	// fêtes et anniversaires personnels du jour
	const fetes = vivantSelon(() => {
		const md = [d.getMonth() + 1, d.getDate()];
		return () => db.fetes.where('[mois+jour]').equals(md).toArray();
	}, [] as FetePerso[]);
	const fetesDuJour = $derived(fetes.v.filter((f) => !f.supprimeLe));
	const anniversaire = (f: FetePerso) =>
		f.annee && d.getFullYear() > f.annee
			? `, ${d.getFullYear() - f.annee}${d.getFullYear() - f.annee === 1 ? 'er' : 'e'} anniversaire`
			: '';

	// note du jour
	const note = vivantSelon(
		() => {
			const k = `note:${date}`;
			return () => db.notes.get(k);
		},
		undefined as NoteJour | undefined
	);
	async function noter(corps: string) {
		const existante = await db.notes.get(`note:${date}`);
		if (existante) await enregistrer('notes', { ...existante, corps });
		else if (corps.trim()) await creer<NoteJour>('notes', { id: `note:${date}`, origine: 'personnel', date, corps });
	}
	const decaler = (n: number) => {
		const x = new Date(d);
		x.setDate(x.getDate() + n);
		return iso(x);
	};
	const estAujourdhui = $derived(date === iso(new Date()));

	// écran d'accueil : une fois par ouverture de l'app (mémorisé pour la session de l'onglet)
	let accueil = $state(false);
	$effect(() => {
		try {
			accueil = !sessionStorage.getItem('accueil-vu');
		} catch {
			accueil = false;
		}
	});
	function entrer() {
		accueil = false;
		try {
			sessionStorage.setItem('accueil-vu', '1');
		} catch {
			/* stockage indisponible */
		}
	}
	// couronnes : une quête achevée s'annonce une fois, par une carte (recalculée quand on coche)
	let nouvelle = $state<Couronne | null>(null);
	$effect(() => {
		void cochesDuJour.v.length;
		void faitsDuJour.v.length;
		if (!estAujourdhui) return;
		Promise.all([couronnesDeLaBase(date), vues()]).then(([cs, v]) => {
			nouvelle = [...cs].reverse().find((c) => !v.has(c.id)) ?? null;
		});
	});
	// la barre d'onglets se retire derrière la carte, comme pour l'écran d'accueil
	$effect(() => {
		const ouvert = !!nouvelle && estAujourdhui && !accueil;
		document.documentElement.classList.toggle('accueil-ouvert', ouvert);
		return () => document.documentElement.classList.remove('accueil-ouvert');
	});
	async function rendreGrace() {
		if (nouvelle) await marquerVue(nouvelle.id);
		const [cs, v] = await Promise.all([couronnesDeLaBase(date), vues()]);
		nouvelle = [...cs].reverse().find((c) => !v.has(c.id)) ?? null;
	}
</script>

<svelte:head><title>Aujourd’hui — Hortus Sacrum</title></svelte:head>

{#if jour && accueil && estAujourdhui}
	<Accueil
		introit={jour.introit_incipit ?? ''}
		introitFr={jour.introit?.fr?.[0] ?? ''}
		invocation={jour.martyrologe.map((m) => invocation(m.texte)?.texte).find(Boolean) ?? ''}
		avancement={total ? faits / total : 0}
		{entrer}
	/>
{:else if nouvelle && estAujourdhui}
	<div class="voile-couronne" role="dialog" aria-modal="true" aria-label="Couronne achevée : {nouvelle.titre}">
		<CarteCouronne c={nouvelle} fermer={rendreGrace} />
	</div>
{/if}
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
			{#if ligneDeContexte}<p class="contexte" title={sourcesDuContexte}>{ligneDeContexte}</p>{/if}

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
				{#if actionsDeGraces(f.profil).length}
					<p class="graces petit">
						<span class="pc rub">En action de grâces :</span>
						{#each actionsDeGraces(f.profil) as [id, nom], i (id)}{#if i}
								·
							{/if}<a href="/prieres/{encodeURIComponent(id)}">{nom}</a>{/each}
					</p>
				{/if}
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

		{#if jaculatoire && vie.textes.get(jaculatoire)}
			{@const t = vie.textes.get(jaculatoire)!}
			<button class="jaculatoire brut" class:dite={ditePourCetteOuverture} onclick={dire} aria-pressed={ditePourCetteOuverture}>
				<span class="jac-texte">{t.corps.replace(/\s+/g, ' ').trim()}</span>
				<span class="jac-pied interface">
					{#if ditePourCetteOuverture}Dite{valeurJaculatoire ? ` · ${valeurJaculatoire}` : ''}{:else}Toucher pour la dire{valeurJaculatoire
							? ` · ${valeurJaculatoire}`
							: ''}{/if}
				</span>
			</button>
		{/if}

		<section class="liste" aria-label="Liste du jour">
			<details class="bilan">
				<summary class="interface">
					<span class="etiquette">Bilan du jour</span>
					<span class="trait"><span style="width: {total ? (100 * faits) / total : 0}%"></span></span>
					<span class="chiffres-alignes"
						>{faits} / {total}{minutes.tout > 0 ? ` · ${enMinutes(Math.max(0, minutes.tout - minutes.fait))} restantes` : ''}</span
					>
				</summary>
				<div
					class="avancement interface temps"
					title="Durée estimée d’après les pages du jour ; chaque durée se règle dans « Régler le programme »"
				>
					<span class="etiquette">Temps de prière</span>
					<span class="trait"><span style="width: {minutes.tout ? (100 * minutes.fait) / minutes.tout : 0}%"></span></span>
					<span class="chiffres-alignes">{enMinutes(minutes.fait)} / {enMinutes(minutes.tout)}</span>
				</div>
				{#if indulgences && enJours(indulgences.possibles) > 0}
					<div class="avancement interface indulg" title="Indulgences partielles des prières cochées (Enchiridion de 1952)">
						<span class="etiquette">Indulgences</span>
						<span class="trait"
							><span style="width: {Math.min(100, (100 * enJours(indulgences.gagnees)) / enJours(indulgences.possibles))}%"></span></span
						>
						<span class="chiffres-alignes">{enClair(indulgences.gagnees)}</span>
					</div>
					<p class="aide total">
						sur {enClair(indulgences.possibles)} pour le programme entier ; indulgences partielles de l’Enchiridion de 1952
					</p>
				{/if}
				{#if promesses.length}
					<p class="aide"><strong>Promesses en cours</strong></p>
					{#each promesses as { p, o } (p.id)}<p class="aide">
							<strong>{p.titre}</strong>{#if o?.total}
								({o.rang}/{o.total}){/if} : {p.promesses}
						</p>{/each}
				{/if}
				{#if jr && vie.vocabulaire}
					<details class="cadre">
						<summary class="aide"
							>Fins, objets, grâces, personnes, formes{manquesRequis.length
								? ` : manque ${manquesRequis.map((m) => libelle(m.dimension, m.valeur)).join(', ')}`
								: ''}</summary
						>
						{#each DIMENSIONS as d (d)}
							{@const couvertes = jr.couverture[d]}
							{@const manques = jr.manques.filter((m) => m.dimension === d)}
							<p class="aide">
								<strong>{vie.vocabulaire.dimensions[d].libelle}</strong> — couvert : {couvertes
									.map((c) => libelle(d, c.valeur))
									.join(', ') || 'rien'}.
							</p>
							{#if manques.length}
								<ul class="aide manques">
									{#each manques as m (m.valeur)}
										{@const p = propositionPour(d, m.valeur)}
										<li class:requis={m.requis}>
											{libelle(d, m.valeur)}{#if p}
												: <a href={`/prieres/${encodeURIComponent(p.id)}`}>{p.titre}</a>{/if}
										</li>
									{/each}
								</ul>
							{/if}
						{/each}
						<p class="aide">Le classement des prières se relit dans leur fiche (Modifier) ; il ne change pas la liste du jour.</p>
					</details>
				{/if}
				{#if jr?.a_fournir.length}
					<p class="aide">
						À transcrire pour ce jour : {jr.a_fournir.map((a) => a.quoi).join(' ; ')}.
					</p>
				{/if}
				<div class="seuils interface" role="group" aria-label="Jour chargé : quelles dévotions afficher">
					{#each SEUILS as [r, latin, fr] (r)}
						<button class="brut" aria-pressed={seuil === r} title={fr} onclick={() => regler(r)}>{latin}</button>
					{/each}
				</div>
				<p class="regler"><a href="/programme">Régler le programme</a></p>
			</details>

			{#if !jr}
				<p class="aide attente">Le programme du jour se prépare…</p>
			{/if}
			{#each MOMENTS as [moment, nom] (moment)}
				{@const elements = lignes.filter((l) => l.moment === moment)}
				{#if elements.length || (moment === 'journee' && lectures.length)}
					<div class="tete">
						<Ornement nom="grecque" />
						<h2>{nom}</h2>
					</div>
					<ul>
						{#each elements as l (l.id)}
							{@const n = recitations(l)}
							{@const fait = faites(l)}
							{@const sous = sousTitre(l)}
							{@const m = minutesDUneRecitation(l, vie.corps)}
							<li class:fini={fait >= n}>
								<Case libelle={l.titre} bind:cochee={() => fait >= n, () => cocher(l, date, fait, idsPratiques)} />
								<div class="corps">
									<a class="titre" href="/pratique/{encodeURIComponent(l.id)}?date={date}">{l.titre}</a>
									{#if sous}<span class="sous">{sous}</span>{/if}
									{#if l.heures?.length}<span class="heures interface">{l.heures.join(', ')}</span>{/if}
									{#if m > 0}<span class="duree interface">≈ {enMinutes(m)}</span>{/if}
								</div>
								{#if n > 1}
									<button
										class="medaillon brut"
										onclick={() => cocher(l, date, fait, idsPratiques)}
										aria-label="{fait} sur {n} : compter une récitation de plus"
									>
										<Ornement nom="medaillon" taille={34} />
										<span class="pc">{ROMAINS[fait] || '·'}<i>/</i>{ROMAINS[n]}</span>
									</button>
								{/if}
							</li>
						{/each}
						{#if moment === 'journee' && lectures.length}
							<li class="lectures" class:fini={lues === lectures.length}>
								<span class="compte pc chiffres-alignes" aria-hidden="true">{lues}/{lectures.length}</span>
								<div class="corps">
									<a class="titre" href="/lecture{estAujourdhui ? '' : `?date=${date}`}">Lectures du jour ({lues}/{lectures.length})</a>
									<details class="a-lire">
										<summary class="sous">{lectures.map((x) => x.lecture.titre).join(' · ')}</summary>
										{#each lectures as x (x.lecture.id)}
											{@const l = x.lecture}
											{@const lien = `${l.route}${estAujourdhui ? '' : `?date=${date}`}`}
											<p class="lu">
												{#if x.heures}
													<span class="heures-dites pc chiffres-alignes" aria-hidden="true">{x.faites}/{x.total}</span>
													<a href={lien}
														>{l.titre} : {x.faites} heure{(x.faites ?? 0) > 1 ? 's' : ''} dite{(x.faites ?? 0) > 1 ? 's' : ''} sur {x.total}</a
													>
												{:else}
													<Case libelle="{l.titre} : lu" bind:cochee={() => x.lu, () => lire(l.id)} />
													<a href={lien}>{l.titre}</a>
												{/if}
											</p>
										{/each}
									</details>
								</div>
							</li>
						{/if}
					</ul>
				{/if}
			{/each}
		</section>

		<details class="note-jour" open={!!note.v?.corps}>
			<summary class="pc">Note du jour</summary>
			<textarea
				rows="3"
				aria-label="Note du jour"
				value={note.v?.corps ?? ''}
				onblur={(ev) => noter(ev.currentTarget.value)}
				placeholder="Une intention, une résolution, une grâce reçue"
			></textarea>
		</details>

		<details class="martyrologe">
			<summary>
				<span class="pc">Martyrologe</span>
				<span class="etiquette">{jour.martyrologe.length} éloge{jour.martyrologe.length > 1 ? 's' : ''} · les saints de ce jour</span>
			</summary>
			{#each jour.martyrologe as m, i (i)}
				{@const inv = invocation(m.texte)}
				{@const la = invocationLatine(m.texte_la)?.texte ?? nomLatin(m.texte_la)}
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
		</details>

		<div class="cul"><Ornement nom="fleuron" /></div>
	</main>
{/if}

<style>
	.bandeau {
		height: 5px;
		border-bottom: var(--hs-cheveu) solid var(--hs-or-trait);
	}
	.ecran {
		max-width: var(--hs-colonne);
		margin: 0 auto;
		padding: var(--hs-e6) var(--hs-marge-mobile) 0;
	}
	.jour {
		text-align: center;
	}
	.date {
		margin: 0;
		font-size: 1.0625rem;
		color: var(--hs-encre-douce);
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 4px;
	}
	.pas {
		display: inline-grid;
		place-items: center;
		width: 40px;
		height: 40px;
		color: var(--hs-encre-douce);
	}
	.contexte {
		margin: -2px 0 var(--hs-e4);
		font-size: 0.9375rem;
		font-style: italic;
		color: var(--hs-encre-douce);
	}
	ul.manques {
		margin: 0 0 var(--hs-e2);
		padding-left: 1.2em;
		list-style: disc;
	}
	.manques li {
		display: list-item;
		min-height: 0;
		padding: 2px 0;
		border: 0;
	}
	.manques li.requis {
		color: var(--hs-encre);
		font-weight: 600;
	}
	.revenir {
		margin: 0;
		font-size: 1rem;
	}
	a.titre {
		color: var(--hs-encre);
		text-decoration: none;
	}
	.temps {
		margin: 2px 0 var(--hs-e5);
	}
	h1 {
		font-size: var(--hs-t3);
	}
	h1.fete {
		color: var(--hs-rubrique);
	}
	.rang {
		margin: 0;
		color: var(--hs-encre-douce);
		font-size: 1.0625rem;
	}
	.comm {
		margin: 0;
		font-size: 1rem;
		font-style: italic;
		line-height: 1.4;
		text-wrap: balance;
	}
	.comm .pc {
		font-style: normal;
		color: var(--hs-encre-douce);
	}
	.jeune {
		margin: var(--hs-e2) 0 0;
		font-size: 1.0625rem;
	}

	.introit {
		margin-top: var(--hs-e5);
		border-block: var(--hs-cheveu) solid var(--hs-filet);
		text-align: left;
	}
	.introit summary {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		justify-content: center;
		gap: 4px 12px;
		padding: var(--hs-e3) 0;
	}
	.station {
		font-size: 0.9375rem;
		color: var(--hs-encre-douce);
		font-style: italic;
		flex-basis: 100%;
		text-align: center;
	}
	.colonnes {
		display: grid;
		gap: var(--hs-e5);
		padding: var(--hs-e2) 0 var(--hs-e4);
	}
	.colonnes :global(.lecture p) {
		text-align: left;
		font-size: 1.0625rem;
	}
	.source {
		font-size: 0.875rem;
		color: var(--hs-encre-douce);
		font-style: italic;
		text-align: center;
		margin: 0 0 var(--hs-e4);
	}

	.liste {
		margin-top: var(--hs-e7);
	}
	.avancement {
		display: flex;
		align-items: center;
		gap: 12px;
		color: var(--hs-encre-douce);
	}
	.trait {
		flex: 1;
		height: 1px;
		background: var(--hs-filet);
		position: relative;
	}
	.trait span {
		position: absolute;
		inset: -1px auto -1px 0;
		background: var(--hs-vert);
		transition: width var(--hs-duree-lente) var(--hs-courbe);
	}

	.indulg {
		margin-top: var(--hs-e2);
	}
	.indulg .trait span {
		background: var(--hs-or);
	}
	.total {
		margin: 2px 0 0;
		text-align: right;
	}
	.perso {
		margin: var(--hs-e3) 0 0;
		font-style: italic;
	}
	.voile-couronne {
		position: fixed;
		inset: 0;
		z-index: 30;
		overflow-y: auto;
		padding: calc(24px + env(safe-area-inset-top)) var(--hs-marge-mobile) calc(24px + env(safe-area-inset-bottom));
		background: color-mix(in srgb, var(--hs-fond) 94%, transparent);
		display: grid;
		place-items: center;
		animation: venir-carte 700ms var(--hs-courbe);
	}
	@keyframes venir-carte {
		from {
			opacity: 0;
			transform: translateY(8px);
		}
		to {
			opacity: 1;
			transform: none;
		}
	}
	.graces {
		margin: 2px 0 0;
		padding-left: 1.2em;
	}
	.note-jour {
		margin-top: var(--hs-e6);
		border-block: var(--hs-cheveu) solid var(--hs-filet);
	}
	.note-jour summary {
		padding: 12px 0;
		color: var(--hs-encre-douce);
	}
	.note-jour textarea {
		margin-bottom: var(--hs-e4);
	}
	.regler {
		margin: var(--hs-e2) 0 0;
		text-align: right;
		font-family: var(--hs-interface);
		font-size: var(--hs-t0);
		letter-spacing: var(--hs-chasse-interface);
	}
	.tete {
		margin-top: var(--hs-e7);
		text-align: center;
		display: grid;
		gap: var(--hs-e3);
	}
	.tete h2 {
		font-size: var(--hs-t2);
	}
	ul {
		list-style: none;
		margin: var(--hs-e3) 0 0;
		padding: 0;
	}
	li {
		display: flex;
		align-items: center;
		gap: 14px;
		padding: 11px 0;
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
		min-height: 56px;
	}
	.corps {
		flex: 1;
		min-width: 0;
		display: grid;
	}
	.titre {
		line-height: 1.3;
		transition: color var(--hs-duree) var(--hs-courbe);
	}
	li.fini .titre {
		color: var(--hs-encre-douce);
	}
	.sous {
		font-style: italic;
		font-size: 1rem;
		line-height: 1.35;
		color: var(--hs-encre-douce);
	}
	.heures {
		color: var(--hs-encre-douce);
		font-size: 0.75rem;
		margin-top: 2px;
	}
	.duree {
		color: var(--hs-encre-douce);
		font-size: 0.75rem;
		margin-top: 2px;
		opacity: 0.85;
	}
	.seuils {
		display: flex;
		justify-content: flex-end;
		flex-wrap: wrap;
		gap: var(--hs-e1, 6px) var(--hs-e2);
		margin: var(--hs-e1, 6px) 0 0;
		font-size: var(--hs-t0);
		letter-spacing: var(--hs-chasse-interface);
	}
	.seuils button {
		color: var(--hs-encre-douce);
		padding: 2px 0;
		min-height: 0;
		background: none;
		border: 0;
		border-bottom: 1px solid transparent;
		font: inherit;
		letter-spacing: inherit;
		cursor: pointer;
	}
	.seuils button[aria-pressed='true'] {
		color: var(--hs-encre);
		border-bottom-color: currentColor;
	}
	.medaillon {
		position: relative;
		flex: none;
		width: 34px;
		height: 34px;
		padding: 0;
		border: 0;
		background: none;
		color: var(--hs-or);
		cursor: pointer;
		line-height: 0;
	}
	.medaillon span {
		position: absolute;
		inset: 0;
		display: grid;
		place-items: center;
		grid-auto-flow: column;
		justify-content: center;
		color: var(--hs-encre);
		font-size: 0.8125rem;
		line-height: 1;
	}
	.medaillon i {
		font-style: normal;
		color: var(--hs-encre-douce);
		margin: 0 1px;
	}
	li.fini .medaillon {
		color: var(--hs-vert);
	}

	.eloge {
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
	}
	.eloge summary {
		padding: 10px 0;
	}
	.invocation::before {
		content: '✠';
		color: var(--hs-rubrique);
		margin-right: 10px;
		font-size: 0.8em;
	}
	.invocation.sans {
		color: var(--hs-encre-douce);
		font-style: italic;
	}
	.invocation.sans::before {
		content: '·';
	}
	.nom-latin {
		display: block;
		margin-left: 1.55rem;
		font-size: 1rem;
		font-style: italic;
		color: var(--hs-encre-douce);
		line-height: 1.35;
	}
	.texte {
		margin: 0 0 12px 1.5rem;
		font-size: 1.0625rem;
		text-align: justify;
		hyphens: auto;
	}
	.tous {
		text-align: center;
		margin: var(--hs-e5) 0 var(--hs-e2);
		font-style: italic;
	}
	.cul {
		margin: var(--hs-e7) auto 0;
		max-width: 16rem;
	}

	.jaculatoire {
		display: grid;
		gap: 4px;
		width: 100%;
		margin: var(--hs-e5) 0 0;
		padding: var(--hs-e3) var(--hs-e2);
		background: none;
		border: 0;
		border-block: var(--hs-cheveu) solid var(--hs-or-trait);
		text-align: center;
		cursor: pointer;
		color: var(--hs-encre);
		font: inherit;
	}
	.jac-texte {
		font-style: italic;
		font-size: 1.125rem;
		line-height: 1.4;
		text-wrap: balance;
	}
	.jac-pied {
		font-size: var(--hs-t0);
		letter-spacing: var(--hs-chasse-interface);
		color: var(--hs-encre-douce);
	}
	.jaculatoire.dite .jac-pied {
		color: var(--hs-vert);
	}
	.bilan summary {
		display: flex;
		align-items: center;
		gap: 12px;
		color: var(--hs-encre-douce);
		cursor: pointer;
		min-height: 44px;
	}
	.bilan[open] summary {
		margin-bottom: var(--hs-e2);
	}
	.attente {
		margin-top: var(--hs-e5);
		font-style: italic;
	}
	li.lectures {
		align-items: flex-start;
	}
	.compte {
		flex: none;
		width: 26px;
		text-align: center;
		color: var(--hs-or-texte);
		font-size: 0.875rem;
		padding-top: 4px;
	}
	.heures-dites {
		flex: none;
		width: 26px;
		text-align: center;
		font-size: 0.75rem;
		color: var(--hs-or-texte);
	}
	.a-lire summary {
		cursor: pointer;
	}
	.lu {
		display: flex;
		align-items: center;
		gap: 12px;
		margin: 8px 0 0;
	}
	.martyrologe {
		margin-top: var(--hs-e6);
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
	}
	.martyrologe > summary {
		display: grid;
		justify-items: center;
		gap: 2px;
		padding: var(--hs-e3) 0;
		cursor: pointer;
		font-size: var(--hs-t2);
	}

	@media (min-width: 700px) {
		h1 {
			font-size: var(--hs-t4);
		}
		.colonnes {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
