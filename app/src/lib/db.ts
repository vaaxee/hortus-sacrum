import Dexie, { type Table } from 'dexie';
import type {
	Base, Coche, ElementListe, Fait, FetePerso, Meditation, NomTable, NoteJour, Pratique, Recueil, Texte, Version
} from './types';
import { TABLES } from './types';

/** Base locale (IndexedDB). La synchronisation entre appareils viendra s'y brancher (étape 6). */
export class HebdoDB extends Dexie {
	textes!: Table<Texte, string>;
	pratiques!: Table<Pratique, string>;
	liste!: Table<ElementListe, string>;
	recueils!: Table<Recueil, string>;
	meditations!: Table<Meditation, string>;
	fetes!: Table<FetePerso, string>;
	notes!: Table<NoteJour, string>;
	versions!: Table<Version, number>;
	coches!: Table<Coche, number>;
	faits!: Table<Fait, number>;
	meta!: Table<{ cle: string; valeur: unknown }, string>;

	constructor(nom = 'hebdomada') {
		super(nom);
		this.version(1).stores({
			textes: 'id, partie, categorie, origine, supprimeLe, ordre',
			pratiques: 'id, type, origine, supprimeLe',
			liste: 'id, moment, ordre, supprimeLe',
			recueils: 'id, supprimeLe',
			meditations: 'id, recueilId, rang, supprimeLe',
			fetes: 'id, [mois+jour], supprimeLe',
			notes: 'id, date, supprimeLe',
			versions: '++id, [table+objetId], date',
			coches: '++id, date, [date+elementId]',
			meta: 'cle'
		});
		this.version(2).stores({ faits: '++id, [pratiqueId+date], pratiqueId, date' });
	}
}

export const db = new HebdoDB();

const maintenant = () => new Date().toISOString();

export function nouvelId(): string {
	return crypto.randomUUID();
}

/** Contenu d'un objet sans ses champs techniques : sert aux versions et à l'original. */
export function contenu<T extends Base>(o: T): string {
	const { original, creeLe, modifieLe, supprimeLe, ...reste } = o;
	return JSON.stringify(reste);
}

function table<T extends Base>(nom: NomTable): Table<T, string> {
	return db[nom] as unknown as Table<T, string>;
}

/** Crée un objet. Les objets du livret ou d'une source vérifiée gardent leur original. */
export async function creer<T extends Base>(nom: NomTable, o: Omit<T, 'creeLe' | 'modifieLe'>): Promise<T> {
	const t = maintenant();
	const obj = { ...o, creeLe: t, modifieLe: t } as T;
	if (obj.origine !== 'personnel' && !obj.original) obj.original = contenu(obj);
	await table<T>(nom).put(obj);
	return obj;
}

/** Enregistre une modification en gardant la version précédente dans l'historique. */
export async function enregistrer<T extends Base>(nom: NomTable, o: T): Promise<T> {
	const avant = await table<T>(nom).get(o.id);
	const obj = { ...o, modifieLe: maintenant() };
	await db.transaction('rw', table<T>(nom), db.versions, async () => {
		if (avant && contenu(avant) !== contenu(obj)) {
			await db.versions.add({ table: nom, objetId: o.id, date: avant.modifieLe, contenu: contenu(avant) });
		}
		await table<T>(nom).put(obj);
	});
	return obj;
}

export async function dupliquer<T extends Base & { titre: string }>(nom: NomTable, id: string): Promise<T | undefined> {
	const o = await table<T>(nom).get(id);
	if (!o) return;
	const { original, supprimeLe, ...reste } = o;
	return creer<T>(nom, { ...(reste as T), id: nouvelId(), origine: 'personnel', titre: `${o.titre} (copie)` });
}

/** Suppression en deux temps : d'abord la corbeille. */
export async function mettreALaCorbeille(nom: NomTable, id: string): Promise<void> {
	await table(nom).update(id, { supprimeLe: maintenant() } as Partial<Base>);
}

