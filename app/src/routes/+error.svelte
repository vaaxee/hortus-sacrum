<script lang="ts">
	import { page } from '$app/state';

	/**
	 * Page d'erreur : au lieu d'un « Internal Error » muet, le message réel, pour que l'utilisateur puisse le signaler.
	 */
</script>

<section class="page erreur" role="alert">
	<h1>Une erreur est survenue</h1>
	<p>La page « {page.url.pathname} » n’a pas pu s’afficher.</p>
	<p class="detail"><strong>{page.status}</strong> — {page.error?.message ?? 'erreur inconnue'}</p>
	<p>Une capture de cet écran suffit à la signaler. Vos données ne sont pas touchées.</p>
	<p><a href="/">Revenir à aujourd’hui</a></p>
</section>

<style>
	.erreur {
		padding: var(--hs-e5, 1.5rem) var(--hs-e4, 1rem);
		display: grid;
		gap: var(--hs-e3, 0.75rem);
	}
	.detail {
		font-family: ui-monospace, monospace;
		font-size: 0.85rem;
		word-break: break-word;
	}
</style>
