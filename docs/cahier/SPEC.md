# Spécification fonctionnelle

## 1. Écrans

1. **Aujourd’hui** (écran d’accueil), de haut en bas :
   - **Bandeau liturgique** :
     - date ; temps liturgique ; office du jour avec son rang ;
     - pastille de couleur ;
     - commémoraisons ;
     - Introït (incipit, et texte complet latin et français dépliable, d’après le Missel) ;
     - station romaine s’il y en a une ;
     - jeûne et abstinence en rouge.
   - **« Vie du saint »** dépliable, pour le ou les saints du jour :
     - niveau 1 : la notice du Martyrologe romain ;
     - niveau 2 : les leçons historiques du Bréviaire (leçons IV à VI du 2e nocturne, en français et en latin, dans Divinum Officium : fichiers `horas/Francais/Sancti/MM-DD.txt`, sections `[Lectio4]` à `[Lectio6]`) ;
     - niveau 3 : la notice de Guéranger, *L’Année liturgique*, si elle a été extraite.
   - **Méditation du jour** (voir §6), avec la pratique et la résolution quand le recueil en donne une.
   - **Liste à cocher du jour** (voir §4). Chaque ligne ouvre la prière correspondante.
   - **Micro-martyrologe** (voir §5).
2. **Calendrier** : vue mois et vue semaine.
   - Mêmes informations que le calendrier papier.
   - Filtres : fêtes, jeûnes, dévotions, neuvaines, saints favoris, anniversaires spirituels.
3. **Prières** : la bibliothèque complète.
   - Toutes les prières du *Jardin de l’âme*, puis celles ajoutées (par l’utilisateur ou proposées et validées).
   - Recherche ; classement par partie ; favoris.
   - Chaque prière affiche : français ; latin dépliable ; « usage » ; indulgence (Ench. 1952) ; source.
4. **Mes dévotions** : les suivis en cours et à venir (§3).
5. **Profil spirituel** :
   - dates de baptême, confirmation, première communion, consécrations (Montfort, Sacré-Cœur…), fête patronale ;
   - saints favoris, pour lesquels un rappel est envoyé la veille de leur fête ;
   - heures des rappels ;
   - choix des recueils de méditation.
6. **Historique** : jours cochés, régularité, et séries comme « 5 / 9 premiers vendredis ».

## 2. Calendrier liturgique

- Données 2026-2027 déjà calculées : `donnees/calendrier_2026-2027.json` (364 jours, du 29 novembre 2026 au 27 novembre 2027).
- Le moteur (`moteur/engine.py`, `build.py`) s’appuie sur les **données** du projet Divinum Officium (GitHub `DivinumOfficium/divinum-officium`) :
  - `web/www/Tabulae/Kalendaria` (1570 → 1888 → 1906 → 1939 → 1954) ;
  - `Tabulae/Transfer` ;
  - les rangs numériques `[Rank]`.
- Il est **à étendre aux autres années** et à valider jour par jour contre un ordo de 1954 imprimé si on en trouve un (voir `SOURCES.md`).
- Le jeûne et l’abstinence sont calculés dans `moteur/devo.py` (CIC 1917).
- Les stations sont dans `moteur/stations.py`, recopiées du *Missale Romanum* typique de 1920.

## 3. Suivis de dévotions (cœur de l’app)

Types d’objets :

| Type | Exemples | Comportement |
|---|---|---|
| Série à jours comptés | 7 dimanches de S. Joseph, 13 mardis de S. Antoine, 9 premiers vendredis, 5 premiers samedis, 15 samedis du Rosaire… | Jours fixés par la règle (« les 7 dim. avant le 19 mars » ou « n consécutifs à partir de… »). Compteur n/N. Alerte si un jour est manqué (« série interrompue : recommencer ? »). Prière du jour liée. |
| Neuvaine | Neuvaines préparatoires aux fêtes ; neuvaine libre | 9 jours, prière du jour (prière fixe ou propre à chaque jour) |
| Trentain de prières | 30 jours à une intention | Compteur 1/30, intention notée, rappel quotidien |
| Préparation et consécration | Montfort : 33 jours (12 + 3 × 7), puis renouvellement | Phase du jour affichée, avec ses prières propres selon le *Traité de la vraie dévotion* (n° 227-233) ; rappel de l’anniversaire |
| Mois | Mois du saint Nom de Jésus, de S. Joseph, de Marie, du Sacré-Cœur, du Précieux Sang, du Cœur Immaculé, des Sept Douleurs, du Rosaire, des fidèles trépassés, de l’Immaculée Conception | Pieux exercice indulgencié (Ench. 1952, n° 118, 466, 325, 253, 217, 389, 381, 398, 589, 364), avec la méditation du recueil de mois si on en a un |
| Vigile, jeûne | Vigiles, Quatre-Temps, Carême | Rappel la veille |

Règles :

