/**
 * Couronnes : la trace sobre d'une quête achevée (série à jours comptés, mois entier, constance, lecture).
 * Tout est déduit de l'historique déjà enregistré et synchronisé (faits des pratiques, coches de la liste) :
 * rien à stocker, sinon les couronnes déjà montrées (meta locale « couronnes-vues »).
 * Un jour manqué n'est jamais rattrapé : la série recommence (décision du 14 nov.).
 */
import { MOIS_DEVOTION, NOMS_MOIS } from './calendrier.ts';
import { LIVRES } from './livres-bible.ts';
import { occurrences, versIso } from './pratiques.ts';
import type { Coche, ElementListe, Fait, Pratique } from './types.ts';

export type Genre = 'serie' | 'mois' | 'constance' | 'lecture';

export interface Couronne {
	/** Identité stable : sert à ne montrer la carte qu'une fois. */
	id: string;
	genre: Genre;
	/** Titre d'honneur, tiré de la tradition. */
	titre: string;
	/** La quête accomplie, dite en clair. */
	quete: string;
	date: string;
	/** Premier jour de la quête, quand elle s'étend sur plusieurs jours. */
	debut?: string;
	/** Verset de l'Écriture en exergue (référence Crampon, avec la Vulgate si elle diffère). */
	verset: string;
	/** Promesse ou grâce attachée à la pratique, avec sa source (pratique.promesses, ou fiche de l'Enchiridion). */
	promesse?: string;
	/** Combien de fois cette quête a été achevée, celle-ci comprise. */
	fois: number;
	pratiqueId?: string;
}

interface Modele { re: RegExp; titre: string; verset: string; grace?: string; /** la grâce ne vaut que pour une série de cette longueur */ pour?: number }

/**
 * Titres des séries à jours comptés (la première règle qui convient l'emporte). Les grâces citées sont celles que
 * l'Église a attachées à la pratique, avec leur référence ; une promesse inscrite dans la pratique passe avant.
 */
