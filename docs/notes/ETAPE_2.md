# Étape 2 — Socle modifiable : ce qui a changé

## Décisions reportées
- Vos réponses du 12 novembre sont dans `A_FOURNIR.md` et `docs/LISTE_DU_JOUR.md`.
- `docs/cahier/SPEC.md` a un nouveau §9, « Tout est modifiable ». Le plan révisé est dans `docs/PLAN_ETAPES.md`.

## L'app (dossier `app/`)
- SvelteKit 3 en TypeScript, entièrement statique. Les données vivent dans le navigateur (IndexedDB) ; la synchronisation viendra s'y brancher à l'étape 6.
- **Modèle de données** (`src/lib/types.ts`, `src/lib/db.ts`) pour les prières, pratiques, éléments de liste, recueils, méditations, fêtes personnelles et notes. Tout objet porte :
  - son **origine** : « Livret », « Source officielle vérifiée » ou « Ajout personnel » ;
  - une copie de son **original**, pour « Restaurer l'original » ;
  - un **historique des versions** ;
  - une **corbeille** : suppression en deux temps.
- **Bibliothèque de prières** : les 62 pièces du livret, classées par partie ; recherche sans accents ; favoris ; filtre « Mes ajouts » ; badges.
- **Fiche d'une prière** : français, latin dépliable, indulgence, source dépliable. Actions : modifier, dupliquer, favori, historique, restaurer l'original, corbeille.
- **Éditeur au clavier** : boutons ℣, ℟, rouge, italique, intertitre ; colonne latine en option ; aperçu.
- **Copier-coller** : le nettoyage recolle les mots coupés, retire les sauts de ligne parasites et les espaces doubles, reconnaît ℣ et ℟ et détache le titre. Il affiche ce qu'il a changé, et vous corrigez dans l'aperçu avant d'enregistrer. Il ne change aucun mot.
- **Réglages** : export complet en JSON ; import par fusion ou par remplacement ; corbeille.
- **Aujourd'hui** : pour l'instant, seulement le bandeau liturgique du jour.

## Vérifié
- Tests du nettoyage et du rendu : 7 sur 7.
- Contrôle de types : 0 erreur. Compilation : réussie.
- Dans le navigateur :
  - modification d'une prière du livret, puis badge « modifié », historique et restauration de l'original ;
  - collage d'un texte d'essai, enregistré comme « Ajout personnel », mis à la corbeille puis supprimé ;
  - export puis import ;
  - affichage en largeur de téléphone.

## Pas encore fait
- Import PDF et photo avec OCR : étape 3.
- Les éditeurs de la liste du jour, des pratiques, des recueils et du calendrier personnel. Leur modèle de données existe ; les écrans viennent aux étapes 4, 5 et 9.
- Export PDF d'une sélection : étape 10.
- Fonctionnement hors ligne complet et installation sur iPhone : à faire avec la mise en ligne, étape 6.
