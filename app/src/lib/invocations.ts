/**
 * Invocations du micro-martyrologe (SPEC §5) : générées à partir du nom relevé
 * dans l'éloge du Martyrologe romain, au vouvoiement.
 *   « À Constantinople, saint Théophane et ses compagnons. » → « Saint Théophane et vos compagnons, priez pour nous. »
 * Sans nom reconnu avec certitude, on ne propose pas d'invocation : l'éloge reste affiché seul.
 */

const TITRES =
	'Martyrs?|Martyres?|Vierges?|Évêques?|Evêques?|Archevêques?|Confesseurs?|Papes?|Pontifes?|Prêtres?|Diacres?|Sous-Diacres?|Sous-diacres?|Abbés?|Abbesses?|Apôtres?|Évangélistes?|Docteurs?|Veuves?|Moines?|Ermites?|Anachorètes?|Lecteurs?|Exorcistes?|Acolytes?|Soldats?|Rois?|Reines?|Empereurs?|Impératrices?|Patriarches?|Prophètes?|Cardinal|Cardinaux|Pénitentes?|Solitaires?|Frères|Sœurs|Lévites?|Disciples?';
const RE_TITRE = new RegExp(`^(?:${TITRES})(?![\\p{L}])`, 'u');
const RANGS = 'reine|roi|pape|évêque|abbé|abbesse|prêtre|diacre|vieillard|martyrs?|frères|sœurs|vierges?|apôtres?|confesseurs?|prophètes?|patriarches?|pontifes?|soldats?|moines?|enfants?|ermites?|femmes?|hommes?|vieillards?|docteurs?|lévites?';

// un nom : un ou plusieurs mots à majuscule, avec particules (« Jean de la Croix », « Pie V », « Louis-Marie »)
const MOT = `\\p{Lu}[\\p{L}’'-]*`;
const NOM = `${MOT}(?:\\s+(?:(?:de la|de|du|des|d’|le|la|l’)\\s*)?${MOT}|\\s+(?:I{1,3}|IV|VI{0,3}|IX|X{1,3}|Ier|II?e))*`;
const RE_NOM = new RegExp(`^${NOM}$`, 'u');

const RE_SUJET = new RegExp(
	`(?:^|[\\s’'(])(saints?|saintes?|bienheureux|bienheureuses?|Saints?|Saintes?|Bienheureux|Bienheureuses?)\\s+((?:(?:${RANGS}|${TITRES}|très|glorieux|illustres?)\\s+)*)`,
	'u'
);
const RE_COMPAGNONS =
	/\b(?:et|avec)\s+(?:de\s+)?(?:ses|leurs)\s+compagn|et\s+[\p{L}\s-]{0,40}\bautres\b|avec\s+[\p{L}\s-]{0,40}\bautres\b|et\s+(?:ses|leurs)\s+(?:frères|fils|sœurs|disciples|enfants)/u;

export interface Invocation {
	texte: string;
	noms: string[];
}

function premierePhrase(t: string): string {
	const sans = t.replace(/\([^)]*\)/g, '');
	const m = sans.match(/^.*?[.;:](?=\s+\p{Lu}|\s*$)/u);
	return (m ? m[0] : sans).replace(/[.;:]\s*$/, '');
}

function liste(noms: string[]): string {
	if (noms.length <= 1) return noms.join('');
	return `${noms.slice(0, -1).join(', ')} et ${noms[noms.length - 1]}`;
}

