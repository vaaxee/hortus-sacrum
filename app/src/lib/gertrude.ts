/**
 * Prière de sainte Gertrude au saint du jour, selon sa catégorie (P. Denis, « Prières de sainte Gertrude », p. 234-242 ;
 * SPEC § 11) : martyr, confesseur, vierge et martyre, vierge ; à défaut, « Au Saint ou à la Sainte dont on célèbre la fête ».
 * Le « N... » de la prière reçoit le nom du saint, tiré de l'office du calendrier (« S. André, Apôtre » → « André »).
 */

export interface PriereDuSaint {
	id: string;
	/** Nom à mettre à la place de « N... » (vide si la prière n'en a pas, ou pour plusieurs saints). */
	nom: string;
}

/** « S. Pierre Chrysologue, Évêque, Confesseur et Docteur de l'Église » → { titres, nom, plusieurs } */
function analyser(office: string): { nom: string; titres: string; plusieurs: boolean } | null {
	const m = /^(SS\.|Stes|S\.|Ste|Bx|Bse)\s+([^,]+),\s*(.+)$/u.exec(office.trim());
	if (!m) return null;
	const plusieurs = m[1] === 'SS.' || m[1] === 'Stes' || /\bet\b/u.test(m[2]);
	return { nom: m[2].trim(), titres: m[3], plusieurs };
}

/** La prière de sainte Gertrude qui convient au saint de cet office, ou null (fête du Seigneur, de la sainte Vierge…). */
export function priereDuSaint(office: string, estFeteSanctorale: boolean): PriereDuSaint | null {
	if (!estFeteSanctorale) return null;
	const a = analyser(office);
	if (!a) return null;
	const t = a.titres;
	const generique = { id: 'gertrude:saint-du-jour', nom: '' };
	if (a.plusieurs) return generique;
	if (/Vierge et Martyre/u.test(t)) return { id: 'gertrude:a-une-vierge-et-martyre', nom: a.nom };
	if (/\bVierge\b/u.test(t)) return { id: 'gertrude:a-une-vierge', nom: a.nom };
	if (/Martyr\b/u.test(t)) return { id: 'gertrude:a-un-martyr', nom: a.nom };
	if (/Confesseur|Abbé/u.test(t)) return { id: 'gertrude:a-un-confesseur', nom: a.nom };
	return generique;
}

/** Met le nom du saint à la place de « N... » (ou « N. »). */
export function avecLeNom(corps: string, nom: string): string {
	return nom ? corps.replace(/\bN\.(?:\.\.|…)?/gu, nom) : corps;
}
