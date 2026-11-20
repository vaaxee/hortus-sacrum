import { describe, expect, it } from 'vitest';
import { avecLeNom, priereDuSaint } from './gertrude.ts';

describe('prière de sainte Gertrude au saint du jour', () => {
	it('choisit la prière selon la catégorie', () => {
		expect(priereDuSaint('Ste Bibiane, Vierge et Martyre', true)).toEqual({ id: 'gertrude:a-une-vierge-et-martyre', nom: 'Bibiane' });
		expect(priereDuSaint('Ste Lucie, Vierge', true)?.id).toBe('gertrude:a-une-vierge');
		expect(priereDuSaint('S. Clément Ier, Pape et Martyr', true)).toEqual({ id: 'gertrude:a-un-martyr', nom: 'Clément Ier' });
		expect(priereDuSaint('S. Pierre Chrysologue, Évêque, Confesseur et Docteur de l’Église', true)?.id).toBe('gertrude:a-un-confesseur');
		expect(priereDuSaint('S. André, Apôtre', true)).toEqual({ id: 'gertrude:saint-du-jour', nom: '' });
		expect(priereDuSaint('SS. Simon et Jude, Apôtres', true)?.id).toBe('gertrude:saint-du-jour');
	});
	it('rien pour une fête du Seigneur ou de la sainte Vierge', () => {
		expect(priereDuSaint('Immaculée Conception de la Bienheureuse Vierge Marie', true)).toBeNull();
		expect(priereDuSaint('Férie', false)).toBeNull();
	});
	it('met le nom à la place de « N... »', () => {
		expect(avecLeNom('Je vous salue, saint N..., illustre Confesseur', 'François-Xavier')).toBe(
			'Je vous salue, saint François-Xavier, illustre Confesseur'
		);
	});
});
