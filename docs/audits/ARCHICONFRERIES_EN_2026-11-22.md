# Manuels d'archiconfréries en anglais : recherche, pièces, proposition d'intégration (22 nov. 2026)

Décision de l'utilisateur du 22 nov. : les manuels d'archiconfréries antérieurs à Vatican II sont admis comme sources ;
ceux qui ne sont pas en français peuvent être traduits, **à condition** de chercher d'abord une version française
ancienne de chaque pièce. Branche `claude/archiconfreries-en`. Rien n'est branché dans `programme.json`.

Règle appliquée (CLAUDE.md § 13, skill `hortus-sources`) :

1. version française ancienne d'abord (manuel français de la même archiconfrérie, Beringer 1925, recueils déjà
   présents) : l'anglais ne sert alors que d'index ;
2. sinon traduction de travail littérale, marquée `traduction: "Hortus Sacrum, traduction de travail du 22 novembre
   2026, à relire"`, original anglais gardé entier dans le champ `anglais` (à côté de `latin`), aucune indulgence
   comptée (can. 934 § 2) ; formules usuelles (Notre Père, Je vous salue, Marie, Gloire au Père) laissées sous leur
   forme française courante, sans les réécrire.

Méthode : couche texte d'archive.org (ABBYY) pour repérer, puis lecture de chaque page sur l'image
(`https://archive.org/download/<id>/page/n<N>.jpg`), seconde lecture Tesseract (`fra+lat`, `eng`, `--psm 6`) et
contrôle des mots de chaque pièce absents de la seconde lecture (tous revus sur l'image : coupures de fin de ligne,
accents, lettres retournées). Fichiers téléchargés hors dépôt (scratchpad).

## Bilan

