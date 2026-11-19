# Audit du corpus de prières (18 novembre 2026)

Agent « Audit du corpus de prières ». Lecture seule : aucun texte de prière n'a été modifié.

## Périmètre

- Fichiers lus : `data/prieres/sources.json` (142 pièces), `data/prieres/jardin.json` (62 pièces du livret),
  `app/src/lib/seed.ts`, `app/src/lib/liste.ts`, `app/src/lib/plan.ts`, `app/src/lib/calendrier.ts` (`MOIS_DEVOTION`),
  `app/src/lib/meditations.ts` (`RECUEIL_DU_MOIS`) et `data/calendar/2026-2027.json`.
- Les critères sont ceux de la mission. Ils sont lus à la lumière de la SPEC, § 10 et § 11, surtout du principe 1 du § 11 :
  une prière n'apparaît qu'une fois par jour.
- **Indulgences : hors du champ de cet audit**, à la demande de la session principale, qui corrige `indulgences.json`.
  - Règle de l'utilisateur : seules les œuvres de l'*Enchiridion* de 1952 sont indulgenciées.
  - Les écarts relevés avant cette consigne sont seulement transmis, en annexe A.
- **Gravité** :
  - **bloquant** : enfreint une règle absolue (texte sans source, promesse sans source, source bannie ou non admise) ou le
    principe « une fois par jour » ;
  - **à corriger** : erreur avérée ;
  - **à vérifier** : doute à lever sur le scan ou la source ;
  - **suggestion** : amélioration.
- **Identifiants** : `jardin:` désigne une pièce du livret (identifiant de `jardin.json` précédé de `jardin:`, comme dans
  l'app). Les autres sont ceux de `sources.json`.

## Résumé

- **Exactitude** : très bonne pour les pièces recopiées d'éditions anciennes.
  - Sur un échantillon de 54 pièces comparées à leur scan, aucune coquille d'OCR ni aucun mot modernisé n'ont été trouvés
    dans les textes. Les seuls écarts viennent de la couche OCR des scans.
  - Deux divergences d'édition et une rubrique abrégée sont à reprendre (§ 4).
- **Faiblesse principale : le livret.**
  - Une vingtaine de pièces du *Jardin de l'âme* n'ont pas de source ancienne. Certaines sont des compositions modernes
    (offrande du matin, devoirs de charité, etc.).
  - Plusieurs promesses y sont données sans source (chapelet de saint Michel, sept grâces des Douleurs, promesses du
    Rosaire).
  - La promesse de saint Michel figure encore dans `jardin.json`, alors qu'`A_FOURNIR.md` la dit retirée.
- **Agencement : des répétitions systématiques**, contraires au § 11, principe 1.
  - Les lignes « Dévotion du jour de la semaine » reprennent des prières qui ont déjà leur ligne propre le même jour.
  - C'est le cas cinq jours sur sept : chapelet des Morts le lundi, chapelet de saint Michel le mardi, litanies de saint
    Joseph et prière pour la pureté le mercredi, communion spirituelle le jeudi, Crucifix le vendredi, Cœur affligé de
    Marie et litanies de la sainte Vierge le samedi.
- **Temps liturgique : peu exploité.**
  - Le seul remplacement saisonnier est celui de l'Angélus par le Regina cæli.
  - Les antiennes mariales du temps sont transcrites (Weber) mais ne sont reliées à rien.
  - Il n'y a rien pour le Carême ni la Semaine sainte : pas de chemin de croix, pas de Miserere.
  - Pour la Fête-Dieu, ni Adoro te ni Lauda Sion ; pour le Christ-Roi et le 31 décembre, aucun lien.
  - Trois mois n'ont aucune prière propre : février (Sainte Famille), août (Cœur immaculé) et octobre (la prière à saint
    Joseph *Ad te, beate Ioseph*, qui suit le chapelet en octobre).
- **Sélection** :
  - doublons d'édition : Flèche d'or, petite couronne de Montfort, litanies du Sacré-Cœur, exercice du Cœur affligé de
    Marie, promesses de la sainte Face, treize mardis et quinze mardis ;
  - une prière à l'intention périmée : celle du cardinal Mercier, qui demande la canonisation de Montfort, faite en 1947 ;
  - plusieurs litanies non approuvées pour l'usage public, à signaler comme privées.

---

## 1. Pertinence selon le jour, la semaine, le mois et l'année

### 1.1 Dédicace des jours de la semaine

La dédicace est correcte et traditionnelle : dimanche, la Trinité ; lundi, les défunts ; mardi, les Anges ; mercredi, saint
Joseph ; jeudi, le Saint-Sacrement ; vendredi, la Passion et le Sacré-Cœur ; samedi, la sainte Vierge. Les écarts :

| # | Pièce | Gravité | Constat | Correction proposée |
|---|---|---|---|---|
| T1 | `LITANIES_PAR_JOUR[4]` (jeudi) : `paroissien:litanies-saint-nom` | suggestion | Les litanies du saint Nom tournent déjà le dimanche. Le jeudi, consacré au Saint-Sacrement, en reçoit aussi. | Le jeudi : les seules litanies du Saint-Sacrement (`fervent:litanies-saint-sacrement`). Pour une deuxième pièce, l'*Adoro te devote* (Ench. 1952, n° 166 ; traduction ancienne à transcrire, par ex. Paroissien romain, Tours, Mame, 1890, qui donne les hymnes du Saint-Sacrement : à vérifier). |
| T2 | `LITANIES_PAR_JOUR[2]` (mardi) : `jardin:litanies-de-la-sainte-face` | suggestion | Le mardi est bien le jour de la sainte Face selon sœur Marie de Saint-Pierre. Le mardi mêle donc deux dédicaces (Anges, sainte Face), ce qui est voulu. | Garder, mais l'écrire dans le titre de la ligne (« mardi : saints Anges et sainte Face »), pour que l'alternance se comprenne. |
| T3 | `jardin:heure-sainte` dans « Dévotion du jeudi » | à corriger | L'Heure sainte est donnée **tous les jeudis** par la dévotion du jeudi. Le plan la donne **aussi** la veille du premier vendredi (« Heure sainte (veille du premier vendredi) », `plan.ts`). Le premier jeudi du mois, elle paraît deux fois. | Une seule déclaration : chaque jeudi, facultative, *ou* le premier jeudi seulement. Voir Q3. |
| T4 | `jardin:auguste-reine-des-cieux` (usage « quot. ; surtout le mar. ») | suggestion | La pièce n'est reliée à aucune ligne. | La rattacher au mardi (saints Anges) comme pièce de la roue. Le texte est déjà celui de l'Ench. 1952, n° 345 (vérifié). |

