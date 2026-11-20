/**
 * Données réelles pour les tests du programme (Node seulement) : programme, textes (sources et livret), calendrier
 * 2026-2027 et plan de l'année tel que l'app l'importe.
 */
import { readFileSync } from 'node:fs';
import type { Jour } from '../calendrier.ts';
import { pratiquesDuPlan } from '../plan.ts';
import { pieceVersTexte } from '../livret.ts';
import type { Pratique, Texte } from '../types.ts';
import type { Programme } from './types.ts';

const lire = <T>(chemin: string): T => JSON.parse(readFileSync(new URL(`../../../../data/${chemin}`, import.meta.url), 'utf-8')) as T;

export const PROGRAMME = lire<Programme>('programme/programme.json');

const sources = lire<{ pieces: Texte[] }>('prieres/sources.json').pieces;
const livret = lire<{ pieces: Parameters<typeof pieceVersTexte>[0][] }>('prieres/jardin.json').pieces.map(pieceVersTexte);
export const TEXTES = new Map<string, Texte>([...livret, ...sources].map((t) => [t.id, t]));
export const corps = (id: string) => TEXTES.get(id)?.corps;

export const CALENDRIER = lire<Jour[]>('calendar/2026-2027.json');

/** Plan importé comme le fait l'app (importerPlan), pour l'année liturgique 2026-2027. */
export const PLAN: Pratique[] = pratiquesDuPlan(CALENDRIER, [...TEXTES.values()]).map((b) => ({
	...b,
	creeLe: '',
	modifieLe: ''
}));
