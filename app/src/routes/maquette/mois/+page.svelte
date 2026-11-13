<script lang="ts">
	import { page } from '$app/state';
	import { MOIS_DEVOTION, moisDu, NOMS_MOIS, RANG, teinte, type Jour } from '#lib/calendrier.ts';
	import Arche from '#lib/design/Arche.svelte';
	import Ornement from '#lib/design/Ornement.svelte';

	const cle = $derived(page.url.searchParams.get('m') ?? '2026-12');
	const an = $derived(Number(cle.slice(0, 4)));
	const mois = $derived(Number(cle.slice(5, 7)));
	let jours: Jour[] = $state([]);
	$effect(() => {
		moisDu(an, mois).then((j) => (jours = j));
	});

	const GRANDS = ['1re cl.', '2e cl.', 'dim. 1re cl.', 'dim. 2e cl.', 'dim.', 'vigile 1re cl.'];
	const principaux = $derived(jours.filter((j) => GRANDS.includes(j.rang)));
	/** En exergue : l'Introït de la première fête de 1re classe du mois. */
	const exergue = $derived(jours.find((j) => j.rang === '1re cl.' && j.introit) ?? jours.find((j) => j.introit));
	const antienne = (l: string[] | null | undefined) => l?.find((x) => x.startsWith('v. '))?.slice(3) ?? '';
	const reference = (l: string[] | null | undefined) => l?.find((x) => x.startsWith('!'))?.slice(1).replace(/\.$/, '') ?? '';
	const jeunes = $derived(jours.filter((j) => j.jeune_abstinence && j.jeune_abstinence.code !== 'A'));
	const ABR = ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'];
	const jourSem = (j: Jour) => ABR[new Date(j.date + 'T12:00:00').getDay()];
	const ROMAIN = (n: number) => {
		const t: [number, string][] = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'], [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'], [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']];
		let s = '';
		for (const [v, c] of t) while (n >= v) { s += c; n -= v; }
		return s;
	};
</script>

<svelte:head><title>{NOMS_MOIS[mois]} {an} — Hortus Sacrum</title></svelte:head>

