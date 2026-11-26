/** Évaluation des conditions `quand` du programme. Fonction pure. */
import type { AncreMensuelle, Quand } from './types.ts';

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
	if (q.autour && !dansLaFenetre(q.autour, j.date)) return false;
	if (q.office !== undefined && !(j.office && new RegExp(q.office, 'u').test(j.office))) return false;
	if (q.ou && !q.ou.some((x) => vaut(x, j))) return false;
	if (q.sauf && vaut(q.sauf, j)) return false;
	return true;
}

const JOUR = 86400000;

/** Jour d'ancrage d'un mois (mois de 1 à 12 ; débordement admis : 0 = décembre de l'année d'avant). */
function ancreDuMois(an: number, mois: number, a: AncreMensuelle): Date {
	if ('jour' in a) return new Date(an, mois - 1, a.jour, 12);
	const premier = new Date(an, mois - 1, 1, 12);
	return new Date(an, mois - 1, 1 + ((a.jour_semaine - premier.getDay() + 7) % 7) + 7 * (a.rang - 1), 12);
}

/** La date tombe-t-elle entre ancre + de et ancre + a (compris), pour une occurrence de l'ancre ? */
function dansLaFenetre(f: NonNullable<Quand['autour']>, date: string): boolean {
	const d = new Date(date + 'T12:00:00');
	const ancres: Date[] = [];
	if (typeof f.ancre === 'string') {
		const [m, jj] = f.ancre.split('-').map(Number);
		for (let an = d.getFullYear() - 1; an <= d.getFullYear() + 1; an++) ancres.push(new Date(an, m - 1, jj, 12));
	} else {
		// fenêtres mensuelles de quelques semaines au plus : deux mois de part et d'autre suffisent
		for (let k = -2; k <= 2; k++) ancres.push(ancreDuMois(d.getFullYear(), d.getMonth() + 1 + k, f.ancre));
	}
	return ancres.some((x) => {
		const ecart = Math.round((d.getTime() - x.getTime()) / JOUR);
		return ecart >= f.de && ecart <= f.a;
	});
}
