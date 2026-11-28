import { describe, expect, it } from 'vitest';
import { appliquerReglages, journee } from './journee.ts';
import { vaut } from './quand.ts';
import { couper, extraire, fragments, partIncluse } from './texte.ts';
import type { Journee, Programme } from './types.ts';
import { CALENDRIER, corps, CYCLES, dimensions, PLAN, PROGRAMME, VOCABULAIRE } from './donnees-de-test.ts';

const jourDe = (date: string) => {
	const j = CALENDRIER.find((x) => x.date === date);
	if (!j) throw new Error(date);
	return j;
};
const calculer = (date: string, programme: Programme = PROGRAMME, extra = {}) =>
	journee(programme, { jour: jourDe(date), pratiques: PLAN, corps, ...extra });
const ligne = (jr: Journee, id: string) => jr.lignes.find((l) => l.id === id);
const textesDe = (jr: Journee, id: string) => (ligne(jr, id)?.sections ?? []).map((s) => s.texte);

describe('texte.ts', () => {
	const t = '## A\n\nun\n\n### 1° x\n\ndeux\n\n### 2° y\n\ntrois\n\n## B\n\nquatre';
	it('extrait une section jusqu’au titre de même niveau', () => {
		expect(extraire(t, { section: '### 1° x' })).toBe('### 1° x\n\ndeux');
		expect(extraire(t, { section: '## A' })).toBe('## A\n\nun\n\n### 1° x\n\ndeux\n\n### 2° y\n\ntrois');
		expect(extraire(t, { section: '## Z' })).toBeNull();
	});
	it('extrait le n-ième titre (jour de neuvaine) et retire des paragraphes', () => {
		expect(extraire(t, { rang_du_jour: { niveau: 3 } }, 2)).toBe('### 2° y\n\ntrois');
		expect(extraire(t, { rang_du_jour: { niveau: 3 } }, 3)).toBeNull();
		expect(extraire(t, { retirer: ['deux'] })).not.toContain('deux');
	});
	it('coupe après chaque partie et se recompose', () => {
		const m = couper(t, [{ point: 'p', apres_chaque: { niveau: 3, motif: '^\\d+° ' } }])!;
		expect(m.map((x) => x.points.length)).toEqual([1, 1, 0]);
		expect(m.map((x) => extraire(t, x.extrait)).join('\n\n')).toBe(t);
	});
	it('inclusion : le don de crainte est contenu dans le Cœur affligé de Marie', () => {
		const don = fragments(corps('beringer:don-crainte')!);
		expect(partIncluse(don, fragments(corps('beringer:coeur-afflige-de-marie')!))).toBeGreaterThan(0.5);
		expect(partIncluse(don, fragments(corps('paroissien:priere-du-soir')!))).toBe(0);
	});
});

describe('quand', () => {
	it('jours, mois, temps, office, ou, sauf', () => {
		const j = { date: '2027-03-27', temps: 'Temps de la Passion', office: 'Samedi saint' };
		expect(vaut({ jours_semaine: [6], mois: [3] }, j)).toBe(true);
		expect(vaut({ ou: [{ tempora: ['Temps pascal'] }, { office: '^Samedi saint$' }] }, j)).toBe(true);
		expect(vaut({ sauf: { jours_semaine: [6] } }, j)).toBe(false);
		expect(vaut({ dates: ['03-27'] }, j)).toBe(true);
		expect(vaut({ semaines_du_mois: [4] }, j)).toBe(true);
	});
	it('autour : jours comptés avant ou après une ancre (premier vendredi, jour du mois, fête fixe)', () => {
		const vendredi = { ancre: { rang: 1, jour_semaine: 5 }, de: -9, a: -1 };
		const jours = (q: Parameters<typeof vaut>[0], de: string, a: string) => {
			const out: string[] = [];
			for (let d = new Date(de + 'T12:00:00'); d <= new Date(a + 'T12:00:00'); d.setDate(d.getDate() + 1)) {
				const date = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
				if (vaut(q, { date })) out.push(date);
			}
			return out;
		};
		// premier vendredi le 1er janvier 2027 : la neuvaine passe d'une année à l'autre
		expect(jours({ autour: vendredi }, '2026-12-15', '2027-01-10')).toEqual([
			'2026-12-23',
			'2026-12-24',
			'2026-12-25',
			'2026-12-26',
			'2026-12-27',
			'2026-12-28',
			'2026-12-29',
			'2026-12-30',
			'2026-12-31'
		]);
		expect(jours({ autour: { ancre: { jour: 1 }, de: 0, a: 8 } }, '2027-02-25', '2027-03-12')[0]).toBe('2027-03-01');
		expect(jours({ autour: { ancre: { jour: 1 }, de: 0, a: 8 } }, '2027-02-25', '2027-03-12')).toHaveLength(9);
		// les cinq dimanches avant le 13 août 2027
		expect(jours({ jours_semaine: [0], autour: { ancre: '08-13', de: -35, a: -1 } }, '2027-06-01', '2027-09-01')).toEqual([
			'2027-07-11',
			'2027-07-18',
			'2027-07-25',
			'2027-08-01',
			'2027-08-08'
		]);
		// fête fixe au début de janvier : la fenêtre commence l'année civile d'avant
		expect(jours({ jours_semaine: [0], autour: { ancre: '01-06', de: -14, a: -1 } }, '2026-12-01', '2027-01-10')).toEqual([
			'2026-12-27',
			'2027-01-03'
		]);
	});
});

