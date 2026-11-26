# Prières obligatoires : titre de chaque élément — 26 novembre 2026

Demande de l'utilisateur du 26 nov. (prioritaire) :

1. **prière du soir** : là où le Paroissien ne donne qu'un *Ave*, trois *Ave Maria* « spéciaux » (pratique indulgenciée,
   prescrite ou promise) ; ni les trois *Ave* de sainte Mechtilde (déjà au chapelet), ni l'*Ave* d'or (rotation de
   sainte Gertrude) ;
2. **chapelet** : un premier *Pater* et un premier *Gloria* « spéciaux » à l'ouverture, courts, avec indulgence,
   prescription ou promesse ;
3. **règle** : dans les seules prières obligatoires, chaque prière dite doit avoir un **titre** (indulgence de
   l'*Enchiridion* de 1952, prescription de l'Église ou d'une archiconfrérie, promesse attestée). Sans titre : chercher un
   remplaçant ancien de même fonction et de longueur voisine ; sans remplaçant, la prière reste, sans marque.

Branche `claude/prieres-obligatoires`. **`programme.json` n'est pas modifié** : l'utilisateur tranchera, puis on
intégrera. Pièces nouvelles dans `data/prieres/sources.json` (7), fiches dans `data/prieres/indulgences.json` (6),
chacune relue sur l'image ; voir `SOURCES_UTILISEES.md`, section du 26 novembre.

## Lignes retenues comme obligatoires

Les quatre entrées de rang `praecipua` de `programme.json` : `prog:priere-du-matin` (avec l'offrande),
`prog:angelus`, `prog:chapelet`, `prog:priere-du-soir`, **et ce qui s'y insère chaque jour** (Salve Regina du matin,
Flèche d'or, prière pour les agonisants, *Crux ave* et salutations de Jahenny, fins de dizaine, fruits des mystères,
âmes du soir, don du jour, Sub tuum, consécrations des fêtes, Sainte Famille en février). Les autres lignes (dévotions
du jour, Triple Couronne, sainte Brigitte, cordon, neuvaines) sont surérogatoires : hors champ.

## Sources du titre

- ***Enchiridion indulgentiarum*** (S. Pén. Ap., Vatican, 1952), seul compte des indulgences (SPEC § 11) ; numéros vus
  sur l'image (archive.org `enchiridion_indulgentiarum_1952`).
- ***Thésaurisons pour le ciel*** (Carmel de Montréal, 1941), traductions certifiées (can. 934 § 2) ; son
  **« Aide-mémoire : la journée indulgenciée »** (p. 187-188, vu sur l'image) donne un plan ancien des prières du lever,
  du matin et du soir **toutes indulgenciées** : il a servi de guide pour les remplaçants (offrande de la journée :
  n° 23 et 28 ; abandon à la volonté de Dieu : n° 6, 26, 223 ; actes des vertus : n° 189 ; soir : acte d'abandon, n° 12).
- Beringer, *Les Indulgences*, 1925, quand il rend mot pour mot la formule de 1952.
- Manuels d'archiconfréries (règle du 22 nov.) pour les prescriptions ; révélations approuvées pour les promesses.

Abréviations : **I** = indulgence (Ench. 1952), **P** = prescription, **Pr** = promesse, **—** = aucun titre.
Longueurs en mots (rubriques non comptées).

## 1. Prière du matin et offrande (`prog:priere-du-matin`)

| # | Élément (texte actuel) | Titre | Remplaçant proposé (source, titre) | Longueur |
|---|---|---|---|---|
| 1 | Signe de croix (Paroissien 1890) | **I** n° 678 (3 ans) | — | 14 |
| 2 | « Très sainte et très auguste Trinité… » (adoration) | — | aucun remplaçant à fonction égale dans l'*Aide-mémoire* ; garder | 46 |
| 3 | « Mon Dieu, je vous remercie… je vous en consacre toutes les pensées… » (remerciement et offrande) | — | **Oraison de Prime** « Seigneur, Dieu tout-puissant, qui nous avez fait parvenir… » (`thesaurisons:oraison-de-prime`, *Thésaurisons* n° 28) — **I** n° 60 (5 ans, le matin) ; c'est l'« offrande de la journée » de l'*Aide-mémoire* | 75 → 53 |
| 4 | « Adorable Jésus, divin modèle… » (résolution) | — | aucun ; garder (l'oraison de Prime, n° 3, porte aussi la résolution d'éviter le péché) | 64 |
| 5 | « Mon Dieu, vous connaissez ma faiblesse… » (demande) | — | aucun ; garder | 64 |
| 6 | *Pater noster* (latin) | — (le *Pater* seul n'est pas indulgencié en 1952) | aucun ; garder | 50 |
| 7 | *Ave Maria* (latin) | — | voir § 5 : les trois *Ave* de saint Alphonse peuvent se dire **matin et soir** (Beringer n° 444) ; au matin, à trancher | 31 |
| 8 | *Credo* | **I** n° 43 | — | 76 |
| 9 | *Confiteor*, *Misereatur*, *Indulgentiam* | **I** n° 691 (*Confiteor*) | — | 93 |
| 10 | « Sainte Vierge, Mère de Dieu, ma mère et ma patronne… » | — | suivi du **Salve Regina** (n° 332, 293) déjà inséré : il remplit la fonction ; garder | 65 |
| 11 | « Ange du ciel, mon fidèle et charitable guide… » | — | *Angele Dei* (Ench. 1952, n° 452 d'après la table, non vu sur l'image) : traduction certifiée à recopier → `A_FOURNIR.md` | 37 |
| 12 | « Grand saint, dont j'ai l'honneur de porter le nom… » | — | aucun remplaçant trouvé ; garder | 37 |
| 13 | Actes de foi, d'espérance, de charité | **I** n° 36 (3 ans chacun) | — | 109 |
| 14 | Salve Regina et ℣. *Dignare me* (insertion) | **I** n° 332 et 293 | — | 98 |
| 15 | Intention d'indulgences (livret, sans source ancienne) | **P** : l'intention au moins générale est requise pour gagner les indulgences (can. 925 § 2) ; texte moderne | **Acte d'offrande des actions de la journée pour gagner les indulgences**, Archiconfrérie du Cœur immaculé de Marie (`desgenettes:acte-d-offrande-pour-les-indulgences`, Desgenettes 1852, p. 434-435) — **P** (archiconfrérie) et même fonction canonique | 60 → 100 |
| 16 | Acte de soumission à la volonté de Dieu (livret) | — | **Recevez, Seigneur, toute ma liberté** (`thesaurisons:suscipe`, *Thésaurisons* n° 26) — **I** n° 52 (3 ans) ; « acte de total abandon » de l'*Aide-mémoire* | 303 → 71 |
| 17 | Acte d'intention de communion spirituelle perpétuelle (livret) | **I** n° 164 (quelle que soit la formule) | — | 298 |
| 18 | Acte de recommandation des âmes rencontrées (livret) | — | **Entre vos mains, Seigneur** (saint Edmond) (`ench1952:entre-vos-mains-saint-edmond`) — **I** n° 55 (3 ans ; concession **en français**) : remet à Dieu « mon âme, mes parents, mes bienfaiteurs, mes amis et mes ennemis et tout le peuple catholique » ; c'est l'autre « offrande de la journée » de l'*Aide-mémoire* | 285 → 124 |
| 19 | Devoir envers l'Église et ses ministres (livret) | — | aucun remplaçant de même fonction relu ; garder (voir `A_FOURNIR.md`) | 156 |
| 20 | Devoir envers la famille (livret) | — | en partie couvert par n° 18 (saint Edmond : « mes parents ») ; garder | 103 |
| 21 | Devoir envers la patrie (livret) | — | candidat sans indulgence : `desgenettes:priere-salut-de-la-france` (archiconfrérie, **P** faible : prière publiée, non imposée) ; garder | 198 |
| 22 | Devoir envers les pauvres, les persécutés, les affligés (livret) | — | aucun ; garder | 92 |
| 23 | Devoir envers moi-même (livret) | — | aucun ; garder | 99 |
| 24 | Champ « intentions particulières » | (pas une prière) | — | — |
| 25 | *Crux ave* (Jahenny, insertion) | **I** n° 187 | — | court |
| 26 | Prière pour les agonisants (insertion) | **I** n° 671 (trois fois le jour) | — | 112 |
| 27 | Consécration du jour de fête (Garde d'honneur, Desgenettes, Janvier) | **P** : formules des archiconfréries, le jour de leur fête | — | — |

## 2. Angélus (`prog:angelus`)

| # | Élément | Titre | Remplaçant | Longueur |
|---|---|---|---|---|
| 1 | Angélus (Regina cæli au temps pascal), avec l'oraison | **I** n° 331 (10 ans) | — | 133 |
| 2 | Flèche d'or (insertion) | **Pr** et **P** : acte dicté à la sœur Saint-Pierre, prescrit par le manuel de l'Archiconfrérie de la Sainte-Face (Janvier 1895, p. 181, approuvé par le card. Meignan) ; pas dans l'Ench. 1952 | — | 72 |
| 3 | Prière pour les agonisants (midi) | **I** n° 671 | — | 112 |

## 3. Chapelet (`prog:chapelet`)

| # | Élément | Titre | Remplaçant | Longueur |
|---|---|---|---|---|
| 1 | Chapelet de saint Dominique, notice (Sambucy) | (notice) — le chapelet entier : **I** n° 395 (5 ans ; plénière mensuelle ; plénière chaque fois devant le Saint-Sacrement) | — | — |
| 2 | Ouverture de Montfort (« Je m'unis à tous les Saints… », offrande du Credo, du *Pater* et des trois *Ave*) | — (Montfort ; non indulgencié) | garder (c'est la méthode retenue) | ~120 |
| 3 | *Credo* | **I** n° 43 | — | 76 |
| 4 | **Premier *Pater*** | — | **voir § 6** | — |
| 5 | Trois *Ave* sous la forme de sainte Mechtilde | **Pr** (révélation à sainte Mechtilde, Denis, p. 206-208) | — | 385 |
| 6 | **Premier *Gloria*** | — | **voir § 6** | — |
| 7 | Offrande de chaque dizaine et « Grâce du Mystère… » (Montfort) | **P** : la méditation des mystères est requise pour l'indulgence du chapelet (Ench. 1952, n° 395 ; Sambucy : « on est obligé… de méditer sur les mystères ») ; l'offrande de Montfort en est la forme | — | ~45 / dizaine |
| 8 | Dizaines (*Pater*, dix *Ave*, *Gloria*) | **I** n° 395 (pour le tiers du Rosaire) | — | — |
| 9 | Fruit du mystère (Rosaire-Vivant 1841, insertion) | **P** : prière du mystère de l'Association du Rosaire-Vivant (Montréal 1841, approuvé) | — | ~25 / dizaine |
| 10 | « Ô mon Jésus, pardonnez-nous… » (Fatima, insertion) | **P/Pr** : demande de Notre-Dame à Fatima (13 juillet 1917 ; apparitions déclarées dignes de foi en 1930) ; **pas** dans l'Ench. 1952 | — | 30 |
| 11 | « Ô Marie conçue sans péché, priez pour nous qui avons recours à vous » | **I** n° 357 (300 jours ; concession en italien ; la phrase est tirée de Weber, p. 477 : traduction non déclarée fidèle → indulgence à confirmer) | — | 11 |
| 12 | Conclusion de Montfort « Dieu seul » (« Je vous salue, Marie, Fille très aimable du Père éternel… », « Loué soit… », bénédiction) | — | aucun ; garder | ~260 |

## 4. Prière du soir et examen (`prog:priere-du-soir`)

| # | Élément | Titre | Remplaçant | Longueur |
|---|---|---|---|---|
| 1 | Don du Saint-Esprit du jour (Beringer, insertion) | **I** partielle : une des sept invocations du n° 383 (*Vi compatisco*), l'indulgence est attachée à la prière entière (`sans_compte`) | — | ~55 |
| 2 | Signe de croix | **I** n° 678 | — | 14 |
| 3 | « Je vous adore, ô mon Dieu… Je crois… J'espère… Je vous aime… » | — (actes des vertus, mais formule du Paroissien, non d'un catéchisme) | aucun ; garder | 61 |
| 4 | « Quelles actions de grâces vous rendrai-je… » | — | aucun ; garder | 95 |
| 5 | « Source éternelle de lumière, Esprit-Saint… » ; examen | — | aucun ; garder | 56 |
| 6 | « Me voici, Seigneur, tout couvert de confusion… » (contrition) | — (l'acte de contrition est **I** n° 36 « quelle que soit la formule » d'un catéchisme approuvé ; le Paroissien n'en est pas un) | à trancher : acte de contrition d'un catéchisme approuvé à fournir (`A_FOURNIR.md`) | 116 |
| 7 | « Que je souhaiterais… » (ferme propos) | — | aucun ; garder | 100 |
| 8 | *Notre Père* | — | aucun ; garder | 63 |
| 9 | ***Je vous salue, Marie*** (un seul) | — | **les trois *Ave* de saint Alphonse, voir § 5** | 48 → 3 × 48 + 3 × 14 |
| 10 | *Je crois en Dieu* | **I** n° 43 | — | 115 |
| 11 | *Je confesse à Dieu* | **I** n° 691 | — | 141 |
| 12 | « Bénissez, ô mon Dieu, le repos… » | — | aucun ; garder | 60 |
| 13 | Prière pour les vivants et les défunts | — | aucun ; garder | 91 |
| 14 | Trois salutations à Jésus crucifié (Jahenny, insertion) | **Pr** : promesses rapportées par Marie-Julie Jahenny (révélation privée **non approuvée**) — titre faible, à trancher | — | — |
| 15 | Prière pour les agonisants | **I** n° 671 | — | 112 |
| 16 | Prière du jour pour les âmes (Beringer n° 615, sauf le lundi) | indulgence de Beringer 1925 (Léon XIII) **non retrouvée** dans l'Ench. 1952 | aucun ; garder | ~70 |
| 17 | A la Sainte Famille (février) | **I** n° 643 | — | ~50 |
| 18 | *Sub tuum* et ℣. *Dignare me* | **I** n° 333 et 293 | — | ~60 |

## 5. Les trois *Ave* du soir — candidats

| Candidat | Source | Titre | Longueur | Remarque |
|---|---|---|---|---|
| **A. Trois *Ave Maria* avec « Par votre Immaculée Conception, ô Marie, purifiez et sanctifiez mon corps et mon âme »** (`beringer:trois-ave-immaculee-conception`) | Beringer 1925, t. I, n° 444, p. 234 : « Prière quotidienne à la Vierge immaculée. — Trois fois, *Je vous salue, Marie*, en ajoutant chaque fois l'invocation » ; note : « Saint Alphonse de Liguori… recommandait aux fidèles cette pratique pour chaque matin et chaque soir, comme un excellent moyen de défense contre les tentations impures. » | **I** Ench. 1952, n° 358 (« Ave Maria, etc. Per tuam immaculatam Conceptionem, o Maria, redde purum corpus meum et sanctam animam meam »), 300 jours **chaque fois** (donc 3 × 300 jours) ; français certifié identique : *Thésaurisons*, n° 285 (« Contre les tentations impures ») | 3 × (48 + 14) | C'est la pratique indiquée par l'utilisateur. La formule exacte n'est pas « par votre pure et immaculée Conception » : Beringer, *Thésaurisons* et l'Ench. portent « Par votre Immaculée Conception… purifiez et sanctifiez mon corps et mon âme ». |
| B. « Ma Mère, préservez-moi du péché mortel », puis trois *Ave* (`thesaurisons:ma-mere-preservez-moi`) | *Thésaurisons*, n° 268, p. 98 | **I** Ench. 1952, n° 297, 300 jours | 8 + 3 × 48 | Même structure, intention de persévérance. |
| C. « Virgo ante partum… Ave Maria » (trois fois) | Ench. 1952, n° 295 (300 j.), vu sur l'image | **I** | — | Aucune traduction certifiée trouvée : non transcrit. |

**Recommandation : A.** Intégration proposée : dans `prog:priere-du-soir`, l'extrait « ## La Salutation angélique » du
Paroissien garde son *Ave*, précédé de la rubrique et suivi de l'invocation de `beringer:trois-ave-immaculee-conception`
(trois fois). La même pratique vaut le matin (Beringer : « matin et soir ») : à décider pour le n° 7 du matin.

## 6. Premier *Pater* et premier *Gloria* du chapelet — candidats

| Candidat | Source | Titre | Longueur | Remarque |
|---|---|---|---|---|
| **P1/G1. Le premier *Pater*, le premier *Ave* et le *Gloria* de l'ouverture dits « aux intentions du Souverain Pontife »** (`thesaurisons:prieres-intentions-souverain-pontife`) | *Thésaurisons*, notes explicatives 4), p. 17 ; Ench. 1952, p. XV, note 1 a) : « Clausula *precandi ad mentem Summi Pontificis* plane adimpletur… recitationem ad eam mentem unius *Pater*, *Ave* et *Gloria* » (S. Pén. Ap., 20 sept. 1933) | **P** de l'Église : remplit la condition des indulgences plénières, en particulier celles du chapelet (n° 395 : plénière mensuelle si le chapelet est dit chaque jour ; plénière **chaque fois** devant le Saint-Sacrement, avec confession et communion) | 0 mot ajouté (une rubrique d'intention) | Court, ancien, utile tous les jours. Le premier *Ave* reste celui de sainte Mechtilde (promesse, non indulgence : pas de conflit). |
| G2. Trois *Gloria Patri* « en action de grâces à la Sainte Trinité pour tous les dons et privilèges dont Elle a daigné gratifier la très sainte Vierge Marie » (`thesaurisons:trois-gloria-privileges-de-marie`) | *Thésaurisons*, n° 355, p. 125 ; Ench. 1952, n° 47 | **I** 500 jours pour chaque récitation des trois *Gloria* le matin, à midi ou le soir | 3 × 20 | Exige **trois** *Gloria* et l'heure (matin, midi, soir). Can. 933 : un même *Gloria* ne peut servir à la fois à G2 et à P1. |
| P2. *Pater* offert « en union de cette louange » (sainte Mechtilde) : « Père très-saint, je vous offre cette prière… » | *Prières de sainte Gertrude* (Denis, 1864, p. 41-42 ; archive.org `bub_gb_GhXeTuoGrbUC`) ; *Livre de la grâce spéciale*, IV, 30 (1921) | **Pr** « Ainsi je suppléerai à ses péchés et à ses négligences… on doit croire pieusement qu'il recevra la même grâce » | ~45 | Promesse attachée au *Pater* dit **à la Préface de la messe**, non au chapelet : transposition. Non transcrit. |
| P3. Offrande de Montfort déjà dite (« ce *Pater* et ces trois *Ave*, pour honorer l'Unité de votre essence et la Trinité de vos personnes ») | Montfort | — | (déjà présent) | Aucun titre. |

Recherche sans résultat d'une **promesse ou indulgence attachée en propre au premier *Pater* ou au premier *Gloria* du
chapelet** : Beringer 1925 (n° 901 : le *Credo*, le *Gloria* et trois *Ave* du début sont « un usage louable, mais non
pas nécessaire… pour obtenir une augmentation des trois vertus théologales »), Ench. 1952 (n° 395 et suivants),
*Thésaurisons*, Montfort, Sambucy, Denis (Gertrude et Mechtilde), *Livre de la grâce spéciale* (1921), manuels du
Rosaire déjà ouverts (Rosaire-Vivant 1841, *Trois Confréries* 1902, Livret 1903). Voir `A_FOURNIR.md`.

**Recommandation : P1/G1** — à l'ouverture, une rubrique : « Ce *Pater*, ce premier *Ave* et ce *Gloria*, aux
intentions du Souverain Pontife » (formule de rubrique à rédiger par l'app : c'est une mise en page, pas un texte de
prière ; la notice `thesaurisons:prieres-intentions-souverain-pontife` en donne la source). **Variante** si l'utilisateur
préfère une indulgence propre au *Gloria* : G2, en disant trois *Gloria* au lieu d'un (le chapelet doit alors être dit le
matin, à midi ou le soir), et P1 réduit au *Pater* et au premier *Ave*… ce qui ne remplit plus la clause (il y faut un
*Gloria*) : G2 et P1 ensemble demandent donc quatre *Gloria*. D'où la préférence pour P1/G1 seul.

## 7. Bilan

- Éléments examinés : **60** (matin 27, Angélus 3, chapelet 12, soir 18), dont 59 prières (le champ d'intentions n'en
  est pas une).
- **Avec titre** : 29 (indulgence 21 ; prescription 5 ; promesse 3), dont la fin de dizaine de Fatima, la Flèche d'or
  et les salutations de Jahenny à titre discuté.
- **Sans titre, remplaçant proposé** : 6 — matin n° 3 (oraison de Prime), 16 (*Suscipe*), 18 (saint Edmond) ; soir
  n° 9 (trois *Ave* de saint Alphonse) ; chapelet n° 4 et 6 (intention du Souverain Pontife). Plus un élément titré
  mais moderne, remplacé par un texte ancien de même fonction : matin n° 15 (offrande de Desgenettes).
- **Sans titre, sans remplaçant** (restent, sans marque, décision de l'utilisateur) : 24 — matin n° 2, 4, 5, 6, 7, 10,
  11, 12, 19-23 ; chapelet n° 2 et 12 ; soir n° 3-8, 12, 13, 16 : surtout les parties propres du Paroissien, le *Pater*
  et l'*Ave* seuls du matin, l'invocation à l'Ange et au saint patron, les cinq « devoirs » du livret, la conclusion
  « Dieu seul » de Montfort, la prière du jour pour les âmes (indulgence de 1925 non reprise en 1952).

## 8. Points à trancher par l'utilisateur

1. Trois *Ave* du soir : A (recommandé), B ou C ; aussi le matin ?
2. Ouverture du chapelet : P1/G1 (recommandé) ou G2.
3. Offrande du matin : remplacer les textes du livret (intention d'indulgences, soumission, recommandation des âmes) par
   Desgenettes, le *Suscipe* et saint Edmond, ou les garder à côté ? L'oraison de Prime à la place du paragraphe
   d'offrande du Paroissien, ou en plus ?
4. Salutations de Jahenny et Flèche d'or : promesse d'une révélation non approuvée (Jahenny) — titre accepté ou non ?
5. Acte de contrition du soir : chercher la formule d'un catéchisme approuvé (indulgence n° 36) ?

## Indulgences

Fiches ajoutées à `data/prieres/indulgences.json`, toutes **vues sur l'image** de l'*Enchiridion* de 1952 :
n° 358 (`beringer:trois-ave-immaculee-conception`), 297 (`thesaurisons:ma-mere-preservez-moi`), 55
(`ench1952:entre-vos-mains-saint-edmond`), 52 (`thesaurisons:suscipe`), 60 (`thesaurisons:oraison-de-prime`), 47
(`thesaurisons:trois-gloria-privileges-de-marie`). Elles ne comptent dans la journée qu'une fois les pièces branchées.