/** Génère l'invocation d'une entrée du martyrologe, ou null si le nom n'est pas sûr. */
export function invocation(eloge: string): Invocation | null {
	const phrase = premierePhrase(eloge);
	const m = RE_SUJET.exec(phrase);
	if (!m) return null;
	const genre = m[1].toLowerCase();
	const pluriel = /s$/.test(genre) && genre !== 'bienheureux' ? true : false;
	const titresApres = m[2].trim();
	const suite = phrase.slice(m.index + m[0].length);

	// noms : jetons séparés par « , » et « et », en sautant les titres ; on s'arrête au premier jeton qui n'est ni l'un ni l'autre
	const noms: string[] = [];
	const jetons = suite.replace(/^\s*,\s*/, '').split(/\s*,\s*(?:et\s+)?|\s+et\s+/u);
	const RE_TETE = new RegExp(`^(${NOM})(?=\\s+\\p{Ll})`, 'u');
	let reste: string[] = [];
	for (let i = 0; i < jetons.length; i++) {
		// « François Xavier de la Compagnie de Jésus » → « François Xavier »
		const j = jetons[i].trim().replace(/\s+(?:de la|de l’|du|des|de)\s+(?:Compagnie|Ordre|Société|Congrégation|Tiers|Frères).*$/u, '');
		if (!j) continue;
		if (RE_TITRE.test(j)) continue;
		if (/^\p{Ll}+$/u.test(j)) continue; // apposition d'un mot : « soldat », « chantre »
		if (RE_NOM.test(j) && j.split(/\s+/).length <= 5) {
			noms.push(j);
			continue;
		}
		// « Marcellin encore enfant », « Julien avec cinq mille autres » : le nom en tête du jeton
		const tete = j.match(RE_TETE);
		if (tete) noms.push(tete[1]);
		reste = jetons.slice(i + 1);
		break;
	}
	// liste interrompue alors que d'autres noms suivent : on ne prétend pas les avoir tous
	const incomplet = pluriel && reste.some((x) => RE_NOM.test(x.trim()));
	const compagnons = RE_COMPAGNONS.test(suite) || incomplet || (pluriel && noms.length === 1);
	const multiple = noms.length > 1 || (pluriel && !noms.length);

	let tete: string;
	if (genre.startsWith('bienheureu')) {
		tete = genre === 'bienheureuse' ? 'Bienheureuse' : genre === 'bienheureuses' ? 'Bienheureuses' : 'Bienheureux';
	} else if (genre.startsWith('sainte')) {
		tete = multiple ? 'Saintes' : 'Sainte';
	} else {
		tete = multiple ? 'Saints' : 'Saint';
	}

	if (!noms.length) {
		// groupe anonyme : « les saints Martyrs, qui… » → « Saints Martyrs, priez pour nous. »
		const titre = `${titresApres} ${suite}`.trim().match(new RegExp(`^(?:${TITRES})`, 'u'));
		if (!pluriel || !titre) return null;
		return { texte: `${tete} ${titre[0]}, priez pour nous.`, noms: [] };
	}
	const suiteInv = compagnons ? ' et vos compagnons' : '';
	return { texte: `${tete} ${liste(noms)}${suiteInv}, priez pour nous.`, noms };
}

/** Formule finale des Litanies des saints (SPEC §5). */
export const TOUS_LES_SAINTS = 'Tous les saints et saintes de Dieu, intercédez pour nous.';

/**
 * Le nom latin tel qu'il est imprimé dans l'éloge du Martyrologe (cas et accents compris),
 * ex. « sanctæ Barbaræ Vírginis et Mártyris », « sanctórum Mártyrum Robustiáni et Marci ».
 * Rien n'est décliné ni transformé : on découpe seulement le passage qui nomme le saint.
 */
export function nomLatin(eloge: string | null | undefined): string | null {
	if (!eloge) return null;
	const m = /(?:^|[\s,])((?:[Ss]anct|[Bb]e[aá]t)\p{L}*)\s/u.exec(eloge);
	if (!m) return null;
	const debut = m.index + m[0].indexOf(m[1]);
	const suite = eloge.slice(debut).split(/[;:.(]|,\s*(?:qui|quæ|quod|cujus|quorum|quarum|ubi|sub|cum)\b/u)[0];
	const mots = suite.split(/\s+/);
	const garde: string[] = [mots[0]];
	let nomVu = false;
	const LIENS = /^(et|ac|atque|ejúsque|ejusque|item|de|a|ab)$/u;
	for (const brut of mots.slice(1)) {
		const mot = brut.replace(/,$/, '');
		if (!mot) continue;
		if (/^\p{Lu}/u.test(mot)) {
			nomVu = true;
			garde.push(brut);
		} else if (!nomVu || LIENS.test(mot)) {
			garde.push(brut); // nombres avant le nom (« trigínta septem ») et liaisons
		} else break;
	}
	while (garde.length > 1 && (LIENS.test(garde[garde.length - 1].replace(/,$/, '')) || /^\p{Ll}/u.test(garde[garde.length - 1]) && !nomVu)) garde.pop();
	const nom = garde.join(' ').replace(/,$/, '').trim();
	return nomVu ? nom : null;
}