const SERIES: Modele[] = [
	{ re: /premiers samedis/i, titre: 'Enfant du Cœur Immaculé', verset: 'Jn 19, 27', pour: 5,
		grace: '« Vois mon Cœur entouré des épines qu’y enfoncent les hommes ingrats, par leurs blasphèmes et leurs ingratitudes. Toi, du moins, tâche de me consoler et dis que tous ceux qui, pendant cinq mois, le premier samedi, se confesseront, recevront la sainte communion, réciteront un chapelet, me tiendront compagnie pendant quinze minutes en méditant sur les quinze mystères du Rosaire, en esprit de réparation, je promets de les assister à l’heure de la mort, avec toutes les grâces nécessaires pour le salut de leur âme. » (Pontevedra, 10 décembre 1925 ; La Porte Latine, FSSPX, « La grande promesse des premiers samedis ».)' },
	{ re: /premiers samedis/i, titre: 'Enfant du Cœur Immaculé', verset: 'Jn 19, 27', pour: 8,
		grace: 'Pour qui fait les exercices de réparation huit premiers samedis de suite, une fois dans sa vie : indulgence plénière à l’article de la mort (S. C. du Saint-Office, 13 juin 1912 ; Ench. 1952, n° 367).' },
	{ re: /premiers vendredis/i, titre: 'Consolateur du Sacré-Cœur', verset: 'Ps 69, 21 | 68, 21', pour: 9,
		grace: 'Une pratique qui était familière à la V. M.-M., et que Notre Seigneur lui avait suggérée, en lui faisant espérer, pour ceux qui l’observeraient, la grâce de la pénitence finale et celle de recevoir les sacrements de l’Église avant de mourir, c’est de faire une neuvaine de communions à cette intention et pour honorer le cœur de Jésus-Christ, en plaçant chacune de ces communions à chaque premier vendredi du mois, pendant neuf mois de suite. (P. F.-X. Gautrelet, S. J., Le premier vendredi de chaque mois sanctifié par la dévotion au Sacré-Cœur de Jésus, Lyon-Paris, Périsse, 1855, p. 12.)' },
	{ re: /montfort|consécration/i, titre: 'Esclave d’amour de Jésus en Marie', verset: 'Jn 19, 27' },
	{ re: /douze samedis/i, titre: 'Couronne de douze étoiles', verset: 'Ap 12, 1' },
	{ re: /sept dimanches.*immacul/i, titre: 'Lis de l’Immaculée', verset: 'Ct 2, 2' },
	{ re: /sept dimanches.*joseph/i, titre: 'Familier de saint Joseph', verset: 'Mt 1, 24' },
	{ re: /sept dimanches/i, titre: 'Fidèle des sept dimanches', verset: 'Ex 20, 8' },
	{ re: /trentain/i, titre: 'Libérateur des âmes', verset: '2 M 12, 46' },
	{ re: /immacul/i, titre: 'Servant de l’Immaculée', verset: 'Ct 4, 7' },
	{ re: /sacré-c(œ|oe)ur/i, titre: 'Adorateur du Sacré-Cœur', verset: 'Mt 11, 29' },
	{ re: /noël/i, titre: 'Veilleur de Bethléem', verset: 'Lc 2, 15' },
	{ re: /assomption/i, titre: 'Cortège de l’Assomption', verset: 'Ct 8, 5' },
	{ re: /nativité de notre-dame|nativité de la/i, titre: 'Héraut de l’Aurore', verset: 'Ct 6, 10 | 6, 9' },
	{ re: /saint-esprit|pentecôte/i, titre: 'Temple de l’Esprit-Saint', verset: '1 Co 6, 19' },
	{ re: /rosaire|chapelet/i, titre: 'Rosiériste de Marie', verset: 'Lc 1, 28' },
	{ re: /toussaint|saints/i, titre: 'Concitoyen des saints', verset: 'Ep 2, 19' },
	{ re: /joseph/i, titre: 'Familier de saint Joseph', verset: 'Mt 1, 24' },
	{ re: /neuvaine/i, titre: 'Fidèle de la neuvaine', verset: 'Lc 18, 1' },
	{ re: /./, titre: 'Fidèle jusqu’au bout', verset: 'Mt 24, 13' }
];

/** Titre d'honneur de chaque mois entier, avec son verset. */
const MOIS: Record<number, [string, string]> = {
	1: ['Héraut du saint Nom', 'Ph 2, 10'],
	2: ['Hôte de Nazareth', 'Lc 2, 51'],
	3: ['Familier de saint Joseph', 'Mt 1, 24'],
	4: ['Adorateur du très saint Sacrement', 'Jn 6, 51 | 6, 51-52'],
	5: ['Fleur du mois de Marie', 'Ct 2, 12'],
	6: ['Disciple du Cœur de Jésus', 'Mt 11, 29'],
	7: ['Serviteur du Précieux Sang', '1 P 1, 18-19'],
	8: ['Enfant du Cœur Immaculé', 'Lc 2, 19'],
	9: ['Compagnon de Notre-Dame des Douleurs', 'Lc 2, 35'],
	10: ['Rosiériste de Marie', 'Lc 1, 28'],
	11: ['Ami des âmes du purgatoire', '2 M 12, 46'],
	12: ['Servant de l’Immaculée', 'Ct 4, 7']
};

/** Paliers de constance : jours de suite sans manquer une ligne quotidienne. */
const PALIERS: [number, string, string][] = [
	[40, 'Compagnon du désert', 'Mt 4, 1-2'],
	[365, 'Colonne du temple', 'Ap 3, 12']
];

const J = 86400000;
const midi = (s: string) => new Date(s + 'T12:00:00');
const lendemain = (s: string) => versIso(new Date(midi(s).getTime() + J));

