// Contrôle des invocations du martyrologe sur toute une année (src/lib/martyrologe-controle.ts).
// Usage, depuis app/ : node --experimental-strip-types scripts/controle-martyrologe.mjs [2026-2027]
// Écrit docs/audits/martyrologe-invocations-reste.tsv : date, clé de l'éloge, genre du défaut, détail.
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { controler } from '../src/lib/martyrologe-controle.ts';

const racine = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const annee = process.argv[2] ?? '2026-2027';
const jours = JSON.parse(readFileSync(join(racine, 'data', 'calendar', `${annee}.json`), 'utf-8'));
const lignes = ['date\tcle\tgenre\tdetail'];
const compte = {};
for (const j of jours) {
	for (const m of j.martyrologe ?? []) {
		for (const a of controler(m.texte, m.texte_la)) {
			compte[a.genre] = (compte[a.genre] ?? 0) + 1;
			lignes.push([j.date, m.cle, a.genre, a.detail].join('\t'));
		}
	}
}
writeFileSync(join(racine, 'docs', 'audits', 'martyrologe-invocations-reste.tsv'), lignes.join('\n') + '\n');
console.log(annee, compte);