{#if jours.length}
	<div class="bande-mois"><Ornement nom="mosaique" /></div>
	<main class="ecran entree">
		<header>
			<h1 class="mois">{NOMS_MOIS[mois]}</h1>
			<p class="an pc chiffres-alignes">Anno Domini {ROMAIN(an)}</p>
			<Ornement nom="laurier" />
		</header>

		<Arche solennel>
			<span class="lis"><Ornement nom="lis" taille={30} /></span>
			<h2 class="devotion">{MOIS_DEVOTION[mois].nom}</h2>
			<p class="ref imprime">{MOIS_DEVOTION[mois].reference}</p>
		</Arche>

		{#if exergue?.introit}
			<blockquote class="exergue">
				<p class="la" lang="la">{antienne(exergue.introit.la)}</p>
				{#if exergue.introit.fr}<p class="fr">{antienne(exergue.introit.fr)}</p>{/if}
				<footer class="imprime">
					<span class="rub">Introït</span> — {exergue.office}, {Number(exergue.date.slice(8))} {NOMS_MOIS[mois].toLowerCase()}
					{#if reference(exergue.introit.la)}<span class="cit">({reference(exergue.introit.la)})</span>{/if}
				</footer>
			</blockquote>
		{/if}

		<section aria-label="Dimanches et fêtes du mois">
			<div class="tete">
				<Ornement nom="grecque" />
				<h2>Dimanches et fêtes</h2>
			</div>
			<table class="ordo">
				<tbody>
					{#each principaux as j}
						<tr class:fete={j.est_fete_sanctorale || j.rang.startsWith('dim')}>
							<td class="p"><span class="pastille" style="--pastille: {teinte(j)}" title={j.couleur}></span></td>
							<td class="d pc chiffres-alignes">{Number(j.date.slice(8))} <span>{jourSem(j)}</span></td>
							<td class="o">
								{j.office}
								<span class="r pc">{RANG[j.rang] ?? j.rang}</span>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</section>

		{#if jeunes.length}
			<p class="jeunes">
				<span class="pc rub">Jeûne</span>
				{jeunes.map((j) => `${Number(j.date.slice(8))} (${jourSem(j)})`).join(', ')}.
				<span class="note">Abstinence tous les vendredis.</span>
			</p>
		{/if}

		<div class="pied">
			<Ornement nom="perles" />
			<span class="cherubin"><Ornement nom="cherubin" taille={34} /></span>
		</div>
	</main>
{/if}

<style>
	/* en DA grecque, la bande de mosaïque est déjà en tête de tous les écrans */
	:global(:root[data-da='grecque']) .bande-mois { display: none; }
	.ecran { max-width: var(--hs-colonne); margin: 0 auto; padding: var(--hs-e7) var(--hs-marge-mobile) 0; }
	header { text-align: center; display: grid; gap: var(--hs-e2); margin-bottom: var(--hs-e6); }
	header p { margin: 0; }
	/* Almendra : seul caractère d'accent de l'écran, pour le nom du mois */
	.mois {
		font-family: var(--hs-accent); font-weight: 400; text-transform: none; letter-spacing: 0.01em;
		font-size: clamp(var(--hs-t5), 15vw, 4.75rem); line-height: 1.05; color: var(--hs-rubrique);
	}
	.an { color: var(--hs-encre-douce); font-size: 1.0625rem; margin-bottom: var(--hs-e4) !important; }
	.lis { color: var(--hs-or); line-height: 0; }
	.devotion { font-style: normal; text-transform: uppercase; letter-spacing: var(--hs-chasse-capitales); font-size: var(--hs-t2); line-height: 1.25; max-width: 16rem; }
	.ref { margin: 0; font-style: italic; font-size: 1rem; color: var(--hs-encre-douce); max-width: 17rem; line-height: 1.35; text-wrap: balance; }

	.exergue { margin: var(--hs-e7) auto 0; max-width: 30rem; text-align: center; padding: 0; }
	.exergue p { margin: 0; text-wrap: balance; }
	.exergue .la { font-family: var(--hs-titre); font-style: italic; font-weight: 500; font-size: var(--hs-t2); line-height: 1.3; }
	.exergue .fr { margin-top: var(--hs-e3); font-size: 1.0625rem; color: var(--hs-encre-douce); }
	.exergue footer { margin-top: var(--hs-e3); font-size: 0.9375rem; color: var(--hs-encre-douce); }
	.cit { white-space: nowrap; }

	.tete { margin-top: var(--hs-e7); text-align: center; display: grid; gap: var(--hs-e3); }
	.tete h2 { font-size: var(--hs-t2); }

	/* réglé comme un ordo ancien : filets fins, pas de bandes, dates en petites capitales */
	.ordo { width: 100%; border-collapse: collapse; margin-top: var(--hs-e4); }
	.ordo td { padding: 9px 0; border-bottom: var(--hs-cheveu) solid var(--hs-filet); vertical-align: baseline; }
	.ordo tr:first-child td { border-top: var(--hs-cheveu) solid var(--hs-filet); }
	.p { width: 22px; }
	.d { width: 4.6rem; white-space: nowrap; font-size: 1.125rem; }
	.d span { color: var(--hs-encre-douce); }
	.o { line-height: 1.3; }
	.r { display: block; font-size: 0.9375rem; color: var(--hs-encre-douce); }
	tr.fete .o { color: var(--hs-rubrique); }
	tr.fete .r { color: var(--hs-encre-douce); }

	.jeunes { margin: var(--hs-e5) 0 0; font-size: 1.0625rem; text-align: center; text-wrap: balance; }
	.note { color: var(--hs-encre-douce); font-style: italic; }
	.pied { margin-top: var(--hs-e7); display: grid; justify-items: center; gap: var(--hs-e5); }
	.cherubin { color: var(--hs-or); }
</style>
