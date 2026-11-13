<script lang="ts">
	import { page } from '$app/state';
	import { db, estModifie } from '#lib/db.ts';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import { vivant } from '#lib/live.ts';
	import { rendre } from '#lib/markup.ts';
	import type { Texte } from '#lib/types.ts';

	const id = $derived(page.url.searchParams.get('id') ?? 'jardin:te-joseph-celebrent');
	const texte = $derived(vivant(() => db.textes.get(id), undefined as Texte | undefined));
	let latin = $state(true);

	type Bloc = { genre: 'rubrique' | 'verset' | 'titre' | 'traduction' | 'texte'; fr: string; la?: string };

	/** Paragraphes du texte ; les strophes latines s'apparient à la suite de paragraphes simples de même longueur. */
	const blocs = $derived.by((): Bloc[] => {
		const t = $texte;
		if (!t) return [];
		const genre = (p: string): Bloc['genre'] =>
			p.startsWith('[r]') && p.endsWith('[/r]') ? 'rubrique'
			: /^(℣\.|℟\.)/.test(p) ? 'verset'
			: p.startsWith('## ') ? 'titre'
			: p.startsWith('[') ? 'traduction' : 'texte';
		const out: Bloc[] = t.corps.split(/\n{2,}/).filter(Boolean).map((p) => ({ genre: genre(p), fr: p }));
		const la = t.latin.split(/\n{2,}/).filter(Boolean);
		if (la.length) {
			for (let i = 0; i + la.length <= out.length; i++) {
				if (out.slice(i, i + la.length).every((b) => b.genre === 'texte')) {
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

<svelte:head><title>{$texte?.titre ?? 'Prière'} — Hortus Sacrum</title></svelte:head>

{#if $texte}
	{@const t = $texte}
	<main class="ecran entree">
		<a class="retour interface" href="/maquette"><Icone nom="retour" taille={16} /> {$texte.partie || 'Prières'}</a>

		<header>
			<h1>{t.titre}</h1>
			<p class="marques">
				<span class="cartouche {ORIGINE[t.origine][0]}">{ORIGINE[t.origine][1]}</span>
				{#if estModifie(t)}<span class="cartouche personnel">modifié</span>{/if}
			</p>
			{#if t.usage}<p class="usage"><span class="pc rub">usage :</span> <em>{t.usage}</em></p>{/if}
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
			<a class="bouton principal" href="/prieres/{encodeURIComponent(t.id)}">Modifier</a>
			<button class="bouton">Dupliquer</button>
			<button class="bouton danger">Corbeille</button>
		</div>
	</main>
{/if}

<style>
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