- **Enchaînement sans chevauchement** : le planificateur propose les séries de façon qu’une seule série occupe un même jour de la semaine à la fois, comme dans le calendrier papier. Seuls les premiers vendredis et samedis peuvent coïncider avec une autre série.
- Rappels canoniques à afficher dans les explications :
  - l’indulgence plénière ne se gagne qu’**une fois par jour** (CIC 1917, can. 928 §1) ;
  - une même confession et une même communion valent pour plusieurs indulgences (can. 933).
- Le plan 2026-2027 déjà choisi est dans le JSON (champ `devotions`) et dans la page « Les dévotions de l’année » du calendrier papier. Il doit être éditable.

## 4. Proposition de nouvelle structure de la liste quotidienne

À montrer à l’utilisateur et à faire valider avant de coder. Elle part de son modèle Notion, mais elle est ordonnée selon le déroulement de la journée et remplie automatiquement pour la partie « Propre ».

**Matin**
- Offrande du matin et intention d’indulgences (*Jardin*, p. 1)
- Prière du matin, avec Ave Maria de la mort et Salve Regina
- Intentions particulières du jour (champ libre)
- Consécration personnelle (renouvellement court)

**Propre du jour** (rempli automatiquement)
- Office du jour : lire la notice ou la vie du saint (dépliable)
- Méditation du jour
- Dévotion du jour de la semaine, d’après les dédicaces : lundi, les âmes du purgatoire ; mardi, les Anges ; etc.
- Dévotion à jours comptés en cours, s’il y en a une (avec n/N)
- Neuvaine ou trentain en cours, s’il y en a un
- Dévotion du mois
- Jeûne ou abstinence, s’il y a lieu (rappel, sans case à cocher)

**Au fil du jour**
- Angélus (6 h, midi, 18 h ; Regina Cæli au temps pascal)
- Chapelet
- Une **couronne selon le jour**, au lieu des trois chaque jour. À proposer à l’utilisateur :
  - lundi : couronne des 50 Requiem ;
  - mardi : couronne angélique ;
  - vendredi : couronne du Sacré-Cœur ;
  - les autres jours, au choix.
- 15 oraisons de sainte Brigitte (compteur sur l’année, sans les promesses)
- Vendredi à 15 h : devant le Crucifix (*Jardin*, p. 71)

**Soir**
- Examen de conscience
- Prière du soir, avec Ave Maria de la mort et Sub tuum præsidium
- Litanies du jour
- Demande des dons du Saint-Esprit

**Martyrologe** : invocations (voir §5)

Chaque élément peut être activé ou désactivé, déplacé, et réglé par jour de la semaine. Les éléments cochés sont horodatés.

**Textes absents du livret, à sourcer ou à demander à l’utilisateur** : « Ave Maria de la mort », prière du matin et du soir, couronne du Sacré-Cœur, couronne angélique, couronne des 50 Requiem, demande des dons du Saint-Esprit, examen de conscience. Les chercher d’abord dans la Raccolta de 1943 et l’Enchiridion de 1952 ; sinon, demander à l’utilisateur sa version.

## 5. Micro-martyrologe et invocations

- Source : *Martyrologe romain*, traduction française dans Divinum Officium (`horas/Francais/Martyrologium/MM-DD.txt` ; latin dans `horas/Latin/Martyrologium/`). Déjà extrait pour 2026-2027 dans le champ `martyrologe` du JSON : une entrée par saint.
- **Tradition à respecter** : au chœur, le martyrologe se lit **la veille**, à Prime (on annonce les saints du lendemain). Prévoir deux vues :
  - « les saints d’aujourd’hui » ;
  - « lecture de Prime » : celle du lendemain, avec la phrase de l’« annonce de la lune », si on la trouve dans les sources DO.
- **Invocations** : pour chaque saint ou groupe de saints de l’entrée, une ligne d’invocation à toucher. Exemples : « Saint Théophane et vos compagnons, priez pour nous. », « Sainte Barbe, priez pour nous. »
  - L’invocation est **générée** à partir du nom, à la deuxième personne du pluriel (vouvoiement).
  - L’adapter au singulier ou au pluriel et au genre.
  - Pour les bienheureux : « Bienheureux N., priez pour nous ».
  - Afficher en dessous le texte de l’éloge (dépliable).
- Bouton « invoquer tous les saints du jour » : liste des invocations à la suite, terminée par « Tous les saints et saintes de Dieu, intercédez pour nous. » (formule des Litanies des saints).

## 6. Méditations : sources et attribution

**But** : une méditation par jour, choisie dans le recueil **le plus pertinent pour ce jour**. Règle de priorité, à affiner avec l’utilisateur :

1. Une neuvaine ou un mois en cours qui a son propre recueil de méditations. Exemples :
   - mars : un *Mois de saint Joseph* ;
   - mai : un *Mois de Marie* ;
   - juin : un *Mois du Sacré-Cœur* ;
   - novembre : un *Mois des âmes du purgatoire* ;
   - certains donnent une pratique par jour.
