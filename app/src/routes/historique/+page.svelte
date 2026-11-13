<script lang="ts">
	import { iso } from '#lib/calendrier.ts';
	import { db } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import { occurrences } from '#lib/pratiques.ts';
	import type { Coche, ElementListe, Fait, Pratique } from '#lib/types.ts';

	/** Historique : régularité de chaque dévotion et grille de constance, depuis le premier jour coché. */
	const liste = vivant(() => db.liste.orderBy('ordre').toArray(), [] as ElementListe[]);
	const coches = vivant(() => db.coches.toArray(), [] as Coche[]);
	const faits = vivant(() => db.faits.toArray(), [] as Fait[]);
	const pratiques = vivant(() => db.pratiques.toArray(), [] as Pratique[]);

	let semaines = $state(12);
	const J = 86400000;
	const auj = new Date(iso(new Date()) + 'T12:00:00');
	// la grille finit le dimanche de la semaine en cours ; on remonte de N semaines
	const finGrille = new Date(auj.getTime() + ((7 - auj.getDay()) % 7) * J);
	const jours = $derived(Array.from({ length: semaines * 7 }, (_, i) => iso(new Date(finGrille.getTime() - (semaines * 7 - 1 - i) * J))));
	const premier = $derived([...$coches.map((c) => c.date), ...$faits.map((f) => f.date)].sort()[0]);
	const compte = (d: string) => !!premier && d >= premier && d <= iso(auj);

	// éléments dont le suivi se fait par les pratiques ou par une page propre
	const GENERIQUES = ['Dévotion à jours comptés', 'Neuvaine ou trentain'];
	const elements = $derived($liste.filter((e) => e.actif && !e.supprimeLe && !GENERIQUES.some((g) => e.titre.startsWith(g))));
	const nCoches = $derived.by(() => {
		const m = new Map<string, number>();
		for (const c of $coches) m.set(`${c.date}|${c.elementId}`, (m.get(`${c.date}|${c.elementId}`) ?? 0) + 1);
		return m;
	});
	const fait = (e: ElementListe, d: string) => (nCoches.get(`${d}|${e.id}`) ?? 0) >= Math.max(1, e.rappels.length);
	const prevu = (e: ElementListe, d: string) => e.jours[new Date(d + 'T12:00:00').getDay()];

	const parJour = $derived(
		jours.map((d) => {
			if (!compte(d)) return { d, taux: -1 };
			const p = elements.filter((e) => prevu(e, d));
			return { d, taux: p.length ? p.filter((e) => fait(e, d)).length / p.length : -1 };
		})
	);
	const niveau = (t: number) => (t < 0 ? 'hors' : t === 0 ? 'n0' : t < 0.34 ? 'n1' : t < 0.67 ? 'n2' : t < 1 ? 'n3' : 'n4');

	const regularite = $derived(
		elements
			.map((e) => {
				const p = jours.filter((d) => compte(d) && prevu(e, d));
				const f = p.filter((d) => fait(e, d)).length;
				return { titre: e.titre, prevus: p.length, faits: f, taux: p.length ? f / p.length : 0, cases: jours.slice(-28).map((d) => (!compte(d) || !prevu(e, d) ? 'hors' : fait(e, d) ? 'fait' : 'manque')) };
			})
			.filter((x) => x.prevus > 0)
	);
	const faitsSet = $derived(new Set($faits.map((f) => `${f.pratiqueId}|${f.date}`)));
	const suiviPratiques = $derived(
		$pratiques
			.filter((p) => p.active && !p.supprimeLe && p.type !== 'roue' && premier)
			.map((p) => {
				const occ = occurrences(p.regle, jours[0] < premier! ? premier! : jours[0], iso(auj));
				const f = occ.filter((o) => faitsSet.has(`${p.id}|${o.date}`)).length;
				return { titre: p.titre, prevus: occ.length, faits: f, taux: occ.length ? f / occ.length : 0 };
			})
			.filter((x) => x.prevus > 0)
	);
	/** Jours de suite où toute la liste a été faite, jusqu'à hier (aujourd'hui n'est pas fini). */
	const serie = $derived.by(() => {
		let n = 0;
		for (let i = parJour.length - 1; i >= 0; i--) {
			const { d, taux } = parJour[i];
			if (d >= iso(auj)) continue;
			if (taux === 1) n++;
			else break;
		}
		return n;
	});
	const pct = (t: number) => `${Math.round(t * 100)} %`;
	const NOMS_JOURS = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];
</script>

