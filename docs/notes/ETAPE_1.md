# Étape 1 — Données : ce qui a changé

## Calendrier : n'importe quelle année
- Le moteur est réécrit en Python, le langage du moteur d'origine. Il calcule l'année de son côté et produit un fichier par année, que l'app lira hors ligne. C'est le plus souple : on ajoute une année par une commande, sans toucher à l'app.
- Il calcule toute année liturgique :
  - Avent, Noël, Épiphanie et ses dimanches reportés après la Pentecôte ;
  - Septuagésime, Carême, temps pascal ;
  - Quatre-Temps, lettre dominicale et translations de Divinum Officium ;
  - années bissextiles : jour bissexte le 24 février, S. Matthias le 25.
- **Contrôle** : sur les 364 jours de 2026-2027, le nouveau moteur redonne exactement le calendrier papier pour l'office, le rang, la couleur, les commémoraisons, la station, la notice, le jeûne, les dévotions et le martyrologe. Il diffère en quelques points, chaque fois pour corriger l'ancien :
  - **22 février 2027** : « Chaire de S. Pierre, Apôtre **à Antioche** ». L'ancien moteur lisait à tort une variante monastique.
  - **28 et 29 mai 2027** (dans l'octave de la Fête-Dieu) : Introït *Cibavit eos*, celui de la fête, au lieu de *Benedicta sit*, celui de la Trinité.
  - Les incipits d'un seul mot sont complétés (« Salve, sancta Parens », « Cognovi, Domine »). Trois Introïts manquants sont trouvés : vigile de l'Épiphanie, Visitation, vigile de la Toussaint anticipée.
  - Les féries du temps de la Septuagésime sont en violet. Le cas ne se présentait pas en 2027.
- **Années générées** : de 2025-2026 à 2030-2031, dans `data/calendar/`.
- **Dévotions à jours comptés** : un planificateur automatique enchaîne les séries sans chevauchement.
  - Sur 2026-2027, il retrouve à lui seul le plan que vous aviez accepté. Ce plan reste enregistré dans `data/plans/2026-2027.json` et prime sur le planificateur ; il sera modifiable dans l'app.
  - Neuvaines et préparation de Montfort sont calculées d'après la date réelle des fêtes. Exemple : l'Annonciation transférée au 5 avril 2027.
- **Jeûne et abstinence** : règle française par défaut. En France, le vendredi qui tombe une fête de précepte du droit commun (Circoncision, Épiphanie…) garde l'abstinence, avec une mention.

## Prières du livret
- Les **62 pièces** du *Jardin de l'âme* sont extraites mot pour mot vers `data/prieres/jardin.json`. Chaque pièce a :
  - titre, partie, page, ligne « usage » et indulgence ;
  - sa source, telle qu'imprimée ;
  - son texte découpé en blocs : paragraphes, ℣/℟, strophes latin-français, litanies, mystères, rubriques.
- Contrôle croisé avec le PDF : les écarts restants viennent des lettrines et des coupures de mots du PDF.

## Liste du jour
- La structure tient compte de vos réponses : `docs/LISTE_DU_JOUR.md`.
- Une trouvaille pour votre usage : **Pie VI (5 avril 1786)** a indulgencié le *Salve Regina* le matin et le *Sub tuum* le soir, **avec leurs versets**. La référence est Beringer, éd. 1925, n° 429. C'est exactement votre pratique du matin et du soir. Les versets doivent être dits pour gagner l'indulgence.

## Non fait, ou en attente de vous
- **Propre de France** : absent des données de Divinum Officium. Le moteur peut l'accueillir (`register_local`), mais il faut une source (A_FOURNIR n° 9).
- **Annonce de la lune** du martyrologe (lecture de Prime) : à calculer à l'étape 2.
- **Textes nouveaux** : aucun n'a encore été recopié dans la base. Les sources repérées et les questions sont dans `A_FOURNIR.md`.