2. Une fête de 1re ou 2e classe : Guéranger, *L’Année liturgique*, pour la fête.
3. Un temps fort (Avent, Septuagésime, Carême, Passion, temps pascal) : Guéranger pour le jour, ou un recueil de méditations quotidiennes ancien.
4. Sinon : un recueil de méditations quotidiennes ancien, pour le temps après la Pentecôte ou après l’Épiphanie.

**Sources** :
- Pistes déjà repérées : voir `SOURCES.md`.
- Tout recueil doit être **antérieur à 1955** et du domaine public.
- Stocker le texte découpé par jour, avec l’édition et la page.
- OCR : relire et corriger les coquilles évidentes sans changer le texte.

**Le Petit Sacristain** (le-petit-sacristain.blogspot.com) : blog cité par **lien** seulement. Ses articles récents sont surtout des prières et des témoignages. Ne pas recopier ses textes ; proposer un lien « à lire aussi » quand un article correspond au jour.

## 7. Rappels (notifications)

- **Matin** (heure réglable) : « Aujourd’hui : [office] — [jeûne] — [n/N série] — [neuvaine j/9] ».
- **Soir** (heure réglable) : « Prière du soir — reste à faire : … ».
- **Veille** :
  - des fêtes de 1re et 2e classe et des fêtes des saints favoris ;
  - du début d’une neuvaine ou d’une série ;
  - des jours de jeûne ;
  - des premiers vendredis et samedis.
- **Anniversaires spirituels** : la veille et le jour même.
- **Heures fixes par dévotion** : Angélus ; 15 h le vendredi ; heure de garde (Garde d’honneur) ; prière pour les agonisants trois fois par jour.
- Tout est désactivable un par un.

## 8. Modèle de données (indicatif)

- `jour_liturgique` : date, office, rang, couleur, commémoraisons, introït, station, jeûne, références DO.
- `martyrologe_entree` : date, clé, texte FR, texte LA, invocation.
- `priere` : id, titre, partie, texte FR, texte LA, usage, indulgence, référence Ench., source, ajoutée_par.
- `meditation` : recueil, jour ou clé, titre, texte, pratique, source.
- `serie` (dévotion suivie) : type, règle, dates, priere_id, compteur, état.
- `liste_modele` : éléments, ordre, jours actifs ; `coche` : date, élément, horodatage, utilisateur.
- `profil` : anniversaires, saints favoris, heures des rappels, abonnements push.

## 9. Tout est modifiable par l'utilisateur (ajout du 12 novembre 2026, prioritaire)

L'utilisateur peut ajouter, retirer ou modifier à la main à peu près tout, dans l'app.

**Objets modifiables**
- **Prières et textes** : créer, modifier, supprimer, dupliquer. Champs : texte français, latin en option, usage, indulgence, source (ouvrage, édition, page), partie, catégorie.
- **Pratiques et dévotions** (jours comptés, neuvaines, trentains, consécrations, dévotions du mois et du jour de la semaine) : règle de dates (« les N jours avant telle fête », « N mardis consécutifs à partir de… », jour fixe), prières liées, promesses, indulgence, source.
- **Liste quotidienne** : ajouter, retirer, réordonner par glisser-déposer, jours de la semaine, heure de rappel de chaque élément.
- **Méditations et recueils** : ajouter un recueil, le découper par jours, l'affecter à un mois, un temps liturgique, une fête ou une neuvaine.
- **Calendrier** : fêtes et saints personnels, anniversaires spirituels, notes sur un jour.

**Trois façons de saisir, pour tout**
1. **Clavier** : éditeur simple, boutons ℣, ℟, rouge (rubrique), italique ; colonne latine en option.
2. **Copier-coller** : nettoyage automatique (sauts de ligne parasites, mots coupés en fin de ligne, espaces doubles, ℣ et ℟ reconnus), aperçu à corriger avant d'enregistrer.
3. **PDF ou photo** : choix du fichier et d'une plage de pages ; extraction (pdf.js) ; OCR dans le navigateur si le PDF est scanné ou s'il s'agit d'une photo (Tesseract.js, français et latin) ; découpage et correction dans l'aperçu ; enregistrement en une ou plusieurs pièces, source pré-remplie (titre du PDF et page).

**Garde-fous**
- Origine de chaque élément, affichée par un badge : « Livret », « Source officielle vérifiée », « Ajout personnel ».
- Les éléments d'origine restent modifiables, avec « Restaurer l'original ».
- Historique des versions de chaque texte ; suppression en deux temps (corbeille, restauration possible).
- Export et import complets en JSON ; export PDF d'une sélection de prières.
- Les règles sur les sources s'appliquent à ce que l'assistant ajoute. Les ajouts de l'utilisateur ne sont pas bloqués : ils sont marqués « Ajout personnel ».