export async function sortirDeLaCorbeille(nom: NomTable, id: string): Promise<void> {
	const o = await table(nom).get(id);
	if (!o) return;
	delete o.supprimeLe;
	await table(nom).put(o);
}

export async function supprimerDefinitivement(nom: NomTable, id: string): Promise<void> {
	await db.transaction('rw', table(nom), db.versions, async () => {
		await table(nom).delete(id);
		await db.versions.where('[table+objetId]').equals([nom, id]).delete();
	});
}

/** Le rang dans une liste n'est pas du contenu : le changer ne fait pas d'un objet un objet « modifié ». */
function sansOrdre(json: string): string {
	const { ordre, ...reste } = JSON.parse(json) as Record<string, unknown>;
	return JSON.stringify(reste);
}

export function estModifie(o: Base): boolean {
	return !!o.original && sansOrdre(o.original) !== sansOrdre(contenu(o));
}

/** Revient à l'état d'origine (livret ou source vérifiée) ; l'état actuel passe dans l'historique. */
export async function restaurerOriginal<T extends Base>(nom: NomTable, id: string): Promise<T | undefined> {
	const o = await table<T>(nom).get(id);
	if (!o?.original) return o;
	const orig = JSON.parse(o.original) as T & { ordre?: number };
	// on garde le rang actuel : restaurer un texte ne le déplace pas
	const ordre = (o as { ordre?: number }).ordre;
	return enregistrer<T>(nom, { ...o, ...orig, ...(ordre === undefined ? {} : { ordre }), original: o.original });
}

export async function versions(nom: NomTable, id: string): Promise<Version[]> {
	const v = await db.versions.where('[table+objetId]').equals([nom, id]).toArray();
	return v.sort((a, b) => b.date.localeCompare(a.date));
}

export async function restaurerVersion<T extends Base>(nom: NomTable, id: string, v: Version): Promise<T | undefined> {
	const o = await table<T>(nom).get(id);
	if (!o) return;
	return enregistrer<T>(nom, { ...o, ...(JSON.parse(v.contenu) as T) });
}

// ------------------------------------------------------------------ export / import
export interface Sauvegarde {
	format: 'hebdomada';
	version: 1;
	date: string;
	tables: Record<string, unknown[]>;
}

export async function exporter(): Promise<Sauvegarde> {
	const tables: Record<string, unknown[]> = {};
	for (const nom of [...TABLES, 'versions', 'coches', 'faits', 'meta'] as const) {
		tables[nom] = await (db[nom] as Table).toArray();
	}
	return { format: 'hebdomada', version: 1, date: maintenant(), tables };
}

/** Importe une sauvegarde. « remplacer » vide d'abord la base ; « fusionner » garde l'objet le plus récent. */
export async function importer(s: Sauvegarde, mode: 'remplacer' | 'fusionner'): Promise<number> {
	if (s?.format !== 'hebdomada' || !s.tables) throw new Error('Ce fichier n’est pas une sauvegarde Hebdomada.');
	let n = 0;
	const noms = [...TABLES, 'versions', 'coches', 'faits', 'meta'] as const;
	await db.transaction('rw', noms.map((x) => db[x] as Table), async () => {
		for (const nom of noms) {
			const lignes = (s.tables[nom] ?? []) as Record<string, unknown>[];
			const t = db[nom] as Table;
			if (mode === 'remplacer') {
				await t.clear();
				await t.bulkPut(lignes);
				n += lignes.length;
				continue;
			}
			if (nom === 'versions' || nom === 'coches' || nom === 'faits') continue; // la fusion ne duplique pas les journaux
			for (const l of lignes) {
				const cle = (l.id ?? l.cle) as string;
				const existant = (await t.get(cle)) as Record<string, unknown> | undefined;
				if (!existant || String(l.modifieLe ?? '') > String(existant.modifieLe ?? '')) {
					await t.put(l);
					n++;
				}
			}
		}
	});
	return n;
}
