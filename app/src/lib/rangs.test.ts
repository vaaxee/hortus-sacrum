import { describe, expect, it } from 'vitest';
import { garde, rangElement, rangPratique } from './rangs.ts';

describe('rangs des dévotions', () => {
	it('donne un rang de départ selon le titre, et respecte le choix de l’utilisateur', () => {
		expect(rangElement({ titre: 'Prière du matin' })).toBe('praecipua');
		expect(rangElement({ titre: 'Cordon de saint Joseph : sept Gloria Patri' })).toBe('supererogatoria');
		expect(rangElement({ titre: 'Salve Regina, avec ses versets' })).toBe('pia');
		expect(rangElement({ titre: 'Prière du matin', rang: 'pia' })).toBe('pia');
		expect(rangPratique({})).toBe('praecipua');
	});
	it('filtre selon le seuil du jour chargé', () => {
		expect(garde('supererogatoria', 'supererogatoria')).toBe(true);
		expect(garde('supererogatoria', 'pia')).toBe(false);
		expect(garde('pia', 'praecipua')).toBe(false);
		expect(garde('praecipua', 'praecipua')).toBe(true);
	});
});
