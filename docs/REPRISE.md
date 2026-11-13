# Reprise du travail (session cloud / téléphone)

À lire en premier par toute nouvelle session Claude. Lire ensuite `docs/PLAN_ETAPES.md`, `docs/LISTE_DU_JOUR.md`, `SOURCES_UTILISEES.md`, `A_FOURNIR.md`.

## Règles absolues

- Aucun texte de prière, de méditation, de vie de saint ou d'indulgence écrit de mémoire. Uniquement des sources anciennes identifiées, recopiées mot pour mot, avec leur référence. Texte introuvable : l'inscrire dans `A_FOURNIR.md` et le demander.
- Prières courantes : seulement sites sédévacantistes et/ou FSSPX (ex. La Porte Latine), ou Catholique de France.
- **Bannis** : Hozana, Aleteia, Notre-Dame de Chrétienté — ne jamais utiliser ni citer.
- Exception : Guéranger, *L'Année liturgique*, transcrit par l'abbaye Saint-Benoît de Port-Valais.
- Éviter l'OCR quand une transcription propre existe ; sinon corriger l'OCR en relisant les scans (archive.org, Gallica).
- Arbitrage : piété, cohérence, praticité, tradition. Tout doit rester modifiable dans l'app.
- Secrets Supabase (VAPID, clé cron) : dans le Vault, jamais dans le dépôt.

## Déploiement

Chaque push sur `main` reconstruit automatiquement https://hortus-sacrum.vercel.app (≈ 30 s ; Vercel : racine `app`, `npm run build`, dont le prebuild lance `scripts/seed.mjs` qui copie `data/` vers `app/static/data`). `deployer.ps1` ne sert plus. Avant de pousser : `npm run check` et `npm run build` dans `app/`.

## Architecture en bref

- SvelteKit (Svelte 5 runes, adapter-static) dans `app/`, Dexie local-first, imports `#lib/*`.
- Données : `data/prieres/sources.json`, `data/recueils/` (hamon, chaignon, breviaire, mois-*, gueranger/index + vNN), `data/calendar/*.json` généré par `engine/hebdo` (champ `tempora`).
- Livraison des textes aux appareils existants : étapes de migration dans `app/src/lib/seed.ts` (une méta par étape ; ne pas écraser ce que l'utilisateur a modifié, comparer `modifieLe === DEPART`).
- Méditation du jour : `app/src/lib/meditations.ts` (livre du mois d'abord, sinon Hamon dimanches et temps forts, Chaignon en semaine ordinaire ; Guéranger = lecture).
- Rappels push : Supabase `jlbcpkmysmdehjocqzmb`, `supabase/functions/*`, sans compte (identifiant d'appareil).
- Charte : grecque (outremer `#0E0C52`, cobalt) et latine (nacre `#faf5ef` / rubis `#7a1f2b` le jour ; bordeaux `#22080f` / rubis vif `#f08593` la nuit) ; motifs fleur de lys, croix pattée, rinceaux.

## Reste à faire

1. **Guéranger** depuis la transcription de Port-Valais : remplacer `data/recueils/gueranger/*.json` (clés `T:<tempora>`, `D:MM-DD`, `F:…`) par le texte propre.
2. **OCR à corriger sur scans** : d'abord novembre (Berlioux, `data/recueils/mois-purgatoire.json`, ex. « ^^^REMiER POINT »), puis Hamon, Chaignon, autres livres de mois.
3. **Étape 10** : PDF (livret de prières 110×170, fiche du jour, calendrier mensuel) ; historique (régularité par dévotion, grille de constance) ; profil spirituel (sacrements, consécrations, fête patronale, saints préférés avec rappel la veille).
4. Optionnel : formule de renouvellement de la consécration au cordon (non trouvée), litanies du lundi/mardi/jeudi, prières de la dévotion du dimanche, livre du mois de juillet, `{{ .Token }}` dans le modèle d'e-mail Supabase.
