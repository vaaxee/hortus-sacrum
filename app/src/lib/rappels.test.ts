import { describe, expect, it, vi } from 'vitest';

vi.mock('./sync.ts', () => ({ supabase: () => ({}) }));
vi.mock('./db.ts', () => ({ db: {} }));

const { rappelsDu, REGLAGES_DEFAUT } = await import('./rappels.ts');

const jours: Record<string, { office: string; rang: string; jeune_abstinence: { code: string; libelle: string } | null }> = {
	'2026-12-07': { office: 'S. Ambroise', rang: '3e cl.', jeune_abstinence: null },
	'2026-12-08': { office: 'Immaculée Conception', rang: '1re cl.', jeune_abstinence: null }
};
const ctx = {
	liste: [{ id: 'l1', titre: 'Angélus', moment: 'journee', etiquette: 'ordinaire', ordre: 1, jours: [true, true, true, true, true, true, true], rappels: ['06:00', '12:00', '18:00'], textes: ['paroissien:angelus'], actif: true, origine: 'officielle', creeLe: '', modifieLe: '' }],
	pratiques: [],
	fetes: [{ id: 'f1', titre: 'Mon baptême', genre: 'anniversaire', mois: 12, jour: 8, rappelVeille: true, notes: '', origine: 'personnel', creeLe: '', modifieLe: '' }],
	titres: { 'paroissien:angelus': 'Angélus' },
	jour: async (d: string) => jours[d] as never
};

describe('rappels du jour', () => {
	it('matin, heures fixes, soir et veille de fête', async () => {
		const r = await rappelsDu('2026-12-07', { ...REGLAGES_DEFAUT, actif: true }, ctx as never);
		const titres = r.map((x) => `${x.quand.getHours()}h ${x.titre}`);
		expect(titres).toEqual(['6h Angélus', '7h Aujourd’hui, lundi 7 décembre', '12h Angélus', '18h Angélus', '20h Demain, mardi 8 décembre', '21h Prière du soir']);
		expect(r.find((x) => x.titre.startsWith('Demain'))!.corps).toContain('Immaculée Conception');
		expect(r.find((x) => x.titre.startsWith('Demain'))!.corps).toContain('Mon baptême');
	});
	it('respecte les rappels désactivés', async () => {
		const r = await rappelsDu('2026-12-07', { ...REGLAGES_DEFAUT, actif: true, heuresFixes: false, soir: '', veille: '' }, ctx as never);
		expect(r.map((x) => x.titre)).toEqual(['Aujourd’hui, lundi 7 décembre']);
	});
});
