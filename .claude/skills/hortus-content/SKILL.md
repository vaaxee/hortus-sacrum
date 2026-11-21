---
name: hortus-content
description: Ajout et correction de contenu dans les données d'Hortus Sacrum (data/prieres/sources.json, jardin.json, recueils, indulgences.json, programme.json › a_fournir, roues), livraison aux appareils (revision, seed), balisage. À charger avant d'écrire dans data/ ou d'ajouter une pièce, un recueil ou une méditation.
---

# Hortus Sacrum — contenu

Charger d'abord `hortus-sources` (provenance). Références : `docs/PLAN_GENERAL.md`, `docs/REPRISE.md` (Architecture),
`docs/cahier/SPEC.md` § 9.

## Où vit chaque contenu

| Contenu | Fichier | Produit par |
|---|---|---|
| Livret *Le Jardin de l'âme* (62 pièces) | `data/prieres/jardin.json` | `engine/livret/extract.py` |
| Textes sourcés (`paroissien:`, `beringer:`, `janvier:`, `gertrude:`, `ramiere:`…) | `data/prieres/sources.json` (`{ note, pieces[] }`) | transcription relue, scripts `engine/recueils/*`, `engine/indulgences/*` |
| Indulgences (Ench. 1952) | `data/prieres/indulgences.json` | `engine/indulgences/{ench1952,verif1952,beringer1925,thesaurisons_livret}.py` |
| Classements | `data/prieres/dimensions-textes.json` | voir `hortus-dimensions` |
| Recueils de méditations | `data/recueils/*.json`, `gueranger/` | `engine/recueils/*.py` |
| Écriture | `data/ecriture/<livre>.json` | `engine/ecriture/bible.py` |
| Roues | `data/roues.json` | `engine/roues/construire.py` |
| Office | `data/office/parvum.json` | `engine/office/parvum.py` |
| Programme | `data/programme/*.json` | à la main, voir `hortus-ordo` |

`app/scripts/seed.mjs` (prédev/prébuild) copie `data/` vers `app/static/data` : tout nouveau fichier de données doit y
être ajouté.

## Forme d'une pièce

```json
{ "id": "ouvrage:slug", "titre": "…", "partie": "…", "categorie": "", "usage": "…", "indulgence": "",
  "source": { "ouvrage": "…", "edition": "Lieu, éditeur, année", "page": "7-12", "url": "https://archive.org/details/…" },
  "latin": "", "corps": "…", "revision": 2 }
```

Balisage : `*italique*` (rubriques imprimées en italique), `## intertitre`, `℣`/`℟`, `[r]…[/r]` rubriques non comptées
dans les durées. Rendu par `app/src/lib/markup.ts` (seul usage de `{@html}`).

## Livraison sans écraser l'utilisateur

- Correction d'un texte déjà livré : **incrémenter `revision`** (sources.json, et pièces du livret via
  `revisionsDuLivret`). `seed.ts › reviser()` remplace le texte seulement s'il n'a pas été modifié (meta `revisions`).
- Recueils : relus à chaque lancement.
- Programme : donnée livrée + surcouche Dexie ; jamais de migration destructive sans archivage (historique des versions,
  corbeille).
- Un texte retiré : corbeille si non modifié, jamais suppression sèche.

## Après chaque ajout

`SOURCES_UTILISEES.md` mis à jour ; `A_FOURNIR.md` pour ce qui manque ; puis la chaîne du skill `hortus-qa`
(les tests `donnees-anciennes`, `indulgences`, `unicite`, `composees` lisent `data/`).
