# Neuvaines et dévotions à jours comptés (26 novembre 2026)

Demande de l'utilisateur (26 nov.) : « Ajoute en priorité chaque neuvaine, douzaine, trentaine ou autre dévotion à
jours comptés que tu trouves dans les différents manuels. Je sais que dans le Bréviaire du Sacré-Cœur il doit y avoir
une neuvaine avant chaque premier vendredi du mois. Pour le reste aussi. »

Branche `claude/neuvaines`. Méthode : inventaire du corpus (`data/prieres/sources.json`, `jardin.json`,
`data/recueils/*`, Petit bréviaire du Sacré-Cœur) et des manuels déjà repérés (Beringer 1925, Janvier 1895, Québec
1867, audits des archiconfréries). Aucun texte de mémoire : les textes intégrés sont ceux du corpus, ou relus sur
l'image du scan (Beringer n° 671).

## 1. Ce qui change dans le moteur

`Quand` reçoit **une** clé typée, `autour` (`app/src/lib/programme/types.ts`, `quand.ts`) : jours comptés à partir d'un
jour d'ancrage, `de` et `a` en jours (compris).

| Ancre | Sens | Exemple |
|---|---|---|
| `"MM-JJ"` | fête fixe, chaque année | `{ ancre: "08-13", de: -35, a: -1 }` + `jours_semaine: [0]` = les cinq dimanches avant le 13 août |
| `{ jour: n }` | le n-ième jour de chaque mois | `{ ancre: { jour: 1 }, de: 0, a: 8 }` = du 1er au 9 |
| `{ rang, jour_semaine }` | le rang-ième jour de semaine de chaque mois | `{ ancre: { rang: 1, jour_semaine: 5 }, de: -9, a: -1 }` = les neuf jours qui finissent la veille du premier vendredi |

Fonction pure, déterministe ; les fêtes mobiles restent en `code_tempora`, les fêtes fixes simples en `dates`. Test :
`journee.test.ts › quand › autour` (passage d'une année civile à l'autre compris).

## 2. Intégrées dans ce lot

