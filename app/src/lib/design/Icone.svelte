<script lang="ts">
	/** HORTUS SACRUM — icônes au trait fin (1,5 px), géométriques, d'après des symboles chrétiens. */
	type Nom =
		| 'aujourdhui'
		| 'calendrier'
		| 'prieres'
		| 'lecture'
		| 'devotions'
		| 'profil'
		| 'chevron'
		| 'retour'
		| 'jour'
		| 'nuit'
		| 'etoile'
		| 'plume'
		| 'source';

	let { nom, taille = 24 }: { nom: Nom; taille?: number } = $props();
</script>

<svg
	width={taille}
	height={taille}
	viewBox="0 0 24 24"
	fill="none"
	stroke="currentColor"
	stroke-width="1.5"
	stroke-linecap="round"
	stroke-linejoin="round"
	aria-hidden="true"
>
	{#if nom === 'aujourdhui'}
		<!-- soleil levant sur l'horizon : le jour présent -->
		<path d="M3 18.500h18" /><path d="M6.500 18.500a5.500 5.500 0 0 1 11 0" />
		<path d="M12 6.500V4M5.300 10.300L3.600 8.600M18.700 10.300l1.700-1.700" />
	{:else if nom === 'calendrier'}
		<!-- page d'ordo : une arche au-dessus des lignes -->
		<path d="M5 21V10a7 7 0 0 1 14 0v11z" /><path d="M8.500 13h7M8.500 17h7" />
	{:else if nom === 'prieres'}
		<!-- livre ouvert -->
		<path d="M12 6.500C10 5 7 4.500 3.500 5v13.500c3.500-.500 6.500 0 8.500 1.500c2-1.500 5-2 8.500-1.500V5C17 4.500 14 5 12 6.500z" />
		<path d="M12 6.500V20" />
	{:else if nom === 'lecture'}
		<!-- lutrin : livre ouvert posé sur son pied -->
		<path d="M4 8.500l8 3l8-3v4l-8 3l-8-3z" /><path d="M12 11.500v4" /><path d="M12 15.500V21M8.500 21h7" />
	{:else if nom === 'devotions'}
		<!-- cœur surmonté d'une croix -->
		<path d="M12 21C6.500 17.200 4 14 4 11.200A4 4 0 0 1 12 9.500a4 4 0 0 1 8 1.700c0 2.800-2.500 6-8 9.800z" />
		<path d="M12 7V2.500M10 4.300h4" />
	{:else if nom === 'profil'}
		<!-- lis -->
		<path d="M12 3c2.200 2.800 2.200 6.500 0 10.500c-2.200-4-2.200-7.700 0-10.500z" />
		<path d="M10.700 13C8.300 11.700 6 9.500 4 9c-.500 3 1.300 5.500 5 6" />
		<path d="M13.300 13c2.400-1.300 4.700-3.500 6.700-4c.500 3-1.300 5.500-5 6" />
		<path d="M8 15h8M12 15v6" />
	{:else if nom === 'chevron'}
		<path d="M9 6l6 6l-6 6" />
	{:else if nom === 'retour'}
		<path d="M15 6l-6 6l6 6" />
	{:else if nom === 'jour'}
		<circle cx="12" cy="12" r="4" /><path
			d="M12 3v2.500M12 18.500V21M3 12h2.500M18.500 12H21M5.600 5.600l1.800 1.800M16.600 16.600l1.800 1.800M5.600 18.400l1.800-1.800M16.600 7.400l1.800-1.800"
		/>
	{:else if nom === 'nuit'}
		<path d="M19.500 14.500A8 8 0 0 1 9.500 4.500a8 8 0 1 0 10 10z" />
	{:else if nom === 'etoile'}
		<path d="M12 3.500l2.300 5.600l6 .500l-4.600 3.900l1.500 5.900L12 16.200l-5.200 3.200l1.500-5.900L3.700 9.600l6-.500z" />
	{:else if nom === 'plume'}
		<path d="M19.500 4.500c-7 0-11.500 4-12.500 12l-2 3M7 16.500c4.500 0 8-1.500 10-5" />
	{:else if nom === 'source'}
		<path d="M6 4.500h9l3 3V19.500H6z" /><path d="M9 11h6M9 14.500h6" />
	{/if}
</svg>
