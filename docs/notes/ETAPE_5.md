# Étape 5 — Pratiques et calendrier personnels

## Fait
- **Règles de dates** (`app/src/lib/pratiques.ts`) : jours de suite, jours avant une fête, jour de chaque mois (premier vendredi, veille), jour fixe, mois entier, jour de chaque semaine. Compteur n/N, série en cours ou à venir, jours manqués, « recommencer aujourd'hui ».
- **Jours manqués** : comptés seulement après le premier jour coché d'une série. Une série commencée avant l'installation, ou jamais suivie, n'apparaît pas « interrompue ».
- **Plan de l'année → pratiques modifiables** (`plan.ts`) : au premier lancement, les dévotions du calendrier (année liturgique en cours et suivante) deviennent des pratiques avec leur règle. Sur 2026-2027, elles retombent exactement sur les dates du calendrier papier (tests).
- **Dévotions** : « En cours », « À venir », « Chaque mois, chaque année », avec médaillon de compteur et alerte de série interrompue ; bouton « Reprendre le plan de l'année ».
- **Fiche d'une pratique** : jours de la série à cocher ; en cas d'interruption, « Recommencer aujourd'hui » ou « Je les avais faits » ; prières liées, promesses, indulgence, source ; modifier, dupliquer, masquer, restaurer l'original, corbeille.
- **Ajouter une pratique** : à partir d'un modèle (neuvaine, trentain, série, consécration), puis formulaire complet.
- **Fêtes et anniversaires** (Profil → Fêtes, saints et anniversaires) : anniversaires spirituels, saints favoris et fête patronale, fêtes locales ; jour, mois, année facultative, rappel la veille, notes ; corbeille.
- **Aujourd'hui** : les pratiques du jour remplacent les deux lignes génériques, avec case et compteur ; vos fêtes du jour, avec le nombre d'années (« 26e anniversaire ») ; note du jour.
- **Calendrier** : bascule Mois / Semaine. La vue semaine (dimanche à samedi) montre office, rang, commémoraisons, jeûne, vos pratiques et vos fêtes, avec des filtres. Le mois liste aussi vos fêtes.

## Vérifié
- Tests : 45 sur 45. Contrôle de types : 0 erreur.
- Navigateur, largeur de téléphone : création d'une neuvaine, coche du premier jour (1 sur 9), présence sur Aujourd'hui ; ajout d'un baptême, visible sur Aujourd'hui et dans la semaine ; vue semaine avec ses filtres. Données d'essai effacées ensuite.

## Pas fait
- Les rappels « la veille » sont enregistrés mais n'envoient rien (étape 7).
- La vue semaine n'a pas été regardée sur grand écran.