### 1.2 Temps liturgique et fêtes

| # | Pièce | Gravité | Constat | Correction proposée |
|---|---|---|---|---|
| T5 | `beringer:salve-regina` (matin) et `beringer:sub-tuum` (soir) ; `weber:alma-redemptoris`, `weber:ave-regina-caelorum`, `beringer:regina-caeli` | à corriger | L'antienne mariale ne change pas avec le temps. Les antiennes du temps sont transcrites, Weber 1890 donnant leurs dates (Alma de l'Avent à la Purification, Ave Regina jusqu'au Jeudi saint, Regina cæli au temps pascal, Salve ensuite), mais aucune n'est reliée. Au temps pascal, le Regina cæli remplace déjà l'Angélus (`PASCAL`, `liste.ts`). | Ajouter à `remplacementsDuTemps` la règle de l'antienne du temps, d'après les rubriques de Weber, p. 305-308. Le choix de la ligne (matin ou soir) est à arbitrer : voir Q1. |
| T6 | Carême, temps de la Passion, Semaine sainte | à corriger (manque) | Ces temps n'ont **aucune prière propre**. Le *Stabat Mater* (`weber:stabat-mater`) et les quinze oraisons de sainte Brigitte existent, mais ne sont pas liés au temps. | (a) Chemin de croix de saint Alphonse, dans *Livre de prières et de méditations* (scan Google, exemplaire de la Bibliothèque de l'Adoration réparatrice, `/tmp/claude-0/lig2/lp.pdf`, chapitre « Le Chemin de la Croix » ; l'édition est à relever sur la page de titre). Ou celui du Manuel de Janvier 1895 (« Exercice du Chemin de la Croix pour les besoins de l'Église », `vendor/sources/face/janvier.pdf`). (b) Le *Miserere* (Ps 50), latin et français, dans le Paroissien 1890. (c) Le *Stabat* relié aux vendredis de Carême et au temps de la Passion. |
| T7 | Fête-Dieu et son octave | suggestion (manque) | Pas d'hymne eucharistique. | *Adoro te devote* et *Lauda Sion* (Ench. 1952, n° 166 et 167). Texte latin et traduction du Paroissien 1890, aux offices de la Fête-Dieu. |
| T8 | Christ-Roi (dernier dimanche d'octobre) | suggestion | `thesaurisons:au-christ-roi` ne sert qu'aux anniversaires du baptême. | Le relier aussi à la fête. L'acte de consécration du genre humain, *Iesu dulcissime, Redemptor humani generis*, figure dans l'Ench. 1952 (à transcrire depuis une traduction ancienne approuvée). |
| T9 | 31 décembre et 1er janvier | suggestion | `paroissien:te-deum` et `jardin:veni-creator-spiritus` ne sont rattachés ni au dernier jour de l'année ni au premier. | Te Deum le 31 décembre, Veni Creator le 1er janvier : c'est la coutume, et l'Ench. 1952, n° 684 b, nomme le dernier jour de l'année. |
| T10 | Pentecôte | suggestion | Le Veni Creator est en place. La séquence *Veni, Sancte Spiritus* manque ; seule l'invocation brève est dans la Triple Couronne. | Séquence, latin et traduction, du Paroissien 1890 (messe de la Pentecôte), pour l'octave et la neuvaine du Saint-Esprit. |
| T11 | Neuvaine au Saint-Esprit (plan, 7-15 mai 2027) | à corriger (manque) | Aucun texte n'est relié : la neuvaine est absente de `TEXTES_DES_DEVOTIONS`. Il en va de même pour les neuvaines à saint Joseph, à saint Michel et à saint Gabriel, et pour celle de Montfort, déjà notée dans REPRISE. | Saint-Esprit : la *Neuvaine du Saint-Esprit* authentique de saint Alphonse (*Œuvres*, 1876, t. XIV, p. 373-391), déjà repérée dans `A_FOURNIR.md` ; ou le Veni Creator chaque jour, à défaut. Saint Joseph : les sept Douleurs et Allégresses (`jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph`). Saint Michel : le chapelet de saint Michel (voir aussi la tradition, § 2). Saint Gabriel : l'oraison `jardin:a-saint-gabriel-archange`. |
| T12 | « Prière à S. Gabriel » le 24 mars 2027, mercredi saint ; neuvaine du 15 au 23 mars | à vérifier | En 2027, la fête tombe pendant la Semaine sainte. Le plan garde la prière ce jour-là. | Vérifier avec l'agent « Liturgie » le sort de la fête selon les rubriques de 1954 (empêchée ou transférée). Décaler la prière et la neuvaine en conséquence. |
| T13 | `jardin:a-marie-mediatrice-de-toutes-graces` (usage « sam. ; 31 mai ») | à vérifier | Messe propre de certains lieux, accordée en 1921. Depuis 1954, le 31 mai est la fête de Marie Reine, que le moteur (« calendrier 1954 ») place sans doute ce jour-là. | Garder l'oraison comme prière du samedi. Pour le 31 mai, signaler qu'il s'agit de la fête locale d'avant 1954. |

### 1.3 Mois consacrés

`MOIS_DEVOTION` donne un nom et une référence à chaque mois. Seuls cinq mois ont un recueil de méditations
(`RECUEIL_DU_MOIS` : mars, mai, juin, juillet, novembre). Prières disponibles ou absentes pour les autres mois :

| # | Mois | Gravité | Constat | Correction proposée |
|---|---|---|---|---|
| M1 | Janvier (saint Nom) | suggestion | `paroissien:litanies-saint-nom` existe, mais n'est pas reliée à la ligne « Dévotion du mois ». | Relier les litanies du saint Nom à la ligne de janvier. |
| M2 | Février (Sainte Famille) | à corriger (manque) | Le corpus ne contient **aucune prière à la Sainte Famille**. | Consécration de la famille à la Sainte Famille (Léon XIII, 1892). Elle figure dans l'Ench. 1952 (*Consecratio sacrae Familiae*, section Sainte Famille). Traduction française ancienne à transcrire, par ex. depuis un manuel d'avant 1958 imprimé avec approbation. |
| M3 | Avril (mois eucharistique) | suggestion | Les *Visites au Saint-Sacrement* de saint Alphonse (`liguori-visites`) sont dans la bibliothèque, mais ne sont pas liées au mois. | Une visite par jour en avril, en lecture. |
| M4 | Août (Cœur immaculé de Marie) | suggestion | `weber:priere-tres-saint-coeur-de-marie` existe, mais n'est pas reliée au mois. | La relier au mois d'août. Piste : un mois du Cœur immaculé ancien, à chercher. |
| M5 | Octobre (Rosaire) | à corriger (manque) | La prière à saint Joseph *Ad te, beate Ioseph*, que Léon XIII a prescrite après le chapelet en octobre (encyclique *Quamquam pluries*, 1889), est **absente**. | Ench. 1952, n° 476 (*Ad te, beate Ioseph*, vu à la table). Traduction ancienne à transcrire : Beringer 1925 la donne dans la partie « saint Joseph ». À insérer en fin de chapelet en octobre, ce qui rejoint les points d'insertion du § 11, principe 2. |
| M6 | Décembre (Immaculée Conception) | suggestion | La neuvaine (du 29 novembre au 7 décembre) et le petit chapelet existent. Après le 8, rien n'est relié. | Le petit chapelet de l'Immaculée Conception (`weber:petit-chapelet-immaculee-conception`) comme dévotion du mois. |
| M7 | Septembre (Douleurs) | suggestion | Trois pièces se recouvrent : `jardin:les-sept-douleurs-de-marie`, `beringer:coeur-afflige-de-marie` et `weber:o-quot-undis`. | Garder une seule forme de l'exercice (voir S3) et le *Stabat* comme hymne du mois. |

---

## 2. Conformité à la tradition

### 2.1 Textes sans source ancienne (livret)

Règle : aucun texte de mémoire ; sources anciennes identifiées seulement. `A_FOURNIR.md` connaît déjà le problème
(« 29 pièces du livret sans ligne source »). Les pièces suivantes n'ont **aucune** source, ou sont manifestement des
compositions récentes :

| # | Pièce | Gravité | Constat | Correction proposée |
|---|---|---|---|---|
| D1 | `jardin:intention-d-indulgences`, `jardin:acte-de-soumission-a-la-volonte-de-dieu`, `jardin:acte-d-intention-de-communion-spirituelle-perpetuelle`, `jardin:acte-de-recommandation-des-ames-rencontrees` ; recopiées dans `hortus:offrande-du-matin` | **bloquant** | Pas de source. Le style est moderne : « baiser mystique déposé sur Votre hostie », « canal muet de grâce », « Co-Rédemptrice ». Ce sont des compositions. Un paragraphe de l'acte de soumission (« j'accepte de votre main le genre de mort… ») reprend une prière ancienne connue, qui doit garder sa forme propre. | Au choix de l'utilisateur (Q2). (a) Les marquer « composé pour le livret », comme `hortus:renouvellement-cordon-saint-joseph`. (b) Ou les remplacer par des formules anciennes : offrande de l'Apostolat de la prière (Gautrelet, *Le premier vendredi…*, scan `/tmp/claude-0/gau/v.pdf`, déjà au chantier « Apostolat de la prière ») ; communion spirituelle de saint Alphonse (*Visites*, Lyon, Périsse, 1862, déjà transcrites dans `liguori-visites`) ; acceptation de la mort : la prière de saint Pie X, à chercher dans l'Ench. 1952, section « Pro bona morte », pour en prendre la forme exacte. |
| D2 | `jardin:devoir-envers-l-eglise-et-ses-ministres`, `-la-famille`, `-la-patrie`, `-les-pauvres-…`, `-moi-meme` | **bloquant** | Compositions récentes, sans source : « Saint Pie X, défenseur de la foi », « martyrs de la Révolution », « retour d'un saint pape ». La dernière intention est une prise de position ecclésiologique ; elle relève du choix de l'utilisateur, pas d'un texte reçu. | Comme D1 : les marquer « composé » ou les remplacer (Q2). Pour la patrie, piste ancienne : la prière pour la France du *Paroissien romain* 1890 (*Domine, salvam fac…*, à vérifier). |
| D3 | `jardin:oraison-a-marie` | à corriger | La rubrique l'attribue au *Secret de Marie*, sans édition. | Sourcer sur une édition ancienne du *Secret de Marie* (XIXe s.), ou sur l'édition Gaume du *Traité*, si elle la donne (à chercher dans `/tmp/claude-0/mtf/m.pdf`). |
| D4 | `jardin:la-petite-couronne-de-la-tres-sainte-vierge` | à corriger | Source : « Œuvres complètes de saint Louis-Marie, **1966** ». C'est une édition postconciliaire, et le texte double `montfort:petite-couronne` (Gaume 1843). | Retirer cette version ; garder `montfort:petite-couronne` (Gaume 1843, p. 204, vérifiée). |
| D5 | `jardin:la-triple-couronne-d-or-du-sacre-c-ur-de-jesus` et ses trois couronnes (ordres 21 à 24) ; `hortus:triple-couronne-1/2/3` | **bloquant** | Pas de source. Les pages composées tirent de là leur ordinaire, et le texte parle de « la délivrance de notre sainte Mère l'Église ». | Retrouver le manuel d'origine : Garde d'honneur du Sacré-Cœur, Bourg (fin du XIXe s.). Sinon, inscrire la pièce dans `A_FOURNIR.md`. |
| D6 | `jardin:offrande-de-la-sainte-face` | à corriger | Pas de source. Ses « promesses » doublent `janvier:promesses-sainte-face`. | Prendre l'offrande et les promesses dans Janvier 1895 (`vendor/sources/face/janvier.pdf`) ; supprimer la notice du livret. |
| D7 | `jardin:les-sept-offrandes-du-precieux-sang` | à corriger | Pas de source. La comparaison avec *Thésaurisons* n'a rien retrouvé. | Traduction ancienne à identifier : Beringer 1925, partie « Précieux Sang », ou Boylesve 1882 (mois du Précieux Sang, déjà utilisé). |
| D8 | `jardin:litanies-de-notre-dame-des-sept-douleurs` | à corriger | Pas de source. Ces litanies ne sont pas approuvées pour l'usage public (voir T-L). | Sourcer sur un manuel ancien (Weber 1890, partie « Notre-Dame des Douleurs », p. 380-400, à vérifier) ou les retirer. |
| D9 | `jardin:chapelet-des-saintes-plaies` | à vérifier | Pas de source. C'est une révélation privée (sœur Marie-Marthe Chambon). Son statut ecclésiastique n'est pas indiqué dans la pièce. | Sourcer sur un opuscule ancien, avec l'imprimatur, et indiquer le statut d'après ce document. Ne rien affirmer sans lui. |
| D10 | `jardin:priere-du-cardinal-mercier` | à corriger | Pas de source. L'intention est périmée : canonisation de Montfort, faite en 1947. Elle demande aussi la définition de la Médiation universelle, question pendante. | La retirer de la sélection (S6) ou la garder comme document historique, sans usage. |
| D11 | Notices de pratique sans source : `jardin:cinq-dimanches-des-stigmates-…`, `sept-dimanches-de-saint-joseph`, `treize-mardis-de-saint-antoine` (ordre 51), `quinze-mardis-de-saint-dominique` (ordre 52), `premier-mercredi-du-mois`, `treize-vendredis-…`, `sept-vendredis-des-douleurs`, `douze-samedis-…`, `sept-samedis-…` | à corriger | Ce sont des rubriques de pratique, pas des prières, mais leur règle (nombre de jours, conditions) doit avoir une source. | Les rattacher à l'article de l'Ench. 1952 qui définit l'exercice (la session principale tient ces références) ou à Beringer 1925. |