**Décisions liées** : pas de propre de France (calendrier romain universel ; fêtes personnelles ajoutées dans l'app) ; « Ave Maria de la mort » retiré ; chapelet des Morts (Pie IX, 1873) à la place des 50 Requiem ; prières du matin et du soir du *Paroissien romain* (Tours, Mame, 1890).

## 10. Critique du 17 novembre 2026 et réponses (prioritaire)

Règle commune : « faire le plus de dévotion avec le moins d'actes séparés, pour garder du temps pour le devoir d'état ».

### Améliorations
1. **Martyrologe chanté** : pour **chaque** saint ou groupe nommé au Martyrologe du jour, une invocation latine
   chantable tirée du Martyrologe romain latin (nom, qualité, lieu), terminée par « ora pro nobis » :
   ex. « Sancta Barbara, virgo Nicomediae, ora pro nobis peccatoribus. Amen. »
2. **Dévotions combinées** : **fusion dans la ligne**. Quand deux dévotions peuvent se dire en un seul acte, la
   ligne contient directement la forme combinée et les deux sont cochées ensemble (réglable dans « Régler la liste »).
   Ex. : les 3 Ave de l'introduction du chapelet remplacés par les 3 Ave révélés à sainte Gertrude (un pour chaque
   Personne de la Trinité, pour une bonne mort). Chercher d'autres combinaisons du même genre.
3. **Rosaire, méthode de saint Louis-Marie de Montfort** sur la page du chapelet ; clausules **toutes de Montfort**
   (*Le Secret admirable du très saint Rosaire*, méthodes de réciter), 2 par mystère (30), latin et français.
4. **Angélus → Regina cæli au temps pascal** : déjà en place (`remplacementsDuTemps`, Beringer 1925 n° 428).
5. **Cordon de saint Joseph** : avant chacun des 7 Gloria, une invocation des **Litanies de saint Joseph**
   (Joseph très chaste, très prudent, très obéissant, très fidèle, miroir de patience, amant de la pauvreté,
   modèle des travailleurs), latin et français.
6. **Sub tuum** : avant les versets, les invocations « Domina nostra, mediatrix nostra, advocata nostra, tuo Filio
   nos reconcilia, tuo Filio nos commenda, tuo Filio nos repræsenta », latin et français (source ancienne à citer).

### Corrections
1. **Méditations** : relire sur le scan **tous** les recueils, dans l'ordre où ils s'affichent (Mois des âmes,
   Hamon, Chaignon, Guéranger, Visites).
2. **Indulgences** : une invocation indulgenciée répétée dans une prière compte autant de fois qu'elle est dite.
3. **Dévotions « terminées » sans avoir été commencées** : les dévotions du plan dont la date est passée ne doivent
   pas s'afficher « terminées » (dire « passée » ou « manquée » selon qu'elle a été commencée ou non).
4. **Triple Couronne d'or** : la ligne du jour doit montrer l'invocation propre et les mystères de la couronne du
   jour (1re lun. mer. sam. ; 2e mar. ven. ; 3e jeu. dim.).

### Ajouts
1. **Petit bréviaire du Sacré-Cœur de Jésus** (petits offices pour chaque jour de la semaine et exercice pendant la
   messe, tirés de sainte Marguerite-Marie ; Nancy, Le Chevallier, 13e éd., imprimatur 21 mars 1883 ; PDF fourni).
   *Fait :* les sept offices (`breviaire-sc:office-<jour>`, extraits par `engine/recueils/breviaire_sc/extraire.py`,
   relus) ; ligne « Petit bréviaire du Sacré-Cœur » qui donne l'office du jour de la semaine
   (`hortus:petit-breviaire-du-jour`). La Recommandation du dimanche, à laquelle les autres jours renvoient, est recopiée
   dans chacun. Reste : l'exercice pendant la messe, les litanies, la neuvaine.
2. **Prières et promesses de sainte Gertrude** : PDF reçu (Denis, *Prières de sainte Gertrude*, 11e éd., Lethielleux).
   *Fait :* les trois Ave de sainte Mechtilde pour une bonne mort (p. 206-208), joints à la ligne du chapelet, où ils
   tiennent lieu des trois Ave du début (`gertrude:trois-ave-bonne-mort`).
3. **Jaculatoires indulgenciées** : un recueil classé par rapport indulgence / longueur (Ench. 1952) **et** une
   ligne du jour avec les 10 meilleures, qui tournent ; chacune compte dans le total.
4. **Apostolat de la prière** : offrande quotidienne et pratiques (P. Ramière / Gautrelet, XIXe s.), sans les
   intentions mensuelles récentes.
