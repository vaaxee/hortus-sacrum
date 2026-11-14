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
compact(join(racine, 'data', 'prieres', 'sources.json'), join(cible, 'prieres', 'sources.json'));
// roues symboliques (engine/roues/construire.py)
compact(join(racine, 'data', 'roues.json'), join(cible, 'roues.json'));
for (const f of readdirSync(join(racine, 'data', 'calendar'))) {
	compact(join(racine, 'data', 'calendar', f), join(cible, 'calendar', f));
}
// recueils de méditations et de lectures, découpés par jour (data/recueils/*.json)
mkdirSync(join(cible, 'recueils'), { recursive: true });
for (const f of readdirSync(join(racine, 'data', 'recueils'))) {
	if (f.endsWith('.json')) compact(join(racine, 'data', 'recueils', f), join(cible, 'recueils', f));
}
// index légers des recueils (sans les textes) : pour afficher le titre de la méditation du jour sans tout charger
mkdirSync(join(cible, 'recueils', 'index'), { recursive: true });
for (const f of readdirSync(join(racine, 'data', 'recueils'))) {
	if (!f.endsWith('.json')) continue;
	const r = JSON.parse(readFileSync(join(racine, 'data', 'recueils', f), 'utf-8'));
	r.entrees = r.entrees.map(({ cle, titre, tome, page }) => ({ cle, titre, tome, page, corps: '' }));
	writeFileSync(join(cible, 'recueils', 'index', f), JSON.stringify(r));
}
// Guéranger : un index et un fichier par volume
mkdirSync(join(cible, 'recueils', 'gueranger'), { recursive: true });
for (const f of readdirSync(join(racine, 'data', 'recueils', 'gueranger'))) {
	compact(join(racine, 'data', 'recueils', 'gueranger', f), join(cible, 'recueils', 'gueranger', f));
}
console.log('données copiées dans static/data');
