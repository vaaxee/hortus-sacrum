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

## Étape 9 — Méditations et lectures

| Recueil | Édition | Usage | Accès |
|---|---|---|---|
| Hamon, *Méditations à l'usage du clergé et des fidèles pour tous les jours de l'année*, 3 t. | Paris, Victor Lecoffre ; Lyon ; t. I 1879 (10e éd.), t. II 1894 | 437 méditations découpées par jour (temporal, dates fixes, Sacré-Cœur, dimanches d'octobre, Dédicace) dans `data/recueils/hamon.json` ; texte OCR, coquilles possibles | PDF Google Livres fournis par l'utilisateur (`vendor/sources/hamon/`) |
| Chaignon, S. J., *La méditation, ou le fidèle sanctifié par la pratique de l'oraison mentale*, 3 t. | Paris, 1872 | 213 méditations : parcours de 95 méditations suivi dans l'ordre les jours ordinaires ; 118 pour l'année liturgique, dont 88 rattachées à un jour, proposées en second choix ; OCR, coquilles possibles | archive.org `lamditationoulef01chai`, `…02chai`, `…03chai` |
| *Breviarium Romanum*, leçons du IIe nocturne (IV-VI) du sanctoral, latin et traduction française | rubriques de 1911 (Divino Afflatu), données Divinum Officium ; la leçon abrégée de 1960 est écartée | 322 offices, dont 277 avec le français, dans `data/recueils/breviaire.json` ; page « Office du jour et vie du saint » | dépôt Divinum Officium (`vendor/do`) |
| Dom Guéranger, *L'Année liturgique*, 15 vol. (continuée par Dom Fromage) | Tours, Mame, 1911 | 423 lectures (93 jours du temporal, 270 dates de saints) dans `data/recueils/gueranger/` ; lecture du jour sous la méditation et notice sur la page du saint ; OCR, coquilles possibles ; des féries d'Avent et la semaine de Pâques manquent (intitulés illisibles) | archive.org `lanneliturgiqu01gu` … `lanneliturgiqu15gu` ; texte propre pour 202 lectures : https://www.domgueranger.net/lannee-liturgique/ et https://abbe-pivert.com/dom-gueranger-annee-liturgique/ (pièces latines omises) |
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

## Indulgences (compteur), 14 novembre 2026

Règle : la concession la plus récente fait foi : *Enchiridion indulgentiarum*, 1952 (archive.org `enchiridion_indulgentiarum_1952`) ; à défaut *Thésaurisons pour le ciel*, Carmel de Montréal, 1941, imprimatur du 28 avril 1941, d'après les *Preces et Pia Opera* de 1938 (http://www.liberius.net/livre.php?id_livre=1335) ; à défaut Beringer 1925. Données : `data/prieres/indulgences.json` (indulgences partielles seulement ; plénières et indulgences réservées aux confréries non comptées). Vérifiés dans l'Enchiridion : n° 36 (actes de foi, d'espérance, de charité), 43 (Symbole des Apôtres), 114, 221, 293, 319, 331, 332, 333, 462, 478, 585, 671, 687, 691 (Confiteor), 395 (chapelet), litanies du Sacré-Cœur.

| Le chapelet de saint Dominique (manière de le réciter, méditation des mystères) | Abbé L. de Sambucy, *Manuel du chapelet et du rosaire de la Sainte Vierge*, approbation de Mgr de Quélen, 29 mars 1837 | 28-31 | bibliotheque-catholique.com (rubrique Mariologie) |

Inventaire des manuels de piété de bibliotheque-catholique.com : `docs/notes_sources/inventaire_bibliotheque_catholique.md` (138 titres retenus sur 4 884 PDF).

## Sources consultées pour l'inventaire (textes pas encore recopiés)

| Source | Édition | Ce qu'on y a repéré | Accès |
|---|---|---|---|
| Beringer, *Les Indulgences, leur nature et leur usage* | trad. Ph. Mazoyer, 4e éd. française, Paris, P. Lethielleux, 1925 ; approuvée par la S. Pénitencerie ; t. I et II | n° 428 Angélus et Regina Cæli ; litanies n° 305, 377, 439, 487 ; n° 274-276 b (Saint-Esprit) ; t. II : chapelet des Morts (Nîmes, Pie IX 1873) | archive.org `lesindulgences0001beri`, `lesindulgences0002beri` |
| Beringer, *Les Indulgences* | éd. française 1905, t. I et II | contrôle | archive.org `lesindulgencesle01beri`, `lesindulgencesle02beri` |
| ***Enchiridion indulgentiarum*** | S. Pénitencerie, Typis polyglottis Vaticanis, 1952 | n° 175 *Mensis eucharisticus* | archive.org `enchiridion_indulgentiarum_1952` |
| ***The Raccolta*** | trad. anglaise officielle (exemplaire numérisé de 1949) | contrôle (dons du Saint-Esprit) | archive.org `raccoltaofficial0000spen_1` |
| *Livre d'or des âmes du purgatoire* | J.-S. Benoit, Montréal, E. Michaud ; imprimatur du 3 juillet 1925 | à exploiter (lundi, novembre) | archive.org `livre-d-or-des-ames-du-purgatoire-000001152` |

## Sites récents consultés (cités par lien seulement)
- La Porte Latine, « Prières du matin et du soir » : https://laportelatine.org/spiritualite/prieres-et-devotions/prieres-matin-et-soir
- Catholique de France, « Prière du matin », « Prière du soir », « L'Angélus » : https://catholiquedefrance.fr/priere-du-matin/
