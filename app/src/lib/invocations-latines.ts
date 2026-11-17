/**
 * Invocations latines chantables, tirées de l'éloge latin du Martyrologe romain (SPEC § 10) :
 *   « Nicomedíæ pássio sanctæ Bárbaræ, Vírginis et Mártyris; quæ… »
 *   → « Sancta Bárbara, virgo et martyr Nicomedíæ, ora pro nobis peccatoribus. Amen. »
 * Les noms sont au génitif dans l'éloge : on les met au vocatif par des règles de déclinaison, les titres par une table.
 * Sans nom sûr, pas d'invocation (l'éloge reste affiché).
 */

const sansAccent = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/æ/g, 'ae').replace(/œ/g, 'oe');

/** Titres au génitif (singulier, puis pluriel) → forme d'invocation (vocatif singulier ; nominatif pluriel). */
const TITRES: Record<string, string> = {
	episcopi: 'episcope', martyris: 'martyr', confessoris: 'confessor', virginis: 'virgo', abbatis: 'abbas', diaconi: 'diacone',
	presbyteri: 'presbyter', papae: 'papa', pontificis: 'pontifex', doctoris: 'doctor', cardinalis: 'cardinalis', regis: 'rex',
	reginae: 'regina', viduae: 'vidua', monachi: 'monache', eremitae: 'eremita', apostoli: 'apostole', evangelistae: 'evangelista',
	levitae: 'levita', militis: 'miles', abbatissae: 'abbatissa', prophetae: 'propheta', sacerdotis: 'sacerdos', subdiaconi: 'subdiacone',
	lectoris: 'lector', exorcistae: 'exorcista', patriarchae: 'patriarcha', archiepiscopi: 'archiepiscope', anachoretae: 'anachoreta',
	matris: 'mater', pueri: 'puer', infantis: 'infans', poenitentis: 'pœnitens', imperatoris: 'imperator', imperatricis: 'imperatrix',
	martyrum: 'martyres', virginum: 'virgines', episcoporum: 'episcopi', confessorum: 'confessores', monachorum: 'monachi',
	presbyterorum: 'presbyteri', diaconorum: 'diaconi', militum: 'milites', fratrum: 'fratres', sororum: 'sorores', abbatum: 'abbates',
	pontificum: 'pontifices', tribuni: 'tribune', solitarii: 'solitarie', reclusi: 'recluse', apostolorum: 'apostoli', puerorum: 'pueri', virorum: 'viri', mulierum: 'mulieres', sociorum: 'socii'
};
/** Mots de liaison dans la liste des titres. */
const ET = new Set(['et', 'ac', 'atque']);
const ORNEMENTS = new Set(['ecclesiae']); // « Ecclésiæ Doctóris » → « Ecclesiæ doctor »