describe('journee()', () => {
	it('mercredi : une seule page pour le cordon, les Gloria sans les invocations', () => {
		const jr = calculer('2026-12-02');
		expect(ligne(jr, 'prog:cordon-gloria')).toBeUndefined();
		const gloria = ligne(jr, 'prog:devotion-mercredi')!.sections.find((s) => s.texte === 'hortus:cordon-sept-gloria')!;
		const texte = extraire(corps('hortus:cordon-sept-gloria')!, gloria.extrait)!;
		expect(texte).toContain('Gloire au Père');
		expect(texte).not.toContain('Joseph très chaste');
	});

	it('les autres jours : les Gloria avec leurs invocations', () => {
		expect(textesDe(calculer('2026-12-01'), 'prog:cordon-gloria')).toContain('hortus:cordon-sept-gloria');
	});

	it('chapelet du jour, avec l’invocation à la fin de chaque dizaine', () => {
		const jr = calculer('2026-12-03'); // jeudi : mystères joyeux
		const l = ligne(jr, 'prog:chapelet')!;
		expect(l.sousTitre).toBe('Mystères joyeux');
		expect(l.sections.some((s) => s.genre === 'editorial' && s.contenu === '## Le chapelet de saint Dominique')).toBe(true);
		expect(l.sections.filter((s) => s.origine === 'prog:fin-dizaine-o-marie')).toHaveLength(5);
		expect(l.invites).toContain('prog:fin-dizaine-o-marie');
	});

	it('Angélus : Flèche d’or à chaque fois, prière pour les agonisants à midi seulement', () => {
		const l = ligne(calculer('2026-12-01'), 'prog:angelus')!;
		expect(l.heures).toEqual(['06:00', '12:00', '18:00']);
		expect(l.sections.map((s) => s.texte)).toEqual(['paroissien:angelus', 'janvier:fleche-d-or', 'jardin:priere-pour-les-agonisants']);
		expect(l.sections[2].heure).toBe('12:00');
	});

	it('temps pascal : Regina cæli ; samedi saint : les deux', () => {
		expect(textesDe(calculer('2027-04-03'), 'prog:angelus').slice(0, 1)).toEqual(['beringer:regina-caeli']);
		expect(textesDe(calculer('2027-03-27'), 'prog:angelus').slice(0, 2)).toEqual(['paroissien:angelus', 'beringer:regina-caeli']);
	});

	it('prière du matin : Salve après l’invocation à la Vierge, Crux ave et agonisants à la fin', () => {
		const s = (ligne(calculer('2026-12-01'), 'prog:priere-du-matin')?.sections ?? [])
			.filter((x) => x.genre !== 'editorial' && x.genre !== 'partie')
			.map((x) => x.texte);
		expect(s).toEqual([
			'paroissien:priere-du-matin',
			// décision du 26 nov. : l'oraison de Prime à la place du paragraphe d'offrande du Paroissien
			'thesaurisons:oraison-de-prime',
			'paroissien:priere-du-matin',
			'beringer:salve-regina',
			'paroissien:priere-du-matin',
			// l'offrande, composée à l'affichage, chacun sous son titre ; depuis le 26 nov., des textes indulgenciés ou
			// prescrits à la place de l'intention d'indulgences, de l'acte de soumission et de la recommandation du livret
			'desgenettes:acte-d-offrande-pour-les-indulgences',
			'thesaurisons:suscipe',
			'jardin:acte-d-intention-de-communion-spirituelle-perpetuelle',
			'ench1952:entre-vos-mains-saint-edmond',
			'jardin:devoir-envers-l-eglise-et-ses-ministres',
			'jardin:devoir-envers-la-famille',
			'jardin:devoir-envers-la-patrie',
			'jardin:devoir-envers-les-pauvres-les-persecutes-les-affliges',
			'jardin:devoir-envers-moi-meme',
			undefined, // champ des intentions
			'jahenny:scapulaire-benediction-protection',
			'jardin:priere-pour-les-agonisants',
			// du 1er au 9 du mois : l'offrande de la neuvaine de réparation (Beringer n° 671)
			'beringer:neuvaine-reparation-sacre-coeur'
		]);
	});

	it('samedi : pas de don séparé (il est dans le Cœur affligé) ; une seule litanie', () => {
		const jr = calculer('2026-12-12');
		expect(jr.textes.has('beringer:don-crainte')).toBe(false);
		expect(textesDe(jr, 'prog:devotion-samedi')).toContain('beringer:coeur-afflige-de-marie');
		expect(textesDe(jr, 'prog:devotion-samedi').filter((t) => t?.includes('litanies'))).toHaveLength(1);
	});

	it('septembre : les sept Douleurs chaque jour, sans don ni Cœur affligé', () => {
		const jr = calculer('2027-09-04');
		expect(ligne(jr, 'prog:sept-douleurs-septembre')).toBeDefined();
		expect(jr.textes.has('beringer:coeur-afflige-de-marie')).toBe(false);
		expect([...jr.textes.keys()].some((t) => t.startsWith('beringer:don-'))).toBe(false);
	});

	it('premier samedi : le chapelet est annoté, sans ligne de plus', () => {
		const jr = calculer('2026-12-05');
		expect(
			ligne(jr, 'prog:chapelet')!
				.annotations.map((a) => a.texte)
				.join(' ')
		).toMatch(/premiers samedis/i);
		expect(jr.lignes.some((l) => l.id.startsWith('plan:') && /samedi/i.test(l.titre))).toBe(false);
	});

	it('neuvaine de Noël : la partie du jour seulement, avec le compteur', () => {
		const l = calculer('2026-12-18').lignes.find((x) => x.id.endsWith('neuvaine-de-noel'))!;
		expect(l.titre).toMatch(/3\/9/);
		const s = l.sections[0];
		expect(extraire(corps(s.texte!)!, s.extrait, s.rang)).toMatch(/^### Troisième jour/);
	});

	it('une pratique du plan déjà dite dans la journée annote la ligne qui la porte', () => {
		// neuvaine à saint Michel (20-28 sept.) un mardi : le chapelet de saint Michel est déjà dans la dévotion du mardi
		const jr = calculer('2027-09-21');
		expect(jr.fusions.some((f) => f.texte === 'jardin:chapelet-de-saint-michel-archange' && f.vers === 'prog:devotion-mardi')).toBe(true);
		expect(
			ligne(jr, 'prog:devotion-mardi')!
				.annotations.map((a) => a.texte)
				.join()
		).toMatch(/Michel/);
	});

	it('prière de sainte Gertrude à la fin de l’office du saint, avec son nom', () => {
		const jr = calculer('2026-12-03'); // S. François Xavier, Confesseur
		const s = jr.lectures.find((l) => l.id === 'lec:saint')!.sections[0];
		expect(s.texte).toBe('gertrude:a-un-confesseur');
		expect(s.nom).toBe('François-Xavier');
	});

	it('un invité dont l’hôte est désactivé devient une ligne à part', () => {
		const jr = calculer('2026-12-01', PROGRAMME, { reglages: [{ id: 'prog:angelus', actif: false }] });
		expect(ligne(jr, 'prog:angelus')).toBeUndefined();
		expect(textesDe(jr, 'prog:fleche-d-or')).toEqual(['janvier:fleche-d-or']);
	});

	it('un ajout personnel passe par la garde : un texte déjà dit est retiré et signalé', () => {
		const perso = {
			id: 'perso:1',
			titre: 'Mes litanies',
			revision: 1,
			source: 'ajout personnel',
			page: { moment: 'soir' as const, ordre: 95, sections: [{ texte: 'beringer:sub-tuum' }] }
		};
		const jr = calculer('2026-12-01', PROGRAMME, { reglages: [{ id: 'perso:1', entree: perso }] });
		expect(jr.conflits).toEqual([{ texte: 'beringer:sub-tuum', garde: 'prog:priere-du-soir', retire: 'perso:1' }]);
	});

	it('la liste d’avant la refonte aurait été refusée (doublons du mercredi et du samedi)', () => {
		const ancien: Programme = {
			...PROGRAMME,
			entrees: [
				...PROGRAMME.entrees,
				{
					id: 'x:devotion-mercredi',
					titre: 'ancienne',
					revision: 1,
					source: 'test',
					page: { moment: 'journee', ordre: 1, sections: [{ texte: 'beringer:saint-joseph-purete' }] }
				}
			]
		};
		expect(calculer('2026-12-02', ancien).conflits.map((c) => c.texte)).toEqual(['beringer:saint-joseph-purete']);
	});

	it('les réglages : ordre et durée changés, entrée livrée désactivée', () => {
		const e = appliquerReglages(PROGRAMME.entrees, [
			{ id: 'prog:chapelet', ordre: 5, duree: 25, modifieLe: '' },
			{ id: 'prog:brigitte', actif: false, modifieLe: '' }
		]);
		expect(e.find((x) => x.id === 'prog:chapelet')).toMatchObject({ duree: 25, page: { ordre: 5 } });
		expect(e.some((x) => x.id === 'prog:brigitte')).toBe(false);
	});

	it('textes à fournir du jour', () => {
		expect(
			calculer('2027-03-03')
				.a_fournir.map((a) => a.quoi)
				.join()
		).toMatch(/Chemin de croix/);
	});
});

describe('contexte dévotionnel et couverture (lot « Dimensions »)', () => {
	const avec = (date: string) => calculer(date, PROGRAMME, { cycles: CYCLES, dimensions, vocabulaire: VOCABULAIRE });

	it('vendredi → Passion, avec sa source ; couverte par la dévotion du vendredi', () => {
		const jr = avec('2026-12-04');
		expect(jr.contexte.objets).toContain('passion');
		expect(jr.contexte.sources).toContainEqual({ dimension: 'objet', valeur: 'passion', de: 'vendredi' });
		expect(jr.couverture.objet.find((c) => c.valeur === 'passion')?.par).toContain('prog:devotion-vendredi');
	});

	it('juillet → Précieux Sang ; Carême → réparation ; temps pascal → action de grâces', () => {
		expect(avec('2027-07-09').contexte.sources).toContainEqual({ dimension: 'objet', valeur: 'precieux-sang', de: 'mois de juillet' });
		expect(avec('2027-03-03').contexte.fins).toEqual(['reparation']);
		expect(avec('2027-04-06').contexte.fins).toEqual(['action-de-graces']);
		expect(avec('2026-12-02').contexte.fins).toEqual([]); // le thème de la semaine du mois n'est pas adopté
	});

	it('fête du sanctoral : le saint est noté ; fête de la Vierge : objet ajouté', () => {
		expect(avec('2026-12-03').contexte.sanctoral).toMatch(/François-Xavier/);
		expect(avec('2026-12-08').contexte.objets).toContain('sainte-vierge');
	});

	it('manques : les valeurs non couvertes, les fins principales marquées requises', () => {
		const jr = avec('2026-12-01');
		const couvertes = new Set(jr.couverture.fin.map((c) => c.valeur));
		for (const m of jr.manques) expect(couvertes.has(m.valeur) && m.dimension === 'fin').toBe(false);
		for (const m of jr.manques.filter((x) => x.dimension === 'fin' && VOCABULAIRE.fins_principales.includes(x.valeur)))
			expect(m.requis).toBe(true);
	});

	it('sans cycles ni dimensions : contexte vide, mêmes lignes', () => {
		const a = calculer('2026-12-04');
		expect(a.contexte.objets).toEqual([]);
		expect(a.lignes).toEqual(avec('2026-12-04').lignes);
	});
});

describe('prières de sainte Gertrude dans la dévotion du jour (demande du 22 nov.)', () => {
	const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
	it('une seule par jour, du thème du jour, et toutes reviennent au fil des semaines', () => {
		const vues = new Map<string, Set<string>>();
		for (const j of CALENDRIER) {
			const k = new Date(j.date + 'T12:00:00').getDay();
			const l = ligne(calculer(j.date), `prog:devotion-${JOURS[k]}`);
			if (!l) continue;
			const g = l.sections.filter((s) => s.texte?.startsWith('gertrude:'));
			expect(g, j.date).toHaveLength(1);
			if (!vues.has(JOURS[k])) vues.set(JOURS[k], new Set());
			vues.get(JOURS[k])!.add(g[0].texte!);
		}
		expect([...vues.values()].map((v) => v.size)).toEqual([3, 2, 4, 2, 1, 9, 6]);
		expect(vues.get('vendredi')).toContain('gertrude:salut-plaies');
		expect(vues.get('samedi')).toContain('gertrude:salutation-d-or');
	});
});

describe('archiconfréries intégrées (décisions du 22 nov.)', () => {
	const textes = (date: string, id: string) => (ligne(calculer(date), id)?.sections ?? []).map((s) => s.texte);
	it('âmes du purgatoire : la prière du jour chaque soir, sauf le lundi', () => {
		expect(textes('2026-12-01', 'prog:priere-du-soir')).toContain('beringer:ames-purgatoire-mardi');
		expect(textes('2026-11-30', 'prog:priere-du-soir').some((t) => t?.startsWith('beringer:ames-purgatoire'))).toBe(false);
	});
	it('premier vendredi : prière réparatrice et rénovation de la Garde d’honneur', () => {
		expect(textes('2026-12-04', 'prog:devotion-vendredi')).toEqual(
			expect.arrayContaining(['garde1886:priere-reparatrice', 'garde1886:renovation-enrolement'])
		);
		expect(textes('2026-12-11', 'prog:devotion-vendredi')).not.toContain('garde1886:priere-reparatrice');
	});
	it('août : la louange du jour (Desgenettes) dans la dévotion du jour', () => {
		const l = ligne(calculer('2027-08-03'), 'prog:devotion-mardi');
		expect(l?.sections.find((s) => s.texte === 'desgenettes:louanges-de-la-semaine')?.extrait?.section).toBe('## Le mardi.');
		expect(textes('2027-07-06', 'prog:devotion-mardi')).not.toContain('desgenettes:louanges-de-la-semaine');
	});
	it('février et fête de la Sainte Famille ; consécrations le jour de leur fête', () => {
		expect(textes('2027-02-03', 'prog:priere-du-soir')).toContain('beringer:a-la-sainte-famille');
		expect(textes('2027-01-10', 'prog:priere-du-soir')).toContain('beringer:a-la-sainte-famille');
		expect(textes('2027-06-04', 'prog:priere-du-matin')).toContain('garde1886:consecration-coeur-de-jesus');
		expect(textes('2027-08-22', 'prog:priere-du-matin')).toContain('desgenettes:oraison-consecration-coeur-de-marie');
		expect(textes('2027-02-09', 'prog:priere-du-matin')).toContain('janvier:consecration-archiconfrerie');
		expect(textes('2027-02-10', 'prog:priere-du-matin')).not.toContain('janvier:consecration-archiconfrerie');
	});
});

describe('neuvaine à la très sainte Trinité (demande du 26 nov.)', () => {
	const ID = 'prog:neuvaine-trinite';
	const ORDINAUX = ['Premier', 'Deuxième', 'Troisième', 'Quatrième', 'Cinquième', 'Sixième', 'Septième', 'Huitième', 'Neuvième'];
	const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
	it('tombe sur neuf jours, du samedi vigile de la Pentecôte au dimanche de la Trinité', () => {
		expect(jours).toEqual([
			'2027-05-15',
			'2027-05-16',
			'2027-05-17',
			'2027-05-18',
			'2027-05-19',
			'2027-05-20',
			'2027-05-21',
			'2027-05-22',
			'2027-05-23'
		]);
		expect(jourDe('2027-05-15').office).toBe('Vigile de la Pentecôte');
		expect(jourDe('2027-05-23').office).toBe('Très Sainte Trinité');
	});
	it('chaque date porte son jour de la neuvaine ; la consécration de dom Marmion le jour de la Trinité seulement', () => {
		jours.forEach((date, k) => {
			const sections = ligne(calculer(date), ID)!.sections;
			const titres = sections.filter((s) => s.genre === 'editorial').map((s) => s.contenu);
			expect(titres, date).toEqual([expect.stringMatching(new RegExp(`^### ${ORDINAUX[k]} jour de la neuvaine`))]);
			const textes = sections.map((s) => s.texte);
			expect(textes, date).toEqual(
				expect.arrayContaining([
					'beringer:trinite-adoration-action-de-graces',
					'beringer:trinite-trois-offrandes',
					'beringer:trinite-toute-puissance'
				])
			);
			expect(textes.includes('thibaut:marmion-consecration-trinite'), date).toBe(k === 8);
		});
	});
});

const ORDINAUX = ['Premier', 'Deuxième', 'Troisième', 'Quatrième', 'Cinquième', 'Sixième', 'Septième', 'Huitième', 'Neuvième'];
const iso = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
/** Les n jours qui précèdent une date (AAAA-MM-JJ), dans l'ordre. */
const joursAvant = (date: string, n: number) =>
	Array.from({ length: n }, (_, k) => {
		const d = new Date(date + 'T12:00:00');
		d.setDate(d.getDate() - n + k);
		return iso(d);
	});

describe('neuvaine au Sacré-Cœur avant le premier vendredi (Petit bréviaire, demande du 26 nov.)', () => {
	const ID = 'prog:neuvaine-premier-vendredi';
	const premiersVendredis = CALENDRIER.filter((j) => {
		const d = new Date(j.date + 'T12:00:00');
		return d.getDay() === 5 && d.getDate() <= 7;
	}).map((j) => j.date);
	const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
	it('les neuf jours qui finissent le jeudi, veille de chaque premier vendredi de 2026-2027', () => {
		expect(premiersVendredis).toHaveLength(12);
		const fin = CALENDRIER[CALENDRIER.length - 1].date;
		const attendus = [...premiersVendredis, '2027-12-03']
			.flatMap((v) => joursAvant(v, 9))
			.filter((d) => d >= CALENDRIER[0].date && d <= fin);
		expect(jours).toEqual(attendus);
		expect(jours.slice(0, 5)).toEqual(['2026-11-29', '2026-11-30', '2026-12-01', '2026-12-02', '2026-12-03']);
		expect(jours.slice(-4)).toEqual(['2027-11-24', '2027-11-25', '2027-11-26', '2027-11-27']);
	});
	it('chaque date porte son jour ; amende honorable et consécration le neuvième jour seulement', () => {
		for (const v of premiersVendredis.slice(1)) {
			joursAvant(v, 9).forEach((date, k) => {
				const sections = ligne(calculer(date), ID)!.sections;
				const titres = sections.filter((s) => s.genre === 'editorial').map((s) => s.contenu);
				expect(titres[0], date).toMatch(new RegExp(`^### ${ORDINAUX[k]} jour de la neuvaine`));
				const textes = sections.filter((s) => s.genre === 'texte');
				expect(textes[0].texte, date).toBe('breviaire-sc:neuvaine');
				expect(
					textes.slice(1).map((s) => s.extrait?.section),
					date
				).toEqual(k === 8 ? ['## ∗ Amende honorable au Sacré-Cœur', '## ∗ Consécration au Sacré-Cœur de Jésus'] : []);
				expect(new Date(date + 'T12:00:00').getDay() === 4 || k < 8, date).toBe(true);
			});
		}
	});
});

describe('neuvaine de la sainte Face (Janvier 1895), avant la fête de saint Pierre', () => {
	const ID = 'prog:neuvaine-sainte-face';
	const ROMAINS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'];
	it('du 20 au 28 juin, chaque jour sa méditation, l’ouverture et les prières du premier jour', () => {
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
		expect(jours).toEqual(joursAvant('2027-06-29', 9));
		jours.forEach((date, k) => {
			const s = ligne(calculer(date), ID)!.sections.filter((x) => x.genre === 'texte');
			const jourDuLivre = s.filter((x) => x.extrait?.section?.startsWith('## ')).map((x) => x.extrait!.section);
			expect(jourDuLivre, date).toEqual([expect.stringMatching(new RegExp(`^## ${ROMAINS[k]}e?r? jour\\. `))]);
			expect(
				s.some((x) => x.extrait?.de === 'Seigneur, je veux rechercher votre Face'),
				date
			).toBe(k > 0);
			expect(
				s.some((x) => x.extrait?.section === '### Prières'),
				date
			).toBe(k > 0 && k < 8);
			for (const x of s) expect(extraire(corps(x.texte!)!, x.extrait), date).not.toContain('Voir le Ier jour');
		});
	});
});

describe('dimanches de saint Jean Berchmans et de saint Stanislas Kostka (Jardin de l’âme)', () => {
	const dimanches = (id: string) => CALENDRIER.filter((j) => ligne(calculer(j.date), id)).map((j) => j.date);
	const titre = (date: string, id: string) => ligne(calculer(date), id)!.sections.find((s) => s.genre === 'editorial')?.contenu;
	it('les cinq dimanches avant le 13 août 2027, chacun son rang', () => {
		const d = dimanches('prog:cinq-dimanches-berchmans');
		expect(d).toEqual(['2027-07-11', '2027-07-18', '2027-07-25', '2027-08-01', '2027-08-08']);
		expect(d.map((x) => titre(x, 'prog:cinq-dimanches-berchmans'))).toEqual([
			'### Premier dimanche',
			'### Deuxième dimanche',
			'### Troisième dimanche',
			'### Quatrième dimanche',
			'### Cinquième et dernier dimanche'
		]);
	});
	it('les dix dimanches avant le 13 novembre 2027', () => {
		const d = dimanches('prog:dix-dimanches-stanislas');
		expect(d).toHaveLength(10);
		expect(d[0]).toBe('2027-09-05');
		expect(d[9]).toBe('2027-11-07');
		expect(d.every((x) => new Date(x + 'T12:00:00').getDay() === 0)).toBe(true);
		expect(titre(d[0], 'prog:dix-dimanches-stanislas')).toBe('### Premier dimanche');
		expect(titre(d[9], 'prog:dix-dimanches-stanislas')).toBe('### Dixième et dernier dimanche');
	});
});

describe('neuvaine à saint François d’Assise (Québec 1867), du 25 septembre au 3 octobre', () => {
	const ID = 'prog:neuvaine-saint-francois';
	it('chaque jour : l’hymne, la vertu du jour sans les renvois, le répons de la fin', () => {
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
		expect(jours).toEqual(joursAvant('2027-10-04', 9));
		jours.forEach((date, k) => {
			const s = ligne(calculer(date), ID)!.sections.filter((x) => x.genre === 'texte');
			expect(
				s.map((x) => x.extrait?.section?.split('.')[0]),
				date
			).toEqual(['## Au commencement de chaque exercice', `## ${k + 1}${k ? 'e' : 'er'} jour`, '## A la fin de chaque exercice']);
			for (const x of s) {
				const t = extraire(corps(x.texte!)!, x.extrait)!;
				expect(t, date).toBeTruthy();
				expect(t, date).not.toMatch(/page 3[79]\./);
			}
		});
	});
});

describe('neuvaine pour la fête de saint Joseph (Confrérie de Montréal), du 10 au 18 mars', () => {
	const ID = 'prog:neuvaine-saint-joseph-montreal';
	const ORD = ['Premier', 'Deuxième', 'Troisième', 'Quatrième', 'Cinquième', 'Sixième', 'Septième', 'Huitième', 'Neuvième'];
	it('la prière préparatoire, puis la vertu du jour', () => {
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
		expect(jours).toEqual(joursAvant('2027-03-19', 9));
		jours.forEach((date, k) => {
			const s = ligne(calculer(date), ID)!.sections.filter((x) => x.genre === 'texte');
			expect(
				s.map((x) => x.extrait?.section?.split('.')[0]),
				date
			).toEqual(['## Prière préparatoire', `## ${ORD[k]} jour`]);
			for (const x of s) expect(extraire(corps(x.texte!)!, x.extrait), date).toBeTruthy();
		});
	});
});

describe('neuvaine à saint François-Xavier (Québec 1880), aux dates de Beringer : 4-12 mars, veille le 3', () => {
	it('la veille, la considération préparatoire ; puis neuf jours (4-12 mars 2027) : considération du jour, prières, litanies', () => {
		const ID = 'prog:neuvaine-saint-francois-xavier';
		const JOURS = ['Premier', 'Second', 'Troisième', 'Quatrième', 'Cinquième', 'Sixième', 'Septième', 'Huitième', 'Dernier'];
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
		expect(jours).toEqual(joursAvant('2027-03-13', 10));
		jours.forEach((date, k) => {
			const s = ligne(calculer(date), ID)!.sections.filter((x) => x.genre === 'texte');
			const attendu = k === 0 ? ['## Considération pour la veille de la neuvaine'] : [`## ${JOURS[k - 1]} jour`, undefined, undefined];
			expect(s.map((x) => x.extrait?.section?.split('.')[0]), date).toEqual(attendu);
			if (k > 0) expect(s.slice(1).map((x) => x.texte), date).toEqual(['xavier1880:prieres-neuvaine', 'xavier1880:litanies-saint-francois-xavier']);
			const t = extraire(corps(s[0].texte!)!, s[0].extrait)!;
			expect(t, date).toBeTruthy();
			expect(t, date).not.toMatch(/page 41/);
		});
	});
});

describe('neuvaine à saint Joseph pour une grâce particulière (Confrérie de Montréal), sans date', () => {
	it('recueil de circonstance : la pièce a ses neuf jours, mais n’entre dans aucune journée', () => {
		const ID = 'confreriejoseph:neuvaine-grace-particuliere';
		const t = corps(ID)!;
		expect(t.match(/^## .*$/gm)).toEqual([
			'## Prière préparatoire',
			...['Ier', 'IIe', 'IIIe', 'IVe', 'Ve', 'VIe', 'VIIe', 'VIIIe', 'IXe'].map((n) => expect.stringMatching(new RegExp(`^## ${n} jour\\. Saint Joseph`)))
		]);
		for (const j of CALENDRIER) {
			const jr = calculer(j.date);
			expect([...jr.lignes, ...jr.lectures].some((l) => l.sections.some((x) => x.texte === ID)), j.date).toBe(false);
		}
	});
});

describe('neuvaine au Saint-Esprit de saint Alphonse (Tournois 1897), de l’Ascension à la vigile de la Pentecôte', () => {
	it('dix jours, 6-15 mai 2027 : une méditation par jour, dans l’ordre', () => {
		const ID = 'prog:neuvaine-saint-esprit';
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
		expect(jours).toEqual(joursAvant('2027-05-16', 10));
		jours.forEach((date, k) => {
			const s = ligne(calculer(date), ID)!.sections.filter((x) => x.genre === 'texte');
			expect(s.map((x) => x.extrait?.section?.split('.')[0]), date).toEqual([`## ${k + 1}${k ? 'e' : 're'} méditation`]);
			expect(extraire(corps(s[0].texte!)!, s[0].extrait), date).toMatch(/### Affections et prières/);
		});
	});
});

describe('méditations de l’Avent de saint Alphonse (Tournois 1897), demande du 28 nov.', () => {
	const ID = 'prog:meditations-avent';
	const JOURS = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
	const rang = (t: string) => `${t[3]}${t[3] === '1' ? 'er' : 'e'}`;
	it('une méditation par jour du temporal, dans l’ordre du livre, jusqu’à la neuvaine de Noël', () => {
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID));
		expect(jours[0].date).toBe('2026-11-29');
		expect(jours.every((j) => j.date < '2026-12-16')).toBe(true);
		for (const j of jours) {
			const s = ligne(calculer(j.date), ID)!.sections.filter((x) => x.genre === 'texte');
			const attendu = `## ${rang(j.tempora!)} ${JOURS[Number(j.tempora!.slice(-1))]}`;
			expect(s.map((x) => x.extrait?.section?.split('.')[0]), j.date).toEqual([attendu]);
			expect(extraire(corps(s[0].texte!)!, s[0].extrait), j.date).toMatch(/### Affections et prières/);
		}
	});
	it('ne recouvre pas la neuvaine de Noël (16-24 décembre)', () => {
		for (const date of ['2026-12-16', '2026-12-20', '2026-12-24']) expect(ligne(calculer(date), ID), date).toBeUndefined();
	});
});

describe('neuvaine à sainte Anne (Montréal 1878), du 17 au 25 juillet', () => {
	it('chaque jour sa considération, sans les renvois, puis les prières de la fin', () => {
		const ID = 'prog:neuvaine-sainte-anne';
		const ORD = ['Premier', 'Second', 'Troisième', 'Quatrième', 'Cinquième', 'Sixième', 'Septième', 'Huitième', 'Neuvième'];
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
		expect(jours).toEqual(joursAvant('2027-07-26', 9));
		jours.forEach((date, k) => {
			const s = ligne(calculer(date), ID)!.sections.filter((x) => x.genre === 'texte');
			expect(s.map((x) => x.extrait?.section?.split('.')[0]), date).toEqual([`## ${ORD[k]} jour`, '## Prières que l’on doit faire chaque jour à la fin des Exercices de la Neuvaine'.replace('’', "'")]);
			for (const x of s) {
				const t = extraire(corps(x.texte!)!, x.extrait)!;
				expect(t, date).toBeTruthy();
				expect(t, date).not.toMatch(/Voir à la fin/i);
			}
		});
	});
});

describe('neuvaine au Très Saint Sacrement (Montréal), les neuf jours qui finissent la veille de la Fête-Dieu', () => {
	it('18-26 mai 2027 ; le 1er jour en entier, ensuite le début et la fin du 1er jour autour de la prière du jour', () => {
		const ID = 'prog:neuvaine-fete-dieu';
		const ORD = ['Ier', 'IIème', 'IIIème', 'IVème', 'Vième', 'VIème', 'VIIème', 'VIIIème', 'IXème'];
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
		expect(jours).toEqual(joursAvant('2027-05-27', 9));
		expect(jourDe('2027-05-27').tempora).toBe('Pent01-4');
		jours.forEach((date, k) => {
			const s = ligne(calculer(date), ID)!.sections.filter((x) => x.genre === 'texte');
			const titres = s.map((x) => x.extrait!.section);
			if (k === 0) expect(titres, date).toEqual(['## Ier jour']);
			else
				expect(titres, date).toEqual([
					'## Ier jour',
					`## ${ORD[k]} jour`,
					'## Ier jour',
					...(k === 8 ? ['## Prière pour la Cloture de la Neuvaine'] : [])
				]);
			for (const x of s) {
				const t = extraire(corps(x.texte!)!, x.extrait)!;
				expect(t, date).toBeTruthy();
				if (k > 0) expect(t, date).not.toMatch(/etc\.\*/);
			}
		});
	});
});

describe('triduums des trois fêtes de saint Joseph (Confrérie de Montréal)', () => {
	const ID = 'prog:triduums-saint-joseph';
	const parties = (date: string) =>
		ligne(calculer(date), ID)!
			.sections.filter((s) => s.genre === 'texte')
			.map((s) => `${s.extrait?.section?.split('.')[0]} ${s.extrait?.de ? 'jour' : 'triduum'}`);
	it('Fiançailles, 19 mars, Patronage : trois jours, puis la prière du jour de la fête', () => {
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
		expect(jours).toEqual([
			'2026-12-31',
			'2027-01-01',
			'2027-01-02',
			'2027-01-03',
			'2027-03-16',
			'2027-03-17',
			'2027-03-18',
			'2027-03-19',
			'2027-04-11',
			'2027-04-12',
			'2027-04-13',
			'2027-04-14'
		]);
		expect(parties('2027-01-01')).toEqual(['## I triduum']);
		expect(parties('2027-01-03')).toEqual(['## I jour']);
		expect(parties('2027-03-17')).toEqual(['## II triduum']);
		expect(parties('2027-03-19')).toEqual(['## II jour']);
		expect(parties('2027-04-12')).toEqual(['## III triduum']);
		expect(jourDe('2027-04-14').office).toMatch(/^Patronage de S\. Joseph/);
		expect(parties('2027-04-14')).toEqual(['## III jour']);
		for (const d of jours)
			for (const s of ligne(calculer(d), ID)!.sections.filter((x) => x.genre === 'texte'))
				expect(extraire(corps(s.texte!)!, s.extrait), d).toBeTruthy();
	});
});

describe('neuvaine de réparation au Sacré-Cœur, du 1er au 9 de chaque mois (Beringer n° 671)', () => {
	it('l’offrande à la fin de la prière du matin, les jours 1 à 9 de chaque mois seulement', () => {
		const jours = CALENDRIER.filter((j) =>
			ligne(calculer(j.date), 'prog:priere-du-matin')!.sections.some((s) => s.texte === 'beringer:neuvaine-reparation-sacre-coeur')
		).map((j) => j.date);
		expect(jours.length).toBe(12 * 9);
		expect(jours.every((d) => Number(d.slice(8)) <= 9)).toBe(true);
		expect(jours.slice(0, 9)).toEqual(Array.from({ length: 9 }, (_, k) => `2026-12-0${k + 1}`));
	});
});

describe('lot B des archiconfréries intégré (décisions du 26 nov.)', () => {
	const sections = (date: string, id: string) => ligne(calculer(date), id)?.sections ?? [];
	it('chapelet : le fruit propre de chaque mystère après chaque dizaine', () => {
		const s = sections('2026-11-30', 'prog:chapelet'); // lundi : mystères joyeux
		const fruits = s.filter((x) => x.texte === 'rosairevivant1841:fruits-des-quinze-mysteres').map((x) => x.extrait?.section);
		expect(fruits).toEqual([
			'## Premier mystère joyeux',
			'## Second mystère joyeux',
			'## Troisième mystère joyeux',
			'## Quatrième mystère joyeux',
			'## Cinquième mystère joyeux'
		]);
		// chaque fruit suit sa dizaine : il vient après la prière de fin de dizaine, et avant la dizaine suivante
		const k = s.findIndex((x) => x.texte === 'rosairevivant1841:fruits-des-quinze-mysteres');
		expect(s.slice(0, k).some((x) => x.texte === 'fsspx:o-mon-jesus-fatima')).toBe(true);
		expect(
			sections('2026-12-01', 'prog:chapelet').find((x) => x.texte === 'rosairevivant1841:fruits-des-quinze-mysteres')?.extrait?.section
		).toBe('## Premier mystère douloureux');
	});
	it('mercredi, mardi, juillet et fête du saint Nom', () => {
		const t = (d: string, id: string) => sections(d, id).map((x) => x.texte);
		expect(t('2026-12-02', 'prog:devotion-mercredi')).toContain('cordonjoseph1871:souvenez-vous-a-saint-joseph');
		expect(t('2026-12-01', 'prog:devotion-mardi')).toContain('janvier:priere-de-pie-ix-sainte-face');
		expect(t('2027-07-02', 'prog:devotion-vendredi')).toContain('beringer:offrande-du-precieux-sang');
		expect(t('2027-06-04', 'prog:devotion-vendredi')).not.toContain('beringer:offrande-du-precieux-sang');
		expect(t('2027-01-03', 'prog:saint-nom-de-jesus')).toContain('saintnom1899:petit-office-saint-nom-de-jesus');
		expect(ligne(calculer('2027-01-04'), 'prog:saint-nom-de-jesus')).toBeUndefined();
	});
});

describe('lot A des archiconfréries intégré (décisions du 26 nov.)', () => {
	const t = (date: string, id: string) => (ligne(calculer(date), id)?.sections ?? []).map((s) => s.texte);
	const PREPARATION = [
		'lefebvre1870:protestation-pour-bien-mourir',
		'lefebvre1870:testament-spirituel-saint-charles',
		'lefebvre1870:priere-saint-vincent-ferrier-bonne-mort',
		'lefebvre1870:autre-testament-spirituel',
		'lefebvre1870:priere-sainte-gertrude-ave-candidum'
	];
	it('vendredi : les litanies de la Passion et des Sept-Douleurs (Lefebvre) entrent dans la roue, une par semaine', () => {
		const vendredis = ['2026-12-04', '2026-12-11', '2026-12-18', '2026-12-25', '2027-01-01', '2027-01-08', '2027-01-15', '2027-01-22'];
		const vues = new Set(vendredis.flatMap((d) => t(d, 'prog:devotion-vendredi')).filter((x) => x?.includes('litanies')));
		expect(vues).toEqual(
			new Set([
				'beringer:litanies-sacre-coeur',
				'jardin:litanies-de-notre-dame-des-sept-douleurs',
				'lefebvre1870:litanies-de-la-passion',
				'lefebvre1870:litanies-notre-dame-des-sept-douleurs'
			])
		);
		for (const d of vendredis) expect(t(d, 'prog:devotion-vendredi').filter((x) => x?.includes('litanies'))).toHaveLength(1);
	});
	it('premier vendredi : un texte de préparation à la mort, qui change chaque mois', () => {
		const premiers = ['2026-12-04', '2027-01-01', '2027-02-05', '2027-03-05', '2027-04-02'];
		const choisis = premiers.map((d) => t(d, 'prog:devotion-vendredi').filter((x) => PREPARATION.includes(x ?? '')));
		for (const c of choisis) expect(c).toHaveLength(1);
		expect(new Set(choisis.flat())).toEqual(new Set(PREPARATION));
		expect(t('2026-12-11', 'prog:devotion-vendredi').some((x) => PREPARATION.includes(x ?? ''))).toBe(false);
		expect(t('2026-12-04', 'prog:devotion-vendredi')).toEqual(t('2026-12-04', 'prog:devotion-vendredi')); // déterministe
	});
	it('novembre : les âmes les plus oubliées et la délivrance des âmes, une semaine sur deux, le soir', () => {
		const AMES = ['perpetuelsecours1878:ames-les-plus-oubliees', 'precieuxsang1890:priere-delivrance-ames-purgatoire'];
		const soirs = ['2027-11-02', '2027-11-09', '2027-11-16', '2027-11-23'].map((d) =>
			t(d, 'prog:priere-du-soir').filter((x) => AMES.includes(x ?? ''))
		);
		for (const s of soirs) expect(s).toHaveLength(1);
		expect(new Set(soirs.flat())).toEqual(new Set(AMES));
		expect(t('2026-12-01', 'prog:priere-du-soir').some((x) => AMES.includes(x ?? ''))).toBe(false);
	});
	it('1er juillet : consécration au Précieux Sang ; fête de N.-D. du Perpétuel-Secours : consécration de l’Archiconfrérie', () => {
		expect(t('2027-07-01', 'prog:priere-du-matin')).toContain('precieuxsang1890:consecration-au-precieux-sang');
		expect(t('2027-07-02', 'prog:priere-du-matin')).not.toContain('precieuxsang1890:consecration-au-precieux-sang');
		// fête « fixée au dimanche qui précède le 24 juin » (manuel de Montréal, 1878, p. 141) : le 20 juin 2027
		expect(t('2027-06-20', 'prog:priere-du-matin')).toContain('perpetuelsecours1878:consecration-archiconfrerie');
		expect(t('2027-06-27', 'prog:priere-du-matin')).not.toContain('perpetuelsecours1878:consecration-archiconfrerie');
		expect(t('2027-06-22', 'prog:priere-du-matin')).not.toContain('perpetuelsecours1878:consecration-archiconfrerie');
	});
});

describe('supplique de la Médaille miraculeuse (texte donné par l’utilisateur, 27 nov. 2026), le 27 de chaque mois', () => {
	const ID = 'prog:supplique-medaille-miraculeuse';
	it('le 27 de chaque mois seulement, à 17 h 30, sans la rubrique finale dans le texte compté', () => {
		const jours = CALENDRIER.filter((j) => ligne(calculer(j.date), ID)).map((j) => j.date);
		expect(jours.length).toBeGreaterThanOrEqual(11);
		for (const d of jours) expect(d.slice(8), d).toBe('27');
		const l = ligne(calculer(jours[0]), ID)!;
		const s = l.sections.filter((x) => x.genre === 'texte');
		expect(s.map((x) => x.texte)).toEqual(['utilisateur:supplique-medaille-miraculeuse']);
		const t = extraire(corps(s[0].texte!)!, s[0].extrait)!;
		expect(t.trimEnd().endsWith('dans le Ciel. Ainsi soit-il.')).toBe(true);
		expect(l.sections.some((x) => x.genre === 'editorial' && x.contenu?.includes('Salve Regina'))).toBe(true);
	});
});
