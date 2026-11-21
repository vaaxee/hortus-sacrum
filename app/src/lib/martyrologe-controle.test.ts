import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { controler, type Anomalie } from './martyrologe-controle.ts';
import { invocation } from './invocations.ts';
import { invocationLatine } from './invocations-latines.ts';

interface Eloge {
	cle: string;
	texte: string;
	texte_la?: string;
}
type Jour = { date: string; martyrologe?: Eloge[] };
const lire = (annee: string): Jour[] => JSON.parse(readFileSync(new URL(`../../../data/calendar/${annee}.json`, import.meta.url), 'utf-8'));
// l'année liturgique 2026-2027 (contrôle de l'année) ; novembre 2026 est encore dans 2025-2026
const jours = lire('2026-2027');
const novembre = lire('2025-2026');
const eloge = (date: string, cle: string) => novembre.find((j) => j.date === date)!.martyrologe!.find((m) => m.cle === cle)!;

describe('martyrologe : invocations française et latine', () => {
	it('18 nov. : les deux saints des basiliques, dans les deux langues', () => {
		const m = eloge('2026-11-18', 'Petri-Pauli');
		expect(invocation(m.texte)?.texte).toBe('Saints Pierre et Paul, priez pour nous.');
		expect(invocationLatine(m.texte_la)?.texte).toBe('Sancti Petre et Paule, apostoli, orate pro nobis peccatoribus. Amen.');
		expect(controler(m.texte, m.texte_la)).toEqual([]);
	});
	it('20 nov. : « Thebánæ legiónis » n’est pas un nom', () => {
		const m = eloge('2026-11-20', 'Octavii-Solutoris');
		expect(invocationLatine(m.texte_la)?.texte).toBe('Sancti Octávi, Solutor et Adventor, martyres, orate pro nobis peccatoribus. Amen.');
		expect(controler(m.texte, m.texte_la)).toEqual([]);
	});
	it('vocatifs et titres corrigés au contrôle de l’année', () => {
		expect(invocationLatine('Constantinópoli sancti Daniélis Stylítæ.')?.texte).toBe(
			'Sancte Daniel, stylita, ora pro nobis peccatoribus. Amen.'
		);
		expect(
			invocationLatine('Sanctárum Perpétuæ et Felicitátis Mártyrum, quæ sequénti die gloriósam martýrii corónam a Dómino recepérunt.')
				?.texte
		).toBe('Sanctæ Perpétua et Felicitas, martyres, orate pro nobis peccatoribus. Amen.');
		expect(invocationLatine('Hierosólymis Præsentátio beátæ Dei Genitrícis Vírginis Maríæ in Templo.')?.texte).toBe(
			'Beata Dei Genitrix María, virgo, ora pro nobis peccatoribus. Amen.'
		);
	});
	it('contrôle de l’année : pas plus de défauts que la liste du 21 nov. (docs/audits/martyrologe-invocations-reste.tsv)', () => {
		const compte: Record<Anomalie['genre'], number> = { nombre: 0, vocatif: 0, decoupage: 0, manque: 0 };
		for (const j of jours) for (const m of j.martyrologe ?? []) for (const a of controler(m.texte, m.texte_la)) compte[a.genre]++;
		// plafonds : ce qui reste à reprendre à la main (noms de la 3e déclinaison au vocatif incertain, listes
		// françaises abrégées en « et vos compagnons ») ; un plafond dépassé signale une régression
		expect(compte.decoupage).toBeLessThanOrEqual(1);
		expect(compte.vocatif).toBeLessThanOrEqual(180);
		expect(compte.nombre).toBeLessThanOrEqual(82);
		expect(compte.manque).toBeLessThanOrEqual(42);
	});
});
