<script lang="ts">
	/**
	 * Réglages techniques (compte, rappels, apparence, sauvegarde, corbeille), affichés en bas du Profil
	 * (REFONTE § 4.1 : un seul profil). L’ancienne adresse /reglages mène ici.
	 */
	import { direction, theme, type Direction, type Theme } from '#lib/apparence.ts';
	import Badge from '#lib/Badge.svelte';
	import { deconnecter, envoyerLien, etatSync, synchroniser, verifierCode } from '#lib/sync.ts';
	import { db, exporter, importer, sortirDeLaCorbeille, supprimerDefinitivement, type Sauvegarde } from '#lib/db.ts';
	import { vivant } from '#lib/live.ts';
	import type { Texte } from '#lib/types.ts';
	import { abonner, desabonner, ecrireReglages, essai, lireReglages, planifier, type ReglagesRappels } from '#lib/rappels.ts';

	const corbeille = vivant(async () => (await db.textes.toArray()).filter((t) => t.supprimeLe), [] as Texte[]);
	const compte = vivant(async () => ({ textes: await db.textes.count(), versions: await db.versions.count() }), {
		textes: 0,
		versions: 0
	});

	let imageAccueil = $state('tableau');
	try {
		imageAccueil = localStorage.getItem('accueil-image') || 'tableau';
	} catch {
		/* stockage indisponible */
	}
	const themes: [Theme, string][] = [
		['auto', 'Selon l’appareil'],
		['jour', 'Jour'],
		['nuit', 'Nuit']
	];
	const directions: [Direction, string][] = [
		['latine', 'Latine'],
		['grecque', 'Grecque, outremer et cobalt']
	];
	let courriel = $state('');
	let lienEnvoye = $state('');
	let erreurCompte = $state('');
	async function demanderLien() {
		erreurCompte = '';
		if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(courriel.trim())) return (erreurCompte = 'Cette adresse de courriel n’est pas valide.');
		const e = await envoyerLien(courriel);
		if (e) erreurCompte = `Le lien n’a pas pu être envoyé : ${e}`;
		else lienEnvoye = courriel.trim();
	}
	// rappels
	let reglages = $state<ReglagesRappels | undefined>();
	let messageRappels = $state('');
	lireReglages().then((r) => (reglages = r));
	const iphoneSansInstall =
		typeof navigator !== 'undefined' && /iPhone|iPad/.test(navigator.userAgent) && !window.matchMedia('(display-mode: standalone)').matches;
	async function sauverRappels() {
		if (!reglages) return;
		await ecrireReglages($state.snapshot(reglages));
		try {
			const n = await planifier();
			messageRappels = reglages.actif ? `${n} rappels préparés pour les 14 jours qui viennent.` : '';
		} catch (e) {
			messageRappels = `Les rappels n’ont pas pu être préparés : ${(e as Error).message}`;
		}
	}
	async function basculerRappels(oui: boolean) {
		if (!reglages) return;
		messageRappels = '';
		if (oui) {
			const err = await abonner();
			if (err) return (messageRappels = err);
		} else {
			await desabonner();
		}
		reglages.actif = oui;
		await sauverRappels();
	}
	async function essayer() {
		const err = await essai();
		messageRappels = err ? `L’essai a échoué : ${err}` : 'Rappel d’essai envoyé : il arrive dans la minute.';
	}

	let code = $state('');
	async function validerCode() {
		erreurCompte = '';
		const e = await verifierCode(lienEnvoye, code);
		if (e) erreurCompte = `Ce code n’a pas été accepté : ${e}`;
		else {
			lienEnvoye = '';
			code = '';
		}
	}

	const heure = (iso: string) => new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
	let message = $state('');
	let attente: Sauvegarde | undefined = $state();
	let aSupprimer: string | undefined = $state();

	async function sauvegarder() {
		const s = await exporter();
		const url = URL.createObjectURL(new Blob([JSON.stringify(s, null, 1)], { type: 'application/json' }));
		const a = document.createElement('a');
		a.href = url;
		a.download = `hebdomada-${s.date.slice(0, 10)}.json`;
		a.click();
		URL.revokeObjectURL(url);
		message = 'Sauvegarde téléchargée.';
	}

	async function choisir(e: Event) {
		const f = (e.currentTarget as HTMLInputElement).files?.[0];
		message = '';
		attente = undefined;
		if (!f) return;
		try {
			const s = JSON.parse(await f.text()) as Sauvegarde;
			if (s.format !== 'hebdomada') throw new Error();
			attente = s;
		} catch {
			message = 'Ce fichier n’est pas une sauvegarde Hebdomada.';
		}
	}

	async function lancer(mode: 'remplacer' | 'fusionner') {
		if (!attente) return;
		const n = await importer(attente, mode);
		message = `Import terminé : ${n} élément${n > 1 ? 's' : ''} ${mode === 'remplacer' ? 'restaurés' : 'ajoutés ou mis à jour'}.`;
		attente = undefined;
	}
</script>

