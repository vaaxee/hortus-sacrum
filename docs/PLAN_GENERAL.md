# Plan général d'Hortus Sacrum (17 novembre 2026)

Ce document est la référence commune de tous les agents. Les consignes de `docs/REPRISE.md` et de `docs/cahier/SPEC.md`
(surtout le § 10) s'imposent à tous.

## Consignes communes (rappel)

- **Aucun texte de prière, de méditation, de vie de saint ou d'indulgence écrit de mémoire.**
  - On n'utilise que des sources anciennes identifiées, recopiées mot pour mot, avec leur référence (ouvrage, édition,
    page).
  - Un texte introuvable s'inscrit dans `A_FOURNIR.md`.
- **Prières courantes** : on les prend seulement sur des sites sédévacantistes ou FSSPX (ex. La Porte Latine), ou sur
  Catholique de France.
- **Bannis** : Hozana, Aleteia, Notre-Dame de Chrétienté. On ne les utilise pas et on ne les cite jamais.
- **OCR** :
  - on l'évite quand une transcription propre existe ;
  - sinon, on corrige l'OCR en relisant les scans ;
  - on garde l'orthographe de l'édition.
- **Arbitrage** : piété, cohérence, praticité, tradition. Tout reste modifiable dans l'app.
- **Ne jamais écraser une modification de l'utilisateur.**
  - Pour corriger un texte déjà livré, on incrémente son champ `revision` (dans `data/prieres/sources.json`). L'app le
    remplace alors, sauf si l'utilisateur l'a modifié.
  - Les recueils de méditations (`data/recueils/*.json`) sont relus à chaque lancement de l'app.
- **Secrets** : ils vont dans le Vault de Supabase, jamais dans le dépôt.
- **Après chaque lot** :
  - lint, check, tests et build ;
  - audit des consignes ;
  - PR fusionnée dans `main`.

## Rôles

| # | Rôle | Fichiers dont il a la charge | Quand |
|---|---|---|---|
| 1 | **Transcripteur** : scans → texte propre relu, avec référence | `data/prieres/sources.json`, `engine/recueils/*` (nouveaux scripts) | En continu |
| 2 | **Relecteur des méditations** : relecture sur les scans, dans l'ordre d'affichage | `data/recueils/*.json`, `engine/recueils/relecture/*` | En continu |
| 3 | **Gardien des consignes** : sources, références, indulgences, A_FOURNIR | lecture seule, `A_FOURNIR.md`, docs | Après chaque lot |
| 4 | **Ingénieur de l'app** : fonctionnalités, migrations Dexie, pages du jour | `app/src/lib`, `app/src/routes` | Par lot |
| 5 | **Qualité** : ESLint, Prettier, tests vitest et Playwright, Lighthouse | configuration de `app/`, tests | Par lot |
| 6 | **Esthétique et accessibilité** : charte, typographie, mobile, contrastes, mode sombre | CSS, `app/src/lib/design` | Par lot |
| 7 | *(optionnel)* **Liturgie** : martyrologe, ordo, temps, fêtes | `engine/calendrier`, `data/calendar` | Si besoin |

Le chef d'orchestre (la session principale) :
- fusionne le travail des agents ;
- vérifie ;
- fait l'audit ;
- tient ce plan à jour.

Chaque agent ne touche que ses fichiers, pour éviter les conflits.

## Chantiers

**En cours**
- **Transcripteur** : la fin du *Petit bréviaire du Sacré-Cœur* (exercice pendant la messe, litanies, neuvaine) ; les
  compléments de la Sainte Face (Janvier 1895) ; l'Apostolat de la prière (offrande et pratiques, Ramière ou Gautrelet,
  sans les intentions mensuelles récentes).
- **Relecteur** : relecture de toutes les méditations, dans l'ordre d'affichage.

**À venir**
- Les prières de sainte Gertrude, quand l'utilisateur aura choisi lesquelles transcrire.
- La traduction française ancienne des invocations du Sub tuum.

**Faits**
- Mise en place du lint (ESLint et Prettier).

## Outils (relevé du 21 novembre 2026)

- **Skills du projet** (`.claude/skills/`, versionnés) : `hortus-sources`, `hortus-liturgie`, `hortus-ordo`,
  `hortus-dimensions`, `hortus-calendar`, `hortus-content`, `hortus-ocr`, `hortus-qa`.
- **Sous-agents du projet** (`.claude/agents/`) : `hortus-architecte`, `hortus-frontend`, `hortus-qa`, `hortus-sources`,
  `hortus-liturgie` (rôles ci-dessus, chacun limité à ses fichiers).
- **Skills de la session** : `code-review`, `simplify`, `security-review`, `pdf`, `skill-creator`, `deep-research`.
- **Connecteurs** : GitHub, Supabase (projet `jlbcpkmysmdehjocqzmb`), Vercel, Graphify, Context7 (documentation
  technique), Parallel Search (recherche web), Linear (non utilisé).
- **Tests de bout en bout** : Playwright (`@playwright/test` 1.63.0, version du Chromium installé), `npm run test:e2e`
  après `npm run build` ; projets bureau-clair, bureau-sombre, telephone.
- **OCR** : Tesseract 5 (fra, lat), à réinstaller dans une session neuve (`hortus-ocr`).
- **Divinum Officium** : `vendor/do` épinglé au commit `454a86ea` (0 écart de `compare_2026.py`).
- **Graphify** : graphe du code (`app/`, `engine/`, docs), sans les données ni les PDF (`.graphifyignore`).
  - Connecteur : `graphify_impact`, `graphify_callers`, `graphify_find`, `query_graph`… ; le graphe vaut pour le commit
    indiqué par `commitSha` (à comparer à `git rev-parse HEAD`). Offre gratuite : seul `README.md` est indexé parmi les
    documents.
  - En local (si installé) : `graphify update .` (sortie dans `graphify-out/`, non versionné).
  - À utiliser avant chaque refonte, pour mesurer l'impact d'un changement.
