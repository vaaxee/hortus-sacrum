<script lang="ts">
	import Badge from '#lib/Badge.svelte';
	import { db, exporter, importer, sortirDeLaCorbeille, supprimerDefinitivement, type Sauvegarde } from '#lib/db.ts';
	import { vivant } from '#lib/live.ts';
	import type { Texte } from '#lib/types.ts';

	const corbeille = vivant(async () => (await db.textes.toArray()).filter((t) => t.supprimeLe), [] as Texte[]);
	const compte = vivant(async () => ({ textes: await db.textes.count(), versions: await db.versions.count() }), {
		textes: 0,
		versions: 0
	});

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

<svelte:head><title>Réglages — Hebdomada</title></svelte:head>

<main class="page">
	<h1>Réglages</h1>

	<section>
		<h2>Sauvegarde</h2>
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
		<h2>Corbeille</h2>
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
</main>

<style>
	section { margin-top: 1.4rem; }
	h2 { margin-bottom: 0.4rem; }
	.fichier { position: relative; overflow: hidden; }
	.fichier input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
	.choix { margin-top: 0.8rem; padding: 0.7rem 0.9rem; border: 1px solid var(--filet); border-radius: 0.5rem; background: var(--carte); }
	.choix p { margin: 0 0 0.5rem; }
	.ligne { padding: 0.5rem 0; border-bottom: 1px solid var(--filet); }
</style>
