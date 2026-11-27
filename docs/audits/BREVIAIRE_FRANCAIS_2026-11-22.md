# Bréviaire romain et Officium parvum : recherche d'une traduction française ancienne (22 novembre 2026)

Demande de l'utilisateur (22 nov.) : trouver une traduction française **ancienne et identifiée** du Bréviaire romain et
de l'Officium parvum B.M.V., pour afficher le français en regard du latin. Règle (REFONTE § 5.5, CLAUDE.md § 13 et
§ 15) : le français ne s'affiche que si son édition ancienne est identifiée ; aucune traduction faite par le modèle ; les
fichiers `Francais` de Divinum Officium, qui ne disent pas leur édition, restent écartés.

Ce document : les éditions examinées, la recommandation, ce qui a été transcrit, ce qui reste.

## 1. Officium parvum B.M.V.

| Édition | Accès | Approbation | Français | Scan, couche texte | Verdict |
|---|---|---|---|---|---|
| **Petit office de la Sainte Vierge et des morts, sépulture des défunts, messe, chemin de la croix, prières des quarante-heures, etc.**, Montréal, 1905 (emblème de la Congrégation de Notre-Dame de Montréal sur la page de titre) ; traducteur non nommé | archive.org `cihm_98272` (microfiche ICMH/Canadiana 98272, exemplaire de la Bibliothèque nationale du Québec ; 349 images, 300 ppi) | « Permis d'imprimer, ✠ Zotique, Év. de Pogla, V. G., Aux. à Montréal, 4 juin 1905 » (Mgr Zotique Racicot), vu sur l'image n5 | **Oui**, en regard : français page paire, latin page impaire ; les trois offices (Purification-Avent, Avent, Noël-Purification), le temps pascal, la Septuagésime, l'office des Morts | Lisible ; quelques lettres effacées ou brisées ; couche ABBYY correcte sur la plupart des pages, illisible sur une page sur dix environ (pages sombres ou de travers) | **Retenu** |
| *Petit office de la Sainte Vierge Marie avec l'office des morts…, selon le Bréviaire romain*, Tournai, Desclée, Lefebvre et Cie, 1875 | bibliotheque-catholique.com (`00/Mariologie/Petit office de la Sainte Vierge Marie selon le bréviaire romain.pdf`, scan Google) | *Imprimatur* de Mgr Dumont, évêque de Tournai | **Non** : latin seul, rubriques en français | Bon | Écarté (pas de traduction) |
| Dom Gaétan Froment, *Le Petit office de la Sainte Vierge expliqué et commenté*, édition latine-française, Ligugé, impr. Saint-Martin, 1893 | trouvé seulement sur Scribd (téléversement d'un particulier) ; ni archive.org, ni Google Livres (quota de l'API épuisé), ni Gallica (accès bloqué par Cloudflare depuis l'environnement) | Abbé de Ligugé ; *Imprimatur* de Poitiers, 12 avril 1893 | Oui, avec commentaire | Inconnu | **Piste** : meilleure édition française (bénédictine, commentée) si un scan libre est trouvé ; Scribd n'est pas une source admise |
| *Le Petit office de la très sainte Vierge noté en plain-chant*, Solesmes, 1893 | churchmusicassociation.org (PDF) | *Imprimatur* du Mans, 1893 | Non (latin noté) | — | Écarté |
| *Guide du jeune homme* (1882, `cihm_45340`) ; *Mine spirituelle* (1883, `cihm_53671` ; 1915, `minespirituelleo00sain`) ; *Office de la Sainte Vierge* (1873, `cihm_92865`) | archive.org | — | Latin seul pour l'office (les recueils traduisent les prières, pas les psaumes de l'office) | — | Écartés |
| *Paroissien romain*, Tours, Mame, 1890 (déjà dans le projet) | `paroissienromain00tour` | Archevêque de Tours | Oui, mais « Office ordinaire de la sainte Vierge » = Vêpres du commun du Bréviaire, pas le Petit office | Bon | Écarté pour le Petit office (utile pour les Vêpres du dimanche) |
| Éditions de 1947 (Roguet, sur le psautier de Bea) et 1959 (*editio amplior*, Bea, trad. Mont-César) | non numérisées | — | — | — | Hors période (psautier de Bea, rubriques postérieures) |

