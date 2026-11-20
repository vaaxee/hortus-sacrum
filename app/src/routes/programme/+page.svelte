<script lang="ts">
	import { db, nouvelId } from '#lib/db.ts';
	import Ornement from '#lib/design/Ornement.svelte';
	import { chargerProgramme } from '#lib/programme/charger.ts';
	import type { EntreeProgramme, Moment, Programme, ReglageProgramme } from '#lib/programme/types.ts';
	import type { Texte } from '#lib/types.ts';
	import { vivantSelon } from '#lib/vivant.svelte.ts';

	/**
	 * Régler le programme (remplace « Régler la liste ») : chaque pratique se désactive, se règle en durée, en heures de
	 * rappel et en jours ; on y ajoute ses propres prières. Les réglages vont dans la table « programme » ; le programme
	 * livré n'est jamais modifié, et une correction livrée ne les écrase pas.
	 */
	let programme = $state.raw<Programme | null>(null);
	chargerProgramme().then((p) => (programme = p));
	const reglages = vivantSelon(() => () => db.programme.toArray(), [] as ReglageProgramme[]);
	const textes = vivantSelon(() => () => db.textes.toArray(), [] as Texte[]);
	const parId = $derived(new Map(reglages.v.map((r) => [r.id, r])));

	const MOMENTS: [Moment, string][] = [
		['matin', 'Matin'],
		['journee', 'Au fil du jour'],
		['soir', 'Soir']
	];
	const JOURS = ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'];

	/** Les pratiques réglables : pages et petites pratiques insérées, puis les ajouts personnels. */
	const entrees = $derived.by(() => {
		if (!programme) return [];
		const livrees = programme.entrees.filter((e) => e.page || e.insertions).map((e) => parId.get(e.id)?.entree ?? e);
		const perso = reglages.v.filter((r) => r.entree && !programme!.entrees.some((e) => e.id === r.id)).map((r) => r.entree!);
		return [...livrees, ...perso];
	});
	const momentDe = (e: EntreeProgramme): Moment =>
		e.page?.moment ?? programme?.entrees.find((x) => x.id === e.insertions?.[0]?.hote)?.page?.moment ?? 'journee';
	const ordreDe = (e: EntreeProgramme) => parId.get(e.id)?.ordre ?? e.page?.ordre ?? 0;
	const actif = (e: EntreeProgramme) => parId.get(e.id)?.actif !== false;
	const hote = (e: EntreeProgramme) => {
		const h = e.insertions?.[0]?.hote;
		return h ? (programme?.entrees.find((x) => x.id === h)?.titre ?? '') : '';
	};
	const joursDe = (e: EntreeProgramme): number[] => (parId.get(e.id)?.quand ?? e.quand)?.jours_semaine ?? [0, 1, 2, 3, 4, 5, 6];
	/** Les jours ne se règlent que sur une pratique de chaque jour, ou un ajout personnel. */
	const joursReglables = (e: EntreeProgramme) => e.id.startsWith('perso:') || !e.quand || !!e.quand.jours_semaine;

	async function regler(id: string, patch: Partial<ReglageProgramme>) {
		const r = parId.get(id) ?? { id, modifieLe: '' };
		await db.programme.put({ ...$state.snapshot(r), ...patch, id, modifieLe: new Date().toISOString() } as ReglageProgramme);
	}
	async function basculerJour(e: EntreeProgramme, k: number) {
		const j = new Set(joursDe(e));
		if (j.has(k)) j.delete(k);
		else j.add(k);
		const jours = [...j].sort();
		if (e.id.startsWith('perso:')) {
			const entree = { ...$state.snapshot(e), quand: jours.length === 7 ? undefined : { jours_semaine: jours } } as EntreeProgramme;
			await regler(e.id, { entree });
		} else await regler(e.id, { quand: jours.length === 7 && !e.quand ? undefined : { ...e.quand, jours_semaine: jours } });
	}
	function heures(v: string): string[] {
		return v
			.split(/[,;\s]+/)
			.map((h) => h.trim())
			.filter((h) => /^\d{1,2}:\d{2}$/.test(h))
			.map((h) => h.padStart(5, '0'));
	}
	async function retirer(id: string) {
		await db.programme.delete(id);
	}

	// ajout personnel
	let nouveauTitre = $state('');
	let nouveauMoment = $state<Moment>('journee');
	let nouvellePriere = $state('');
	const titresConnus = $derived(new Map(textes.v.filter((t) => !t.supprimeLe).map((t) => [t.titre, t.id])));
	async function ajouter() {
		const texte = titresConnus.get(nouvellePriere.trim());
		const titre = nouveauTitre.trim() || nouvellePriere.trim();
		if (!titre) return;
		const id = `perso:${nouvelId()}`;
		const entree: EntreeProgramme = {
			id,
			titre,
			revision: 1,
			source: 'ajout personnel',
			page: { moment: nouveauMoment, ordre: 100, sections: texte ? [{ texte }] : [] }
		};
		await regler(id, { entree });
		nouveauTitre = nouvellePriere = '';
	}