5. **Sainte Face** : compléter d'après le Manuel de l'Archiconfrérie (Janvier, Tours 1895, PDF fourni).
6. **Scapulaire de bénédiction et de protection** (Marie-Julie Jahenny, extase du 23 août 1878, d'après *La Bonne
   Nouvelle*) : port du scapulaire ; 5 ou 7 *Crux ave* ; 1 à 3 minutes de méditation de la Passion ; les trois
   salutations à Jésus crucifié ; intentions (texte fourni par l'utilisateur le 17 nov.).
7. **Durée** : chaque prière a une durée **estimée d'après la longueur du texte** (récitation vocale), méditation et
   chapelet à durée fixe, toutes **modifiables à la main** ; total du jour en tête de liste.

### Cadre pratique : étiquettes et bilan du jour
Chaque prière reçoit des étiquettes ; l'écran du jour montre un **bilan** (ce qui est couvert, ce qui manque) et
propose une prière pour combler un manque. Le calendrier quotidien ne fait qu'instancier ces catégories.
- **Fins** : adoration, action de grâces, réparation, demande, intercession.
- **Objets** : Dieu / Trinité, Jésus-Christ, Eucharistie, Sacré-Cœur, sainte Vierge, Cœur immaculé, saint Joseph,
  anges, saints, âmes du purgatoire, sainte Face, etc.
- **Grâces à demander** : salut, persévérance finale, sanctification, charité, vertus, préservation du péché,
  protection physique et santé, vocation / devoir d'état, grâces temporelles.
- **Personnes** : soi-même, famille, amis, ennemis, pécheurs, Église et prêtres, dirigeants, mourants, âmes du
  purgatoire.
- **Pratiques** : messe, office, oraison, méditation, chapelet, examen, lecture spirituelle, dévotions, pénitence,
  actes jaculatoires.

*Fait :* `app/src/lib/etiquettes.ts`. Les étiquettes sont déduites du titre et du texte par mots-clés ; elles se corrigent
par des cases à cocher dans la fiche de la prière, et celles de l’utilisateur remplacent alors les étiquettes déduites. Le
bilan du jour, sur l’écran du jour, montre pour chaque catégorie ce qui est couvert et ce qui manque, avec la prière la plus
courte de la bibliothèque qui comble chaque manque.

### Corrections du 17 novembre au soir (prioritaire)

1. **Une page par prière composée.** Quand une ligne réunit plusieurs textes, on les présente en **une seule page**, celle
   du jour. Ces pages sont composées par `engine/composer/composer.py`, à partir des textes sourcés, sans rien réécrire :
   - **Triple Couronne d’or** : trois pages (`hortus:triple-couronne-1/2/3`). Chacune contient l’ordinaire, l’invocation
     propre à sa place et les mystères avant les prières finales. Seule la couronne du jour s’affiche : 1re le lundi, le
     mercredi et le samedi ; 2e le mardi et le vendredi ; 3e le jeudi et le dimanche.
   - **Offrande du matin** : les actes du livret en une page (`hortus:offrande-du-matin`). Rien n’y répète la prière du
     matin.
   - **Chapelet** : une page par série de mystères (`hortus:chapelet-joyeux/douloureux/glorieux`). Chaque page contient
     la manière de saint Dominique, la méthode de saint Louis-Marie de Montfort et les trois Ave de sainte Mechtilde, avec
     des boutons vers les autres mystères pour dire le rosaire entier. Le chapelet du jour : joyeux le lundi et le jeudi ;
     douloureux le mardi et le vendredi ; glorieux le mercredi, le samedi et le dimanche. Plus de roue des chapelets.
   - Mécanisme : identifiants « du jour » (`SELON_LE_JOUR`, `app/src/lib/liste.ts`).
2. **Invocations latines chantées : sans le lieu**, qui casse le rythme. Seule exception, l’invocation connue par un chant :
   « Sancta Barbara, virgo Nicomediæ, ora pro nobis peccatoribus, amen ».
3. **Après chaque lot : lint et nettoyage** (code mort, migrations devenues inutiles), **puis audit des consignes**
   (sources bannies, secrets, textes sans source, textes de mémoire). Ce qui sort des consignes est corrigé sans attendre.
4. **Reprendre ce qui a été laissé en pause.** Avant de conclure, relire l’historique et la liste des tâches.

## 11. Refonte du 18 novembre 2026 (prioritaire, décisions de l'utilisateur)

L'utilisateur est le bêta-testeur de son app. **Chaque exemple qu'il signale illustre un principe** : on corrige
l'exemple, puis toutes les autres occurrences du même problème, et l'on cherche la cause de fond. On ne préserve pas
l'architecture si elle est mauvaise.

### Principes
1. **Une prière n'apparaît qu'une fois par jour.** La liste du jour est calculée à partir d'un **programme unique**. Chaque
   pratique y est déclarée une seule fois, rattachée à son jour, sa semaine, son mois ou son temps. Un test échoue dès
   qu'un texte paraît deux fois dans une journée, y compris à l'intérieur d'une page composée.
2. **Intégrer plutôt qu'ajouter.** Une prière, une invocation ou une petite pratique qui peut se glisser naturellement dans
   une autre séquence y est insérée, au lieu de devenir une tâche. Les séquences hôtes ont des **points d'insertion** :
   - fin de dizaine du chapelet ;
   - Angélus ;
   - prière du matin et prière du soir ;
   - fin de l'office du saint.

   Les pages explicatives des dévotions restent consultables (onglet Dévotions), sans encombrer la liste.
   - Exemple : à chaque fin de dizaine, « Ô mon Jésus, pardonnez-nous… », « Ô Marie conçue sans péché… » (médaille
     miraculeuse) et « Cœur immaculé de Marie… » (scapulaire vert), d'après des sources admises.
   - Exemple : les invocations du scapulaire de Marie-Julie Jahenny sont réparties entre la prière du matin et la prière
     du soir ; la ligne propre disparaît.
   - Exemple : les oraisons de sainte Brigitte tiennent lieu de méditation de la Passion ; pas de tâche de méditation en
     plus.
3. **Ce qui se lit sort de la liste du jour.** Un onglet **Lecture** comprend quatre sections :
   - **Office** : les bréviaires ;
   - **Écriture** : l'Évangile ;
   - **Doctrine** : la Somme théologique ;
   - **Spirituel** : méditations, vie et office du saint, lectures.

   Dans Aujourd'hui, une seule **ligne récapitulative** (« Lectures du jour (2/4) ») ouvre Lecture et compte dans
   l'avancement.
4. **Une page par pratique, en sections dépliables.** Les heures canoniales d'un office s'ouvrent chacune par un bouton ;
   elles ne sont pas affichées toutes à la suite.
5. **Écran du jour sobre.** Les jauges (jardin du jour, temps de prière, indulgences) et le bilan se dévoilent par un
   bouton. Une **jaculatoire indulgenciée** différente s'affiche à chaque ouverture ; la toucher la compte comme dite,
   indulgences comprises. Les jaculatoires ne sont plus une tâche.

### Décisions
- **Navigation.** Cinq onglets en bas : Aujourd'hui, Lecture, Prières, Dévotions, Calendrier. Le Profil devient une icône
  en haut à droite.
- **Bréviaires** dans Lecture › Office :
  - le Petit bréviaire du Sacré-Cœur ;
  - le **Bréviaire romain, heures complètes, rubriques d'avant 1955** (saint Pie X, *Divino afflatu*), d'après Divinum
    Officium, qui compile les éditions typiques ;
  - l'**Officium parvum** de la sainte Vierge, à chercher d'abord dans Divinum Officium, sinon dans une édition
    latin-français ancienne, avec les variantes des temps.
- **Somme théologique** : un article par jour, **traduction Lachat (1856), latin en regard**, à la suite depuis la Iª
  pars, q. 1, a. 1.
- **Mercredi** : une seule page réunit le renouvellement de la consécration au cordon de saint Joseph et les sept Gloria.
  **Les autres jours** : une seule page pour les Gloria.
- **Sainte Gertrude** :
  - on transcrit toutes ses prières avec promesse de Notre-Seigneur ou de la sainte Vierge qui sont pertinentes : pour
    les morts, culte des saints, Passion, sainte Vierge, Trinité, Notre-Seigneur ; de même pour celles de sainte
    Mechtilde ;
  - à la fin de l'office du saint du jour, on ajoute la prière de sainte Gertrude propre à sa catégorie (vierge, vierge et
    martyre, confesseur…), avec le nom du saint à la place du « N. ».
