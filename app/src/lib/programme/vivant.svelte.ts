/**
 * La journée calculée, tenue à jour dans un composant : programme livré, jour liturgique, pratiques, réglages de
 * l'utilisateur et textes (pour couper les pages hôtes et estimer les durées). À appeler pendant l'initialisation.
 */
import { jourDu, type Jour } from '../calendrier.ts';
import { db } from '../db.ts';
import type { Pratique, Texte } from '../types.ts';
import { vivantSelon } from '../vivant.svelte.ts';
import { dimensionsEffectives } from '../dimensions.ts';
import { chargerProgramme } from './charger.ts';
import { chargerClassements, chargerCycles, chargerVocabulaire } from './dimensions.ts';
import { journee } from './journee.ts';
import type { ClassementTexte, Cycles, Journee, Programme, ReglageProgramme, Vocabulaire } from './types.ts';

export function journeeVivante(date: () => string) {
	let programme = $state.raw<Programme | null>(null);
	chargerProgramme().then((p) => (programme = p));
	// lot « Dimensions » : de quoi décrire la journée (contexte, couverture), sans rien y changer
	let cycles = $state.raw<Cycles | null>(null);
	let vocabulaire = $state.raw<Vocabulaire | null>(null);
	let classements = $state.raw<Record<string, ClassementTexte> | null>(null);
	chargerCycles().then((c) => (cycles = c));
	chargerVocabulaire().then((v) => (vocabulaire = v));
	chargerClassements().then((c) => (classements = c));
	let jour = $state.raw<Jour | undefined>();
	$effect(() => {
		const d = date();
		jourDu(d).then((j) => {
			if (date() === d) jour = j;
		});
	});
	const pratiques = vivantSelon(() => () => db.pratiques.toArray(), [] as Pratique[]);
	const reglages = vivantSelon(() => () => db.programme.toArray(), [] as ReglageProgramme[]);
	const textes = vivantSelon(() => () => db.textes.toArray(), [] as Texte[]);
	const parId = $derived(new Map(textes.v.filter((t) => !t.supprimeLe).map((t) => [t.id, t])));
	const corps = (id: string) => parId.get(id)?.corps;
	const dimensions = (id: string) => {
		const t = parId.get(id);
		return t ? dimensionsEffectives(t, classements?.[id]).valeurs : undefined;
	};
	const jr = $derived.by((): Journee | null => {
		const d = date();
		if (!programme || !textes.v.length) return null;
		const j = jour?.date === d ? jour : { date: d };
		return journee(programme, { jour: j, pratiques: pratiques.v, corps, reglages: reglages.v, cycles, dimensions, vocabulaire });
	});
	return {
		get jr() {
			return jr;
		},
		/** Jour liturgique de la date affichée (undefined pendant le chargement, ou hors des années calculées). */
		get jour() {
			return jour?.date === date() ? jour : undefined;
		},
		get programme() {
			return programme;
		},
		get pratiques() {
			return pratiques.v;
		},
		get textes() {
			return parId;
		},
		get vocabulaire() {
			return vocabulaire;
		},
		get classements() {
			return classements;
		},
		dimensions,
		corps
	};
}
