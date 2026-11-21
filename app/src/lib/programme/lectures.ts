/**
 * « Lectures du jour (n/N) » : un seul calcul pour Aujourd'hui et pour Lecture. Une lecture est lue quand sa coche
 * existe ; un office l'est quand chacune de ses heures canoniales est cochée (une coche par heure). Fonctions pures.
 */
import { cocheDeLHeure, heuresDe, type Heure } from './heures.ts';
import type { Journee, Lecture } from './types.ts';

export interface EtatLecture {
	lecture: Lecture;
	lu: boolean;
	/** Office : ses heures, et celles qui sont cochées. */
	heures?: Heure[];
	faites?: number;
	total?: number;
}

/** Les heures de l'office d'une lecture (premier texte qui en a), ou rien. */
export function heuresDeLaLecture(l: Lecture, corps: (id: string) => string | undefined): Heure[] {
	for (const s of l.sections) {
		const t = s.texte ? corps(s.texte) : undefined;
		const h = t ? heuresDe(t) : [];
		if (h.length) return h;
	}
	return [];
}

export function etatDesLectures(
	jr: Journee,
	coches: Record<string, number>,
	corps: (id: string) => string | undefined
): { lectures: EtatLecture[]; lues: number; total: number } {
	const lectures = jr.lectures
		.filter((l) => l.compte)
		.map((l): EtatLecture => {
			const heures = heuresDeLaLecture(l, corps);
			const canoniales = heures.filter((h) => h.canoniale);
			if (!canoniales.length) {
				// l'Évangile se coche aussi par « J'ai lu ce chapitre » (/ecriture : coche « lecture:Mt 5 »)
				const lu = (coches[l.id] ?? 0) > 0 || (l.section === 'ecriture' && Object.keys(coches).some((k) => k.startsWith('lecture:')));
				return { lecture: l, lu };
			}
			const faites = canoniales.filter((h) => (coches[cocheDeLHeure(l.id, h.cle)] ?? 0) > 0).length;
			return { lecture: l, lu: faites === canoniales.length, heures, faites, total: canoniales.length };
		});
	return { lectures, lues: lectures.filter((x) => x.lu).length, total: lectures.length };
}
