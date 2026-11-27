# Manuels d'archiconfréries, lot A — 25 novembre 2026

Demande de l'utilisateur du 25 nov. : finir l'OCR des manuels d'archiconfréries et d'associations pieuses trouvés
(`ARCHICONFRERIES_FR_2026-11-22.md` § 4), puis en extraire et classer le contenu. **Bilan : 77 pièces nouvelles** (Lefebvre 20, Picard 4, Précieux-Sang 7, Notre-Dame du Chemin 8, Perpétuel-Secours 38), aucune traduction de travail, aucune indulgence comptée. Lot A : Bonne Mort (Lefebvre 1870,
Picard 1873), Précieux Sang (Saint-Hyacinthe 1890), Saint-Sacrement (Québec 1920), N.-D. du Perpétuel Secours
(Montréal 1878). Branche `claude/archi-lot-a`. **Rien n'est branché dans `programme.json`** ni classé dans
`dimensions-textes.json` : l'utilisateur tranchera (§ 7).

Méthode (skill `hortus-ocr`) : pour chaque page, deux lectures indépendantes — couche texte ABBYY d'archive.org
(`_djvu.xml`, avec les coordonnées des mots) et Tesseract (`fra+lat`, `--psm 6`, image `page/n<N>.jpg`) — alignées mot
à mot ; les cas où une seule lecture donne un mot connu du corpus du projet sont pris d'office, sauf les mots que l'OCR
confond (cette/celle/celte, ou/on, me/ma, votre/voire…) et les fragments de mots coupés ; tous les autres désaccords
(lettres, accents, ponctuation) sont tranchés sur une bande de l'image ; chaque pièce est ensuite relue sur l'image de
la page entière (titres, rubriques, italiques, mots que les deux lectures ont lus pareillement faux : « celte vie »,
« pilié », « Jésusdonnant »), et les mots de chaque pièce absents des deux lectures sont listés et vérifiés
(il ne reste que des mots recollés en fin de ligne). Orthographe et ponctuation de l'édition gardées (« très-sainte »,
« Barcelonne », « ingnominieuse », « devoilées ») ; seules quelques coquilles évidentes sont corrigées, et notées dans
le champ `page` de la pièce. Fichiers téléchargés et scripts dans le scratchpad, non versionnés.

Préfixes : `lefebvre1870:` (Bonne Mort, Paris), `picard1873:` (Bonne Mort, Montréal), `precieuxsang1890:` (Précieux Sang), `ndchemin1920:` (Saint-Sacrement, Québec), `perpetuelsecours1878:` (Perpétuel Secours).

## 1. Bonne Mort — Lefebvre, *La science de bien mourir*, Paris, 1870

- **Édition** : R. P. Al. Lefebvre, S. J., *La science de bien mourir, manuel de l'Association de la Bonne Mort (établie
  dans l'église du Jésus, à Paris, et agrégée à la congrégation primaire de Rome)*, 5e éd., Paris, Librairie
  Saint-Germain-des-Prés, 1870 ; lettre d'approbation du cardinal Gousset, archevêque de Reims (déjà citée pour
  `lefebvre1870:acte-de-consecration-bonne-mort`).
- **URL** : https://archive.org/details/lasciencedebienm00lefeuoft (exemplaire de Holy Redeemer, Windsor ; page
  imprimée = image n + 15, p. 401 = n416).
- **Table de la IIe partie, « Prières spéciales à l'usage des associés »** (p. 483-484) : acte de consécration (401),
  prières pendant la messe (403), messe pour demander la grâce d'une bonne mort (412), messe des morts (416), hymne au
  saint Sacrement (422), litanies de la Passion (424), litanies de N.-D. des Sept-Douleurs (427), autres litanies (429),
  *Stabat Mater* (431), pieux exercice en l'honneur du Cœur affligé de Marie (434), litanies de saint Joseph (436),
  prières pour les agonisants (439), litanies pour obtenir une bonne mort (447), protestation pour bien mourir de
  S. Alphonse (449), testament spirituel de S. Charles (452), autre testament (454), prière pour la grâce d'une bonne
  mort (456), prière contre la mort subite (457), *En ego* (458), *Anima Christi* (459), *Suscipe* (460), consécration
  de S. Louis de Gonzague *O Domina* (461), prière de sainte Gertrude *Ave candidum* (462), prières à saint Joseph (463,
  464), à saint Michel (464), à l'ange gardien (465), pour les associés vivants, agonisants (465) et décédés (466) ;
  cantiques (467-479).

