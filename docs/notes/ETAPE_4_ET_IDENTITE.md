# Identité Hortus Sacrum et écran Aujourd'hui : ce qui a changé

## Identité visuelle, appliquée à toute l'app
- **Jetons** : `app/src/lib/design/tokens.css` (couleurs, échelle 1,25, espaces, traits, mouvement).
- **Deux directions artistiques**, chacune avec son jour et sa nuit :
  - **latine** : ivoire, parchemin, lapis, rouge de missel, or en filet ;
  - **grecque** : bichromie outremer (fonds, arche, encre) et cobalt (icônes, cases, liens, tesselles), or en filet, bande de mosaïque en tête de chaque écran.
- Le choix se fait dans **Profil → Apparence** : thème (selon l'appareil, jour, nuit) et direction. Il est gardé sur l'appareil.
- **Ornements et icônes** en SVG : `Ornement.svelte`, `Icone.svelte`, `Arche.svelte`, `Case.svelte`.
- **Navigation** : cinq onglets (Aujourd'hui, Calendrier, Prières, Dévotions, Profil) en bas au téléphone, avec la palmette d'or sur l'onglet actif ; colonne de gauche à l'ordinateur.
- L'app s'appelle maintenant Hortus Sacrum (titre, icône au chrisme, manifeste).
- La maquette (`/maquette`) est retirée : ses écrans sont devenus les vrais.

## Écrans
- **Aujourd'hui** (étape 4, en partie) :
  - fête du jour dans l'arche, Introït dépliable en latin et en français, jeûne ;
  - liste du jour réelle : les coches sont enregistrées et horodatées, les prières répétées ont un compteur, chaque ligne ouvre sa prière ;
  - martyrologe complet avec invocations ;
  - jour précédent et jour suivant.
- **Calendrier** : ouverture du mois (dévotion du mois, Introït en exergue, dimanches et fêtes), mois précédent et suivant ; chaque fête ouvre son jour.
- **Prières** : bibliothèque, fiche (latin dépliable, indulgence et source en marge sur grand écran), éditeur, copier-coller, import PDF et photo, tous dans le nouveau style.
- **Dévotions** : les dévotions et neuvaines des trente prochains jours, d'après le plan de l'année.
- **Profil** : apparence, sauvegarde, corbeille.

## Vérifié
- Tests : 26 sur 26. Contrôle de types : 0 erreur. Compilation : réussie.
- Dans le navigateur, en largeur de téléphone : les sept écrans s'ouvrent sans erreur ni débordement ; une coche s'enregistre ; le changement de thème et de direction s'applique.

## Pas encore fait
- **Éditeur de la liste du jour** (ajouter, retirer, réordonner par glisser-déposer, jours, heures de rappel).
- Vue « lecture de Prime » du martyrologe et annonce de la lune.
- Vie du saint (leçons du Bréviaire), méditation du jour.
- Vue semaine et filtres du calendrier.
- Ornements : croix en gloire et ange héraut du dossier, bande cosmatesque, motifs floraux des pages mariales, lettrines des méditations.
- Compteurs de séries et édition des pratiques (étape 5).
- Pas encore vu sur iPhone.

## Complément : éditeur de la liste du jour (13 novembre 2026)
- **Aujourd'hui → Régler la liste** ouvre l'éditeur (`/liste`).
- Pour chaque moment de la journée : changer l'ordre en glissant la poignée (doigt ou souris) ou avec les flèches ; ajouter un élément.
- Pour chaque élément : titre, moment, genre (ordinaire ou propre), jours de la semaine, heures de rappel (plusieurs heures = prière comptée plusieurs fois), prières liées (recherche dans la bibliothèque), masquer ou afficher, restaurer l'original, corbeille.
- Corbeille en bas de l'écran : rétablir, ou supprimer pour de bon en deux temps.
- Changer l'ordre ne marque plus un élément comme « modifié », et « Restaurer l'original » ne le déplace pas.

Essayé dans le navigateur, en largeur de téléphone : flèches, glisser-déposer à la souris, jours, heure, prière liée, ajout, corbeille, suppression. Revérifié après le restylage : modifier une prière, historique, restaurer l'original. Tests : 29 sur 29.

Les heures de rappel sont enregistrées mais n'envoient encore aucune notification (étape 7). Le glisser-déposer n'a pas été essayé au doigt sur un vrai téléphone.
