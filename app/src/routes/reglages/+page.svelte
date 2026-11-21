<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	/**
	 * Ancienne adresse : les réglages sont maintenant en bas du Profil (REFONTE § 4.1, un seul profil).
	 * La requête et le fragment sont gardés (lien de connexion par courriel, qui revient ici).
	 */
	onMount(() => {
		goto(`/profil${location.search}${location.hash || '#reglages'}`, { replaceState: true });
	});
</script>

<svelte:head><title>Profil — Hortus Sacrum</title></svelte:head>

<main class="page entree">
	<p class="petit">Les réglages sont maintenant dans <a href="/profil#reglages">le Profil</a>.</p>
</main>
