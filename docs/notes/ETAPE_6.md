# Étape 6 — Compte et synchronisation (en cours)

## Fait
- **Projet Supabase** « hortus-sacrum » créé dans votre organisation (offre gratuite, 0 €/mois, hébergé à Paris).
- **Base** (`supabase/migrations/`) : une table `documents`, une ligne par objet (prière, pratique, élément de liste, coche…), avec règles par utilisateur : chacun ne lit et n'écrit que ses propres données. Le plus récent l'emporte ; les suppressions se propagent. Aucune alerte de sécurité Supabase.
- **Synchronisation** (`app/src/lib/sync.ts`) : chaque appareil garde tout en local et fonctionne hors ligne. Chaque modification entre dans une file d'envoi ; la synchronisation reçoit d'abord ce qui a changé ailleurs, puis envoie la file. Elle se lance à la connexion, à l'ouverture de l'app, au retour du réseau et deux secondes après une modification.
- Les données de départ (livret, liste, plan) portent une date ancienne : installées sur un second appareil, elles ne remplacent jamais une modification faite sur le premier.
- **Profil → Compte** : connexion par lien envoyé par courriel ; état de la synchronisation ; « Synchroniser maintenant » ; déconnexion.
- **Hors ligne** : un service worker garde l'app, le calendrier et le livret sur l'appareil.

## Vérifié
- Contrôle de types : 0 erreur. Tests : 45 sur 45. Compilation : réussie, service worker produit.
- Navigateur : la section Compte s'affiche ; une modification de prière entre bien dans la file d'envoi.

## Pas vérifié
- La connexion et la synchronisation réelles entre deux appareils : il faut votre adresse et votre boîte de courriel.

## Reste à faire
- Réglage Supabase de l'adresse de retour du lien (à faire par vous, voir ci-dessous).
- Mise en ligne (Vercel), avec votre accord.
- Modèles de reconnaissance de texte (OCR) à embarquer pour l'usage hors ligne.

## À faire par vous dans Supabase
Tableau de bord → projet « hortus-sacrum » → Authentication → URL Configuration :
- Redirect URLs : ajouter `http://localhost:5173/**` (et, après la mise en ligne, l'adresse du site).
