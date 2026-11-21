/**
 * Invocations latines chantables, tirées de l'éloge latin du Martyrologe romain (SPEC § 10) :
 *   « Nicomedíæ pássio sanctæ Bárbaræ, Vírginis et Mártyris; quæ… »
 *   → « Sancta Bárbara, virgo et martyr, ora pro nobis peccatoribus. Amen. »
 * Sans le lieu : il casserait le rythme du chant (demande du 17 nov.).
 * Les noms sont au génitif dans l'éloge : on les met au vocatif par des règles de déclinaison, les titres par une table.
 * Sans nom sûr, pas d'invocation (l'éloge reste affiché).
 */

const sansAccent = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/æ/g, 'ae').replace(/œ/g, 'oe');

/** Titres au génitif (singulier, puis pluriel) → forme d'invocation (vocatif singulier ; nominatif pluriel). */
const TITRES: Record<string, string> = {
	episcopi: 'episcope',
	martyris: 'martyr',
	confessoris: 'confessor',
	virginis: 'virgo',
	abbatis: 'abbas',
	diaconi: 'diacone',
	presbyteri: 'presbyter',
	papae: 'papa',
	pontificis: 'pontifex',
	doctoris: 'doctor',
	cardinalis: 'cardinalis',
	regis: 'rex',
	reginae: 'regina',
	viduae: 'vidua',
	monachi: 'monache',
	eremitae: 'eremita',
	apostoli: 'apostole',
	evangelistae: 'evangelista',
	levitae: 'levita',
	militis: 'miles',
	abbatissae: 'abbatissa',
	prophetae: 'propheta',
	sacerdotis: 'sacerdos',
	subdiaconi: 'subdiacone',
	lectoris: 'lector',
	exorcistae: 'exorcista',
	patriarchae: 'patriarcha',
	archiepiscopi: 'archiepiscope',
	anachoretae: 'anachoreta',
	matris: 'mater',
	pueri: 'puer',
	infantis: 'infans',
	poenitentis: 'pœnitens',
	imperatoris: 'imperator',
	imperatricis: 'imperatrix',
	martyrum: 'martyres',
	virginum: 'virgines',
	episcoporum: 'episcopi',
	confessorum: 'confessores',
	monachorum: 'monachi',
	presbyterorum: 'presbyteri',
	diaconorum: 'diaconi',
	militum: 'milites',
	fratrum: 'fratres',
	sororum: 'sorores',
	abbatum: 'abbates',
	pontificum: 'pontifices',
	tribuni: 'tribune',
	solitarii: 'solitarie',
	reclusi: 'recluse',
	apostolorum: 'apostoli',
	puerorum: 'pueri',
	virorum: 'viri',
	mulierum: 'mulieres',
	sociorum: 'socii',
	// ajoutés au contrôle de l'année (21 nov.) : titres et surnoms pris jusque-là pour des noms
	protomartyris: 'protomartyr',
	praecursoris: 'præcursor',
	archidiaconi: 'archidiacone',
	ducis: 'dux',
	comitis: 'comes',
	senatoris: 'senator',
	proconsulis: 'proconsul',
	principis: 'princeps',
	praesidis: 'præses',
	commentariensis: 'commentariensis',
	stylitae: 'stylita'
};
/** Nombres (« sanctórum trium Puerórum », « Septem Dormiéntium ») : jamais des noms. */
const NOMBRES = new Set([
	'trium',
	'duorum',
	'duarum',
	'quattuor',
	'quatuor',
	'quinque',
	'sex',
	'septem',
	'octo',
	'novem',
	'decem',
	'quadraginta'
]);
/** Adjectif de lieu ou de peuple : « Assisiénsis », « Nilópolis », « Thebánæ (legiónis) ». */
const LIEU = /(?:ensis|ensium|polis)$/;
const ADJECTIF_DEVANT_NOM = /(?:anae|ana|ani|anorum|inae|inorum)$/;
/** Noms communs qu'un adjectif de peuple qualifie (« Thebánæ legiónis », « Beneventánæ civitátis »). */
const COLLECTIFS = new Set([
	'legionis',
	'civitatis',
	'ecclesiae',
	'provinciae',
	'urbis',
	'gentis',
	'regionis',
	'oppidi',
	'coloniae',
	'dioecesis'
]);
/** Titres suivis d'un complément au génitif, jamais d'un autre saint (« Procónsulis Carthaginis », « Præcursóris Dómini »). */
const A_COMPLEMENT = new Set(['proconsulis', 'praecursoris', 'praesidis', 'principis', 'ducis', 'comitis']);
/** Titres qui sont aussi des noms de saints : en tête, sans nom avant eux, ce sont des noms (« sancti Senatóris Epíscopi »). */
const AUSSI_NOMS = new Set(['senatoris', 'sacerdotis']);
/** Invocations connues par un chant (le lieu y est, et fait partie de l'air) : nom au vocatif → invocation. */
const CHANTS: Record<string, string> = {
	Bárbara: 'Sancta Bárbara, virgo Nicomedíæ, ora pro nobis peccatoribus. Amen.'
};
/** Mots de liaison dans la liste des titres. */
const ET = new Set(['et', 'ac', 'atque']);
const ORNEMENTS = new Set(['ecclesiae']); // « Ecclésiæ Doctóris » → « Ecclesiæ doctor »

