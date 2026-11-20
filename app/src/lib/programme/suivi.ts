/**
 * Cocher une ligne de la journée calculée. Une ligne se coche une fois par récitation (Angélus : trois) ; ses invités
 * sont cochés avec elle. Une pratique du plan (ligne propre, ou annotation d'une ligne hôte) est suivie dans `faits`,
 * comme avant, pour les séries, l'Historique et les couronnes.
 */
import { db } from '../db.ts';
import { basculerFait, marquerFaits } from '../suivi.ts';
import { recitations } from './bilan.ts';
import type { Ligne } from './types.ts';

export type Suivable = Pick<Ligne, 'id' | 'heures' | 'annotations'>;

/** Pratiques du plan qui annotent la ligne (elles se cochent avec elle). */
const pratiquesAnnotees = (l: Suivable, pratiques: Set<string>) => [
	...new Set(l.annotations.map((a) => a.source).filter((s) => pratiques.has(s)))
];

/**
 * Une récitation de plus (ou tout décocher si la ligne était finie). `faites` : récitations déjà cochées ce jour-là.
 * `pratiques` : identifiants de la table `pratiques` (une ligne qui en porte un est une pratique du plan).
 */
export async function cocher(l: Suivable, date: string, faites: number, pratiques: Set<string>): Promise<void> {
	if (pratiques.has(l.id)) return basculerFait(l.id, date);
	const total = recitations(l);
	const annotees = pratiquesAnnotees(l, pratiques);
	if (faites >= total) {
		await db.coches.where('[date+elementId]').equals([date, l.id]).delete();
		for (const p of annotees) await db.faits.where('[pratiqueId+date]').equals([p, date]).delete();
		return;
	}
	await db.coches.add({ date, elementId: l.id, rang: faites, horodatage: new Date().toISOString() });
	if (faites + 1 >= total) for (const p of annotees) await marquerFaits(p, [date]);
}

/** Une jaculatoire dite : une coche « jac:<id> » (comptée dans les indulgences du jour). */
export async function direJaculatoire(id: string, date: string): Promise<void> {
	const n = await db.coches
		.where('[date+elementId]')
		.equals([date, `jac:${id}`])
		.count();
	await db.coches.add({ date, elementId: `jac:${id}`, rang: n, horodatage: new Date().toISOString() });
}
