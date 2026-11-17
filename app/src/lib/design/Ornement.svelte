<script lang="ts">
	/**
	 * HORTUS SACRUM — ornements au trait fin, une seule couleur (currentColor).
	 * Bandes (grecque, laurier, perles, mosaique) : se répètent sur toute la largeur.
	 */
	type Nom =
		| 'fleuron'
		| 'grecque'
		| 'laurier'
		| 'perles'
		| 'mosaique'
		| 'palmette'
		| 'coin'
		| 'medaillon'
		| 'cherubin'
		| 'chrisme'
		| 'lis'
		| 'brin'
		| 'croix'
		| 'croix-pattee';

	let { nom, taille = 24, titre = '' }: { nom: Nom; taille?: number; titre?: string } = $props();
	const uid = $props.id();
</script>

{#if nom === 'fleuron'}
	<!-- filet d'or avec fleuron centré -->
	<div class="filet" role="presentation">
		<span></span>
		<!-- latine : fleur de lys entre deux croisettes -->
		<svg class="da-latine" viewBox="0 0 40 16" width="40" height="16" aria-hidden="true">
			<g fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round">
				<path d="M20 1.5c1.7 1.8 1.7 4.4 0 6.6c-1.7-2.2-1.7-4.8 0-6.6z" />
				<path d="M20 9.2c-1.1-2.5-3.4-3.3-5.2-1.9c1 .2 1.9.9 2.1 2" />
				<path d="M20 9.2c1.1-2.5 3.4-3.3 5.2-1.9c-1 .2-1.9.9-2.1 2" />
				<path d="M16.8 9.6h6.4M20 9.6v3.4M18.4 14.2c.6-.7 1-1 1.6-1s1 .3 1.6 1" />
				<path d="M6 8.5h3M7.5 7v3M31 8.5h3M32.5 7v3" />
			</g>
		</svg>
		<svg class="da-grecque" viewBox="0 0 40 16" width="40" height="16" aria-hidden="true">
			<g fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round">
				<path d="M20 2.5c2.2 2 2.2 4.2 0 5.5c-2.2-1.3-2.2-3.5 0-5.5z" />
				<path d="M20 8v5.5" />
				<path d="M20 11c-2.6-.2-4.6-1.4-5.6-3.6c2.6-.3 4.6.9 5.6 3.6z" />
				<path d="M20 11c2.6-.2 4.6-1.4 5.6-3.6c-2.6-.3-4.6.9-5.6 3.6z" />
				<path d="M11.5 8.5c-2 .9-4 .9-6 0M28.5 8.5c2 .9 4 .9 6 0" />
				<circle cx="3" cy="8.5" r=".7" /><circle cx="37" cy="8.5" r=".7" />
			</g>
		</svg>
		<span></span>
	</div>
{:else if nom === 'grecque'}
	<!-- latine : rinceau de vigne (tige ondulée, feuilles, grains de raisin en rubis) -->
	<svg class="bande da-latine" height="12" width="100%" aria-hidden="true">
		<defs>
			<pattern id="{uid}-r" width="32" height="12" patternUnits="userSpaceOnUse">
				<g fill="none" stroke="currentColor" stroke-width="0.8" stroke-linecap="round">
					<path d="M0 6c4-5 12-5 16 0s12 5 16 0" />
					<path d="M8 2.3c1.8-1.6 4-1.4 5 .2c-1.8 1.2-3.6 1.2-5-.2z" />
					<path d="M24 9.7c-1.8 1.6-4 1.4-5-.2c1.8-1.2 3.6-1.2 5 .2z" />
				</g>
				<g fill="var(--hs-rubrique)">
					<circle cx="4.2" cy="9" r=".9" /><circle cx="2.6" cy="10.3" r=".9" /><circle cx="4.6" cy="11" r=".8" />
					<circle cx="27.8" cy="3" r=".9" /><circle cx="29.4" cy="1.7" r=".9" /><circle cx="27.4" cy="1" r=".8" />
				</g>
			</pattern>
		</defs>
		<rect width="100%" height="12" fill="url(#{uid}-r)" />
	</svg>
	<svg class="bande da-grecque" height="8" width="100%" aria-hidden="true">
		<defs>
			<pattern id="{uid}-g" width="16" height="8" patternUnits="userSpaceOnUse">
				<path d="M0 7.5h12.5v-7h-9v4.5h5.5v-2" fill="none" stroke="currentColor" stroke-width="0.75" />
			</pattern>
		</defs>
		<rect width="100%" height="8" fill="url(#{uid}-g)" />
	</svg>
{:else if nom === 'laurier'}
	<svg class="bande" height="12" width="100%" aria-hidden="true">
		<defs>
			<pattern id="{uid}-l" width="18" height="12" patternUnits="userSpaceOnUse">
				<g fill="none" stroke="currentColor" stroke-width="0.75" stroke-linecap="round">
					<path d="M0 6h18" />
					<path d="M3 6c1.5-3.2 4-4.2 7-3.6c-1.2 2.8-3.6 4-7 3.6z" />
					<path d="M3 6c1.5 3.2 4 4.2 7 3.6c-1.2-2.8-3.6-4-7-3.6z" />
					<circle cx="14.5" cy="6" r="1" />
				</g>
			</pattern>
		</defs>
		<rect width="100%" height="12" fill="url(#{uid}-l)" />
	</svg>
{:else if nom === 'perles'}
	<svg class="bande" height="6" width="100%" aria-hidden="true">
		<defs>
			<pattern id="{uid}-p" width="14" height="6" patternUnits="userSpaceOnUse">
				<g fill="none" stroke="currentColor" stroke-width="0.75">
					<circle cx="3" cy="3" r="2" /><path d="M7.5 1.2v3.6M10 1.2v3.6" />
				</g>
			</pattern>
		</defs>
		<rect width="100%" height="6" fill="url(#{uid}-p)" />
	</svg>
{:else if nom === 'mosaique'}
	<!-- tesselles byzantines : petits carrés et losanges, or, lapis, vert, rubis -->
	<svg class="bande mosaique" height="14" width="100%" aria-hidden="true">
		<defs>
			<pattern id="{uid}-m" width="28" height="14" patternUnits="userSpaceOnUse">
				<rect x=".5" y=".5" width="13" height="13" fill="none" stroke="var(--hs-or)" stroke-width="0.75" />
				<path d="M7 2.2L11.8 7L7 11.8L2.2 7z" fill="var(--hs-lapis-brut)" />
				<rect x="5.6" y="5.6" width="2.8" height="2.8" fill="var(--hs-or)" />
				<rect x="14.5" y=".5" width="13" height="13" fill="none" stroke="var(--hs-or)" stroke-width="0.75" />
				<rect x="16.6" y="2.6" width="3.6" height="3.6" fill="var(--hs-rubis-brut)" />
				<rect x="21.8" y="2.6" width="3.6" height="3.6" fill="var(--hs-vert-brut)" />
				<rect x="16.6" y="7.8" width="3.6" height="3.6" fill="var(--hs-vert-brut)" />
				<rect x="21.8" y="7.8" width="3.6" height="3.6" fill="var(--hs-rubis-brut)" />
				<rect x="20.1" y="6.1" width="1.8" height="1.8" fill="var(--hs-or)" />
			</pattern>
		</defs>
		<rect width="100%" height="14" fill="url(#{uid}-m)" />
	</svg>
{:else}
	<svg
		class="motif"
		width={nom === 'cherubin' ? taille * 2.14 : taille}
		height={taille}
		viewBox={nom === 'cherubin' ? '-13.5 -8.2 27 12.6' : '0 0 24 24'}
		role={titre ? 'img' : undefined}
		aria-label={titre || undefined}
		aria-hidden={titre ? undefined : 'true'}
	>
		{#if nom === 'palmette'}
			<g fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
				<path d="M12 20V7" />
				<path d="M12 7c-1.4-1.6-1.4-3.4 0-5c1.4 1.6 1.4 3.4 0 5z" />
				<path d="M12 12c-2.6-.6-4.4-2.4-5-5.2c2.8.4 4.6 2.2 5 5.2z" />
				<path d="M12 12c2.6-.6 4.4-2.4 5-5.2c-2.8.4-4.6 2.2-5 5.2z" />
				<path d="M12 17c-3.2.2-5.8-1.2-7.6-4c3.4-.6 6 .8 7.6 4z" />
				<path d="M12 17c3.2.2 5.8-1.2 7.6-4c-3.4-.6-6 .8-7.6 4z" />
				<path d="M7.5 21.5h9" />
			</g>
		{:else if nom === 'coin'}
			<!-- quart de rosace pour les angles des cadres importants -->
			<g fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round">
				<path d="M1 23V1h22" />
				<path d="M4.5 16A11.5 11.5 0 0 1 16 4.5" />
				<path d="M4.5 4.5l6.2 6.2M4.5 10c1.6-.4 3-.2 4.3.7M10 4.5c-.4 1.6-.2 3 .7 4.3" />
				<circle cx="4.5" cy="4.5" r="1.4" />
			</g>
		{:else if nom === 'medaillon'}
			<g fill="none" stroke="currentColor">
				<circle cx="12" cy="12" r="11" stroke-width="1" />
				<circle cx="12" cy="12" r="9" stroke-width="0.5" />
			</g>
		{:else if nom === 'chrisme'}
			<g fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
				<path d="M12 21.5V3h2.6a3.3 3.3 0 0 1 0 6.6H12" />
				<path d="M5.5 6.5l13 13M18.5 6.5l-13 13" />
			</g>
		{:else if nom === 'lis'}
			<g fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
				<path d="M12 2.5c2.4 3 2.4 7 0 11.5c-2.4-4.5-2.4-8.500 0-11.5z" />
				<path d="M10.600 13.500C8 12 5.500 9.500 3.500 9c-.6 3.200 1.400 6 5.500 6.500" />
				<path d="M13.400 13.500C16 12 18.500 9.500 20.500 9c.6 3.200-1.400 6-5.500 6.500" />
				<path d="M7.500 15.500h9M12 15.500V22M9.500 19h5" />
			</g>
		{:else if nom === 'brin'}
			<!-- le brin qui se dessine dans la case cochée -->
			<g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
				<path class="trace" pathLength="1" d="M12 20V6" />
				<path class="trace" pathLength="1" d="M12 14c-3.4-.4-5.400-2.400-6-5.600c3.400.2 5.400 2.200 6 5.600z" />
				<path class="trace" pathLength="1" d="M12 10.500c3-.4 4.800-2.200 5.400-5c-3 .2-4.800 2-5.400 5z" />
			</g>
		{:else if nom === 'croix-pattee'}
			<!-- croix pattée : bras évasés, au trait -->
			<path
				fill="none"
				stroke="currentColor"
				stroke-width="1"
				stroke-linejoin="miter"
				d="M10 2.5h4l-.9 7.6l7.6-.9v4l-7.6-.9l.9 7.6h-4l.9-7.6l-7.6.9v-4l7.6.9z"
			/>
		{:else if nom === 'croix'}
			<g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
				<path d="M12 3v18M6.500 8.500h11" />
			</g>
		{:else if nom === 'cherubin'}
			<!-- chérubin du calendrier papier (docs/calendrier/source/cherub.tex), retranscrit trait pour trait -->
			<g transform="scale(1,-1)" fill="none" stroke="currentColor" stroke-width="0.19" stroke-linecap="round" stroke-linejoin="round">
				{#each [1, -1] as s}
					<g transform="scale({s},1)">
						<path
							d="M2.9 1.4C4.5 4.8 8.5 7.2 12.6 7.4C12.2 6.4 11.8 5.9 11.1 5.4C12 4.9 12 4.1 11.3 3.6C10 3.6 9.4 3.3 9.4 2.4C8.6 2.6 7.3 2.1 7.2 1C6.2 1.1 5.1.5 5-.6C4.3-.6 3.6-.9 3.2-1.4"
						/>
						<path d="M4.4 2.6C6.6 4.6 8.6 5.6 11.1 5.4" />
						<path d="M5 1.6C6.6 2.8 8.6 3.4 11.3 3.6" />
						<path d="M4.6.4C5.6 1.2 6.6 1.5 7.2 1" />
					</g>
				{/each}
				<circle cx="0" cy="0.2" r="3.3" fill="var(--hs-fond)" />
				{#each [[-1.8, 3], [0, 3.5], [1.8, 3]] as [x, y]}
					<path d="M{x - 0.6} {y}A.6.6 0 1 0 {x} {y - 0.6}" />
				{/each}
				<path d="M-1.6.6A.6.6 0 0 1-.472.6" />
				<path d="M.5.6A.6.6 0 0 1 1.628.6" />
				<path d="M-.5-1.3C-.2-1.65.2-1.65.5-1.3" />
			</g>
		{/if}
	</svg>
{/if}

<style>
	.filet {
		display: flex;
		align-items: center;
		gap: 12px;
		color: var(--hs-or);
		width: 100%;
	}
	.filet span {
		flex: 1;
		border-top: var(--hs-cheveu) solid var(--hs-or-trait);
	}
	.filet svg {
		flex: none;
	}
	.bande {
		display: block;
		color: var(--hs-or);
	}
	.motif {
		display: inline-block;
		flex: none;
	}
</style>
