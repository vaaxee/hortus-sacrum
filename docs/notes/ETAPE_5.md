# Étape 5 — Pratiques et calendrier personnels (en cours)

## Fait
- **Règles de dates** (`app/src/lib/pratiques.ts`) : jours de suite, jours avant une fête, jour de chaque mois (premier vendredi, veille), jour fixe, mois entier, jour de chaque semaine. Compteur n/N, série en cours ou à venir, jours manqués, « recommencer aujourd'hui ».
- **Plan de l'année → pratiques modifiables** (`plan.ts`) : au premier lancement, les dévotions du calendrier (année liturgique en cours et suivante) deviennent des pratiques avec leur règle. Sur 2026-2027, elles retombent exactement sur les dates du calendrier papier (tests).
- **Dévotions** : liste « En cours », « À venir », « Chaque mois, chaque année », avec médaillon de compteur et alerte de série interrompue ; bouton « Reprendre le plan de l'année ».
- **Fiche d'une pratique** : jours de la série à cocher, alerte « Série interrompue » avec « Recommencer aujourd'hui » ou « Je les avais faits », prières liées, promesses, indulgence, source ; modifier, dupliquer, masquer, restaurer l'original, corbeille.
- **Ajouter une pratique** : modèles neuvaine, trentain, série, consécration, puis formulaire complet.
- **Aujourd'hui** : les pratiques du jour remplacent les deux lignes génériques, avec case et compteur ; fêtes personnelles du jour ; note du jour.

## Vérifié
- Tests : 44 sur 44. Contrôle de types : 0 erreur.
- Navigateur : l'écran Dévotions s'ouvre, 54 pratiques importées, sans erreur.

## Pas vérifié
- La fiche d'une pratique, la création, les coches de série, et les pratiques sur l'écran Aujourd'hui n'ont pas été essayées dans le navigateur.
- Les séries de l'année en cours apparaissent « interrompues » puisqu'aucun jour passé n'a été coché : à traiter (ne compter les manques qu'à partir du premier jour coché ou de l'installation).

## Pas fait
- Éditeur des fêtes, saints et anniversaires personnels (le modèle et l'affichage du jour existent, pas l'écran de saisie).
- Vue semaine du calendrier ; fêtes personnelles dans le calendrier.