| Pièce | Statut | Id | Indulgence imprimée |
|---|---|---|---|
| Messe pour demander la grâce d'une bonne mort (du Missel romain), p. 412-415 | **nouvelle** | `lefebvre1870:messe-pour-une-bonne-mort` | — |
| Litanies de la Passion, avec verset et oraison, p. 424-426 | **nouvelle** | `lefebvre1870:litanies-de-la-passion` | — |
| Litanies de N.-D. des Sept Douleurs « composées, dit-on, par Pie VII » (Mère affligée, Mère abandonnée…), p. 427-429 | **nouvelle** (autre texte que `jardin:litanies-de-notre-dame-des-sept-douleurs`) | `lefebvre1870:litanies-notre-dame-des-sept-douleurs` | — |
| Autres litanies de N.-D. des Sept-Douleurs (une invocation par douleur), p. 429-431 | **nouvelle** | `lefebvre1870:autres-litanies-notre-dame-des-sept-douleurs` | — |
| Litanies de saint Joseph (« image du Père céleste… », litanies de dévotion privée, pas celles de 1909), p. 436-438 | **nouvelle** | `lefebvre1870:litanies-de-saint-joseph` | — |
| Prière pour les agonisants : litanie, *Partez, âme chrétienne*, recommandation de l'âme, prières après le décès (Rituel), p. 439-446 | **nouvelle** | `lefebvre1870:priere-pour-les-agonisants` | — |
| Protestation pour bien mourir de S. Alphonse, p. 449-451 | **nouvelle** | `lefebvre1870:protestation-pour-bien-mourir` | — |
| Testament spirituel de S. Charles Borromée, p. 452-454 | **nouvelle** | `lefebvre1870:testament-spirituel-saint-charles` | — |
| Autre formule de testament spirituel, p. 454-455 | **nouvelle** | `lefebvre1870:autre-testament-spirituel` | (vise l'indulgence plénière des associés à la mort) |
| Prière de S. Vincent Ferrier pour une bonne mort (latin-français), p. 456 | **nouvelle** | `lefebvre1870:priere-saint-vincent-ferrier-bonne-mort` | — |
| Prière pour être préservé d'une mort subite, p. 457-458 | **nouvelle** | `lefebvre1870:priere-preserve-mort-subite` | — |
| Prière de sainte Gertrude à Marie, *Ave, candidum lilium* (latin-français), p. 462 | **nouvelle** | `lefebvre1870:priere-sainte-gertrude-ave-candidum` | — |
| Prière à saint Joseph patron de la bonne mort ; *Ave Joseph*, p. 463 | **nouvelles** | `lefebvre1870:priere-saint-joseph-patron-bonne-mort`, `lefebvre1870:ave-joseph` | — |
| Autre prière à saint Joseph pour une grâce particulière ; prière à saint Michel, p. 464 | **nouvelles** | `lefebvre1870:saint-joseph-grace-particuliere`, `lefebvre1870:priere-a-saint-michel-bonne-mort` | — |
| Prière à l'ange gardien ; pour les associés vivants, agonisants, décédés, p. 465-466 | **nouvelles** | `lefebvre1870:priere-a-l-ange-gardien-bonne-mort`, `lefebvre1870:priere-pour-les-associes-vivants`, `-agonisants`, `-decedes` | — |
| Pieux exercice en l'honneur du Cœur affligé de Marie, p. 434-436 | **déjà présent** sous une autre traduction : `beringer:coeur-afflige-de-marie` | — | 300 j., Pie VII, 14 janv. 1815 (non compté) |
| Litanies pour obtenir une bonne mort, p. 447-449 | **déjà présentes** : `beringer:pour-une-bonne-mort` (Lefebvre les attribue à « une demoiselle née protestante, convertie à quinze ans, morte à dix-huit ans en odeur de sainteté ») | — | — |
| Autre prière pour demander la grâce d'une bonne mort (« Que je meure comme les saints Patriarches… »), p. 456-457 | **déjà présente** dans Chaignon (`chaignon` S:61) | — | — |
| *En ego* (p. 458), *Memorare* (460), *O Domina mea* (461), *O felix Maria* et *Salve Regina* (461-462), *Stabat* (431), oraison « dite efficace » à saint Joseph (464) | **déjà présents** (`jardin:chaque-vendredi-devant-le-crucifix`, `weber:souvenez-vous`, `weber:priere-saint-louis-de-gonzague`, `beringer:salve-regina`, `weber:stabat-mater`, `beringer:saint-joseph-purete`) | — | — |
| *Anima Christi*, *Suscipe* (459-460) | déjà présents dans les recueils ; laissés | — | — |
| Prières pendant la messe (403-411), messe des morts (416-421), hymne *Adoro te* traduite (422-423), cantiques | **laissés** : méthode générale de la messe, textes du Missel, cantiques ; à reprendre si l'utilisateur les veut | — | — |

## 2. Bonne Mort — [Picard], *Petit manuel des Associés de l'Union de prières et de la Bonne Mort*, Montréal, 1873

- **Édition** : *Petit manuel des Associés de l'Union de prières et de la Bonne Mort*, Montréal, Eusèbe Senécal,
  imprimeur, 1873 (page de titre) ; attribué à Eustache Picard, p. s. s. (Canadiana) ; préface non signée ; **aucune
  approbation imprimée** dans l'exemplaire numérisé (statuts d'une confrérie paroissiale de Notre-Dame de Montréal,
  sous la direction du Séminaire de Saint-Sulpice). Microfiche CIHM n° 04796 (Bibliothèque nationale du Québec).