/** Génitif d'un nom propre → vocatif (singulier). */
export function vocatif(nom: string): string {
	const n = nom;
	const r = (de: RegExp, vers: string) => (de.test(n) ? n.replace(de, vers) : null);
	return (
		r(/ii$/u, 'i') ?? // Gregórii → Gregóri
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
	// lieu : ce qui précède le sujet, sans les mots d'office (pássio, natális…)
	const avant = eloge.slice(0, m.index + m[1].length).trim();
	const lieu = avant
		.split(/\s+/)
		.filter((w) => !/^(passio|natalis|depositio|inventio|ordinatio|item|elevatio|apud|eodem|die|pridie|eadem|ipso)$/.test(sansAccent(w).replace(/[.,;]/g, '')))
		.join(' ')
		.replace(/[,;]\s*$/, '')
		.trim();
	// lieu sûr seulement : court, sans relative, sans mot de fête (octave, dédicace, translation, vigile…)
	const fete = /octava|dedicatio|translatio|vigilia|commemoratio|ibidem|basilic/.test(sansAccent(lieu));
	const lieuSur = !fete && lieu.split(/\s+/).length <= 4 && !/\b(qu[aiæe]|est|sunt)\b/u.test(lieu) ? lieu : '';
	// segment du sujet : jusqu'à la première relative ou au premier point-virgule
	const debut = m.index + m[0].length;
	const segment = eloge.slice(debut).split(/[;:.(]|,\s*(?:qui|quæ|quod|cujus|quorum|quarum|ubi|sub|cum|in|a|ab|ex|apud|cognomento|cognoménto)\b|\s(?:quos|quas|quibus|quorum|quarum|qui|quæ)\b/iu)[0];
	const groupes = segment.split(/\s*,\s*|\s+(?:et|ac|atque)\s+/u).map((g) => g.trim()).filter(Boolean);
	const noms: string[] = [];
	const titres: string[] = [];
	let socii = false;
	let finNoms = false;
	for (const g of groupes) {
		const mots = g.split(/\s+/);
		const personne: string[] = [];
		let particule = false;
		for (const mot of mots) {
			const k = sansAccent(mot);
			if (k === 'sociorum' || k === 'aliorum' || k === 'sociarum' || k === 'aliarum') { socii = true; finNoms = true; break; }
			if (k === 'regis' && personne.length) { personne.push(mot); continue; } // « Joánnis-Francísci Regis » : nom, non titre
			if (TITRES[k]) {
				// au pluriel, les titres de chacun (« Diodóri Presbýteri ») ne qualifient pas le groupe
				if (!pluriel || /um$/.test(k)) { if (!titres.includes(TITRES[k])) titres.push(TITRES[k]); }
				if (noms.length && !pluriel) finNoms = true;
				continue;
			}
			if (ORNEMENTS.has(k)) { titres.push('Ecclesiæ'); continue; }
			if (personne.length && /^(de|a|ab)$/.test(k)) { particule = true; personne.push(mot); continue; }
			if (/^\p{Lu}/u.test(mot) && !/(orum|arum)$/.test(k)) {
				if (finNoms) break; // adjectif de lieu après un titre (« Epíscopi Ravennátis ») : laissé de côté
				personne.push(particule ? mot : vocatif(mot)); // après « a », « de » : le mot reste tel quel (« a Cruce »)
				continue;
			}
			if (personne.length) { if (!pluriel) finNoms = true; break; } // mot en minuscule : fin du nom
		}
		while (personne.length && /^(de|a|ab)$/i.test(personne[personne.length - 1])) personne.pop();
		if (personne.length && (!finNoms || !noms.length)) noms.push(personne.join(' '));
		if (!pluriel && noms.length) finNoms = true;
	}
	if (!noms.length) return null;
	const voc = noms;
	const plusieurs = pluriel || voc.length > 1 || socii;
	const tete = plusieurs ? (fem && voc.every((v) => /a$/.test(v)) ? (beat ? 'Beatæ' : 'Sanctæ') : beat ? 'Beati' : 'Sancti') : fem ? (beat ? 'Beata' : 'Sancta') : beat ? 'Beate' : 'Sancte';
	const liste = voc.length > 1 ? `${voc.slice(0, -1).join(', ')} et ${voc[voc.length - 1]}` : voc[0];
	// titres : « virgo et martyr », « episcope et confessor et Ecclesiæ doctor » ; au pluriel, nominatif pluriel
	const t = titres
		.map((x, i) => (x === 'Ecclesiæ' && titres[i + 1] ? `Ecclesiæ ${titres[i + 1]}` : titres[i - 1] === 'Ecclesiæ' ? '' : x))
		.filter(Boolean);
	const qualite = t.length ? `, ${t.join(' et ')}` : '';
	const ou = lieuSur ? ` ${lieuSur.replace(/^In\s/u, 'in ')}` : '';
	const fin = plusieurs ? 'orate pro nobis peccatoribus. Amen.' : 'ora pro nobis peccatoribus. Amen.';
	return { texte: `${tete} ${liste}${socii ? ' et socii' : ''}${qualite}${ou}, ${fin}`, pluriel: plusieurs };
}