### 2.2 Révélations privées et promesses

| # | Pièce | Gravité | Statut, constat | Correction proposée |
|---|---|---|---|---|
| R1 | `jardin:chapelet-de-saint-michel-archange`, notice « Promesses » (Antonia d'Astonaco, 1751) | **bloquant** | La promesse n'a pas de source. `A_FOURNIR.md` (audit du 17 nov.) dit que la mention « a été retirée », mais elle est **toujours dans `jardin.json`**, donc dans l'app. | Retirer la notice ; ne la rétablir qu'avec une source ancienne (*Raccolta* 1910 ou autre), comme prévu dans `A_FOURNIR.md`. |
| R2 | `jardin:les-sept-douleurs-de-marie`, notice « Les sept grâces promises » (« selon les révélations de sainte Brigitte ») | **bloquant** | Pas de source ; ces sept grâces ne sont pas référencées dans les *Révélations*. L'**offrande du chapelet** vient en outre d'une « Confrérie Marie Corédemptrice, paroisse Saint-Eugène–Sainte-Cécile », source contemporaine hors des sources admises, et sa formulation est récente (« notre unique voie pour venir à vous »). | Retirer la notice et l'offrande ; garder le corps de l'exercice (Beringer, n° 138, texte vérifié par ailleurs, voir S3). |
| R3 | `jardin:quinze-samedis-du-rosaire`, notice « Promesses du Rosaire » (saint Dominique et le bienheureux Alain de la Roche) | **bloquant** | Pas de source. Le texte en est un résumé. | Les retirer, ou les citer textuellement d'une source ancienne : un manuel du Rosaire avec approbation, par ex. Sambucy 1837 (`/tmp/claude-0/sam/s.pdf`), qui parle d'Alain de la Roche (à vérifier : la liste des quinze promesses y figure-t-elle ?). |
| R4 | `jardin:les-quinze-oraisons-de-sainte-brigitte` | à corriger | La notice signale correctement le *monitum* du Saint-Office de 1954, et les promesses ne sont pas reproduites. Mais l'usage, « quot., **pendant une année entière** », est la pratique liée à ces promesses. Source sans page : « Les trois dévotions des prédestinés, 1888 ». | Usage : « quotidien, ou le vendredi », sans durée d'un an. Ajouter l'édition et la page de la source. |
| R5 | `jahenny:scapulaire-benediction-protection` | à vérifier | Révélation privée (Marie-Julie Jahenny, 1878). Aucune approbation canonique n'est connue de l'audit ; le statut est à établir d'après une source. La source est *La Bonne Nouvelle*, publication contemporaine hors des sources admises, texte fourni par l'utilisateur. La pièce l'annonce honnêtement comme révélation privée. | Indiquer dans la fiche « révélation privée, non examinée par l'Église » ou le statut exact, si une source le donne. Chercher une édition ancienne des extases (P. Roussel, 1878-1880). L'intégration au matin et au soir est décidée au § 11. |
| R6 | `jardin:premiers-samedis-du-mois` (Pontevedra, 1925) | à vérifier | Les apparitions de Fatima sont approuvées (évêque de Leiria, 1930). La demande de Pontevedra est rapportée par sœur Lucie. La traduction de la promesse n'a pas de source. | Citer la traduction de La Porte Latine (FSSPX, source admise), déjà utilisée pour les couronnes (REPRISE, point 8). |
| R7 | `jardin:premiers-vendredis-du-mois`, `jardin:heure-sainte` | conforme | Sainte Marguerite-Marie, canonisée ; sources citées (*Vie et Œuvres*, 1915). | — |
| R8 | `jardin:la-fleche-d-or`, `janvier:*`, `thesaurisons:sainte-face-therese` | conforme | Sœur Marie de Saint-Pierre : la dévotion est reçue par l'Archiconfrérie de la Sainte-Face (manuel de Janvier « revu d'après les décrets du Saint-Office »). | Voir S1 pour le doublon. |
| R9 | `jardin:auguste-reine-des-cieux` (P. Cestac) | conforme | La prière figure dans l'Ench. 1952, n° 345 ; le texte français est identique (vérifié). | Ajouter la source « Ench. 1952, n° 345 » dans la fiche (la pièce n'en a pas). |

