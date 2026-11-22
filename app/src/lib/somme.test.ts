import { readdirSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { articleDuJour, voisins, type IndexSomme, type Question } from './somme.ts';

/** Somme théologique (lot 10) : structure des fichiers livrés, ordre de lecture, latin et français alignés. */
const dossier = new URL('../../../data/somme/', import.meta.url);
const lire = <T>(f: string) => JSON.parse(readFileSync(new URL(f, dossier), 'utf8')) as T;
const index = lire<IndexSomme>('index.json');
const fichiers = readdirSync(dossier)
	.filter((f) => /^Ia-\d\d\.json$/.test(f))
	.sort();
const questions = fichiers.map((f) => lire<Question>(f));

describe('Somme : données', () => {
	it('les questions se suivent depuis la Iª q. 1, sans trou', () => {
		expect(fichiers.length).toBeGreaterThanOrEqual(2);
		questions.forEach((q, i) => {
			expect(q.question).toBe(i + 1);
			expect(q.ref).toBe(`Iª q. ${i + 1}`);
			expect(q.partie).toBe('Ia');
		});
	});

	it("l'index donne tous les articles, dans l'ordre, et rien d'autre", () => {
		const attendus = questions.flatMap((q, i) => q.articles.map((a) => ({ ref: a.ref, fichier: fichiers[i] })));
		expect(index.articles.map(({ ref, fichier }) => ({ ref, fichier }))).toEqual(attendus);
		index.articles.forEach((e, i) => {
			expect(e.ref).toBe(`Iª q. ${e.question} a. ${e.article}`);
			const prec = index.articles[i - 1];
			if (prec)
				expect(e.question === prec.question ? e.article === prec.article + 1 : e.question === prec.question + 1 && e.article === 1).toBe(
					true
				);
			else expect([e.question, e.article]).toEqual([1, 1]);
		});
	});

	it('latin et français alignés, aucune partie vide', () => {
		for (const q of questions) {
			expect(q.titre.la && q.titre.fr && q.prooemium.la && q.prooemium.fr).toBeTruthy();
			for (const a of q.articles) {
				expect(a.titre.la && a.titre.fr, a.ref).toBeTruthy();
				expect(a.objections.length, a.ref).toBeGreaterThan(0);
				for (const p of [...a.objections, a.sed_contra, a.respondeo, ...a.reponses]) {
					expect(p.la.trim(), a.ref).not.toBe('');
					// Lachat omet parfois le « Sed contra » (Iª q. 1 a. 5) : le manque est dit dans les notes de l'article
					if (p === a.sed_contra && !p.fr) expect(a.notes?.join(' '), a.ref).toMatch(/Sed contra/);
					else expect(p.fr.trim(), a.ref).not.toBe('');
				}
				// objections numérotées comme dans Lachat : « Il paroît … 1° », puis « 2° », « 3° »…
				a.objections.slice(1).forEach((o, k) => expect(o.fr, a.ref).toMatch(new RegExp(`^${k + 2}(°|\\. )`)));
				expect(a.objections[0].fr, a.ref).toMatch(/^Il paro[iî]t/);
				if (a.sed_contra.fr) expect(a.sed_contra.fr, a.ref).toMatch(/^Mais /);
				expect(a.reponses[0].fr, a.ref).toMatch(/^(Je réponds aux |Ces observations)/);
				expect(a.objections.length, a.ref).toBe(a.objections.filter((o) => o.la).length);
				expect(a.pages.fr[0]).toBeLessThanOrEqual(a.pages.fr[1]);
			}
		}
	});

	it('aucune marque de relecture ou de vote restée dans le texte', () => {
		for (const q of questions) {
			const t = JSON.stringify([q.titre, q.prooemium, q.articles]);
			expect(t).not.toMatch(/[⟦⟧⁞¶]/);
			expect(t).not.toMatch(/\(Conclusion/);
		}
	});

	it('chaque question porte sa source et sa révision', () => {
		for (const q of questions) {
			expect(q.source.fr.url).toMatch(/^https:\/\/archive\.org\//);
			expect(q.source.la.url).toMatch(/^https:\/\/archive\.org\//);
			expect(q.source.fr.edition).toMatch(/Vivès/);
			expect(q.revision).toBeGreaterThanOrEqual(1);
		}
	});

	it("les titres d'article sont les questions posées", () => {
		// l'intitulé « ARTICLE II. » n'est pas gardé : le titre français est la question posée
		for (const q of questions) for (const a of q.articles) expect(a.titre.fr, a.ref).not.toMatch(/^ARTICLE/);
	});
});

describe('Somme : article du jour', () => {
	const ix: IndexSomme = {
		note: '',
		articles: [
			{ ref: 'Iª q. 1 a. 1', fichier: 'Ia-01.json', question: 1, article: 1 },
			{ ref: 'Iª q. 1 a. 2', fichier: 'Ia-01.json', question: 1, article: 2 },
			{ ref: 'Iª q. 2 a. 1', fichier: 'Ia-02.json', question: 2, article: 1 }
		]
	};
	it('sans marque-page : le premier article', () => {
		expect(articleDuJour(ix, undefined, '2026-11-22')).toEqual({ entree: ix.articles[0], fin: false });
	});
	it('lu un autre jour : le suivant ; lu ce jour : le même', () => {
		expect(articleDuJour(ix, { ref: 'Iª q. 1 a. 2', date: '2026-11-21' }, '2026-11-22').entree.ref).toBe('Iª q. 2 a. 1');
		expect(articleDuJour(ix, { ref: 'Iª q. 1 a. 2', date: '2026-11-22' }, '2026-11-22').entree.ref).toBe('Iª q. 1 a. 2');
	});
	it('tout est lu : le dernier, avec « fin »', () => {
		expect(articleDuJour(ix, { ref: 'Iª q. 2 a. 1', date: '2026-11-01' }, '2026-11-22')).toEqual({ entree: ix.articles[2], fin: true });
	});
	it('marque-page inconnu (données changées) : on reprend au début', () => {
		expect(articleDuJour(ix, { ref: 'IIª q. 9 a. 9', date: '2026-11-01' }, '2026-11-22').entree.ref).toBe('Iª q. 1 a. 1');
	});
	it('voisins', () => {
		expect(voisins(ix, 'Iª q. 1 a. 2')).toEqual({ avant: ix.articles[0], apres: ix.articles[2] });
		expect(voisins(ix, 'Iª q. 1 a. 1').avant).toBeUndefined();
	});
	it('les données livrées commencent par Iª q. 1 a. 1', () => {
		expect(articleDuJour(index, undefined, '2026-11-22').entree.ref).toBe('Iª q. 1 a. 1');
	});
});