- **Refonte de la liste** : la liste actuelle est **remplacée** par le programme. On garde les ajouts personnels, les
  durées et les rappels ; l'ancienne liste reste dans l'historique des versions.
- **Filtres** par thème et par type sur les prières, et sur les autres contenus quand c'est utile.
- **Décor** :
  - les bandeaux respectent la zone sûre de l'iPhone (encoche) dans les deux directions artistiques ;
  - la direction **latine** reçoit son propre bandeau ;
  - l'arche du saint du jour reçoit des ornements.
- **Bug** : « Internal Error » à chaque passage du Profil à l'Historique sur le téléphone de l'utilisateur. Il n'est pas
  reproduit sur une base neuve, donc il dépend sans doute des données. À corriger : rendre l'Historique tolérant aux
  données incomplètes, et ajouter une page d'erreur qui affiche le message réel.
- **Sub tuum** : la traduction française des invocations n'a pas de source. On garde le latin seul.

### Méthode de travail
Les agents spécialisés sont mobilisés :
- audit des dévotions et de leur organisation ;
- audit du corpus de prières (pertinence selon le jour, la semaine, le mois et l'année ; tradition ; agencement ;
  exactitude ; sélection) ;
- ingénieur-concepteur (ergonomie, intuitivité, tests).

Après chaque implémentation :
- lint et formatage ;
- tests ;
- relecture des fichiers modifiés et revue critique du code ;
- corrections, puis nouvelle vérification.

