# Sources réellement utilisées

## Étape 1 — Données

| Source | Édition | Usage | Accès |
|---|---|---|---|
| **Divinum Officium** (données) | dépôt GitHub, version « Divino Afflatu - 1954 » ; tables `Kalendaria` 1570 → 1954, `Transfer`, rangs `[Rank]`, `horas/*/Martyrologium`, `missa/*` | calendrier, rangs, commémoraisons, Introït, Martyrologe (latin et français) | https://github.com/DivinumOfficium/divinum-officium (clone partiel dans `vendor/do`, non versionné) |
| ***Missale Romanum*** | édition typique, 1920 | stations romaines (relevé repris de `moteur/stations.py`) | archive.org `000missaleromanum-1920` |
| **Code de droit canonique** | 1917, can. 1247, 1250-1254 | jeûne et abstinence | — |
| ***Le Jardin de l'âme*** | livret validé, 84 p. | 62 pièces extraites mot pour mot vers `data/prieres/jardin.json` | `docs/livret/source/*.tex` |
| ***Calendrier liturgique 2026-2027*** | calendrier papier validé | référence de contrôle du moteur (364 jours) ; plan des dévotions | `data/source/calendrier_2026-2027.json` |

## Étape 8 — Textes recopiés (relus sur le scan de chaque page)

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Prière du matin (avec Pater, Ave, Credo, Confiteor en latin ; actes de foi, d'espérance et de charité) | *Paroissien romain*, Tours, A. Mame et fils, 1890 | 7-12 | archive.org `paroissienromain00tour` |
| Angélus (français et latin, oraison) | idem | 16-17 | idem |
| Prière du soir (avec examen de conscience) | idem | 18-23 | idem |
| Salve Regina et Sub tuum, avec leurs versets et leurs indulgences (Pie VI, 5 avril 1786) | Beringer, *Les Indulgences*, t. I, n° 429, Paris, Lethielleux, 1925 | 224-225 | archive.org `lesindulgences0001beri` |
| Prière pour les défunts : psaume *De profundis* (latin et français), versets, oraison | *Paroissien romain*, Mame, 1890 (coquille « ea omnibus » corrigée en « ex omnibus », signalée dans la fiche) | 26-27 | archive.org `paroissienromain00tour` |
| Chapelet des Morts : manière de le réciter, origine, indulgences (réservées aux associés de N.-D. du Suffrage) | Beringer 1925, t. II, n° 306 a | 322-323 | archive.org `lesindulgences0002beri` |
| Cordon de saint Joseph : pratique des sept *Gloria Patri*, indulgences de l'archiconfrérie de Rome | Beringer 1925, t. II, n° 266 | 256-257 | idem |
| *Gloria Patri* (français et latin) | Beringer 1925, t. I, n° 238 et note 1 | 130 | archive.org `lesindulgences0001beri` |
| Litanies du saint Nom de Jésus, avec l'oraison | *Paroissien romain*, Mame, 1890 | 13-16 | archive.org `paroissienromain00tour` |
| Litanies de la sainte Vierge | idem | 23-25 | idem |
| Litanies des Saints, avec l'oraison | idem | 61-66 | idem |
| Litanies du Sacré-Cœur (latin et français), indulgence (Léon XIII, 2 avril 1899) | Beringer 1925, t. I, n° 377 (répons en accolade répété à chaque invocation ; « savientiæ » corrigé) | 186-188 | archive.org `lesindulgences0001beri` |
| Litanies de saint Joseph (latin et français), indulgence (Pie X, 18 mars 1909) | Beringer 1925, t. I, n° 487 (répons en accolade répété) | 258-259 | idem |
| A saint Joseph pour obtenir la vertu de pureté (français, latin en note), indulgence (Pie IX, 1877) | Beringer 1925, t. I, n° 480 | 252 | idem |
| Regina Cæli (latin et français, oraison, indulgences) ; remplace l'Angélus au temps pascal | Beringer 1925, t. I, n° 428 | 222-223 | archive.org `lesindulgences0001beri` |
| En l'honneur du Cœur affligé de Marie : prière entière et ses sept invocations, une par don du Saint-Esprit (un don par jour) | Beringer 1925, t. I, n° 450 | 237-238 | archive.org `lesindulgences0001beri` |

## Bréviaire romain (lot 9, 21 novembre 2026)

| Texte | Source | Accès |
|---|---|---|
| *Breviarium Romanum*, heures complètes (Matines à Complies), latin, chaque jour de l'année liturgique 2026-2027 | Divinum Officium, version « Divino Afflatu - 1954 » (rubriques de saint Pie X, 1911, avec les changements jusqu'en 1954, sans ceux de 1955 ni de 1960) ; texte produit par le moteur du site lui-même, exécuté hors ligne sur le dépôt épinglé (commit `454a86ea`) | https://github.com/DivinumOfficium/divinum-officium ; `engine/office/breviaire.py` → `data/office/breviaire/` |

Le français n'est pas donné : les fichiers français de DO ne disent pas leur édition (REFONTE § 5.5). Éditions bilingues
anciennes identifiées le 22 nov. (`docs/audits/BREVIAIRE_FRANCAIS_2026-11-22.md`) : Fillion, *Le nouveau psautier du
Bréviaire romain*, 7e éd., Lecoffre-Gabalda, 1917 (archive.org `lenouveaupsautie00gl`) pour les psaumes ; Hugueny, *Le
Bréviaire romain, textes latins et français*, Labergerie, 1934 (rééd. 1947 ; archive.org `le-breviaire-romain-000001439`
et fascicules) pour le reste ; choix confirmé par l'utilisateur le 22 nov.

