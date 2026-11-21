// Compositeur d'ordo (LOT_DIMENSIONS § 6, lot D5) : écrit le rapport docs/audits/ORDO_<début>_<fin>.md.
// Lancer depuis app/ :  npm run ordo -- 2026-11-29 2026-12-24
// Il n'écrit que le rapport : jamais dans data/.
import { writeFileSync } from 'node:fs';
import { dimensionsEffectives } from '../src/lib/dimensions.ts';
import { journee } from '../src/lib/programme/journee.ts';
import { ordoDuJour, rapportOrdo } from '../src/lib/programme/ordo.ts';
import {
	CALENDRIER,
	CLASSEMENTS,
	corps,
	CYCLES,
	dimensions,
	PLAN,
	PROGRAMME,
	TEXTES,
	VOCABULAIRE
} from '../src/lib/programme/donnees-de-test.ts';

const [debut = '2026-11-29', fin = '2026-12-24'] = process.argv.slice(2);
const jours = CALENDRIER.filter((j) => j.date >= debut && j.date <= fin);
if (!jours.length) {
	console.error(`Aucun jour du calendrier entre ${debut} et ${fin}.`);
	process.exit(1);
}
const biblio = {
	textes: TEXTES.values(),
	dimensions: (t: Parameters<typeof dimensionsEffectives>[0] & { id: string }) => dimensionsEffectives(t, CLASSEMENTS[t.id]),
	formules: PROGRAMME.formules
};
const ordo = jours.map((jour) =>
	ordoDuJour(journee(PROGRAMME, { jour, pratiques: PLAN, corps, cycles: CYCLES, dimensions, vocabulaire: VOCABULAIRE }), jour.office, {
		...biblio,
		textes: TEXTES.values()
	})
);
const libelle = (d: keyof typeof VOCABULAIRE.dimensions, v: string) => VOCABULAIRE.dimensions[d].valeurs[v] ?? v;
const sortie = new URL(`../../docs/audits/ORDO_${debut}_${fin}.md`, import.meta.url);
writeFileSync(sortie, rapportOrdo(ordo, libelle));
const requis = ordo.reduce((n, j) => n + j.manques.filter((m) => m.requis).length, 0);
console.log(`${sortie.pathname} : ${ordo.length} jours, ${requis} manques requis.`);