- **URL** : https://archive.org/details/cihm_04796 (page imprimée p = image n + 2 environ ; p. 14 = n12).
- **Contenu** (pas de table) : préface (5) ; avantages des deux associations (7) ; règlements, devoirs et indulgences de
  l'Union de prières et de bonnes œuvres (9-11 : chaque jour un *Pater* et un *Ave* pour le dernier associé défunt et
  pour celui qui doit mourir le premier, et l'invocation « Saint Joseph, priez pour nous ») ; règlements de la Confrérie
  de l'Adoration perpétuelle du Saint-Sacrement et de la Bonne Mort (12-22 : consécration de réception, pratiques —
  penser chaque jour à la mort, sept *Requiem* par jour, une demi-heure par semaine devant le Saint-Sacrement, confession
  et communion mensuelles, assemblée le premier samedi avec chapelet des morts et litanies de la bonne mort) ; amende
  honorable au Sacré Cœur (23) ; acte d'offrande et de consécration au Sacré-Cœur (25) ; *En ego* (28) ; acte héroïque
  (29-31) ; *Souvenez-vous* (32) ; liste des associés défunts depuis 1851 (33 et suiv.).

| Pièce | Statut | Id | Indulgence imprimée |
|---|---|---|---|
| Consécration à Notre-Seigneur au Saint-Sacrement, p. 14-15 | **nouvelle** | `picard1873:consecration-au-saint-sacrement` | plénière le jour de la réception |
| Amende honorable au Sacré Cœur de Jésus, p. 23-25 | **nouvelle** | `picard1873:amende-honorable-sacre-coeur` | — |
| Acte d'offrande et de consécration au Sacré-Cœur, avec *O Cor Jesu, amoris victima* (latin-français), p. 25-27 | **nouvelle** | `picard1873:acte-d-offrande-sacre-coeur` | — |
| Formule de l'acte héroïque (« O Marie, Mère de miséricorde… »), p. 31 | **nouvelle** (autre formule que `jardin:acte-heroique-de-charite`) | `picard1873:formule-acte-heroique` | Pie IX, 30 sept. 1852 (non compté) |
| *En ego* (« O bon et très-doux Jésus »), p. 28 ; *Souvenez-vous*, p. 32 | **déjà présents** (`jardin:chaque-vendredi-devant-le-crucifix`, `weber:souvenez-vous`) | — | plénière (Pie VII, 10 avril 1821) ; 100 j. et plénière mensuelle |
| Règlements, pratiques, liste des défunts | **laissés** (prose ; les pratiques servent à la proposition, § 7) | — | — |

## 3. Précieux Sang — *Nouveau manuel du Très-Précieux Sang… ou le Livre des élus*, Saint-Hyacinthe, 1890

- **Édition** : *Nouveau manuel du Très-Précieux Sang de Notre Seigneur Jésus-Christ, ou le Livre des élus, renfermant
  les plus belles pratiques et prières en l'honneur du sang adorable…*, Saint-Hyacinthe, Monastère du Précieux-Sang
  (Sœurs adoratrices du Précieux-Sang), 1890 ; « Approbation » : « Nous approuvons le Nouveau Manuel du Très Précieux
  Sang… et nous en permettons l'impression… St-Hyacinthe, 18 Déc. 1889. † L. Z. Év. de St-Hyacinthe » (p. [II]).
  Microfiche CIHM n° 92923 ; 701 images, ~650 p.
- **URL** : https://archive.org/details/cihm_92923 (image n = page + 11 environ dans la 1re moitié ; décalage différent
  après les mires de la microfiche, vers n388).
