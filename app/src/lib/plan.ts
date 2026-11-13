/**
 * Plan de l'année → pratiques modifiables.
 * Lit les dévotions inscrites au calendrier (plan accepté ou proposé par le moteur)
 * et en fait des pratiques avec leur règle de dates, que l'utilisateur peut ensuite changer.
 */
import type { Jour } from './calendrier.ts';
import type { Pratique, Regle, Texte, TypePratique } from './types.ts';
import { SOURCE_VIDE } from './types.ts';

type Brut = Omit<Pratique, 'creeLe' | 'modifieLe'>;

const versDate = (s: string) => new Date(s + 'T12:00:00');
const iso = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const plus = (s: string, n: number) => {
	const d = versDate(s);
	d.setDate(d.getDate() + n);
	return iso(d);
};

/** Neuvaines dont la fête est à date fixe : (mois, jour) de la fête. Les autres suivent Pâques. */
const mobile = (titre: string) => /Saint-Esprit|Sacré-Cœur/.test(titre);

export function pratiquesDuPlan(annee: Jour[], textes: Texte[]): Brut[] {
	// les séries datées portent l'année liturgique dans leur identifiant ; les règles qui reviennent chaque année, non
	const an = annee.length ? annee[0].date.slice(0, 4) : '';
	// regroupe les libellés « Titre — n/N » ou « Titre — 3e jour »
	const groupes = new Map<string, { type: string; cle?: string; page: number | null; jours: { date: string; suite: string }[] }>();
	for (const j of annee) {
		for (const d of j.devotions) {
			let [titre, suite = ''] = d.libelle.split(' — ');
			if (d.cle === 'montfort') titre = d.libelle.startsWith('Consécration') ? 'Consécration à Jésus par Marie (renouvellement)' : 'Préparation à la consécration de Montfort';
			const g = groupes.get(titre) ?? { type: d.type, cle: d.cle, page: d.page_jardin, jours: [] };
			g.jours.push({ date: j.date, suite });
			groupes.set(titre, g);
		}
	}
	const parPage = (page: number | null) =>
		page === null ? [] : textes.filter((t) => t.origine === 'livret' && t.source.page === String(page) && !t.supprimeLe).map((t) => t.id).slice(0, 3);

	const out: Brut[] = [];
	for (const [titre, g] of groupes) {
		const premier = g.jours[0].date;
		const d0 = versDate(premier);
		let regle: Regle;
		let type: TypePratique = g.type === 'neuvaine' ? 'neuvaine' : 'jours_comptes';
		const compte = g.jours[0].suite.match(/^(\d+)\/(\d+)/);

		if (g.cle === 'montfort' && titre.startsWith('Préparation')) {
			type = 'consecration';
			regle = { genre: 'consecutifs', nombre: 33, jourSemaine: null, debut: premier };
		} else if (g.cle === 'montfort') {
			type = 'consecration';
			regle = { genre: 'consecutifs', nombre: 1, jourSemaine: null, debut: premier };
		} else if (g.type === 'neuvaine') {
			const fete = versDate(plus(premier, 9));
			regle = mobile(titre)
				? { genre: 'consecutifs', nombre: 9, jourSemaine: null, debut: premier }
				: { genre: 'avant_fete', nombre: 9, jourSemaine: null, mois: fete.getMonth() + 1, jour: fete.getDate() };
		} else if (g.cle === 'vendredi1' || g.cle === 'samedi1') {
			regle = { genre: 'mensuel', rang: 1, jourSemaine: d0.getDay(), nombre: g.cle === 'vendredi1' ? 9 : 5, debut: premier };
		} else if (g.cle === 'mercredi') {
			regle = { genre: 'mensuel', rang: 1, jourSemaine: 3 };
		} else if (g.cle === 'heure') {
			regle = { genre: 'mensuel', rang: 1, jourSemaine: 5, decalage: -1 };
		} else if (compte) {
			// série hebdomadaire comptée : on remonte au premier jour si l'année commence en cours de série
			const debut = plus(premier, -7 * (Number(compte[1]) - 1));
			regle = { genre: 'consecutifs', nombre: Number(compte[2]), jourSemaine: d0.getDay(), debut };
		} else {
			regle = { genre: 'fixe', mois: d0.getMonth() + 1, jour: d0.getDate() };
		}
		out.push({
			id: `plan:${regle.genre === 'consecutifs' || (regle.genre === 'mensuel' && regle.nombre) ? an + ':' : ''}${titre.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60)}`,
			origine: 'livret',
			titre: titre.replace(/^Premier (vendredi|samedi) du mois$/, (m, j) => (j === 'vendredi' ? 'Neuf premiers vendredis du mois' : 'Cinq premiers samedis du mois')),
			type,
			regle,
			textes: parPage(g.page),
			promesses: '',
			indulgence: '',
			source: { ...SOURCE_VIDE, edition: 'Le Jardin de l’âme (livret)', page: g.page ? String(g.page) : '' },
			notes: '',
			active: true
		});
	}
	return out;
}
