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

1. **Guéranger** : **fait en partie** (13 nov.) : 202 lectures sur 423 reprises du texte propre de domgueranger.net (Avent → temps pascal) et d'abbe-pivert.com (jours et saints choisis jusqu'au temps après la Pentecôte), appariées à l'OCR par recoupement de suites de mots (`engine/recueils/relecture/gueranger/`). Ces transcriptions omettent les pièces latines. Restent en OCR surtout les t. 8, 9, 12-15 (temps après la Pentecôte, sanctoral de juin à novembre) : à corriger sur scans comme Berlioux, ou à reprendre d'une autre transcription.
2. **OCR à corriger sur scans** : novembre (Berlioux) **fait** (méthode et scripts dans `engine/recueils/relecture/`) ; restent Hamon, Chaignon, les autres livres de mois.
3. **Étape 10** : **faite** (14 nov.) : `/imprimer` (livret 110 × 170, fiche du jour A5, calendrier A4), `/historique`, `/profil`, liens depuis l'onglet Profil.
4. **Roue symbolique** : **faite** (14 nov.) : `/roue`, `app/src/lib/roues.ts`, données `data/roues.json` (générées par `engine/roues/construire.py` à partir de la Vulgate clémentine). Départ : premier dimanche de l'Avent.
   - **À remplir (demande du 14 nov.)** : chaque élément de chaque roue doit mener à un texte à lire ou à prier. Liées : vertus théologales, plaies, douleurs de Marie, dons du Saint-Esprit, douleurs de saint Joseph, Credo, mystères du Rosaire, chapelets. **Vides (20 roues)** : un Dieu, Trinité, mages, œuvres satisfactoires, concupiscences, fins dernières, évangélistes, vertus cardinales, sacrements, vices capitaux, œuvres de miséricorde (2), demandes du Pater, sept paroles, psaumes de la pénitence (6 sur 7), béatitudes, chœurs des anges, commandements, fruits du Saint-Esprit, apôtres, et la lecture des Évangiles (89 chapitres : texte du chapitre absent). Exemple de l'utilisateur : choisir « les 4 évangélistes » doit permettre de lire le chapitre d'Évangile du jour. Se fait au fur et à mesure, sources anciennes seulement.
5. Optionnel restant : litanies des défunts (lundi) introuvables ; formule de renouvellement du cordon (non trouvée) ; modèle d'e-mail avec code (`supabase/modeles/lien-magique.html`) : **abandonné** (14 nov.), Supabase interdit de modifier les modèles en offre gratuite sans SMTP personnalisé ; l'utilisateur s'en passe (les rappels ne dépendent pas du compte). Faits : litanies du dimanche, mardi, jeudi ; dévotion du dimanche ; mois de juillet (Boylesve).