/** Séries à jours comptés achevées sans manquer de jour. */
function deSeries(pratiques: Pratique[], faits: Fait[], aujourdhui: string): Couronne[] {
	const parPratique = new Map<string, Set<string>>();
	for (const f of faits) {
		if (!parPratique.has(f.pratiqueId)) parPratique.set(f.pratiqueId, new Set());
		parPratique.get(f.pratiqueId)!.add(f.date);
	}
	const out: Couronne[] = [];
	for (const p of pratiques) {
		const fait = parPratique.get(p.id);
		if (!fait?.size || p.type === 'roue') continue;
		const premier = [...fait].sort()[0];
		const occ = occurrences(p.regle, premier, aujourdhui).filter((o) => o.total > 1);
		const series: (typeof occ)[] = [];
		for (const o of occ) {
			if (o.rang === 1 || !series.length) series.push([]);
			series[series.length - 1].push(o);
		}
		const modeles = SERIES.filter((m) => m.re.test(p.titre));
		let n = 0;
		for (const s of series) {
			const modele = modeles.find((m) => !m.pour || m.pour === s.length) ?? { ...modeles[0], grace: undefined };
			const complete = s.length && s[0].rang === 1 && s.length === s[0].total && s.every((o) => fait.has(o.date));
			if (!complete || s[s.length - 1].date > aujourdhui) continue;
			n++;
			const date = s[s.length - 1].date;
			out.push({
				id: `serie:${p.id}:${s[0].date}`, genre: 'serie', titre: modele.titre, verset: modele.verset,
				quete: `${p.titre}, ${s.length} sur ${s.length}`, date, debut: s[0].date,
				promesse: p.promesses?.trim() || modele.grace, fois: n, pratiqueId: p.id
			});
		}
	}
	return out;
}

/** Jours où une ligne de la liste a été cochée. */
function joursCoches(coches: Coche[]): Map<string, Set<string>> {
	const m = new Map<string, Set<string>>();
	for (const c of coches) {
		if (!m.has(c.elementId)) m.set(c.elementId, new Set());
		m.get(c.elementId)!.add(c.date);
	}
	return m;
}

/** Mois entiers : la ligne « Dévotion du mois » cochée chaque jour d'un mois civil terminé. */
function deMois(liste: ElementListe[], parLigne: Map<string, Set<string>>, aujourdhui: string): Couronne[] {
	const out: Couronne[] = [];
	const lignes = liste.filter((e) => e.titre.startsWith('Dévotion du mois'));
	const parMois = new Map<string, number>();
	for (const e of lignes) {
		const jours = parLigne.get(e.id);
		if (!jours) continue;
		const mois = new Set([...jours].map((d) => d.slice(0, 7)));
		for (const m of [...mois].sort()) {
			const [an, mo] = m.split('-').map(Number);
			const n = new Date(an, mo, 0).getDate();
			const fin = `${m}-${String(n).padStart(2, '0')}`;
			if (fin >= aujourdhui) continue;
			let tous = true;
			for (let j = 1; j <= n && tous; j++) tous = jours.has(`${m}-${String(j).padStart(2, '0')}`);
			if (!tous) continue;
			const fois = (parMois.get(String(mo)) ?? 0) + 1;
			parMois.set(String(mo), fois);
			const [titre, verset] = MOIS[mo];
			out.push({
				id: `mois:${m}`, genre: 'mois', titre, verset, date: fin, fois, debut: `${m}-01`,
				quete: `${MOIS_DEVOTION[mo]?.nom ?? 'Dévotion du mois'} : chaque jour de ${NOMS_MOIS[mo].toLowerCase()} ${an}`
			});
		}
	}
	return out;
}

