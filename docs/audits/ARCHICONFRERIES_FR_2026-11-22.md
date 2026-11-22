# Manuels d'archiconfréries en français — 22 novembre 2026

Décision de l'utilisateur du 22 nov. : les manuels d'archiconfréries antérieurs à Vatican II sont des sources admises.
Ce lot recherche les manuels **en français**, les télécharge, les lit en double lecture, en extrait les pièces nouvelles et
propose leur place dans le programme. **Rien n'est branché dans `programme.json`** : l'utilisateur tranchera.

Méthode de lecture (skill `hortus-ocr`) : pour chaque page transcrite, deux lectures indépendantes (couche texte du
scan — Google ou ABBYY d'archive.org — et Tesseract `fra`), alignées mot à mot (`deux.py`), puis chaque désaccord et
chaque fin de page courbée tranchés **sur l'image** de la page (rendue à 300 dpi). La ponctuation a été contrôlée à part :
la couche texte de Google perd souvent les deux-points, Tesseract les points d'exclamation ; l'union des deux a été
vérifiée sur l'image. Orthographe de l'édition gardée (« siége », « très-sainte », « Eglise »). Fichiers téléchargés dans
le scratchpad, non versionnés.

Préfixes : `janvier:` (Sainte-Face), `desgenettes:` (Cœur de Marie), `garde1886:` (Garde d'honneur).

## 1. Sainte-Face — Janvier, Tours, 1895 (compléments)

- **Édition** : Abbé P.-D. Janvier, *Manuel de l'Archiconfrérie de la Sainte-Face*, « revu et corrigé d'après les décrets
  du Saint-Office », « approuvé par Son Éminence le cardinal Meignan », 3e éd., Tours, Bureau de l'Oratoire, 1895
  (page de titre). Scan Google (exemplaire des Fontaines, Chantilly), 299 p. de PDF ; PDF = page + 7.
- **URL** : https://pdfs.bibliotheque-catholique.com/pdfs/piete/ (titre : « Abbé Pierre-Désiré Janvier - Manuel de
  l'Archiconfrérie de la Sainte-Face revue et corrigé… ») — même fichier que les pièces `janvier:` déjà livrées.
- **Table** (p. 275-276) : I. Documents officiels, statuts, indulgences, promesses (93), neuvaine de méditations (112) ;
  II. Litanies et formules : invocations d'après l'Écriture (143), invocations à Jésus outragé (151), amende honorable
  (157), consécration (160), acte d'amour (162), acte de réparation (163), prière de saint Augustin (164), autre acte de
  réparation (165), acte d'admiration (166), prière pour le triomphe de l'Église (168), prières de M. Dupont (169-174),
  litanies de l'humilité (175), cri d'amour (176), prière de Pie IX (177), louanges de la sainte Face (178), bénédiction de
  saint François (179), louanges au saint Nom de Dieu (179), quarantaine de saint Louis (180), Flèche d'or (181) ;
  III. Petit chemin de croix (181), prières et exercices de réparation (193-206 : prière au Père éternel, 24 adorations,
  salutation, offrande pour la France…), exercice de N.-D. des Sept-Douleurs (207), cantiques ; IV. Appendice : chemin de
  croix (221), couronne du saint Nom de Dieu (234), couronne du saint Nom de Jésus (236), petit scapulaire (237), petite
  couronne (237), rosaire (239), petit sachet (243), sept Ave (245), chapelet des Sept-Douleurs (245), évangile (246),
  messe (248), petit office du saint Nom de Dieu (253).

| Pièce | Statut | Nature | Indulgence (selon le manuel) |
|---|---|---|---|
| Invocations « tirées de l'Écriture » (litanies, latin-français), p. 143-150 | **nouvelle** `janvier:litanies-sainte-face-ecriture` | litanie | — |
| Invocations à Jésus outragé dans sa Face, p. 151-156 | **doublon** : c'est le texte de `jardin:litanies-de-la-sainte-face` (sœur Saint-Pierre) ; le livret n'a pas de source ancienne, Janvier peut lui en servir (à relire mot à mot avant) | litanie | — |
| Amende honorable, p. 157-160 | déjà présente `janvier:amende-honorable-sainte-face` | acte | — |
| Consécration à la sainte Face à l'usage des membres (« embûches de Satan »), p. 160-161 | **nouvelle** `janvier:consecration-archiconfrerie` | consécration | — |
| Consécration de soi-même, p. 161-162 | déjà présente `janvier:consecration-sainte-face` | consécration | — |
| Acte d'amour, p. 162-163 | **nouvelle** `janvier:acte-d-amour-sainte-face` | acte | — |
| Acte de réparation, p. 163-164 | **nouvelle** `janvier:acte-de-reparation-sainte-face` | acte | — |
| Acte de réparation pour tous les outrages de la sainte Face, p. 165-166 | **nouvelle** `janvier:reparation-outrages-sainte-face` | acte | — |
| Louanges de la sainte Face, p. 178 | **nouvelle** `janvier:louanges-sainte-face` | louanges | — |
| Louanges au saint Nom de Dieu (« Dieu soit béni »), p. 179-180 | **nouvelle** `janvier:louanges-saint-nom-de-dieu` (forme de 1895, neuf louanges) | louanges | 1 an ; plénière mensuelle (Pie VII 1801, Pie IX 1847) |
| Couronne à la gloire du saint Nom de Dieu, p. 234-235 | **nouvelle** `janvier:couronne-saint-nom-de-dieu` (« la monde » imprimé ainsi) | chapelet | — |
| Couronne en l'honneur du saint Nom de Jésus, p. 236-237 | **nouvelle** `janvier:couronne-saint-nom-de-jesus` | chapelet | — |
| Sept Ave à Marie Mère de douleurs, p. 245 | **nouvelle** `janvier:sept-ave-mere-de-douleurs` (= Beringer n° 447, cf. A_FOURNIR) | pratique | 300 j. ; plénière mensuelle |
| Petite couronne (= « petit chapelet » du catalogue), rosaire, chemin de croix, neuvaine, petit office, promesses, Flèche d'or | déjà présentes (`janvier:*`) | — | — |
| Chapelet des Sept-Douleurs, p. 245-246 | non repris : renvoie au « premier exercice » pour versets et oraison ; doublon de `jardin:les-sept-douleurs-de-marie` | chapelet | 200/100 j. |
| Prière de saint Augustin, acte d'admiration, triomphe de l'Église, prières de M. Dupont, litanies de l'humilité, prière de Pie IX, 24 adorations, offrande pour la France, grand chemin de croix (221-233), évangile, messe | non transcrites (place limitée ; à reprendre si l'utilisateur les veut) | — | — |

## 2. Très-saint et immaculé Cœur de Marie

### 2.1 Desgenettes, Paris, 1852 — retenu

- **Édition** : M. Dufriche-Desgenettes, curé de N.-D.-des-Victoires, *Manuel d'instructions et de prières, à l'usage des
  membres de l'Archiconfrérie du très-saint et immaculé Cœur de Marie…*, 13e éd., refondue et augmentée, Paris, Sagnier et
  Bray, **1852** (page de titre ; la notice d'archive.org dit 1846 à tort). Statuts autorisés par « Hyacinthe, Archevêque
  de Paris », 16 décembre 1836 (p. IV). Scan Google (Oxford), 503 p. de PDF ; PDF = page + 35 pour la fin du volume.
- **URL** : https://archive.org/details/manueldinstruct00dufrgoog (texte ABBYY `_djvu.xml` ; le PDF n'a pas de couche texte).
- **Table** (p. 463-464) : statuts, brefs ; I. notice historique, instructions, catéchisme des indulgences ; II. Office et
  prières : prières du matin et du soir, litanies du saint Nom de Jésus, pénitence, communion, office de la fête du
  saint Cœur de Marie (messe, none, vêpres, complies), dévotions et offices ordinaires (messes des samedis, Compassion),
  indulgences (oraison préparatoire, cinq prières aux intentions du Pape, acte d'offrande du matin), **prières** :
  consécration des œuvres de la journée (435), préparation à la messe du saint Cœur de Marie (436), exercice de louanges
  pour tous les jours de la semaine (437-444), prière journalière à la sainte Vierge (444), retour du pécheur (445), cri du
  cœur pénitent (447), oraison pour se consacrer au sacré Cœur de Marie (449), litanies du saint Cœur de Marie (450), prière
  d'une mère (452), prière pour le salut de la France (453) ; fête de N.-D.-des-Victoires (454-461).

| Pièce | Statut | Nature | Indulgence |
|---|---|---|---|
| Exercice de louanges et de prières pour chaque jour de la semaine (saint Alphonse ; sept prières, chacune suivie de trois Ave en réparation des blasphèmes), p. 437-444 | **nouvelle** `desgenettes:louanges-de-la-semaine` | prière par jour | Pie VII, 21 juin 1808 : 300 j. / plénière mensuelle |
| Consécration des œuvres de la journée au saint Cœur de Marie, p. 435 | **nouvelle** `desgenettes:consecration-oeuvres-de-la-journee` | offrande du matin | — |
| Oraison pour se consacrer au sacré Cœur de Marie, p. 449-450 | **nouvelle** `desgenettes:oraison-consecration-coeur-de-marie` (même texte que l'« Acte de consécration au sacré Cœur de Marie » du *Petit manuel* de Montréal, 1841) | consécration | — |
| Litanies du saint Cœur de Marie, p. 450-452 | **nouvelle** `desgenettes:litanies-saint-coeur-de-marie` (litanies de dévotion privée) | litanie | — |
| Prière d'une mère à la très-sainte Vierge, p. 452-453 | **nouvelle** `desgenettes:priere-d-une-mere` (aussi dans le manuel de Québec, 1857) | prière | — |
| Prière pour le salut de la France, p. 453 | **nouvelle** `desgenettes:priere-salut-de-la-france` | prière | — |
| Prière journalière à la sainte Vierge, p. 444-445 | **à transcrire** : premier mot après « Vierge » taché sur le scan (A_FOURNIR) | prière | — |
| Cinq prières aux intentions du Souverain Pontife, p. 432-434 ; acte d'offrande pour les indulgences, p. 434-435 | non transcrites (candidates pour la règle des indulgences) | prières | — |
| Litanies de la sainte Vierge, Stabat, Magnificat, Memorare, office et messe propres | doublons de textes livrés ou liturgiques | — | — |

### 2.2 Autres éditions trouvées (non transcrites)

- *Petit manuel de l'Archiconfrérie du Très-Saint et Immaculé Cœur de Marie*, établie dans la cathédrale de Montréal le
  7 février 1841, 1re éd. en Canada, Montréal, Bureau des Mélanges religieux, 1841 ; approbation d'Ignace Bourget, évêque
  de Montréal, 2 février 1841 — archive.org `cihm_51354` (réimpr. 1843 : `cihm_51355`). Contenu : approbation, mandement,
  statuts, acte de consécration (doublon de Desgenettes p. 449), litanies de la sainte Vierge, Stabat. OCR très médiocre ;
  le PDF d'archive.org renvoie une erreur 500 le 22 nov. Rien de nouveau par rapport à Desgenettes.
- *Manuel de la Confrérie du Très-St. et Immaculé Cœur de Marie, érigée dans le diocèse de Québec*, Québec, A. Côté, 1857
  — `cihm_37163` : prière d'une mère (doublon), prière pour les jeunes gens (à voir).

## 3. Garde d'honneur du Sacré-Cœur — Bourg, 1886 — retenu

- **Édition** : *Manuel de l'Archiconfrérie de la Garde d'Honneur du Sacré Cœur de Jésus*, 9e éd., Bourg-en-Bresse, au
  Monastère de la Visitation, 1886 ; « Approuvée par Mgr l'Evêque de Belley » ; approbation de « + Pierre, Évêque de
  Belley », Belley, Vendredi saint 23 mars 1883 (p. [III]). Imprimé à Fécamp, L. Durand et fils. 374 p. de PDF ; PDF = page + 44.
- **URL** : Google Livres `YxAtAYVrCuwC` (Bibliothèque des Fontaines, Lyon) ; le téléchargement Google demande un captcha :
  PDF lu dans la copie de ce même scan déposée par la paroisse Saint-Eugène–Sainte-Cécile
  (https://saint-eugene.net/wp-content/uploads/2025/05/1886_Manuel_de_l_archiconfrerie_de_la_Garde_d_Honneur_du_Sacre_Coeur.pdf).
  Autres éditions repérées : 1881 (Google `yjyjtig3i_IC`), Google `xEZv7YdJMYoC`.
- **Table** (p. 371-374) : I. Le Cœur blessé, origine, l'Heure de Garde, la très précieuse Offrande, union au Sauveur
  immolé, la sainte Milice, billets-zélateurs, adoration réparatrice, supplication perpétuelle ; II. statuts, indulgences,
  organisation, formule d'enrôlement (117) ; III. premier soupir de la journée (130), **prières de l'Archiconfrérie**
  (131-136), premier vendredi (137-147 : rénovation de l'enrôlement, exercice du matin, exercice du soir, prière
  réparatrice), cantique, consécration au Cœur de Jésus (150), amende honorable pour la fête du Sacré-Cœur (151), litanies
  du Sacré-Cœur et de la B. Marguerite-Marie, prières indulgenciées, prières pendant la messe, confession, communion,
  visites au Saint-Sacrement (avec un exercice de réparation à la sainte Face), visite à la sainte Vierge et à saint Joseph,
  bonne mort et défunts (trois Ave, prières de sainte Gertrude), petit office du Sacré-Cœur (265), heure sainte (274),
  chemin de la croix (285).

| Pièce | Statut | Nature | Indulgence |
|---|---|---|---|
| Offrande de l'Heure de Garde (avec les invocations), p. 131-132 | **nouvelle source** `garde1886:offrande-heure-de-garde` ; même texte que l'offrande de `jardin:offrandes-de-la-garde-d-honneur` (livret moderne de Saint-Eugène), qui n'avait pas d'édition ancienne | offrande | invocations : 100 et 300 j. |
| Très précieuse Offrande (deux prières), p. 132 | **nouvelle source** `garde1886:tres-precieuse-offrande` ; **écart** : 1886 dit « faites-*moi* miséricorde », le livret « faites-*nous* » | offrande | 80 et 100 j., Pie IX, 13 juin 1876 |
| Acte d'oblation (*Ecce venio*), p. 133 | **nouvelle** `garde1886:acte-d-oblation` | acte | — |
| Acte d'adoration réparatrice, p. 133-134 | **nouvelle** `garde1886:adoration-reparatrice` | acte | — |
| Rénovation de l'enrôlement, p. 139 | **nouvelle** `garde1886:renovation-enrolement` | consécration | — |
| Prière au Cœur de Jésus blessé par la lance, p. 140-141 | **nouvelle** `garde1886:coeur-blesse-par-la-lance` | prière | — |
| Amende honorable, p. 141-142 | **nouvelle** `garde1886:amende-honorable` | acte | — |
| Prière à Marie au pied de la Croix, p. 143-144 | **nouvelle source** `garde1886:priere-a-marie-au-pied-de-la-croix` (même texte que la 3e partie du livret) | prière | — |
| Prière réparatrice (« Nous vous consolerons, Seigneur »), p. 145-147 | **nouvelle** `garde1886:priere-reparatrice` | litanie | — |
| Consécration au Cœur de Jésus, p. 150-151 | **nouvelle** `garde1886:consecration-coeur-de-jesus` | consécration | — |
| Acte de suprême confiance (livret) | **non trouvé** dans la table de 1886 : reste sans édition ancienne | — | — |
| Acte d'oblation des âmes-victimes (134-136), amende honorable pour la fête du Sacré-Cœur (151), petit office du Sacré-Cœur (265), heure sainte (274) | non transcrits (à reprendre au besoin) | — | — |

## 4. Autres archiconfréries : manuels trouvés (identifiés, non transcrits)

| Confrérie | Manuel trouvé (français) | Accès | Remarque |
|---|---|---|---|
| Bonne Mort | A. Lefebvre, S. J., *La science de bien mourir : manuel de l'Association de la bonne mort*, Paris, 1870 | archive.org `lasciencedebienm00lefeuoft` | II. partie (p. 401-440) : acte de consécration, messe pour la bonne mort, litanies de la Passion, deux litanies de N.-D. des Sept-Douleurs, pieux exercice du Cœur affligé, prières pour les agonisants ; neuvaines à saint Joseph. Meilleur candidat pour le lot suivant. |
| Bonne Mort (Union de prières) | E. Picard, *Petit manuel des Associés de l'union de prières et de la bonne mort*, [Montréal], 1873 | `cihm_04796` | consécration à N.-S., amende honorable au Sacré-Cœur, acte héroïque |
| Agonie de N.-S. (Paris, rue de Sèvres) | **non trouvé** | — | voir A_FOURNIR |
| Précieux Sang | *Nouveau manuel du Très-Précieux Sang… ou le Livre des élus*, Saint-Hyacinthe, Monastère du Précieux-Sang, 1890 (approbation épiscopale en tête) | `cihm_92923` (706 images) | confrérie du Précieux-Sang, chapelet, neuvaines ; à dépouiller |
| Saint-Sacrement | *Petit manuel des adorateurs et des adoratrices du Très Saint Sacrement*, Québec, 1920 | `cihm_78894` | amendes honorables, petite consécration, prière de la Garde d'honneur |
| Saint-Rosaire | *Livret de la Confrérie du T.S. Rosaire*, Montréal, 1903, imprimatur de l'évêque des Trois-Rivières ; *Petit manuel du Rosaire-vivant*, 1841 ; *Les Trois confréries dominicaines* (Rosaire, Saint Nom de Jésus, Cordon de saint Thomas), 1902 | `cihm_77301`, `cihm_39974`, `cihm_78783` | méthode et indulgences ; peu de prières nouvelles |
| Saint Nom de Jésus | *Manuel de la Confrérie du Saint Nom de Jésus ou Saint Nom de Dieu*, Saint-Hyacinthe, Dominicains, 1899, imprimatur de l'évêque de Saint-Hyacinthe | `cihm_26544` | petit office ou salutation du saint Nom (p. 22), litanies du saint Nom (déjà livrées) |
| Notre-Dame des Sept Douleurs | J. Allibert, *Manuel de la Confrérie de Notre-Dame-des-sept-douleurs*, Lyon, Lambert-Gentot, 1838 | Google Livres `YAkym_DUqF0C`, `F47ut9G1E94C` (téléchargement bloqué par captcha) | à télécharger à la main |
| Cordon de saint François | *Le Cordon de saint François d'Assise*, [Québec], 1876 ; Mgr de Ségur, *Le cordon séraphique*, 1877 | `cihm_10448`, `cihm_13440` | prières latines de la bénédiction, peu de prières privées |
| N.-D. du Perpétuel Secours | [Rédemptoriste], *Notre-Dame du Perpétuel-Secours… son histoire, archiconfrérie et exercices de piété*, Montréal, J.-B. Rolland, 1878 ; approbations et imprimatur de Montréal | `cihm_52280` (231 images) | 27 prières « pour les diverses circonstances » (p. 182-217) : riche ; à dépouiller |
| Saint-Joseph | *Manuel de la Confrérie de Saint-Joseph*, Montréal, hospice Saint-Joseph, s. d. ; *Vertu miraculeuse du cordon de St. Joseph*, Montréal, 1871 | `cihm_61528`, `cihm_28660` | prières des associés, mercredis, sept douleurs, cordon ; l'archiconfrérie d'Angers (Jésuites) : **non trouvée** |

## 5. Proposition d'intégration (non appliquée)

Principe : « le moins pour le plus, le simple mais le saint, la variété mais la sobriété ». Aucune ligne quotidienne
nouvelle ; on prolonge des séquences existantes.

1. **Mardi (sainte Face)** — `prog:devotion-mardi`, roue `roue:litanies-2` : ajouter
   `janvier:litanies-sainte-face-ecriture` à la rotation (litanies de l'Ange gardien, de la sainte Face — Saint-Pierre —,
   de la sainte Face — Écriture), une par semaine. Coût nul : la ligne existe.
2. **Angélus / Flèche d'or** — rien à ajouter. Les **louanges au saint Nom de Dieu** (`janvier:louanges-saint-nom-de-dieu`)
   pourraient remplacer, *le dimanche seulement*, la Flèche d'or de l'Angélus du soir, ou s'ajouter au Salut si l'app
   en a un. À trancher ; sinon, rester au recueil.
3. **Premier vendredi du mois** — `jardin:premiers-vendredis-du-mois` : insérer `garde1886:priere-reparatrice` (la
   prière réparatrice de l'exercice du soir) et, après la communion, `garde1886:renovation-enrolement` si l'utilisateur est
   garde d'honneur. Une fois par mois.
4. **Heure de garde** — remplacer la source moderne de `jardin:offrandes-de-la-garde-d-honneur` par l'édition de 1886
   (offrande de l'heure, très précieuse offrande, prière à Marie au pied de la Croix) : correction du livret avec
   `revision`, à décider (l'écart « faites-moi / faites-nous miséricorde » est à trancher : garder 1886).
5. **Août (mois du Cœur immaculé)** — la prière du jour de l'*Exercice de louanges* de Desgenettes
   (`desgenettes:louanges-de-la-semaine`, section du jour de la semaine, suivie de trois Ave) dans
   `prog:devotion-samedi` ou comme insertion du mois d'août, une par jour selon le jour de la semaine (pratique propre de
   l'Archiconfrérie). Hors août : la prière du *samedi* seule, en rotation du samedi.
6. **Consécrations** (`janvier:consecration-archiconfrerie`, `desgenettes:oraison-consecration-coeur-de-marie`,
   `garde1886:consecration-coeur-de-jesus`) — une fois l'an, à la fête : Sainte Face (mardi de la Quinquagésime),
   Cœur immaculé (22 août), Sacré-Cœur (vendredi après l'octave du Saint-Sacrement), là où une ligne de fête existe déjà.
7. **France** — `desgenettes:priere-salut-de-la-france` aux fêtes nationales du calendrier (sainte Jeanne d'Arc, Assomption
   — vœu de Louis XIII) ; la dimension *personne* n'a pas de valeur « patrie » : à décider (valeur nouvelle ou
   « dirigeants »).
8. Le reste (couronnes du saint Nom de Dieu et de Jésus, actes, prière d'une mère, litanies du saint Cœur de Marie) :
   recueil, consultable, sans ligne au programme.

Classement **deviné** ajouté dans `data/prieres/dimensions-textes.json` pour les seules pièces des points 1, 2, 3, 5, 6 (Sainte
Face) et 7 : `janvier:litanies-sainte-face-ecriture`, `janvier:louanges-saint-nom-de-dieu`,
`janvier:consecration-archiconfrerie`, `garde1886:priere-reparatrice`, `garde1886:renovation-enrolement`,
`desgenettes:louanges-de-la-semaine`, `desgenettes:priere-salut-de-la-france` (champ `devinee` : à relire).

## 6. Indulgences

Les concessions citées par les manuels (Pie VII 1801 et 1808, Pie IX 1847 et 1876, sept Ave) sont reportées dans le champ
`indulgence` des pièces, **non comptées** : seule l'*Enchiridion* de 1952 fait foi (SPEC § 11). À vérifier dans
l'Enchiridion : louanges « Dieu soit béni » (forme complète de 1952, plus longue que celle de 1895), très précieuse
offrande, sept Ave (Ench. 1952 ?), exercice de la semaine de saint Alphonse.
