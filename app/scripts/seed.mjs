// Copie les données générées (../data) dans static/data pour l'app.
import { cpSync, mkdirSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const racine = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const cible = join(racine, 'app', 'static', 'data');
mkdirSync(join(cible, 'prieres'), { recursive: true });
mkdirSync(join(cible, 'calendar'), { recursive: true });
cpSync(join(racine, 'data', 'prieres', 'jardin.json'), join(cible, 'prieres', 'jardin.json'));
for (const f of readdirSync(join(racine, 'data', 'calendar'))) {
	cpSync(join(racine, 'data', 'calendar', f), join(cible, 'calendar', f));
}
console.log('données copiées dans static/data');