### Indulgences (décision du 19 novembre 2026, prioritaire)
- **Seules comptent les œuvres de l'Enchiridion indulgentiarum de 1952.** Le décret de la S. Pénitencerie du 3 mars 1952
  abroge toutes les concessions générales qu'il ne reprend pas (« obrogatis ceteris omnibus generalibus indulgentiarum
  concessionibus, quae in hoc enchiridion non sint relatae »). Les œuvres qu'il reprend avec changement suivent la forme
  de 1952 (Praenotanda 2). Les indulgences des confréries, des objets bénits et des lieux ne sont pas « générales »
  (Praenotanda 1) : elles sont signalées, sans être comptées.
- **Traductions** (Praenotanda 3 ; can. 934 § 2) : une prière concédée en latin ou en italien ne porte l'indulgence en
  français que si sa traduction est déclarée fidèle par la S. Pénitencerie ou par un Ordinaire du lieu.
  - *Thésaurisons pour le ciel* (Montréal, 1941) est certifié (G. Chartier, vicaire général, 28 avril 1941).
  - Aucune traduction française officielle de l'Enchiridion de 1952 n'a été trouvée ; celle de 1969 (Lethielleux)
    concerne le nouvel Enchiridion.
  - Chaque fiche porte `langue` et `traduction` ; sans traduction approuvée, l'app affiche la note du can. 934.
- Vérification des 100 fiches sur le texte de 1952 (agent Indulgences, 20 nov.) : seul le chapelet de saint Michel est
  abrogé. Trois concessions d'abord déclarées abrogées à tort ont été rétablies (n° 234, 199 et 383). Les textes
  français ont été remplacés, quand c'était possible, par ceux de Thésaurisons (`revision`). Les traductions qui restent
  à trouver sont dans `A_FOURNIR.md`.
- Données : `data/prieres/indulgences.json` ; scripts `engine/indulgences/ench1952.py`, `verif1952.py`, `beringer1925.py`, puis `thesaurisons_livret.py`. Un test vérifie que chaque fiche
  comptée cite l'Enchiridion de 1952. Les mentions d'indulgence recopiées des anciens manuels ne sont pas affichées.
- **Décision du 20 novembre : latin en premier.** Pour une prière concédée en latin (ou en italien) sans traduction
  française approuvée, la page s'ouvre sur le latin, qui porte l'indulgence ; le français reste en regard, avec la note
  du can. 934, et ne compte pas. Quand une traduction approuvée existe, le français vient en premier. Recherche d'un
  recueil français approuvé (1938-1958) en cours ; rien ne sera utilisé avant d'être soumis à l'utilisateur.
- **Décisions du 20 novembre (après recherche)** :
  - **Beringer 1925** (décret de la S. Pénitencerie du 11 juillet 1925, t. I, p. v-vi : traduction reconnue fidèle) vaut
    traduction approuvée, **quand son français répond mot pour mot à la formule de 1952**. Les hymnes en vers (Veni
    Creator, Ave maris stella, Stabat) sont des paraphrases : elles restent en latin d'abord.
  - **Pater, Ave, Gloria** : les traductions usuelles gardent l'indulgence (*L'Ami du clergé*, 9 avril 1931, p. 252-253 :
    fidélité « notoire »). Le chapelet en français compte.
  - **Report pièce par pièce (20 nov., soir)** : Perpétuel Secours, les « Trois *Ave Maria* » de la formule de 1952 sont
    gardés en rubrique ; litanies du saint Nom, la traduction de Beringer est tenue pour approuvée telle quelle ; litanies de
    Lorette, ajouter les invocations postérieures à 1890 (Bon Conseil, Reine de la paix, Reine élevée au ciel), sourcées, le
    latin seul à défaut de traduction approuvée.
  - **Report fait le 20 nov.** (`beringer1925.py`, chaque texte relu sur le scan et comparé à la formule de 1952) : Angélus
    et Regina cæli, De profundis, Magnificat, En ego, Sept Douleurs (Beringer n° 450 = Ench. n° 383), Perpétuel Secours
    (avec les trois Ave de 1952), chapelet. Non retenus, faute de répondre mot pour mot à 1952 : « Doux Cœur de Jésus »,
    Douleurs et allégresses de saint Joseph (remplacés depuis par Thésaurisons, voir plus bas).
  - **Décisions du 21 nov.** : litanies du saint Nom de Beringer approuvées telles quelles ; litanies de Lorette
    complétées dans l'ordre de 1952 (Mère du bon conseil et Reine de la paix de Beringer ; « Regina in caelum assumpta »
    en latin, faute de traduction approuvée ; oraison de Thésaurisons n° 126) ; trois Ave du Perpétuel Secours gardés.
  - **Report de Thésaurisons dans le livret (21 nov.)** : « Doux Cœur de mon Jésus… » (n° 82 ; Triple Couronne et ses
    trois pages), Douleurs et allégresses de saint Joseph (n° 150), prière pour les agonisants (n° 498). Les pièces du
    livret peuvent porter `revision`, appliquée comme pour les textes sourcés (`reviserLivret`).