<div class="reglages">
	<section>
		<h3>Compte</h3>
		{#if $etatSync.genre === 'deconnecte'}
			<p class="petit">
				Connectez-vous pour retrouver vos prières, votre liste et vos dévotions sur le téléphone et sur l’ordinateur. Sans compte, tout
				reste sur cet appareil.
			</p>
			{#if lienEnvoye}
				<p class="epreuve envoye">
					Un courriel a été envoyé à <strong>{lienEnvoye}</strong>. Dans l’app installée sur l’écran d’accueil, saisissez ici le
					<strong>code</strong> qu’il contient (le lien, lui, s’ouvre dans le navigateur).
				</p>
				<label
					><span>Code reçu</span><input
						type="text"
						inputmode="numeric"
						autocomplete="one-time-code"
						maxlength="10"
						bind:value={code}
					/></label
				>
				<div class="rangee">
					<button class="principal" disabled={code.replace(/\s/g, '').length < 6} onclick={validerCode}>Se connecter</button>
					<button
						class="discret"
						onclick={() => {
							lienEnvoye = '';
							code = '';
						}}>Changer d’adresse</button
					>
				</div>
			{:else}
				<label><span>Adresse de courriel</span><input type="text" inputmode="email" autocomplete="email" bind:value={courriel} /></label>
				<div class="rangee"><button class="principal" onclick={demanderLien}>Recevoir un lien de connexion</button></div>
			{/if}
			{#if erreurCompte}<p class="erreur" role="alert">{erreurCompte}</p>{/if}
		{:else}
			<p>Connecté : <strong>{$etatSync.courriel}</strong></p>
			<p class="petit" role="status">
				{#if $etatSync.genre === 'en_cours'}Synchronisation en cours…
				{:else if $etatSync.genre === 'a_jour'}À jour, synchronisé à {heure($etatSync.quand)}.
				{:else if $etatSync.genre === 'erreur'}La synchronisation a échoué : {$etatSync.message}. Vos données restent sur cet appareil ;
					réessayez quand la connexion revient.{/if}
			</p>
			<div class="rangee">
				<button onclick={() => synchroniser()}>Synchroniser maintenant</button>
				<button class="discret" onclick={deconnecter}>Se déconnecter</button>
			</div>
		{/if}
	</section>

	<hr class="filet" />

	<section>
		<h3>Rappels</h3>
		{#if reglages}
			<p class="petit">
				Le matin, le soir, la veille des fêtes, des jeûnes et des neuvaines, et aux heures fixes des dévotions (réglées dans « Liste du jour
				»). Les rappels arrivent même app fermée ; ils sont préparés pour les 14 jours qui viennent, à chaque ouverture de l’app.
			</p>
			{#if iphoneSansInstall}
				<p class="epreuve">
					Sur iPhone, les notifications ne marchent que depuis l’app installée : dans Safari, touchez le bouton Partager, puis « Sur l’écran
					d’accueil ». Ouvrez ensuite Hortus Sacrum depuis l’écran d’accueil et revenez ici.
				</p>
			{/if}
			<label class="case"
				><input type="checkbox" checked={reglages.actif} onchange={(e) => basculerRappels(e.currentTarget.checked)} /> Recevoir les rappels sur
				cet appareil</label
			>
			{#if reglages.actif}
				<div class="rangee heures">
					<label><span>Matin</span><input type="time" bind:value={reglages.matin} onchange={sauverRappels} /></label>
					<label><span>Soir</span><input type="time" bind:value={reglages.soir} onchange={sauverRappels} /></label>
					<label><span>Veille</span><input type="time" bind:value={reglages.veille} onchange={sauverRappels} /></label>
				</div>
				<p class="aide">Effacer une heure supprime ce rappel.</p>
				<label class="case"
					><input type="checkbox" bind:checked={reglages.heuresFixes} onchange={sauverRappels} /> Heures fixes des dévotions (Angélus, agonisants,
					15 h le vendredi…)</label
				>
				{#if reglages.heuresFixes}
					<label
						><span>Pour les dévotions</span>
						<select bind:value={reglages.rangMini} onchange={sauverRappels}>
							<option value="supererogatoria">de tous les rangs</option>
							<option value="pia">Præcipua et Pia</option>
							<option value="praecipua">Præcipua seulement</option>
						</select>
					</label>
				{/if}
				<label class="case"
					><input type="checkbox" bind:checked={reglages.veilleFetes} onchange={sauverRappels} /> La veille des fêtes de 1re et 2e classe</label
				>
				<label class="case"
					><input type="checkbox" bind:checked={reglages.veilleJeune} onchange={sauverRappels} /> La veille des jours de jeûne et d’abstinence</label
				>
				<label class="case"
					><input type="checkbox" bind:checked={reglages.premiersVendrediSamedi} onchange={sauverRappels} /> La veille des premiers vendredis
					et samedis</label
				>
				<label class="case"
					><input type="checkbox" bind:checked={reglages.veillePratiques} onchange={sauverRappels} /> La veille du début d’une neuvaine ou d’une
					série</label
				>
				<label class="case"
					><input type="checkbox" bind:checked={reglages.fetesPerso} onchange={sauverRappels} /> Mes fêtes et anniversaires (la veille et le jour)</label
				>
				<div class="rangee"><button onclick={essayer}>Envoyer un rappel d’essai</button></div>
			{/if}
			{#if messageRappels}<p class="petit" role="status">{messageRappels}</p>{/if}
		{/if}
	</section>

	<hr class="filet" />

	<nav class="raccourcis" aria-label="Réglages">
		<a href="/fetes">Fêtes, saints et anniversaires</a>
		<a href="/liste">Liste du jour</a>
		<a href="/devotions">Pratiques et dévotions</a>
	</nav>

	<hr class="filet" />

	<section>
		<h3>Apparence</h3>
		<label
			><span>Image de l’écran d’accueil</span>
			<select
				value={imageAccueil}
				onchange={(ev) => {
					imageAccueil = ev.currentTarget.value;
					try {
						localStorage.setItem('accueil-image', imageAccueil);
					} catch {
						/* */
					}
				}}
			>
				<option value="tableau">Le tableau de Velázquez</option>
				<option value="gravure">Sa gravure à l’or</option>
			</select>
		</label>
		<p class="aide">Thème</p>
		<div class="rangee" role="group" aria-label="Thème">
			{#each themes as [v, nom] (v)}
				<button aria-pressed={$theme === v} onclick={() => theme.set(v)}>{nom}</button>
			{/each}
		</div>
		<p class="aide">Direction artistique</p>
		<div class="rangee" role="group" aria-label="Direction artistique">
			{#each directions as [v, nom] (v)}
				<button aria-pressed={$direction === v} onclick={() => direction.set(v)}>{nom}</button>
			{/each}
		</div>
	</section>

	<hr class="filet" />

	<section>
		<h3>Sauvegarde</h3>
		<p class="petit">{$compte.textes} prières, {$compte.versions} versions en historique. Tout est gardé sur cet appareil.</p>
		<div class="rangee">
			<button class="principal" onclick={sauvegarder}>Exporter tout (JSON)</button>
			<label class="bouton fichier">
				Importer une sauvegarde
				<input type="file" accept="application/json,.json" onchange={choisir} />
			</label>
		</div>
		{#if attente}
			<div class="choix">
				<p>Sauvegarde du {new Date(attente.date).toLocaleDateString('fr-FR', { dateStyle: 'long' })}. Que faire ?</p>
				<div class="rangee">
					<button onclick={() => lancer('fusionner')}>Fusionner (garde le plus récent)</button>
					<button onclick={() => lancer('remplacer')}>Tout remplacer</button>
					<button class="discret" onclick={() => (attente = undefined)}>Annuler</button>
				</div>
				<p class="petit">« Tout remplacer » efface ce qui est sur cet appareil et le remplace par la sauvegarde.</p>
			</div>
		{/if}
		{#if message}<p role="status">{message}</p>{/if}
	</section>

	<hr class="filet" />

	<section>
		<h3>Corbeille</h3>
		{#each $corbeille as t (t.id)}
			<div class="rangee ligne">
				<a href="/prieres/{encodeURIComponent(t.id)}">{t.titre}</a>
				<Badge objet={t} />
				<span class="espace"></span>
				<button onclick={() => sortirDeLaCorbeille('textes', t.id)}>Rétablir</button>
				{#if aSupprimer === t.id}
					<button class="principal" onclick={() => supprimerDefinitivement('textes', t.id)}>Confirmer la suppression</button>
				{:else}
					<button class="discret" onclick={() => (aSupprimer = t.id)}>Supprimer pour de bon</button>
				{/if}
			</div>
		{:else}
			<p class="petit">La corbeille est vide.</p>
		{/each}
	</section>
</div>

<style>
	section {
		margin-top: 1.4rem;
	}
	h3 {
		margin-bottom: var(--hs-e3);
		font-size: var(--hs-t2);
	}
	.envoye {
		font-size: 1rem;
		margin: 0 0 var(--hs-e2);
	}
	.raccourcis {
		display: grid;
	}
	.raccourcis a {
		padding: 12px 0;
		border-bottom: var(--hs-cheveu) solid var(--hs-filet);
		text-decoration: none;
		color: var(--hs-encre);
	}
	.aide {
		margin: var(--hs-e4) 0 var(--hs-e2);
	}
	.fichier {
		position: relative;
		overflow: hidden;
	}
	.fichier input {
		position: absolute;
		inset: 0;
		opacity: 0;
		cursor: pointer;
	}
	.choix {
		margin-top: 0.8rem;
		padding: 0.7rem 0.9rem;
		border: 1px solid var(--hs-filet);
		border-radius: 0;
		background: var(--hs-surface);
	}
	.choix p {
		margin: 0 0 0.5rem;
	}
	.ligne {
		padding: 0.5rem 0;
		border-bottom: 1px solid var(--hs-filet);
	}
</style>