### 2.3 Litanies non approuvées pour l'usage public

| # | Pièces | Gravité | Constat | Correction proposée |
|---|---|---|---|---|
| T-L | `fervent:litanies-sainte-trinite`, `fervent:litanies-ange-gardien`, `fervent:litanies-saint-sacrement`, `jardin:litanies-de-la-sainte-face`, `jardin:litanies-de-notre-dame-des-sept-douleurs`, `fsspx:litanies-…`, `salve-regina:litanies-…`, `petit-sacristain:litanies-bonne-mort`, `breviaire-sc:litanies` | suggestion | Seules les litanies des Saints, de Lorette, du saint Nom, du Sacré-Cœur et de saint Joseph sont approuvées pour l'Église entière (l'Ench. 1952 n'indulgencie que celles-là). Les autres sont des litanies **de dévotion privée**. Leur usage privé est légitime, mais l'app ne le dit pas. `breviaire-sc:litanies` le dit, lui : c'est le texte d'avant l'approbation de 1899. | Une mention uniforme « litanies de dévotion privée » dans l'usage de chaque pièce. |
| T-S | `salve-regina:litanies-fideles-defunts` (salve-regina.com) ; `petit-sacristain:litanies-bonne-mort` (blog *Le Petit Sacristain*, 2016) | à vérifier | Ces sites sont hors des sources admises pour les prières courantes (sites sédévacantistes ou FSSPX, ou Catholique de France). Les textes ont été fournis par l'utilisateur. La pièce de salve-regina.com cite elle-même sainte Thérèse, donc elle est postérieure à 1925, et son « auteur [est] inconnu ». | Chercher une source ancienne. Pour la bonne mort, les litanies « Quand mes pieds immobiles… » se trouvent dans des manuels du XIXe s. (par ex. le *Livre de prières* de saint Alphonse, `/tmp/claude-0/lig2/lp.pdf` : à vérifier). Sinon, demander à l'utilisateur s'il garde ces sources (Q5). |
| T-C | `beringer:sub-tuum` : invocations « Domina nostra, Mediatrix nostra… » (christusregnat.com) | à vérifier | Site hors de la liste admise ; fourni par l'utilisateur. Pas de source ancienne. Conformément au § 11, le français n'est pas donné ; c'est bien le cas. | Chercher une source ancienne de ces invocations (manuel latin d'avant 1958). En attendant, mentionner dans la fiche « source : site, fourni par l'utilisateur ». |

