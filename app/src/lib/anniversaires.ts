/**
 * Anniversaires du profil spirituel (baptême, confirmation, première communion, mariage, ordination, consécrations) :
 * prières d'action de grâces proposées ce jour-là, toutes tirées de sources anciennes.
 */
export const ACTIONS_DE_GRACES: Record<string, [string, string][]> = {
	bapteme: [
		['thesaurisons:au-christ-roi', 'Rénover les promesses du baptême'],
		['paroissien:te-deum', 'Te Deum']
	],
	defaut: [
		['paroissien:te-deum', 'Te Deum'],
		['thesaurisons:action-de-graces', 'Action de grâces']
	]
};

const ANNIVERSAIRES = ['bapteme', 'confirmation', 'communion', 'mariage', 'ordre', 'consecration'];

/** Prières d'action de grâces pour une date du profil, ou rien si ce n'est pas un anniversaire (saint patron…). */
export function actionsDeGraces(profil?: string): [string, string][] {
	if (!profil || !ANNIVERSAIRES.includes(profil)) return [];
	return ACTIONS_DE_GRACES[profil] ?? ACTIONS_DE_GRACES.defaut;
}
