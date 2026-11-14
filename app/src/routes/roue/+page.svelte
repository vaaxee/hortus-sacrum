<script lang="ts">
	import { page } from '$app/state';
	import { iso } from '#lib/calendrier.ts';
	import { db, enregistrer, estModifie, restaurerOriginal } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import Rosace, { type Anneau } from '#lib/design/Rosace.svelte';
	import Icone from '#lib/design/Icone.svelte';
	import { vivant } from '#lib/live.ts';
	import { debutAnnee, elementDu, grandCycle, pas, position, uniteDe } from '#lib/roues.ts';
	import type { Pratique, Texte, UniteRoue } from '#lib/types.ts';

	const date = $derived(page.url.searchParams.get('date') ?? iso(new Date()));
	const d = $derived(new Date(date + 'T12:00:00'));
	const dateLongue = $derived(d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }));
	const decaler = (n: number) => {
		const x = new Date(d);
		x.setDate(x.getDate() + n);
		return iso(x);
	};

	const roues = vivant(async () => (await db.pratiques.toArray()).filter((p) => p.type === 'roue' && !p.supprimeLe), [] as Pratique[]);
	const titres = vivant(async () => Object.fromEntries((await db.textes.toArray()).map((t: Texte) => [t.id, t.titre])), {} as Record<string, string>);
	const n = (r: Pratique) => r.elements?.length ?? 0;
	const actives = $derived($roues.filter((r) => r.active && n(r) > 0).sort((a, b) => n(a) - n(b) || a.titre.localeCompare(b.titre)));
	/** La rosace : roues actives de 2 à 15 éléments ; les longues (lecture suivie) sont données à part. */
	const dansLaRosace = $derived(actives.filter((r) => n(r) > 1 && n(r) <= 15));
	const suivies = $derived(actives.filter((r) => n(r) > 15));
	const unite = $derived(actives.find((r) => n(r) === 1));

	const COULEURS: Record<number, string> = {
		// couleurs fixes de la palette (les rôles changent selon la direction artistique) : vitraux distincts
		3: 'var(--hs-rubis-brut)', 4: 'var(--hs-lapis-brut)', 5: 'var(--hs-rubis-brut)', 7: 'var(--hs-amethyste-brut)', 8: 'var(--hs-vert-brut)',
		9: 'var(--hs-lapis-brut)', 10: 'var(--hs-vert-brut)', 12: 'var(--hs-or-brut)', 15: 'var(--hs-rose-brut)'
	};
	const couleur = (r: Pratique) => COULEURS[n(r)] ?? 'var(--hs-lapis-brut)';
	const anneaux: Anneau[] = $derived(dansLaRosace.map((r) => ({ id: r.id, nombre: n(r), position: position(r, date), couleur: couleur(r), titre: r.titre })));
	let choisi = $state('');

	const ROMAINS = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV'];
	const chiffre = (k: number) => ROMAINS[k] ?? String(k);
	const quotidiennes = $derived(dansLaRosace.filter((r) => uniteDe(r) === 'jour').map(n));
	const cycle = $derived(grandCycle(quotidiennes));
	const jourDuCycle = $derived(cycle > 1 ? (pas(date, 'jour') % cycle) + 1 : 0);
	const debut = $derived(debutAnnee(date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }));

	// ------------------------------------------------------------ réglages
	const parNombre = $derived.by(() => {
		const m = new Map<number, Pratique[]>();
		for (const r of [...$roues].sort((a, b) => a.titre.localeCompare(b.titre))) m.set(n(r), [...(m.get(n(r)) ?? []), r]);
		return [...m.entries()].sort((a, b) => a[0] - b[0]);
	});
	const UNITES: [UniteRoue, string][] = [['jour', 'chaque jour'], ['semaine', 'chaque semaine'], ['mois', 'chaque mois']];
	async function basculer(r: Pratique) {
		await enregistrer('pratiques', { ...r, active: !r.active });
	}
	async function changerUnite(r: Pratique, u: UniteRoue) {
		await enregistrer('pratiques', { ...r, regle: { genre: 'roue', unite: u } });
	}
	async function renommer(r: Pratique, k: number, fr: string) {
		if (!r.elements || r.elements[k].fr === fr.trim() || !fr.trim()) return;
		const elements = r.elements.map((e, i) => (i === k ? { ...e, fr: fr.trim() } : e));
		await enregistrer('pratiques', { ...r, elements });
	}
	let ouverte = $state('');