| Texte | Source | Accès |
|---|---|---|
| Psautier du Bréviaire romain en français, psaume par psaume et verset par verset (numérotation de la Vulgate), avec les cantiques ; **psautier complet** (27 nov.) : les 150 psaumes et 17 cantiques (Laudes, *Benedictus*, *Magnificat*, *Nunc dimittis*), 2684 versets, office du dimanche au samedi (voir l'audit pour le détail) ; le symbole *Quicumque*, absent de Fillion, reste à prendre chez Hugueny ; données non branchées | L. Cl. Fillion, *Le nouveau psautier du Bréviaire romain, texte et traduction, avec notes succinctes*, 7e éd. « soigneusement revue », Paris, Lecoffre, J. Gabalda, 1917 ; *Nihil obstat* H. Garriguet, sup. s. s. ; *Imprimatur* Paris, 4 juin 1912, P. Thomas, v. g. ; traduction de la Vulgate (« au fond, celle de Sacy », revue) ; pages françaises impaires 13-531 ; double lecture (couche ABBYY d'archive.org, Tesseract fra), désaccords tranchés et chaque page relue sur l'image ; décisions rejouables `engine/recueils/relecture/fillion/decisions.txt` | archive.org `lenouveaupsautie00gl` (exemplaire de l'Université d'Ottawa, images n<page + 13>) → `data/office/breviaire-fr/psautier-fillion.json` ; contrôle `engine/office/test_psautier_fr.py` |

| Texte | Source | Accès |
|---|---|---|
| *Officium parvum B.M.V.*, français de toutes les heures (201 paragraphes alignés sur 224 de `data/office/parvum.json`, 12 illisibles sur le scan ; proposition non branchée) | *Petit office de la Sainte Vierge et des morts…*, Montréal, 1905, « Permis d'imprimer » de Mgr Zotique Racicot, aux. de Montréal, 4 juin 1905 ; latin-français en regard, traducteur non nommé ; pp. 10-180 ; double lecture (ABBYY, Tesseract) puis relecture de chaque page sur l'image | archive.org `cihm_98272` (images n11-n184, pages françaises) → `data/office/parvum-fr.json` ; contrôle `engine/office/test_parvum_fr.py` |

## Somme théologique (lot 10, 22 novembre 2026)

| Texte | Source | Accès |
|---|---|---|
| *Somme théologique*, Iª pars, q. 1 à 5 (30 articles), français | *Somme théologique de S. Thomas d'Aquin*, traduite en français et annotée par F. Lachat, Paris, Louis Vivès, 4e éd., 1880, t. I, p. 3-103 (même composition que l'exemplaire de 1874, Harvard/Google, utilisé en contrôle). Vote de quatre lectures (Tesseract et ABBYY, sur les deux scans) ; chaque ligne sans accord relue sur l'image (`engine/somme/corrections_fr.txt`) ; orthographe de l'édition gardée (« paroît », « connoître », « privilége ») ; notes de Lachat et paragraphes « (Conclusion. — …) » des éditeurs non repris | archive.org `sommetheologique01thom` (contrôle `sommethologique07lachgoog`) → `engine/somme/construire.py` → `data/somme/Ia-NN.json`, `index.json` |
| Même texte, latin | *Sancti Thomae Aquinatis Opera omnia iussu Leonis XIII*, t. IV, Rome, Typographia Polyglotta, 1888 ; texte de la transcription du Corpus Thomisticum (E. Alarcón), contrôlé par alignement sur la lecture ABBYY du scan léonin (`engine/somme/latin_controle.py`) ; écarts isolés vus sur l'image (`corrections_la.txt` : « etc. » rétabli, q. 5 a. 2) ; intitulés des questions et articles relus sur l'image (`titres_la.json`) ; ponctuation du Corpus Thomisticum | archive.org `operaomniaiussui04thom` ; https://www.corpusthomisticum.org/sth1001.html |
| *Somme théologique*, Iª pars, q. 6 à 11 (24 articles), français et latin | Même édition et même méthode (Lachat, Vivès 1880, t. I, p. 104-180 ; latin léonin du Corpus Thomisticum contrôlé sur le scan de 1888) ; chaque ligne relue sur l'image de 1880 (lignes douteuses aussi sur celle de 1874) ; écarts latins vus sur l'image : q. 6 a. 4 « per se ens » (le Corpus Thomisticum donne « bonum »), q. 12 a. 3 « etc. » | idem |

Points laissés tels qu'imprimés (Lachat) : « Ici se présente dix questions » (q. 1), « 2. » pour « 2° » (q. 3 a. 4,
obj. 2), deux réponses numérotées « 3° » (q. 5 a. 3, la quatrième), « il y beaucoup de bien » (q. 5 a. 5, lettre tombée
à l'impression, même chose sur les deux exemplaires), « impartaite » (q. 4 a. 3), « consiste-elle » (q. 5). Le *Sed
contra* de la q. 1 a. 5 n'est pas traduit par Lachat : le latin est donné seul (note dans l'article). Le latin n'a pas été
relu mot à mot sur l'image : seuls les écarts isolés de l'alignement automatique l'ont été.

Iª q. 6-11 (25 nov.) : laissés tels qu'imprimés « Dieu est il-le souverain bien? » et « Dieu seul est-il-bon par essence? » (q. 6), réponse 1 numérotée « 2° » (q. 7 a. 2), « 5° » pour « 3° » (q. 10 a. 2, obj. 3, note dans l'article), « 3. » (q. 10 a. 4, rép. 3), « l'éternié » (q. 10 a. 3), « non-seulemnt » (q. 11 a. 3), « opposé ou multiple » (q. 11 a. 2). Numéros absents chez Lachat (marque « § » dans `corrections_fr.txt`, note dans l'article) : q. 6 a. 1 obj. 2, q. 7 a. 3 rép. 4, q. 11 a. 3 rép. 2. La q. 10 a. 1 n'a pas de *Sed contra* (léonine et Lachat). Mots abîmés sur les deux exemplaires, complétés par le contexte : voir `A_FOURNIR.md`.

## Étape 9 — Méditations et lectures

