<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import Badge from '#lib/Badge.svelte';
	import {
		creer, db, dupliquer, enregistrer, estModifie, mettreALaCorbeille, nouvelId, restaurerOriginal, sortirDeLaCorbeille,
		supprimerDefinitivement
	} from '#lib/db.ts';
	import Case from '#lib/design/Case.svelte';
	import Icone from '#lib/design/Icone.svelte';
	import Ornement from '#lib/design/Ornement.svelte';
	import FichePratique from '#lib/FichePratique.svelte';
	import { vivant } from '#lib/live.ts';
	import { etat, recommencer, regleEnClair, versIso } from '#lib/pratiques.ts';
	import { basculerFait, marquerFaits } from '#lib/suivi.ts';
	import { SOURCE_VIDE, type Fait, type Pratique, type Texte } from '#lib/types.ts';

	const id = $derived(decodeURIComponent(page.params.id ?? ''));
	const nouvelle = $derived(id === 'nouvelle');
	const pratique = $derived(vivant(() => db.pratiques.get(id), undefined as Pratique | undefined));
	const faits = $derived(vivant(() => db.faits.where('pratiqueId').equals(id).toArray(), [] as Fait[]));
	const textes = vivant(() => db.textes.toArray(), [] as Texte[]);
	const aujourdhui = versIso(new Date());

	const dates = $derived(new Set($faits.map((f) => f.date)));
	const e = $derived($pratique ? etat($pratique, aujourdhui, dates) : undefined);
	const liees = $derived($pratique ? $pratique.textes.map((t) => $textes.find((x) => x.id === t)).filter((x): x is Texte => !!x) : []);

	let edition = $state(false);
	let brouillon: Pratique | undefined = $state();
	let erreur = $state('');
	let aSupprimer = $state(false);

	// création : quatre points de départ courants
	const MODELES: [string, Partial<Pratique>][] = [
		['Neuvaine', { titre: 'Neuvaine', type: 'neuvaine', regle: { genre: 'consecutifs', nombre: 9, jourSemaine: null, debut: aujourdhui } }],
		['Trentain', { titre: 'Trentain de prières', type: 'trentain', regle: { genre: 'consecutifs', nombre: 30, jourSemaine: null, debut: aujourdhui } }],
		['Série de jours comptés', { titre: 'Série', type: 'jours_comptes', regle: { genre: 'consecutifs', nombre: 7, jourSemaine: new Date().getDay(), debut: aujourdhui } }],
		['Consécration', { titre: 'Consécration', type: 'consecration', regle: { genre: 'fixe', mois: new Date().getMonth() + 1, jour: new Date().getDate() } }]
	];
	function partirDe(m: Partial<Pratique>) {
		brouillon = {
			id: nouvelId(), origine: 'personnel', titre: '', type: 'jours_comptes',
			regle: { genre: 'consecutifs', nombre: 9, jourSemaine: null, debut: aujourdhui },
			textes: [], promesses: '', indulgence: '', source: { ...SOURCE_VIDE }, notes: '', active: true,
			creeLe: '', modifieLe: '', ...structuredClone(m)
		};
	}

	function modifier() {
		if (!$pratique) return;
		brouillon = structuredClone($pratique);
		edition = true;
	}
	async function sauver() {
		erreur = '';
		if (!brouillon) return;
		if (!brouillon.titre.trim()) return (erreur = 'Donnez un titre à cette pratique.');
		const b = $state.snapshot(brouillon) as Pratique;
		if (nouvelle) {
			const { creeLe, modifieLe, ...reste } = b;
			await creer<Pratique>('pratiques', reste);
			goto(`/devotions/${encodeURIComponent(b.id)}`, { replaceState: true });
		} else {
			await enregistrer('pratiques', b);
			edition = false;
		}
		brouillon = undefined;
	}
	async function reprendre() {
		if (!$pratique) return;
		await enregistrer('pratiques', { ...$pratique, regle: recommencer($pratique.regle, aujourdhui) });
	}
	async function copier() {
		const c = await dupliquer<Pratique>('pratiques', id);
		if (c) goto(`/devotions/${encodeURIComponent(c.id)}`);
	}
	async function jeter() {
		await mettreALaCorbeille('pratiques', id);
		goto('/devotions');
	}
	async function effacer() {
		await db.faits.where('pratiqueId').equals(id).delete();
		await supprimerDefinitivement('pratiques', id);
		goto('/devotions');
	}
	const jourCourt = (s: string) => new Date(s + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' });
	const TYPES: Record<string, string> = {
		jours_comptes: 'Dévotion à jours comptés', neuvaine: 'Neuvaine', trentain: 'Trentain', consecration: 'Consécration',
		mois: 'Dévotion du mois', jour_semaine: 'Dévotion du jour de la semaine'
	};
</script>

<svelte:head><title>{nouvelle ? 'Ajouter une pratique' : ($pratique?.titre ?? 'Pratique')} — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<a class="retour" href="/devotions"><Icone nom="retour" taille={16} /> Dévotions</a>

	{#if nouvelle || (edition && brouillon)}
		<div class="tete-page"><h1>{nouvelle ? 'Ajouter une pratique' : 'Modifier'}</h1></div>
		{#if nouvelle && !brouillon}
			<p class="petit">De quoi partir ?</p>
			<div class="rangee">
				{#each MODELES as [nom, m]}<button onclick={() => partirDe(m)}>{nom}</button>{/each}
			</div>
		{:else if brouillon}
			<FichePratique bind:pratique={brouillon} />
			{#if erreur}<p class="erreur" role="alert">{erreur}</p>{/if}
			<div class="rangee actions">
				<button class="principal" onclick={sauver}>Enregistrer</button>
				{#if nouvelle}<a class="bouton" href="/devotions">Annuler</a>{:else}<button onclick={() => (edition = false)}>Annuler</button>{/if}
			</div>
			{#if nouvelle}<p class="petit">Cette pratique sera marquée « Ajout personnel ».</p>{/if}
		{/if}
	{:else if !$pratique}
		<p>Cette pratique est introuvable.</p>
	{:else}
		{@const p = $pratique}
		<div class="tete-page">
			<h1>{p.titre}</h1>
			<p class="rangee"><Badge objet={p} /></p>
			<p class="regle"><span class="pc rub">{TYPES[p.type]}</span><br /><em>{regleEnClair(p.regle)}</em></p>
			{#if p.notes}<p class="notes">{p.notes}</p>{/if}
			<Ornement nom="fleuron" />
		</div>

		{#if p.supprimeLe}
			<p class="alerte">Cette pratique est dans la corbeille. <button onclick={() => sortirDeLaCorbeille('pratiques', id)}>La rétablir</button></p>
		{/if}

		{#if e?.manquees.length}
			<div class="alerte epreuve" role="status">
				<p><strong>Série interrompue.</strong> {e.manquees.length} jour{e.manquees.length > 1 ? 's' : ''} sans coche : {e.manquees.map((o) => jourCourt(o.date)).join(', ')}.</p>
				<div class="rangee">
					<button class="principal" onclick={reprendre}>Recommencer aujourd’hui</button>
					<button onclick={() => marquerFaits(id, e.manquees.map((o) => o.date))}>Je les avais faits</button>
				</div>
			</div>
		{/if}

		{#if e?.serie.length}
			<section>
				<div class="tete-section">
					<Ornement nom="grecque" />
					<h2>{e.phase === 'a_venir' ? 'Série à venir' : 'Série en cours'}</h2>
					<p class="petit chiffres-alignes">{e.faites} sur {e.serie.length}</p>
				</div>
				<ul class="reglee jours">
					{#each e.serie as o (o.date)}
						<li class:futur={o.date > aujourdhui} class:auj={o.date === aujourdhui}>
							<Case libelle="{jourCourt(o.date)}, {o.rang} sur {o.total}" bind:cochee={() => dates.has(o.date), () => basculerFait(id, o.date)} />
							<span class="rang pc chiffres-alignes">{o.rang}</span>
							<span class="date">{jourCourt(o.date)}{o.date === aujourdhui ? ', aujourd’hui' : ''}</span>
						</li>
					{/each}
				</ul>
			</section>
		{:else if e?.prochaine}
			<p class="petit prochain">Prochain jour : {jourCourt(e.prochaine.date)}.</p>
		{/if}

		{#if liees.length}
			<section>
				<div class="tete-section"><Ornement nom="grecque" /><h2>Prières</h2></div>
				<ul class="reglee">
					{#each liees as t (t.id)}
						<li><a class="priere-liee" href="/prieres/{encodeURIComponent(t.id)}">{t.titre}</a></li>
					{/each}
				</ul>
			</section>
		{/if}

		{#if p.promesses}
			<section class="texte">
				<h3>Promesses</h3>
				<p>{p.promesses}</p>
			</section>
		{/if}
		{#if p.indulgence}<p class="marge"><span class="cartouche ind">Ind.</span> {p.indulgence}</p>{/if}
		{#if p.source.ouvrage || p.source.edition}
			<p class="marge imprime">{[p.source.ouvrage, p.source.edition, p.source.page && `p. ${p.source.page}`].filter(Boolean).join(', ')}</p>
		{/if}

		<div class="rangee actions">
			<button class="principal" onclick={modifier}>Modifier</button>
			<button onclick={copier}>Dupliquer</button>
			<button onclick={() => enregistrer('pratiques', { ...p, active: !p.active })}>{p.active ? 'Masquer' : 'Afficher'}</button>
			{#if estModifie(p)}<button onclick={() => restaurerOriginal('pratiques', id)}>Restaurer l’original</button>{/if}
			{#if !p.supprimeLe}
				<button class="danger" onclick={jeter}>Mettre à la corbeille</button>
			{:else if aSupprimer}
				<button class="danger" onclick={effacer}>Confirmer la suppression</button>
			{:else}
				<button class="discret" onclick={() => (aSupprimer = true)}>Supprimer pour de bon</button>
			{/if}
		</div>
	{/if}
</main>

<style>
	.tete-page :global(.filet) { max-width: 16rem; }
	.regle { font-size: 1.0625rem; line-height: 1.4; }
	.notes { font-style: italic; max-width: 30rem; }
	.alerte { color: var(--hs-rubrique); padding: var(--hs-e4); margin: 0 0 var(--hs-e4); }
	.alerte p { margin: 0 0 var(--hs-e3); color: var(--hs-encre); }
	.alerte strong { color: var(--hs-rubrique); font-weight: 500; font-variant-caps: all-small-caps; letter-spacing: var(--hs-chasse-petites-cap); }
	.tete-section .petit { margin: -6px 0 0; }
	.jours li { gap: 14px; min-height: 48px; }
	.jours li.futur { opacity: 0.55; }
	.jours li.auj .date { color: var(--hs-lapis); }
	.rang { width: 1.6rem; text-align: right; color: var(--hs-encre-douce); }
	.priere-liee { flex: 1; padding: 12px 0; text-decoration: none; color: var(--hs-encre); }
	.prochain { text-align: center; }
	.texte { margin-top: var(--hs-e6); }
	.texte h3 { color: var(--hs-rubrique); text-align: center; margin-bottom: var(--hs-e3); }
	.texte p { text-align: justify; hyphens: auto; white-space: pre-line; }
	.marge { margin: var(--hs-e5) 0 0; font-size: 1rem; color: var(--hs-encre-douce); line-height: 1.45; }
	.actions { margin-top: var(--hs-e6); }
</style>
