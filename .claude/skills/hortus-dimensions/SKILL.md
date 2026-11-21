---
name: hortus-dimensions
description: Matrice dévotionnelle d'Hortus Sacrum (dimensions fin, objet, grâce, personne, forme ; cycles ; contexte, couverture, manques ; lots D1-D5). À charger avant de classer un texte, d'étendre le vocabulaire, de toucher cycles.json, contexte.ts, matrice.test.ts, ou de concevoir le compositeur d'ordo.
---

# Hortus Sacrum — dimensions

Référence : `docs/conception/LOT_DIMENSIONS.md` (elle prime). Principe : **on compose à la conception ; la journée
reste fixe à l'exécution.** La matrice décrit, vérifie, propose ; elle ne choisit jamais seule ce qui est prié.

## Système existant (le seul : pas de second système de tags)

| Élément | Fichier |
|---|---|
| Vocabulaire fermé, libellés, `fins_principales` | `data/programme/dimensions.json` |
| Classement des textes (`releve`, `devinee`) | `data/prieres/dimensions-textes.json` (89 textes ; **0 relu** au 21 nov.) |
| Cycles (jour de semaine, mois, temps ; `semaine_du_mois` **vide**) | `data/programme/cycles.json` |
| Types `Dimension`, `Dimensions`, `ContexteDevotionnel`, `Couverture` | `app/src/lib/programme/types.ts` |
| Contexte, couverture, manques | `app/src/lib/programme/contexte.ts`, appelés dans `journee()` |
| Déduction par motifs (brouillon → `devinee`) | `app/src/lib/etiquettes.ts`, `app/src/lib/dimensions.ts`, `app/scripts/dimensions.mjs` |
| Relecture dans la fiche | `app/src/lib/ClassementTexte.svelte`, `FicheTexte.svelte` |
| Tests | `app/src/lib/programme/matrice.test.ts`, `dimensions.test.ts`, `etiquettes.test.ts` |

État des lots : voir `LOT_DIMENSIONS.md` § 7, « État des lots ». D1, D3 et D4 (`motif` sur chaque entrée) faits ;
D2 (relecture humaine) à faire.

## Distinctions (ne jamais fusionner)

- **fin** : ce que fait l'acte (adoration, action de grâces, réparation, propitiation, demande, intercession, louange…) ;
- **objet** : vers qui/quoi il porte (Trinité, Passion, Sacré-Cœur, sainte Vierge, saint Joseph, âmes du purgatoire…) ;
- **grâce** : ce qui est demandé (sens actuel du projet : ne pas renommer ni fusionner) ;
- **personne** : pour qui (soi-même, famille, pécheurs, Église et prêtres, mourants, défunts…) ;
- **forme** : comment (oraison, litanie, chapelet, office, méditation, lecture, examen, jaculatoire…) ; ex-`pratique`.

Les intentions particulières de l'utilisateur ne sont pas une dimension des textes.

## Règles d'extension

- Ajouter une valeur : dans `dimensions.json` (et ses libellés), jamais en dur dans le code ; ne jamais supprimer une
  valeur livrée utilisée. Valeurs évoquées mais **absentes** aujourd'hui (expiation, contrition, satisfaction, offrande,
  jeûne, aumône, visite, communion…) : à ajouter seulement sur décision explicite.
- Une dimension nouvelle (temporelle ou dévotionnelle) à sémantique propre devient un champ indépendant typé, pas une
  chaîne générique.
- **Thème de la semaine du mois : non adopté.** Ne pas remplir `semaine_du_mois` ni activer le test 6 sans décision
  explicite de l'utilisateur et conception écrite (question 1 du § 8).
- Le contexte **ne retire ni n'ajoute** de ligne ; ce qui varie s'écrit en `Quand` / `{ selon: 'quand' }` dans le programme.
- Traçabilité : chaque valeur du contexte garde son origine (`sources: { dimension, valeur, de }`).
- Un classement livré doit être relu (`releve`) avant d'entrer dans un test bloquant ; sinon le test avertit.
- La surcouche utilisateur remplace la donnée livrée dimension par dimension ; changer un classement ne marque pas le
  texte comme modifié (il continue de recevoir ses `revision`).