Recherches sans résultat : archive.org (titres « petit office », « office de la sainte vierge », « officium parvum »,
« heures », par langue fre), recherche web (Parallel Search) sur Gallica, Google Livres, HathiTrust.

### Faisabilité de l'alignement

`data/office/parvum.json` compte **224 paragraphes** latins (dédoublonnés) ; les heures en sont des listes d'indices.
L'édition de 1905 suit le même latin (texte de saint Pie V revu sous Urbain VIII ; le psautier du Petit office n'a pas
été touché par *Divino afflatu*). Écarts constatés sur les Complies :

- l'édition **abrège** ce que DO écrit en entier : « Je vous salue, Marie, etc. », « Gloire soit au Père, etc. »
  (sauf à l'ouverture de l'heure), Pater, Ave, Credo réduits à leurs premiers mots latins ; ces abréviations sont gardées ;
- un même paragraphe latin peut correspondre à **deux traductions** dans l'édition (le verset *Angelus Domini*, para. 12,
  traduit « a annoncé… a conçu » au capitule, « annonça… conçut » après l'*Alma Redemptoris*) : alignement partiel,
  signalé ;
- l'hymne est traduite en **prose**, une strophe par paragraphe (alignement strophe à strophe possible) ;
- les psaumes : un alinéa français par verset latin, alignement ligne à ligne possible ;
- une traduction de l'antienne *Spiritus Sanctus* omet l'« alleluia » du latin (para. 14) ; gardé tel qu'imprimé.

L'alignement par indice est donc faisable, avec une note par paragraphe. Une **empreinte du latin** (SHA-1, 12 caractères)
accompagne chaque entrée : si `engine/office/parvum.py` régénère `parvum.json` et déplace les indices, le contrôle
`engine/office/test_parvum_fr.py` échoue au lieu d'afficher un français en face du mauvais latin.

## 2. Bréviaire romain

