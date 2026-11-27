/**
 * Ce que vaut la journée calculée : durées (d'après les pages composées), avancement, indulgences de l'Enchiridion
 * de 1952, et jaculatoire d'ouverture. Fonctions pures.
 */
import { minutesDuTexte } from '../durees.ts';
import { fois, somme, valeurDuJour, type Fiche, type Indulgences, type Valeur } from '../indulgences.ts';
import { extraire, normaliser } from './texte.ts';
import type { Journee, Lecture, Ligne, SectionResolue } from './types.ts';

export type Corps = (id: string) => string | undefined;

/** Le texte réellement dit d'une section (extrait compris). */
export function contenuDe(s: SectionResolue, corps: Corps): string {
	const t = s.texte ? corps(s.texte) : undefined;
	return t ? (extraire(t, s.extrait, s.rang) ?? '') : '';
}

/** Nombre de récitations prévues d'une ligne (Angélus : trois). */
export const recitations = (l: Pick<Ligne, 'heures'>) => Math.max(1, l.heures?.length ?? 0);

/** Minutes d'une récitation : les prières dites, sans les notices ; les parties propres à une heure comptent à part. */
function minutesDes(sections: SectionResolue[], corps: Corps): number {
	return sections
		.filter((s) => s.genre === 'texte')
		.map((s) => contenuDe(s, corps))
		.reduce((a, t) => a + (t ? minutesDuTexte(t) : 0), 0);
}

/** Durée de la ligne pour la journée entière (minutes) ; la durée réglée à la main prime. */
export function minutesDeLaLigne(l: Ligne, corps: Corps): number {
	if (l.duree !== undefined) return l.duree * recitations(l);
	const communes = l.sections.filter((s) => !s.heure);
	const propres = l.sections.filter((s) => s.heure);
	return minutesDes(communes, corps) * recitations(l) + minutesDes(propres, corps);
}

/** Durée d'une seule récitation (affichée sur la ligne). */
export function minutesDUneRecitation(l: Ligne, corps: Corps): number {
	return minutesDeLaLigne(l, corps) / recitations(l);
}

// ------------------------------------------------------------------ indulgences

/** Une fiche ne compte que si elle cite l'Enchiridion de 1952 et, hors du français, a une traduction approuvée. */
export const ficheValable = (f: Fiche | undefined): f is Fiche =>
	!!f && /Ench\. 1952/.test(f.ref) && (f.langue === undefined || f.langue === 'français' || !!f.traduction);

/** Récitations de chaque texte : `faites` donne le nombre de récitations faites de chaque ligne. */
function compter(lignes: Ligne[], faites: (l: Ligne) => number): Map<string, number> {
	const n = new Map<string, number>();
	for (const l of lignes) {
		const k = Math.min(faites(l), recitations(l));
		if (!k) continue;
		const heures = l.heures ?? [];
		for (const s of l.sections) {
			// la suite d'un texte coupé dans une page composée n'est pas une récitation de plus
			if (s.genre !== 'texte' || !s.texte || s.suite) continue;
			// une partie propre à une heure n'est dite qu'à cette récitation-là
			const dites = s.heure ? (heures.indexOf(s.heure) < k ? 1 : 0) : k;
			n.set(s.texte, (n.get(s.texte) ?? 0) + dites);
		}
	}
	return n;
}

function valeur(n: Map<string, number>, ind: Indulgences, date: string, tempora?: string | null): Valeur {
	const vs: Valeur[] = [];
	// une concession « une fois le jour » ne se gagne qu'une fois, même portée par deux textes (deux neuvaines au
	// Sacré-Cœur les mêmes jours, Ench. 1952 n° 250) : comptée une fois par numéro de l'Enchiridion
	const unique = new Map<string, Valeur>();
	for (const [id, k] of n) {
		const f = ind.fiches[id];
		if (!ficheValable(f) || k <= 0) continue;
		if (f.frequence === 'chaque fois') vs.push(fois(valeurDuJour(f, date, tempora), k));
		else {
			const v = valeurDuJour(f, date, tempora);
			const deja = unique.get(f.ref);
			if (!deja || v.ans * 365 + v.jours > deja.ans * 365 + deja.jours) unique.set(f.ref, v);
		}
	}
	return somme([...vs, ...unique.values()]);
}

/** Indulgences partielles gagnées (lignes cochées, jaculatoires dites) et possibles (programme entier du jour). */
export function indulgencesDuJour(
	jr: Journee,
	faites: (l: Ligne) => number,
	jaculatoires: Map<string, number>,
	ind: Indulgences,
	tempora?: string | null
): { gagnees: Valeur; possibles: Valeur } {
	const gagnees = compter(jr.lignes, faites);
	for (const [id, k] of jaculatoires) gagnees.set(id, (gagnees.get(id) ?? 0) + k);
	return {
		gagnees: valeur(gagnees, ind, jr.date, tempora),
		possibles: valeur(compter(jr.lignes, recitations), ind, jr.date, tempora)
	};
}

// ------------------------------------------------------------------ jaculatoire d'ouverture

/** Jaculatoires permises à l'ouverture (décisions du 20 nov.) : fiche de l'Enchiridion de 1952, traduction approuvée. */
export function jaculatoiresPermises(ids: string[], ind: Indulgences | null, existe: (id: string) => boolean): string[] {
	return ids.filter((id) => existe(id) && ficheValable(ind?.fiches[id]));
}

/** Texte de toute la journée, réduit aux mots, pour écarter une jaculatoire déjà dite dans une page. */
export function texteDeLaJournee(pages: (Ligne | Lecture)[], corps: Corps): string {
	return ` ${pages.flatMap((p) => p.sections.map((s) => normaliser(contenuDe(s, corps)))).join(' ')} `;
}

/** Une jaculatoire au hasard, autre que la dernière montrée et absente des pages du jour. */
export function jaculatoireAOuvrir(
	permises: string[],
	corps: Corps,
	texteDuJour: string,
	derniere?: string,
	hasard: () => number = Math.random
): string | undefined {
	const libres = permises.filter((id) => {
		const n = normaliser(corps(id) ?? '');
		return n && !texteDuJour.includes(` ${n} `);
	});
	const choix = libres.length > 1 ? libres.filter((id) => id !== derniere) : libres;
	return choix.length ? choix[Math.floor(hasard() * choix.length)] : undefined;
}
