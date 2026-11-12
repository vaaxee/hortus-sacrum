import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { invocation } from './invocations.ts';

const inv = (t: string) => invocation(t)?.texte ?? null;

describe('invocation', () => {
	it.each([
		['À Constantinople, saint Théophane et ses compagnons.', 'Saint Théophane et vos compagnons, priez pour nous.'],
		['À Nicomédie, la passion de sainte Barbe, Vierge et Martyre. Durant la persécution de Maximin, elle subit d’abord les rigueurs de la prison.', 'Sainte Barbe, priez pour nous.'],
		['À Alexandrie, les saints Martyrs Pierre, Sévère et Leuce.', 'Saints Pierre, Sévère et Leuce, priez pour nous.'],
		['Dans la province du Pont, le bienheureux Mélèce, Évêque et Confesseur. Déjà très remarquable par son érudition.', 'Bienheureux Mélèce, priez pour nous.'],
		['À Rome, l’anniversaire de saint Jean Berchmans, érudit de la Compagnie de Jésus et Confesseur, remarquable par l’innocence de sa vie.', 'Saint Jean Berchmans, priez pour nous.'],
		['Saint Pierre Chrysologue, Évêque de Ravenne, Confesseur et Docteur de l’Église, dont il est fait mention le 4 des nones de ce mois (2 décembre).', 'Saint Pierre Chrysologue, priez pour nous.'],
		['Le même jour, les saints Martyrs Carpophore, Prêtre, et Abonde, Diacre. Durant la persécution de Dioclétien, ils furent meurtris.', 'Saints Carpophore et Abonde, priez pour nous.'],
		['À Nicomédie, saint Cyriaque et dix autres Martyrs.', 'Saint Cyriaque et vos compagnons, priez pour nous.'],
		['En Égypte, saint Julien, Martyr, avec cinq mille autres chrétiens.', 'Saint Julien et vos compagnons, priez pour nous.'],
		['À Halberstadt, en Germanie, le paisible sommeil de la bienheureuse reine Mathilde, mère d’Othon Ier, empereur des Romains.', 'Bienheureuse Mathilde, priez pour nous.'],
		['En Cappadoce, la commémoraison des saints Martyrs, qui, durant la persécution de Maximien Galère, eurent les jambes brisées.', 'Saints Martyrs, priez pour nous.'],
		['À Néocésarée, dans le Pont (aujourd’hui Niksar en Turquie), l’anniversaire de saint Grégoire, Évêque et Confesseur, illustre par sa doctrine.', 'Saint Grégoire, priez pour nous.'],
		['En Perse encore, les saints Parmène, Heliménas, Chrysotèle, Prêtres, Luc et Mucius, Diacres. Leur martyre est décrit ailleurs.', 'Saints Parmène, Heliménas, Chrysotèle, Luc et Mucius, priez pour nous.'],
		['À Rome, sainte Théodora, noble matrone qui, durant la persécution de Dioclétien, s’appliquait au service des Martyrs.', 'Sainte Théodora, priez pour nous.']
	])('%s', (eloge, attendu) => {
		expect(inv(eloge)).toBe(attendu);
	});

	it('pas d’invocation pour un mystère ou un éloge sans nom', () => {
		expect(inv('L’Épiphanie du Seigneur.')).toBeNull();
		expect(inv('Sur le Mont Thabor, la Transfiguration de Notre Seigneur Jésus-Christ.')).toBeNull();
	});

	it('couvre l’essentiel d’une année de martyrologe', () => {
		const annee = JSON.parse(readFileSync('../data/calendar/2026-2027.json', 'utf-8')) as { martyrologe: { texte: string }[] }[];
		const eloges = annee.flatMap((j) => j.martyrologe.map((m) => m.texte));
		const avec = eloges.filter((e) => invocation(e));
		expect(avec.length / eloges.length).toBeGreaterThan(0.9);
		// aucune invocation ne doit contenir de minuscule en tête de nom ni de ponctuation parasite
		for (const e of avec) expect(invocation(e)!.texte).toMatch(/^(Saints?|Saintes?|Bienheureux|Bienheureuses?) \p{Lu}[^.;:()]*, priez pour nous\.$/u);
	});
});