/** Génitif d'un nom propre → vocatif (singulier). */
export function vocatif(nom: string): string {
	const n = nom;
	const r = (de: RegExp, vers: string) => (de.test(n) ? n.replace(de, vers) : null);
	return (
		(n === 'Dei' ? n : null) ?? // « Dei Genitrix » : complément, reste au génitif
		r(/ii$/u, 'i') ?? // Gregórii → Gregóri
		r(/([aeiu])[eé]lis$/u, '$1el') ?? // Daniélis → Daniel ; Misaélis → Misael (noms hébreux en -el)
		r(/t[aá]tis$/u, 'tas') ?? // Felicitátis → Felicitas ; Caritátis → Caritas
		r(/cr[aá]tis$/u, 'crates') ?? // Sócratis → Sócrates
		r(/rd[oó]tis$/u, 'rdos') ?? // Sacerdótis → Sacérdos (le saint évêque de Limoges)
		r(/g[eé]nis$/u, 'genes') ?? // Hermógenis → Hermógenes
		r(/cl[ií]s$/u, 'cles') ?? // Themístoclis → Themístocles
		r(/(æ|ae)$/u, 'a') ?? // Bárbaræ → Bárbara ; Sabbæ → Sabba
		r(/nnis$/u, 'nnes') ?? // Joánnis → Joánnes
		r(/[oó]nis$/u, 'o') ?? // Annónis → Anno
		r(/(í|i)cis$/u, 'ix') ?? // Felícis → Felix
		r(/[eé]ntis$/u, 'ens') ?? // Cleméntis → Clemens
		r(/[aá]ntis$/u, 'ans') ??
		r(/[oó]ris$/u, 'or') ?? // Victóris → Victor
		r(/(é|e)tis$/u, 'es') ?? // Agnétis → Agnes
		r(/[aá]nis$/u, 'anes') ?? // Theóphanis → Theóphanes
		r(/i$/u, 'e') ?? // Petri → Petre ; Osmúndi → Osmúnde
		n
	);
}

export interface InvocationLatine {
	texte: string;
	pluriel: boolean;
	/** Les noms au vocatif, dans l'ordre de l'éloge (pour le contrôle avec l'invocation française). */
	noms: string[];
}

