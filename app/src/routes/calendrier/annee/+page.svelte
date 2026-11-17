<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { datesPerso, ecart, moisCivils, plusJours, series, superpositions, temps, type Serie } from '#lib/annee.ts';
	import { anneeLiturgique, iso, MOIS_DEVOTION, NOMS_MOIS, type Jour } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import { debutAnnee } from '#lib/roues-calcul.ts';
	import type { FetePerso, Pratique } from '#lib/types.ts';

	/** Vue d'ensemble de l'année liturgique : frise des mois, ou roue de l'année. Toucher un jour l'ouvre. */
	const aujourdhui = iso(new Date());
	const an = $derived(Number(page.url.searchParams.get('a') ?? debutAnnee(aujourdhui).getFullYear()));
	let jours = $state<Jour[]>([]);
	let charge = $state(false);
	$effect(() => {
		const a = an;
		charge = false;
		anneeLiturgique(a).then((j) => {
			jours = j ?? [];
			charge = true;
		});
	});
	const pratiques = vivant(() => db.pratiques.toArray(), [] as Pratique[]);
	const fetes = vivant(() => db.fetes.toArray(), [] as FetePerso[]);

	const debut = $derived(jours[0]?.date ?? '');
	const fin = $derived(jours[jours.length - 1]?.date ?? '');
	const N = $derived(jours.length);
	const segments = $derived(jours.length ? temps(jours) : []);
	const mois = $derived(debut ? moisCivils(debut, fin) : []);
	const lesSeries = $derived(debut ? series($pratiques, debut, fin) : []);
	const couloirs = $derived(Math.max(0, ...lesSeries.map((s) => s.couloir + 1)));
	const doubles = $derived(superpositions(lesSeries));
	const dates = $derived(debut ? datesPerso($fetes, debut, fin) : []);
	const parDate = $derived(new Map(jours.map((j) => [j.date, j])));
	const grandes = $derived(new Set(jours.filter((j) => j.rang === '1re cl.' || j.rang === 'dim. 1re cl.').map((j) => j.date)));
	const tempsDu = (d: string) => segments.find((s) => s.debut <= d && s.fin >= d);

	// une couleur par dévotion, dans l'ordre où elles apparaissent
	const PALETTE = [
		'var(--hs-rubrique)',
		'var(--hs-amethyste)',
		'var(--hs-or)',
		'var(--hs-vert)',
		'var(--hs-rose)',
		'var(--hs-or-texte)',
		'var(--hs-lapis)'
	];
	const couleurs = $derived(new Map([...new Set(lesSeries.map((s) => s.pratique))].map((id, i) => [id, PALETTE[i % PALETTE.length]])));
	const legende = $derived([...new Map(lesSeries.map((s) => [s.pratique, s])).values()]);

	/** Les superpositions, regroupées par dévotions qui se croisent : « A et B : 5, 7 et 21 septembre ». */
	const conflits = $derived.by(() => {
		const parNoms = new Map<string, string[]>();
		for (const d of [...doubles].sort()) {
			const noms = lesSeries
				.filter((s) => s.dates.includes(d))
				.map((s) => s.titre)
				.join(' et ');
			parNoms.set(noms, [...(parNoms.get(noms) ?? []), d]);
		}
		return [...parNoms].map(([noms, ds]) => ({ noms, dates: ds })).sort((a, b) => a.dates[0].localeCompare(b.dates[0]));
	});
	/** « 5, 7 et 21 septembre ; 2 octobre » ; une suite de jours devient « du 5 au 9 décembre ». */
	function enJours(ds: string[]): string {
		const plages: [string, string][] = [];
		for (const d of ds) {
			const der = plages[plages.length - 1];
			if (der && ecart(der[1], d) === 1) der[1] = d;
			else plages.push([d, d]);
		}
		return plages.map(([a, b]) => (a === b ? dateCourte(a) : `du ${dateCourte(a)} au ${dateCourte(b)}`)).join(', ');
	}
	const dateCourte = (d: string) => new Date(d + 'T12:00:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'long' });

	let vue = $state<'frise' | 'roue'>('frise');
	try {
		if (localStorage.getItem('annee-vue') === 'roue') vue = 'roue';
	} catch {
		/* rien */
	}
	function choisir(v: 'frise' | 'roue') {
		vue = v;
		try {
			localStorage.setItem('annee-vue', v);
		} catch {
			/* rien */
		}
	}
	const ouvrir = (d: string) => goto(`/?date=${d}`);

	// ---- frise : une ligne par mois, une colonne par jour
	const morceaux = (s: Serie, m: { debut: string; fin: string }) => {
		const a = s.debut > m.debut ? s.debut : m.debut,
			b = s.fin < m.fin ? s.fin : m.fin;
		return a <= b
			? {
					a: Number(a.slice(8)),
					b: Number(b.slice(8)),
					premier: a === s.debut,
					points: s.dates.length < ecart(s.debut, s.fin) + 1 ? s.dates.filter((d) => d >= a && d <= b).map((d) => Number(d.slice(8))) : []
				}
			: null;
	};
	const joursDuMois = (m: { an: number; mois: number }) => new Date(m.an, m.mois, 0).getDate();

	// ---- roue : l'année en cercle, à partir du premier dimanche de l'Avent, en haut
	const angle = (i: number) => (i / N) * 2 * Math.PI - Math.PI / 2;
	const pt = (r: number, a: number) => `${(r * Math.cos(a)).toFixed(2)} ${(r * Math.sin(a)).toFixed(2)}`;
	function arc(r1: number, r2: number, i0: number, i1: number): string {
		const a0 = angle(i0),
			a1 = angle(i1);
		const grand = i1 - i0 > N / 2 ? 1 : 0;
		return `M ${pt(r2, a0)} A ${r2} ${r2} 0 ${grand} 1 ${pt(r2, a1)} L ${pt(r1, a1)} A ${r1} ${r1} 0 ${grand} 0 ${pt(r1, a0)} Z`;
	}
	const idx = (d: string) => ecart(debut, d);
	const largeur = $derived(Math.min(9, 70 / Math.max(1, couloirs)));
	const rayonCouloir = (c: number) => 150 - c * (largeur + 2);
	function touche(ev: MouseEvent) {
		const svg = ev.currentTarget as SVGSVGElement;
		const r = svg.getBoundingClientRect();
		const x = ((ev.clientX - r.left) / r.width) * 420 - 210,
			y = ((ev.clientY - r.top) / r.height) * 420 - 210;
		if (Math.hypot(x, y) < 60) return;
		let a = Math.atan2(y, x) + Math.PI / 2;
		if (a < 0) a += 2 * Math.PI;
		ouvrir(plusJours(debut, Math.min(N - 1, Math.floor((a / (2 * Math.PI)) * N))));
	}
	const aujIdx = $derived(debut && aujourdhui >= debut && aujourdhui <= fin ? idx(aujourdhui) : -1);
</script>

<svelte:head><title>L’année — Hortus Sacrum</title></svelte:head>

<main class="ecran entree">
	<div class="vues" role="group" aria-label="Vue">
		<a class="bouton" href="/calendrier">Mois</a>
		<a class="bouton" href="/calendrier/semaine">Semaine</a>
		<span class="bouton actif" aria-current="page">Année</span>
	</div>

	<div class="tete-page">
		<p class="etiquette">Annus Domini</p>
		<h1 class="chiffres-alignes">
			<a class="pas" href="/calendrier/annee?a={an - 1}" aria-label="Année précédente"><Icone nom="retour" taille={18} /></a>
			{an}-{an + 1}
			<a class="pas" href="/calendrier/annee?a={an + 1}" aria-label="Année suivante"><Icone nom="chevron" taille={18} /></a>
		</h1>
		{#if debut}<p class="petit">Du premier dimanche de l’Avent ({dateCourte(debut)}) au {dateCourte(fin)} {fin.slice(0, 4)}.</p>{/if}
		<div class="choix" role="group" aria-label="Forme">
			<button aria-pressed={vue === 'frise'} onclick={() => choisir('frise')}>Frise</button>
			<button aria-pressed={vue === 'roue'} onclick={() => choisir('roue')}>Roue</button>
		</div>
	</div>

	{#if charge && !jours.length}
		<p class="centre">Le calendrier de cette année n’est pas encore généré. <a href="/calendrier/annee">Revenir à l’année en cours</a></p>
	{:else if jours.length}
		{#if vue === 'frise'}
			<div class="frise">
				{#each mois as m (m.debut)}
					{@const n = joursDuMois(m)}
					<section class="mois">
						<h2><span class="pc">{NOMS_MOIS[m.mois]}</span> <span class="devotion">{MOIS_DEVOTION[m.mois]?.nom}</span></h2>
						<div class="grille" style="--n: {n}">
							{#each Array(n) as _, k (k)}
								{@const d = `${m.an}-${String(m.mois).padStart(2, '0')}-${String(k + 1).padStart(2, '0')}`}
								{@const t = tempsDu(d)}
								{#if parDate.has(d)}
									<a
										class="jour"
										href="/?date={d}"
										style="--c: var(--hs-lit-{t?.couleur ?? 'vert'})"
										class:dim={new Date(d + 'T12:00:00').getDay() === 0}
										class:grande={grandes.has(d)}
										class:auj={d === aujourdhui}
										class:double={doubles.has(d)}
										title="{dateCourte(d)} — {parDate.get(d)?.office}"
										aria-label="{dateCourte(d)} : {parDate.get(d)?.office}"
									>
										<span>{k + 1}</span>
										{#if dates.some((x) => x.date === d)}<i class="perso" aria-hidden="true">✦</i>{/if}
									</a>
								{:else}
									<span class="jour hors" aria-hidden="true"></span>
								{/if}
							{/each}
						</div>
						{#if couloirs}
							<div class="couloirs" style="--n: {n}; --k: {couloirs}">
								{#each lesSeries as s (s.pratique + s.debut)}
									{@const x = morceaux(s, m)}
									{#if x}
										{#if x.points.length}
											<span class="fil" style="grid-column: {x.a} / {x.b + 1}; grid-row: {s.couloir + 1}; --c: {couleurs.get(s.pratique)}"
											></span>
											{#each x.points as p (p)}<span
													class="point"
													style="grid-column: {p}; grid-row: {s.couloir + 1}; --c: {couleurs.get(s.pratique)}"
												></span>{/each}
										{:else}
											<span
												class="barre"
												class:debut={x.premier}
												style="grid-column: {x.a} / {x.b + 1}; grid-row: {s.couloir + 1}; --c: {couleurs.get(s.pratique)}"
												title={s.titre}
											></span>
										{/if}
									{/if}
								{/each}
							</div>
						{/if}
						{#each dates.filter((x) => x.date >= m.debut && x.date <= m.fin) as x (x.id + x.date)}
							<p class="date-perso"><span class="or">✦</span> {Number(x.date.slice(8))} : {x.titre}</p>
						{/each}
					</section>
				{/each}
			</div>
		{:else}
			<figure class="roue">
				<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_noninteractive_element_interactions -->
				<svg viewBox="-210 -210 420 420" role="img" aria-label="La roue de l’année {an}-{an + 1}" onclick={touche}>
					<!-- mois -->
					{#each mois as m, i (m.debut)}
						{@const mid = angle((idx(m.debut) + idx(m.fin) + 1) / 2)}
						<path d={arc(184, 200, idx(m.debut), idx(m.fin) + 1)} class="anneau-mois" class:pair={i % 2 === 0} />
						{#if idx(m.fin) - idx(m.debut) > 8}
							<text
								x={190 * Math.cos(mid)}
								y={190 * Math.sin(mid)}
								class="nom-mois"
								transform="rotate({(mid * 180) / Math.PI + 90} {190 * Math.cos(mid)} {190 * Math.sin(mid)})"
								>{NOMS_MOIS[m.mois].slice(0, 4)}</text
							>
						{/if}
					{/each}
					<!-- temps liturgiques -->
					{#each segments as s (s.debut)}
						<path d={arc(162, 182, idx(s.debut), idx(s.fin) + 1)} style="fill: var(--hs-lit-{s.couleur})" class="temps"
							><title>{s.titre}</title></path
						>
					{/each}
					<!-- grandes fêtes -->
					{#each [...grandes] as d (d)}
						<circle cx={158 * Math.cos(angle(idx(d) + 0.5))} cy={158 * Math.sin(angle(idx(d) + 0.5))} r="1.8" class="grande" />
					{/each}
					<!-- dévotions -->
					{#each lesSeries as s (s.pratique + s.debut)}
						{@const r = rayonCouloir(s.couloir)}
						{#if s.dates.length < ecart(s.debut, s.fin) + 1}
							<path
								d={arc(r - largeur / 2 - 0.6, r - largeur / 2 + 0.6, idx(s.debut), idx(s.fin) + 1)}
								style="fill: {couleurs.get(s.pratique)}"
								opacity="0.35"
							/>
							{#each s.dates as d (d)}<circle
									cx={(r - largeur / 2) * Math.cos(angle(idx(d) + 0.5))}
									cy={(r - largeur / 2) * Math.sin(angle(idx(d) + 0.5))}
									r={Math.min(3, largeur / 2)}
									style="fill: {couleurs.get(s.pratique)}"
								/>{/each}
						{:else}
							<path d={arc(r - largeur, r, idx(s.debut), idx(s.fin) + 1)} style="fill: {couleurs.get(s.pratique)}"
								><title>{s.titre}</title></path
							>
						{/if}
					{/each}
					<!-- dates personnelles -->
					{#each dates as x (x.id + x.date)}
						<text x={206 * Math.cos(angle(idx(x.date) + 0.5))} y={206 * Math.sin(angle(idx(x.date) + 0.5)) + 3} class="etoile"
							>✦<title>{x.titre}</title></text
						>
					{/each}
					<!-- aujourd'hui -->
					{#if aujIdx >= 0}
						<line x1="0" y1="0" x2={200 * Math.cos(angle(aujIdx + 0.5))} y2={200 * Math.sin(angle(aujIdx + 0.5))} class="aiguille" />
						<circle cx="0" cy="0" r="3" class="moyeu" />
					{/if}
					<circle r="58" class="centre-roue" />
					<text y="-14" class="centre-titre">Annus Domini</text>
					<text y="8" class="centre-an">{an}-{an + 1}</text>
					{#if aujIdx >= 0}<text y="26" class="centre-temps">{tempsDu(aujourdhui)?.titre.replace('Temps ', '')}</text>{/if}
				</svg>
				<figcaption class="petit">
					Le premier dimanche de l’Avent est en haut ; l’année tourne dans le sens des aiguilles d’une montre. Toucher la roue ouvre ce
					jour.
				</figcaption>
			</figure>
		{/if}

		<section class="legende">
			<Ornement nom="fleuron" />
			<h2 class="pc">Légende</h2>
			<ul class="temps-liste">
				{#each segments as s (s.debut)}<li>
						<span class="pastille" style="--c: var(--hs-lit-{s.couleur})"></span>{s.titre}
						<span class="petit">({dateCourte(s.debut)} – {dateCourte(s.fin)})</span>
					</li>{/each}
			</ul>
			{#if legende.length}
				<h3 class="pc">Mes dévotions</h3>
				<ul>
					{#each legende as s (s.pratique)}
						<li>
							<span class="pastille" style="--c: {couleurs.get(s.pratique)}"></span><a href="/devotions/{encodeURIComponent(s.pratique)}"
								>{s.titre}</a
							>
							<span class="petit"
								>— {lesSeries
									.filter((x) => x.pratique === s.pratique)
									.map((x) => (x.debut === x.fin ? dateCourte(x.debut) : `${dateCourte(x.debut)} – ${dateCourte(x.fin)}`))
									.join(' ; ')}</span
							>
						</li>
					{/each}
				</ul>
			{:else}
				<p class="petit">
					Aucune dévotion à jours comptés cette année (neuvaine, trentain, 33 jours…) : elles apparaîtront ici, sur leurs couloirs.
				</p>
			{/if}
			{#if conflits.length}
				<details class="conflits">
					<summary
						><span class="pc rub">Superpositions</span>
						<span class="petit">({doubles.size} jour{doubles.size > 1 ? 's' : ''}, soulignés en rouge sur la frise)</span></summary
					>
					<ul>
						{#each conflits as c (c.noms)}<li><strong>{c.noms}</strong> : {enJours(c.dates)}</li>{/each}
					</ul>
				</details>
			{/if}
			{#if dates.length}
				<h3 class="pc">Mes dates</h3>
				<ul>
					{#each dates as x (x.id + x.date)}<li><span class="or">✦</span> {dateCourte(x.date)} : {x.titre}</li>{/each}
				</ul>
			{/if}
		</section>
	{/if}
</main>

<style>
	.ecran {
		max-width: 46rem;
		margin: 0 auto;
		padding: var(--hs-e6) var(--hs-marge-mobile) var(--hs-e7);
	}
	.vues {
		display: flex;
		justify-content: center;
		margin-bottom: var(--hs-e5);
	}
	.vues .bouton {
		min-height: 36px;
		border-radius: 0;
	}
	.vues .actif {
		background: color-mix(in srgb, var(--hs-lapis) 14%, transparent);
		border-color: var(--hs-or);
	}
	.tete-page {
		text-align: center;
	}
	h1 {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--hs-e3);
	}
	.pas {
		display: inline-grid;
		place-items: center;
		width: 34px;
		height: 34px;
		color: var(--hs-or-texte);
	}
	.choix {
		display: inline-flex;
		gap: var(--hs-e2);
		margin-top: var(--hs-e3);
	}
	.choix button {
		min-height: 36px;
	}
	.centre {
		text-align: center;
	}

	.frise {
		display: grid;
		gap: var(--hs-e4);
		margin-top: var(--hs-e5);
	}
	.mois h2 {
		font-size: 1rem;
		margin: 0 0 4px;
		display: flex;
		gap: var(--hs-e2);
		align-items: baseline;
		flex-wrap: wrap;
	}
	.devotion {
		font-family: var(--hs-titre);
		font-style: italic;
		color: var(--hs-encre-douce);
		font-size: 0.95rem;
		text-transform: none;
		letter-spacing: 0;
	}
	.grille,
	.couloirs {
		display: grid;
		grid-template-columns: repeat(31, minmax(0, 1fr));
		gap: 1px;
	}
	.jour {
		position: relative;
		aspect-ratio: 1 / 1.25;
		display: grid;
		place-items: end center;
		padding-bottom: 1px;
		border-radius: 2px;
		background: color-mix(in srgb, var(--c) 34%, var(--hs-fond));
		border: 0.5px solid color-mix(in srgb, var(--hs-or) 35%, transparent);
		color: var(--hs-encre);
		text-decoration: none;
		font-size: 0.56rem;
		line-height: 1;
		font-variant-numeric: lining-nums;
	}
	.jour.dim {
		background: color-mix(in srgb, var(--c) 58%, var(--hs-fond));
		font-weight: 600;
	}
	.jour.grande::before {
		content: '';
		position: absolute;
		top: 2px;
		left: 50%;
		width: 4px;
		height: 4px;
		margin-left: -2px;
		border-radius: 50%;
		background: var(--hs-or);
	}
	.jour.auj {
		outline: 1.5px solid var(--hs-rubrique);
		outline-offset: 0;
		z-index: 1;
	}
	.jour.double {
		box-shadow: inset 0 -2px 0 var(--hs-rubrique);
	}
	.jour.hors {
		background: transparent;
		border-color: transparent;
	}
	.perso {
		position: absolute;
		top: -3px;
		right: -1px;
		font-style: normal;
		font-size: 0.6rem;
		color: var(--hs-or-texte);
	}
	.couloirs {
		grid-auto-rows: 6px;
		row-gap: 2px;
		margin-top: 3px;
	}
	.barre {
		background: var(--c);
		border-radius: 3px;
		min-height: 6px;
	}
	.barre.debut {
		border-top-left-radius: 6px;
		border-bottom-left-radius: 6px;
	}
	.fil {
		align-self: center;
		height: 1px;
		background: var(--c);
		opacity: 0.5;
	}
	.point {
		justify-self: center;
		align-self: center;
		width: 6px;
		height: 6px;
		border-radius: 50%;
		background: var(--c);
	}
	.date-perso {
		margin: 3px 0 0;
		font-size: 0.85rem;
		font-style: italic;
	}
	.or {
		color: var(--hs-or-texte);
		font-style: normal;
	}

	.roue {
		margin: var(--hs-e4) auto 0;
		max-width: 520px;
		text-align: center;
	}
	.roue svg {
		width: 100%;
		height: auto;
		cursor: pointer;
	}
	.anneau-mois {
		fill: color-mix(in srgb, var(--hs-or) 10%, var(--hs-fond));
		stroke: var(--hs-or-trait);
		stroke-width: 0.5;
	}
	.anneau-mois.pair {
		fill: color-mix(in srgb, var(--hs-or) 22%, var(--hs-fond));
	}
	.nom-mois {
		font-family: var(--hs-interface);
		font-size: 7px;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		fill: var(--hs-encre-douce);
		text-anchor: middle;
		dominant-baseline: middle;
	}
	.temps {
		stroke: var(--hs-fond);
		stroke-width: 0.6;
		opacity: 0.85;
	}
	circle.grande {
		fill: var(--hs-or);
	}
	.etoile {
		font-size: 9px;
		fill: var(--hs-or-texte);
		text-anchor: middle;
	}
	.aiguille {
		stroke: var(--hs-rubrique);
		stroke-width: 1.4;
	}
	.moyeu {
		fill: var(--hs-rubrique);
	}
	.centre-roue {
		fill: var(--hs-fond);
		stroke: var(--hs-or-trait);
		stroke-width: 0.8;
	}
	.centre-titre {
		font-family: var(--hs-interface);
		font-size: 7.5px;
		letter-spacing: 0.18em;
		text-transform: uppercase;
		fill: var(--hs-or-texte);
		text-anchor: middle;
	}
	.centre-an {
		font-family: var(--hs-titre);
		font-size: 17px;
		fill: var(--hs-encre);
		text-anchor: middle;
	}
	.centre-temps {
		font-family: var(--hs-titre);
		font-style: italic;
		font-size: 8px;
		fill: var(--hs-encre-douce);
		text-anchor: middle;
	}

	.legende {
		margin-top: var(--hs-e6);
	}
	.legende h2 {
		text-align: center;
		font-size: 0.85rem;
		margin: var(--hs-e3) 0;
	}
	.legende h3 {
		font-size: 0.8rem;
		margin: var(--hs-e4) 0 var(--hs-e2);
	}
	.legende ul {
		list-style: none;
		padding: 0;
		margin: 0;
		display: grid;
		gap: 4px;
	}
	.conflits {
		margin-top: var(--hs-e4);
	}
	.conflits summary {
		cursor: pointer;
	}
	.conflits ul {
		margin-top: var(--hs-e2);
	}
	.conflits strong {
		font-weight: 600;
	}
	.pastille {
		display: inline-block;
		width: 10px;
		height: 10px;
		border-radius: 50%;
		background: var(--c);
		margin-right: 8px;
		vertical-align: baseline;
	}
</style>