| Recueil | Édition | Usage | Accès |
|---|---|---|---|
| Hamon, *Méditations à l'usage du clergé et des fidèles pour tous les jours de l'année*, 3 t. | Paris, Victor Lecoffre ; Lyon ; t. I 1879 (10e éd.), t. II 1894 | 437 méditations découpées par jour (temporal, dates fixes, Sacré-Cœur, dimanches d'octobre, Dédicace) dans `data/recueils/hamon.json` ; texte OCR, coquilles possibles | PDF Google Livres fournis par l'utilisateur (`vendor/sources/hamon/`) |
| Chaignon, S. J., *La méditation, ou le fidèle sanctifié par la pratique de l'oraison mentale*, 3 t. | Paris, 1872 | 213 méditations : parcours de 95 méditations suivi dans l'ordre les jours ordinaires ; 118 pour l'année liturgique, dont 88 rattachées à un jour, proposées en second choix ; OCR relu à deux lectures, parcours (S:1-S:96) et méditations de l'Avent et du temps de Noël (24, hors parcours) relus sur le scan le 22 nov., coquilles possibles ailleurs | archive.org `lamditationoulef01chai`, `…02chai`, `…03chai` |
| *Breviarium Romanum*, leçons du IIe nocturne (IV-VI) du sanctoral, latin et traduction française | rubriques de 1911 (Divino Afflatu), données Divinum Officium ; la leçon abrégée de 1960 est écartée | 322 offices, dont 277 avec le français, dans `data/recueils/breviaire.json` ; page « Office du jour et vie du saint » | dépôt Divinum Officium (`vendor/do`) |
| Dom Guéranger, *L'Année liturgique*, 15 vol. (continuée par Dom Fromage) | Tours, Mame, 1911 | 423 lectures (93 jours du temporal, 270 dates de saints) dans `data/recueils/gueranger/` ; lecture du jour sous la méditation et notice sur la page du saint ; OCR, coquilles possibles (t. 8 : 2 avril et 5 avril relus sur le scan le 22 nov.) ; des féries d'Avent et la semaine de Pâques manquent (intitulés illisibles) | archive.org `lanneliturgiqu01gu` … `lanneliturgiqu15gu` ; texte propre pour 202 lectures : https://www.domgueranger.net/lannee-liturgique/ et https://abbe-pivert.com/dom-gueranger-annee-liturgique/ (pièces latines omises) |
| Lefebvre, S. J., *Mois de saint Joseph* (mars) | 1890 | 31 jours, en tête de la méditation en mars | archive.org `moisdesaintjosep00lefe` |
| Lefebvre, S. J., *Mois de Marie : contemplations sur trente mystères* (mai) | 1888 | 31 jours (le 28 très court : coupure de l'OCR) | archive.org `moisdemarieconte00lefe` |
| Lefebvre, S. J., *Mois du Sacré-Cœur* (juin) | 1869 | 29 jours (le 23 manque, le 21 est tronqué) | archive.org `moisdusacrecoeur00lefe` |
| Berlioux, *Mois des âmes du purgatoire, méditations pratiques pour chaque jour* (novembre) | 1888 | 30 jours, **relus sur les scans** (14 nov. 2026) : double OCR comparée mot à mot, 454 désaccords tranchés sur l'image, p. 164 recopiée ; méthode dans `engine/recueils/relecture/` | archive.org `moisdesamesdupur00berl` |
| Boylesve, S. J., *Le mois du Précieux Sang de N.-S. Jésus-Christ* (juillet) | Saint-Hyacinthe, 1882 (imprimatur du 30 mai 1882) | 31 jours, **recopiés page par page sur le scan** (contrôle par une seconde lecture OCR) ; `data/recueils/transcriptions/boylesve-precieux-sang.txt` | archive.org `cihm_41458` |

## Textes ajoutés le 14 novembre 2026 (relus sur le scan)

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Litanies du très-saint Sacrement, avec l'oraison | Spitz, *Le Fervent chrétien*, 4e éd., Einsiedeln, Benziger, 1868 (approbations des évêques de Bâle et de Strasbourg) | 169-172 | archive.org `leferventchretie00spit` |
| Litanies de la très-sainte Trinité, avec la prière | idem | 430-432 | idem |
| Litanies de l'Ange gardien, avec la prière | idem | 579-580 | idem |
| Roues symboliques : listes et versets | Vulgate clémentine ; *Catéchisme de saint Pie X* ; Bréviaire romain (S. Grégoire, 29 sept., neuf chœurs) ; Paroissien 1890 ; *Jardin de l'âme* | — | `engine/roues/construire.py` |

## Textes ajoutés le 21 novembre 2026 (relus sur l'image du scan, en attente de validation)

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Petite prière du Cœur agonisant de Jésus, à dire après l'Angelus (`apostolat1864:coeur-agonisant`) | Ramière, *Petit manuel de l'Apostolat de la prière*, 1re éd. canadienne d'après la 4e éd. française, Montréal, J.-B. Rolland et fils, 1864 ; approbation de Mgr Bourget | 106-107 (règle de l'Angelus p. 138) | archive.org `cihm_39977` (pages n121, n122, n153) |
| « O mon Jésus, pardonnez-nous nos péchés ! délivrez-nous du feu de l'enfer !… » (Fatima, forme de 1943, `castelbranco1943:o-mon-jesus-fatima`) | J. Castelbranco, *Le miracle inouï de Fatima*, Montréal, 1943 ; imprimatur du 5 juin 1943 | 38 (et 47) | archive.org `lemiracleinouide00cast` (pages n39, n48 ; imprimatur n3) |
| « Ô mon Jésus, pardonnez-nous nos péchés… », forme courante (fin de dizaine ; décision de l'utilisateur du 22 nov.) | FSSPX Actualités, « Ô mon Jésus, pardonnez-nous nos péchés », 12 juillet 2019 (site admis pour les prières courantes) | — | https://fsspx.news/fr/news/o-mon-jesus-pardonnez-nous-nos-peches-22114 |

## Manuels d'archiconfréries en français (22 novembre 2026, non branchés au programme)

Double lecture (couche texte du scan et Tesseract `fra`), désaccords et fins de page tranchés sur l'image ; audit et
proposition d'intégration : `docs/audits/ARCHICONFRERIES_FR_2026-11-22.md`.

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Litanies de la sainte Face tirées de l'Écriture (latin-français), consécration à l'usage des membres, acte d'amour, deux actes de réparation, louanges de la sainte Face, louanges au saint Nom de Dieu, couronnes du saint Nom de Dieu et du saint Nom de Jésus, sept Ave à la Mère de douleurs (`janvier:*`, 10 pièces) | Abbé P.-D. Janvier, *Manuel de l'Archiconfrérie de la Sainte-Face*, 3e éd., Tours, Bureau de l'Oratoire, 1895, approuvé par le cardinal Meignan | 143-150, 160-166, 178-180, 234-237, 245 | bibliotheque-catholique.com (PDF Google) |
| Exercice de louanges pour chaque jour de la semaine (saint Alphonse), consécration des œuvres de la journée, oraison pour se consacrer au sacré Cœur de Marie, litanies du saint Cœur de Marie, prière d'une mère, prière pour le salut de la France (`desgenettes:*`, 6 pièces) | Dufriche-Desgenettes, *Manuel d'instructions et de prières… de l'Archiconfrérie du très-saint et immaculé Cœur de Marie*, 13e éd., Paris, Sagnier et Bray, 1852 ; statuts autorisés par Mgr de Quélen, 16 déc. 1836 | 435-453 | archive.org `manueldinstruct00dufrgoog` |
| Offrande de l'Heure de Garde, très précieuse Offrande, acte d'oblation, adoration réparatrice, rénovation de l'enrôlement, prière au Cœur blessé par la lance, amende honorable, prière à Marie au pied de la Croix, prière réparatrice, consécration au Cœur de Jésus (`garde1886:*`, 10 pièces) | *Manuel de l'Archiconfrérie de la Garde d'Honneur du Sacré Cœur de Jésus*, 9e éd., Bourg-en-Bresse, Monastère de la Visitation, 1886 ; approbation de l'évêque de Belley, 23 mars 1883 | 131-151 | Google Livres `YxAtAYVrCuwC` (copie PDF du même scan : saint-eugene.net) |

## Manuels d'archiconfréries en anglais (22 novembre 2026, relus sur l'image, à valider)

Décision de l'utilisateur du 22 nov. ; détail, tables des matières et proposition d'intégration :
`docs/audits/ARCHICONFRERIES_EN_2026-11-22.md`. Le français ancien est pris quand il existe ; sinon traduction de travail
marquée (`traduction`), original anglais gardé (`anglais`), aucune indulgence comptée.

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Pour une bonne mort (« Jésus, mon Seigneur, Dieu de bonté… », avec la prière au Père éternel) (`beringer:pour-une-bonne-mort`) ; même prière que les « Invocations for a Good Death » de la Bona Mors et que les litanies données d'après Le Petit Sacristain | Beringer 1925, t. I, n° 582 | 310-312 | archive.org `lesindulgences0001beri` (images n325-n327) |
| Pour les âmes du purgatoire, une prière par jour de la semaine (`beringer:ames-purgatoire-*`, 7 pièces) ; équivalent des « Prayers for the whole week » du *Purgatorian Consoler* | Beringer 1925, t. I, n° 615 (« Je uous salue » corrigé) | 323-324 | idem (n338-n339) |
| A la Sainte Famille (`beringer:a-la-sainte-famille`) | Beringer 1925, t. I, n° 298 | 151 | idem (n166) |
| Acte de consécration de l'Association de la Bonne Mort (`lefebvre1870:acte-de-consecration-bonne-mort`) | Al. Lefebvre, S. J., *La science de bien mourir, manuel de l'Association de la Bonne Mort*, 5e éd., Paris, Librairie Saint-Germain-des-Prés, 1870 | 401-402 | archive.org `lasciencedebienm00lefeuoft` (n416-n417) |
| Petit chapelet du précieux Sang, avec l'oraison « O Sang très-précieux » et l'oraison *Omnipotens* (`boylesve1882:petit-chapelet-precieux-sang`) | [Boylesve], *Le mois du Précieux Sang*, Saint-Hyacinthe, 1882 (lettres retournées corrigées, liste dans la fiche) | 42-43, 48-49 | archive.org `cihm_41458` (n43-n44, n49-n50) |
| Cordon de saint François : les six *Pater*, *Ave* et *Gloria* (`cordon1876:six-pater-ave-gloria`) | *Le Cordon de saint François d'Assise*, Québec, imprimatur du 2 déc. 1876 († E. A. [Taschereau]) | 2-3 | archive.org `cihm_10448` (n6-n7) |
| **Traduction de travail** : réflexions sur la mort, du dimanche au samedi (`bonamors1896:reflexion-*`, 7 pièces) | *The Manual of the Bona Mors Confraternity*, New York, Apostleship of Prayer, 1896, imprimatur de Mgr Corrigan | 33-34 | archive.org `manualofbonamors00unse` (n44-n45) |
| **Traduction de travail** : courtes prières en disant les *Pater* (`cordon1878:courtes-prieres`) | *Manual of the Arch-Confraternity of the Cord of S. Francis*, Londres, Burns & Oates, 1878, imprimatur du 21 fév. 1878 | 35, 37 | archive.org `ManualCordOfSFrancis` (n45) |
| **Traduction de travail** : acte de consécration à Jésus, Marie, Joseph (`saintefamille1875:acte-de-consecration`) | *Manual of the Arch-Confraternity of the Holy Family*, [Québec], 1875 ; statuts approuvés par l'évêque de Liège, 29 juil. 1850 | 44-45 | archive.org `manualofthearchc00unknuoft` (n47-n48) |

Manuels consultés sans pièce ajoutée : *The Book of the Confraternity of the Precious Blood*, Londres, 1850 (rescrit de
Pie IX, 12 août 1850 ; `TheBookOfTheConfraternity`) et Caswall, *Confraternity Manual of the Most Precious Blood*,
Londres, 1861 (`ConfraternityManualOfThe`) ; *Purgatorian Consoler*, Baltimore, 1868 (`purgatorianconso00queluoft`) ;
*Manual of the Confraternity of Our Lady of Perpetual Help*, New York, [19..] (`manualofconfrate00arch`) ; Janvier,
*Manual of the Archconfraternity of the Holy Face* (`manualofthe-archconfraternityofthe-holy-face`) ; Beringer 1925,
t. II, n° 230, 234, 255, 262, 272, 306, 308 (sommaires français des archiconfréries) ; *Enchiridion* 1952, n° 594, 636-649
(contrôle, sur l'OCR).

## Manuels d'archiconfréries, lot A (25 novembre 2026, relus sur l'image, non branchés)

Double lecture (couche texte ABBYY d'archive.org et Tesseract `fra+lat`, `--psm 6`), désaccords tranchés sur l'image
de la page, puis contrôle des mots de chaque pièce absents des deux lectures ; orthographe de l'édition gardée.
Indulgences imprimées reportées sans être comptées. Détail, tables des matières, pièces laissées et proposition
d'intégration : `docs/audits/ARCHICONFRERIES_LOT_A_2026-11-25.md`.

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Messe pour demander la grâce d'une bonne mort, litanies de la Passion, deux litanies de N.-D. des Sept-Douleurs, litanies de saint Joseph, prière pour les agonisants (recommandation de l'âme), protestation pour bien mourir (S. Alphonse), deux testaments spirituels (S. Charles et autre formule), prière de S. Vincent Ferrier (latin-français), prière contre la mort subite, prière de sainte Gertrude *Ave candidum lilium*, deux prières à saint Joseph, *Ave Joseph*, prières à saint Michel et à l'ange gardien, prières pour les associés vivants, agonisants et décédés (`lefebvre1870:*`, 20 pièces) | Al. Lefebvre, S. J., *La science de bien mourir, manuel de l'Association de la Bonne Mort*, 5e éd., Paris, Librairie Saint-Germain-des-Prés, 1870 | 412-466 | archive.org `lasciencedebienm00lefeuoft` (n427-n481) |
| Consécration à Notre-Seigneur au Saint-Sacrement (réception), amende honorable au Sacré Cœur, acte d'offrande et de consécration au Sacré-Cœur avec *O Cor Jesu, amoris victima*, formule de l'acte héroïque « O Marie, Mère de miséricorde » (`picard1873:*`, 4 pièces) | [E. Picard], *Petit manuel des Associés de l'Union de prières et de la Bonne Mort*, Montréal, E. Senécal, 1873 | 14-31 | archive.org `cihm_04796` (n12-n29) |
| Horloge de la Passion (24 jaculatoires), chapelet du Précieux-Sang avec considérations et prières, chapelet de la Divine Miséricorde, prière pour la délivrance des âmes du purgatoire (« Ayez pitié, ô tendre Jésus »), offrande du Précieux Sang au Père éternel pour obtenir sa bénédiction, consécration au Précieux Sang, prière de sainte Catherine de Sienne (`precieuxsang1890:*`, 7 pièces) | *Nouveau manuel du Très-Précieux Sang… ou le Livre des élus*, Saint-Hyacinthe, Monastère du Précieux-Sang, 1890 ; approbation de L.-Z. Moreau, 18 déc. 1889 | 193-200, 231-239, 266, 350-355, 556 | archive.org `cihm_92923` |
| Amende honorable au Très Saint-Sacrement (« Pardon, Seigneur, pardon »), consécration au Sacré-Cœur pour les associés, heure d'adoration dialoguée (actes de religion, de remerciement, de charité, de contrition), prière fondée sur les promesses du Sacré-Cœur, prière pour la communion quotidienne, acclamations, amende honorable à Jésus-Christ présent dans le Sacrement de l'autel, consécration du genre humain (Léon XIII) (`ndchemin1920:*`, 8 pièces) | *Petit manuel des adorateurs et des adoratrices du Très Saint Sacrement*, Québec, Notre-Dame du Chemin, 1920 | 14-52 | archive.org `cihm_78894` |
| Consécration de l'Archiconfrérie, douze invocations, sept prières générales (prière à réciter fréquemment, confiance, grâce de toujours prier, grâces nécessaires au salut, persévérance, bonne mort) et les trente « prières spéciales appropriées à toutes les demandes » avec leurs oraisons jaculatoires (secours en toutes choses, jaculatoires de la journée, tiédeur, vertu, amour divin… âmes du purgatoire) (`perpetuelsecours1878:*`, 38 pièces) | [Un Père rédemptoriste], *Notre-Dame du Perpétuel-Secours… son histoire, archiconfrérie et exercices de piété*, Montréal, J.-B. Rolland, 1878 | 143-205 | archive.org `cihm_52280` (images n146-n208) |

## Manuels d'archiconfréries, lot B (25-26 novembre 2026, non branchés au programme)

Double lecture (couche texte du scan et Tesseract ; colonnes latin-français lues séparément), chaque désaccord vu sur
l'image ; détail, tables des matières, pièces laissées et proposition d'intégration :
`docs/audits/ARCHICONFRERIES_LOT_B_2026-11-25.md`.

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Petit office ou Salutation du très saint Nom de Jésus (bienheureux Jourdain de Saxe), latin et français (`saintnom1899:petit-office-saint-nom-de-jesus`) | *Manuel de la Confrérie du Saint Nom de Jésus ou Saint Nom de Dieu*, Saint-Hyacinthe, Dominicains, 1899, *imprimatur* de l'évêque de Saint-Hyacinthe | 20-32, 44 | archive.org `cihm_26544` |
| Souvenez-vous à saint Joseph, invocation « Bon saint Joseph, notre guide », jaculatoires « Jésus, Marie, Joseph » (`cordonjoseph1871:*`, 3 pièces) | *Vertu miraculeuse du cordon de St. Joseph*, nouvelle éd., Montréal, E. Senécal, 1871, « vu et approuvé » par Mgr Bourget, 30 déc. 1870 | 59-60 | archive.org `cihm_28660` |
| Consécration à saint Joseph, prière des associés, prière pour la grâce d'une bonne mort (`confreriejoseph:*`, 3 pièces) | *Manuel de la Confrérie de Saint Joseph*, Montréal, hospice Saint-Joseph, s. d. (sans approbation imprimée) | 26, 56 | archive.org `cihm_61528` |
| Fruits et prières des quinze mystères du Rosaire (`rosairevivant1841:fruits-des-quinze-mysteres`) | *Petit manuel du Rosaire-Vivant*, Montréal, L. Perrault, approuvé par H. Hudon, V. G., 20 sept. 1841 | 19-33 | archive.org `cihm_39974` |
| Prière quotidienne de la Milice angélique (cordon de saint Thomas) (`troisconfreries:priere-quotidienne-milice-angelique`) | *Les Trois Confréries dominicaines*, Ottawa, A. Bureau, s. d. [vers 1902] | 61-62 | archive.org `cihm_78783` |
| Prière de saint Augustin, acte d'admiration, triomphe de l'Église, prières de M. Dupont, litanies de l'humilité, prière de Pie IX, aspirations, vingt-quatre adorations, offrande pour la France (`janvier:*`, 9 pièces) | Janvier, *Manuel de l'Archiconfrérie de la Sainte-Face*, 3e éd., Tours, 1895 | 164-177, 194-201 | bibliotheque-catholique.com (PDF Google) |
| Acte d'oblation des âmes-victimes, amende honorable pour la fête du Sacré-Cœur (`garde1886:*`, 2 pièces) | *Manuel de l'Archiconfrérie de la Garde d'Honneur*, 9e éd., Bourg, 1886 | 134-136, 151-152 | copie saint-eugene.net du scan Google `YxAtAYVrCuwC` |
| Oraison préparatoire et cinq prières aux intentions du Souverain Pontife, acte d'offrande pour les indulgences (`desgenettes:*`, 2 pièces) | Desgenettes, *Manuel… de l'Archiconfrérie du très-saint et immaculé Cœur de Marie*, 13e éd., Paris, 1852 | 432-435 | archive.org `manueldinstruct00dufrgoog` |
| Père éternel, je vous offre le Sang très précieux… (`beringer:offrande-du-precieux-sang`) ; équivalent de l'« Ejaculatory Offering » de Caswall 1861 | Beringer 1925, t. I, n° 250 | 132-133 | archive.org `lesindulgences0001beri` (n147-n148) |
| **Traduction de travail** : colloque avec Jésus crucifié, prières de S. Pie V (`bonamors1896:colloque-saint-pie-v`) | *The Manual of the Bona Mors Confraternity*, New York, 1896 | 22-23 | archive.org `manualofbonamors00unse` (n33-n34) |
| **Traduction de travail** : invocation de la Trinité pour les âmes du purgatoire (`purgatorian1868:invocation-trinite-ames-purgatoire`) | *Purgatorian Consoler*, Baltimore, J. Murphy, 1868 | 312-313 | archive.org `purgatorianconso00queluoft` (n317-n318) |

Manuels consultés sans pièce ajoutée : Mgr de Ségur, *Le Cordon séraphique*, Québec, 1877 (`cihm_13440`) ; *Livret de
la Confrérie du T. S. Rosaire*, Montréal, 1903 (`cihm_77301`) ; *Notice sur le Tiers-Ordre de la pénitence*, Québec,
1867 (`cihm_29653`) ; *Manuel du Tiers-Ordre*, 1885 (`cihm_62202`).

## Neuvaine à la très sainte Trinité (26 novembre 2026, relue sur l'image, à valider)

Demande de l'utilisateur : neuvaine indulgenciée finissant le dimanche de la Trinité, consécration de dom Marmion le
dernier jour (`prog:neuvaine-trinite`). L'indulgence de la neuvaine (Ench. 1952, n° 48 ; Beringer n° 639) vaut pour
**des prières quelconques** en l'honneur de la sainte Trinité dites neuf jours de suite : faute d'une neuvaine imprimée
jour par jour (voir `A_FOURNIR.md`), la page reprend chaque jour les prières à la sainte Trinité de Beringer ci-dessous.
Transcription sur l'image de chaque page ; seconde lecture Tesseract (fra) comparée mot à mot, écarts tranchés sur
l'image (« exerciée », coquille de l'édition, gardée).

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Notice : Triduum ou neuvaine en l'honneur de la très sainte Trinité (`beringer:neuvaine-trinite`) | Beringer 1925, t. I, n° 639 | 340 | archive.org `lesindulgences0001beri` (n355) |
| Adoration et action de grâces (`beringer:trinite-adoration-action-de-graces`) ; porte la fiche d'indulgence de la neuvaine | Beringer 1925, t. I, n° 255 a (Ench. 1952, n° 45, en italien) | 134-135 | idem (n149-n150) |
| Trois offrandes à la très sainte Trinité (`beringer:trinite-trois-offrandes`) | Beringer 1925, t. I, n° 256 | 135 | idem (n150) |
| « Toute-puissance du Père… » (`beringer:trinite-toute-puissance`) | Beringer 1925, t. I, n° 252 (Ench. 1952, n° 53, en latin) | 133 | idem (n148) |
| Consécration de dom Columba Marmion (Noël 1908, renouvelée le 25 mars 1909) (`thibaut:marmion-consecration-trinite`) | Dom R. Thibaut, *Un maître de la vie spirituelle. Dom Columba Marmion, abbé de Maredsous*, 2e éd., Abbaye de Maredsous, 1930 (imprimatur, Namur, 8 sept. 1929), ch. « Grâces d'union » | 190 | archive.org `un0000unse` (n215) |
| Indulgence de la neuvaine : 7 ans une fois le jour ; plénière la neuvaine achevée | *Enchiridion indulgentiarum*, 1952, n° 48 (S. C. Indulg., 8 août 1847 ; S. Pén. Ap., 18 mars 1932), vu sur l'image | 19 | archive.org `enchiridion_indulgentiarum_1952` (n34) |

## Prières obligatoires : titres et remplaçants (26 novembre 2026, relus sur l'image ; branchés le 26 nov. sauf l'acte de contrition)

Audit : `docs/audits/PRIERES_OBLIGATOIRES_2026-11-26.md`. Chaque texte lu sur l'image de la page (archive.org, page
`n<N>.jpg`), fiche d'indulgence ajoutée seulement après lecture de l'*Enchiridion* de 1952 sur l'image.

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Trois Ave Maria à la Vierge immaculée, matin et soir (saint Alphonse) (`beringer:trois-ave-immaculee-conception`) | Beringer 1925, t. I, n° 444 ; Ench. 1952, n° 358 ; même français : *Thésaurisons*, n° 285 (p. 101, n101) | 234 | archive.org `lesindulgences0001beri` (n249) ; Ench. n256 |
| Ma Mère, préservez-moi du péché mortel, trois Ave (`thesaurisons:ma-mere-preservez-moi`) | *Thésaurisons pour le ciel*, 1941, n° 268 ; Ench. 1952, n° 297 | 98 | archive.org `thesaurisons-pour-le-ciel-000001335` (n98) ; Ench. n212 |
| Entre vos mains, Seigneur (saint Edmond) (`ench1952:entre-vos-mains-saint-edmond`) | *Enchiridion indulgentiarum*, 1952, n° 55 (concession en français) ; *Thésaurisons*, n° 23 | 22-23 | archive.org `enchiridion_indulgentiarum_1952` (n37-n38) |
| Recevez, Seigneur, toute ma liberté (`thesaurisons:suscipe`) | *Thésaurisons*, n° 26 ; Ench. 1952, n° 52 (latin, p. 21, n36) | 27 | `thesaurisons-pour-le-ciel-000001335` (n27) |
| Oraison de Prime « Seigneur, Dieu tout-puissant, qui nous avez fait parvenir » (`thesaurisons:oraison-de-prime`) | *Thésaurisons*, n° 28 ; Ench. 1952, n° 60 (latin, p. 25, n40) | 27 | idem (n27) |
| Notice : trois *Gloria Patri* matin, midi et soir pour les privilèges de la sainte Vierge (`thesaurisons:trois-gloria-privileges-de-marie`) | *Thésaurisons*, n° 355 ; Ench. 1952, n° 47 (p. 19, n34) | 125 | idem (n125) |
| Notice : un *Pater*, un *Ave* et un *Gloria* aux intentions du Souverain Pontife (`thesaurisons:prieres-intentions-souverain-pontife`) | *Thésaurisons*, notes explicatives, 4) ; Ench. 1952, p. XV, note 1 a) (S. Pén. Ap., 20 sept. 1933) | 17 | idem (n17) ; Ench. n14 |
| Acte de contrition (`quebec1888:acte-de-contrition`, non branché) | *Le Catéchisme des provinces ecclésiastiques de Québec, Montréal et Ottawa*, Québec, A. Côté, approuvé le 20 avril 1888 (card. Taschereau) ; Ench. 1952, n° 36 | 5 | archive.org `lecatchismedes00qu` (n6) |
| *Aide-mémoire : la journée indulgenciée* (plan des prières du lever, du matin, de la journée et du soir) | *Thésaurisons*, p. 187-188 : sert de guide aux remplaçants, non transcrit | 187-188 | idem (n187-n188) |
## Neuvaines et dévotions à jours comptés (26 novembre 2026, à valider)