- **Table** (p. 653-662, très abîmée sur la microfiche) : partie préliminaire (fêtes mobiles, conditions des indulgences,
  nomenclature des confréries, calendrier et pieux souvenirs de chaque mois, indulgences apostoliques, du jubilé, des
  Quarante-Heures, neuvaine de la grâce) ; Ire partie : histoire et doctrine de la dévotion, Confrérie du Très-Précieux-
  Sang (érection, avantages, conditions), Garde d'honneur du Précieux-Sang ; IIe partie, la journée : prières du matin,
  litanies du saint Nom de Jésus, messe, repas, travail, invocations au Précieux-Sang, oraisons jaculatoires, chapelet
  (« Prions Marie »), **Horloge de la Passion** (193), litanies de la sainte Vierge (200), prière du soir (213) ; IIIe
  partie, l'adoration (une « heure » par chapitre) : devoirs des adorateurs, prières générales pour chaque heure (prière
  préparatoire à N.-D. du Précieux-Sang, **consécration au Précieux Sang** 231, amende honorable 233, communion
  spirituelle *Sitio* 237, prière pour les âmes du purgatoire et **offrande pour obtenir la bénédiction** 238), messes
  pour chaque jour de la semaine (248-335), hommages, **chapelet du Précieux-Sang** (350), litanies de Jésus agonisant,
  l'Heure sainte, conversion des pécheurs, visite au Saint-Sacrement, chemins de croix (494-535), clef du Paradis,
  Sacré-Cœur, rosaire (575), office du Précieux-Sang, sept joies et sept douleurs ; appendice (décrets d'érection et de
  translation de la Confrérie, 1850-1878 ; Garde d'honneur, 1888-1889).

| Pièce | Statut | Id | Indulgence imprimée (non comptée) |
|---|---|---|---|
| Horloge de la Passion et oraisons jaculatoires (de 7 h du soir à 6 h du soir), p. 193-200 | **nouvelle** | `precieuxsang1890:horloge-de-la-passion` | 40 j. par jaculatoire (év. de Saint-Hyacinthe) |
| Consécration au Précieux Sang, p. 231-232 | **nouvelle** | `precieuxsang1890:consecration-au-precieux-sang` | 40 j. (Saint-Hyacinthe) ; 100 j. (card. Taschereau) |
| Prière efficace pour la délivrance des âmes du purgatoire (« Ayez pitié, ô tendre Jésus », P. Ste Gertrude), p. 238 | **nouvelle** | `precieuxsang1890:priere-delivrance-ames-purgatoire` | 40 j. (Saint-Hyacinthe) |
| Offrande du Précieux Sang au Père éternel pour obtenir sa bénédiction, p. 238-239 | **nouvelle** | `precieuxsang1890:offrande-pere-eternel-benediction` | Léon XII, 25 oct. 1823 (rattachement à vérifier) |
| Chapelet de la Divine Miséricorde (« Mon Jésus, miséricorde »), p. 266 | **nouvelle** | `precieuxsang1890:chapelet-divine-misericorde` | Pie IX, 26 sept. 1846 |
| Chapelet du Précieux-Sang, sept mystères avec considérations et prières, prière finale « O Sang très-précieux » et oraison, p. 350-355 | **nouvelle forme** : la forme brève (« Couronne des trente-trois années ») et l'oraison sont déjà dans `boylesve1882:petit-chapelet-precieux-sang` ; la forme longue est propre au manuel | `precieuxsang1890:chapelet-du-precieux-sang` | 7 ans et 7 quarantaines ; 300 j. ; 40 j. |
| Prière de sainte Catherine de Sienne au Précieux Sang, p. 556 | **nouvelle** | `precieuxsang1890:priere-sainte-catherine-precieux-sang` | — |
| Sept offrandes du Précieux Sang (p. 187-189 env.) | **déjà présentes** (`jardin:les-sept-offrandes-du-precieux-sang`) | — | — |
| Litanies de Jésus agonisant (p. 375), neuvaine de la grâce (préliminaire), Heure sainte, amende honorable (233), communion spirituelle *Sitio* (237), prière du matin et du soir propres, messes pour chaque jour de la semaine, chemins de croix, office du Précieux-Sang | **laissés pour ce lot** : la microfiche est très abîmée vers n388 (mires intercalées, décalage des images à refaire) ; les litanies de Jésus agonisant et l'amende honorable sont les premières à reprendre. Les « neuvaines » annoncées ne sont, dans ce manuel, qu'une neuvaine de la grâce à saint François Xavier signalée dans la partie préliminaire, sans texte propre trouvé | — | — |
| Instructions, histoire, considérations en prose | laissées, comme demandé | — | — |

## 4. Saint-Sacrement — *Petit manuel des adorateurs et des adoratrices du Très Saint Sacrement*, Québec, 1920

- **Édition** : *Petit manuel des adorateurs et des adoratrices du Très Saint Sacrement de Notre-Dame du Chemin*,
  Québec, Notre-Dame du Chemin, 1920 ; dédicace « A nos paroissiens… fruit de nos retraites d'automne », signée Joseph
  Waddel, S. J. (p. [3]) ; **pas d'approbation ni d'imprimatur imprimés** dans l'exemplaire numérisé (paroisse jésuite de
  Québec ; manuel d'une association paroissiale d'adoration, non d'une archiconfrérie). 52 p. Microfiche CIHM n° 78894
  (Bibliothèque nationale du Canada).
- **URL** : https://archive.org/details/cihm_78894 (la couche texte est décalée de trois images sur les images
  `page/n<N>.jpg` : texte du feuillet L = image n(L-4)).
- **Table** (p. 52) : 1re méthode, Heure-sainte du Saint-Rosaire (3-19 : quinze mystères avec offrandes de chaque
  dizaine, petite consécration au Sacré-Cœur, amende honorable au Très Saint-Sacrement, consécration pour les associés du
  Sacré-Cœur, *Anima Christi*, *En ego*) ; 2e méthode, programme et prières (20-30 : actes dialogués, prière sur les
  promesses, communion quotidienne, louanges) ; 3e méthode, les quatre fins du sacrifice d'après le P. Eymard (31-52 :
  lectures pour l'adoration, l'action de grâces, la réparation, la supplication ; acclamations ; amende honorable ;
  « Nous vous consolerons » ; litanies du Sacré-Cœur ; consécration du genre humain).

