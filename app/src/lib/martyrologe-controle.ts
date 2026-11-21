/**
 * Contrôle des invocations du martyrologe (audit des consignes du 20 nov.) : pour chaque éloge, l'invocation française
 * (`invocations.ts`) et l'invocation latine chantée (`invocations-latines.ts`) doivent nommer les mêmes saints.
 * Quatre familles de défauts :
 *   - « nombre » : le français et le latin ne nomment pas autant de saints (18 nov. : « Saint Pierre » / « Sancti Petre
 *     et Paule », corrigé) ;
 *   - « vocatif » : un nom latin garde une désinence de génitif (« Olympíadis », « Apollináris ») ;
 *   - « decoupage » : un mot pris pour un nom n'en est pas un (20 nov. : « Thebána », de « Thebánæ legiónis », corrigé) :
 *     adjectif de lieu, persécuteur à l'ablatif (« Décio imperánte ») ;
 *   - « manque » : une seule des deux langues a son invocation.
 * Le contrôle ne corrige rien : il signale. `scripts/controle-martyrologe.mjs` écrit la liste de l'année.
 */
import { invocation } from './invocations.ts';
import { invocationLatine } from './invocations-latines.ts';

export interface Anomalie {
	genre: 'nombre' | 'vocatif' | 'decoupage' | 'manque';
	detail: string;
}

const sansAccent = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const COLLECTIFS = /^(?:legionis|civitatis|ecclesiae|provinciae|urbis|gentis|regionis|oppidi|coloniae|dioecesis)$/;
const PERSECUTEUR = /^(?:imperatore|praeside|principe|judice|imperante|jubente|regnante)$/;

export function controler(texte: string, texteLa: string | null | undefined): Anomalie[] {
	const out: Anomalie[] = [];
	if (!texteLa) return out;
	const fr = invocation(texte);
	const la = invocationLatine(texteLa);
	if (!fr && la) out.push({ genre: 'manque', detail: `pas d'invocation française ; latin : ${la.texte}` });
	if (fr && !la && fr.noms.length) out.push({ genre: 'manque', detail: `pas d'invocation latine ; français : ${fr.texte}` });
	if (!fr || !la) return out;
	if (fr.noms.length && la.noms.length !== fr.noms.length)
		out.push({ genre: 'nombre', detail: `${fr.noms.length} en français (${fr.texte}) / ${la.noms.length} en latin (${la.texte})` });
	// mots de l'éloge, sans accents, pour retrouver ce qui suit chaque nom
	const mots = sansAccent(texteLa)
		.replace(/[,;:.()]/g, ' ')
		.split(/\s+/)
		.filter(Boolean);
	for (const nom of la.noms) {
		for (const mot of nom.split(/[\s-]+/)) {
			const k = sansAccent(mot);
			if (/^(de|a|ab|dei)$/.test(k) || !/^\p{Lu}/u.test(mot)) continue;
			// génitif resté (« Nicoláe » est un vocatif juste : « -ae » n'est signalé que si l'éloge n'a pas « -ai »)
			if (/(is|orum|arum)$/.test(k) || (/ae$/.test(k) && !mots.includes(k.slice(0, -1) + 'i')))
				out.push({ genre: 'vocatif', detail: `« ${mot} » dans ${la.texte}` });
			if (/(ensis|ensium|polis)$/.test(k)) out.push({ genre: 'decoupage', detail: `« ${mot} » est un lieu : ${la.texte}` });
			const radical = k.slice(0, Math.max(3, k.length - 2));
			const i = mots.findIndex((w) => w.startsWith(radical));
			const suivant = i >= 0 ? mots[i + 1] : undefined;
			if (suivant && COLLECTIFS.test(suivant))
				out.push({ genre: 'decoupage', detail: `« ${mot} » est un adjectif (${suivant}) : ${la.texte}` });
			if (suivant && PERSECUTEUR.test(suivant))
				out.push({ genre: 'decoupage', detail: `« ${mot} » est le persécuteur (${suivant}) : ${la.texte}` });
		}
	}
	return out;
}
