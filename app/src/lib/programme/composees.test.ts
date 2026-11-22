/**
 * Lot 6 : les pages composées à l'affichage par le programme (chapelet, Triple Couronne, offrande du matin) sont, mot
 * pour mot, celles que livrait engine/composer/composer.py (références figées dans references/pages-composees.json).
 */
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { contenuDe } from './bilan.ts';
import { journee } from './journee.ts';
import type { Ligne } from './types.ts';
import { CALENDRIER, corps, PLAN, PROGRAMME } from './donnees-de-test.ts';

const REF = JSON.parse(readFileSync(new URL('./references/pages-composees.json', import.meta.url), 'utf-8')) as {
	pages: Record<string, { titre: string; corps: string }>;
};

/** Le texte de la page, sans les petites pratiques insérées (fin de dizaine) ni celles des autres entrées. */
function page(l: Ligne, de?: (s: Ligne['sections'][number]) => boolean): string {
	return (
		l.sections
			.filter((s) => s.origine === l.id && (!de || de(s)))
			// une partie de la page (titre replié) tient lieu du titre « ## … » de la page livrée
			.map((s) => (s.genre === 'editorial' ? (s.contenu ?? '') : s.genre === 'partie' ? `## ${s.contenu}` : contenuDe(s, corps)))
			.join('\n\n')
	);
}
const jourDeSemaine = (k: number) => CALENDRIER.find((j) => new Date(j.date + 'T12:00:00').getDay() === k)!;
const ligneDu = (k: number, id: string) =>
	journee(PROGRAMME, { jour: jourDeSemaine(k), pratiques: PLAN, corps }).lignes.find((l) => l.id === id)!;

describe('pages composées à l’affichage = pages livrées par composer.py', () => {
	const CHAPELET: Record<string, number> = { joyeux: 1, douloureux: 2, glorieux: 3 };
	for (const [nom, k] of Object.entries(CHAPELET))
		it(`chapelet, mystères ${nom}`, () => {
			expect(page(ligneDu(k, 'prog:chapelet'))).toBe(REF.pages[`hortus:chapelet-${nom}`].corps);
		});

	const COURONNE: Record<number, number> = { 1: 1, 2: 2, 3: 4 };
	for (const [n, k] of Object.entries(COURONNE))
		it(`Triple Couronne, ${n}e couronne`, () => {
			expect(page(ligneDu(k, 'prog:triple-couronne'))).toBe(REF.pages[`hortus:triple-couronne-${n}`].corps);
			// la correction livrée le 20 nov. (Thésaurisons n° 82) est bien dans la page composée depuis le livret
			expect(page(ligneDu(k, 'prog:triple-couronne'))).toContain('[Doux Cœur de mon Jésus, faites que je vous aime de plus en plus.]');
		});

	it('offrande du matin (dans la page de la prière du matin)', () => {
		const l = ligneDu(1, 'prog:priere-du-matin');
		const debut = l.sections.findIndex((s) => s.genre === 'editorial');
		const fin = l.sections.findIndex((s) => s.genre === 'partie' && s.contenu === 'Intentions et recommandations');
		const offrande = { ...l, sections: l.sections.slice(debut, fin) };
		expect(page(offrande)).toBe(REF.pages['hortus:offrande-du-matin'].corps);
	});

	it('prière du matin et du soir : en parties titrées, les devoirs de charité repliés', () => {
		const parties = (l: Ligne) => l.sections.filter((s) => s.genre === 'partie').map((s) => (s.replie ? `(${s.contenu})` : s.contenu));
		expect(parties(ligneDu(1, 'prog:priere-du-matin'))).toEqual([
			'Prière du matin',
			'Actes de foi, d’espérance et de charité',
			'Offrande de la journée',
			'(Actes des devoirs de charité)',
			'Intentions et recommandations'
		]);
		expect(parties(ligneDu(1, 'prog:priere-du-soir'))).toEqual([
			'Don du Saint-Esprit du jour',
			'Prière du soir',
			'Recommandations du soir'
		]);
		// la prière du Paroissien, coupée en deux parties, reste entière et comptée une fois
		const matin = ligneDu(1, 'prog:priere-du-matin');
		const morceaux = matin.sections.filter((s) => s.texte === 'paroissien:priere-du-matin');
		expect(morceaux.map((s) => contenuDe(s, corps)).join('\n\n')).toBe(corps('paroissien:priere-du-matin')!.trim());
		expect(morceaux.filter((s) => !s.suite)).toHaveLength(1);
		// le Salve Regina reste après « Invoquons la sainte Vierge », à la fin de la première partie
		const k = matin.sections.findIndex((s) => s.origine === 'prog:salve-regina');
		expect(matin.sections[k + 1]?.contenu).toBe('Actes de foi, d’espérance et de charité');
	});

	it('chaque jour a sa couronne et ses mystères, avec le sous-titre de la ligne', () => {
		expect(ligneDu(0, 'prog:triple-couronne').sousTitre).toMatch(/^Troisième couronne/);
		expect(ligneDu(5, 'prog:chapelet').sousTitre).toBe('Mystères douloureux');
	});

	it('un texte coupé en plusieurs parties n’est compté qu’une fois (« suite »)', () => {
		const l = ligneDu(1, 'prog:triple-couronne');
		const ordinaire = l.sections.filter((s) => s.texte === 'jardin:la-triple-couronne-d-or-du-sacre-c-ur-de-jesus');
		expect(ordinaire.length).toBeGreaterThan(1);
		expect(ordinaire.filter((s) => !s.suite)).toHaveLength(1);
	});
});
