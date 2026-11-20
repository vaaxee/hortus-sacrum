/**
 * Bascule en base (une seule fois, meta « programme-v1 ») et retours en arrière depuis la page « Ce qui a changé ».
 * Le plan de la bascule est calculé par migration.ts (pur, testé).
 */
import { db } from '../db.ts';
import type { ElementListe } from '../types.ts';
import { entreeDe, planifierMigration, type Annulation, type Changement } from './migration.ts';
import type { Programme, ReglageProgramme } from './types.ts';

export const META_BASCULE = 'programme-v1';
export const META_ARCHIVE = 'liste-v1-archive';

export interface EtatBascule {
	date: string;
	changements: (Changement & { annule?: boolean })[];
}

/** Bascule l'ancienne liste vers le programme. Ne fait rien si c'est déjà fait. Renvoie l'état noté. */
export async function basculer(programme: Programme): Promise<EtatBascule> {
	const deja = (await db.meta.get(META_BASCULE))?.valeur as EtatBascule | undefined;
	if (deja) return deja;
	const maintenant = new Date().toISOString();
	const liste = await db.liste.toArray();
	const { reglages, changements } = planifierMigration(liste, programme, maintenant);
	const etat: EtatBascule = { date: maintenant, changements };
	await db.transaction('rw', [db.liste, db.versions, db.meta, db.programme], async () => {
		if (liste.length) {
			// l'ancienne liste reste lisible : une version par ligne (historique des versions) et l'ensemble dans meta
			for (const e of liste) {
				await db.versions.add({ table: 'liste', objetId: e.id, date: maintenant, contenu: JSON.stringify(e) });
			}
			await db.meta.put({ cle: META_ARCHIVE, valeur: { date: maintenant, liste } });
		}
		for (const r of reglages) {
			const existant = await db.programme.get(r.id);
			if (!existant) await db.programme.put(r);
		}
		await db.meta.put({ cle: META_BASCULE, valeur: etat });
	});
	return etat;
}

/** L'ancienne liste archivée (vide sur une installation qui n'en a jamais eu). */
export async function ancienneListe(): Promise<ElementListe[]> {
	return (((await db.meta.get(META_ARCHIVE))?.valeur as { liste?: ElementListe[] } | undefined)?.liste ?? []).slice();
}

async function modifier(id: string, f: (r: ReglageProgramme) => ReglageProgramme | null): Promise<void> {
	const r = (await db.programme.get(id)) ?? { id, modifieLe: '' };
	const x = f({ ...r });
	if (x === null) await db.programme.delete(id);
	else await db.programme.put({ ...x, modifieLe: new Date().toISOString() });
}

/** Annule un changement de la bascule. */
export async function annuler(a: Annulation, indice: number): Promise<void> {
	if ('reactiver' in a) await modifier(a.reactiver, (r) => ({ ...r, actif: true }));
	else if ('supprimer' in a) await modifier(a.supprimer, () => null);
	else
		await modifier(a.retirer.id, (r) => {
			delete r[a.retirer.champ];
			return r;
		});
	const etat = (await db.meta.get(META_BASCULE))?.valeur as EtatBascule | undefined;
	if (etat?.changements[indice]) {
		etat.changements[indice].annule = true;
		await db.meta.put({ cle: META_BASCULE, valeur: etat });
	}
}

/** Reprend une ancienne ligne telle qu'elle était, comme ajout personnel. */
export async function reprendreTelleQuelle(ancienne: ElementListe): Promise<string> {
	const id = `perso:${ancienne.id}:reprise`;
	await db.programme.put({ id, entree: entreeDe({ ...ancienne, actif: true }, id), modifieLe: new Date().toISOString() });
	return id;
}