</script>

<svelte:head><title>Régler le programme — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<div class="tete-page">
		<p class="etiquette">Aujourd’hui</p>
		<h1>Régler le programme</h1>
		<Ornement nom="fleuron" />
		<p class="petit">
			Chaque pratique est déclarée une seule fois ; les petites prières se disent à l’intérieur d’une autre page. Désactivez, réglez la
			durée, les heures et les jours, ou ajoutez vos prières. <a href="/programme/changements">Ce qui a changé</a>
		</p>
	</div>

	{#each MOMENTS as [m, nom] (m)}
		{@const liste = entrees.filter((e) => momentDe(e) === m).sort((a, b) => ordreDe(a) - ordreDe(b))}
		{#if liste.length}
			<section>
				<h2>{nom}</h2>
				<ul>
					{#each liste as e (e.id)}
						<li class:eteinte={!actif(e)}>
							<label class="actif">
								<input type="checkbox" checked={actif(e)} onchange={(ev) => regler(e.id, { actif: ev.currentTarget.checked })} />
								<span class="nom">{e.titre}</span>
							</label>
							{#if hote(e)}<p class="aide">Dite dans « {hote(e)} »</p>{/if}
							{#if actif(e)}
								<div class="reglages interface">
									{#if e.page}
										<label
											>Durée (min)
											<input
												type="number"
												min="0"
												step="1"
												value={parId.get(e.id)?.duree ?? e.duree ?? ''}
												placeholder="auto"
												onchange={(ev) =>
													regler(e.id, { duree: ev.currentTarget.value === '' ? undefined : Number(ev.currentTarget.value) })}
											/></label
										>
										<label
											>Heures
											<input
												type="text"
												inputmode="numeric"
												value={(parId.get(e.id)?.heures ?? e.page.heures ?? []).join(', ')}
												placeholder="aucune"
												onchange={(ev) => regler(e.id, { heures: heures(ev.currentTarget.value) })}
											/></label
										>
									{/if}
									{#if joursReglables(e)}
										<div class="jours" role="group" aria-label="Jours">
											{#each JOURS as j, k (k)}
												<button class="brut" aria-pressed={joursDe(e).includes(k)} onclick={() => basculerJour(e, k)}>{j}</button>
											{/each}
										</div>
									{/if}
									{#if e.id.startsWith('perso:')}<button class="brut retirer" onclick={() => retirer(e.id)}>Retirer</button>{/if}
								</div>
							{/if}
						</li>
					{/each}
				</ul>
			</section>
		{/if}
	{/each}

	<section class="ajout">
		<h2>Ajouter une prière</h2>
		<label>Prière <input list="prieres-connues" bind:value={nouvellePriere} placeholder="Chercher une prière de la bibliothèque" /></label>
		<datalist id="prieres-connues">
			{#each [...titresConnus.keys()] as t (t)}<option value={t}></option>{/each}
		</datalist>
		<label>Titre de la ligne <input bind:value={nouveauTitre} placeholder="(le titre de la prière)" /></label>
		<label
			>Moment
			<select bind:value={nouveauMoment}>
				{#each MOMENTS as [m, nom] (m)}<option value={m}>{nom}</option>{/each}
			</select></label
		>
		<button onclick={ajouter}>Ajouter</button>
	</section>
</main>

<style>
	section {
		margin-top: var(--hs-e6);
	}
	h2 {
		font-size: var(--hs-t2);
	}
	ul {
		list-style: none;
		padding: 0;
		margin: var(--hs-e3) 0 0;
	}
	li {
		padding: 10px 0;
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
	}
	li.eteinte .nom {
		color: var(--hs-encre-douce);
		text-decoration: line-through;
	}
	.actif {
		display: flex;
		align-items: center;
		gap: 12px;
		min-height: 44px;
	}
	.actif input {
		width: 22px;
		height: 22px;
		flex: none;
	}
	.aide {
		margin: 0 0 0 34px;
	}
	.reglages {
		display: flex;
		flex-wrap: wrap;
		gap: 8px 16px;
		margin: 6px 0 0 34px;
		font-size: var(--hs-t0);
	}
	.reglages label {
		display: grid;
		gap: 2px;
	}
	.reglages input {
		width: 7.5rem;
	}
	.jours {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
	}
	.jours button {
		padding: 4px 6px;
		min-height: 32px;
		border: var(--hs-cheveu) solid var(--hs-filet);
		background: none;
		color: var(--hs-encre-douce);
		font: inherit;
	}
	.jours button[aria-pressed='true'] {
		color: var(--hs-encre);
		border-color: var(--hs-or-trait);
	}
	.retirer {
		color: var(--hs-rubrique);
		background: none;
		border: 0;
		font: inherit;
		text-decoration: underline;
	}
	.ajout {
		display: grid;
		gap: var(--hs-e3);
	}
	.ajout label {
		display: grid;
		gap: 4px;
	}
</style>
