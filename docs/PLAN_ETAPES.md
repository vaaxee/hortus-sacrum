# Plan des étapes (révisé le 12 novembre 2026)

Remplace CONSIGNE §4. Validation de l'utilisateur à la fin de chaque étape.

| # | Étape | Contenu | État |
|---|---|---|---|
| 1 | Données | Moteur du calendrier pour toute année ; 62 pièces du livret en base | faite |
| 2 | **Socle modifiable** | App installable (PWA) ; modèle de données où tout est éditable (origine, versions, corbeille, restauration de l'original) ; bibliothèque de prières ; éditeur au clavier ; saisie par copier-coller avec nettoyage et aperçu ; export et import JSON | faite |
| 3 | Import PDF et photo | pdf.js, plage de pages ; OCR Tesseract.js (français, latin) ; découpage en pièces ; source pré-remplie | faite |
| 4 | Aujourd'hui et liste du jour | Bandeau liturgique, martyrologe et invocations ; liste à cocher éditable (glisser-déposer, jours, heure de rappel, pièces répétées dans la journée) ; chaque ligne ouvre sa prière | faite, à valider (restent : lecture de Prime, vie du saint) |
| 5 | Pratiques et calendrier personnels | Éditeur de pratiques (règles de dates, prières liées, promesses, indulgence, source) ; compteurs et séries interrompues ; fêtes et saints personnels, anniversaires, notes ; vues mois et semaine | faite, à valider |
| 6 | Compte et synchronisation | Supabase (lien magique, règles par utilisateur) ; synchronisation téléphone et PC ; mise en ligne | à faire |
| 7 | Rappels | Notifications push ; écran d’aide iPhone | fait (13 nov.) |
| 8 | Contenu sourcé | Paroissien 1890 (matin, soir, litanies, Angélus) ; chapelet des Morts ; cordon de S. Joseph ; Sacré-Cœur ; dons du Saint-Esprit | fait (13 nov.) ; restent des litanies (défunts, saints Anges, Saint-Sacrement) et la formule du cordon |
| 9 | Méditations et vies de saints | Éditeur de recueils (découpage par jours, affectation) ; Guéranger, « mois » ; leçons du Bréviaire | fait (13 nov.) : Hamon, Chaignon, Guéranger, Bréviaire, mois ; éditeur de recueils fait (21 nov., lot 11) |
| 10 | Finitions | Export PDF d'une sélection ; historique et régularité ; profil spirituel | à faire |

Somme théologique (lot 10 de `docs/conception/REFONTE_2026-11-18.md` § 6, 22 nov.) : Iª q. 1-5 (30 articles) livrées
dans `data/somme` (Lachat, Vivès 1880, relu sur l'image ; latin léonin du Corpus Thomisticum) ; page
`/lecture/doctrine`, marque-page (meta `marque-somme`), lecture comptée dans « Lectures du jour ». Iª q. 6-11 livrées le 25 nov. Suite : q. 12-13.

Ordre voulu : l'éditeur passe avant le contenu, pour que tout texte ajouté ensuite soit d'emblée modifiable.

| — | Identité Hortus Sacrum | Jetons, ornements, deux directions artistiques (latine, grecque), jour et nuit, appliqués à toute l'app | faite, à valider |
