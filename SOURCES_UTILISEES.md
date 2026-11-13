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
