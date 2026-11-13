/** Étiquette courte de l'origine d'un texte : le manuel ou l'auteur ; la référence complète reste sur la page du texte. */
export function etiquetteSource(o: { origine: string; source?: { ouvrage?: string; edition?: string } }): string {
	if (o.origine === 'livret') return 'Livret';
	if (o.origine === 'personnel') return 'Ajout personnel';
	const ouvrage = o.source?.ouvrage ?? '';
	const annee = (o.source?.edition ?? '').match(/1[5-9]\d\d/)?.[0];
	if (/^Paroissien romain/i.test(ouvrage)) return `Paroissien romain${annee ? `, ${annee}` : ''}`;
	if (/^Beringer/i.test(ouvrage)) return `Beringer, Les Indulgences${annee ? `, ${annee}` : ''}`;
	if (!ouvrage) return 'Source ancienne';
	// « Auteur, Titre, … » → « Auteur, Titre » ; sinon le début du titre
	const morceaux = ouvrage.split(/,\s*/);
	const court = morceaux.length > 1 && morceaux[0].length < 40 ? `${morceaux[0]}, ${morceaux[1]}` : morceaux[0];
	return court.length > 48 ? court.slice(0, 46).trimEnd() + '…' : court;
}