---

## 3. Agencement

### 3.1 Répétitions dans une même journée (§ 11, principe 1)

La liste de départ (`listeParDefaut`) et les migrations de `seed.ts` relient la même prière à deux lignes **le même
jour** :

| # | Jour | Prière répétée | Lignes en cause | Gravité | Correction proposée |
|---|---|---|---|---|---|
| A1 | Lundi | `beringer:chapelet-des-morts` et `paroissien:de-profundis` | « Chapelet des Morts » (`jour(1)`, `LIENS_SOURCES`) **et** « Dévotion du lundi » (`DEVOTIONS_SEMAINE[1]`) | **bloquant** | Une seule déclaration dans le programme. La dévotion du lundi devient le chapelet des Morts lui-même, ou une autre pièce (litanies des défunts, acte héroïque). |
| A2 | Mardi | `jardin:chapelet-de-saint-michel-archange` | « Chapelet de saint Michel » (`jour(2)`) **et** « Dévotion du mardi » | **bloquant** | Idem : la dévotion du mardi est le chapelet de saint Michel, avec l'oraison à saint Gabriel et *Auguste Reine* (T4). |
| A3 | Mercredi | `beringer:litanies-saint-joseph` | « Litanies du jour » (`LITANIES_PAR_JOUR[3]`) **et** « Dévotion du mercredi » | **bloquant** | La dévotion du mercredi donne les Douleurs et Allégresses de saint Joseph ; les litanies restent à « Litanies du jour ». |
| A4 | Mercredi | `beringer:saint-joseph-purete` | « Cordon de saint Joseph : renouvellement… » (`CORDON_TEXTES`) **et** « Dévotion du mercredi » | **bloquant** | La prière pour la pureté va seulement dans la page du cordon du mercredi (§ 11 : une page « renouvellement + sept Gloria »). |
| A5 | Jeudi | `jardin:acte-d-intention-de-communion-spirituelle-perpetuelle` | « Offrande du matin » (`hortus:offrande-du-matin`, chaque jour) **et** « Dévotion du jeudi » | **bloquant** | La retirer de la dévotion du jeudi, qui garde l'Heure sainte et les litanies du Saint-Sacrement, ou une Visite de saint Alphonse. |
| A6 | Vendredi | `jardin:chaque-vendredi-devant-le-crucifix` | « Devant le Crucifix » (`jour(5)`, 15 h) **et** « Dévotion du vendredi » | **bloquant** | Une seule ligne. |
| A7 | Vendredi | `beringer:litanies-sacre-coeur` | « Dévotion du vendredi » **et** roue « Litanies du vendredi », une semaine sur deux | **bloquant** | La dévotion du vendredi garde le Crucifix ; les litanies restent à la roue. |
| A8 | Samedi | `paroissien:litanies-sainte-vierge` | « Dévotion du samedi » **et** roue « Litanies du samedi », une semaine sur deux | **bloquant** | La dévotion du samedi garde le Cœur affligé ou le petit office ; les litanies restent à la roue. |
| A9 | Samedi | Invocation n° 1 du « Cœur affligé de Marie » | `beringer:coeur-afflige-de-marie` (dévotion du samedi) **et** `beringer:don-crainte` (« Demande du don de crainte de Dieu », samedi soir), qui en est un extrait | **bloquant** | Le samedi, ne pas donner de ligne « don » séparée (le don est demandé dans l'exercice) ; ou changer la pièce du samedi. |
| A10 | Dimanche | `fervent:litanies-sainte-trinite` | « Dévotion du dimanche » **et** roue « Litanies du dimanche » | **bloquant** | La dévotion du dimanche reçoit une autre pièce trinitaire, par ex. le Te Deum ou le *Gloria Patri* médité, ou rien. |
| A11 | Chaque jour | `beringer:cordon-saint-joseph` **et** `hortus:cordon-sept-gloria` sur la même ligne (`remplacerTextes('cordon-gloria')`) | La notice de Beringer et l'arrangement disent tous deux « sept Gloria ». | à corriger | Le § 11 décide d'une seule page. Garder `hortus:cordon-sept-gloria` et mettre la notice de Beringer en tête de page. |
| A12 | Chaque jour | Jaculatoires `thesaurisons:jac-33` (« Mon Jésus, miséricorde ») et `jac-85` (« Jésus, doux et humble de cœur ») | Elles sont aussi dans les pages de la Triple Couronne (`hortus:triple-couronne-*`). | suggestion | Le § 11 retire les jaculatoires de la liste : la répétition disparaît d'elle-même. Sinon, exclure de la rotation celles que contient la couronne du jour. |

Cause de fond : `DEVOTIONS_SEMAINE` a été écrit pour une ligne générique « Dévotion du jour », avant que les mêmes prières
aient leur ligne propre. Le **programme unique** du § 11 doit déclarer chaque pièce une fois, et le test « un texte par
jour » doit parcourir aussi l'intérieur des pages composées.

### 3.2 Ordre dans la journée

| # | Pièce | Gravité | Constat | Correction proposée |
|---|---|---|---|---|
| A13 | « Offrande du matin » (`liste:1`), avant « Prière du matin » (`liste:2`) | à corriger | L'usage de `hortus:offrande-du-matin` dit « à la suite de la prière du matin », mais la liste la place avant. La prière du matin du Paroissien contient déjà une offrande de la journée (« Je vous en consacre toutes les pensées, les paroles, les actions et les peines »). L'« Intention d'indulgences » la redit. | Ordre proposé : signe de croix et offrande brève au lever (une phrase, par ex. l'offrande de l'Apostolat de la prière), puis la prière du matin, puis les actes complémentaires. Voir Q4. |
| A14 | Soir : « Prière du soir et examen » (`liste:22`), puis Sub tuum, Litanies du jour, Demande d'un don | à corriger | La prière du soir du Paroissien se termine par la recommandation à Dieu pour la nuit. L'antienne mariale finit traditionnellement la journée, comme aux Complies. Les litanies et le don viennent donc après l'examen et avant l'antienne. | Ordre : Litanies du jour, Demande du don, Prière du soir et examen, Sub tuum ou antienne du temps (T5) **en dernier**. |
| A15 | `sambucy:chapelet-saint-dominique`, usage « (voir la roue des trois chapelets) » | à corriger | La roue des chapelets est retirée (`roue-chapelets-retiree`, SPEC § 10). | Usage : « voir le chapelet du jour ». |
| A16 | `hortus:chapelet-*` : rubrique de Sambucy en tête de page (« Manière de le réciter », « Méditation des mystères », chapelet de sainte Brigide) | suggestion | Une page pratique commence par deux paragraphes d'explication, dont l'un parle d'un autre chapelet. | Replier ces rubriques dans une section dépliable « Notice » (§ 11, principe 4). |
| A17 | `jardin:les-quinze-oraisons-de-sainte-brigitte` (chaque jour, ~11 000 signes) et `hortus:petit-breviaire-du-jour` (chaque jour, ~13 000 à 22 000 signes) | suggestion | Ces deux pièces très longues s'ajoutent chaque jour au chapelet, à la Triple Couronne et au reste. C'est contraire à la règle « le plus de dévotion avec le moins d'actes ». Le § 11 fait déjà des oraisons la méditation de la Passion. | Brigitte : méditation de la Passion (§ 11), le vendredi et en Carême. Petit bréviaire : dans Lecture › Office (§ 11), hors de la liste. |

---

## 4. Exactitude des textes

### 4.1 Méthode

- Chaque pièce a été alignée mot à mot (`difflib`) sur la couche texte de son scan, après normalisation des ligatures,
  des traits d'union de fin de ligne et du balisage de l'app.
- Pour les longues pièces, l'alignement s'est fait paragraphe par paragraphe.
- Chaque écart a été classé :
  - **bruit de l'OCR du scan** : mots collés (« délivreznous »), lettres mal lues (« bénio », « noire » pour « notre »),
    titres courants, colonne latine entremêlée ;
  - **écart réel** : à lire sur l'image de la page.
- Un écart a été vérifié sur l'image : *voulût* chez Gertrude, p. 206. Le scan imprime bien *voulût* ; le texte de l'app
  est juste.
- Scans utilisés : Paroissien 1890 (`/tmp/claude-0/par/p.txt`), Weber (`/tmp/claude-0/web/w.pdf`), *Thésaurisons*
  (`/tmp/claude-0/thes/t.pdf`), Sambucy (`/tmp/claude-0/sam/s.pdf`), Montfort, *Traité*, Gaume (`/tmp/claude-0/mtf/m.pdf`),
  méthode du Rosaire (`vendor/sources/montfort/methode.pdf`), Janvier (`vendor/sources/face/janvier.pdf`), Gertrude
  (`/tmp/claude-0/ger/g.pdf`), saint Alphonse, *Neuvaine au Sacré-Cœur* (`/tmp/claude-0/lig/sc.pdf`).
- Beringer 1925, le *Fervent chrétien* et le Recueil de neuvaines de 1886 ne sont pas disponibles en local ; ils n'ont
  pas été comparés.

### 4.2 Échantillon : 54 pièces comparées

Conformes, sans écart réel (seulement le bruit OCR du scan) :

- Paroissien 1890 (11) : `priere-du-matin`, `angelus` (français et latin), `priere-du-soir`, `de-profundis` (français
  et latin), `litanies-saint-nom`, `litanies-sainte-vierge`, `litanies-des-saints`, `acte-de-foi`, `acte-d-esperance`,
  `acte-de-charite`, `te-deum` (voir E5).
- Weber (26) : toutes les pièces `weber:*`, de `alma-redemptoris` à `trois-prieres-perpetuel-secours`. Pour
  `neuvaine-immaculee-conception`, les 21 paragraphes ont été pris un par un. Le latin des hymnes ne se compare pas
  automatiquement : le scan imprime le latin et le français en colonnes, et l'OCR les entremêle. Le français, lui, est
  conforme.
- Sambucy (1) : `chapelet-saint-dominique`.
- Montfort (3) : `preparation-consecration`, `petite-couronne`, `methode-rosaire` (52 paragraphes).
- *Thésaurisons* (3, plus la liste des 40 jaculatoires de `thesaurisons:jaculatoires-classees`) : `action-de-graces`,
  `au-christ-roi`, `sainte-face-therese`.
- Janvier (5) : `fleche-d-or`, `amende-honorable-sainte-face`, `consecration-sainte-face`, `promesses-sainte-face`,
  `petite-couronne-sainte-face` (voir E3).
- Gertrude (1) : `trois-ave-bonne-mort`.
- Saint Alphonse (1) : `liguori:neuvaine-sacre-coeur` (40 paragraphes).
- Livret (2) : `jardin:consecration-de-soi-meme-…` et `jardin:la-fleche-d-or`, comparées au *Traité* (Gaume) et à
  Janvier (voir E1 et E2).

### 4.3 Écarts relevés

| # | Pièce | Gravité | Constat | Correction proposée |
|---|---|---|---|---|
| E1 | `jardin:la-fleche-d-or` | à corriger | Le livret ajoute « au ciel, sur la terre **et dans les enfers** ». Janvier 1895, p. 181 (manuel revu d'après les décrets du Saint-Office, avec l'approbation de l'archevêque de Tours), dit seulement « au ciel, sur la terre, par toutes les créatures… ». La rubrique du livret dit aussi « dictée » ; Janvier dit « dicté » (l'acte). Source du livret : « Dévotion à la Sainte Face…, 1887 », sans page. | Garder la seule version `janvier:fleche-d-or` (S1). Si l'utilisateur tient à la forme longue, qui circule d'après les écrits de la sœur, la sourcer sur l'édition de 1887 avec sa page. |
| E2 | `jardin:consecration-de-soi-meme-a-jesus-christ-la-sagesse-incarnee-` | à vérifier | Comparé au *Traité*, éd. Gaume (`/tmp/claude-0/mtf/m.pdf`, p. 238-240) : « vrai Dieu et **vrai** homme » (Gaume : « vrai Dieu et homme ») ; « faites **à** mon Baptême » (Gaume : « **dans** mon baptême ») ; « par **ce** moyen » (Gaume : « par **son** moyen ») ; « je vous choisis aujourd'hui, **ô Marie**, en présence… » (Gaume : sans « ô Marie »). La rubrique de renouvellement (« tout ce qu'on a fait ») paraphrase Gaume (« ils ont »). Source du livret : le titre du *Traité*, sans édition. | Aligner sur Gaume, p. 238-240 (édition déjà utilisée pour `montfort:preparation-consecration`), et citer édition et page. |
| E3 | `janvier:petite-couronne-sainte-face` | à corriger (texte tronqué) | La rubrique omet la phrase de Janvier, p. 237 : « Les trente-trois petits grains représentent les trente-trois années de la vie mortelle de Notre-Seigneur. » Elle fond ensuite la suite en « Les trente premiers **petits grains**, qui rappellent… » ; Janvier dit « Les trente premiers qui rappellent… ». La phrase finale de Janvier sur la récitation quotidienne manque aussi. | Rétablir la rubrique mot pour mot (Janvier, p. 237-239) et incrémenter `revision`. |
| E4 | `jardin:les-sept-offrandes-du-precieux-sang` | à vérifier | Aucun texte correspondant n'a été trouvé dans *Thésaurisons*. | Voir D7. |
| E5 | `paroissien:te-deum` (latin) | à vérifier | Dans la colonne latine, l'alignement n'a pas retrouvé « extolle illos » ni le premier « æternum » de « usque in æternum » ; c'est sans doute une ligne perdue par l'OCR. | Lire le verset sur l'image (Paroissien 1890, p. 106-110). |
| E6 | Gloria Patri en français | suggestion | Trois formes coexistent. `hortus:cordon-sept-gloria` : « Gloire au Père… maintenant et toujours, comme dans le commencement et dans les siècles des siècles ». `montfort:methode-rosaire` : « comme elle était dès le commencement, maintenant et toujours, dans tous les siècles des siècles ». Paroissien : « comme il était au commencement… ». Dans l'arrangement du cordon, l'ordre « maintenant… comme dans le commencement » n'est celui d'aucune des sources citées. | Pour l'arrangement du cordon, prendre la forme de Beringer, t. II, n° 266, sa source déclarée (à lire sur le scan). |
| E7 | `beringer:*`, `fervent:*`, `neuvaines-1886:*` | à vérifier (non couvert) | Les scans ne sont pas disponibles en local ; ces pièces ne sont pas dans l'échantillon. | Télécharger Beringer (`archive.org/details/lesindulgences0001beri`) et le recueil de 1886 (`cihm_29753`), puis passer le même script (`cmp.py`, `para.py`, dans le dossier de travail de l'audit). |

