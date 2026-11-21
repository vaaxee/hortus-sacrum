/**
 * Pratiques et dévotions : calcul des jours d'après la règle, compteur n/N,
 * détection des séries interrompues. Jour de semaine : 0 = dimanche … 6 = samedi.
 */
import type { Pratique, Regle } from './types.ts';

export interface Occurrence {
	date: string;
	/** Rang dans la série, à partir de 1 ; 0 si la pratique n'est pas comptée. */
	rang: number;
	/** Longueur de la série ; 0 si elle n'est pas comptée. */
	total: number;
}

const J = 86400000;
const versDate = (s: string) => new Date(s + 'T12:00:00');
export const versIso = (d: Date) =>
	`${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const plus = (d: Date, n: number) => new Date(d.getTime() + n * J);

/** Le rang-ième jour de semaine du mois (rang 1 = premier). */
function niemeDuMois(an: number, mois: number, rang: number, jourSemaine: number): Date {
	const d = new Date(an, mois - 1, 1, 12);
	const decal = (jourSemaine - d.getDay() + 7) % 7;
	return plus(d, decal + 7 * (rang - 1));
}

/** Toutes les occurrences d'une règle entre deux dates incluses (AAAA-MM-JJ). */
export function occurrences(regle: Regle | undefined, de: string, a: string): Occurrence[] {
	const out: Occurrence[] = [];
	// données anciennes ou incomplètes : pas de règle, pas de jours (jamais d'erreur ni de boucle sans fin)
	if (!regle || typeof regle !== 'object') return out;
	const d0 = versDate(de);
	const d1 = versDate(a);
	const dans = (d: Date) => d >= d0 && d <= d1;
	const ajouter = (d: Date, rang: number, total: number) => {
		if (dans(d)) out.push({ date: versIso(d), rang, total });
	};

	switch (regle.genre) {
		case 'consecutifs': {
			const pas = regle.jourSemaine === null ? 1 : 7;
			let debut = versDate(regle.debut);
			if (regle.jourSemaine !== null) debut = plus(debut, (regle.jourSemaine - debut.getDay() + 7) % 7);
			for (let i = 0; i < regle.nombre; i++) ajouter(plus(debut, i * pas), i + 1, regle.nombre);
			break;
		}
		case 'avant_fete': {
			for (let an = d0.getFullYear(); an <= d1.getFullYear() + 1; an++) {
				const fete = new Date(an, regle.mois - 1, regle.jour, 12);
				if (regle.jourSemaine === null) {
					for (let i = 0; i < regle.nombre; i++) ajouter(plus(fete, i - regle.nombre), i + 1, regle.nombre);
				} else {
					// les N jours de semaine qui précèdent la fête
					let dernier = plus(fete, -1);
					if (!(regle.jourSemaine >= 0 && regle.jourSemaine <= 6) || isNaN(dernier.getTime())) continue;
					while (dernier.getDay() !== regle.jourSemaine) dernier = plus(dernier, -1);
					for (let i = 0; i < regle.nombre; i++) ajouter(plus(dernier, -7 * (regle.nombre - 1 - i)), i + 1, regle.nombre);
				}
			}
			break;
		}
		case 'fixe': {
			for (let an = d0.getFullYear(); an <= d1.getFullYear(); an++) ajouter(new Date(an, regle.mois - 1, regle.jour, 12), 0, 0);
			break;
		}
		case 'mensuel': {
			const decalage = regle.decalage ?? 0;
			const total = regle.nombre ?? 0;
			if (total && regle.debut) {
				// série comptée : N mois de suite à partir du mois de « debut »
				const deb = versDate(regle.debut);
				for (let i = 0; i < total; i++) {
					const m = new Date(deb.getFullYear(), deb.getMonth() + i, 1, 12);
					ajouter(plus(niemeDuMois(m.getFullYear(), m.getMonth() + 1, regle.rang, regle.jourSemaine), decalage), i + 1, total);
				}
			} else {
				for (
					let m = new Date(d0.getFullYear(), d0.getMonth() - 1, 1, 12);
					m <= plus(d1, 31);
					m = new Date(m.getFullYear(), m.getMonth() + 1, 1, 12)
				) {
					ajouter(plus(niemeDuMois(m.getFullYear(), m.getMonth() + 1, regle.rang, regle.jourSemaine), decalage), 0, 0);
				}
			}
			break;
		}
		case 'mois_entier': {
			for (let an = d0.getFullYear(); an <= d1.getFullYear(); an++) {
				const n = new Date(an, regle.mois, 0).getDate();
				for (let j = 1; j <= n; j++) ajouter(new Date(an, regle.mois - 1, j, 12), j, n);
			}
			break;
		}
		case 'roue':
			// une roue n'a pas de jours propres : son élément change chaque jour (voir roues.ts)
			break;
		case 'hebdomadaire': {
			for (let d = plus(d0, (regle.jourSemaine - d0.getDay() + 7) % 7); d <= d1; d = plus(d, 7)) ajouter(d, 0, 0);
			break;
		}
	}
	return out.sort((x, y) => x.date.localeCompare(y.date));
}

/** L'occurrence d'une pratique à une date donnée, s'il y en a une. */
export function occurrenceDu(p: Pratique, date: string): Occurrence | undefined {
	return occurrences(p.regle, date, date)[0];
}

export interface Etat {
	/** Occurrences de la série en cours ou de la prochaine (vide si rien dans l'année qui vient). */
	serie: Occurrence[];
	prochaine?: Occurrence;
	/** Nombre d'occurrences accomplies dans la série. */
	faites: number;
	/** Occurrences passées de la série qui n'ont pas été cochées. */
	manquees: Occurrence[];
	phase: 'en_cours' | 'a_venir' | 'terminee' | 'permanente';
}

/**
 * État d'une pratique à la date du jour : série en cours, compteur, jours manqués.
 * « faits » : dates déjà cochées pour cette pratique.
 */
export function etat(p: Pratique, aujourdhui: string, faits: Set<string>): Etat {
	const t = versDate(aujourdhui);
	const toutes = occurrences(p.regle, versIso(plus(t, -400)), versIso(plus(t, 400)));
	const comptee = toutes.some((o) => o.total > 0);
	const prochaine = toutes.find((o) => o.date >= aujourdhui);
	if (!comptee) {
		return { serie: [], prochaine, faites: 0, manquees: [], phase: prochaine ? 'permanente' : 'terminee' };
	}
	// séries : chaque suite d'occurrences qui recommence au rang 1
	const series: Occurrence[][] = [];
	for (const o of toutes) {
		if (o.rang === 1 || !series.length) series.push([]);
		series[series.length - 1].push(o);
	}
	const complete = (s: Occurrence[]) => s[0].rang === 1;
	const enCours = series.find((s) => complete(s) && s[0].date <= aujourdhui && s[s.length - 1].date >= aujourdhui);
	const aVenir = series.find((s) => complete(s) && s[0].date > aujourdhui);
	const serie = enCours ?? aVenir ?? [];
	const faites = serie.filter((o) => faits.has(o.date)).length;
	// on ne compte un jour comme manqué qu'après le premier jour coché de la série :
	// une série commencée avant l'installation, ou jamais suivie, n'est pas « interrompue »
	const premierFait = enCours?.find((o) => faits.has(o.date))?.date;
	const manquees = enCours && premierFait ? enCours.filter((o) => o.date > premierFait && o.date < aujourdhui && !faits.has(o.date)) : [];
	return { serie, prochaine, faites, manquees, phase: enCours ? 'en_cours' : aVenir ? 'a_venir' : 'terminee' };
}

const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
const MOIS = ['', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
const RANGS = ['', 'premier', 'deuxième', 'troisième', 'quatrième', 'cinquième'];
const dateFr = (s: string) => versDate(s).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
const quantieme = (j: number) => (j === 1 ? '1er' : String(j));

/** La règle dite en clair, pour l'affichage. */
export function regleEnClair(r: Regle): string {
	switch (r.genre) {
		case 'consecutifs':
			// un seul jour (renouvellement d'une consécration) : pas de « 1 jours de suite »
			if (r.nombre === 1) return `le ${dateFr(r.debut)}`;
			return r.jourSemaine === null
				? `${r.nombre} jours de suite, à partir du ${dateFr(r.debut)}`
				: `${r.nombre} ${JOURS[r.jourSemaine]}s de suite, à partir du ${dateFr(r.debut)}`;
		case 'avant_fete':
			return r.jourSemaine === null
				? `les ${r.nombre} jours avant le ${quantieme(r.jour)} ${MOIS[r.mois]}`
				: `les ${r.nombre} ${JOURS[r.jourSemaine]}s avant le ${quantieme(r.jour)} ${MOIS[r.mois]}`;
		case 'fixe':
			return `chaque année, le ${quantieme(r.jour)} ${MOIS[r.mois]}`;
		case 'mensuel': {
			const base =
				r.decalage === -1
					? `la veille du ${RANGS[r.rang]} ${JOURS[r.jourSemaine]} du mois`
					: `le ${RANGS[r.rang]} ${JOURS[r.jourSemaine]} de chaque mois`;
			return r.nombre && r.debut
				? `${base}, ${r.nombre} mois de suite à partir de ${MOIS[versDate(r.debut).getMonth() + 1]} ${versDate(r.debut).getFullYear()}`
				: base;
		}
		case 'mois_entier':
			return `chaque jour du mois de ${MOIS[r.mois]}`;
		case 'hebdomadaire':
			return `chaque ${JOURS[r.jourSemaine]}`;
		case 'roue':
			return `un élément par ${r.unite}, depuis le premier dimanche de l’Avent`;
	}
}

/** Pour reprendre une série interrompue : la même règle, recommencée à partir d'aujourd'hui. */
export function recommencer(r: Regle, aujourdhui: string): Regle {
	if (r.genre === 'consecutifs') return { ...r, debut: aujourdhui };
	if (r.genre === 'mensuel' && r.nombre) return { ...r, debut: aujourdhui };
	if (r.genre === 'avant_fete') {
		// la série rattachée à une fête devient une série libre de même longueur
		return { genre: 'consecutifs', nombre: r.nombre, jourSemaine: r.jourSemaine, debut: aujourdhui };
	}
	return r;
}
