<script lang="ts">
	/**
	 * HORTUS SACRUM — icônes au trait fin, d'après des symboles chrétiens, dessinées comme une gravure :
	 * le trait principal à 1,5 px, les tailles et les hachures (classe « fin ») à 0,75 px.
	 */
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
		| 'source'
		| 'matin'
		| 'midi'
		| 'soir';

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
		<g class="fin"><path d="M9 18.500a3 3 0 0 1 6 0M8.300 7.600l-.7-1.300M15.700 7.600l.7-1.300M6 21h12" /></g>
	{:else if nom === 'calendrier'}
		<!-- page d'ordo : une arche, une croisette à la clef, les lignes des jours -->
		<path d="M5 21V10a7 7 0 0 1 14 0v11z" />
		<g class="fin"><path d="M7 21V10.200a5 5 0 0 1 10 0V21M9.300 14h5.400M9.300 17.300h5.400M12 6.600v2.600M10.800 7.700h2.400" /></g>
	{:else if nom === 'prieres'}
		<!-- livre ouvert, une croisette sur la page, le signet qui pend -->
		<path d="M12 6.500C10 5 7 4.500 3.500 5v13.500c3.500-.500 6.500 0 8.500 1.500c2-1.500 5-2 8.500-1.500V5C17 4.500 14 5 12 6.500z" />
		<path d="M12 6.500V20" />
		<g class="fin"
			><path
				d="M7.700 8.800v4.400M6.200 10.200h3M14.300 9.300c1.400-.5 2.800-.6 4.200-.4M14.300 12c1.400-.5 2.800-.6 4.200-.4M16 18.700v3l.9-.8l.9.8v-3"
			/></g
		>
	{:else if nom === 'lecture'}
		<!-- lutrin : livre ouvert posé sur son pied, le signet -->
		<path
			d="M3.500 9.500c3-.900 5.800-.600 8.500 1c2.700-1.600 5.500-1.900 8.500-1v4.700c-3-.900-5.800-.600-8.500 1c-2.700-1.600-5.500-1.900-8.500-1z"
		/>
		<path d="M12 15.200V21M8.500 21h7" />
		<g class="fin"
			><path
				d="M12 10.500v4.700M5.700 11.300c1.700-.300 3.200-.100 4.600.5M13.700 11.800c1.400-.600 2.900-.800 4.600-.5M10.300 18h3.400M15 14.500v3.200l.8-.7l.8.7v-3.600"
			/></g
		>
	{:else if nom === 'devotions'}
		<!-- Sacré-Cœur : la croix, les flammes, la couronne d'épines -->
		<path d="M12 21C6.500 17.200 4 14 4 11.200A4 4 0 0 1 12 9.500a4 4 0 0 1 8 1.700c0 2.800-2.500 6-8 9.800z" />
		<path d="M12 7V2.500M10.200 4.200h3.600" />
		<g class="fin"
			><path
				d="M9.300 7.700c-.700-1-.400-2 .400-2.600M14.700 7.700c.700-1 .400-2-.400-2.600M5.800 13.200c4 1.500 8.400 1.500 12.400 0M8.300 13.300l-.400 1.200M11 13.900l.1-1.200M13.600 13.800l.4 1.100M16 13.300l.5-1"
			/></g
		>
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
	{:else if nom === 'matin'}
		<!-- soleil levant : laudes et prime -->
		<path d="M2.500 17h19" /><path d="M7 17a5 5 0 0 1 10 0" />
		<path d="M12 9.500V6.500M7.200 11.700L5.400 10M16.800 11.700l1.800-1.700" />
		<g class="fin"><path d="M4.800 14.300l-2-.4M19.200 14.300l2-.4M9.400 8.700l-.6-1.400M14.600 8.700l.6-1.400M6 19.500h12M9 21.500h6" /></g
		>
	{:else if nom === 'midi'}
		<!-- soleil au plus haut : le cours du jour -->
		<circle cx="12" cy="12" r="4" />
		<path
			d="M12 2.500v3M12 18.500v3M2.500 12h3M18.500 12h3M5.300 5.300l2.100 2.100M16.600 16.600l2.100 2.100M5.300 18.700l2.100-2.100M16.600 7.400l2.100-2.100"
		/>
		<g class="fin"
			><circle cx="12" cy="12" r="1.600" /><path
				d="M8.300 3.300l.7 1.700M15.700 3.300l-.7 1.700M3.300 8.300l1.700.7M3.300 15.700l1.700-.7M20.700 8.300l-1.700.7M20.700 15.700l-1.700-.7M8.300 20.700l.7-1.700M15.700 20.700l-.7-1.700"
			/></g
		>
	{:else if nom === 'soir'}
		<!-- croissant et étoile du soir : vêpres et complies -->
		<path d="M14.500 4.200A7.800 7.800 0 1 0 19.800 16a6.300 6.300 0 0 1-5.300-11.800z" />
		<g class="fin"
			><path d="M18.500 3v3.400M16.800 4.700h3.400M20.800 9.300v1.800M19.900 10.200h1.800M10.200 9.800c-.700 1.500-.700 3.300.2 4.800" /></g
		>
	{:else if nom === 'source'}
		<path d="M6 4.500h9l3 3V19.500H6z" /><path d="M9 11h6M9 14.500h6" />
	{/if}
</svg>

<style>
	svg {
		flex: none;
	}
	.fin {
		stroke-width: 0.75;
	}
</style>
