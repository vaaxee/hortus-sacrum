// Copie les données générées (../data) dans static/data pour l'app, en JSON compact.
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const racine = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const cible = join(racine, 'app', 'static', 'data');
const compact = (de, vers) => writeFileSync(vers, JSON.stringify(JSON.parse(readFileSync(de, 'utf-8'))));
mkdirSync(join(cible, 'prieres'), { recursive: true });
mkdirSync(join(cible, 'calendar'), { recursive: true });
compact(join(racine, 'data', 'prieres', 'jardin.json'), join(cible, 'prieres', 'jardin.json'));
for (const f of readdirSync(join(racine, 'data', 'calendar'))) {
	compact(join(racine, 'data', 'calendar', f), join(cible, 'calendar', f));
}
console.log('données copiées dans static/data');