| Ligne du programme | Texte et source | Jours (année 2026-2027) | Partie du jour | Indulgence |
|---|---|---|---|---|
| `prog:neuvaine-premier-vendredi` (journée, 76) | `breviaire-sc:neuvaine` : *Petit bréviaire du Sacré-Cœur de Jésus*, 13e éd., Nancy, Le Chevallier, imprimatur 21 mars 1883, p. 151-155 (PDF fourni par l'utilisateur, déjà transcrit et relu page à page, commit `11859ca`) ; le 9e jour, amende honorable et consécration au Sacré-Cœur **du même livre** (fin de l'exercice pour la messe, `breviaire-sc:exercice-messe`, p. 119-140), comme le demande la rubrique (« terminer par une Amende honorable et une Consécration au Sacré-Cœur de Jésus ») | les 9 jours qui finissent le jeudi, veille du premier vendredi : 25 nov.-3 déc. 2026 (dans l'année : 29 nov.-3 déc.), 23-31 déc. 2026, 27 janv.-4 févr., 24 févr.-4 mars, 24 mars-1er avr., 28 avr.-6 mai, 26 mai-3 juin, 23 juin-1er juill., 28 juill.-5 août, 25 août-2 sept., 22-30 sept., 27 oct.-4 nov. 2027 (et 24-27 nov. 2027 pour le 3 déc.) | intentions et rubrique en notice repliée ; titre « Premier jour »… par `autour` ; prières de la neuvaine chaque jour ; amende honorable et consécration le 9e jour | Ench. 1952, n° 250 (neuvaine au Sacré-Cœur, prières quelconques, 7 ans une fois le jour) : **non ajoutée** à `indulgences.json` — elle y est déjà sur `liguori:neuvaine-sacre-coeur`, et les deux neuvaines tombent les mêmes jours en 2027 (26 mai-3 juin) : la compter deux fois serait faux. À trancher (§ 5) |
| `prog:neuvaine-reparation-sacre-coeur` (insertion, fin de la prière du matin) | `beringer:neuvaine-reparation-sacre-coeur` (**nouvelle**) : offrande « Divin Cœur de Jésus, je vous offre, par le Cœur compatissant de Marie… », Beringer, *Les Indulgences*, trad. Mazoyer, 4e éd., Paris, Lethielleux, 1925, t. I, n° 671, p. 353, relue sur l'image (archive.org `lesindulgences0001beri`, n368) | du 1er au 9 de chaque mois (108 jours dans l'année) | l'offrande du jour, « On offre chacun de ces jours en récitant cette prière » | Pie X, 1907 (Beringer) ; non retrouvée dans les fiches de 1952 : dans le champ `indulgence`, **non comptée** |
| `prog:neuvaine-sainte-face` (journée, 76) | `janvier:neuvaine-meditations-sainte-face` (déjà transcrite) : abbé Janvier, *Manuel de l'Archiconfrérie de la Sainte-Face*, 3e éd., Tours, 1895, p. 112-142 | 20-28 juin 2027. Le livre ne date pas la neuvaine ; **arbitrage** : avant la fête principale de l'Archiconfrérie, saint Pierre (29 juin ; art. V de l'érection, p. 65-66) | la méditation du jour (`extrait.section`) ; les jours 2 à 8, l'ouverture et les prières du premier jour, auxquelles le livre renvoie (« Voir le Ier jour ») : extraits du 1er jour, renvois retirés à l'affichage (`retirer`) | aucune propre |
| `prog:cinq-dimanches-berchmans` (journée, 75) | `jardin:cinq-dimanches-de-saint-jean-berchmans` (*Jardin de l'âme*, p. 63 ; Beringer 1905, n° 294) | 11 juill.-8 août 2027 (les cinq dimanches avant le 13 août) | titre « Premier dimanche »… ; la pratique et l'invocation | celle du livret (Ench. 1952, n° 526, dans la fiche du livret) |
| `prog:dix-dimanches-stanislas` (journée, 75) | `jardin:dix-dimanches-de-saint-stanislas-kostka` (*Jardin de l'âme*, p. 66 ; Beringer 1905, n° 179) | 5 sept.-7 nov. 2027 (les dix dimanches avant le 13 novembre) | titre « Premier dimanche »… ; les trois prières | celle du livret (Ench. 1952, n° 502) |

Berchmans et Stanislas étaient au catalogue du planificateur (`engine/hebdo/devotions.py`), mais écartés parce qu'ils
recouvrent d'autres dimanches (Ignace ; Stigmates, Immaculée Conception) : l'utilisateur veut garder les recouvrements,
ils deviennent des lignes du programme, indépendantes du plan.

Classements devinés ajoutés (`data/prieres/dimensions-textes.json`, `devinee`, à relire, D2) :
`breviaire-sc:neuvaine`, `breviaire-sc:exercice-messe`, `beringer:neuvaine-reparation-sacre-coeur`,
`janvier:neuvaine-meditations-sainte-face`, `jardin:cinq-dimanches-de-saint-jean-berchmans`,
`jardin:dix-dimanches-de-saint-stanislas-kostka`.

## 3. Déjà intégrées avant ce lot (rappel)

| Dévotion | Comment | Jours 2026-2027 |
|---|---|---|
| Neuvaine à l'Immaculée Conception (Weber 1899) | plan, `rang_du_jour` | 29 nov.-7 déc. 2026 |
| Premier mercredi (S. Joseph) | plan, annote le mercredi | 1er mercredi |
| Heure sainte, veille du premier vendredi | plan, annote le jeudi | 1er jeudi… veille |
| Neuf premiers vendredis (acte de réparation, promesse) | plan, ligne propre | 1er vendredi |
| Cinq premiers samedis | plan, annote le chapelet | 1er samedi |
| Neuvaine de Noël (S. Alphonse, 1897) | plan, `rang_du_jour` | 16-24 déc. 2026 |
| Six dimanches de S. Thomas d'Aquin | plan | 20 déc. 2026-24 janv. 2027 |
| Treize vendredis de S. François de Paule | plan, annote le vendredi | 8 janv.-2 avr. |
| Sept dimanches de S. Joseph | plan | 31 janv.-14 mars |
| Préparation de Montfort (33 jours) et consécration | plan, `rangs` | 3 mars-5 avr. |
| Neuvaine à S. Joseph ; à S. Gabriel | plan (Douleurs et Allégresses ; prière à S. Gabriel) | 10-18 mars ; 15-23 mars |
| Treize mardis de S. Antoine | plan (répons *Si quæris*) | 16 mars-8 juin |
| Six dimanches de S. Louis de Gonzague | plan | 11 avr.-16 mai |
| Quinze samedis du Rosaire | plan, annote le chapelet | 17 avr.-24 juill. |
| Neuvaine à S. Louis-Marie Grignion de Montfort | plan, annote la prière du matin : **prière à fournir** | 19-27 avr. |
| Neuvaine au Saint-Esprit ; Veni Creator | plan | 7-15 mai ; 16 mai |
| Neuvaine à la très sainte Trinité (Beringer, Marmion) | `prog:neuvaine-trinite`, `code_tempora` | 15-23 mai |
| Dix dimanches de S. Ignace | plan | 23 mai-25 juill. |
| Neuvaine au Sacré-Cœur (S. Alphonse, 1884) | plan, `rang_du_jour` | 26 mai-3 juin |
| Quinze mardis de S. Dominique | plan | 15 juin-21 sept. |
| Sept vendredis des Douleurs ; Sept samedis de N.-D. de la Merci | plan | 30 juill.-10 sept. ; 31 juill.-11 sept. |
| Neuvaines de l'Assomption et de la Nativité (Lévis 1886) | plan | 6-14 août ; 30 août-7 sept. |
| Cinq dimanches des Stigmates | plan | 15 août-12 sept. |
| Douze samedis avant l'Immaculée Conception | plan, annote le chapelet | 18 sept.-27 nov. |
| Neuvaines à S. Michel, du Rosaire, de la Toussaint | plan (chapelet de S. Michel ; chapelet et litanies ; litanies des saints) | 20-28 sept. ; 28 sept.-6 oct. ; 23-31 oct. |
| Sept dimanches de l'Immaculée Conception | plan | 10 oct.-21 nov. |
| Mois (Marie, Sacré-Cœur, Précieux Sang, âmes…) | méditation du mois (`meditations.ts`) | chaque mois |

## 4. Recouvrements (gardés, comme l'utilisateur le veut)

- **29 nov.-3 déc. 2026** : neuvaine du premier vendredi, neuvaine de l'Immaculée Conception, neuvaine de réparation
  (1er-9 déc.) ; **23-24 déc.** : avec la neuvaine de Noël ; **25 déc.** : la neuvaine du premier vendredi (1er janv.
  2027) court sur Noël et son octave.
- **24 mars-1er avr. 2027** : la neuvaine du premier vendredi (2 avril) traverse la Semaine sainte et Pâques (28 mars) ;
  elle recouvre aussi la préparation de Montfort.
- **26 mai-3 juin 2027** : deux neuvaines au Sacré-Cœur les mêmes jours (Petit bréviaire, pour le premier vendredi
  4 juin, qui est aussi la fête du Sacré-Cœur ; S. Alphonse, pour la fête). Pas de doublon de texte ; indulgence
  n° 250 comptée une seule fois (sur S. Alphonse).
- **20-28 juin** : neuvaine de la sainte Face ; **23 juin-1er juill.** : neuvaine du premier vendredi.
- **Dimanches** : Berchmans (11 juill.-8 août) avec S. Ignace (jusqu'au 25 juill.) ; Stanislas (5 sept.-7 nov.) avec
  les Stigmates (jusqu'au 12 sept.) et les Sept dimanches de l'Immaculée Conception (10 oct.-21 nov.).
- **22-30 sept.** : neuvaine du premier vendredi avec S. Michel (20-28) et le Rosaire (28 sept.-6 oct.).
- **Du 1er au 9 de chaque mois** : neuvaine de réparation avec le premier vendredi, le premier samedi, le premier
  mercredi, et souvent la neuvaine du premier vendredi.

Unicité vérifiée sur toute l'année 2026-2027 (`unicite.test.ts`) : aucun texte deux fois le même jour.

## 5. À trancher par l'utilisateur

1. **Indulgence de la neuvaine du premier vendredi** : Ench. 1952, n° 250 vaut pour toute neuvaine au Sacré-Cœur
   (prières quelconques). L'ajouter à `indulgences.json` la compterait aussi du 26 mai au 3 juin, en double avec celle
   de S. Alphonse. Proposition : l'ajouter et retirer ces jours-là celle de S. Alphonse, ou laisser ainsi.
2. **Date de la neuvaine de la sainte Face** : avant saint Pierre (choisi), ou avant la fête de la sainte Face du mardi
   de la Quinquagésime (jour des consécrations de l'app, `Quadp3-2`).
3. **Sept dimanches de S. Camille de Lellis** (`jardin:sept-dimanches-de-saint-camille-de-lellis`) : « sept dim.
   consécutifs », sans fête d'attache dans le livret ni dans Beringer : non datés, non intégrés. Une date à choisir
   (avant sa fête, 18 juillet ?).

## 6. À transcrire (scan déjà repéré)

| Dévotion | Source | Jours | Note |
|---|---|---|---|
| Neuvaine en l'honneur de S. François d'Assise (hymne, méditation et prière de chaque jour, répons des stigmates) | *Notice sur le Tiers-Ordre de la pénitence de Saint-François d'Assise, suivie de neuvaines, litanies, etc.*, Québec, 1867, p. 37-51 | 25 sept.-3 oct. (fête le 4 oct.) | archive.org `cihm_29653` (PDF p. 43-57) ; OCR médiocre (encre du verso) : relire chaque page sur l'image |
| Neuvaine en l'honneur de sainte Élisabeth de Hongrie | même notice, p. 52-60 | 10-18 nov. (fête le 19 nov.) | `cihm_29653` (PDF p. 58-71) |
| Neuvaine préparatoire aux fêtes de S. Joseph ; neuvaine pour des grâces particulières ; prières des premiers dimanches et des mercredis ; mois de S. Joseph | *Manuel de la Confrérie de Saint-Joseph*, Montréal, s. d. (`docs/audits/ARCHICONFRERIES_LOT_B_2026-11-25.md`) | 10-18 mars ; mars | archive.org `cihm_61528`, p. 37, 45, 65, 89, 117 |
| Litanies, prière et neuvaine de S. François (Cordon, 1878) | anglais ; le français est la notice de Québec 1867 ci-dessus | — | voir lot B |

## 7. Sans texte propre (prières au choix) ou introuvables

Beringer 1925, t. I (archive.org `lesindulgences0001beri`) donne pour ces neuvaines la seule concession, « en récitant
n'importe quelles prières approuvées » : pas de texte à transcrire ; une ligne ne s'ajoute que si l'utilisateur choisit
les prières.

| Dévotion | Beringer | Jours | État |
|---|---|---|---|
| Neuvaine au Saint-Esprit ; neuvaine et octave de la Pentecôte | n° 642-643 | vendredi après l'Ascension → vigile | au plan (Veni Creator) ; la neuvaine de S. Alphonse (dix méditations sur l'amour divin, sans prière par jour) : voir `A_FOURNIR.md` |
| Neuvaine avant la Fête-Dieu ; triduum dans l'octave | n° 649, 652 | 9 jours avant la Fête-Dieu | non intégrée (prières au choix) |
| Onze neuvaines des fêtes de la sainte Vierge (Présentation, Annonciation, Visitation, Purification, Sept Douleurs, Cœur de Marie…) | n° 757 | 9 jours avant chaque fête | Immaculée, Nativité, Assomption, Rosaire au plan ; les autres sans texte propre |
| Douze samedis ou dimanches (premier du mois) en l'honneur de Marie Immaculée | n° 760 | 1er samedi ou dimanche de 12 mois | recouvre les premiers samedis (plan) |
| Neuvaines à S. Raphaël et à l'Ange gardien | n° 775 | à tout moment ; Ange gardien avant le 2 oct. | non intégrées (texte à choisir) |
| Mois de mars à S. Joseph | n° 777 | mars | mars : Douleurs et Allégresses le mercredi (programme) ; mois de S. Joseph de Montréal à transcrire (§ 6) |
| Neuf mardis et neuvaine à sainte Anne | n° 778 | 9 mardis avant le 26 juillet ; 17-25 juill. | aucun texte au corpus : à chercher (manuel de Sainte-Anne-de-Beaupré) |
| Neuvaine ou mois de S. François d'Assise | n° 781 | 25 sept.-3 oct. | texte de Québec 1867 à transcrire (§ 6) |
| Neuvaine « de la grâce » de S. François Xavier | n° 786 | 4-12 mars | aucun texte au corpus : à chercher (formule de la neuvaine de la grâce dans un manuel jésuite ancien) |
| Triduum ou neuvaine à S. Jean-Baptiste, à S. Étienne | n° 491, 492 | avant le 24 juin ; avant le 26 déc. | non intégrés |
| Neuvaine pour les âmes du purgatoire | *Purgatorian Consoler* (anglais) | — | chercher d'abord le *Livre d'or des âmes du purgatoire* (lot B) |
| Prière ancienne au B. Louis-Marie Grignion de Montfort | — | 19-27 avr. | `A_FOURNIR.md` (deux candidats sans intégration) |
| Triduum à N.-D. du Perpétuel Secours (`weber:trois-prieres-perpetuel-secours`) | Beringer n° 459 ; Ench. 1952, n° 427 | sans date propre dans la source | non daté ; la fête (27 juin) n'est pas au calendrier universel de 1954 |

## 8. Bréviaire du Sacré-Cœur

Le PDF fourni par l'utilisateur (*Petit bréviaire du Sacré-Cœur de Jésus*, Nancy, 1883) **n'est pas dans le
conteneur** (`vendor/sources/` ne le contient pas). La neuvaine du premier vendredi en avait été transcrite et relue
page à page (`engine/recueils/breviaire_sc_suite/neuvaine.md`, commit `11859ca`) : rien n'a été réécrit ici.
Les mêmes prières servent les neuf jours ; la rubrique fixe la fin au jeudi, veille du premier vendredi.

## 9. Tests

`journee.test.ts` : `quand › autour` ; neuvaine du premier vendredi (les dates des douze premiers vendredis de
2026-2027, le titre de chaque jour, l'amende honorable et la consécration le 9e jour seulement, toujours un jeudi) ;
neuvaine de réparation (12 × 9 jours, offrande à la fin de la prière du matin) ; sainte Face (20-28 juin, méditation du
jour, ouverture et prières du premier jour, plus aucun renvoi) ; Berchmans et Stanislas (dimanches et rang).
`unicite.test.ts` et `matrice.test.ts` inchangés et verts sur toute l'année.

## 10. Suite (branche `claude/neuvaines-2`)

Décisions de l'utilisateur : la neuvaine de la sainte Face reste du 20 au 28 juin ; l'indulgence n° 250 est comptée.

1. **Ench. 1952, n° 250**, vu sur l'image (p. 156-157, archive.org `enchiridion_indulgentiarum_1952` n171-n172) :
   fiche ajoutée sur `breviaire-sc:neuvaine` (7 ans une fois le jour, prières quelconques). `bilan.ts` compte désormais
   une concession « une fois le jour » **une seule fois par numéro** de l'Enchiridion, même portée par deux textes :
   le 28 mai 2027, les deux neuvaines au Sacré-Cœur ne donnent que 7 ans (test `bilan.test.ts`).
   **Lecture stricte (décision de l'utilisateur, 26 nov.)** : la concession vaut pour deux neuvaines par an, « tum
   immediate ante festum … tum alio infra annum tempore ». Celle qui précède la fête est comptée sur la neuvaine de
   S. Alphonse (`liguori:neuvaine-sacre-coeur`, déjà porteuse du n° 250) ; **l'autre est la première neuvaine du
   premier vendredi de l'année liturgique, celle du premier vendredi de décembre** (choix de l'utilisateur ; elle
   commence quelques jours avant le 1er dimanche de l'Avent et finit entre le 22 novembre et le 6 décembre). La fiche
   de `breviaire-sc:neuvaine` ne vaut donc que du 22 novembre au 6 décembre (`partielles[].quand.dates`) ; les onze
   autres neuvaines du mois restent au programme sans indulgence comptée. En 2026-2027 : 29 nov.-3 déc. 2026 (le début,
   25-28 nov., est dans l'année précédente) et 24-27 nov. 2027 (neuvaine du 3 déc. 2027).
4. **Sainte Élisabeth** : non retenue par l'utilisateur (26 nov.) ; la neuvaine de Québec 1867 n'est pas ajoutée.
2. **Neuvaine à saint François d'Assise** (`tiersordre1867:neuvaine-saint-francois`, nouvelle) : *Notice sur le
   Tiers-Ordre de la pénitence…*, Québec, 1867, p. 37-51, recopiée page à page sur l'image (taches d'encre relues à
   300 dpi ; orthographe et fautes de l'édition gardées : « bienheureureux », « autérités », « consolatien »…).
   `prog:neuvaine-saint-francois`, 25 sept.-3 oct. : chaque jour l'hymne, la vertu et sa prière, le répons, verset,
   oraison et *Tantum ergo* de la fin (imprimés une fois après le 1er jour, rangés à la fin de la pièce) ; les renvois
   « page 37 », « page 39 » retirés à l'affichage.
3. **Neuvaine pour se préparer aux fêtes de saint Joseph** (`confreriejoseph:neuvaine-fetes-saint-joseph`, nouvelle) :
   *Manuel de la Confrérie de Saint Joseph*, Montréal, s. d., p. 65-68 (aucune approbation imprimée dans le scan,
   comme les autres pièces de ce manuel déjà livrées). `prog:neuvaine-saint-joseph-montreal`, 10-18 mars : prière
   préparatoire et prière du jour (foi, espérance, charité, humilité, obéissance, recueillement, fuite du péché, salut,
   consécration). Recouvre la neuvaine du plan (Douleurs et Allégresses), gardée.

5. **Neuvaine à saint François-Xavier** (`xavier1880:prieres-neuvaine`, nouvelle) : *Neuvaine en l'honneur de saint
   François-Xavier*, nouvelle édition, Québec, A. F. E. Darveau, 1880, **approbation de l'archevêque de Québec (E. A.
   [Taschereau]), 15 déc. 1879, vue sur l'image** (PDF p. 5) ; « prières pour tous les jours de la neuvaine »,
   p. 41-47, recopiées sur l'image (prière à Dieu, oraison à S. François-Xavier, antiennes et oraisons de la Passion et
   de l'Immaculée Conception). `prog:neuvaine-saint-francois-xavier` : **jours de l'édition** (« commence, à la
   Basilique de Notre-Dame, le premier samedi du carême et finit le second dimanche ») : `Quadp3-6` … `Quad2-0`,
   13-21 févr. 2027 ; titre de chaque jour, prières communes. La date de Beringer (4-12 mars, Strasbourg) n'est pas
   prise : à changer si l'utilisateur la préfère. **Reste à transcrire** : la considération et les réflexions de chaque
   jour (p. 29-129 environ, avec la veille) et les litanies de S. François-Xavier (latin et français, p. 48 s.).

Outils : `engine/recueils/neuvaines/` (textes relus en `.md`, `pieces.json`, `inserer.py`).

**Recherche des autres neuvaines datées** : Immaculée Conception (Weber), Noël (S. Alphonse), Sacré-Cœur (S.
Alphonse), Assomption et Nativité (Lévis 1886) sont déjà au plan avec leur texte. Sainte Élisabeth : non retenue (ci-dessus).
Restent à transcrire : les triduums des trois fêtes de saint Joseph et la neuvaine pour une grâce particulière (`cihm_61528`) ; la neuvaine de
saint François Xavier (archive.org : une vingtaine d'éditions de Québec, 1772-1887, dont `cihm_62891`, 1880, avec
instruction sur les indulgences, et `cihm_04687`, 1869) ; la neuvaine du Saint-Esprit de S. Alphonse (dix méditations).
