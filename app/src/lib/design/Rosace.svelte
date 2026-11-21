<script lang="ts">
	/**
	 * La roue symbolique dessinée en rosace : au centre l'unité, puis un anneau par roue (3, 4, 7, 12…),
	 * chaque anneau découpé en autant de vitraux que d'éléments. L'élément du jour monte au sommet, sous la croix.
	 */
	export interface Anneau {
		id: string;
		nombre: number;
		position: number;
		couleur: string;
		titre: string;
	}
	let { anneaux, choisi = $bindable(''), centre = 'Unus' }: { anneaux: Anneau[]; choisi?: string; centre?: string } = $props();

	const R0 = 46; // rayon du médaillon central
	const R1 = 188; // bord extérieur des anneaux
	const ROMAINS = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV'];

	const bornes = $derived.by(() => {
		const n = anneaux.length || 1;
		const ep = (R1 - R0) / n;
		return anneaux.map((_, i) => [R0 + i * ep + 3, R0 + (i + 1) * ep - 3] as const);
	});

	const pt = (r: number, a: number) => [r * Math.sin(a), -r * Math.cos(a)];
	/** Un vitrail : secteur d'anneau entre a0 et a1 (radians, 0 au sommet), avec un léger jour entre les pièces. */
	function vitrail(r0: number, r1: number, a0: number, a1: number): string {
		const g0 = 2.2 / r0,
			g1 = 2.2 / r1;
		const [x1, y1] = pt(r1, a0 + g1),
			[x2, y2] = pt(r1, a1 - g1);
		const [x3, y3] = pt(r0, a1 - g0),
			[x4, y4] = pt(r0, a0 + g0);
		const grand = a1 - a0 > Math.PI ? 1 : 0;
		const f = (v: number) => v.toFixed(2);
		return `M${f(x1)} ${f(y1)}A${r1} ${r1} 0 ${grand} 1 ${f(x2)} ${f(y2)}L${f(x3)} ${f(y3)}A${r0} ${r0} 0 ${grand} 0 ${f(x4)} ${f(y4)}Z`;
	}
	/** Rotation qui amène l'élément du jour au sommet. */
	const tour = (a: Anneau) => -((a.position + 0.5) * 360) / a.nombre;
	const perles = Array.from({ length: 48 }, (_, i) => pt(R1 + 8, (i * Math.PI * 2) / 48));
</script>

<svg
	class="rosace"
	viewBox="-212 -212 424 424"
	role="img"
	aria-label="La roue symbolique : l’élément du jour de chaque roue est au sommet, sous la croix"
