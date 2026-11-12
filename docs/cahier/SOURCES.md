# Sources

Classées par usage. Toujours citer l’édition utilisée.

## Liturgie et calendrier

- **Divinum Officium** : https://github.com/DivinumOfficium/divinum-officium. On utilise ses **données** ; son code Perl n’est pas nécessaire.
  - `web/www/Tabulae/Kalendaria/*.txt` : calendriers successifs.
  - `Tabulae/Transfer/*.txt` : translations selon la lettre dominicale et la date de Pâques.
  - `horas/{Latin,Francais}/{Sancti,Tempora,Commune}` : offices, rangs, leçons, dont les leçons historiques des saints.
  - `horas/{Latin,Francais}/Martyrologium/MM-DD.txt` : **Martyrologe romain** (latin et français).
  - `missa/{Latin,Francais}/{Sancti,Tempora}` : propres de la messe : Introït, Collecte, Épître, Évangile… Les communs de la messe sont dans `horas/*/Commune`.
- **Missale Romanum**, édition typique de 1920 : archive.org, identifiant `000missaleromanum-1920`. Source des **stations** (déjà extraites dans `moteur/stations.py`).
- **Code de droit canonique de 1917** : can. 1247 (fêtes de précepte), 1250-1254 (jeûne et abstinence), 928 et 933 (indulgences). Texte anglais : https://www.canonlaw.info (page « codexQuon »).
- **Saint Louis-Marie Grignion de Montfort**, *Traité de la vraie dévotion*, n° 227-233 (préparation à la consécration) : édition ancienne à trouver.

## Indulgences et prières

- ***Enchiridion indulgentiarum***, S. Pénitencerie, Typis polyglottis Vaticanis, **1952** : archive.org `enchiridion_indulgentiarum_1952` (texte OCR : `enchiridion_indulgentiarum_1952_djvu.txt`).
  - C’est la **référence** pour toutes les indulgences.
  - Numéros des pieux exercices des mois : 118 (janvier, saint Nom de Jésus), 466 (mars, S. Joseph), 325 (mai, Marie), 253 (juin, Sacré-Cœur), 217 (juillet, Précieux Sang), 389 (août, Cœur Immaculé), 381 (septembre, Douleurs), 398 (octobre, Rosaire), 589 (novembre, trépassés), 364 (décembre, Immaculée Conception).
- **Raccolta** 1943 (trad. anglaise officielle) : archive.org `raccoltaofficial0000spen_1`.
- **Beringer**, *Les Indulgences*, 1905 : archive.org `lesindulgencesle01beri`.
- ***Livre d’or des âmes du purgatoire***, 1925 : archive.org `livre-d-or-des-ames-du-purgatoire-000001152`.
- **Sainte Marguerite-Marie** : Gauthey, *Vie et Œuvres*, t. II (archive.org `vieetoeuvre02alac`) ; *Recueil des écrits*, 1865 (`wotb_6878724`).
- **AAS** 1928 (acte de réparation de Pie XI) et 1954 (monitum sur les promesses de sainte Brigitte) : vatican.va.
- Les textes déjà vérifiés et leurs références sont dans `notes_sources/` et dans le livret (`livret/source`).

## Méditations et vies de saints

- **Dom Guéranger**, *L’Année liturgique* : volumes sur archive.org (ex. `lanneliturgiqu05gu`). Faire l’inventaire des volumes et des éditions.
- **Bibliothèque catholique** : https://www.bibliotheque-catholique.com/
  - Portail de livres anciens en PDF, en téléchargement gratuit, classés par catégorie (Piété, Liturgie, Hagiographies…).
  - Y chercher des recueils de méditations quotidiennes et des « mois » (S. Joseph, Marie, Sacré-Cœur, âmes du purgatoire…).
  - Vérifier pour chaque livre la date de l’édition d’origine, qui doit être antérieure à 1955 et du domaine public.
  - Citer l’édition d’origine.
- **Autres pistes à vérifier** (archive.org, Gallica, Canadiana) :
  - *Mois des âmes du purgatoire* (archive.org `moisdesamesdupur00berl`) ;
  - *Mois de saint Joseph* (Canadiana `oocihm.04686`, `oocihm.62879`) ;
  - méditations quotidiennes, par exemple Hamon, *Méditations à l’usage du clergé et des fidèles*, et Chaignon. **Vérifier l’existence et l’édition avant tout usage.**
- **Le Petit Sacristain** : http://le-petit-sacristain.blogspot.com/. Cité par **lien** seulement.

## À ne pas utiliser

- Textes et calendriers postérieurs à 1955 (réforme de 1955, 1960/1962, Novus Ordo).
- Recueils de promesses non approuvées.
- Toute source dont l’édition n’est pas identifiable.
