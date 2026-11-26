# Manuels d'archiconfréries, lot A — 25 novembre 2026

Demande de l'utilisateur du 25 nov. : finir l'OCR des manuels d'archiconfréries et d'associations pieuses trouvés
(`ARCHICONFRERIES_FR_2026-11-22.md` § 4), puis en extraire et classer le contenu. Lot A : Bonne Mort (Lefebvre 1870,
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

Préfixes : `lefebvre1870:` (Bonne Mort, Paris).

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