>
	<defs>
		<radialGradient id="rosace-lumiere" cx="0" cy="0" r="200" gradientUnits="userSpaceOnUse">
			<stop offset="0" stop-color="var(--hs-or)" stop-opacity="0.22" />
			<stop offset="0.55" stop-color="var(--hs-or)" stop-opacity="0.05" />
			<stop offset="1" stop-color="var(--hs-or)" stop-opacity="0" />
		</radialGradient>
	</defs>

	<!-- halo et cercles de pierre -->
	<circle r="206" fill="url(#rosace-lumiere)" />
	<circle r={R1 + 14} class="pierre" />
	<circle r={R1 + 3} class="pierre fin" />
	{#each perles as [x, y], i (i)}<circle cx={x} cy={y} r="1.3" class="perle" />{/each}

	{#each anneaux as a, i (a.id)}
		{@const [r0, r1] = bornes[i]}
		<g
			class="anneau"
			class:choisi={choisi === a.id}
			style="--verre: {a.couleur}; transform: rotate({tour(a)}deg)"
			role="button"
			tabindex="0"
			aria-label="{a.titre}, {a.position + 1} sur {a.nombre}"
			onclick={() => (choisi = a.id)}
			onkeydown={(e) => (e.key === 'Enter' || e.key === ' ') && (choisi = a.id)}
		>
			{#each Array(a.nombre) as _, k (k)}
				{@const a0 = (k * Math.PI * 2) / a.nombre}
				{@const a1 = ((k + 1) * Math.PI * 2) / a.nombre}
				{@const m = (a0 + a1) / 2}
				{@const [lx, ly] = pt((r0 + r1) / 2, m)}
				<path d={vitrail(r0, r1, a0, a1)} class="verre" class:jour={k === a.position} />
				{#if a.nombre <= 15 && r1 - r0 > 14}
					{@const vu = ((((m * 180) / Math.PI + tour(a)) % 360) + 360) % 360}
					<text
						x={lx}
						y={ly}
						class="chiffre"
						class:jour={k === a.position}
						transform="rotate({(m * 180) / Math.PI + (vu > 90 && vu < 270 ? 180 : 0)} {lx} {ly})">{ROMAINS[k + 1] ?? k + 1}</text
					>
				{/if}
			{/each}
		</g>
	{/each}

	<!-- médaillon de l'unité -->
	<circle r={R0 - 4} class="medaillon" />
	<circle r={R0 - 9} class="pierre fin" />
	<g class="chrisme" stroke-linecap="round" stroke-linejoin="round">
		<path d="M0 -24V24M-15 -15L15 15M15 -15L-15 15" />
		<path d="M0 -24c9 0 13 4 13 9s-4 9-13 9" />
	</g>
	<text y="38" class="centre">{centre}</text>

	<!-- la croix pattée au sommet marque le jour -->
	<g class="croix" transform="translate(0 {-(R1 + 14)})">
		<path d="M0 -10l3 7h-6zM0 10l3 -7h-6zM-10 0l7 3v-6zM10 0l-7 3v-6z" />
		<circle r="2" />
	</g>
</svg>

<style>
	.rosace {
		width: 100%;
		max-width: 30rem;
		display: block;
		margin: 0 auto;
		overflow: visible;
	}
	.pierre {
		fill: none;
		stroke: var(--hs-or);
		stroke-width: 1.2;
		opacity: 0.85;
	}
	.pierre.fin {
		stroke-width: 0.6;
		opacity: 0.6;
	}
	.perle {
		fill: var(--hs-or);
		opacity: 0.7;
	}
	.anneau {
		transition: transform 900ms var(--hs-courbe);
		cursor: pointer;
		outline: none;
	}
	.verre {
		fill: color-mix(in srgb, var(--verre) 16%, var(--hs-fond));
		stroke: var(--hs-or);
		stroke-width: 0.6;
		stroke-opacity: 0.55;
		transition: fill var(--hs-duree-lente) var(--hs-courbe);
	}
	.verre.jour {
		fill: color-mix(in srgb, var(--verre) 78%, var(--hs-fond));
		stroke-width: 1.4;
		stroke-opacity: 1;
	}
	.anneau:hover .verre:not(.jour),
	.anneau.choisi .verre:not(.jour) {
		fill: color-mix(in srgb, var(--verre) 30%, var(--hs-fond));
	}
	.anneau:focus-visible .verre {
		stroke-width: 1.6;
		stroke-opacity: 1;
	}
	.chiffre {
		font-family: var(--hs-titre);
		font-size: 9px;
		letter-spacing: 0.06em;
		text-anchor: middle;
		dominant-baseline: central;
		fill: color-mix(in srgb, var(--verre) 70%, var(--hs-encre));
		pointer-events: none;
	}
	.chiffre.jour {
		fill: var(--hs-fond);
		font-weight: 600;
	}
	.medaillon {
		fill: color-mix(in srgb, var(--hs-or) 18%, var(--hs-fond));
		stroke: var(--hs-or);
		stroke-width: 1.2;
	}
	.chrisme path {
		fill: none;
		stroke: var(--hs-or-texte);
		stroke-width: 1.6;
	}
	.centre {
		font-family: var(--hs-titre);
		font-style: italic;
		font-size: 9px;
		text-anchor: middle;
		fill: var(--hs-or-texte);
		letter-spacing: 0.08em;
	}
	.croix path {
		fill: var(--hs-rubrique);
	}
	.croix circle {
		fill: var(--hs-or);
	}
	@media (prefers-reduced-motion: reduce) {
		.anneau {
			transition: none;
		}
	}
</style>