| Pièce | Statut | Id | Indulgence imprimée |
|---|---|---|---|
| Amende honorable à N.-S. au Très Saint-Sacrement (« Pardon, Seigneur, pardon ! »), p. 14-16 | **nouvelle** | `ndchemin1920:amende-honorable-tres-saint-sacrement` | — |
| Consécration au Sacré-Cœur pour les Associés, p. 17 | **nouvelle** | `ndchemin1920:consecration-sacre-coeur-associes` | — |
| Heure d'adoration dialoguée (P./T.), p. 20-26 | **nouvelle** | `ndchemin1920:heure-d-adoration-dialoguee` | — |
| Prière fondée sur les promesses à la B. Marguerite-Marie (« Seigneur, vous nous l'avez promis »), p. 27-28 | **nouvelle** | `ndchemin1920:priere-promesses-sacre-coeur` | — |
| Prière pour la communion quotidienne, p. 28-29 | **nouvelle** (prière de la S. C. des Indulgences, 1905 : à rapprocher de l'Enchiridion) | `ndchemin1920:priere-pour-la-communion-quotidienne` | — |
| Acclamations (« Seigneur, nous vous adorons ! »), p. 33-34 | **nouvelle** | `ndchemin1920:acclamations-adoration` | — |
| Amende honorable à Jésus-Christ présent dans le Sacrement de l'autel, p. 38-39 | **nouvelle** | `ndchemin1920:amende-honorable-jesus-present` | 300 j. (non compté) |
| Acte de consécration du genre humain au Sacré-Cœur (Léon XIII, 1899), p. 51-52 | **nouvelle** dans `sources.json` (forme de 1899, antérieure aux additions de 1925) | `ndchemin1920:consecration-genre-humain-sacre-coeur` | — |
| Petite consécration au Sacré-Cœur (sainte Marguerite-Marie), p. 10-11 | **déjà présente** (`recueils/mois-sacre-coeur` J:18, `breviaire-sc:exercice-messe`) | — | — |
| « Nous vous consolerons, Seigneur », p. 42-44 | **déjà présente** (`garde1886:priere-reparatrice`) | — | — |
| Louanges « Dieu soit béni » (p. 30), litanies du Sacré-Cœur (47-50), *Anima Christi*, *En ego*, offrandes des dizaines du rosaire (`montfort:methode-rosaire`) | **déjà présents** | — | — |
| Lectures du P. Eymard (31-49) | laissées (prose) | — | — |

## 5. N.-D. du Perpétuel Secours — Montréal, 1878

- **Édition** : [Un Père rédemptoriste], *Notre-Dame du Perpétuel-Secours, vierge miraculeuse vénérée à Rome, dans
  l'église de S.-Alphonse de Liguori et en beaucoup d'autres lieux : son histoire, archiconfrérie et exercices de piété en
  son honneur*, Montréal, J.-B. Rolland et fils, 1878 ; approbations et imprimatur de Montréal en tête (audit FR du
  22 nov.). Microfiche CIHM n° 52280.
- **URL** : https://archive.org/details/cihm_52280 (la couche texte est décalée de deux feuillets sur les images
  `page/n<N>.jpg` ; p. 143 = image n146 ; les « p. 182-217 » de l'audit du 22 nov. étaient des numéros d'image).
- **Plan** : Ire partie, histoire de l'image miraculeuse ; IIe partie, l'Archiconfrérie (érection, indulgences,
  consécration, p. 143-144) ; IIIe partie, exercices de piété : ch. I, trois prières indulgenciées de S. Alphonse
  (145-150) ; ch. II, sept prières générales pour demander les grâces nécessaires au salut (151-166) ; ch. III, « prières
  spéciales appropriées à toutes les demandes » (167-205 : trente prières, presque toutes suivies d'une oraison
  jaculatoire) ; appendice, cantiques (206 et suiv.).

| Pièce | Statut | Id |
|---|---|---|
| Consécration à N.-D. du Perpétuel-Secours (Archiconfrérie, avec S. Alphonse), p. 143-144 | **nouvelle** (40 j. imprimés, non comptés) | `perpetuelsecours1878:consecration-archiconfrerie` |
| Trois prières indulgenciées de S. Alphonse, p. 145-150 | **déjà présentes** (`weber:trois-prieres-perpetuel-secours`, Beringer) | — |
| Ch. II, I-VII : douze invocations ; prière à réciter fréquemment ; confiance en Jésus et en Marie ; grâce de toujours prier ; toutes les grâces nécessaires au salut ; persévérance ; bonne mort, p. 151-165 | **nouvelles** | `perpetuelsecours1878:douze-invocations`, `-priere-a-reciter-frequemment`, `-confiance-en-jesus-et-marie`, `-grace-de-toujours-prier`, `-toutes-les-graces-necessaires-au-salut`, `-obtenir-la-perseverance`, `-pour-obtenir-une-bonne-mort` |
| Ch. III, I-XXX : secours en toutes choses (« Venez à mon secours, ô charitable Mère ! ») ; jaculatoires pour les circonstances de la journée ; tiédeur ; acquérir une vertu ; amour divin ; se donner à Dieu sans réserve ; circonstance embarrassante ; vocation ; tentation ; répugnance à un devoir ; peines intérieures ; persécution ; après une faute ; extirpation d'un vice ; occasion ou lien funeste ; sacrilége ; état de péché sans envie d'en sortir ; hommes sans religion ; délai de la conversion ; maladies ; pauvreté ; chagrins de famille ; mort d'une personne chère ; conservation de la foi et nécessités de l'Église ; l'Église et le Souverain-Pontife ; pasteurs ; conversion de personnes ; âmes du purgatoire ; âmes les plus oubliées ; zèle pour leur délivrance, p. 167-205 | **nouvelles** (30 pièces ; chaque oraison jaculatoire gardée avec sa prière) | `perpetuelsecours1878:secours-en-toutes-choses` … `-zele-pour-les-ames-du-purgatoire` |
| Cantiques, histoire | laissés | — |

## 6. Neuvaines et séries à jours comptés repérées (pour l'agent chargé de leur intégration)

Aucune neuvaine **en prières** n'a été transcrite dans ce lot. Repérées dans ces manuels :

- **Lefebvre 1870** : deux *Neuvaines à saint Joseph* (p. 293-392) : neuf méditations sur les vertus (foi … pureté),
  puis neuf sur trois titres, trois mystères et trois vertus de saint Joseph ; ce sont des **instructions en prose**
  (lectures), sans prières propres, à prendre comme lectures d'une neuvaine de mars si on le veut ; l'association
  « se prépare par une neuvaine solennelle » à ses fêtes (pas de texte).
- **Précieux-Sang 1890**, calendrier de la partie préliminaire : **sept vendredis du Carême** (un objet de la Passion
  par vendredi : sainte Couronne d'épines, sainte Lance et saints Clous, cinq Plaies… ; renvoi au « Vendredi » de la
  IIIe partie) ; **six vendredis préparatoires à la fête du Sacré-Cœur** (plénière chaque vendredi) ; **neuvaine de la
  grâce** à saint François-Xavier (du 4 au 12 mars ; renvoi « à la fin de décembre », non trouvé sur la microfiche) ;
  « Prières pour la neuvaine et le mois du Précieux-Sang » (pratique annoncée, texte non retrouvé dans la partie
  lisible) ; **prière à réciter pendant trente jours** pour obtenir une grâce particulière (« Sainte Marie, Vierge des
  vierges, Mère de… », p. 606, « pourrait être récitée chacun des jours du mois de Marie ») : absente du projet,
  **non transcrite** (fin de microfiche abîmée), à reprendre.
- **Perpétuel-Secours 1878** : seulement des triduums historiques (récit), pas de texte de neuvaine.
- **Petit manuel de l'Union de prières 1873** : assemblées le premier samedi du mois (chapelet des morts, litanies de la
  bonne mort) et le dimanche après chaque annonce des Quatre-Temps ; chaque associé : un *Pater* et un *Ave* par jour
  pour le dernier associé défunt et pour celui qui doit mourir le premier, « Saint Joseph, priez pour nous » ; huit
  jours de prières pour un associé défunt, puis huit pour celui qui doit mourir le premier.

