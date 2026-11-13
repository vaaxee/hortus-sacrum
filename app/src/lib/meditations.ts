import type { Jour } from './calendrier.ts';

/** Une méditation ou une lecture d'un recueil ancien, rattachée à un jour par une clé. */
export interface EntreeRecueil {
	/** T:<temporal> (Adv1-0…), D:<MM-JJ> (date fixe), F:<fête mobile>, O:10-<n> (n-ième dimanche d'octobre). */
	cle: string | null;
	titre: string;
	tome: number;
	page: number;
	sommaire?: string;
	corps: string;
}

export interface Recueil {
	id: string;
	titre: string;
	auteur: string;
	editions: Record<string, string>;
	provenance: string;
	entrees: EntreeRecueil[];
}

const cache = new Map<string, Promise<Recueil | null>>();

export function chargerRecueil(id: string, fetchFn: typeof fetch = fetch): Promise<Recueil | null> {
	if (!cache.has(id)) {
		cache.set(id, fetchFn(`/data/recueils/${id}.json`).then((r) => (r.ok ? (r.json() as Promise<Recueil>) : null)).catch(() => null));
	}
	return cache.get(id)!;
}

/**
 * Clés à essayer pour un jour, de la plus propre à la plus générale :
 * fête mobile, dimanche d'octobre, date fixe, puis jour du temporal.
 */
export function clesDuJour(date: string, jour?: Pick<Jour, 'tempora'> | null): string[] {
	const d = new Date(date + 'T12:00:00');
	const md = date.slice(5);
	const cles: string[] = [];
	const t = jour?.tempora ?? null;
	if (t === 'Pent02-5') cles.push('F:sacre-coeur');
	if (d.getMonth() === 9 && d.getDay() === 0) cles.push(`O:10-${Math.ceil(d.getDate() / 7)}`);
	cles.push(`D:${md}`);
	if (t) cles.push(`T:${t}`);
	// 12 et 13 janvier, sans clé du temporal : semaine après le premier dimanche de l'Épiphanie
	else if (md === '01-12' || md === '01-13') cles.push(`T:Epi1-${d.getDay()}`);
	return cles;
}

/** Les méditations du recueil pour ce jour (plusieurs quand une fête en a plusieurs), dans l'ordre du livre. */
export function entreesDuJour(r: Recueil, date: string, jour?: Pick<Jour, 'tempora'> | null): EntreeRecueil[] {
	for (const c of clesDuJour(date, jour)) {
		const trouvees = r.entrees.filter((e) => e.cle === c);
		if (trouvees.length) return trouvees;
	}
	return [];
}
