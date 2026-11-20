/**
 * Données anciennes ou incomplètes (bug « Internal Error » de l'Historique, SPEC § 11).
 *
 * Ces tests décrivent le comportement attendu ; le bug est corrigé (20 nov. 2026).
 * La reproduction complète (navigation Profil → Historique avec des coches anciennes) est dans
 * `app/tests/historique.e2e.mjs`.
 */
import { describe, expect, it } from 'vitest';
import { Worker } from 'node:worker_threads';
import { occurrences } from './pratiques.ts';
import type { Regle } from './types.ts';

const DE = '2026-08-01';
const A = '2026-11-18';

/** Exécute `occurrences` dans un fil séparé, pour qu'une boucle infinie ne bloque pas la suite : rejet après `ms`. */
function occurrencesAvecDelai(regle: unknown, ms = 2000): Promise<unknown[]> {
	const url = new URL('./pratiques.ts', import.meta.url).href;
	const code = `
		const { parentPort, workerData } = require('node:worker_threads');
		import(workerData.url).then((m) => parentPort.postMessage(m.occurrences(workerData.regle, workerData.de, workerData.a)));
	`;
	return new Promise((ok, ko) => {
		const w = new Worker(code, { eval: true, workerData: { url, regle, de: DE, a: A } });
		const minuterie = setTimeout(() => {
			void w.terminate();
			ko(new Error(`occurrences() ne rend pas la main en ${ms} ms (boucle infinie)`));
		}, ms);
		w.on('message', (v) => {
			clearTimeout(minuterie);
			void w.terminate();
			ok(v as unknown[]);
		});
		w.on('error', (e) => {
			clearTimeout(minuterie);
			ko(e);
		});
	});
}

describe('occurrences() sur des règles incomplètes (anciennes versions, imports, synchronisation)', () => {
	it('une pratique sans règle ne fait pas planter le calcul', () => {
		expect(() => occurrences(undefined as unknown as Regle, DE, A)).not.toThrow();
	});

	it('une règle de genre inconnu ne donne aucune date', () => {
		expect(occurrences({ genre: 'semaine' } as unknown as Regle, DE, A)).toEqual([]);
	});

	it('une série dont le début est vide ne donne aucune date invalide', () => {
		const r = { genre: 'consecutifs', nombre: 9, jourSemaine: null, debut: '' } as Regle;
		expect(occurrences(r, DE, A).every((o) => /^\d{4}-\d{2}-\d{2}$/.test(o.date))).toBe(true);
	});

	it('« avant_fete » sans jour de semaine (champ absent) rend la main', async () => {
		const r = { genre: 'avant_fete', nombre: 9, mois: 12, jour: 8 };
		await expect(occurrencesAvecDelai(r)).resolves.toBeInstanceOf(Array);
	});
});