## 7. Proposition d'intégration

**Appliquée le 26 nov.** (décision de l'utilisateur : propositions 1, 2, 3 et la consécration du Perpétuel-Secours ;
branche `claude/archi-lot-a-integration`) :

- **Litanies du vendredi** : `roue:litanies-5` (seed `LITANIES_PAR_JOUR` et `parmi` de `prog:devotion-vendredi`) passe à
  quatre litanies : Sacré-Cœur, Sept-Douleurs (livret), Passion et Sept-Douleurs de Lefebvre ; une par semaine. La roue
  déjà installée n'est mise à jour que si l'utilisateur ne l'a pas modifiée.
- **Premier vendredi** : dans `prog:devotion-vendredi` (`semaines_du_mois: [1]`), un texte de préparation à la mort par
  mois, rotation déterministe `unite: 'mois'` : protestation de S. Alphonse, testament de S. Charles, prière de
  S. Vincent Ferrier, autre testament, *Ave candidum*.
- **Novembre** : à la fin de la prière du soir (`prog:ames-du-soir`, déjà la prière du jour pour les âmes), en alternance
  hebdomadaire, `perpetuelsecours1878:ames-les-plus-oubliees` et `precieuxsang1890:priere-delivrance-ames-purgatoire`.
- **Consécrations des fêtes** (`prog:consecrations-fetes`, fin de la prière du matin) : la consécration au Précieux Sang
  le 1er juillet ; la consécration de l'Archiconfrérie de N.-D. du Perpétuel-Secours le jour de sa fête. Cette fête
  n'est pas dans le calendrier de 1954 du projet (`data/calendar`) ; date retenue d'après le manuel lui-même, p. 141 :
  « le jour de la fête de Notre-Dame du Perpétuel-Secours, fixée au dimanche qui précède le 24 Juin » (vu sur l'image),
  soit le dimanche du 17 au 23 juin.
- Classement deviné (`devinee`) ajouté dans `dimensions-textes.json` pour les onze textes branchés ; tests dans
  `journee.test.ts` (« lot A des archiconfréries intégré »), unicité vérifiée sur l'année.

Proposition initiale :

« Le moins pour le plus, le simple mais le saint, la variété mais la sobriété. » Aucune ligne quotidienne nouvelle ;
on prolonge des séquences existantes. Rien n'est écrit dans `programme.json` ni dans `dimensions-textes.json`.

1. **Litanies du jour** (roue des litanies, déjà en place) : ajouter à la rotation `lefebvre1870:litanies-de-la-passion`
   (vendredi) et une des deux litanies des Sept-Douleurs de Lefebvre (vendredi ou septembre), en alternance avec
   `jardin:litanies-de-notre-dame-des-sept-douleurs`. Coût nul : la ligne existe.
2. **Préparation à la mort, une fois le mois** (pratique de l'Association de la Bonne Mort, Lefebvre et Bona Mors) :
   le jour de la retraite du mois ou le premier vendredi, un seul texte en rotation mensuelle : protestation de
   S. Alphonse, testament spirituel de S. Charles, prière de S. Vincent Ferrier, *Ave candidum* de sainte Gertrude.
   La recommandation de l'âme (`lefebvre1870:priere-pour-les-agonisants`) reste au recueil, ouverte quand on veille un
   mourant ; la messe pour une bonne mort, au recueil (ou le jour de la messe votive, si un jour en est marqué).
3. **Novembre / défunts** : `perpetuelsecours1878:ames-les-plus-oubliees` et `precieuxsang1890:priere-delivrance-ames-purgatoire`
   en insertion du mois de novembre (une par semaine), sans nouvelle ligne ; le chapelet de la Divine Miséricorde
   comme forme possible du chapelet des morts du lundi, au choix.
4. **Premier vendredi du mois** : `ndchemin1920:priere-promesses-sacre-coeur` (« Seigneur, vous nous l'avez promis »)
   après l'acte de réparation déjà prévu ; l'une des deux amendes honorables de Notre-Dame du Chemin en alternance avec
   celle de la Garde d'honneur (proposition du 22 nov.).
5. **Juillet (mois du Précieux Sang)** : l'Horloge de la Passion n'est pas quotidienne ; proposer la jaculatoire de
   trois heures (« Que Jésus soit à jamais béni… ») à l'insertion de 15 h du vendredi, et la consécration au Précieux
   Sang (`precieuxsang1890:consecration-au-precieux-sang`) le 1er juillet ; le chapelet long, au recueil, la forme
   brève (Boylesve) restant celle du mois.
6. **Perpétuel Secours** (fête le dimanche avant la Saint-Jean, ou le 27 juin selon les propres) : la consécration de
   l'Archiconfrérie ce jour-là ; les trente « prières spéciales » forment un **recueil de circonstance** (tentation,
   maladie, deuil, chagrins de famille, vocation…), consultable depuis la fiche du jour, sans ligne au programme ; on
   peut proposer l'invocation « Venez à mon secours » en insertion du mercredi (dévotion rédemptoriste) une fois la
   semaine.
7. Le reste (testaments, prières à saint Joseph et aux anges, actes dialogués d'adoration, acclamations, consécration
   du genre humain de 1899) : recueil, sans ligne.

Pas de classement deviné ajouté : à faire, si l'utilisateur retient une de ces propositions, dans
`data/prieres/dimensions-textes.json` (statut `devinee`).

## 8. Indulgences

Toutes les indulgences imprimées sont reportées dans le champ `indulgence` des pièces, **non comptées** (SPEC § 11 :
seule l'*Enchiridion* de 1952 fait foi ; concessions épiscopales et de confrérie signalées seulement). À vérifier dans
l'Enchiridion : amende honorable à Jésus-Christ présent dans le Sacrement de l'autel (300 j.), offrande du Précieux Sang
pour obtenir la bénédiction (Léon XII, 1823), chapelet de la Divine Miséricorde (Pie IX, 1846), chapelet du
Précieux-Sang (7 ans et 7 quarantaines), consécration à N.-D. du Perpétuel-Secours (40 j.).

### Vérification dans l'Enchiridion de 1952 (27 nov. 2026)

Chaque page vue sur l'image (archive.org `enchiridion_indulgentiarum_1952`, page imprimée p = image n − 15 dans le
corps du livre, n − 19 à partir de la p. 300 environ). Seule l'*Enchiridion* fait foi (SPEC § 11) ; aucune concession
ci-dessous n'y est reprise : **aucune indulgence comptée**, le verdict est dans `indulgences.json` › `sans_compte`
(affiché à la place d'une indulgence, comme pour le chapelet de saint Michel) et la mention du manuel ne s'affiche plus
en marge (`revision` des pièces incrémentée).

| Pièce | Imprimé par le manuel | Enchiridion 1952 |
|---|---|---|
| Amende honorable à Jésus-Christ présent dans le Sacrement de l'autel (`ndchemin1920:amende-honorable-jesus-present`) | 300 j. | **absente** : actes de réparation au Saint-Sacrement n° 173-174 (p. 101), 177-179 (p. 102-108 : *Io vi adoro, Eterno Padre* ; *Vi adoro profondamente* ; *Con quella profonda umiltà*), autres textes ; index « Reparatio », « Reparationis actus » (p. 633-634) ; aucune concession en français de ce texte |
| Offrande du Précieux Sang au Père éternel pour obtenir sa bénédiction (`precieuxsang1890:offrande-pere-eternel-benediction`) | Léon XII, rescrit du 25 oct. 1823 ; 100 j. et plénière mensuelle, offrande « en l'honneur de la Très-Sainte Trinité » (p. 239, vu) | **absente** : Précieux Sang n° 215-222 (p. 138-145 : *Te ergo*, *Salvete Christi vulnera*, mois de juillet, *O Sangue prezioso*, *Eterno Padre, io vi offro il Sangue* n° 219, sept offrandes n° 220, n° 221, n° 222) ; index « Sanguis D. N. I. C. » (p. 636), « Trinitas » ; seules concessions de Léon XII reprises (couche texte) : n° 50 (9 juil. 1828) et n° 336 (21 oct. 1823, consécration à Marie), autres textes |
| Chapelet de la Divine Miséricorde (`precieuxsang1890:chapelet-divine-misericorde`) | Pie IX, 26 sept. 1846 | **chapelet absent** (index « Corona », p. 621 : seulement n° 255, 286, 330, 395) ; la jaculatoire « Gesù mio, misericordia » est le n° 70 (p. 32 : 300 j. ; S. C. Indulg., 24 sept. 1846), déjà comptée seule (`thesaurisons:jac-33`, *Thésaurisons* n° 33, p. 29, même français « Mon Jésus, miséricorde ») |
| Chapelet du Précieux-Sang, forme longue (`precieuxsang1890:chapelet-du-precieux-sang`) et petit chapelet de Boylesve (`boylesve1882:petit-chapelet-precieux-sang`) | 7 ans et 7 quarantaines ; 300 j. (prière finale) | **chapelet absent** (index « Corona » ; n° 215-222). Ses parties y sont : *Te ergo* (n° 215, 300 j., en latin), la prière finale (n° 218, 500 j.), l'oraison (n° 222, 5 ans) ; mais le français du manuel de 1890 n'est pas la traduction approuvée (*Thésaurisons* n° 236, 237 = Beringer n° 394, et n° 81, p. 40-41 et 92-93, autres formules) et l'oraison latine de Boylesve n'a pas le « solemni cultu » de 1952 |
| Consécration à N.-D. du Perpétuel-Secours (40 j.) | indulgence épiscopale | non cherchée : concession d'Ordinaire, jamais comptée (SPEC § 11) |

Proposition pour l'utilisateur (rien n'est fait) : compter, dans les deux chapelets, les invocations indulgenciées
répétées (SPEC § 10, correction 2) ? Le chapelet de la Divine Miséricorde redit « Mon Jésus, miséricorde » sur chaque
petit grain (n° 70, 300 j. chacun), mais le manuel ne dit pas le nombre de grains (« chapelet ordinaire ») ; le
*Te ergo* latin du chapelet du Précieux-Sang est dit sept fois (n° 215, 300 j.). **Recommandation : non**, ces pièces
restent au recueil et ne sont pas au programme ; à reprendre si l'utilisateur en branche une.

### Précieux Sang 1890 : litanies et amende honorable (27 nov. 2026)

Les deux pièces « laissées » au § 3 sont lisibles sur la microfiche (`cihm_92923`), et transcrites sur l'image :
`precieuxsang1890:litanies-de-jesus-agonisant` (p. 371-372, images n385 et n390 ; le manuel les tire du « Manuel du
Cœur agonisant de Jésus ») et `precieuxsang1890:amende-honorable-adorateurs` (p. 233-237, images n243-n247 ; « Prières
générales pour chaque heure de l'adoration »). Coquilles rétablies et notées dans le champ `page` : « l[e] profanent »,
« coulez[,] ô », « che[rs] » (lettres non encrées), « Jesus » sans accent. Un autre exemplaire a été cherché :
Canadiana `oocihm.92923` (IIIF) n'est que la même microfiche ; archive.org n'a que `cihm_92923` ; Google Livres (API
hors quota) et BAnQ sans résultat. Non branchées : à proposer (litanies pour les agonisants, par ex. le premier vendredi
avec la préparation à la mort ; amende honorable en juillet ou à l'heure sainte). Restent au manuel : messes de la
semaine, chemins de croix, office (les dévotions à jours comptés sont à l'agent des neuvaines).
