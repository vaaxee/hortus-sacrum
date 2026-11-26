---
name: hortus-ordo
description: Programme unique et calcul de la journée d'Hortus Sacrum (journee(), data/programme/programme.json, Quand, Choix, insertions, pages composées, unicité, surcouche utilisateur). À charger avant toute modification de la liste du jour, d'une pratique, d'une page composée, d'une rotation, d'un point d'insertion ou de la migration Dexie.
---

# Hortus Sacrum — ordo du jour (programme unique)

Références : `docs/conception/REFONTE_2026-11-18.md` (§ 2, § 2.10 et § 2.8 « Réalisé »), `docs/cahier/SPEC.md` § 11,
`docs/LISTE_DU_JOUR.md`, `docs/audits/AUDIT_DEVOTIONS_2026-11-18.md`.

## Architecture à préserver

```
data/programme/programme.json (livré, revision par entrée)
  ⊕ table Dexie « programme » (surcouche : actif, ordre, durée, rappels, ajouts personnels)
  ⊕ contexte du jour (data/calendar, pratiques du plan, roues)
        ↓
journee(programme, ctx)   — fonction pure, app/src/lib/programme/journee.ts
        ↓
Journee { lignes, lectures, contexte, couverture, manques, … }
        ↓
Aujourd'hui · /pratique/[id] · Imprimer › jour · rappels · historique · tests
```

Interdits : revenir aux migrations ponctuelles dans `seed.ts` ; stocker la liste du jour ; un second moteur ou un
second système de règles `Quand` ; tirage aléatoire dans la journée.

## Vocabulaire (`app/src/lib/programme/types.ts`)

- `Quand` : `jours_semaine`, `semaines_du_mois`, `mois`, `tempora`, `dates` (« MM-JJ » / « AAAA-MM-JJ »), `office`
  (regex), `code_tempora` (code du temporal, « Quadp3-2 »), `ou`, `sauf`. Même vocabulaire que `indulgences.json`.
- `Choix` : identifiant, `selon: 'jour_semaine' | 'rotation' | 'quand' | 'saint_du_jour'`. Un choix donne **un** texte ou rien.
- `Extrait` : `section`, `de`/`a`, `phrase`, `retirer`, `rang_du_jour` — ancres **exactes**, vérifiées par test.
- `Section` : `texte`, `notice`, `point`, `champ`, `editorial` (titre de mise en page), `partie` (titre repliable qui regroupe
  les sections suivantes ; `replie` = fermée à l'ouverture).
- `Insertion` / `Coupure` : points d'insertion (`repartir` : une section par passage d'un point répété, fruit de chaque mystère) (fin de dizaine, Angélus, prières du matin et du soir, fin de l'office du saint).
- `EntreeProgramme.motif` : descriptif, ne filtre rien.

## Règles

1. **Unicité** : un texte une seule fois par jour, y compris dans les pages composées (inclusion : fragments de 8 mots,
   un tiers retrouvé, `fragments()` dans `texte.ts`). Doublon → corriger la composition, jamais masquer à l'interface.
   Seules exceptions : les formules communes déclarées dans `programme.json › formules` (signe de croix, Gloria Patri…).
2. **Intégrer plutôt qu'ajouter** (SPEC § 11.2) : insérer dans une séquence hôte plutôt que créer une ligne.
3. **Déterminisme** : même date + même contexte → même journée. Les roues sont des rotations déterministes.
4. **Texte jamais réécrit** pour la mise en page : pages = extraits par ancres, `editorial` pour les seuls titres de mise en page.
5. **Surcouche** : une correction livrée (`revision`) n'écrase jamais un réglage de l'utilisateur ; lignes modifiées
   reprises avec la page « Ce qui a changé » (`/programme/changements`).
6. Un texte cité doit exister dans `data/prieres/sources.json` ou `jardin.json` ; sinon `a_fournir` dans `programme.json`
   et `A_FOURNIR.md`.
7. **Prières obligatoires** (lignes `praecipua` : matin et offrande, Angélus, chapelet, soir ; décision du 26 nov.) :
   chaque prière dite a un titre (indulgence Ench. 1952, prescription de l'Église ou d'une archiconfrérie, promesse
   attestée) ; un texte sans titre est **remplacé** par un texte ancien de même fonction (jamais ajouté en plus), en
   coupant l'hôte par ancres (`a` / `de`, morceaux suivants en `suite: true`) ; sans remplaçant, il reste. Tableau
   élément par élément : `docs/audits/PRIERES_OBLIGATOIRES_2026-11-26.md`.

## Tests à faire passer (vitest, sur toute l'année 2026-2027)

`journee.test.ts`, `unicite.test.ts`, `composees.test.ts` (pages composées mot pour mot contre
`programme/references/pages-composees.json`), `migration.test.ts`, `heures.test.ts`, `matrice.test.ts`, `bilan.test.ts`.

Avant une modification structurelle : `mcp__Graphify__graphify_impact` / `graphify_callers` sur le symbole touché
(le graphe est à jour quand son `commitSha` = `git rev-parse HEAD`).