| Édition | Accès | Approbation | Couverture | Texte français | Scan | Verdict |
|---|---|---|---|---|---|---|
| **P. Étienne Hugueny, O. P.** (avec l'abbé Obert), *Le Bréviaire romain, textes latins et français*, Paris, Labergerie : corps (Ordinaire, Psautier, Commun des saints), 14 fascicules du Propre du temps, 14 du Propre des saints, 2 suppléments | archive.org, mis en ligne par « oradtrad » d'après les scans de la Bibliothèque Saint Libère (liberius.net) : `le-breviaire-romain-000001439` (corps), `le-breviaire-romain-propre-du-temps-fascicule-<1-14>-…`, `le-breviaire-romain-propre-des-saints-fascicule-<1-14>-…`, `le-breviaire-romain-supplement-<1-2>-…` ; **le fascicule 8 du Propre du temps manque** sur archive.org | *Imprimatur* Paris, 8 sept. 1934 (V. Dupin, v. g.) ; lettres des cardinaux Maurin (Lyon, 1933), Verdier (Paris, 1934), Binet (Besançon, 1932). Le corps numérisé est la « nouvelle édition » achevée d'imprimer le 15 août 1947 (Desclée De Brouwer, Bruges) | **Tout** : psaumes, hymnes (traduction « rythmée »), antiennes, capitules, répons, oraisons, leçons des trois nocturnes, homélies, légendes des saints ; rubriques de *Divino afflatu* (calendrier 1933-1964 en tête) | Psaumes traduits **de l'hébreu** (« traduction critique », le sens de la Vulgate souvent préféré, et donné en note quand il diffère : « V. : qui m'a délivré du filet des chasseurs… ») ; antiennes, hymnes, leçons traduites du latin | Excellent (impression nette, 300-384 ppi) ; couche texte ABBYY bonne mais colonnes latin/français entremêlées | **Recommandé** pour le Bréviaire, sauf pour les psaumes (voir plus bas) |
| **L.-Cl. Fillion**, p. s. s., *Le nouveau psautier du Bréviaire romain, texte et traduction, avec notes succinctes*, 7e éd., Paris, Lecoffre-Gabalda, 1917 | archive.org `lenouveaupsautie00gl` (Université d'Ottawa, 558 images, 500 ppi) | *Nihil obstat* H. Garriguet ; *Imprimatur* Paris, 4 juin 1912 (P. Thomas) | Psautier de saint Pie X (*Divino afflatu*, 1911) dans l'ordre liturgique, avec les cantiques (Benedictus, Magnificat, Nunc dimittis, cantiques de Laudes) ; ni hymnes ni propre | Traduction **de la Vulgate** (« au fond, celle de Sacy », revue), versets numérotés | Bon ; couche texte correcte | **Recommandé pour les psaumes** (Bréviaire et Petit office) |
| *Les hymnes du Bréviaire romain traduites littéralement en français avec le texte latin en regard*, 4 fasc., [Ottawa, Université d'Ottawa], 1900 | archive.org `cihm_58336` … `cihm_58339`, `cihm_48265` | à vérifier | Hymnes seules | Traduction littérale | Microfiche | Complément possible pour les hymnes |
| *La Sainte Bible*, trad. Crampon, Desclée, 1923 (déjà dans le projet, `data/ecriture/ps.json`) | Wikisource relu | *Imprimatur* | Psaumes | **Traduite de l'hébreu**, numérotation hébraïque | — | **Écartée pour le Bréviaire** (voir ci-dessous) |
| Fillion, *Le nouveau psautier…*, autre exemplaire | bibliotheque-catholique.com, `_en_attente` (27 Mo) | — | — | — | — | Doublon de `lenouveaupsautie00gl` |
| Le Tourneux (1688), abbé Bayle, autres « Bréviaire romain traduit » | non trouvés en ligne ; Le Tourneux condamné par l'officialité de Paris (1688, `sentencerendu00pari`) | — | — | — | — | Écartés |

### Crampon 1923 et le psautier du Bréviaire : conclusion prudente

Les psaumes de Crampon **ne peuvent pas servir** de traduction en regard du psautier du Bréviaire :

1. **Texte traduit différent** : Crampon traduit l'hébreu massorétique, le Bréviaire chante la Vulgate (psautier gallican).
   Exemple, Ps 109 (Vulg.), 3 : « *Tecum principium in die virtutis tuæ in splendoribus sanctorum: ex utero, ante
   luciferum, genui te* » ; Crampon (Ps 110, 3) : « Ton peuple accourt à toi au jour où tu rassembles ton armée, avec des
   ornements sacrés ; du sein de l'aurore vient à toi la rosée de tes jeunes guerriers. » Le sens n'est plus le même ;
   l'antienne tirée du verset latin perdrait son appui.
2. **Numérotation décalée** (Ps 9-147 : Vulgate = hébreu − 1, avec des psaumes fusionnés ou coupés : 9-10, 113-115,
   146-147) et **découpage des versets** différent (titres comptés comme versets chez Crampon : Ps 86/87, 1).
3. Vocabulaire étranger à l'office (« Yahweh », « Séla »).

`ps.json` garde d'ailleurs en regard le latin de la Vulgate (numérotation Vulgate du côté latin) : il reste utile en
lecture biblique, pas comme traduction liturgique. Pour les psaumes du Bréviaire, **Fillion 1917** (Vulgate, ordre de
*Divino afflatu*, *imprimatur*) est la bonne source ; Hugueny traduit l'hébreu, comme Crampon, mais donne le sens de la
Vulgate en note quand il s'écarte.

### Faisabilité pour `data/office/breviaire/2026-2027/`

Les psaumes y sont des paragraphes « `[r]Psalmus N[/r]` » à un verset par ligne (867 paragraphes de `communs.json`
contiennent un psaume) : un alignement par **numéro de psaume et de verset** avec Fillion (versets numérotés) est
faisable, mais il faut d'abord découper Fillion par verset (OCR à relire, mise en page par hémistiches). Pour le reste
(hymnes, antiennes, capitules, oraisons, leçons), Hugueny couvre tout, mais l'alignement doit se faire pièce par pièce
(titres du propre, jour par jour) : c'est un chantier de l'ordre de plusieurs milliers de pièces, à mener par lots
(Ordinaire et Complies d'abord, puis psautier, puis commun, puis propres).

## 3. Recommandation

1. **Officium parvum** : édition de **Montréal 1905** (`cihm_98272`), la seule édition latin-français approuvée et
   numérisée librement trouvée ; transcrire le reste par heure, sur le modèle des Complies. Si un scan libre de **Froment,
   Ligugé 1893** apparaît (Gallica, Google Livres), le comparer : traduction bénédictine, commentée, peut-être préférable.
2. **Bréviaire romain** : **Fillion 1917** pour les psaumes et cantiques ; **Hugueny (Labergerie, 1934, rééd. 1947)**
   pour tout le reste. Point à faire trancher par l'utilisateur : Hugueny est mort en 1942 et l'abbé Obert à une date
   inconnue ; les scans portent « toute reproduction à but non lucratif est autorisée » (Bibliothèque Saint Libère) ; le
   projet demande des éditions « antérieures à 1955, domaine public ».
3. **Crampon** : ne pas l'employer pour le psautier liturgique.
4. **Indulgence** : l'Enchiridion 1952 indulgencie la récitation du Petit office ; aucune de ces éditions ne porte de
   déclaration de fidélité (can. 934 § 2) : le compteur continue de s'appuyer sur le latin.

## 4. Ce qui est fait

- `data/office/parvum-fr.json` (proposition, **non branchée** : ni chargeur, ni `seed.mjs`, ni affichage) : une entrée par
  paragraphe latin de `parvum.json` (224), avec `la_sha1`, `statut`, `page`, `fr`, `note`, `lecture`.
  - **état au 22 nov. au soir : 201 paragraphes alignés sur 224** (159 « aligné », 42 « aligné en partie »),
    11 sans équivalent (titres ou rubriques de DO que l'édition n'imprime pas, et le verset de l'Avent *Hodie scietis*,
    para. 120, absent de l'édition), **12 « à transcrire »** (voir § 5) ;
  - par heure : Complies et antiennes finales (pp. 36-58), Vêpres (pp. 10-36), Laudes (pp. 108-136), Prime, Tierce,
    Sexte, None (pp. 138-180), **Matines (pp. 60-106)** : invitatoire et psaume 94, hymne *Quem terra*, psaumes des trois
    nocturnes avec leurs antiennes, Pater et absolution, bénédictions, leçons de l'Avent (S. Luc) et « de Noël à l'Avent »
    (Ecclésiastique) avec leurs répons, *Te Deum* ;
  - « aligné en partie » : un même paragraphe latin imprimé sous plusieurs formes selon l'heure (la forme retenue et
    les autres sont dans la note), formes pascales avec *alleluia* que l'édition n'imprime pas (para. 123, 124),
    répons dont DO omet le Gloria alors que l'édition ne l'imprime qu'avec (122, 135), ouverture de Matines dont
    l'édition omet le répons « Hâtez-vous… » (89, 121, 132).
  - Écarts de l'imprimé gardés et notés (Matines) : « le Très-Haut a sacrifié son tabernacle » (Ps 45, p. 78, pour
    *sanctificavit*), « Eaint-Esprit » (p. 90), « Les fille de Tyr » (p. 76), « Rendons grâce à Dieu » (p. 92),
    « Vous. Seigneur » (p. 92), « Deuxieme », « Troisieme » sans accent ; Pater de la p. 72 « Et ne nous induisez pas
    en tentation » et de la p. 90 « Et ne nous laissez pas succomber à la tentation » (la p. 90 est retenue, l'autre
    notée). Lectures douteuses de Matines : ponctuation effacée après « Saint-Esprit » (Gloria de l'invitatoire, p. 62)
    et après « ô Dieu » (premier verset du *Te Deum*, p. 96), rendues par deux-points et virgule ; répons *Missus est*
    (p. 100) sous une impression tachée, lettres restituées par le contexte (liste dans le champ `lecture`).
- Méthode : texte ABBYY d'archive.org et Tesseract (fra, `--psm 6`) comparés mot à mot à la transcription, puis chaque
  page française (images n37 à n59) relue sur l'image. Lectures sous une impression abîmée, sûres par le contexte :
  « Que vou[s] destinez … à toutes les n[ati]ons » (p. 42), « l'hér[i]tage céleste », « temple [d]e », « chastes
  [e]ntrailles », « les n[a]tions » (p. 44), « bien[h]eureuse » (p. 46), « s'est [l]evée », « digne de v[o]us louer »
  (imprimé « veus », p. 52) ; « prît » (p. 46) vérifié à l'agrandissement. Gardés tels qu'imprimés : « Que le grâce de
  Dieu » (p. 54, renvoi), répons marqué ℣ (p. 54), « J.-C N.-S. » (p. 54), « de la grandeur » pour *agnitionis* (p. 40).
- `engine/office/test_parvum_fr.py` : contrôle de l'alignement (nombre d'entrées, empreintes du latin, statuts).

## 5. Ce qui reste

1. Petit office : **12 paragraphes restent « à transcrire »**, faute d'un scan lisible : la prise de vue de la microfiche
   coupe la marge droite ou l'impression est effacée, et il manque des mots entiers. Ouverture de Laudes (46, 63) et
   psaume 92 avec ses antiennes (47, 66, 71, 80), p. 108 (image n112) ; psaume 125 de None (137, 145, 149), p. 170
   (n174) ; psaume 126 de None (138), p. 172 (n176) ; oraison de Prime « De la Purification à l'Avent » (162), p. 146
   (n150) ; oraison de Sexte (174), p. 168 (n172). archive.org n'a pas d'autre exemplaire de cette édition ; il faut un
   autre scan (Canadiana, BAnQ) ou l'imprimé.
2. Décider comment représenter un paragraphe latin qui a deux traductions selon le contexte (para. 12) : soit une
   variante par heure dans `parvum-fr.json`, soit dédoubler le paragraphe dans `parvum.py`.
3. Brancher l'affichage (chargeur dans `app/src/lib/office/parvum.ts`, `seed.mjs`, test mot pour mot) quand l'office
   entier sera transcrit, ou heure par heure si l'utilisateur le préfère.
4. Bréviaire : Fillion + Hugueny validés par l'utilisateur (22 nov., § 6) ; psautier de Fillion en cours (§ 6) ;
   retrouver le fascicule 8 du Propre du temps d'Hugueny (liberius.net).
5. Froment 1893 : chercher un scan libre (Gallica, Google Livres).

## 6. Bréviaire : décision et psautier de Fillion (22-23 novembre)

**Décision de l'utilisateur (22 nov.)** : Fillion pour les psaumes, Hugueny pour tout le reste (REFONTE § 5.5).

### Fait : `data/office/breviaire-fr/psautier-fillion.json` (non branché)

- Source complète en tête du fichier (ouvrage, 7e édition « soigneusement revue », Lecoffre-Gabalda 1917, *Nihil obstat*
  H. Garriguet, *Imprimatur* Paris 4 juin 1912 P. Thomas, vus sur les images n8-n9 ; URL ; pages), méthode, alignement.
- Chaîne rejouable `engine/recueils/relecture/fillion/` : `prep.py` (filet des notes, zone du texte, Tesseract fra
  `--psm 6`), `brouillon.py` (lectures ABBYY et Tesseract alignées ligne à ligne et mot à mot, désaccords numérotés),
  `decisions.txt` (choix par désaccord, structure des versets, renvois, remarques ; chaque page marquée `ok` a été relue
  entière sur l'image), `appliquer.py` → `pages/p<NNN>.txt` (pages relues, versionnées), `assembler.py` → JSON.
- **Fait : l'office du dimanche entier (pp. 13-97), les Complies de toute la semaine, et le lundi de Matines à None
  (pp. 99-151)**, soit 54 psaumes et 7 cantiques, **959 versets** : Ps 1-20, 23, 26-33, 46, 50, 53, 60, 62, 69, 70,
  76, 85, 87, 90, 92, 94, 99, 102, 109-113, 116, 117, 118, 133, 148 ; cantiques des trois jeunes gens (Dan. 3, 57-88
  et 56 ; Dan. 3, 52-57), de Zacharie, de la sainte Vierge, de Siméon, de David (I Par. 29, 10-13), d'Isaïe (Is. 12).
  Les Vêpres du lundi commencent p. 151 (Ps 114, 3 versets relus sur 9 : en attente, non livré).
- Numéros des versets : ceux de la Vulgate, pris dans l'ordre du latin de DO (`Psalterium/Psalmorum/PsalmN.txt`), et
  vérifiés contre l'imprimé (même nombre de versets, sinon l'assemblage s'arrête). Fillion numérote les secondes parties
  des Ps 9 (« Ut quid, Domine », hébr. 10) et 113 (« Non nobis », hébr. 115) à partir de 1 : numéros de la Vulgate
  donnés, avec une note. Ps 94 (invitatoire) : DO chante le texte du psautier romain, Fillion traduit la Vulgate
  (11 versets contre 10) : numérotation de Fillion, sans alignement ligne à ligne. Benedicite : DO chante deux versets
  par ligne : numéros de Fillion ; la doxologie (« Bénissons le Père… ») est imprimée avec le v. 88.
- Alignement : `lignes_la` (étiquettes des lignes latines de DO, « 2a », « 2b »…) et `ligne_la` (ligne où le verset
  commence) ; `engine/office/test_psautier_fr.py` vérifie, pour chacun des 365 paragraphes « Psalmus N(a-b) » du latin
  livré qui portent un psaume fait, que le nombre de lignes latines égale le nombre d'étiquettes. Un verset que DO laisse
  au milieu d'une ligne (Ps 76, 16) est rattaché à cette ligne.
- Graphies et lectures gardées ou notées (champ `lecture` du verset, 28 versets) : « Seigueur » (Ps 23, 8),
  « environnné » (Ps 114, 3), « jusqu'a » (Ps 17, 7), « rejoui » (Ps 29, 2), « c'est elie » (Ps 26, 4 : l brisé, lu
  « elle ») ; « à » initial perdu par les deux lectures et vu sur l'image (Ps 18, 12 ; Ps 30, 20) ; notes manuscrites au
  crayon dans les marges (Ps 3, 4 ; Ps 17, 29 et 47), non reprises ; « Émigre » (Ps 10, 2), « j'ai désire »
  (Ps 118, 40), « Mon àme » (Ps 102, 2 : accent imprimé grave, circonflexe brisé ?) ; t italiques lus l par l'OCR
  (« retentit », Ps 117, 15 ; « atteint », Ps 70, 19 ; « s'étend », Ps 102, 17) ; points ou traits parasites non repris
  (« tomber,. », Ps 117, 13 ; « Seigneur,. », Ps 118, 174 ; « qui. était », Ps 112, 9 ; « pitié ?- », Ps 76, 10 ;
  « car. j'ai », Ps 85, 3 ; « -Selon », Ps 11, 9) ; note manuscrite au crayon dans la marge (Ps 3, 4), non reprise ;
  « siècles » sous une tache (Dan. 3, 53). Découpage de l'imprimé gardé quand Fillion place un numéro autrement que DO
  (Ps 60, 4 ; Ps 70, 16 et 19). Renvois typographiques (« [fin » imprimé à droite d'une ligne voisine, au-dessus ou
  au-dessous) remis à leur place.
- Mise en forme : un verset sur une ligne (les vers du parallélisme réunis) ; espace avant « ; : ? ! » uniformisée ;
  italiques (mots ajoutés pour le sens) et petites capitales non marqués ; notes de Fillion non reprises.

### Fait le 26-27 novembre : jeudi, vendredi, samedi ; psautier complet

- **Jeudi** (pp. 297-363) : Ps 61, 65, 67, 68, 97, 89, 35, 146, 22, 71-75, 132, 135-137 ; cantiques de Jérémie
  (Jer. xxxi, 10-14) et de Moïse (Exod. xv, 1-19). **Vendredi** (pp. 371-443) : Ps 77-84, 86, 88, 98, 142, 147, 21,
  138-141 ; cantiques d'Isaïe (Is. xlv, 15-26) et d'Habacuc (Hab. iii, 2-19). **Samedi** (pp. 451-519) : Ps 104-108,
  149, 91, 63, 150, 93, 101, 103, 143, 144 ; cantiques de l'Ecclésiastique (Eccli. xxxvi, 1-16) et de Moïse
  (Deut. xxxii, 1-43). Les hauts des pp. 363, 443 (Ps 141 entier) et 519 sont relus.
- Bilan : **150 psaumes, 17 cantiques, 2684 versets** ; `test_psautier_fr.py` : 867 paragraphes « Psalmus » du latin
  livré contrôlés, aucun psaume sans français. Le symbole *Quicumque* (Prime du dimanche, `Psalm234` de DO) n'est pas
  imprimé par Fillion : à prendre chez Hugueny.
- Cantiques que DO coupe autrement que Fillion (Jérémie, Moïse ×2, Isaïe xlv, Habacuc) : numéros de Fillion, sans
  alignement ligne à ligne (note dans chaque pièce) ; l'Ecclésiastique suit les 16 lignes de DO. Habacuc : Fillion titre
  « iii, 1-19 » mais numérote 2-19.
- Numérotation : Ps 132, Fillion compte 4 versets (la Vulgate 3) : numéros de Fillion, le v. 3 rattaché à la ligne
  latine « 2b » ; Ps 147, Fillion numérote 12-20 (hébreu) : numéros de la Vulgate 1-9, avec une note ; Ps 108, 22 :
  « Délivrez-moi, » (fin du v. 21 chez Fillion) compté au v. 22, comme le latin de DO (« Libera me ») ; Ps 68, 20-21,
  Ps 72, 2 et 5, Ps 88, 9 : numéros que les deux lectures avaient perdus, rétablis sur l'image ; numéros
  imprimés au milieu d'une ligne (Ps 97, 9 ; Ps 89, 12 ; Ps 82, 12) : découpage de l'imprimé gardé.
- Lectures notées (champ `lecture`, 83 versets en tout) : « evanouis » sans accent (Ps 89, 9) ; « langue à parcouru »
  (Ps 72, 9) ; « il » brisé (Ps 71, 12) ; « avez » brisé (Ps 73, 15) ; trace au-dessus de « votre » (Ps 73, 11) ;
  « fleuves » sous une tache (Ps 88, 26) ; « voi[-]sins » sans trait d'union (Ps 79, 7) ; ponctuation effacée après
  « instruit » (Ps 93, 12 : virgule retenue) ; « humiliation. car » (Ps 135, 23) ; « les fabricants ; [d'erreurs. »
  (Is. xlv, 16 : point-virgule non repris) ; « extrêmement » sans ponctuation en bout de ligne (Ps 106, 38) ; accents
  et traits parasites non repris (Ps 77, 39 ; Ps 78, 1 ; Ps 107, 11 ; Ps 103, 33 ; Ps 138, 8). Graphies modernisées sur
  l'image seulement quand l'imprimé porte l'accent (« Égypte », « instruisît », « apprît », « nourrît ») ; « Il » lu
  « ]l » ou « II » par l'OCR rétabli.
- `assembler.py` : nouveaux cantiques (`CANTIQUES`), Ps 132 (`DECOUPE`), Ps 147 (`NOTES`).

### Reste (psautier)

- Brancher le psautier (chargeur, affichage en regard du latin, test mot pour mot), avec Hugueny pour le reste.
- Relire, si l'utilisateur le souhaite, les versets marqués `lecture` (points douteux ci-dessus et au § 6).

Renvois typographiques : `appliquer.py` remet chaque « [fin » à la ligne qu'il complète (règle écrite dans la fonction
`renvois`), vérifiée sur chaque page relue ; les cas ambigus (`AMBIGUS=1`) ont été revus (renvoi « [du chaume. » du
cantique de l'Exode corrigé à la main).

### Hugueny : table des fascicules (archive.org, scans de la Bibliothèque Saint Libère, 2014)

Pages de titre lues sur la couche texte, et sur l'image quand elle était douteuse (Propre du temps IV, XI-XIV ; Propre
des saints 3). Toutes portent « LABERGERIE, PARIS » et la mention « © Bibliothèque Saint Libère 2014. Toute reproduction
à but non lucratif est autorisée ».

| Identifiant archive.org | Contenu |
|---|---|
| `le-breviaire-romain-000001439` | Corps du Bréviaire : Ordinaire, Psautier, Commun des saints (« Textes latins et français », « Psallite sapienter » ; *Imprimatur* Paris 1934 ; nouvelle éd. 1947) |
| `le-breviaire-romain-propre-du-temps-fascicule-1-000001180` | Propre du temps I : du Ier dimanche de l'Avent à la vigile de la Nativité |
| `…-propre-du-temps-fascicule-2-000001181` | II : de Noël (25 décembre) à la vigile de l'Épiphanie |
| `…-propre-du-temps-fascicule-3-000001182` | III : de l'Épiphanie (6 janvier) au IIe samedi après l'Épiphanie |
| `…-propre-du-temps-fascicule-4-000001183` | IV : du IIIe dimanche après l'Épiphanie au samedi avant la Quinquagésime (comprend la Septuagésime) |
| `…-propre-du-temps-fascicule-5-000001184` | V : de la Quinquagésime au samedi avant le IVe dimanche de Carême |
| `…-propre-du-temps-fascicule-6-000001185` | VI : du samedi avant le IVe dimanche de Carême au mercredi de la Semaine sainte |
| `…-propre-du-temps-fascicule-7-000001186` | VII : du Jeudi saint au samedi de la semaine de Pâques |
| — | **VIII : absent d'archive.org** (par déduction : du dimanche *in albis* au samedi avant le IVe dimanche après Pâques) |
| `…-propre-du-temps-fascicule-9-000001188` | IX : du IVe dimanche après Pâques au samedi, vigile de la Pentecôte |
| `…-propre-du-temps-fascicule-10-000001189` | X : du dimanche de la Pentecôte au jeudi, octave du Saint-Sacrement |
| `…-propre-du-temps-fascicule-11-000001190` | XI : de la fête du Sacré-Cœur au samedi de la VIe semaine après la Pentecôte |
| `…-propre-du-temps-fascicule-12-000001191` | XII : du VIIe dimanche après la Pentecôte au samedi avant le IIIe dimanche d'août |
| `…-propre-du-temps-fascicule-13-000001192` | XIII : du IIIe dimanche d'août au samedi avant le IIIe dimanche d'octobre |
| `…-propre-du-temps-fascicule-14-000001193` | XIV : du IIe dimanche d'octobre au samedi de la Ve semaine de novembre (titres tels qu'imprimés, XIII et XIV se chevauchent) |
| `le-breviaire-romain-propre-des-saints-fascicule-1-000001194` | Propre des saints 1 : de S. Clément Ier (23 novembre) à S. Thomas apôtre (21 décembre) |
| `…-propre-des-saints-fascicule-2-000001195` | 2 : de S. Hilaire (14 janvier) à S. Jean de Matha (8 février) |
| `…-propre-des-saints-fascicule-3-000001196` | 3 : de S. Cyrille d'Alexandrie (9 février) à S. Benoît abbé (21 mars) |
| `…-propre-des-saints-fascicule-4-000001197` | 4 : de S. Gabriel archange (24 mars) à Ste Catherine de Sienne (30 avril) |
| `…-propre-des-saints-fascicule-5-000001198` | 5 : de S. Philippe et S. Jacques (1er mai) à S. Bède le Vénérable (27 mai) |
| `…-propre-des-saints-fascicule-6-000001199` | 6 : de S. Augustin de Cantorbéry (28 mai) à SS. Jean et Paul (26 juin) |
| `…-propre-des-saints-fascicule-7-000001200` | 7 : du IVe jour dans l'octave de S. Jean-Baptiste (27 juin) à S. Alexis (17 juillet) |
| `…-propre-des-saints-fascicule-8-000001201` (et doublon `…_202302`) | 8 : de S. Camille de Lellis (18 juillet) à la Transfiguration (6 août) |
| `…-propre-des-saints-fascicule-9-000001202` | 9 : de S. Gaétan (7 août) à S. Joseph Calasanz (27 août) |
| `…-propre-des-saints-fascicule-10-000001203` | 10 : de S. Augustin (28 août) aux Stigmates de S. François (17 septembre) |
| `…-propre-des-saints-fascicule-11-000001204` | 11 : de S. Joseph de Cupertino (18 septembre) au Saint Rosaire (7 octobre) |
| `…-propre-des-saints-fascicule-12-000001205` | 12 : de Ste Brigitte (8 octobre) à la vigile de la Toussaint (31 octobre) |
| `…-propre-des-saints-fascicule-13-000001206` | 13 : de la Toussaint (1er novembre) à son octave, et l'office des morts |
| `…-propre-des-saints-fascicule-14-000001207` | 14 : offices des dédicaces et saints du 9 au 22 novembre |
| `le-breviaire-romain-supplement-1-000001208` | Supplément I : bulles de Pie V et Pie X, divisions de l'année liturgique, rubriques générales du Bréviaire |
| `le-breviaire-romain-supplement-2-000001209` | Supplément II : sept psaumes de la pénitence, litanies des saints, bénédiction de la table, prières pour le voyage, préparation à la messe et action de grâces, litanies approuvées, bénédictions diverses |

Le Propre des saints du 1er au 13 janvier (S. Hilaire ouvre le fascicule 2) est sans doute dans le fascicule 2 du Propre
du temps (Noël à l'Épiphanie), à vérifier. Couche texte : Tesseract (`fra+Latin`), colonnes latin et français
entremêlées : la transcription demandera le même travail que pour Fillion (découpe des colonnes, relecture sur l'image).