Inventaire et décisions : `docs/audits/NEUVAINES_2026-11-26.md`. Une seule pièce nouvelle ; les autres lignes mettent
à leurs jours des textes déjà transcrits.

| Texte | Source | Pages | Accès |
|---|---|---|---|
| Neuvaine de réparation au Sacré-Cœur, du 1er au 9 de chaque mois : offrande du jour (`beringer:neuvaine-reparation-sacre-coeur`), **nouvelle**, relue sur l'image | Beringer 1925, t. I, n° 671 (Pie X, 15 (19) nov. 1907 ; indulgence non comptée) | 353 | archive.org `lesindulgences0001beri` (n368) |
| Neuvaine au Sacré-Cœur pour chaque premier vendredi (`breviaire-sc:neuvaine`) ; amende honorable et consécration au Sacré-Cœur (fin de `breviaire-sc:exercice-messe`) | *Petit bréviaire du Sacré-Cœur de Jésus, extrait de la vie et des œuvres authentiques de la Bienheureuse Marguerite-Marie*, 13e éd., Nancy, Librairie Notre-Dame (Le Chevallier frères), imprimatur 21 mars 1883 | 151-155 ; 119-140 | PDF fourni par l'utilisateur (hors conteneur), transcription relue `engine/recueils/breviaire_sc_suite/` |
| Neuvaine en l'honneur de la sainte Face (`janvier:neuvaine-meditations-sainte-face`) ; date : avant la fête principale de l'Archiconfrérie, saint Pierre (art. V) | Janvier, *Manuel de l'Archiconfrérie de la Sainte-Face*, 3e éd., Tours, 1895 | 112-142 ; 65-66 | bibliotheque-catholique.com (PDF Google) |
| Cinq dimanches de S. Jean Berchmans ; dix dimanches de S. Stanislas Kostka (`jardin:*`) | *Le Jardin de l'âme* (livret) | 63, 66 | livret |
| Neuvaine en l'honneur du séraphique Père S. François d'Assise (`tiersordre1867:neuvaine-saint-francois`), **nouvelle** (suite, branche `claude/neuvaines-2`), recopiée page à page sur l'image, fautes de l'édition gardées | *Notice sur le Tiers-Ordre de la pénitence de Saint-François d'Assise, suivie de neuvaines, litanies, etc.*, Québec, 1867 (imprimatur du 24 mai 1867) | 37-51 | archive.org `cihm_29653` (PDF p. 43-57) ; `engine/recueils/neuvaines/` |
| Neuvaine pour se préparer aux fêtes de S. Joseph (`confreriejoseph:neuvaine-fetes-saint-joseph`), **nouvelle**, recopiée sur l'image | *Manuel de la Confrérie de Saint Joseph*, Montréal, s. d. (aucune approbation imprimée dans le scan) | 65-68 | archive.org `cihm_61528` (PDF p. 66-69) |
| Prières pour les fêtes de S. Joseph, triduums des Fiançailles, du 19 mars et du Patronage (`confreriejoseph:prieres-fetes-saint-joseph`), **nouvelle** (27 nov.), recopiée sur l'image | *Manuel de la Confrérie de Saint Joseph*, Montréal, s. d. (aucune approbation imprimée dans le scan) | 69-76 | archive.org `cihm_61528` (PDF p. 70-77) |
| Neuvaine à S. François-Xavier : prières pour tous les jours (`xavier1880:prieres-neuvaine`), **nouvelle**, recopiée sur l'image | *Neuvaine en l'honneur de saint François-Xavier*, nouvelle éd., Québec, A. F. E. Darveau, 1880 ; approbation de l'archevêque de Québec, 15 déc. 1879 (vue sur l'image) | 41-47 | archive.org `cihm_62891` (PDF p. 43-49) |
| Neuvaine à S. François-Xavier : considérations de chaque jour, veille comprise, avec leurs réflexions et prières (`xavier1880:considerations-neuvaine`), **nouvelle** (27 nov., branche `claude/neuvaines-4`), recopiée page à page sur l'image (seconde lecture Tesseract, mots endommagés relus à 300 dpi ; fautes de l'impression gardées) | même édition | 30-98 | archive.org `cihm_62891` (PDF p. 32-103 ; PDF p. 94-96 : mire du microfilm) |
| Litanies de S. François-Xavier, français et latin en regard, et oraison du saint pour la conversion des infidèles (`xavier1880:litanies-saint-francois-xavier`), **nouvelle** (27 nov.), recopiées sur l'image (accents du latin relus à 300 dpi) | même édition | 48-59 | archive.org `cihm_62891` (PDF p. 50-61) |
| Indulgence de la neuvaine au Sacré-Cœur (prières quelconques), sur `breviaire-sc:neuvaine` | *Enchiridion indulgentiarum*, 1952, n° 250, vu sur l'image | 156-157 | archive.org `enchiridion_indulgentiarum_1952` (n171-n172) |