/** Constance : une ligne quotidienne cochée tant de jours de suite (chaque palier, une fois par suite). */
function deConstance(liste: ElementListe[], parLigne: Map<string, Set<string>>, aujourdhui: string): Couronne[] {
	const out: Couronne[] = [];
	for (const e of liste) {
		if (!e.jours.every(Boolean) || e.supprimeLe) continue;
		const jours = [...(parLigne.get(e.id) ?? [])].filter((d) => d <= aujourdhui).sort();
		if (jours.length < PALIERS[0][0]) continue;
		const fois = new Map<number, number>();
		let debut = jours[0], long = 1;
		const verifier = (d: string) => {
			for (const [palier, titre, verset] of PALIERS) {
				if (long !== palier) continue;
				const n = (fois.get(palier) ?? 0) + 1;
				fois.set(palier, n);
				out.push({ id: `constance:${e.id}:${palier}:${debut}`, genre: 'constance', titre, verset, date: d, fois: n,
					quete: `${e.titre}, ${palier} jours de suite`, debut });
			}
		};
		verifier(jours[0]);
		for (let i = 1; i < jours.length; i++) {
			if (jours[i] === lendemain(jours[i - 1])) long++;
			else { debut = jours[i]; long = 1; }
			verifier(jours[i]);
		}
	}
	return out;
}

/** Lectures : chaque Évangile lu en entier (coches « lecture:Mt 5 »), puis les quatre. */
const EVANGILES: [string, string, string][] = [
	['Mt', 'Disciple de saint Matthieu', 'Mt 28, 19-20'], ['Mc', 'Disciple de saint Marc', 'Mc 16, 15'],
	['Lc', 'Disciple de saint Luc', 'Lc 1, 3-4'], ['Jn', 'Disciple de saint Jean', 'Jn 20, 31']
];
function deLectures(coches: Coche[]): Couronne[] {
	const lu = new Map<string, string>();
	for (const c of coches) if (c.elementId.startsWith('lecture:')) {
		const k = c.elementId.slice(8);
		if (!lu.has(k) || c.date < lu.get(k)!) lu.set(k, c.date);
	}
	const out: Couronne[] = [];
	const fins: string[] = [];
	for (const [abr, titre, verset] of EVANGILES) {
		const n = LIVRES[abr]?.chapitres ?? 0;
		const dates = Array.from({ length: n }, (_, i) => lu.get(`${abr} ${i + 1}`));
		if (!n || dates.some((d) => !d)) continue;
		const date = (dates as string[]).sort().at(-1)!;
		fins.push(date);
		out.push({ id: `lecture:${abr}`, genre: 'lecture', titre, verset, date, fois: 1, quete: `${LIVRES[abr].nom} : les ${n} chapitres lus` });
	}
	if (fins.length === 4) {
		out.push({ id: 'lecture:evangiles', genre: 'lecture', titre: 'Héraut de l’Évangile', verset: 'Is 52, 7', date: fins.sort().at(-1)!, fois: 1,
			quete: 'Les quatre Évangiles lus en entier' });
	}
	return out;
}

export function couronnes(p: { pratiques: Pratique[]; faits: Fait[]; liste: ElementListe[]; coches: Coche[]; aujourdhui: string }): Couronne[] {
	const parLigne = joursCoches(p.coches.filter((c) => !c.elementId.startsWith('lecture:')));
	return [
		...deSeries(p.pratiques.filter((x) => !x.supprimeLe), p.faits, p.aujourdhui),
		...deMois(p.liste, parLigne, p.aujourdhui),
		...deConstance(p.liste, parLigne, p.aujourdhui),
		...deLectures(p.coches)
	].sort((a, b) => b.date.localeCompare(a.date));
}

/** Toutes les couronnes, d'après la base locale. */
export async function couronnesDeLaBase(aujourdhui: string): Promise<Couronne[]> {
	const { db } = await import('./db.ts');
	const [pratiques, faits, liste, coches] = await Promise.all([db.pratiques.toArray(), db.faits.toArray(), db.liste.toArray(), db.coches.toArray()]);
	return couronnes({ pratiques, faits, liste, coches, aujourdhui });
}

/** Couronnes déjà montrées (sur cet appareil). */
export async function vues(): Promise<Set<string>> {
	const { db } = await import('./db.ts');
	return new Set(((await db.meta.get('couronnes-vues'))?.valeur as string[] | undefined) ?? []);
}
export async function marquerVue(id: string): Promise<void> {
	const { db } = await import('./db.ts');
	const v = await vues();
	v.add(id);
	await db.meta.put({ cle: 'couronnes-vues', valeur: [...v] });
}