</script>

<svelte:head><title>La roue — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<p class="etiquette">Rota symbolica</p>
		<h1>La roue</h1>
		<p class="date pc chiffres-alignes">
			<a class="pas" href="/roue?date={decaler(-1)}" aria-label="Jour précédent"><Icone nom="retour" taille={16} /></a>
			{dateLongue}
			<a class="pas" href="/roue?date={decaler(1)}" aria-label="Jour suivant"><Icone nom="chevron" taille={16} /></a>
		</p>
		{#if date !== iso(new Date())}<p><a href="/roue">Revenir à aujourd’hui</a></p>{/if}
	</div>

	{#if anneaux.length}
		<figure class="vitrail">
			<Rosace {anneaux} bind:choisi centre={unite?.elements?.[0].la ?? 'Unus'} />
			<figcaption class="petit">
				Toutes les roues partent ensemble le premier dimanche de l’Avent ({debut}).
				{#if cycle > 1}Jour {jourDuCycle} du grand cycle de {cycle} jours, après lequel elles se retrouvent alignées.{/if}
			</figcaption>
		</figure>
	{/if}

	{#if unite}
		<section class="unite">
			<Ornement nom="croix-pattee" taille={18} />
			<p class="h2">{unite.elements?.[0].fr}</p>
			{#if unite.verset}<p class="verset" lang="la">{unite.verset.la} <span class="ref">({unite.verset.ref})</span></p>{/if}
		</section>
	{/if}

	<ol class="legende">
		{#each dansLaRosace as r (r.id)}
			{@const k = position(r, date)}
			{@const e = elementDu(r, date)}
			<li class:choisi={choisi === r.id} style="--verre: {couleur(r)}">
				<button class="brut nombre" onclick={() => (choisi = r.id)} aria-label="Montrer l’anneau {r.titre}">{chiffre(n(r))}</button>
				<div class="corps">
					<p class="titre-roue pc">{r.titre}</p>
					<p class="element">{e?.fr}</p>
					{#if e?.la}<p class="latin" lang="la">{e.la}{#if e.ref} <span class="ref">({e.ref})</span>{/if}</p>{/if}
					{#if e?.texte}<p class="lien"><a href="/prieres/{encodeURIComponent(e.texte)}">{$titres[e.texte] ?? 'La prière'}</a></p>{/if}
					{#if r.verset}<p class="verset" lang="la">{r.verset.la} <span class="ref">({r.verset.ref})</span></p>{/if}
				</div>
				<span class="rang chiffres-alignes">{k + 1}<i>/</i>{n(r)}</span>
			</li>
		{/each}
	</ol>

	{#each suivies as r (r.id)}
		{@const e = elementDu(r, date)}
		<section class="suivie">
			<div class="tete-section">
				<Ornement nom="grecque" />
				<h2>{r.titre}</h2>
			</div>
			<p class="element">{e?.fr}</p>
			<p class="petit">Jour {position(r, date) + 1} sur {n(r)} ; le cycle recommence ensuite, et chaque premier dimanche de l’Avent.</p>
		</section>
	{/each}

	<details class="regles">
		<summary class="pc">Choisir et régler les roues</summary>
		<p class="aide">Une roue active prend place dans la rosace. Chaque nombre a plusieurs roues : vous pouvez en garder une ou plusieurs.
			Les sources de chaque liste sont indiquées ; les noms des éléments se modifient.</p>
		{#each parNombre as [nombre, liste]}
			<fieldset>
				<legend>{nombre === 1 ? 'L’unité' : nombre > 15 ? 'Lectures suivies' : `Le nombre ${nombre}`}</legend>
				{#each liste as r (r.id)}
					<div class="reglage">
						<label class="case"><input type="checkbox" checked={r.active} onchange={() => basculer(r)} /> {r.titre}</label>
						{#if nombre > 1}
							<select aria-label="Rythme de {r.titre}" value={uniteDe(r)} onchange={(ev) => changerUnite(r, ev.currentTarget.value as UniteRoue)}>
								{#each UNITES as [u, nom]}<option value={u}>{nom}</option>{/each}
							</select>
						{/if}
						<button class="discret" onclick={() => (ouverte = ouverte === r.id ? '' : r.id)} aria-expanded={ouverte === r.id}>éléments</button>
					</div>
					{#if ouverte === r.id}
						<ol class="elements">
							{#each r.elements ?? [] as e, k}
								<li><input type="text" value={e.fr} aria-label="Élément {k + 1}" onblur={(ev) => renommer(r, k, ev.currentTarget.value)} />
									{#if e.la}<span class="latin" lang="la">{e.la.length > 90 ? e.la.slice(0, 90) + '…' : e.la}</span>{/if}</li>
							{/each}
						</ol>
						<p class="aide">Source : {r.source.ouvrage}{r.source.edition ? `, ${r.source.edition}` : ''}{#if r.source.url} — <a href={r.source.url} rel="noopener" target="_blank">lien</a>{/if}</p>
						{#if estModifie(r)}<button class="discret" onclick={() => restaurerOriginal('pratiques', r.id)}>Restaurer l’original</button>{/if}
					{/if}
				{/each}
			</fieldset>
		{/each}
	</details>

	<div class="cul"><Ornement nom="fleuron" /></div>
</main>

<style>
	.date { margin: 0; font-size: 1.0625rem; color: var(--hs-encre-douce); display: flex; align-items: center; justify-content: center; gap: 4px; }
	.pas { display: inline-grid; place-items: center; width: 40px; height: 40px; color: var(--hs-encre-douce); }
	.vitrail { margin: 0 0 var(--hs-e5); }
	figcaption { text-align: center; font-style: italic; margin-top: var(--hs-e4); text-wrap: balance; }
	.unite { text-align: center; display: grid; justify-items: center; gap: var(--hs-e2); color: var(--hs-or-texte); margin: var(--hs-e5) 0; }
	.unite .h2 { color: var(--hs-encre); font-size: var(--hs-t2); }
	.verset { margin: 2px 0 0; font-style: italic; font-size: 0.9375rem; color: var(--hs-encre-douce); line-height: 1.4; }
	.ref { font-style: normal; font-variant-caps: all-small-caps; letter-spacing: 0.04em; }

	.legende { list-style: none; padding: 0; margin: var(--hs-e5) 0 0; border-top: var(--hs-cheveu) solid var(--hs-filet); }
	.legende li { display: flex; gap: var(--hs-e4); align-items: flex-start; padding: var(--hs-e4) 0; border-bottom: var(--hs-cheveu) solid var(--hs-filet); }
	.legende li.choisi { background: linear-gradient(90deg, color-mix(in srgb, var(--verre) 10%, transparent), transparent 70%); }
	.nombre {
		flex: none; width: 3rem; height: 3rem; display: grid; place-items: center; border-radius: 50%; cursor: pointer;
		border: var(--hs-trait) solid var(--hs-or); background: color-mix(in srgb, var(--verre) 22%, var(--hs-fond));
		font-family: var(--hs-titre); font-size: 1.125rem; letter-spacing: 0.04em; color: var(--hs-encre);
	}
	.corps { flex: 1; min-width: 0; }
	.titre-roue { color: var(--hs-encre-douce); font-size: 1rem; }
	.element { margin: 0; font-family: var(--hs-titre); font-style: italic; font-size: var(--hs-t2); line-height: 1.2; color: var(--hs-encre); }
	.latin { margin: 2px 0 0; font-style: italic; font-size: 1rem; color: var(--hs-encre-douce); line-height: 1.4; }
	.lien { margin: 4px 0 0; font-size: 1rem; }
	.rang { flex: none; font-size: 0.9375rem; color: var(--hs-encre-douce); padding-top: 4px; }
	.rang i { font-style: normal; margin: 0 2px; }
	.suivie { text-align: center; }
	.suivie .element { margin-top: var(--hs-e4); }
	.regles { margin-top: var(--hs-e7); border-block: var(--hs-cheveu) solid var(--hs-filet); }
	.regles summary { padding: 12px 0; color: var(--hs-encre-douce); }
	.reglage { display: flex; flex-wrap: wrap; align-items: center; gap: var(--hs-e2) var(--hs-e3); padding: 6px 0; }
	.reglage .case { flex: 1 1 14rem; display: flex; gap: 10px; align-items: baseline; }
	.reglage select { width: auto; }
	.elements { margin: 0 0 var(--hs-e3); padding-left: 1.6rem; }
	.elements li { margin: 4px 0; }
	.elements .latin { display: block; font-size: 0.875rem; }
	.cul { margin: var(--hs-e7) auto 0; max-width: 16rem; }
</style>