/** Invocation latine d'un éloge, ou null si le sujet n'est pas reconnu avec assez de sûreté. */
export function invocationLatine(eloge: string | null | undefined): InvocationLatine | null {
	if (!eloge) return null;
	const m = /(^|[\s,])(sanct(?:i|æ|ae|órum|orum|árum|arum)|beát(?:i|æ|ae|órum|árum)|beat(?:i|ae|orum|arum))\s/iu.exec(eloge);
	if (!m) return null;
	const sujet = sansAccent(m[2]);
	const pluriel = /orum|arum/.test(sujet);
	const fem = /ae$|arum$/.test(sujet);
	const beat = sujet.startsWith('beat');
	// segment du sujet : jusqu'à la première relative ou au premier point-virgule
	const debut = m.index + m[0].length;
	const segment = eloge
		.slice(debut)
		.split(
			/[;:.(]|,\s*(?:qui|quæ|quod|cujus|quorum|quarum|ubi|sub|cum|in|a|ab|ex|apud|cognomento|cognoménto)\b|\s(?:quos|quas|quibus|quorum|quarum|qui|quæ|sub|témpore|tempore|jubénte|imperánte)\b|\s(?=\p{Lu}\p{L}*\s+(?:imperánte|jubénte|Imperatóre|Prǽside|Príncipe)\b)|\s(?:a|ab)\s(?=Dómino|Deo|Christo)/iu
		)[0];
	const groupes = segment
		.split(/\s*,\s*|\s+(?:et|ac|atque)\s+/u)
		.map((g) => g.trim())
		.filter(Boolean);
	const noms: string[] = [];
	const titres: string[] = [];
	let socii = false;
	let finNoms = false;
	let arret = false;
	for (const g of groupes) {
		if (arret) break;
		const mots = g.split(/\s+/);
		// au singulier, un groupe qui commence en minuscule (« fíliæ Regis… ») ne parle plus du saint
		if (noms.length && !pluriel && /^\p{Ll}/u.test(mots[0]) && !TITRES[sansAccent(mots[0])]) break;
		// au singulier, un groupe de titres ne peut contenir, en plus, que des adjectifs de lieu (« Ravennátis ») ;
		// sinon il parle d'un autre (« Regis Hungarórum Andréæ fíliæ ») : on s'arrête
		if (
			noms.length &&
			!pluriel &&
			mots.some((w) => {
				const k = sansAccent(w);
				return !TITRES[k] && !ORNEMENTS.has(k) && !ET.has(k) && !/(atis|ensis|ensium|anus|ani|ini)$/.test(k);
			})
		)
			break;
		const personne: string[] = [];
		let particule = false;
		let apresTitre = false;
		let dernierTitre = '';
		for (const [i, mot] of mots.entries()) {
			const k = sansAccent(mot);
			if (NOMBRES.has(k)) continue;
			if (/^\p{Lu}/u.test(mot) && !TITRES[k]) {
				// après un premier nom seulement (« Castrénsis », « Christiána » sont aussi des noms de saints) :
				// « Assisiénsis », « Nilópolis » : un lieu ; « Thebánæ legiónis » : un adjectif devant un nom commun ;
				// après un titre au singulier (« Procónsulis Carthaginis », « Præcursóris Dómini ») : un complément
				const dejaNomme = noms.length > 0 || personne.length > 0;
				if (dejaNomme && LIEU.test(k)) continue;
				if (dejaNomme && apresTitre && A_COMPLEMENT.has(dernierTitre)) continue;
				const suivant = mots[i + 1];
				if (dejaNomme && ADJECTIF_DEVANT_NOM.test(k) && suivant && COLLECTIFS.has(sansAccent(suivant))) break;
			}
			const etaitTitre = apresTitre;
			apresTitre = !!TITRES[k];
			if (apresTitre) dernierTitre = k;
			if (k === 'sociorum' || k === 'aliorum' || k === 'sociarum' || k === 'aliarum') {
				socii = true;
				finNoms = true;
				break;
			}
			if (k === 'regis' && personne.length) {
				personne.push(mot);
				continue;
			} // « Joánnis-Francísci Regis » : nom, non titre
			if (TITRES[k] && !(AUSSI_NOMS.has(k) && !noms.length && !personne.length)) {
				// au pluriel, les titres de chacun (« Diodóri Presbýteri ») ne qualifient pas le groupe
				if (!pluriel || /um$/.test(k)) {
					if (!titres.includes(TITRES[k])) titres.push(TITRES[k]);
				}
				if (noms.length && !pluriel) finNoms = true;
				continue;
			}
			if (ORNEMENTS.has(k)) {
				titres.push('Ecclesiæ');
				continue;
			}
			if (personne.length && /^(de|a|ab)$/.test(k)) {
				particule = true;
				personne.push(mot);
				continue;
			}
			if (/^\p{Lu}/u.test(mot) && !/(orum|arum)$/.test(k)) {
				if (finNoms) {
					// adjectif de lieu juste après un titre (« Epíscopi Ravennátis ») : sauté ; autre personne (« Andréæ Regis ») : fin
					if (etaitTitre) continue;
					arret = true;
					break;
				}
				personne.push(particule ? mot : mot.split('-').map(vocatif).join('-')); // après « a », « de » : le mot reste tel quel (« a Cruce »)
				continue;
			}
			if (personne.length) {
				if (!pluriel) finNoms = true;
				break;
			} // mot en minuscule : fin du nom
		}
		while (personne.length && /^(de|a|ab)$/i.test(personne[personne.length - 1])) personne.pop();
		if (personne.length && (!finNoms || !noms.length)) noms.push(personne.join(' '));
		if (!pluriel && noms.length) finNoms = true;
	}
	if (!noms.length) return null;
	const voc = noms;
	const plusieurs = pluriel || voc.length > 1 || socii;
	const tete = plusieurs
		? fem
			? beat
				? 'Beatæ'
				: 'Sanctæ'
			: beat
				? 'Beati'
				: 'Sancti'
		: fem
			? beat
				? 'Beata'
				: 'Sancta'
			: beat
				? 'Beate'
				: 'Sancte';
	const liste = voc.length > 1 ? `${voc.slice(0, -1).join(', ')} et ${voc[voc.length - 1]}` : voc[0];
	// titres : « virgo et martyr », « episcope et confessor et Ecclesiæ doctor » ; au pluriel, nominatif pluriel
	const t = titres
		.map((x, i) => (x === 'Ecclesiæ' && titres[i + 1] ? `Ecclesiæ ${titres[i + 1]}` : titres[i - 1] === 'Ecclesiæ' ? '' : x))
		.filter(Boolean);
	const qualite = t.length ? `, ${t.join(' et ')}` : '';
	const fin = plusieurs ? 'orate pro nobis peccatoribus. Amen.' : 'ora pro nobis peccatoribus. Amen.';
	const chant = CHANTS[liste];
	if (chant && !plusieurs) return { texte: chant, pluriel: false, noms: voc };
	return { texte: `${tete} ${liste}${socii ? ' et socii' : ''}${qualite}, ${fin}`, pluriel: plusieurs, noms: voc };
}