### Arbitrages des audits du 19 novembre (tranchés par les principes du § 11 ; l'utilisateur peut les reprendre)
Audits : `docs/audits/AUDIT_DEVOTIONS_2026-11-18.md` et `docs/audits/AUDIT_CORPUS_2026-11-18.md`.
- **Matin** : la prière du matin d'abord, l'offrande ensuite (l'usage de l'offrande dit « à la suite »). Les cinq actes
  de l'offrande restent chaque jour, en une seule page.
- **Antiennes mariales** : la structure voulue par l'utilisateur est gardée (Salve Regina le matin, Sub tuum le soir).
  Au temps pascal, le Regina cæli remplace déjà l'Angélus : pas de doublon.
- **Flèche d'or** : une fois à chaque Angélus, insérée dans sa page, dans la forme de Janvier 1895 (source ancienne
  identifiée). L'ajout du livret « et dans les enfers », sans source, est retiré.
- **Prière pour les agonisants** : insérée à l'Angélus de midi et dans les prières du matin et du soir (trois fois par
  jour), sans ligne propre.
- **Don du Saint-Esprit et douleur de Marie du jour** : une même rotation, puisqu'ils sont tirés de la même prière de
  Pie VII ; ils vont dans la prière du soir. La prière entière est indulgenciée (Ench. 1952, n° 383, « Vi compatisco ») ;
  une seule douleur dite à part ne l'est pas.
- **Triple Couronne d'or** : quotidienne, comme dans la liste de l'utilisateur.
- **Chapelet des Morts** : gardé le lundi. Ses indulgences sont réservées aux associés de l'archiconfrérie et ne sont pas
  comptées.
- **Heure sainte** : page explicative, proposée le jeudi dans la page de dévotion du jour, et non une tâche.
- **Actes du livret sans source ancienne** (offrande, devoirs de charité, Triple Couronne) : gardés, puisque le livret est
  celui de l'utilisateur, et marqués « composé pour le livret ». Les intentions sont gardées.
- **Promesses sans source** (saint Michel, sept grâces des Douleurs, promesses du Rosaire, offrande « Marie
  Corédemptrice ») : retirées de l'affichage tant qu'une source ancienne n'est pas trouvée (`A_FOURNIR.md`).
- **Sites hors de la liste admise**, mais fournis par l'utilisateur (christusregnat.com, La Bonne Nouvelle,
  salve-regina.com, Le Petit Sacristain) : gardés avec leur source ; source ancienne à trouver.
- **Prière du cardinal Mercier**, dont l'intention est périmée (définition du dogme de Marie Médiatrice) : gardée dans la
  bibliothèque, retirée de la liste du jour.
- **Litanies** : une seule litanie par jour, celle de la roue. Les litanies disparaissent des pages de dévotion du jour.
- **Temps liturgique** : chemin de croix de saint Alphonse et Miserere en Carême ; Adoro te et Lauda Sion à la Fête-Dieu ;
  Te Deum le 31 décembre ; Veni Creator le 1ᵉʳ janvier ; Christ-Roi. On les ajoute à mesure que des textes sourcés
  sont transcrits.

### Conception de la refonte (20 novembre) : décisions
Document : `docs/conception/REFONTE_2026-11-18.md`. Ergonomie : `docs/audits/ergonomie-2026-11-18.md`. Ordre des lots :
lot 0 (réparations, fait), puis les lots 1, 2 et 3 en parallèle, puis les lots 4 à 10.

Réponses aux questions de l'ingénieur-concepteur, tranchées par les principes du § 11 :
- **Office compté dans « Lectures du jour »** : le Petit bréviaire du Sacré-Cœur. Le Bréviaire romain et l'Officium parvum
  sont proposés dans Lecture › Office, sans être comptés.
- **Bréviaire romain** : en latin seul, tant qu'aucune traduction française ancienne et identifiée n'est trouvée ; aucune
  traduction de mémoire. À fournir : une édition bilingue ancienne.
- **Rappels aux heures canoniales** : aucun par défaut, réglables.
- **Lignes modifiées par l'utilisateur** : reprises automatiquement, avec une page « Ce qui a changé » qui permet de
  revenir en arrière.
- **Jaculatoire d'ouverture** : seulement celles de l'Enchiridion de 1952, dans une traduction approuvée (Thésaurisons
  1941) ou dans la langue de la concession.
- **Les trois seuils** (Omnia, Sine supererogatoriis, Præcipua tantum) sont gardés.