<svelte:head><title>Historique — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<h1>Historique</h1>
		<Ornement nom="fleuron" />
		<p class="petit">La constance se compte depuis le premier jour coché{#if premier} ({new Date(premier + 'T12:00:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}){/if}.</p>
	</div>

	{#if !premier}
		<p class="petit">Rien n’a encore été coché : l’historique se remplira de lui-même.</p>
	{:else}
		<div class="rangee choix" role="group" aria-label="Période">
			<button aria-pressed={semaines === 12} onclick={() => (semaines = 12)}>12 semaines</button>
			<button aria-pressed={semaines === 52} onclick={() => (semaines = 52)}>Un an</button>
		</div>

		<section>
			<h2>Grille de constance</h2>
			<div class="grille" style="--n: {semaines}">
				{#each NOMS_JOURS as j, k}<span class="nj" style="grid-row: {k + 1}">{j}</span>{/each}
				{#each parJour as { d, taux }, i (d)}
					<span class="cel {niveau(taux)}" style="grid-row: {(i % 7) + 1}; grid-column: {Math.floor(i / 7) + 2}"
						title="{new Date(d + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })}{taux >= 0 ? ` : ${pct(taux)}` : ''}"></span>
				{/each}
			</div>
			<p class="aide legende">Moins <span class="cel n0"></span><span class="cel n1"></span><span class="cel n2"></span><span class="cel n3"></span><span class="cel n4"></span> plus
				{#if serie} · liste entière tenue {serie} jour{serie > 1 ? 's' : ''} de suite{/if}</p>
		</section>

		<section>
			<h2>Régularité de chaque dévotion</h2>
			<p class="aide">Sur la période choisie ; les petites cases montrent les quatre dernières semaines.</p>
			<ul class="reg">
				{#each regularite.sort((a, b) => b.taux - a.taux) as r (r.titre)}
					<li>
						<span class="nom">{r.titre}</span>
						<span class="mini">{#each r.cases as c}<i class={c}></i>{/each}</span>
						<span class="taux chiffres-alignes" title="{r.faits} sur {r.prevus}">{pct(r.taux)}</span>
					</li>
				{/each}
			</ul>
		</section>

		{#if suiviPratiques.length}
			<section>
				<h2>Pratiques et séries</h2>
				<ul class="reg">
					{#each suiviPratiques as r (r.titre)}
						<li><span class="nom">{r.titre}</span><span class="taux chiffres-alignes">{r.faits} / {r.prevus}</span></li>
					{/each}
				</ul>
			</section>
		{/if}
	{/if}
</main>

<style>
	section { margin-top: var(--hs-e6); }
	section h2 { font-size: var(--hs-t2); margin-bottom: var(--hs-e3); }
	.choix { justify-content: center; }
	.grille { display: grid; grid-template-columns: 1.2rem repeat(var(--n), 1fr); grid-template-rows: repeat(7, auto); gap: 3px; }
	.nj { font-family: var(--hs-interface); font-size: 0.625rem; color: var(--hs-encre-douce); grid-column: 1; align-self: center; }
	.cel { display: inline-block; aspect-ratio: 1; min-width: 6px; border-radius: 2px; background: var(--hs-surface-douce); border: 0.5px solid var(--hs-filet); }
	.legende .cel { width: 11px; vertical-align: middle; margin: 0 1px; }
	.cel.hors { background: transparent; border-color: transparent; }
	.cel.n0 { background: var(--hs-surface-douce); }
	.cel.n1 { background: color-mix(in srgb, var(--hs-vert-brut) 25%, var(--hs-fond)); }
	.cel.n2 { background: color-mix(in srgb, var(--hs-vert-brut) 50%, var(--hs-fond)); }
	.cel.n3 { background: color-mix(in srgb, var(--hs-vert-brut) 75%, var(--hs-fond)); }
	.cel.n4 { background: var(--hs-vert-brut); border-color: var(--hs-or); }
	.reg { list-style: none; padding: 0; margin: 0; }
	.reg li { display: flex; align-items: center; gap: var(--hs-e3); padding: 8px 0; border-bottom: var(--hs-cheveu) solid var(--hs-filet); }
	.nom { flex: 1; min-width: 0; font-size: 1.0625rem; line-height: 1.3; }
	.mini { display: none; gap: 2px; }
	.mini i { width: 6px; height: 10px; background: var(--hs-surface-douce); }
	.mini i.fait { background: var(--hs-vert-brut); }
	.mini i.manque { background: color-mix(in srgb, var(--hs-rubis-brut) 35%, var(--hs-fond)); }
	.mini i.hors { background: transparent; }
	.taux { flex: none; width: 4.2rem; text-align: right; color: var(--hs-encre-douce); font-size: 0.9375rem; }
	@media (min-width: 560px) { .mini { display: flex; } }
</style>
