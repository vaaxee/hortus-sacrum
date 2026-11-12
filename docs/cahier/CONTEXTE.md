# Contexte

## 1. Qui, quoi

L’utilisateur est un catholique attaché à la liturgie traditionnelle. Il veut une vie de prière ordonnée : une liste quotidienne fixe (l’« Ordinaire ») et un « Propre » qui suit le temps liturgique, le sanctoral, le mois, ainsi que les neuvaines, trentains et dévotions à jours comptés en cours.

Il a déjà deux choses.

1. **Un test sur Notion**, « Hebdomada in Dei servitio » (captures dans `captures/`).
   - Il comprend une page par jour de la semaine (LUNDI… DIMANCHE).
   - Chaque page a deux parties.
     - **ORDINAIRE**
       - *Prières fixes* : prière du matin avec Ave Maria de la mort et Salve Regina ; prière du soir avec Ave Maria de la mort et Sub tuum præsidium ; intentions particulières pour la journée ; chapelet ; couronne du Sacré-Cœur ; couronne angélique ; couronne des 50 Requiem ; 15 oraisons de sainte Brigitte.
       - *Prières particulières au jour* : dévotion du jour ; litanies et prières particulières ; demande des dons du Saint-Esprit.
     - **PROPRE DU TEMPS**
       - *Commun* : dévotion du mois ; sanctoral.
       - *Optionnel* : prière du trentain en cours ; prière d’une neuvaine en cours ; consécration personnelle.
   - Il le juge « médiocre » : c’est statique, sans rappels, et les prières ne s’ouvrent pas.
2. **Deux livrets imprimés**, faits avec lui et validés.
   - *Le Jardin de l’âme* (`livret/`) : 84 pages au format 11 × 17 cm. Prières choisies, avec pour chacune une ligne « usage » (le jour ou le moment recommandé) et l’indulgence d’après l’Enchiridion de 1952.
     - Parties : I. Offrande du matin ; II. Devoirs de charité ; III. Consécration à Jésus par Marie (Montfort) et prières mariales ; IV. Couronnes et chapelets ; V. Réparation ; VI. Litanies ; VII. Hymnes ; VIII. Dévotions à jours comptés.
     - `donnees/index_prieres_jardin.json` donne le titre, la page, l’usage et l’indulgence de chaque pièce. Le texte intégral est dans `livret/source/recueil.tex` et `chunk_*.tex`, en LaTeX : macros `\acte`, `\usage`, `\indulg`, `\source`, `\vr` (verset et répons), `\latin`, `\traduction`, etc., définies dans `bibliotheca-missel.cls`.
   - *Calendrier liturgique 2026-2027* (`calendrier/`) : 136 pages, une semaine par double page.
     - Chaque jour : office, rang, couleur, commémoraisons, Introït, station, notice du Martyrologe pour les fêtes principales, jeûne et abstinence, dévotions à jours comptés enchaînées sans chevauchement, neuvaines, préparation de Montfort.
     - Une double page d’ouverture par mois : dévotion du mois avec sa référence dans l’Enchiridion de 1952, et un Introït en exergue.
     - Toutes ces données sont dans `donnees/calendrier_2026-2027.json`.

## 2. Ce que l’utilisateur a explicitement demandé ou refusé (historique)

- **Retirés du livret** : la « Prière embrasée » (encombrante) ; le Stabat Mater ; les **promesses de sainte Brigitte**. Le monitum du Saint-Office du 28 janvier 1954 (AAS 46, 1954, p. 64) les déclare non authentiques : on garde les oraisons, sans les promesses.
- **Ne rien ajouter sur saint Joseph** dans le livret : il a d’autres manuels. Dans l’app, il peut ajouter des prières lui-même ; demande-lui avant d’en ajouter de ton côté.
- **Pas de scapulaires, ni de pièces de Gertrude ou de Mechtilde.**
- **Promesses attachées aux dévotions** : on les met **seulement si elles existent dans une source sûre** (« si elles n’y sont pas, tu ne les mets pas »).
  - Elles sont déjà dans le livret : la grande promesse du Sacré-Cœur, la demande de l’Heure sainte, la promesse de Pontevedra et les 15 promesses du Rosaire.
  - Les promesses des saintes Plaies n’ont pas été retenues, faute de source française fiable.
- **Usage** : la ligne « usage : » s’écrit en minuscules.
- **Tolérance zéro pour l’approximatif** : « tout ce que tu as fait de mémoire, tu cherches les sources officielles ».

## 3. Charte graphique (reprise des livrets)

- **Police** : EB Garamond (Google Fonts). Petites capitales pour les titres ; chiffres elzéviriens dans le texte.
- **Couleurs** : rouge rubrique `#7C1A1D` (RGB 124, 26, 29) ; encre `#1A1A1A`. Couleurs liturgiques des pastilles : violet `#603078`, rouge `#B01E24`, vert `#2E6E3A`, rose `#DE8CA0`, noir, blanc cerclé.
- **Ornements** (dans `charte/`) :
  - `gloire.pdf` : la croix en gloire avec deux anges hérauts, en frontispice ;
  - `angelot.pdf` : l’ange héraut, en cul-de-lampe ;
  - `cherubin.pdf` : le chérubin du calendrier (source TikZ : `calendrier/source/cherub.tex`).
  - Les convertir en SVG pour le web.
- **Mise en page** : sobre, typographique, beaucoup de blanc. Les mentions « Ind. » sont en très petit corps. Les ℣ et ℟ sont en rouge.

## 4. Jours de la semaine (dédicaces reprises du livret)

Dimanche : la très sainte Trinité. Lundi : les âmes du purgatoire. Mardi : les saints Anges. Mercredi : saint Joseph. Jeudi : le très saint Sacrement. Vendredi : la Passion et le Sacré-Cœur. Samedi : la très sainte Vierge.
