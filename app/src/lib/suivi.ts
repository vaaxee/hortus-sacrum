/** Suivi des pratiques : cocher ou décocher un jour accompli. */
import { db } from './db.ts';

export async function basculerFait(pratiqueId: string, date: string): Promise<void> {
	const existant = await db.faits.where('[pratiqueId+date]').equals([pratiqueId, date]).first();
	if (existant?.id !== undefined) await db.faits.delete(existant.id);
	else await db.faits.add({ pratiqueId, date, horodatage: new Date().toISOString() });
}

export async function marquerFaits(pratiqueId: string, dates: string[]): Promise<void> {
	for (const date of dates) {
		const existant = await db.faits.where('[pratiqueId+date]').equals([pratiqueId, date]).first();
		if (!existant) await db.faits.add({ pratiqueId, date, horodatage: new Date().toISOString() });
	}
}
