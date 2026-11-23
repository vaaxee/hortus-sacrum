/** Évaluation des conditions `quand` du programme. Fonction pure. */
import type { Quand } from './types.ts';

/** Ce que le programme sait du jour : la date, et le jour liturgique s'il est calculé (data/calendar). */
export interface JourDuProgramme {
	date: string;
	temps?: string;
	office?: string;
	est_fete_sanctorale?: boolean;
	/** Code du jour dans le temporal (« Quadp3-2 »). */
	tempora?: string | null;
}

export function vaut(q: Quand | undefined, j: JourDuProgramme): boolean {
	if (!q) return true;
	const d = new Date(j.date + 'T12:00:00');
	if (q.jours_semaine && !q.jours_semaine.includes(d.getDay())) return false;
	if (q.semaines_du_mois && !q.semaines_du_mois.includes(Math.ceil(d.getDate() / 7))) return false;
	if (q.mois && !q.mois.includes(d.getMonth() + 1)) return false;
	if (q.tempora && !(j.temps && q.tempora.includes(j.temps))) return false;
	if (q.dates && !q.dates.some((x) => x === j.date || x === j.date.slice(5))) return false;
	if (q.code_tempora && !(j.tempora && q.code_tempora.includes(j.tempora))) return false;
	if (q.office !== undefined && !(j.office && new RegExp(q.office, 'u').test(j.office))) return false;
	if (q.ou && !q.ou.some((x) => vaut(x, j))) return false;
	if (q.sauf && vaut(q.sauf, j)) return false;
	return true;
}
