# Audit des dévotions et de leur organisation (18 novembre 2026)

Audit en lecture seule, selon les principes du § 11 de `docs/cahier/SPEC.md` (refonte du 18 novembre).

**Méthode**
- La liste du jour d'une installation neuve a été reconstituée en suivant l'ordre exact de `amorcer()` (`app/src/lib/seed.ts`) :
  - liste de départ ;
  - liens `LIENS_SOURCES` ;
  - division des litanies, des dons et des dévotions de la semaine ;
  - fusion de l'examen ;
  - roues des litanies ;
  - `NOUVEAUX_ELEMENTS` ;
  - pages composées.
- Chaque ligne est ensuite résolue par `textesDuJour` (`app/src/lib/liste.ts`), pour la semaine réelle du 15 au 21 novembre 2026. Les roues des litanies sont alors en position 50 depuis le premier dimanche de l'Avent 2025.
- Les recouvrements de texte ont été cherchés automatiquement entre les 142 pièces de `data/prieres/sources.json` et les 62 du livret : suites communes de 5 et de 7 mots, sans tenir compte des accents ni des rubriques. Chaque cas retenu a été relu.
- Durées : on applique la règle de l'app (`app/src/lib/durees.ts` : 120 mots par minute, ou durée fixe par titre).
- **Indulgences** : aucune n'est comptée ici. Seul l'Enchiridion de 1952 fait foi (note de l'utilisateur du 18 nov.) : les indulgences de Beringer, de la Raccolta ou de Thésaurisons ne justifient plus aucun choix d'organisation. Le fichier `data/prieres/indulgences.json` est corrigé à part ; cet audit n'y touche pas.

---

## 1. Tableaux

### 1.1 La liste réelle, ligne par ligne (installation neuve)

Lignes présentes chaque jour (25 lignes en semaine, dont 4 génériques) :

| Moment | Ligne (`id`) | Textes résolus | Durée app |
|---|---|---|---|
| Matin | Offrande du matin (`liste:1`) | `hortus:offrande-du-matin` (4 actes + 5 devoirs) | 13,0 |
| Matin | Prière du matin (`liste:2`) | `paroissien:priere-du-matin` | 6,2 |
| Matin | Salve Regina, avec ses versets (`liste:3`) | `beringer:salve-regina` | 0,8 |
| Matin | Intentions particulières du jour (`liste:4`) | aucun (champ libre) | 1 (fixe) |
| Matin | Cordon : sept Gloria Patri (`liste:5`) | `hortus:cordon-sept-gloria` **+** `beringer:cordon-saint-joseph` | 4,0 |
| Propre | Office du jour et vie du saint (`liste:6`) | page `/saint` (leçons du IIe nocturne) | 5 (fixe) |
| Propre | Méditation du jour (`liste:7`) | page `/meditation` (livre du mois, sinon Hamon ou Chaignon) | 15 (fixe) |
| Propre | La roue du jour (`liste:roue`) | page `/roue` (6 roues actives) | 3 (fixe) |
| Propre | Dévotion du ‹jour› (`liste:8`, `8-1` … `8-6`) | voir 1.2 | 3,4 à 6,4 |
| Propre | Dévotion à jours comptés / Neuvaine ou trentain (`liste:9`, `liste:10`) | pratiques du plan du jour, voir 1.4 | somme des textes |
| Propre | Dévotion du mois (`liste:11`) | page `/mois` | 5 (fixe) |
| Journée | Angélus (`liste:12`) ×3 | `paroissien:angelus` (Regina cæli au temps pascal) | 3,2 |
| Journée | Prière pour les agonisants (`liste:13`) ×3 | `jardin:priere-pour-les-agonisants` | 1,8 |
| Journée | La Flèche d'or (`liste:14`) ×3 | `jardin:la-fleche-d-or` | 7,1 |
| Journée | Chapelet (`liste:15`) | `hortus:chapelet-{joyeux,douloureux,glorieux}` | 20 (fixe) |
| Journée | Triple Couronne d'or (`liste:16`) | `hortus:triple-couronne-{1,2,3}` | 15 (fixe) |
| Journée | Quinze oraisons de sainte Brigitte (`liste:19`) | `jardin:les-quinze-oraisons-de-sainte-brigitte` | 15,0 |
| Journée | Scapulaire de bénédiction et de protection (`liste:scapulaire-jahenny`) | `jahenny:scapulaire-benediction-protection` | 3 (fixe) |
| Journée | Jaculatoires du jour (`liste:jaculatoires`) | 10 des 40 `thesaurisons:jac-*`, par roulement de 4 jours | 2 (fixe) |
| Journée | Petit bréviaire du Sacré-Cœur (`liste:petit-breviaire`) | `breviaire-sc:office-‹jour›` (8 heures) | 16,2 à 20,5 |
| Soir | Prière du soir et examen de conscience (`liste:22`) | `paroissien:priere-du-soir` | 8,3 |
| Soir | Sub tuum, avec ses versets (`liste:23`) | `beringer:sub-tuum` | 0,7 |
| Soir | Litanies du jour (`liste:24`, `24-1` … `24-6`) | voir 1.2 | 2,8 à 17,8 |
| Soir | Demande du don de ‹…› (`liste:25`, `25-1` … `25-6`) | `beringer:don-‹don›` | 0,5 |

S'y ajoutent, certains jours seulement : Chapelet de saint Michel (`liste:17`, mardi), Chapelet des Morts (`liste:18`, lundi), Devant le Crucifix (`liste:20`, vendredi à 15 h) et Cordon : renouvellement et prière pour la pureté (`liste:cordon-mercredi`, mercredi).

### 1.2 Ce qui change selon le jour de la semaine (semaine du 15 au 21 novembre 2026)

| Jour | Dévotion du jour (`DEVOTIONS_SEMAINE`) | Ligne propre | Litanies du jour, résolues | Don | Total app |
|---|---|---|---|---|---|
| Dim. | `fervent:litanies-sainte-trinite` | — | `paroissien:litanies-des-saints`, `paroissien:litanies-saint-nom`, **`paroissien:litanies-des-saints`** (17,8 min) | sagesse | **172,6** (+ 1,5 du plan) |
| Lun. | `paroissien:de-profundis`, `beringer:chapelet-des-morts` | Chapelet des Morts : **les deux mêmes textes** | `fsspx:litanies-delivrance-ames-purgatoire`, `salve-regina:litanies-fideles-defunts` (11 min) | intelligence | **173,9** |
| Mar. | `jardin:chapelet-de-saint-michel-archange`, `jardin:a-saint-gabriel-archange` | Chapelet de saint Michel : **même texte** | `fervent:litanies-ange-gardien`, `jardin:litanies-de-la-sainte-face` | conseil | **178,1** |
| Mer. | `beringer:litanies-saint-joseph`, `beringer:saint-joseph-purete` | Cordon : `hortus:renouvellement-cordon-saint-joseph`, **`beringer:saint-joseph-purete`** | **`beringer:litanies-saint-joseph`** | force | **153,5** |
| Jeu. | `jardin:heure-sainte`, **`jardin:acte-d-intention-de-communion-spirituelle-perpetuelle`** (déjà dans l'offrande) | — | `fervent:litanies-saint-sacrement`, `paroissien:litanies-saint-nom` | science | **160,9** |
| Ven. | **`jardin:chaque-vendredi-devant-le-crucifix`**, **`beringer:litanies-sacre-coeur`** | Devant le Crucifix : **même texte** | **`beringer:litanies-sacre-coeur`**, `jardin:litanies-de-notre-dame-des-sept-douleurs` | piété | **160,6** |
| Sam. | **`paroissien:litanies-sainte-vierge`**, `beringer:coeur-afflige-de-marie` (contient le don du jour) | — | **`paroissien:litanies-sainte-vierge`**, `jardin:litanies-de-notre-dame-des-sept-douleurs` | **crainte (déjà dans le Cœur affligé)** | **160,1** (+ 1,6 du plan) |

Durée estimée par l'app, sans les rappels de fêtes. Elle compte les trois récitations des lignes répétées. En gras : textes en double.

**Cause de fond des litanies multiples.** Une ligne liée à une roue renvoie l'élément du jour de la roue, puis `e.textes.slice(1)` (`liste.ts`, l. 25). Ce comportement a été pensé pour le chapelet : la méthode de Montfort jointe en second texte. Or `roueDesLitanies` donne à la ligne **toutes** les litanies candidates (`seed.ts`, l. 522). D'où le résultat, chaque soir :
- la litanie de la semaine, **suivie de toutes les autres sauf la première** ;
- trois litanies le dimanche ;
- une même litanie dite deux fois, une semaine sur deux, ou chaque semaine le dimanche.

### 1.3 Doublons recensés (même jour)

| # | Jour | Texte en double | Où il paraît | Fréquence |
|---|---|---|---|---|
| 1 | Chaque jour | Gloria Patri | `hortus:cordon-sept-gloria` et `beringer:cordon-saint-joseph`, sur la même ligne. Le second n'est que le Gloria suivi d'une notice. | quotidien |
| 2 | Chaque jour | une ou deux jaculatoires du roulement | jour 1 : `jac-100` (dans l'offrande, devoir envers la famille) et `jac-33` (Triple Couronne) ; jour 2 : `jac-70` (= Crux ave du scapulaire) ; jour 3 : `jac-85` et `jac-134` (Triple Couronne) ; jour 4 : `jac-13` (= « Ô Dieu, venez à mon aide », ouverture de chaque heure du Petit bréviaire) | quotidien |
| 3 | Dimanche | une litanie | la litanie de la roue et le reste de la liste (cf. 1.2) ; la Trinité aussi dans la dévotion du dimanche | chaque dimanche |
| 4 | Lundi | `paroissien:de-profundis` et `beringer:chapelet-des-morts` | Dévotion du lundi et ligne Chapelet des Morts | chaque lundi |
| 5 | Lundi | `salve-regina:litanies-fideles-defunts` | dans la même ligne de litanies | un lundi sur deux |
| 6 | Mardi | `jardin:chapelet-de-saint-michel-archange` | Dévotion du mardi et ligne propre | chaque mardi |
| 7 | Mardi | `jardin:litanies-de-la-sainte-face` | dans la même ligne de litanies | un mardi sur deux |
| 8 | Mercredi | `beringer:saint-joseph-purete` | Cordon du mercredi et Dévotion du mercredi | chaque mercredi |
| 9 | Mercredi | `beringer:litanies-saint-joseph` | Dévotion du mercredi et Litanies | chaque mercredi |
| 10 | Mercredi | les sept invocations « Joseph très chaste… modèle des travailleurs » | les sept Gloria du cordon et les litanies de saint Joseph | chaque mercredi |
| 11 | Jeudi | `jardin:acte-d-intention-de-communion-spirituelle-perpetuelle` | Offrande du matin (page composée) et Dévotion du jeudi | chaque jeudi |
| 12 | Jeudi | `paroissien:litanies-saint-nom` | dans la même ligne de litanies | un jeudi sur deux |
| 13 | Vendredi | `jardin:chaque-vendredi-devant-le-crucifix` | Dévotion du vendredi et ligne de 15 h | chaque vendredi |
| 14 | Vendredi | `beringer:litanies-sacre-coeur` ou `jardin:litanies-de-notre-dame-des-sept-douleurs` | Dévotion et Litanies, ou deux fois dans les Litanies | chaque vendredi |
| 15 | Samedi | `paroissien:litanies-sainte-vierge` ou `jardin:litanies-de-notre-dame-des-sept-douleurs` | idem | chaque samedi |
| 16 | Samedi | invocation n° 1 du Cœur affligé (don de crainte) | `beringer:coeur-afflige-de-marie` et `beringer:don-crainte` | chaque samedi |
| 17 | Mars, mai, juin, juillet, novembre | la méditation du livre du mois | Méditation du jour (`choisirAvecMois`) et page Dévotion du mois (même entrée `J:n`, partie « Prière… » comprise) | chaque jour de ces mois |
| 18 | Jeudi avant le premier vendredi | `jardin:heure-sainte` | Dévotion du jeudi et pratique du plan « Heure sainte » (textes de la p. 69) | mensuel |
| 19 | Premier samedi, de septembre à novembre | `jardin:premiers-samedis-du-mois` et `jardin:douze-samedis-avant-l-immaculee-conception` | les deux pratiques du plan ont les mêmes deux textes (p. 73) : 3 oct. et 7 nov. 2026 | 2 jours par an |
| 20 | 28 sept. – 6 oct. | `sambucy:chapelet-saint-dominique` ; litanies de Lorette le samedi | Neuvaine du Rosaire et chapelet du jour (la page composée contient Sambucy) ; Dévotion du samedi | 9 jours par an |
| 21 | Dimanche de la neuvaine de la Toussaint | `paroissien:litanies-des-saints` | Neuvaine de la Toussaint et Litanies du dimanche | 1 jour par an |
| 22 | Samedi de la neuvaine de l'Immaculée Conception | litanies de la sainte Vierge | Weber (« les litanies ou les répons ») et Dévotion du samedi (5 déc. 2026) | 1 à 2 jours par an |
| 23 | Mardi de la neuvaine de saint Michel | chapelet de saint Michel, **trois fois** | neuvaine (p. 28), Dévotion du mardi, ligne propre (22 sept. 2026) | 1 à 2 jours par an |
| 24 | Mardi de la neuvaine de saint Gabriel | `jardin:a-saint-gabriel-archange` | neuvaine (p. 19) et Dévotion du mardi (16 et 23 mars 2027) | 1 à 2 jours par an |
| 25 | 14 mars 2027 | `jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph` | Sept dimanches de saint Joseph et Neuvaine à saint Joseph (p. 34) | 1 jour par an |
| 26 | Chaque jour (page Roue) | Credo, actes de foi, d'espérance et de charité | roues « articles du Symbole » (→ `paroissien:priere-du-matin`) et « vertus théologales » (→ `paroissien:acte-de-*`, extraits de la prière du matin) | quotidien |

En tout : **26 cas de doublon**. Quatorze reviennent chaque semaine ou chaque jour (n° 1-16, sauf 5, 7 et 12, qui reviennent une semaine sur deux). Neuf dépendent du plan ou du mois (n° 17-25). Le dernier (n° 26) est sur la page de la roue.

**Doublons dans la bibliothèque** (sans effet sur le jour tant qu'on n'en montre qu'une édition) :
- Flèche d'or : `jardin:la-fleche-d-or` et `janvier:fleche-d-or` ;
- litanies du Sacré-Cœur : `beringer:litanies-sacre-coeur` et `breviaire-sc:litanies` ;
- Cœur affligé de Marie : `beringer:coeur-afflige-de-marie` et `jardin:les-sept-douleurs-de-marie`, même prière. Les sept `beringer:don-*` en sont des extraits ;
- les actes de foi, d'espérance et de charité, extraits de `paroissien:priere-du-matin` ;
- le Sub tuum, contenu dans `jardin:la-petite-couronne-de-la-tres-sainte-vierge`.

### 1.4 Pratiques du plan : textes liés à tort (cause : `parPage`)

`pratiquesDuPlan` (`app/src/lib/plan.ts`) relie chaque pratique **aux trois premières pièces du livret imprimées à la même page**. Résultat :

| Pratique du plan | Textes reçus | Texte juste |
|---|---|---|
| Treize mardis de saint Antoine (p. 68) | `treize-mardis-de-saint-antoine` (rubrique), `quinze-mardis-de-saint-dominique`, `premier-mercredi-du-mois` | la rubrique + `jardin:les-treize-mardis-de-saint-antoine` (répons *Si quæris*, p. 37), absent |
| Quinze mardis de saint Dominique (p. 68) | les trois mêmes | `jardin:les-quinze-mardis-de-saint-dominique` (p. 38), absent |
| Premier mercredi : saint Joseph (p. 68) | les trois mêmes (Antoine, Dominique) | rubrique seule ; la pratique renvoie aux Douleurs et Allégresses, ou aux litanies de saint Joseph |
| Heure sainte et Premier vendredi (p. 69) | `heure-sainte` **et** `premiers-vendredis-du-mois`, les deux fois | un texte chacun |
| Premier samedi et Douze samedis (p. 73) | les deux mêmes textes | un texte chacun |
| Sept dimanches de l'Immaculée Conception (p. 65) | + `sept-dimanches-de-saint-camille-de-lellis` | sans Camille |
| Six dimanches de saint Louis de Gonzague (p. 63) | + `cinq-dimanches-de-saint-jean-berchmans` | sans Berchmans |
| Dix dimanches de saint Ignace (p. 66) | + `dix-dimanches-de-saint-stanislas-kostka` | sans Stanislas |
| Treize vendredis de saint François de Paule, Sept vendredis des Douleurs (p. 72) | les deux textes chacune | un texte chacune |
| Neuvaine à saint Gabriel (p. 19) | + `auguste-reine-des-cieux` | sans Auguste Reine |
| Six dimanches de saint Thomas, Sept dimanches de saint Joseph (p. 64) | les deux textes chacune | un texte chacune |
| Préparation à la consécration de Montfort (p. 11), 33 jours | `jardin:consecration-de-soi-meme-…` (l'acte de consécration, 6 min, chaque jour) | `montfort:preparation-consecration` pendant les 33 jours ; l'acte le 34e jour seulement |

### 1.5 Ce qui doit sortir de la liste vers l'onglet Lecture

| Ligne actuelle | Section de Lecture | Remarque |
|---|---|---|
| Office du jour et vie du saint (`/saint`, `data/recueils/breviaire.json`) | Spirituel | à la fin : la prière de sainte Gertrude propre à la catégorie du saint (décision du 18 nov. ; **texte à transcrire**) |
| Méditation du jour (Hamon, Chaignon, livres des mois) | Spirituel | sa durée de 15 min sort du temps de prière |
| Dévotion du mois, les mois qui ont un livre (3, 5, 6, 7, 11) | Spirituel | c'est la même entrée que la méditation : une seule lecture |
| Petit bréviaire du Sacré-Cœur (`breviaire-sc:office-*`) | Office | les huit heures en sections dépliables (principe 4) |
| La roue du jour : chapitre des Évangiles (`lecture-evangiles`, 89 éléments) | Écriture | bouton « J'ai lu ce chapitre » déjà en place |
| La roue du jour : versets des roues à méditer (un seul Dieu, fins dernières…) | Spirituel | « point » de lecture du jour |
| Guéranger, *L'Année liturgique* (déjà lu sur la page Méditation) | Spirituel | — |
| Visites au Saint-Sacrement (`liguori-visites`, J:1 … J:31) | Spirituel | lecture toute trouvée pour avril, mois eucharistique (voir 3.3) |
| *À venir* : Bréviaire romain, Officium parvum, Somme (Lachat) | Office, Doctrine | absents des données |

Avec ces six lignes en moins, la liste perd entre 44 et 49 minutes « de prière » qui sont en fait de la lecture.

### 1.6 Pages explicatives (onglet Dévotions, pas des tâches)

- `beringer:cordon-saint-joseph` : la pratique de l'archiconfrérie. Elle reste lisible, mais ne figure plus comme texte de la ligne.
- `jardin:heure-sainte` : une pratique d'une heure, décrite. Le texte n'est pas une prière, et la ligne annonce 1,3 min.
- `beringer:chapelet-des-morts`, partie « Manière de le réciter ». Ce chapelet est réservé aux associés de l'archiconfrérie de Nîmes : la notice le dit.
- `jahenny:scapulaire-benediction-protection`, parties I (port du scapulaire) et IV (intention). Les parties II et III passent dans la prière du matin et du soir (§ 11).
- Les rubriques des pratiques à jours comptés : treize mardis, sept dimanches, douze samedis, quinze samedis, premiers vendredis et premiers samedis. Ce sont des règles (confession, communion, chapelet), non des textes à dire.
- `jardin:acte-heroique-de-charite` (« une fois pour toutes »), `janvier:promesses-sainte-face`, et les « sept grâces promises » de `jardin:les-sept-douleurs-de-marie`.
- La page Dévotion du mois, les mois sans livre (janvier, février, avril, août, septembre, octobre, décembre) : nom du mois et référence. Rien à cocher.
- La notice de sainte Brigitte (monitum de 1954) et la manière de Sambucy, qui ouvre déjà la page du chapelet.

### 1.7 Incohérences d'organisation

1. **Une dévotion éclatée sur trois moments.** Saint Joseph le mercredi est réparti entre le matin (cordon), le propre (dévotion) et le soir (litanies). De même, les âmes le lundi : propre, journée et soir. Les « dévotions du jour » sont dans le Propre, leurs litanies au Soir.
2. **Sacré-Cœur saturé.** Chaque jour : Triple Couronne (15 min) et Petit bréviaire (16 à 20 min). Le vendredi, s'ajoutent les litanies (deux fois), le Crucifix et l'office du vendredi ; en juin, le mois ; au premier vendredi, la pratique ; avant la fête, la neuvaine.
3. **Heure sainte.** Elle est prévue **chaque jeudi** (dévotion du jeudi) et **le jeudi avant le premier vendredi** (plan), avec le même texte. La pratique décrite est la nuit du jeudi au vendredi.
4. **Flèche d'or : « trois fois ».** La rubrique du livret porte « On dira trois fois cet acte de louange en l'honneur des trois personnes ». La ligne en fait trois rappels (7 h, 12 h, 21 h), sans lien avec l'Angélus.
5. **Durées faussées :**
   - les rubriques `[r]…[/r]` sont comptées comme texte dit. La Flèche d'or vaut ainsi 2,4 min au lieu d'environ 0,5, soit 7,1 min par jour pour 1,5 min réelle ;
   - l'Heure sainte compte pour 1,3 min ;
   - le cordon compte la notice de Beringer ;
   - les quinze Pater et Ave de sainte Brigitte ne sont pas comptés ;
   - une neuvaine compte ses neuf jours chaque jour : Liguori, Sacré-Cœur 25,6 min ; Noël 23,0 ; Assomption 14,3 ; Weber, Immaculée Conception 11,0. Un jour en vaut 2 à 3 ;
   - les jaculatoires valent 2 min fixes pour 10 textes.
6. **Rangs.** Le seuil par défaut affiche tout. Sainte Brigitte est « principale », tandis que la dévotion du jour et les litanies sont « pieuses » : un jour chargé garde 15 min de Brigitte et perd la dévotion propre du jour.
7. **Lignes vides comptées comme tâches.** « Intentions particulières » (pas de texte), Dévotion du mois sans livre (5 min fixes) et La roue du jour (3 min fixes) entrent dans l'avancement du jour.
8. **Don du jour et douleur du jour.** Ce sont deux invocations différentes de la même prière (Cœur affligé), qui ne coïncident pas :
   - les dons suivent Isaïe : dimanche sagesse … samedi crainte ;
   - la roue `douleurs-marie` suit l'ordre des douleurs : dimanche Siméon (crainte) … samedi sépulture (sagesse).

   Elles ne tombent ensemble que le mercredi (force).
9. **Salve Regina le matin, Sub tuum le soir « avec leurs versets ».** Ce choix reposait sur une indulgence de Beringer (n° 429), abrogée. Rien ne suit le temps liturgique, alors que `weber:alma-redemptoris` et `weber:ave-regina-caelorum` existent (antiennes de l'Avent et du temps de la Purification). Seul l'Angélus change au temps pascal (`remplacementsDuTemps`).
10. **Temps liturgique presque muet.** Hors du Regina cæli, ni l'Avent ni le Carême ne modifient la journée. Aucun texte de chemin de croix n'est dans les données : le « petit chemin de croix » de Janvier n'est pas transcrit.
11. **Ordre des moments.** La roue (ordre 75) s'intercale entre la méditation et la dévotion. Le Petit bréviaire, un office distribué aux heures, est une seule tâche de « journée ».
12. **Pratiques du plan qui doublent une pratique quotidienne.** Elles demandent ce que la journée fait déjà, et doivent qualifier la ligne existante au lieu d'en ajouter une :
    - Quinze samedis du Rosaire, Premiers samedis, Douze samedis : chapelet et méditation ;
    - Neuvaine du Rosaire : chapelet et Lorette ;
    - Premier mercredi : litanies de saint Joseph, déjà dites le mercredi.
13. **Jaculatoires indulgenciées.** Le classement « rapport indulgence / longueur » vient de Thésaurisons (1941). Il doit être refait d'après l'Enchiridion de 1952 ; il n'est pas utilisé ici.

---

## 2. Programme unique cible

Règles appliquées :
- une pratique est déclarée une fois, rattachée à son jour, son mois ou son temps ;
- les petites pratiques vont aux **points d'insertion** ;
- ce qui se lit va à **Lecture** ;
- les identifiants sont ceux des données ; aucun texte nouveau.

> Garde-fou canonique, valable seulement pour les œuvres de l'Enchiridion de 1952 : une même œuvre ne gagne pas deux indulgences, sauf exception expresse (CIC 1917, can. 933). On **place** donc deux pratiques dans la même page, sans **fondre** deux récitations indulgenciées en une seule. Exemple : les sept Pater du Crucifix et ceux des Sept vendredis des Douleurs.

### 2.1 Séquences hôtes et leurs points d'insertion

| Hôte (page) | Contenu | Points d'insertion |
|---|---|---|
| **Prière du matin** | `paroissien:priere-du-matin`, puis la section « Offrande » (`hortus:offrande-du-matin`) | (a) après « Invoquons la sainte Vierge » : `beringer:salve-regina` ; (b) après l'offrande : intentions particulières (champ libre, ni tâche ni durée) ; (c) fin : Crux ave, 5 ou 7 fois (`jahenny:…`, II-1) et 1re prière pour les agonisants (`jardin:priere-pour-les-agonisants`) |
| **Angélus**, 3 fois | `paroissien:angelus` ; au temps pascal `beringer:regina-caeli` (le samedi saint, les deux) | après l'oraison : `jardin:la-fleche-d-or` (sans la notice) ; à midi seulement : 2e prière pour les agonisants |
| **Chapelet du jour** | `hortus:chapelet-*` (Sambucy, Montfort, trois Ave de sainte Mechtilde) | fin de dizaine, après « Grâce du mystère… » : « Ô Marie, conçue sans péché, priez pour nous qui avons recours à vous » (1re phrase de `weber:demande-d-une-bonne-mort`, Weber 1899, p. 477) ; les deux autres invocations de l'exemple du § 11 **n'ont pas de source** (§ 2.6). Les jours de Quinze samedis, Premiers samedis, Douze samedis et de neuvaine du Rosaire : rappel de l'intention et du mystère, sans ligne de plus. |
| **Prière du soir** | `paroissien:priere-du-soir` (examen compris) | (a) fin : `beringer:sub-tuum` (latin seul pour « Domina nostra… », décision du 18 nov.) ; (b) le don du jour `beringer:don-*`, sauf le samedi ; (c) les trois salutations à Jésus crucifié (`jahenny:…`, III) ; (d) 3e prière pour les agonisants |
| **Fin de l'office du saint** (Lecture) | leçons du jour | prière de sainte Gertrude selon la catégorie du saint (**à transcrire**) |

La ligne Scapulaire disparaît. Sa minute de méditation de la Passion est tenue par les oraisons de sainte Brigitte (§ 11, exemple 3).

La ligne Jaculatoires disparaît aussi : une jaculatoire s'affiche à l'ouverture de l'écran (principe 5). Il faut alors écarter du tirage du jour celles déjà contenues dans les pages du jour : `jac-100`, `jac-33`, `jac-85`, `jac-134`, `jac-70`, `jac-13`.

### 2.2 Le tronc commun (chaque jour)

| Ordre | Moment | Page | Textes | Durée |
|---|---|---|---|---|
| 1 | Matin | Prière du matin (avec offrande et insertions) | voir 2.1 | ≈ 21 |
| 2 | Matin | Cordon de saint Joseph : sept Gloria (jours autres que le mercredi) | `hortus:cordon-sept-gloria` seul | 1,7 |
| 3 | Midi (et 6 h, 18 h) | Angélus, ×3 | voir 2.1 | ≈ 5,5 au total |
| 4 | Journée | Chapelet du jour | voir 2.1 | 20 |
| 5 | Journée | Triple Couronne d'or (couronne du jour) | `hortus:triple-couronne-{1,2,3}` | 15 |
| 6 | Journée | Quinze oraisons de sainte Brigitte (tient lieu de méditation de la Passion) | `jardin:les-quinze-oraisons-de-sainte-brigitte` | ≈ 20 (avec 15 Pater et 15 Ave) |
| 7 | Selon le jour | **Dévotion du jour**, une seule page, voir 2.3 | — | 4 à 20 |
| 8 | Soir | Prière du soir (avec insertions) | voir 2.1 | ≈ 10 |
| — | Lecture | une ligne « Lectures du jour (n/4) » : office du saint, méditation, Petit bréviaire, Évangile | voir 1.5 | hors temps de prière |

Le tronc commun fait environ **93 min** de prière vocale.

### 2.3 La dévotion du jour : une page par jour de la semaine

Chaque page regroupe ce qui était éclaté entre Propre, Journée et Soir. Elle contient **une** litanie, choisie par la roue de la semaine. Les lignes `liste:8-*`, `liste:17`, `liste:18`, `liste:20`, `liste:24-*` et `liste:cordon-mercredi` disparaissent.

| Jour | Page « Dévotion du ‹jour› » (ordre de la page) | Moment | Durée |
|---|---|---|---|
| Dimanche, la Trinité | une litanie de la roue : `fervent:litanies-sainte-trinite` / `paroissien:litanies-saint-nom` / `paroissien:litanies-des-saints` | soir | ≈ 5 |
| Lundi, les âmes du purgatoire | chapelet des Morts (`beringer:chapelet-des-morts`, invocation ; `paroissien:de-profundis` sur les gros grains, **une fois dans la page**) ; une litanie : `fsspx:litanies-delivrance-ames-purgatoire` / `salve-regina:litanies-fideles-defunts` | journée | ≈ 15 |
| Mardi, les saints Anges | `jardin:chapelet-de-saint-michel-archange` ; oraison `jardin:a-saint-gabriel-archange` ; une litanie : `fervent:litanies-ange-gardien` / `jardin:litanies-de-la-sainte-face` | journée | ≈ 20 |
| Mercredi, saint Joseph | page du cordon (décision du 18 nov.) : `hortus:renouvellement-cordon-saint-joseph`, `beringer:saint-joseph-purete`, `beringer:litanies-saint-joseph`, puis les sept Gloria **sans les invocations**, déjà dites dans les litanies. Elle remplace la ligne 2 ce jour-là. | matin | ≈ 6 |
| Jeudi, le Saint-Sacrement | une litanie : `fervent:litanies-saint-sacrement` / `paroissien:litanies-saint-nom`. La communion spirituelle reste dans l'offrande ; l'Heure sainte devient une page explicative, proposée au plan le jeudi avant le premier vendredi. | soir | ≈ 5 |
| Vendredi, la Passion et le Sacré-Cœur | à 15 h : `jardin:chaque-vendredi-devant-le-crucifix` ; une litanie : `beringer:litanies-sacre-coeur` / `jardin:litanies-de-notre-dame-des-sept-douleurs` | 15 h | ≈ 8 |
| Samedi, la sainte Vierge | `beringer:coeur-afflige-de-marie`, qui contient le don du jour (crainte) ; une litanie : `paroissien:litanies-sainte-vierge` / `jardin:litanies-de-notre-dame-des-sept-douleurs` | soir | ≈ 6 |

### 2.4 Durées par jour, avant et après

| Jour | Avant (app, liste entière) | Avant, sans ce qui se lit | Après (prière) | Lecture du jour, à part |
|---|---|---|---|---|
| Dimanche | 172,6 | ≈ 124 | ≈ 98 | ≈ 45 |
| Lundi | 173,9 | ≈ 126 | ≈ 108 | ≈ 45 |
| Mardi | 178,1 | ≈ 132 | ≈ 113 | ≈ 43 |
| Mercredi | 153,5 | ≈ 109 | ≈ 97 | ≈ 41 |
| Jeudi | 160,9 | ≈ 115 | ≈ 98 | ≈ 43 |
| Vendredi | 160,6 | ≈ 116 | ≈ 101 | ≈ 42 |
| Samedi | 160,1 | ≈ 113 | ≈ 99 | ≈ 44 |

« Avant, sans ce qui se lit » retire la méditation, l'office du saint, la roue, le mois et le Petit bréviaire. « Après » compte les durées réelles : Flèche sans notice, Brigitte avec ses Pater et Ave.

Le gain tient pour un tiers aux doublons et aux litanies multiples (6 à 13 min selon le jour), pour un tiers aux durées faussées, pour un tiers aux insertions. Une neuvaine ou une série du plan ajoute en moyenne 2 à 5 min, une fois les neuvaines réduites au jour.

### 2.5 Ce qui modifie la journée : mois, temps, plan

**Temps liturgique**

| Temps | Changement |
|---|---|
| Temps pascal (samedi saint, midi → samedi avant la Trinité) | Angélus → `beringer:regina-caeli` (en place) |
| Avent → Purification ; Purification → jeudi saint | antienne finale de la Vierge selon le temps (`weber:alma-redemptoris`, `weber:ave-regina-caelorum`) à la fin de la prière du soir : **arbitrage**, question 2 |
| Carême | aucun texte de chemin de croix dans les données : **texte manquant** |

**Mois** (ligne « Dévotion du mois » supprimée comme tâche ; elle devient une page explicative, plus ceci)

| Mois | Lecture (Spirituel) | Pratique ajoutée à une page existante |
|---|---|---|
| Janvier, saint Nom | — | la litanie du saint Nom, aux dimanches et jeudis de janvier, dans la roue des litanies |
| Février, Sainte Famille | — | aucune |
| Mars, saint Joseph | `mois-joseph` (méditation du jour) | `jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph` (usage « mois de mars »), dans la page du mercredi en mars. Les sept dimanches et la neuvaine de saint Joseph (même texte) **ne l'ajoutent pas une 2e fois** le même jour. |
| Avril, mois eucharistique | proposition : `liguori-visites`, visite du jour `J:n` | — |
| Mai, Marie | `mois-marie` | — |
| Juin, Sacré-Cœur | `mois-sacre-coeur` | neuvaine (Liguori) : **la section du jour seulement** |
| Juillet, Précieux Sang | `mois-precieux-sang` | `jardin:les-sept-offrandes-du-precieux-sang` (usage « en juillet »), en ligne du mois ou dans la page du vendredi |
| Août, Cœur immaculé | — | candidat : `weber:priere-tres-saint-coeur-de-marie` (Weber, p. 405-406) |
| Septembre, Sept Douleurs | — | `jardin:les-sept-douleurs-de-marie` (« quot. en septembre ») chaque jour ; le samedi, il tient lieu du Cœur affligé (même prière) |
| Octobre, Rosaire | — | le chapelet est déjà quotidien ; la neuvaine du Rosaire qualifie le chapelet du jour et donne Lorette, sans double le samedi |
| Novembre, les âmes | `mois-purgatoire` (la page « Prière, exemple » est la fin de la même lecture) | — |
| Décembre, Immaculée Conception | — | neuvaine de Weber (29 nov. – 7 déc.) : section du jour ; « litanies **ou** répons » → les **répons** quand Lorette est déjà dite (samedi) |

**Plan**
- Corriger les liens de textes (1.4).
- Une pratique du plan qui demande ce que la journée fait déjà n'ajoute pas de ligne : elle annote la ligne hôte. Exemples : chapelet et méditation des samedis ; litanies du premier mercredi ; Heure sainte du jeudi.
- Une pratique qui apporte un texte propre ajoute une seule ligne, avec le texte du jour seulement :
  - les répons de saint Antoine et de saint Dominique ;
  - la prière de saint Thomas ;
  - l'acte de réparation du premier vendredi ;
  - les jours des neuvaines.

### 2.6 Textes manquants (aucune source dans les données)

1. « Ô mon Jésus, pardonnez-nous nos péchés… » (invocation de fin de dizaine citée par l'utilisateur).
2. « Cœur immaculé de Marie, priez pour nous maintenant et à l'heure de notre mort » (scapulaire vert).
3. Les prières de sainte Gertrude par catégorie de saint (vierge, martyr, confesseur…), pour la fin de l'office du saint. Elles sont à transcrire de Denis, *Prières de sainte Gertrude*.
4. Un texte ancien de chemin de croix pour le Carême (le petit chemin de croix de Janvier 1895 n'est pas transcrit).
5. Le répons de saint Antoine et la pratique de saint Dominique : ils existent (`jardin:les-treize-mardis-de-saint-antoine`, p. 37 ; `jardin:les-quinze-mardis-de-saint-dominique`, p. 38), mais ne sont pas reliés.
6. La prière ancienne à saint Louis-Marie Grignion de Montfort pour sa neuvaine (déjà notée dans `docs/REPRISE.md`).
7. Le Bréviaire romain, l'Officium parvum et la Somme (Lachat), pour Lecture.

---

## 3. Questions qui demandent un arbitrage

Les points tranchés par les principes du § 11 ne sont pas repris ici : doublons, insertions, lectures, pages explicatives, corrections du plan.

1. **Le don du jour et la douleur du jour** (roue `douleurs-marie`). Ce sont deux invocations de la même prière, décalées. Faut-il :
   - (a) aligner la roue des douleurs sur les dons ;
   - (b) aligner les dons sur la roue ;
   - (c) retirer la douleur du jour de la roue ?
2. **Antienne de la Vierge selon le temps.** Le Salve du matin et le Sub tuum du soir « avec versets » reposaient sur une indulgence de Beringer, désormais abrogée. Faut-il garder ce couple toute l'année, ou dire à la fin de la prière du soir l'antienne du temps : Alma Redemptoris, Ave Regina cælorum, Regina cæli, Salve Regina ?
3. **La Triple Couronne et le Petit bréviaire, tous deux quotidiens.** Une fois le bréviaire passé dans Lecture › Office, la Triple Couronne reste-t-elle quotidienne (15 min), ou seulement le vendredi et en juin ?
4. **L'offrande du matin.** 13 min chaque jour, dont 5 actes des devoirs de charité. Faut-il les dire tous chaque jour, ou un par jour de la semaine ?
5. **La Flèche d'or.** Une fois à chacun des trois Angélus, comme proposé ici, ou trois fois de suite, une seule fois par jour, comme on peut lire la rubrique ?
6. **Le chapelet des Morts** est approuvé « pour l'usage des seuls associés » de l'archiconfrérie de Nîmes. Faut-il le garder le lundi, ou le remplacer par le De profundis seul ?
