// Brouillon du classement des textes du programme (lot « Dimensions », D1) : data/prieres/dimensions-textes.json.
// Chaque valeur vient des motifs de app/src/lib/etiquettes.ts et reste « devinée » jusqu'à relecture.
// Un classement relu (champ « releve ») n'est jamais réécrit. Lancer : node scripts/dimensions.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dimensionsDevinees } from '../src/lib/etiquettes.ts';
import { pieceVersTexte } from '../src/lib/livret.ts';
import { textesDuProgramme } from '../src/lib/programme/inventaire.ts';

const racine = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const lire = (chemin) => JSON.parse(readFileSync(join(racine, chemin), 'utf-8'));
const DIMENSIONS = ['fin', 'objet', 'grace', 'personne', 'forme'];

const programme = lire('data/programme/programme.json');
const textes = new Map([
	...lire('data/prieres/jardin.json').pieces.map((p) => {
		const t = pieceVersTexte(p);
		return [t.id, t];
	}),
	...lire('data/prieres/sources.json').pieces.map((t) => [t.id, t])
]);
const chemin = join(racine, 'data/prieres/dimensions-textes.json');
let ancien = {};
try {
	ancien = JSON.parse(readFileSync(chemin, 'utf-8')).textes ?? {};
} catch {
	ancien = {};
}

const sortie = {};
let releves = 0,
	vides = 0;
for (const id of [...textesDuProgramme(programme)].sort()) {
	if (ancien[id]?.releve) {
		sortie[id] = ancien[id];
		releves++;
		continue;
	}
	const t = textes.get(id);
	if (!t) continue;
	const d = dimensionsDevinees(t);
	const presentes = DIMENSIONS.filter((k) => d[k]?.length);
	if (!presentes.length) vides++;
	sortie[id] = { ...Object.fromEntries(presentes.map((k) => [k, d[k]])), devinee: presentes };
}
writeFileSync(
	chemin,
	JSON.stringify(
		{
			description:
				'Classement des textes du programme selon les cinq dimensions (docs/conception/LOT_DIMENSIONS.md, § 3.2). Brouillon déduit par app/scripts/dimensions.mjs : « devinee » liste les dimensions encore à relire ; « releve » date la relecture humaine, après quoi le classement n’est plus réécrit.',
			textes: sortie
		},
		null,
		'\t'
	) + '\n'
);
console.log(`${Object.keys(sortie).length} textes classés (${releves} relus, ${vides} sans aucune valeur devinée)`);