---

## 5. Pertinence de la sélection

### 5.1 Doublons d'édition

| # | Pièces | Gravité | Correction proposée |
|---|---|---|---|
| S1 | `jardin:la-fleche-d-or` / `janvier:fleche-d-or` | à corriger | Garder Janvier (E1). La ligne « La Flèche d'or » (`liste:14`) doit pointer vers `janvier:fleche-d-or`. |
| S2 | `jardin:la-petite-couronne-de-la-tres-sainte-vierge` (éd. 1966) / `montfort:petite-couronne` (Gaume 1843) | à corriger | Garder Gaume (D4). |
| S3 | `beringer:coeur-afflige-de-marie` (Beringer 1925, n° 450) / `jardin:les-sept-douleurs-de-marie` (« Je m'afflige avec vous… », Beringer 1905, n° 138) / `beringer:don-*` (sept extraits) | à corriger | C'est le même exercice, en deux éditions de Beringer. Ses invocations sont en outre découpées en sept « dons ». Garder une seule forme : celle de 1925, avec la page vérifiée sur le scan. Le samedi, ne pas doubler (A9). |
| S4 | `beringer:litanies-sacre-coeur` (texte approuvé, 1899) / `breviaire-sc:litanies` (texte de 1883) | suggestion | Garder les deux : le bréviaire est un livre de lecture (§ 11). Seules les litanies de Beringer entrent dans la liste. C'est déjà indiqué dans l'usage de la pièce du bréviaire. |
| S5 | `jardin:les-treize-mardis-de-saint-antoine` (ordre 30) / `jardin:treize-mardis-de-saint-antoine` (ordre 51) ; `jardin:les-quinze-mardis-de-saint-dominique` (31) / `jardin:quinze-mardis-de-saint-dominique` (52) | suggestion | Ce sont deux fiches par dévotion (prières, puis pratique). Les fondre en une page par pratique (§ 11, principe 4). |
| S6 | `jardin:offrande-de-la-sainte-face` (promesses) / `janvier:promesses-sainte-face` | à corriger | Voir D6. |
| S7 | `paroissien:acte-de-foi/-d-esperance/-de-charite` / `paroissien:priere-du-matin` | conforme | Ce sont des extraits voulus (fiches d'indulgence séparées). Ils ne doivent pas entrer dans la liste du jour avec la prière du matin. |

### 5.2 Pièces de faible intérêt ou à revoir

| # | Pièce | Gravité | Constat |
|---|---|---|---|
| S8 | `jardin:priere-du-cardinal-mercier` | à corriger | Intention périmée (D10). |
| S9 | `jardin:priere-de-la-milice-angelique` | suggestion | Elle est réservée aux associés de la Milice angélique (cordon de saint Thomas). Si l'utilisateur n'est pas associé, la marquer facultative ou la retirer de l'offrande (Q6). |
| S10 | `jardin:offrandes-de-la-garde-d-honneur` | suggestion | Même remarque : elle suppose l'inscription à la Garde d'honneur et une « heure de garde ». |

### 5.3 Grandes prières traditionnelles absentes (pistes, avec une source ancienne proposée)

| # | Prière | Usage | Source proposée |
|---|---|---|---|
| P1 | Chemin de croix (saint Alphonse ou saint Léonard de Port-Maurice) | vendredis de Carême, Semaine sainte | Saint Alphonse, *Livre de prières et de méditations*, scan `/tmp/claude-0/lig2/lp.pdf` (chap. « Le Chemin de la Croix ») ; ou Janvier 1895. |
| P2 | *Miserere* (Ps 50) | Carême, vendredis | Paroissien romain, 1890 (latin et français). |
| P3 | *Adoro te devote*, *Lauda Sion* | jeudi, Fête-Dieu | Paroissien romain, 1890 ; Ench. 1952, n° 166 et 167 pour le latin. |
| P4 | *Ad te, beate Ioseph* (Léon XIII) | octobre, après le chapelet ; mercredi | Ench. 1952, n° 476 ; traduction de Beringer 1925. |
| P5 | Consécration de la famille à la Sainte Famille | février | Ench. 1952 (*Consecratio sacrae Familiae*) ; traduction ancienne à trouver. |
| P6 | Acte de consécration du genre humain au Sacré-Cœur (*Iesu dulcissime, Redemptor*) | Christ-Roi, juin | Ench. 1952 ; traduction ancienne. |
| P7 | Séquence *Veni, Sancte Spiritus* | Pentecôte, neuvaine | Paroissien romain, 1890. |
| P8 | Prières « au son de l'heure », bénédicité et grâces des repas | chaque jour | Paroissien romain, 1890 (prières du chrétien), à vérifier. Elles s'insèrent dans la journée sans être des tâches (§ 11, principe 2). |
| P9 | Prières de sainte Gertrude avec promesse (décision du § 11) | selon la catégorie | Denis, *Prières de sainte Gertrude*, 11e éd. (`/tmp/claude-0/ger/g.pdf`), en cours. |
| P10 | « Ô mon Jésus, pardonnez-nous… », « Ô Marie conçue sans péché… » en fin de dizaine (§ 11) | chapelet | Pour la médaille miraculeuse : Weber 1890 (Notre-Dame de la médaille miraculeuse, à chercher dans `/tmp/claude-0/web/w.pdf`) ; pour la prière de Fatima, La Porte Latine (FSSPX). |

Piste d'intégration (SPEC § 10, dévotions combinées) : l'Ench. 1952, n° 285, indulgencie la récitation de sept *Gloria
Patri* pour obtenir les sept dons du Saint-Esprit. On pourrait remplacer la ligne « Demande du don » par cette forme
ancienne. Mais deux pratiques de sept Gloria (le cordon et les dons) ne peuvent pas se fondre en une seule récitation :
le droit de 1917 exclut, en principe, qu'une même œuvre gagne plusieurs indulgences (CIC 1917, can. 933, à vérifier sur
le texte). Question pour la session principale, qui tient les indulgences.

---

## Questions qui demandent un arbitrage de l'utilisateur

- **Q1. Antienne mariale du temps.**
  - Faut-il remplacer le Salve Regina (matin) ou le Sub tuum (soir) par l'antienne du temps : Alma de l'Avent à la
    Purification, Ave Regina jusqu'au Jeudi saint, Regina cæli au temps pascal, Salve ensuite ?
  - Ou ajouter l'antienne du temps à la fin de la prière du soir, en gardant les deux ?
  - Au temps pascal, le Regina cæli remplace déjà l'Angélus : faut-il éviter de le dire deux fois ?
- **Q2. Actes du livret sans source** (offrande du matin, devoirs de charité, triple couronne) :
  - les garder comme vos propres compositions, marquées « composé pour le livret » ;
  - ou les remplacer par des formules anciennes sourcées (D1, D2, D5) ?
  - Faut-il garder les intentions particulières (« retour d'un saint pape », etc.) ?
- **Q3. Heure sainte** : chaque jeudi ou seulement la veille du premier vendredi ?
- **Q4. Ordre du matin** : faut-il une offrande brève au lever, avant la prière du matin, ou bien la prière du matin
  d'abord, puis les actes ?
- **Q5. Sources hors de la liste admise** (salve-regina.com, *Le Petit Sacristain*, christusregnat.com, *La Bonne
  Nouvelle*) : les garder en attendant une source ancienne, ou retirer les pièces ?
- **Q6. Pièces réservées à des associés** (Milice angélique, Garde d'honneur, chapelet des Morts, cordon de saint
  Joseph) : êtes-vous inscrit à ces confréries ? Sinon, faut-il les marquer facultatives ?
- **Q7. Flèche d'or** : la forme de Janvier 1895, sans « et dans les enfers », ou la forme longue du livret ?

---

## Annexe A. Indulgences : constats transmis à la session principale (non poursuivis)

Ces écarts ont été relevés dans `/tmp/claude-0/ench/e.txt` (Ench. 1952) avant la consigne de ne pas vérifier les
indulgences. Le relevé est partiel. À noter : l'index `/tmp/claude-0/ench/idx.json` contient des numéros mal lus par
l'OCR. Par exemple, le n° 473 y est lu « 478 » et le n° 253 « 293 » ; il faut contrôler la table des matières
(lignes 31000 et suivantes).

- **`beringer:saint-joseph-purete`** : fiche « n° 478 ». Le texte *Virginum Custos et Pater* est le **n° 473** ; le
  n° 478 est « Glorieux saint Joseph, modèle… ».
- **`jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph`** : « n° 410 », mais le n° 410 est la prière à
  Notre-Dame du Cénacle. L'exercice *O Sposo purissimo* est le **n° 470**. Les sept dimanches sont au n° 465, le
  premier mercredi au n° 468 (le livret cite la *Raccolta* 1943).
- **`jardin:dix-dimanches-de-saint-ignace`** : « n° 407 » (prière à Notre-Dame de la Piété). Les dix dimanches de saint
  Ignace sont au **n° 497**.
- **`jardin:chapelet-de-saint-michel-archange`** : la fiche cite Pie IX, 1851 (*Raccolta*). Le chapelet n'est pas dans
  l'Ench. 1952 (n° 441-447 : invocations, neuvaine, prières). Or le décret de promulgation déclare abrogées les
  concessions générales absentes du recueil (« obrogatis ceteris omnibus… quae in hoc enchiridion non sint relatae » ;
  *Praenotanda*, 2).
- **`beringer:coeur-afflige-de-marie`** : la fiche le dit elle-même, la pièce n'est pas dans l'Ench. 1952. Même règle.
- **`thesaurisons:sainte-face-therese`** : la prière est dans l'Ench. 1952, **n° 208**.
- **`thesaurisons:jac-37`** (« Vous êtes le Christ… ») : selon l'Ench. 1952, l'indulgence n'est accordée que
  « coram Ssmo Eucharistiae Sacramento ».

## Annexe B. Outils de l'audit (hors dépôt)

- Script d'alignement : `/tmp/claude-0/-home-user-hortus-sacrum/8ba3c60b-b215-5710-af7f-a44fba5ce285/scratchpad/cmp.py`.
  Usage : `cmp.py <sources.json> <préfixes…>`, avec `F=latin` pour comparer le latin.
- Comparaison par paragraphe : `para.py`, même dossier.
- Pièces du livret : `jcmp.py <jardin.json> id=source…`, même dossier.
- Couches texte des scans : `*.txt`, même dossier.
