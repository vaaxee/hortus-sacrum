# Manuels d'archiconfréries, lot B — 25-26 novembre 2026

Demande de l'utilisateur du 25 nov. : finir l'OCR des manuels d'archiconfréries et d'associations pieuses trouvés,
puis extraire et classer leur contenu. Ce lot reprend les manuels **identifiés mais non transcrits** de l'audit FR
(`ARCHICONFRERIES_FR_2026-11-22.md`, § 4 : Rosaire, Saint Nom de Jésus, cordon de saint François, Saint-Joseph,
Sept Douleurs) et les **restes** des manuels déjà ouverts (Sainte-Face, Garde d'honneur, Desgenettes, manuels anglais).
Branche `claude/archi-lot-b`. **Rien n'est branché dans `programme.json`.**

Méthode (skill `hortus-ocr`) : deux lectures indépendantes de chaque page (couche texte du scan, ABBYY d'archive.org ou
Google, et Tesseract `fra`/`fra+lat`/`eng --psm 6` ; pour les pages à deux colonnes latin-français, chaque colonne
découpée et lue à part), comparaison mot à mot du texte retenu avec chacune des deux lectures, et **chaque désaccord vu
sur l'image** (page entière ou bande de la ligne, 300 dpi). Orthographe et fautes de l'édition gardées et signalées
dans `source.page` ; lettres retournées ou cachées par un pli rétablies seulement quand l'image ne laisse aucun doute
(signalé), sinon pièce laissée. Fichiers téléchargés dans le scratchpad, hors dépôt. Indulgences imprimées recopiées
dans `indulgence`, **non comptées** (seule l'*Enchiridion* de 1952 fait foi).

## Bilan

| Manuel | Pièces ajoutées | Laissées |
|---|---|---|
| 1. Saint Nom de Jésus, Saint-Hyacinthe, 1899 | 1 (petit office) | litanies (déjà livrées), hymne et oraison de la procession, réception |
| 2. Cordon séraphique (Ségur), Québec, 1877 | 0 | psaume *Exaudiat* (latin), formules du prêtre |
| 3. Saint-Joseph : cordon, Montréal, 1871 | 3 | prière du saint cordon (déjà livrée) |
| 3 bis. Saint-Joseph : manuel de la confrérie, Montréal, s. d. | 3 | prière pour connaître sa vocation (fins de ligne cachées), autres prières |
| 4. Rosaire : Rosaire-Vivant, Montréal, 1841 | 1 (15 fruits et prières) | récits des mystères |
| 4 bis. *Les Trois Confréries dominicaines*, Ottawa, [1902] | 1 (Milice angélique) | méditations du Rosaire, notices |
| 4 ter. *Livret de la Confrérie du T. S. Rosaire*, Montréal, 1903 | 0 | méditations, cantiques |
| 5. Notre-Dame des Sept Douleurs (Allibert, Lyon, 1838) | 0 | **introuvable en copie libre** (A_FOURNIR) |
| 6. Sainte-Face (Janvier, 1895), restes | 9 | grand chemin de croix, évangile, messe, cri d'amour |
| 7. Garde d'honneur (1886), restes | 2 | petit office, heure sainte |
| 8. Desgenettes (1852), restes | 2 | — |
| 9. Manuels anglais, restes | 3 (1 français ancien, 2 traductions de travail) | cinq plaies, litanie, chemin de croix (Bona Mors) ; litanies, prière, neuvaine de S. François ; neuvaine des âmes |
| **Total** | **25** | |

## 1. *Manuel de la Confrérie du Saint Nom de Jésus ou Saint Nom de Dieu*, 1899

- **Édition** : Saint-Hyacinthe, au couvent des Dominicains, 1899 ; *Imprimatur* : † L. Z. [Moreau], *Sti Hyacinthi
  Epus* (p. [2]).
- **URL** : https://archive.org/details/cihm_26544 (56 images ; image n*N* = page *N*).
- **Table** (p. [53-54]) : I. Le saint nom de Jésus (3) ; II. Origine et but de la confrérie (8) ; III. Conditions
  d'admission (13) ; IV. Pratiques : la fête principale, la Circoncision (16) ; la procession du deuxième dimanche du
  mois, hymne *Jesu nostra redemptio* et oraison *Sancti nominis tui* (16-19) ; le petit office ou salutation du saint
  Nom de Jésus (20-32) ; les litanies du saint Nom (32-38) ; V. Avantages : indulgences plénières et partielles des
  confrères, indulgences de tous les fidèles qui honorent le saint Nom (39-44) ; VI. Formulaire de la réception
  solennelle (*Veni Creator*, formule latine-française, *Te Deum*, 45-51).

| Pièce | Statut | Id |
|---|---|---|
| Petit office ou Salutation du très saint Nom de Jésus (bienheureux Jourdain de Saxe : hymne *Jesu dulcis memoria*, cinq psaumes J-E-S-U-S avec antiennes, hymne *Jesu Rex admirabilis*, verset, oraison *Deus qui Unigenitum*), latin et français, p. 20-32 | **nouvelle** (latin dans `latin`, fautes du latin imprimé gardées et listées) | `saintnom1899:petit-office-saint-nom-de-jesus` |
| Litanies du saint Nom de Jésus, p. 32-38 | déjà livrées (`paroissien:litanies-saint-nom`) | — |
| Hymne *Jesu nostra redemptio* et oraison de la procession ; *Veni Creator*, *Te Deum*, formule de réception | liturgie ou formules du prêtre | — |

Indulgence imprimée (p. 44) : sept ans et sept quarantaines chaque fois ; plénière mensuelle pour la récitation
quotidienne ; à la Circoncision et à la fête de Jésus de Nazareth (23 oct.). Non comptée.

## 2. Mgr de Ségur, *Le Cordon séraphique*, 1877

- **Édition** : Québec, J. A. Langlais, 1877 (p. de titre) ; décret de la S. C. des Indulgences du 26 mars 1859 pour le
  sommaire du Tiers-Ordre (p. 44).
- **URL** : https://archive.org/details/cihm_13440
- **Table** : le cordon de saint François (3) ; faveurs spirituelles (6) ; les trois nœuds (13) ; réponses aux
  difficultés (18) ; formule de l'absolution générale et de la bénédiction papale (24) ; bénédiction et imposition du
  cordon (25) ; catalogue des indulgences et calendrier franciscain (28) ; le psaume *Exaudiat* (45).
- **Pièces** : aucune nouvelle. La pratique des six *Pater*, *Ave* et *Gloria* (p. 5) est mot pour mot celle de la
  notice de Québec de 1876 déjà livrée (`cordon1876:six-pater-ave-gloria`). Le psaume *Exaudiat* (Ps 19, latin seul,
  avec versets pour le Pape, les bienfaiteurs, les défunts) et les formules latines sont du prêtre ou de la
  fraternité : laissés.

## 3. Saint-Joseph

### 3.1 *Vertu miraculeuse du cordon de St. Joseph démontrée par des exemples*, 1871

- **Édition** : nouvelle édition, Montréal, Eusèbe Senécal, 1871 ; « Vu et approuvé, 30 Décembre 1870. Ig., Evêque de
  Montréal » (p. 60).
- **URL** : https://archive.org/details/cihm_28660
- **Table** (sans table imprimée) : origine du cordon (Anvers, 1659), nature du cordon (sept nœuds), grâces attachées
  (protection, pureté, chasteté, persévérance, bonne mort), indulgences (p. 4-8) ; exemples de guérisons (p. 9-58) ;
  prières (p. 59-60).

| Pièce | Statut | Id |
|---|---|---|
| « Prière efficace ou la prière du saint cordon » (« O saint Joseph, Père et Protecteur des vierges… »), p. 59 | **déjà livrée** (`beringer:saint-joseph-purete`, même texte) | — |
| Souvenez-vous à saint Joseph, p. 59 | **nouvelle** (« appelé Père du Rédempteur… daignez les exaucer » sous des taches, lu sur l'image) | `cordonjoseph1871:souvenez-vous-a-saint-joseph` |
| Invocation « Bon saint Joseph, notre guide… », p. 60 | **nouvelle** | `cordonjoseph1871:invocation-bon-saint-joseph` |
| Oraisons jaculatoires « Jésus, Marie, Joseph… », p. 60 | **nouvelle** (300 jours sur l'image ; la couche texte lit 800) | `cordonjoseph1871:jaculatoires-jesus-marie-joseph` |

Aucune **formule de renouvellement du cordon** dans cette brochure : `hortus:renouvellement-cordon-saint-joseph` reste
une formule composée (A_FOURNIR).

### 3.2 *Manuel de la Confrérie de Saint Joseph*, Montréal, s. d.

- **Édition** : « se trouve à l'hospice St. Joseph, Montréal », sans date ni approbation imprimée dans le scan
  (préface : confrérie établie à Montréal, église Saint-Joseph, rue du Cimetière). Scan de microfiche : chaque page
  est suivie de la marge de la suivante.
- **URL** : https://archive.org/details/cihm_61528 (image n*N* = page *N* pour les pages vues).
- **Table** (p. [193]) : préface (5) ; calendrier (7) ; dévotion à saint Joseph (9) ; statuts (17) ; prières des
  associés (2[1]) ; notice sur le cordon (3[3]) ; prières pour les premiers dimanches (37) ; pour les mercredis (45) ;
  dévotion aux sept douleurs (49) ; notice sur le culte perpétuel (53) ; prières pour tous les jours (57) ; pour
  quelques circonstances (61) ; neuvaine préparatoire aux fêtes (65) ; prières pour les fêtes (69) ; pour les
  pèlerinages (77) ; messe en l'honneur de saint Joseph (81) ; prières pour le mois de saint Joseph (89) ; pratiques
  (113) ; neuvaine pour des grâces particulières (117) ; visites à saint Joseph (129) ; grâces obtenues (137) ; hymnes et
  cantiques (181).

| Pièce | Statut | Id |
|---|---|---|
| Consécration à saint Joseph, p. 26 | **nouvelle** | `confreriejoseph:consecration-a-saint-joseph` |
| Prière des associés (offrande de la journée, culte perpétuel), p. 56 | **nouvelle** (« aimé » coupé par le pli, lu sur l'image) | `confreriejoseph:priere-des-associes` |
| Prière pour demander la grâce d'une bonne mort, p. 56 | **nouvelle** (« bonhenr » imprimé, lu « bonheur ») | `confreriejoseph:grace-d-une-bonne-mort` |
| Prière pour connaître sa vocation, p. 28 | **laissée** : fins de ligne cachées par la page voisine (« à l[a] », « m[e] », « mo[n] »…) ; à reprendre sur un autre exemplaire | — |
| Prières des mercredis, sept douleurs (déjà livrées : `jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph`), mois de saint Joseph, neuvaines, prières pour les circonstances | non transcrites (manuel sans approbation imprimée, scan médiocre) | — |

## 4. Saint-Rosaire

### 4.1 *Petit manuel du Rosaire-Vivant*, 1841

- **Édition** : Montréal, Louis Perrault, [1841] ; « Vu et approuvé. Montréal, 20 Septembre 1841. H. Hudon, V. G.,
  Administrateur du Diocèse » (p. [1]).
- **URL** : https://archive.org/details/cihm_39974 (image n*N* = page *N*+1).
- **Table** : abrégé du règlement (but, méthode des quinzaines, observations, tirage des mystères) ; avis aux
  zélatrices ; les quinze mystères du Rosaire (récit, fruit du mystère, prière) ; litanies du saint Nom de Jésus ;
  litanies de la sainte Vierge.

| Pièce | Statut | Id |
|---|---|---|
| Fruit et prière de chacun des quinze mystères, p. 19-33 (extrait : les récits ne sont pas repris) | **nouvelle** (fautes imprimées gardées : « Obédéon », « ne serait véritable », « Fruit de Mystère ») | `rosairevivant1841:fruits-des-quinze-mysteres` |
| Litanies du saint Nom, de la sainte Vierge | déjà livrées | — |

### 4.2 *Les Trois Confréries dominicaines*, Ottawa, [vers 1902]

- **Édition** : Ottawa, A. Bureau & frères, s. d. (date du catalogue) ; aucune approbation dans le scan ; « pour les
  diplômes d'érection et les manuels de la Confrérie, on aura à s'adresser au couvent des Dominicains de
  St-Hyacinthe ou d'Ottawa ».
- **URL** : https://archive.org/details/cihm_78783
- **Table** (p. [63]) : Confrérie du Très-Saint Rosaire (résumé, mystères, indulgences, roses bénites, Rosaire perpétuel,
  méditations sur les quinze mystères) ; Confrérie du Très-Saint Nom de Jésus (historique, conditions, indulgences) ;
  Confrérie du Cordon de S. Thomas ou Milice angélique (historique, conditions, indulgences, prière quotidienne).

| Pièce | Statut | Id |
|---|---|---|
| Prière quotidienne des confrères de la Milice angélique (« Très-chaste saint Thomas… », *Pater*, *Ave*, *Gloria*, versets, oraison), p. 61-62 | **nouvelle** | `troisconfreries:priere-quotidienne-milice-angelique` |
| Méditations sur les quinze mystères (p. 19-43) | non transcrites (méditations longues, sans approbation imprimée) | — |

### 4.3 *Livret de la Confrérie du T. S. Rosaire*, Montréal, 1903

- **Édition** : Montréal, 1903 ; approbation et *imprimatur* de l'évêque des Trois-Rivières (p. [4]).
- **URL** : https://archive.org/details/cihm_77301
- **Contenu** : règles de la confrérie, indulgences plénières mois par mois, « pour bien réciter le Rosaire »,
  méditations sur les quinze mystères, cantiques notés (*Ave Maria*, *Laudate Mariam*, etc.). Aucune prière nouvelle
  courte : rien d'ajouté.

## 5. Notre-Dame des Sept Douleurs — J. Allibert, Lyon, 1838

Recherche du 26 nov. : archive.org (titres « sept douleurs », « sept-douleurs », « Allibert ») : seules des éditions
modernes ou sans rapport ; HathiTrust (catalogue « Allibert Notre-Dame-des-sept-douleurs ») : rien ; Gallica : rien de
pertinent ; recherche web : seules les deux notices Google Livres (`YAkym_DUqF0C`, Bibliothèque de Lyon ;
`F47ut9G1E94C`, KU Leuven), dont le téléchargement est bloqué. **Rien transcrit** ; inscrit dans `A_FOURNIR.md`.
À noter : Janvier 1895 donne un « Exercice en l'honneur de Notre-Dame des Sept-Douleurs » (p. 207-209, Pie VII,
14 janvier 1815), non repris ici (à comparer avec `jardin:les-sept-douleurs-de-marie`).

## 6. Sainte-Face — Janvier, Tours, 1895 (restes)

Édition, URL et table : voir l'audit FR, § 1 (PDF = page + 7). Couche texte Google relue contre Tesseract ; désaccords,
ponctuation, traits d'union de fin de ligne (« écoutez-nous », « bien-aimé ») vus sur l'image.

| Pièce | Statut | Id |
|---|---|---|
| Prière de saint Augustin, p. 164-165 | **nouvelle** | `janvier:priere-saint-augustin-sainte-face` |
| Acte d'admiration en contemplant la sainte Face, p. 166-167 | **nouvelle** | `janvier:acte-d-admiration-sainte-face` |
| Prière pour demander par la sainte Face le triomphe de l'Église (Dan. IX), p. 168-169 | **nouvelle** | `janvier:triomphe-de-l-eglise-sainte-face` |
| Prières empruntées aux écrits de M. Dupont (I-V) et prières de M. Dupont, résolution de se confesser, p. 169-175 | **nouvelle** (« les opprobres qui vous sont destinées » imprimé ainsi) | `janvier:prieres-de-m-dupont` |
| Litanies de l'humilité, avec l'oraison, p. 175-176 | **nouvelle** | `janvier:litanies-de-l-humilite` |
| Prière de Pie IX (10 mars 1872), p. 177 | **nouvelle** | `janvier:priere-de-pie-ix-sainte-face` |
| Aspirations (sœur Marie de Saint-Pierre ; saint Edme), p. 177 | **nouvelle** | `janvier:aspirations-sainte-face` |
| Vingt-quatre adorations pour réparer les blasphèmes, p. 194-196 | **nouvelle** | `janvier:vingt-quatre-adorations` |
| Offrande des mérites de Notre-Seigneur pour la France, p. 198-201 | **nouvelle** | `janvier:offrande-pour-la-france` |
| Cri d'amour (176), prière au Père éternel (193), salutation et aspirations (196-198), aspirations contre les blasphèmes des Juifs (201-205), prière au véritable réparateur (206), exercice des Sept-Douleurs (207-209), grand chemin de croix, évangile, messe | non transcrits | — |

## 7. Garde d'honneur — Bourg, 1886 (restes)

Édition, URL, table : audit FR, § 3 (PDF = page + 44).

| Pièce | Statut | Id |
|---|---|---|
| Acte d'oblation des âmes-victimes (forme complète de l'*Ecce venio*), p. 134-136 | **nouvelle** ; la forme abrégée est `garde1886:acte-d-oblation` | `garde1886:oblation-des-ames-victimes` |
| Amende honorable et consécration solennelle pour la fête du Sacré-Cœur (formule du curé pour sa paroisse), p. 151-152 | **nouvelle** | `garde1886:amende-honorable-fete-du-sacre-coeur` |
| Petit office du Sacré-Cœur (265), heure sainte (274) | non transcrits | — |

## 8. Desgenettes — Paris, 1852 (restes)

Édition, URL, table : audit FR, § 2.1 (PDF = page + 35). La couche ABBYY de ces pages est très abîmée : texte établi
sur Tesseract et l'image, page par page.

| Pièce | Statut | Id |
|---|---|---|
| Avis, oraison préparatoire et cinq prières aux intentions du Souverain Pontife, p. 432-434 | **nouvelle** (« digne de son divin Époux du prix de sa rançon » imprimé ainsi) | `desgenettes:cinq-prieres-intentions-souverain-pontife` |
| Acte d'offrande des actions de la journée pour gagner les indulgences, p. 434-435 | **nouvelle** | `desgenettes:acte-d-offrande-pour-les-indulgences` |

## 9. Manuels anglais (restes de l'audit EN)

Recherche du français ancien d'abord (Beringer 1925, t. I ; Lefebvre 1870 ; *Notice sur le Tiers-Ordre*, Québec, 1867,
`cihm_29653` ; *Manuel du Tiers-Ordre*, 1885, `cihm_62202`).

| Pièce anglaise | Résultat | Id |
|---|---|---|
| *Ejaculatory Offering of the Precious Blood* (Caswall 1861, n° V) | **français ancien** : Beringer 1925, t. I, n° 250, p. 132-133 (Pie VII, 22 sept. 1817 ; l'OCR lit 1847) | `beringer:offrande-du-precieux-sang` |
| *Act of Reparation to the Precious Blood* (Caswall) | **déjà présent** : c'est l'oraison « O Sang très-précieux de vie éternelle » de `boylesve1882:petit-chapelet-precieux-sang` (= Beringer n° 394) | — |
| *Colloquy with Christ Crucified* (prières de S. Pie V), Bona Mors 1896, p. 22-23 | **traduction de travail** (rien dans Lefebvre 1870 ni Beringer) | `bonamors1896:colloque-saint-pie-v` |
| *Invocation of the Most Holy Trinity for the Souls in Purgatory*, *Purgatorian Consoler* 1868, p. 312-313 | **traduction de travail** des trois invocations ; les oraisons du Missel qui suivent (p. 313-314) ne sont pas traduites | `purgatorian1868:invocation-trinite-ames-purgatoire` |
| Acte héroïque de charité (*Purgatorian Consoler*, p. 437) | **déjà présent** (`jardin:acte-heroique-de-charite`, *Livre d'or des âmes du purgatoire*, 1925) | — |
| Dévotion aux cinq plaies (Bona Mors, p. 12-16) | laissée : dévotion publique chantée (chantre et chœur) ; Beringer donne d'autres prières aux cinq plaies | — |
| Litanie « du Rituel romain », court chemin de croix (Bona Mors) | laissés (la litanie est celle de la recommandation de l'âme) | — |
| Litanies, prière et neuvaine de S. François (Cordon 1878) | laissées : la notice de Québec de 1867 (`cihm_29653`, *imprimatur* du 24 mai 1867) contient « Neuvaine à St. François d'Assise » et « Litanies de St. François », mais le scan ne donne de plusieurs pages que la marge (page des litanies absente) ; le manuel de 1885 (`cihm_62202`) est en anglais à cet endroit | — |
| Neuvaine pour les âmes (*Purgatorian Consoler*) | laissée (longue ; chercher d'abord le *Livre d'or*) | — |

## Traductions de travail à relire par l'utilisateur

| Id | Original | Page |
|---|---|---|
| `bonamors1896:colloque-saint-pie-v` | *Colloquy with Christ Crucified (Prayers of St. Pius V)* | Bona Mors 1896, p. 22-23 |
| `purgatorian1868:invocation-trinite-ames-purgatoire` | *An Invocation of the Most Holy Trinity for the Souls in Purgatory* | *Purgatorian Consoler* 1868, p. 312-313 |

Points à trancher : « *Apostles' Creed* » rendu par la rubrique « Je crois en Dieu » ; « *look down upon* » rendu
« abaissez vos regards sur » ; « *sorrowing and afflicted Mother* » rendu « Mère affligée et désolée » (ordre des
adjectifs inversé pour l'oreille : à revoir) ; « *refresh the three children in the burning fiery furnace* » rendu
« rafraîchi les trois enfants dans la fournaise ardente » ; « *fiercest pangs of love* » rendu « les plus vives angoisses
de l'amour ».

## Proposition d'intégration (non appliquée)

« Le moins pour le plus, le simple mais le saint, la variété mais la sobriété. » Aucune ligne quotidienne nouvelle ;
on prolonge des séquences existantes.

1. **Chapelet du jour — fruit du mystère** (proposition principale) : après chaque dizaine, la courte prière du
   Rosaire-Vivant pour le mystère de la dizaine (`rosairevivant1841:fruits-des-quinze-mysteres`, section du mystère),
   en point d'insertion du chapelet existant, `selon` le jour (joyeux, douloureux, glorieux). Une ou deux lignes par
   dizaine, approuvées (Montréal, 1841), et la variété suit le cycle déjà réglé du chapelet.
2. **Mercredi (saint Joseph)** : `cordonjoseph1871:souvenez-vous-a-saint-joseph` en alternance avec la prière du
   mercredi déjà livrée (une semaine sur deux), et les jaculatoires « Jésus, Marie, Joseph » à la fin de la prière du
   soir **du mercredi seulement**.
3. **Mardi (sainte Face)** : `janvier:priere-de-pie-ix-sainte-face` en conclusion de la dévotion du mardi (cinq
   lignes), en rotation avec ce qui existe.
4. **Indulgences plénières** (premiers vendredis et samedis, fêtes) : là où la ligne demande « prières aux intentions du
   Souverain Pontife », proposer `desgenettes:cinq-prieres-intentions-souverain-pontife` comme forme développée,
   facultative (les cinq *Pater* et *Ave* restent la forme courte).
5. **Saint Nom de Jésus** : `saintnom1899:petit-office-saint-nom-de-jesus` une fois l'an, à la fête du saint Nom (dimanche
   entre la Circoncision et l'Épiphanie), ou le deuxième dimanche du mois pour qui est confrère. Pas plus : c'est un
   office de cinq psaumes.
6. **Juillet (Précieux Sang)** : `beringer:offrande-du-precieux-sang`, une ligne, après le chapelet du Précieux Sang
   déjà proposé par l'audit EN.
7. **Novembre (défunts)** : `purgatorian1868:invocation-trinite-ames-purgatoire` (après relecture de la traduction), en
   alternative le dimanche à la prière du jour pour les âmes.
8. Le reste (Dupont, adorations, offrande pour la France, litanies de l'humilité, Milice angélique, Saint-Joseph de
   Montréal, Garde d'honneur, colloque de S. Pie V) : recueil, consultable, sans ligne au programme.

Classement **deviné** ajouté dans `data/prieres/dimensions-textes.json` pour les seules pièces des points 1 à 7
(8 entrées, champ `devinee`) : `rosairevivant1841:fruits-des-quinze-mysteres`, `saintnom1899:petit-office-saint-nom-de-jesus`,
`janvier:priere-de-pie-ix-sainte-face`, `cordonjoseph1871:souvenez-vous-a-saint-joseph`,
`cordonjoseph1871:jaculatoires-jesus-marie-joseph`, `desgenettes:cinq-prieres-intentions-souverain-pontife`,
`beringer:offrande-du-precieux-sang`, `purgatorian1868:invocation-trinite-ames-purgatoire`.

## Indulgences

Rien n'est ajouté à `data/prieres/indulgences.json`. Concessions citées par les manuels, à vérifier dans
l'*Enchiridion* 1952 avant tout compte : petit office du saint Nom (confrérie dominicaine) ; Souvenez-vous à saint
Joseph (Pie IX, 25 juin 1863) ; « Bon saint Joseph, notre guide » (Pie IX, 27 janv. 1863) ; « Jésus, Marie, Joseph »
(Pie VII, 28 avril 1807) ; offrande du Précieux Sang (Pie VII, 22 sept. 1817 ; Ench. 1952,
*Pater aeterne, offero tibi Sanguinem pretiosissimum…*) ; colloque de S. Pie V (« 60 days »).