## Indulgences (compteur), 14 novembre 2026

Règle : la concession la plus récente fait foi : *Enchiridion indulgentiarum*, 1952 (archive.org `enchiridion_indulgentiarum_1952`) ; à défaut *Thésaurisons pour le ciel*, Carmel de Montréal, 1941, imprimatur du 28 avril 1941, d'après les *Preces et Pia Opera* de 1938 (http://www.liberius.net/livre.php?id_livre=1335) ; à défaut Beringer 1925. Données : `data/prieres/indulgences.json` (indulgences partielles seulement ; plénières et indulgences réservées aux confréries non comptées). Vérifiés dans l'Enchiridion : n° 36 (actes de foi, d'espérance, de charité), 43 (Symbole des Apôtres), 114, 221, 293, 319, 331, 332, 333, 462, 478, 585, 671, 687, 691 (Confiteor), 395 (chapelet), litanies du Sacré-Cœur.

| Le chapelet de saint Dominique (manière de le réciter, méditation des mystères) | Abbé L. de Sambucy, *Manuel du chapelet et du rosaire de la Sainte Vierge*, approbation de Mgr de Quélen, 29 mars 1837 | 28-31 | bibliotheque-catholique.com (rubrique Mariologie) |

Inventaire des manuels de piété de bibliotheque-catholique.com : `docs/notes_sources/inventaire_bibliotheque_catholique.md` (138 titres retenus sur 4 884 PDF).

## Écriture sainte (lectures de la roue), 14 novembre 2026

| Texte | Source | Accès |
|---|---|---|
| La Bible (73 livres), français | *La Sainte Bible*, trad. A. Crampon, Desclée, 1923 ; transcription Wikisource relue sur le fac-similé (pages « Bible Crampon 1923/<livre> »). Seul le texte des versets est gardé (notes, sommaires et intertitres de Crampon écartés). | https://fr.wikisource.org/wiki/Bible_Crampon_1923 ; extraction : `engine/ecriture/bible.py` → `data/ecriture/<livre>.json` |
| La Bible, latin | Vulgate clémentine (scrollmapper/bible_databases, VulgClementine) | https://github.com/scrollmapper/bible_databases |

Numérotation : chaque texte garde la sienne (Crampon suit l'hébreu et le grec : psaumes, Siracide, Jn 6, 52-71, Mt 17, 14-27).

## Sources consultées pour l'inventaire (textes pas encore recopiés)

| Source | Édition | Ce qu'on y a repéré | Accès |
|---|---|---|---|
| Beringer, *Les Indulgences, leur nature et leur usage* | trad. Ph. Mazoyer, 4e éd. française, Paris, P. Lethielleux, 1925 ; approuvée par la S. Pénitencerie ; t. I et II | n° 428 Angélus et Regina Cæli ; litanies n° 305, 377, 439, 487 ; n° 274-276 b (Saint-Esprit) ; t. II : chapelet des Morts (Nîmes, Pie IX 1873) | archive.org `lesindulgences0001beri`, `lesindulgences0002beri` |
| Beringer, *Les Indulgences* | éd. française 1905, t. I et II | contrôle | archive.org `lesindulgencesle01beri`, `lesindulgencesle02beri` |
| ***Enchiridion indulgentiarum*** | S. Pénitencerie, Typis polyglottis Vaticanis, 1952 | n° 175 *Mensis eucharisticus* | archive.org `enchiridion_indulgentiarum_1952` |
| ***The Raccolta*** | trad. anglaise officielle (exemplaire numérisé de 1949) | contrôle (dons du Saint-Esprit) | archive.org `raccoltaofficial0000spen_1` |
| *Livre d'or des âmes du purgatoire* | J.-S. Benoit, Montréal, E. Michaud ; imprimatur du 3 juillet 1925 | à exploiter (lundi, novembre) | archive.org `livre-d-or-des-ames-du-purgatoire-000001152` |

## Textes donnés par l'utilisateur (14 novembre 2026)

| Texte | Source |
|---|---|
| Litanies pour la délivrance des âmes du purgatoire (lundi) | FSSPX, district du Canada : https://sspx.ca/fr/litanies-pour-la-delivrance-des-ames-du-purgatoire-33432 |
| Litanies pour les fidèles défunts (lundi, en alternance) | salve-regina.com, « auteur inconnu, tradition catholique », postérieur à 1925 : http://salve-regina.com/index.php?title=Litanies_pour_les_fid%C3%A8les_d%C3%A9funts |
| Litanies de la bonne mort, avec deux prières | Le Petit Sacristain (blog), oct. 2016 : http://le-petit-sacristain.blogspot.com/2016/10/litanies-de-la-bonne-mort.html |
| Renouvellement de la consécration au cordon de saint Joseph | **Formule composée pour l'app** à la demande de l'utilisateur (aucune formule ancienne trouvée), à partir de Beringer 1925, t. II, n° 266 et 480 |

## Sites récents consultés (cités par lien seulement)
- La Porte Latine, « Prières du matin et du soir » : https://laportelatine.org/spiritualite/prieres-et-devotions/prieres-matin-et-soir
- Catholique de France, « Prière du matin », « Prière du soir », « L'Angélus » : https://catholiquedefrance.fr/priere-du-matin/