| Manuel | Pièces ajoutées | Français ancien trouvé | Traduction de travail |
|---|---|---|---|
| 1. Bona Mors, New York, 1896 | 9 | 2 (Beringer n° 582 ; Lefebvre 1870) | 7 (réflexions du dimanche au samedi) |
| 2. Cordon de S. François, Londres, 1878 | 2 | 1 (notice de Québec, 1876) | 1 (cinq courtes prières) |
| 3. Précieux Sang, Londres, 1850 et 1861 | 1 | 1 (Boylesve, Saint-Hyacinthe, 1882) | 0 |
| 4. Sainte-Famille, Liège / [Québec], 1875 | 2 | 1 (Beringer n° 298) | 1 (acte de consécration) |
| 5. *Purgatorian Consoler*, Baltimore, 1868 | 7 | 7 (Beringer n° 615) | 0 |
| 6. Perpétuel Secours (Lenoir, 1885) | 0 | — (pièces déjà présentes : Weber) | 0 |
| 7. *Mother Love* | 0 | — | — (aucun scan libre d'avant 1962) |
| 8. *The Holy Hour* | 0 | Beringer, t. II, n° 230 (notice) | 0 |
| 9. Sainte-Face (Janvier, 1887) | 0 | comparaison seulement | 0 |
| **Total** | **21** | **12** | **9** |

## 1. *The Manual of the Bona Mors Confraternity*, 1896

- **Édition** : *The Manual of the Bona Mors Confraternity, Association for a Happy Death*, New York, Apostleship of
  Prayer, 27-29 West 16th Street, © 1896 ; *Imprimatur* : Michael Augustine [Corrigan], archevêque de New York.
- **URL** : https://archive.org/details/manualofbonamors00unse (138 images ; page 33 = image n44).
- **Table** : explication de la confrérie (origine, objet, moyens, conditions, pratiques, privilèges, réunions,
  exercices, p. 1-5) ; dévotions publiques (ordre de l'office, cantique *Jesus ever sorrowing Saviour*, *O salutaris*,
  litanie pour une heureuse mort « du Rituel romain », dévotion aux cinq plaies, stations de la Passion, colloque avec
  le Christ en croix « prières de S. Pie V », *Tantum ergo*, *De profundis*, acte de consécration, *Stabat Mater*,
  p. 6-29) ; dévotions privées : le matin (actes, offrande, prière de S. Ignace, pour une bonne mort, *Memorare*,
  S. Joseph, ange gardien, aspiration, p. 30-32), réflexions sur la mort pour chaque jour (p. 33-34), invocations pour
  une bonne mort (p. 35-37), à chaque heure, offrande à la messe, après la communion, prières indulgenciées, prières à
  S. Joseph pour les mourants, court chemin de croix, psaumes de la pénitence, le soir, examen, prières diverses
  (p. 37-62) ; visite des malades, viatique, extrême-onction, dernière bénédiction, recommandation de l'âme, messe des
  morts, sépulture (p. 63-113).
- **Pratique de l'associé** (p. 3) : trois *Pater* et trois *Ave* chaque jour en l'honneur des trois heures d'agonie du
  Christ en croix, examen chaque soir, sacrements chaque mois, préparation à la mort un jour par mois.
- **Indulgences** (p. 4-5) : réservées aux associés ; même sommaire en français dans Beringer 1925, t. II, n° 262
  (p. 248-251). Non comptées.

| Pièce | Statut | Id |
|---|---|---|
| Invocations for a Good Death (p. 35-37) | **français trouvé** : Beringer 1925, t. I, n° 582, « Pour une bonne mort », p. 310-312 (même prière, plus complète). C'est aussi le texte des « Litanies de la bonne mort » prises sur Le Petit Sacristain (`petit-sacristain:litanies-bonne-mort`), qui reçoit ainsi une source ancienne | `beringer:pour-une-bonne-mort` |
| Act of Consecration (p. 26) | **équivalent français** : acte de consécration de l'Association de la Bonne Mort de Paris (agrégée à Rome), Lefebvre, *La science de bien mourir*, 5e éd., 1870, p. 401-402 ; texte différent de l'anglais | `lefebvre1870:acte-de-consecration-bonne-mort` |
| Occasional Reflections on Death, dimanche à samedi (p. 33-34) | **traduction de travail** (aucun équivalent français trouvé dans Lefebvre 1870 ni Beringer) | `bonamors1896:reflexion-dimanche` … `-samedi` |
| Devotion to the Five Wounds (p. 12-16), Colloquy with Christ Crucified (p. 21-22), Litany « from the Roman Ritual » (p. 9-12), court chemin de croix (p. 43-45) | non transcrits (candidats ; la litanie est celle de la recommandation de l'âme du Rituel) | — |
| Memorare, Anima Christi, Suscipe, prière à S. Joseph pour la pureté, jaculatoires (p. 31-41) | **déjà présents** en français dans le projet (Beringer, Thésaurisons, livret) | — |

## 2. *Manual of the Arch-Confraternity of the Cord of S. Francis*, 1878

- **Édition** : compilé par les Franciscains de Stratford, Londres, Burns & Oates, 1878 ; *Nihil obstat* Jacobus
  J. Guiron, *Imprimatur* Daniel Gilbert, vic. gén., 21 février 1878 ; approbation de l'Ordre (Anvers, 20 août 1877 ;
  Malines, 24 août 1877). Fondé sur l'*Essay on the Cord* du P. Pacificus Baker (1792).
- **URL** : https://archive.org/details/ManualCordOfSFrancis (page 37 = image n45).
- **Table** : des confréries (p. 1) ; origine et objet (8) ; signification du cordon (11) ; avantages (12) ; conditions
  (13) ; indulgences (14) ; règles de la confrérie en société (24) ; bénédiction du cordon et absolution générale (27) ;
  réunion mensuelle et procession (30) ; dévotions privées (35) ; chemin de croix (37) ; litanies de S. François (58) ;
  prière à S. François (60) ; neuvaine à S. François (61) ; règle de vie et retraite mensuelle (72) ; cantiques (81) ;
  appendice et sermon (90-91).
- **Pratique** (p. 13-14, 35) : porter le cordon ; coutume de dire chaque jour cinq *Pater*, *Ave*, *Gloria* en
  l'honneur des cinq plaies et de S. François, et un sixième aux intentions du Pape, de préférence les bras en croix
  (mais jamais en public).
- **Indulgences** : réservées aux confrères (dont celles « des Stations » attachées aux six *Pater*, Pie IX, 14 avril
  1856) ; non comptées. Sommaire français à jour : Beringer 1925, t. II, n° 272.

| Pièce | Statut | Id |
|---|---|---|
| Pratique des six *Pater*, *Ave*, *Gloria* | **français trouvé** : *Le Cordon de saint François d'Assise*, Québec, 1876 (*imprimatur* du 2 déc. 1876, † E. A. [Taschereau], arch. de Québec), p. 2-3 | `cordon1876:six-pater-ave-gloria` |
| Short Prayers when saying the Our Fathers (p. 37) | **traduction de travail** (absentes de la notice de Québec) | `cordon1878:courtes-prieres` |
| Litanies, prière et neuvaine de S. François (p. 58-71) | non transcrites (candidates, à chercher d'abord en français : manuel du Tiers-Ordre) | — |

## 3. Précieux Sang : *The Book of the Confraternity of the Precious Blood*, 1850, et Caswall, *Confraternity Manual of the Most Precious Blood*, 1861

- **Éditions** : *The Book of the Confraternity of the Precious Blood, erected by Papal authority… in the church of the
  Oratory of St. Philip Neri, London*, Londres, Burns and Lambert, 19e mille [1850] ; rescrit de Pie IX (audience du
  11 août 1850, Propagande, 12 août 1850 ; Robert Whitty, vic. gén., 24 sept. 1850) étendant à la confrérie les
  indulgences de l'archiconfrérie de S. Nicolas in Carcere. — E. Caswall, *Confraternity Manual of the Most Precious
  Blood*, Londres, Dublin et Derby, Thomas Richardson and Son, 1861 (approbation non imprimée dans le scan).
- **URL** : https://archive.org/details/TheBookOfTheConfraternity ; https://archive.org/details/ConfraternityManualOfThe
- **Table (1850)** : rescrit ; sens de la dévotion ; archiconfrérie de Rome ; sommaire des indulgences ; offrandes au
  Verbe incarné ; offrande du Précieux Sang (sept offrandes) ; aucune obligation. **Table (1861)** : sur la dévotion
  (excellence, culte de latrie, oblation, application des mérites) ; histoire des confréries ; hymnes ; sept offrandes ;
  offrandes pour l'Immaculée Conception ; offrande jaculatoire ; acte de réparation ; petit chapelet des sept effusions ;
  autres pratiques ; textes de l'Écriture à méditer ; la lance et les clous ; les plaies ; catéchismes.

| Pièce | Statut | Id |
|---|---|---|
| Sept offrandes du Précieux Sang | **déjà présentes** (livret, `jardin:les-sept-offrandes-du-precieux-sang`) | — |
| Offrande jaculatoire « Eternal Father, I offer Thee the Precious Blood… » | à chercher dans Beringer (non fait) | — |
| Petit chapelet du Précieux Sang (Little Chaplet of the Seven Blood-sheddings) | **français trouvé** : [Boylesve], *Le mois du Précieux Sang*, Saint-Hyacinthe, 1882 (*imprimatur* du 30 mai 1882 ; déjà source du mois de juillet), « Petit chapelet », p. 42-43, avec les deux oraisons auxquelles il renvoie (p. 48-49) | `boylesve1882:petit-chapelet-precieux-sang` |
| Offrande (main droite), trois offrandes, « Autre chapelet » méditant chaque effusion (Boylesve, p. 41-52) ; acte de réparation (Caswall) | non transcrits (candidats) | — |

## 4. *Manual of the Arch-Confraternity of the Holy Family*, 1875

- **Édition** : *Manual of the Arch-Confraternity of the Holy Family, Jesus, Mary, and Joseph, canonically erected in
  the church of the Redemptorist Fathers, Liege*, [Québec], 1875 (traduction anglaise publiée par les Rédemptoristes) ;
  statuts approuvés par Corneille [van Bommel], évêque de Liège, 29 juillet 1850 (approbations semblables de Malines et
  Tournai) ; brefs de Pie IX des 20 et 23 avril 1847.
- **URL** : https://archive.org/details/manualofthearchc00unknuoft (pages 44-45 = images n47-n48).
- **Table** : notice historique ; statuts (art. I-XX, avec observations) ; approbation ; exercices de la réunion
  hebdomadaire ; réunion des préfets ; consécration solennelle (cérémonies, acte, formule de réception latin-anglais) ;
  communion générale ; retraite et rénovation des vœux du baptême ; patrons de l'année ; messes pour les défunts ;
  chemin de croix ; affiliation ; en l'honneur de N.-D. du Perpétuel Secours ; rénovation des promesses ; brefs
  apostoliques ; sommaire des indulgences.
- **Pratique** (art. XVI) : chaque matin, offrande des actions de la journée à Jésus, Marie et Joseph, renouvelée
  pendant le jour ; chaque soir, examen puis communion spirituelle ; *Pater* et *Ave* matin et soir au patron de
  l'année. Même règle en français : Beringer 1925, t. II, n° 234.
- **Indulgences** : réservées aux associés, non comptées.

| Pièce | Statut | Id |
|---|---|---|
| Act of Consecration (p. 44-45) | **traduction de travail** (manuel français, *Manuel de piété à l'usage des associés*, Bruges et Lille, 12e éd., 1888, cité par Beringer : pas de scan libre trouvé) | `saintefamille1875:acte-de-consecration` |
| « Prayer peculiar to the Holy Family » (p. 92-93) | **français ancien** : Beringer 1925, t. I, n° 298, « A la Sainte Famille », p. 151 (Ench. 1952, n° 643) | `beringer:a-la-sainte-famille` |

## 5. *Purgatorian Consoler*, 1868

- **Édition** : *Purgatorian Consoler : a Manual of Prayers… originally prepared for the use of the Members of the
  Purgatorian Arch-Confraternity, enlarged and adapted to general use, by a Redemptorist Father*, Baltimore, John
  Murphy & Co., 1868, « published with the approbation of the Most Rev. the Archbishop of Baltimore » ; traduction
  augmentée de B. Queloz, C.Ss.R., *La pietà del cristiano verso i morti*.
- **URL** : https://archive.org/details/purgatorianconso00queluoft (482 images).
- **Table** : préface ; fêtes mobiles ; ce que tout chrétien doit savoir ; baptême privé ; prières du matin et du soir ;
  messe ; vêpres ; bénédiction ; confession ; communion ; confirmation ; extrême-onction ; dévotions à Notre-Seigneur, à la
  sainte Vierge, aux saints ; prières pour diverses occasions ; dévotions générales pour les défunts (messe et office des
  morts, prières pour chaque jour de la semaine, neuvaine, prières de sainte Gertrude, invocation de la Trinité…) ; règle
  de vie ; commandements ; devoirs d'état ; instruction sur le purgatoire ; l'archiconfrérie (acte héroïque, p. 437) ;
  indulgences ; index.
- **Indulgences** : celles de l'archiconfrérie (Rome, Rédemptoristes) réservées aux associés ; sommaire français :
  Beringer 1925, t. II, n° 306.

| Pièce | Statut | Id |
|---|---|---|
| Prayers for the whole week (p. 295-297 ; Léon XII, 18 nov. 1826) | **français trouvé** : Beringer 1925, t. I, n° 615, p. 323-324, une pièce par jour | `beringer:ames-purgatoire-dimanche` … `-samedi` |
| Out of the depths after the Angelus at night | **déjà présent** (`paroissien:de-profundis`) | — |
| Prières de sainte Gertrude pour les âmes | **déjà présentes** en français (Denis, `gertrude:*`) | — |
| Acte héroïque de charité (p. 437-441), neuvaine pour les âmes, invocation de la Trinité | non transcrits : chercher d'abord Beringer et le *Livre d'or des âmes du purgatoire* (1925) | — |

## 6. Perpétuel Secours (Lenoir, New York, 1885)

L'édition de Lenoir (1885) n'a pas été trouvée en scan libre (archive.org, recherche web). Une édition voisine existe :
*Manual of the Confraternity of Our Lady of Perpetual Help and Saint Alphonsus*, New York, Redemptorist Fathers,
[19..] (https://archive.org/details/manualofconfrate00arch, sans page de copyright). Les prières principales sont déjà
présentes en français (`weber:priere-notre-dame-du-perpetuel-secours`, `weber:trois-prieres-perpetuel-secours`) ; le
sommaire de l'archiconfrérie est dans Beringer 1925, t. II, n° 255 ; une notice française existe : *Notre-Dame du
Perpétuel-Secours*, Montréal, J.-B. Rolland, 1878 (archive.org `cihm_52280`), non exploitée. Rien d'ajouté.

## 7. *Mother Love* (Archiconfrérie des Mères chrétiennes)

Seule édition sur archive.org : 1975 (`motherloveprayer0000ofmc`), postérieure à 1962, écartée. Le livre dérive de
W. Cramer, *The Christian Mother*, New York, Benziger, 1880 (archive.org `TheChristianMother`, domaine public), première
édition anglaise de 1888 sous le titre *Mother Love* (non trouvée). Sommaire français de l'archiconfrérie : Beringer
1925, t. II, n° 308. Rien d'ajouté (voir `A_FOURNIR.md`).

## 8. *The Holy Hour* (Archiconfrérie de l'Heure sainte)

Pas de section anglaise propre trouvée. La notice française fait foi : Beringer 1925, t. II, n° 230 (Paray-le-Monial ;
archiconfrérie pour la France et la Belgique, bref du 6 avril 1886 ; pour l'Espagne, 1897 ; étendue au monde entier,
Pie X, 27 mars 1914) : une heure de prière dans la nuit du jeudi au vendredi (dès le jeudi après-midi), en union à
l'agonie du Jardin des Oliviers. Rien d'ajouté.

## 9. Janvier, *Manual of the Archconfraternity of the Holy Face*, 1887

Comparaison seulement : le projet suit l'original français (Janvier, *Manuel de l'Archiconfrérie de la Sainte-Face*,
3e éd., Tours, 1895, `janvier:*`). Le manuel anglais (archive.org `manualofthe-archconfraternityofthe-holy-face`) suit
le même plan, avec en supplément l'« Association de prières contre le blasphème » (petit office du saint Nom de Dieu),
déjà signalée comme reste à faire dans `docs/REPRISE.md`. Rien d'ajouté.

## Traductions de travail à relire par l'utilisateur

| Id | Original | Page |
|---|---|---|
| `bonamors1896:reflexion-dimanche` … `-samedi` (7) | *Occasional Reflections on Death* | Bona Mors 1896, p. 33-34 |
| `cordon1878:courtes-prieres` (et la note de la p. 35 citée dans `usage`) | *Short Prayers when saying the Our Fathers* | Cordon 1878, p. 35 et 37 |
| `saintefamille1875:acte-de-consecration` | *Act of Consecration* | Sainte-Famille 1875, p. 44-45 |

Points de traduction à trancher : « put off all undue affection » rendu « dépouillez toute affection déréglée » ;
« be merciful to me a sinner » rendu « soyez miséricordieux envers moi, pécheur » ; dans l'acte de la Sainte-Famille,
le sujet est le nom prononcé à voix basse, d'où « (nom), … vous choisis » sans « je », comme en anglais ; les traits
des pauses sont gardés. Saturday, 2 (« O death, how bitter is thy memory… ») cite Si 41, 1 : on pourrait préférer le
texte de Crampon déjà présent dans `data/ecriture`.

L'app ne montre pas encore les champs `anglais` et `traduction` (type `Texte` inchangé) : la mention de la traduction
et de l'absence d'indulgence est aussi dans `usage`. Afficher l'original dans la fiche demanderait un petit changement
de `FicheTexte.svelte` (non fait).

## Indulgences

Rien n'est ajouté à `data/prieres/indulgences.json`. À vérifier sur le scan de l'*Enchiridion* 1952 avant tout compte :
n° 594 (prières pour chaque jour, 500 jours chacune, suivies de *Pater*, *Ave*, *Requiem* et non du *De profundis*) ;
n° 643 (*Fac nos, Domine Iesu, sanctae Familiae tuae…*, 3 ans). La prière n° 582 de Beringer (Léon XII, 1824) n'est pas
dans l'Enchiridion de 1952 (section *Pro bona morte*, n° 636-649) : concession abrogée, notée comme telle. Le petit
chapelet du Précieux Sang et les indulgences propres des confréries : non comptés.

## Proposition d'intégration (non appliquée)

Principes de l'utilisateur : « le moins pour le plus, le simple mais le saint, la variété mais la sobriété ». Tout
s'insère dans des séquences existantes ; aucune pratique nouvelle n'est obligatoire.

1. **Âmes du purgatoire, chaque soir, une prière du jour** (Beringer n° 615) : insertion dans `prog:priere-du-soir`,
   point `fin`, `{ "selon": "jour_semaine", "valeurs": [beringer:ames-purgatoire-dimanche … -samedi] }`, sur le modèle
   de `prog:don-du-jour`. Une oraison de cinq lignes, suivie d'un *Pater* et d'un *Ave* ; le *De profundis* reste celui
   de la dévotion du lundi (`prog:devotion-lundi`, déjà au programme) pour ne pas doubler ; le lundi, on peut mettre
   `null` (comme le samedi pour le don du jour) si la dévotion du lundi paraît suffire. C'est la proposition principale : peu de texte, une variété réglée
   par la semaine, et le sang de Jésus médité à chaque jour selon la Passion.
2. **Bonne mort** : remplacer la source de `petit-sacristain:litanies-bonne-mort` par `beringer:pour-une-bonne-mort`
   (même prière, édition approuvée) partout où elle serait utilisée ; l'offrir comme prière du premier vendredi ou du
   jour de récollection mensuelle (pratique de la Bonne Mort : « un jour chaque mois pour se préparer à la mort »).
3. **Réflexions sur la mort** (après relecture de la traduction) : une pensée du jour, trois lignes, à la fin de
   l'examen du soir, `selon: jour_semaine`. Alternative plus sobre : seulement en novembre (mois des défunts).
4. **Précieux Sang** : `boylesve1882:petit-chapelet-precieux-sang` en juillet (mois du Précieux Sang, même livre que
   les méditations du mois), à la place du chapelet du jour ou en option le vendredi de juillet.
5. **Sainte Famille** : `beringer:a-la-sainte-famille` en février (mois de la Sainte Famille, décision n° 6 de
   `A_FOURNIR.md`) et le dimanche de la Sainte Famille, une fois le jour, après l'offrande du matin.
6. **Optionnel, hors liste du jour** : actes de consécration (Bonne Mort, Sainte-Famille) et pratique du cordon de
   S. François (pour un utilisateur qui serait reçu dans ces confréries) : consultables dans Prières.

Classements devinés (`devinee`) ajoutés dans `data/prieres/dimensions-textes.json` pour les pièces des points 1 à 5
(17 entrées), à relire.
