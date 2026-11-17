import { describe, expect, it } from 'vitest';
import { invocationLatine, vocatif } from './invocations-latines.ts';

describe('invocations latines du martyrologe', () => {
	it('vocatif des noms', () => {
		expect(vocatif('Bárbaræ')).toBe('Bárbara');
		expect(vocatif('Petri')).toBe('Petre');
		expect(vocatif('Gregórii')).toBe('Gregóri');
		expect(vocatif('Felícis')).toBe('Felix');
		expect(vocatif('Annónis')).toBe('Anno');
		expect(vocatif('Joánnis')).toBe('Joánnes');
	});
	it('une vierge martyre, avec le lieu', () => {
		expect(invocationLatine('Nicomedíæ pássio sanctæ Bárbaræ, Vírginis et Mártyris; quæ, in persecutióne Maximíni…')?.texte)
			.toBe('Sancta Bárbara, virgo Nicomedíæ, ora pro nobis peccatoribus. Amen.');
	});
	it('un évêque au nom en deux mots, sans l’adjectif de lieu', () => {
		expect(invocationLatine('Sancti Petri Chrysólogi, Epíscopi Ravennátis, Confessóris et Ecclésiæ Doctóris, cujus memória…')?.texte)
			.toBe('Sancte Petre Chrysóloge, episcope et confessor et Ecclesiæ doctor, ora pro nobis peccatoribus. Amen.');
	});
	it('un groupe de martyrs', () => {
		expect(invocationLatine('In Túscia sanctórum Mártyrum Joánnis et Festi.')?.texte)
			.toBe('Sancti Joánnes et Feste, martyres, orate pro nobis peccatoribus. Amen.');
	});
	it('pas d’invocation sans saint nommé', () => {
		expect(invocationLatine('Epiphánia Dómini.')).toBeNull();
	});
});
