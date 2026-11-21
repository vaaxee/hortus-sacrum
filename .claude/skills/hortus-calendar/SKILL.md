---
name: hortus-calendar
description: Moteur du calendrier romain de 1954 d'Hortus Sacrum (engine/hebdo, data/calendar). À charger pour toute question ou modification sur le temps liturgique, la précédence, les rangs, commémoraisons, Quatre-Temps, vigiles, jeûne et abstinence, stations, Introït, Martyrologe, ou pour régénérer une année.
---

# Hortus Sacrum — calendrier

Références : `README.md` (« Générer une année »), `docs/cahier/SPEC.md` § 2, `SOURCES_UTILISEES.md` (Étape 1),
`docs/cahier/DECISIONS_ET_LIMITES.md`.

## Ce qui existe (un seul moteur : ne pas en créer un second)

- `engine/hebdo/` (Python 3) : `liturgy` (temps, précédence), `fasting` (CIC 1917, can. 1247, 1250-1254, indult
  français des fêtes de précepte), `stations` (Missel typique 1920), `enrich` (Introït, Martyrologe), `devotions`,
  `do.py` (lecteur des fichiers DO, conditions `rubrica` évaluées pour « Divino Afflatu - 1954 »), `build`.
- Sortie : `data/calendar/AAAA-AAAA.json` (champ `tempora`), copié par `app/scripts/seed.mjs`.
- `AAAA` = année du premier dimanche de l'Avent (`2026` → 2026-2027).
- `engine/legacy/` : ancien moteur, référence seulement.
- Pas de propre de France (décision du 12 nov.) ; calendrier romain universel.

## Données Divinum Officium (non versionnées)

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/DivinumOfficium/divinum-officium vendor/do
cd vendor/do && git sparse-checkout set web/www/Tabulae web/www/horas web/www/missa
git fetch --depth 1 --filter=blob:none origin 454a86ea && git checkout 454a86ea   # commit épinglé
```

**Épinglage obligatoire** : le dépôt DO change (corrections de traductions françaises). Au commit `454a86ea`
(13 nov. 2026) `compare_2026.py` donne 0 écart ; au HEAD de fin novembre, 52 écarts (noms français, une couleur).
L'Officium parvum a été construit au commit `c353daf` (voir `data/office/parvum.json` › `commit`) et son test passe
aux deux. Variable `HEBDO_DO` pour pointer ailleurs.

## Contrôle

```bash
cd engine && python3 tests/compare_2026.py      # doit afficher « 0 écart(s) sur 364 jours »
```

Référence : `data/source/calendrier_2026-2027.json` (calendrier papier validé). Écarts acceptés : `KNOWN` dans le script,
chacun justifié en commentaire.

## Modifier une règle liturgique

1. Documenter la règle et sa source (rubriques 1911 / *Divino afflatu*, CIC 1917, Missel 1920…), jamais « une autre
   tradition plus pratique ».
2. Écrire le test ou l'écart `KNOWN` justifié.
3. Régénérer l'année, relancer `compare_2026.py`, puis `npm run test` (l'unicité et la matrice lisent le calendrier).
4. Mettre à jour `SOURCES_UTILISEES.md` / `DECISIONS_ET_LIMITES.md`.

Ne pas confondre : numéro de semaine du mois (propriété calendaire, `Quand.semaines_du_mois`) et thème de la semaine
(dimension dévotionnelle, **non adopté**, voir skill `hortus-dimensions`).
