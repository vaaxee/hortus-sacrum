<script lang="ts">
	import type { Couronne } from '#lib/couronnes.ts';
	import { lireRef, passage, enClair } from '#lib/ecriture.ts';
	import Ornement from './Ornement.svelte';

	/** Carte enluminée d'une couronne : titre d'honneur, quête accomplie, verset latin en exergue, promesse. */
	let { c, fermer }: { c: Couronne; fermer?: () => void } = $props();

	let verset = $state<{ la: string; fr: string; ref: string } | null>(null);
	$effect(() => {
		const r = lireRef(c.verset);
		if (!r) return;
		passage(r).then((p) => {
			if (p) verset = { la: p.la.map((v) => v[1]).join(' '), fr: p.fr.map((v) => v[1]).join(' '), ref: enClair(r) };
		});
	});
	const dateFr = (s: string) => new Date(s + 'T12:00:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
	const ORDINAL = ['', '', 'deuxième', 'troisième', 'quatrième', 'cinquième', 'sixième', 'septième', 'huitième', 'neuvième', 'dixième'];
</script>

<article class="carte" class:modale={!!fermer}>
	<span class="coin hg" aria-hidden="true"><Ornement nom="coin" taille={22} /></span>
	<span class="coin hd" aria-hidden="true"><Ornement nom="coin" taille={22} /></span>
	<span class="coin bg" aria-hidden="true"><Ornement nom="coin" taille={22} /></span>
	<span class="coin bd" aria-hidden="true"><Ornement nom="coin" taille={22} /></span>

	<svg class="couronne" viewBox="0 0 64 40" aria-hidden="true">
		<path d="M6 34 L4 12 L18 22 L32 4 L46 22 L60 12 L58 34 Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" />
		<path d="M6 34 H58 M8 29 H56" stroke="currentColor" stroke-width="1.2" />
		<circle cx="4" cy="11" r="2.2" fill="currentColor" /><circle cx="32" cy="3" r="2.4" fill="currentColor" /><circle cx="60" cy="11" r="2.2" fill="currentColor" />
		<circle cx="20" cy="31.5" r="1.3" class="gemme" /><circle cx="32" cy="31.5" r="1.6" class="gemme" /><circle cx="44" cy="31.5" r="1.3" class="gemme" />
	</svg>
	<p class="etiquette pc">{c.fois > 1 ? `Couronne achevée pour la ${ORDINAL[c.fois] ?? `${c.fois}e`} fois` : 'Couronne achevée'}</p>
	<h2 class="titre">{c.titre}</h2>
	<Ornement nom="fleuron" />
	<p class="quete">{c.quete}</p>
	<p class="date petit">{c.debut && c.debut !== c.date ? `du ${dateFr(c.debut)} au ${dateFr(c.date)}` : dateFr(c.date)}</p>

	{#if verset}
		<blockquote>
			<p class="la" lang="la">{verset.la}</p>
			<p class="fr">{verset.fr}</p>
			<cite class="petit">{verset.ref}</cite>
		</blockquote>
	{/if}

	{#if c.promesse}
		<div class="promesse">
			<p class="pc rub">Promesse et grâce</p>
			<p>{c.promesse}</p>
		</div>
	{/if}

	{#if fermer}
		<div class="actions">
			<a class="bouton" href="/prieres/{encodeURIComponent('paroissien:te-deum')}" onclick={fermer}>Te Deum</a>
			<button class="principal" onclick={fermer}>Deo gratias</button>
		</div>
	{/if}
</article>

<style>
	.carte {
		position: relative; text-align: center; padding: var(--hs-e6) var(--hs-e5) var(--hs-e5);
		border: 1px solid var(--hs-or-trait); outline: 1px solid var(--hs-or-trait); outline-offset: 4px;
		background: radial-gradient(ellipse at top, color-mix(in srgb, var(--hs-or) 9%, var(--hs-fond)), var(--hs-fond) 70%);
		max-width: 26rem; margin: 8px auto;
	}
	.coin { position: absolute; color: var(--hs-or); line-height: 0; }
	.coin.hg { top: 6px; left: 6px; } .coin.hd { top: 6px; right: 6px; transform: scaleX(-1); }
	.coin.bg { bottom: 6px; left: 6px; transform: scaleY(-1); } .coin.bd { bottom: 6px; right: 6px; transform: scale(-1, -1); }
	.couronne { width: 64px; color: var(--hs-or-texte); }
	.gemme { fill: var(--hs-rubrique); }
	.etiquette { color: var(--hs-or-texte); letter-spacing: 0.16em; margin: var(--hs-e2) 0 0; font-size: 0.8rem; }
	.titre { font-family: var(--hs-titre); font-weight: 400; font-size: var(--hs-t3); margin: var(--hs-e2) 0; color: var(--hs-encre); text-wrap: balance; }
	.quete { margin: var(--hs-e3) 0 0; font-style: italic; text-wrap: balance; }
	.date { margin: 4px 0 0; color: var(--hs-encre-douce); }
	blockquote { margin: var(--hs-e4) 0 0; padding: var(--hs-e3) 0 0; border-top: var(--hs-cheveu) solid var(--hs-or-trait); }
	blockquote p { margin: 0 0 6px; }
	.la { font-style: italic; color: var(--hs-encre-douce); }
	cite { font-style: normal; color: var(--hs-encre-douce); }
	.promesse { margin-top: var(--hs-e4); padding-top: var(--hs-e3); border-top: var(--hs-cheveu) solid var(--hs-or-trait); text-align: left; }
	.promesse .pc { text-align: center; margin: 0 0 6px; font-size: 0.8rem; }
	.promesse p:last-child { margin: 0; }
	.actions { display: flex; justify-content: center; gap: var(--hs-e3); margin-top: var(--hs-e5); flex-wrap: wrap; }
	.actions .bouton, .actions button { min-height: 40px; }
</style>
