import { describe, expect, it } from 'vitest';
import { contenu } from '../db.ts';
import type { ElementListe } from '../types.ts';
import { appliquerReglages, journee } from './journee.ts';
import { CORRESPONDANCE, planifierMigration, traduireCoche } from './migration.ts';
import { CALENDRIER, corps, PLAN, PROGRAMME } from './donnees-de-test.ts';

const TOUS = [true, true, true, true, true, true, true];
const T = '2000-01-01T00:00:00.000Z';

/** Ligne livrée telle que seed.ts la créait, avec son original. */
function livree(id: string, titre: string, x: Partial<ElementListe> = {}, modifs: Partial<ElementListe> = {}): ElementListe {
	const e: ElementListe = {
		id,
		origine: 'officielle',
		titre,
		moment: 'matin',
		etiquette: 'ordinaire',
		ordre: 10,
		jours: TOUS,
		rappels: [],
		textes: [],
		actif: true,
		creeLe: T,
		modifieLe: T,
		...x
	};
	e.original = contenu(e);
	return { ...e, ...modifs };
}

const ANCIENNE: ElementListe[] = [
	livree('liste:1', 'Offrande du matin', { textes: ['hortus:offrande-du-matin'] }),
	livree('liste:2', 'Prière du matin', { textes: ['paroissien:priere-du-matin'] }),
	// Salve désactivé : seule ligne qui mène à son entrée
	livree('liste:3', 'Salve Regina, avec ses versets', { textes: ['beringer:salve-regina'] }, { actif: false }),
	// intentions désactivées, mais la prière du matin reste
	livree('liste:4', 'Intentions particulières du jour', {}, { actif: false }),
	// chapelet : durée réglée à la main, rappel ajouté
	livree('liste:15', 'Chapelet', { textes: ['hortus:chapelet-du-jour'], moment: 'journee' }, { duree: 25, rappels: ['15:00'] }),
	// Brigitte : seulement le vendredi
	livree(
		'liste:19',
		'Quinze oraisons de sainte Brigitte',
		{ textes: ['jardin:les-quinze-oraisons-de-sainte-brigitte'] },
		{ jours: TOUS.map((_, k) => k === 5) }
	),
	// prières de la Triple Couronne changées par l'utilisateur
	livree(
		'liste:16',
		'Triple Couronne d’or du Sacré-Cœur',
		{ textes: ['hortus:triple-couronne-du-jour'] },
		{ textes: ['weber:souvenez-vous'] }
	),
	livree('liste:jaculatoires', 'Jaculatoires du jour', { textes: ['hortus:jaculatoires-du-jour'] }),
	{
		id: 'perso-1',
		origine: 'personnel',
		titre: 'Prière pour ma famille',
		moment: 'soir',
		etiquette: 'ordinaire',
		ordre: 300,
		jours: TOUS.map((_, k) => k === 0),
		rappels: ['20:30'],
		textes: ['weber:priere-saint-ephrem'],
		duree: 4,
		actif: true,
		creeLe: T,
		modifieLe: T
	}
];

describe('bascule de l’ancienne liste', () => {
	const { reglages, changements } = planifierMigration(ANCIENNE, PROGRAMME, '2026-11-20T00:00:00.000Z');
	const r = (id: string) => reglages.find((x) => x.id === id);

	it('chaque ancienne ligne livrée a sa correspondance vers une entrée qui existe', () => {
		for (const cible of Object.values(CORRESPONDANCE))
			if (cible)
				expect(
					PROGRAMME.entrees.some((e) => e.id === cible),
					cible
				).toBe(true);
	});

	it('garde les ajouts personnels avec leurs jours, rappels et durée', () => {
		expect(r('perso:perso-1')?.entree).toMatchObject({
			titre: 'Prière pour ma famille',
			quand: { jours_semaine: [0] },
			duree: 4,
			page: { moment: 'soir', heures: ['20:30'], sections: [{ texte: 'weber:priere-saint-ephrem' }] }
		});
	});

	it('une entrée n’est désactivée que si toutes les anciennes lignes qui y mènent l’étaient', () => {
		expect(r('prog:salve-regina')?.actif).toBe(false);
		expect(r('prog:priere-du-matin')?.actif).toBeUndefined();
		expect(changements.some((c) => c.annuler && 'reactiver' in c.annuler && c.annuler.reactiver === 'prog:salve-regina')).toBe(true);
	});

	it('garde les durées, les rappels et les jours réglés à la main', () => {
		expect(r('prog:chapelet')).toMatchObject({ duree: 25, heures: ['15:00'] });
		expect(r('prog:brigitte')?.quand).toEqual({ jours_semaine: [5] });
	});

	it('des prières changées que le programme ne dit pas deviennent un ajout personnel', () => {
		expect(r('perso:liste:16')?.entree?.page?.sections).toEqual([{ texte: 'weber:souvenez-vous' }]);
	});

	it('les lignes sans ligne propre sont expliquées', () => {
		expect(changements.find((c) => c.anciens.includes('liste:jaculatoires'))?.texte).toMatch(/jaculatoire/);
	});

	it('la journée calculée suit les réglages repris', () => {
		const jour = CALENDRIER.find((j) => j.date === '2026-12-06')!; // dimanche
		const jr = journee(PROGRAMME, { jour, pratiques: PLAN, corps, reglages });
		expect(jr.textes.has('beringer:salve-regina')).toBe(false);
		expect(jr.lignes.find((l) => l.id === 'prog:chapelet')).toMatchObject({ duree: 25, heures: ['15:00'] });
		expect(jr.lignes.some((l) => l.id === 'prog:brigitte')).toBe(false); // seulement le vendredi
		expect(jr.lignes.some((l) => l.id === 'perso:perso-1')).toBe(true);
		expect(appliquerReglages(PROGRAMME.entrees, reglages).some((e) => e.id === 'perso:liste:16')).toBe(true);
	});

	it('une base neuve sans ancienne liste ne produit rien', () => {
		expect(planifierMigration([], PROGRAMME, '')).toEqual({ reglages: [], changements: [] });
	});

	it('traduit les coches anciennes vers la ligne qui porte la pratique', () => {
		expect(traduireCoche('liste:3', PROGRAMME)).toBe('prog:priere-du-matin');
		expect(traduireCoche('liste:14', PROGRAMME)).toBe('prog:angelus');
		expect(traduireCoche('liste:24-3', PROGRAMME)).toBe('prog:devotion-mercredi');
		expect(traduireCoche('liste:petit-breviaire', PROGRAMME)).toBe('lec:office');
		expect(traduireCoche('perso-1', PROGRAMME)).toBe('perso-1');
		expect(traduireCoche('perso-1', PROGRAMME, new Set(['perso-1']))).toBe('perso:perso-1');
	});
});
