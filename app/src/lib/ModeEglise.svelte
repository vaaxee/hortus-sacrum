<script lang="ts">
	import { eglise } from './apparence.ts';
	import Icone from './design/Icone.svelte';

	/**
	 * Mode église (décision du 22 nov.) : un bouton discret sur les pages de prière (pratique, office). Actif, il pose
	 * <html data-eglise> (grand corps de lecture, barre d'onglets et éléments secondaires masqués : app.css) et garde
	 * l'écran allumé par l'API Screen Wake Lock, reprise quand la page redevient visible. Le verrou est relâché à la
	 * sortie du mode ou de la page ; sans l'API, le mode marche quand même.
	 */
	let verrou: WakeLockSentinel | null = null;
	let voulu = false;

	async function verrouiller() {
		if ((verrou && !verrou.released) || !('wakeLock' in navigator) || document.visibilityState !== 'visible') return;
		try {
			const v = await navigator.wakeLock.request('screen');
			// le mode a pu être coupé pendant la demande
			if (voulu) verrou = v;
			else v.release().catch(() => {});
		} catch {
			// refusé (batterie faible, page en arrière-plan, navigateur) : le texte reste grand, l'écran s'éteindra
		}
	}
	function relacher() {
		const v = verrou;
		verrou = null;
		v?.release().catch(() => {});
	}

	$effect(() => {
		if (!$eglise) return;
		const html = document.documentElement;
		html.dataset.eglise = '';
		voulu = true;
		verrouiller();
		const revoir = () => {
			if (document.visibilityState === 'visible') verrouiller();
		};
		document.addEventListener('visibilitychange', revoir);
		return () => {
			voulu = false;
			delete html.dataset.eglise;
			document.removeEventListener('visibilitychange', revoir);
			relacher();
		};
	});
</script>

<button
	class="icone mode-eglise"
	aria-label="Mode église"
	aria-pressed={$eglise}
	title={$eglise ? 'Quitter le mode église' : 'Mode église : grand texte, écran allumé'}
	onclick={() => eglise.update((v) => !v)}><Icone nom="cierge" taille={22} /></button
>
