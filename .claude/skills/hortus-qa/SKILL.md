---
name: hortus-qa
description: Contrôle qualité d'Hortus Sacrum — chaîne de vérification obligatoire après chaque lot (check, lint, vitest, build, Playwright clair/sombre/téléphone, tests Python du moteur, audit des consignes). À charger avant de déclarer un travail terminé, d'ouvrir une PR, ou pour diagnostiquer un test qui échoue.
---

# Hortus Sacrum — QA

Références : `docs/PLAN_GENERAL.md` (« Après chaque lot »), `docs/cahier/SPEC.md` § 10 (corrections du 17 nov. au
soir, point 3) et § 11 (méthode de travail), `docs/audits/`.

## Préalables (environnement cloud)

```bash
cd app && npm ci                                  # dépendances
# vendor/do épinglé à 454a86ea : voir le skill hortus-calendar
```

## Chaîne obligatoire (dans `app/`)

```bash
npm run check          # svelte-kit sync + svelte-check : 0 erreur, 0 avertissement attendus
npm run lint           # ESLint : 0 problème (toute boucle {#each} a sa clé : règle en erreur)
npm run format:check   # Prettier
npm run test           # vitest : unicité et matrice sur toute l'année 2026-2027, pages composées mot pour mot
npm run build          # prébuild = seed.mjs (data/ → static/data)
npm run test:e2e       # Playwright : projets bureau-clair, bureau-sombre, telephone (après build)
node tests/historique.e2e.mjs   # scénarios de l'ancien bug « Internal Error » (après build)
npm run ordo -- <début> <fin>   # facultatif : rapport des manques de la matrice (docs/audits/ORDO_*.md)
```

Moteur Python, quand il est touché :

```bash
cd engine && python3 tests/compare_2026.py     # 0 écart(s) sur 364 jours
python3 engine/office/test_parvum.py           # 93 textes vérifiés
python3 engine/office/test_breviaire.py        # 0 faute, 0 écart d'oraison (calendrier ↔ moteur DO)
```

## Interface

- Nouveau parcours ou nouvelle page → l'ajouter à `app/tests/e2e/` (erreurs console, `pageerror`, pas de défilement
  horizontal au téléphone). L'écran d'accueil se ferme par « Entrer au jardin ».
- Captures : `deviceScaleFactor: 1` pour soi, 2 pour l'utilisateur ; vérifier les deux directions artistiques (latine,
  grecque), jour et nuit, la zone sûre de l'encoche.
- Accessibilité : contrastes de la charte (nacre/rubis, bordeaux/rubis vif, outremer), libellés ARIA des boutons-icônes.

## Revue et audit (après chaque lot)

1. Relire les fichiers modifiés ; skill `code-review` (ou `simplify` pour le nettoyage), `security-review` si Supabase,
   service worker ou entrée utilisateur.
2. Nettoyage : code mort, migrations devenues inutiles.
3. **Audit des consignes** : sites bannis, secrets (rien de Supabase hors du Vault), textes sans source, textes de
   mémoire. Modèle : `docs/audits/AUDIT_CONSIGNES_2026-11-20.md`.
4. Documentation vivante à jour (REPRISE, REFONTE, LOT_DIMENSIONS, A_FOURNIR, SOURCES_UTILISEES).

Un échec se rapporte tel quel, avec la sortie ; on ne désactive ni ne contourne un test (unicité comprise).
