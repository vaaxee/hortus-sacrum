# Audit esthétique — 22 novembre 2026

⚠️ DEGRADED: single-context (delegated read-only run) — l'agent Esthétique travaillait sans outil de sous-agent ni moyen
de questionner l'utilisateur : la revue de conception (évaluation A) et le détecteur (évaluation B) ont été menés dans le
même contexte, la revue d'abord, le détecteur ensuite. Aucun instantané `.impeccable/critique/` n'a été écrit.

- **Méthode** : critique Impeccable (`reference/critique.md`, `critique-rubric.md`), mode **Read / Operate** (écran du
  jour sobre). Identité existante tenue pour autorité : ce sont des propositions de **raffinement**, aucune refonte.
- **Périmètre** : Accueil, Aujourd'hui, Lecture, Lecture › Office (Petit bréviaire du Sacré-Cœur), page d'une pratique
  (Chapelet, `/pratique/prog:chapelet`), Prières, Dévotions, Calendrier (mois), Profil, Méditation, Lecture › Spirituel.
- **Rendus regardés** : 11 écrans × téléphone (390 × 844) et bureau (1280 × 860) × jour et nuit × latine et grecque
  (176 captures à `deviceScaleFactor` 1, plus les pages entières au téléphone), build de `main` au commit `0d9ce5e`,
  `vite preview`. Aucune erreur de page pendant les captures. Captures non versionnées.
- **Contrastes** calculés sur les jetons de `app/src/lib/design/tokens.css` (WCAG 2.1).
- **Rien n'a été corrigé.** Les questions d'ergonomie et de parcours signalées ci-dessous sont à trancher avec l'agent
  `hortus-ux` ; les textes religieux ne sont touchés par aucune proposition (seule leur **présentation** est en cause).

## Verdict de spécificité

**Revue (avant le détecteur).** L'app est singulière et cohérente : on ne pourrait pas la confondre avec une app de
prière générique. Le système « livre d'église » (Garamond, petites capitales, rubrique, double filet d'or, arche en plein
cintre, ornements au trait propres à chaque direction) tient d'un écran à l'autre, et les quatre combinaisons de
couleurs sont dessinées pour elles-mêmes, pas obtenues par inversion. La nuit latine (bordeaux et rubis vif) et la nuit
grecque (outremer et or) sont les plus réussies. Les faiblesses sont de **finition et de hiérarchie**, pas d'identité :
quelques fuites d'une direction dans l'autre, des grammaires d'onglets concurrentes, des contrôles natifs non habillés,
et un écran du jour dont la tâche principale (la liste) commence sous le pli.

**Détecteur** (`impeccable detect`) :

- sources (`app/src/lib/design`, `app/src/routes`, `app/src/lib/*.svelte`) : 0 constat (le détecteur de sources ne juge
  pas la mise en page) ;
- page `/` à 390 × 844 : 5 constats.
  - `low-contrast` : crédit du tableau de l'accueil, `#8c8679` sur `#faf5ef`, **3,3:1** → **fondé** (constat 9).
  - `wide-tracking` × 3 (date, temps liturgique, martyrologe, chasse 0,06 em) → **faux positifs** : ce sont des
    étiquettes en petites capitales, où la chasse est voulue.
  - `cream-palette` (fond `#faf5ef`) → **faux positif** : la nacre est la couleur de la charte latine, choisie par
    l'utilisateur (`docs/REPRISE.md`).

## Note de santé (heuristiques de Nielsen)

| # | Heuristique | Note | Point principal |
|---|---|---|---|
| 1 | Visibilité de l'état du système | 3 | Avancement « 0 / 9 · 1 h 37 restantes », heures dites, n/N clairs ; la couleur liturgique ne se lit qu'à la pastille. |
| 2 | Correspondance avec le monde réel | 4 | Vocabulaire et typographie du livre d'église, ℣/℟, rangs, Introït. |
| 3 | Contrôle et liberté | 3 | Retour, jours précédent/suivant ; accueil à franchir à chaque session. |
| 4 | Cohérence et standards | 2 | Trois grammaires d'onglets ; fuite de la mosaïque grecque dans la latine ; champs de date natifs. |
| 5 | Prévention des erreurs | 3 | Bascules à double codage (losange + couleur) ; peu de risques visuels. |
| 6 | Reconnaissance plutôt que rappel | 3 | Icônes gravées avec libellé ; l'icône du Profil (lis) se lit mal comme « profil ». |
| 7 | Flexibilité et efficacité | 2 | Page de pratique de 7 400 px sans sommaire ; liste du jour sous le pli. |
| 8 | Esthétique et minimalisme | 3 | Très soigné ; en-tête d'Aujourd'hui trop haut, en-tête de Prières chargé. |
| 9 | Reprise après erreur | n/a | Aucun état d'erreur rencontré dans ce passage visuel. |
| 10 | Aide et documentation | 3 | Aides courtes et justes (« Ces séries ont commencé sans vous… »). |
| **Total** | | **26/36** | **Bon (72 %)** |

## Ce qui fonctionne

1. **La typographie de lecture.** Garamond 19 px / 1,55, mesure de 34 rem, chiffres elzéviriens, ℣/℟ en rubrique,
   lettrine de rubrique, versets au fer à gauche : l'office et les méditations se lisent comme un livre, de jour comme de
   nuit (Office, Méditation, Chapelet).
2. **Les quatre palettes.** Tous les textes passent AA dans les quatre combinaisons (encre douce 6,6 à 9,1:1 ; accent
   5,6 à 7,6:1 ; texte de l'arche 6,5 à 8,2:1). La nuit n'est pas une inversion : bordeaux et rubis vif, outremer et or.
3. **Les ornements au service du sens.** Rinceau de vigne / mosaïque en bandeau, lis ou chrisme à la clef de l'arche,
   niche d'or de l'onglet actif, brin dans la case cochée : décor discret, propre à la tradition, jamais sur le texte.

## Constats, par priorité

Gravité : **P0** bloquant, **P1** majeur, **P2** mineur, **P3** finition.

### P1 — à traiter d'abord

**1. Aujourd'hui (téléphone) : la liste du jour commence sous le pli.**
- *Problème* : au téléphone, le premier écran est entièrement pris par la date, le temps, la ligne de contexte, l'arche
  (≈ 320 px), l'Introït, la jaculatoire et le bilan ; aucune case n'est visible sans défiler, dans les quatre
  combinaisons. Au bureau (1280 × 860), même chose : l'arche occupe la moitié de l'écran. Or la liste est la tâche
  (mode Operate) et la SPEC § 11.5 demande un écran du jour sobre.
- *Proposition* : réduire l'arche sur l'écran du jour (marge haute de l'intérieur `clamp(4.5rem, 24%, 6.5rem)` → plus
  faible, titre en t2 au téléphone), rapprocher Introït et jaculatoire en une bande, pour qu'au moins la section
  « Matin » paraisse au premier écran. L'ordre du bandeau voulu par la SPEC § 1 est gardé. **À arbitrer avec
  `hortus-ux`** (hiérarchie du parcours).
- *Fichiers* : `app/src/lib/design/Arche.svelte`, `app/src/routes/+page.svelte` (styles de l'en-tête).
- *Commande* : `/impeccable layout`.

**2. Accueil (bureau) : « Entrer au jardin » hors de l'écran.**
- *Problème* : à 1280 × 860, le tableau et son arche poussent le bouton principal et les trois fleurons sous le pli ;
  l'unique action de l'écran est invisible sans défiler.
- *Proposition* : sur grand écran, limiter la hauteur du tableau à la hauteur disponible (`max-height` en `dvh`) ou
  passer à deux colonnes (tableau à gauche, Introït, invocation et bouton à droite).
- *Fichiers* : `app/src/lib/design/Accueil.svelte`.
- *Commande* : `/impeccable adapt`.

**3. Calendrier (latine) : la mosaïque byzantine apparaît dans la direction latine.**
- *Problème* : la page du mois pose `<Ornement nom="mosaique" />` (`bande-mois`) sans variante latine ; en latine, une
  bande de tesselles bleues et vertes coiffe la page, sous le rinceau de vigne du bandeau. C'est la seule fuite d'une
  direction dans l'autre relevée, mais elle est sur un écran principal.
- *Proposition* : donner à `bande-mois` le motif de la direction (rinceau en latine, mosaïque en grecque), comme le
  bandeau du haut de `+layout.svelte`, ou la retirer (le bandeau du haut porte déjà le motif).
- *Fichiers* : `app/src/routes/calendrier/+page.svelte` (l. 75), `app/src/lib/design/Ornement.svelte`.
- *Commande* : `/impeccable polish`.

**4. Ordinaux en capitales : « 24E DIMANCHE », « 1RE CLASSE ».**
- *Problème* : le titre de l'arche est en `text-transform: uppercase` et les rangs en toutes petites capitales ; la
  donnée « 24e dimanche après la Pentecôte » s'affiche « 24E », « double de 1re classe » devient « 1RE ». En typographie
  française l'ordinal est « 24ᵉ » / « 1ʳᵉ » ; en capitales le « E » se lit comme une lettre du mot. C'est le titre le plus
  vu de l'app.
- *Proposition* : à l'affichage seulement (la donnée du calendrier ne change pas), envelopper le suffixe ordinal
  (`(\d+)(e|re|er|ème)\b`) dans un `<sup>` exclu de la mise en capitales (`text-transform: none`), dans l'arche, la
  liste des dimanches et fêtes et les rangs.
- *Fichiers* : `app/src/routes/+page.svelte` (h1 de l'arche, rang), `app/src/routes/calendrier/+page.svelte`,
  `app/src/app.css` (règle `h1`).
- *Commande* : `/impeccable typeset`.

**5. Trois grammaires d'onglets pour un même geste.**
- *Problème* : choisir une variante se dessine de trois façons : bascules à double filet en petites capitales (Mois /
  Semaine / Année, heures de l'office), texte Manrope souligné (Petit bréviaire / Bréviaire romain / Officium parvum,
  séries de mystères), puces de filtre (Prières). Sur l'Office, deux de ces grammaires se suivent à 40 px d'écart. Le
  Manrope y rompt aussi la règle des petites capitales de la charte.
- *Proposition* : réserver le soulignement Manrope à rien, ou à la seule navigation de second niveau, et passer les
  onglets internes (bréviaires, mystères) en petites capitales de Garamond avec le losange d'or de l'état choisi, comme
  les heures. Décrire la règle dans `DESIGN.md` une fois tranchée.
- *Fichiers* : `app/src/routes/lecture/office/+page.svelte`, `app/src/routes/pratique/[id]/+page.svelte`,
  `app/src/lib/Office.svelte`, `app/src/app.css`.
- *Commande* : `/impeccable polish` (puis `/impeccable document`).

**6. Page d'une pratique (Chapelet) : 7 400 px d'un seul tenant au téléphone.**
- *Problème* : la page enchaîne manière de saint Dominique, méditation des mystères, méthode de Montfort, trois Ave de
  sainte Mechtilde et les quinze mystères, sans sommaire ni sections repliées ; la SPEC § 11.4 demande « une page par
  pratique, en sections dépliables ». Les onglets des séries se coupent mal (« Mystères glorieux » seul sur la deuxième
  ligne).
- *Proposition* : présentation seulement, texte inchangé : intertitres de section en `details` repliables (le mécanisme
  `details::details-content` existe déjà dans `tokens.css`), ou un petit sommaire d'ancres en tête ; onglets des séries
  sur une ligne (libellés courts « Joyeux · Douloureux · Glorieux », la série étant dans le titre). **À arbitrer avec
  `hortus-ux`** (ouverture par défaut de la section du jour).
- *Fichiers* : `app/src/routes/pratique/[id]/+page.svelte`, `app/src/lib/FichePratique.svelte`.
- *Commande* : `/impeccable layout`.

### P2 — prochain passage

**7. Profil : champs de date natifs non habillés.**
- *Problème* : les dates (baptême, confirmation…) gardent le contrôle natif de Chromium : police à chasse fixe, cadre
  gris arrondi, format « mm/dd/yyyy » à l'américaine sur un écran par ailleurs typographié. `input[type='date']` manque à
  la liste des champs de `app.css` (seul `FichePratique.svelte` l'habille localement).
- *Proposition* : ajouter `input[type='date']` au style commun des champs (Garamond, filet en pied, `color-scheme` du
  thème) ; vérifier le format sur iOS (où le contrôle suit la langue de l'appareil).
- *Fichiers* : `app/src/app.css` (section « formulaires »), `app/src/routes/profil/+page.svelte`.
- *Commande* : `/impeccable polish`.

**8. Couleur de l'app installée incohérente avec la direction par défaut.**
- *Problème* : `app.html` annonce `theme-color` `#F8F3E8` (jour) et `#141B2B` (nuit d'encre de lapis, palette abandonnée)
  ; le manifeste annonce `theme_color` `#0E0C52` (outremer) et `background_color` `#F8F3E8`. En latine (défaut), la
  barre du navigateur Android et l'écran de lancement ne sont ni nacre ni bordeaux.
- *Proposition* : aligner les méta `theme-color` sur le fond de la direction et du thème courants (mise à jour par
  `apparence.ts`), et le manifeste sur la direction par défaut. **Question ouverte** dans `PRODUCT.md` (n° 2).
- *Fichiers* : `app/src/app.html`, `app/static/manifest.webmanifest`, `app/src/lib/apparence.ts`.
- *Commande* : `/impeccable polish`.

**9. Accueil : crédit du tableau et fleurons éteints trop pâles.**
- *Problème* : le crédit « Velázquez, *Le Couronnement de la Vierge*, v. 1635 » est à 3,3:1 (opacité 0,7 sur l'encre
  douce) ; c'est la seule provenance de l'image, elle doit se lire. La nuit, les fleurons d'avancement éteints sont
  presque invisibles (lis sombre sur bordeaux ou outremer) : trois marques de progression qu'on ne distingue pas.
- *Proposition* : crédit en encre douce pleine (6,7:1) ; fleurons éteints au trait d'or à faible opacité plutôt qu'en
  encre sombre, allumés en or plein.
- *Fichiers* : `app/src/lib/design/Accueil.svelte` (`.credit`, fleurons).
- *Commande* : `/impeccable polish`.

**10. Prières : en-tête de quatre rangées de contrôles avant le premier titre.**
- *Problème* : recherche, segments (Toutes / Favoris / Mes ajouts), bouton principal « Ajouter une prière », puis deux
  rangées de puces (Thème, Type) défilant à l'horizontale : au téléphone, la première partie de la bibliothèque arrive à
  550 px. Le bouton principal en aplat rubis est la chose la plus forte de l'écran alors qu'ajouter est l'action rare.
- *Proposition* : « Ajouter une prière » en bouton secondaire ou en icône dans l'en-tête ; Thème et Type repliés derrière
  une puce « Filtrer » (ouverte si un filtre est actif). **À arbitrer avec `hortus-ux`**.
- *Fichiers* : `app/src/routes/prieres/+page.svelte`.
- *Commande* : `/impeccable distill`.

**11. Justification au téléphone : grands blancs dans la prose.**
- *Problème* : sur une mesure de ≈ 38 signes (390 px moins les marges), la justification creuse des blancs visibles
  (Méditation : « Troisième moyen de soulager les » ; Chapelet : « lorsqu'on récite le chapelet de saint Dominique »),
  malgré la césure.
- *Proposition* : passer la prose au fer à gauche sous ~ 480 px (`text-align: start` dans une requête de largeur), la
  justifier au-delà ; ou n'activer la justification que si `hyphens: auto` est pris en charge.
- *Fichiers* : `app/src/lib/design/tokens.css` (`.lecture p`).
- *Commande* : `/impeccable typeset`.

**12. Icône du Profil : une fleur de lys qui se lit comme une pousse.**
- *Problème* : en haut à droite de chaque page, la seule entrée vers le Profil est un lis au trait fin de 22 px, sans
  libellé visible ; à cette taille il se lit comme une plante. Il prend la couleur de l'or quand il est actif, ce qui ne
  donne que 1,8:1 sur la nacre.
- *Proposition* : garder un symbole de la tradition, mais plus lisible comme « personne » ou « livre de vie » (par
  exemple un médaillon avec monogramme), ou adjoindre un libellé au bureau seulement ; état actif en accent (rubis,
  cobalt) plutôt qu'en or. **À voir avec `hortus-ux`** (découvrabilité du Profil depuis la refonte).
- *Fichiers* : `app/src/lib/design/Icone.svelte` (`profil`), `app/src/routes/+layout.svelte` (`.profil-haut`).
- *Commande* : `/impeccable polish`.

**13. Focus des boutons-glyphes à l'or clair.**
- *Problème* : `.glyphe:focus-visible` remplace l'anneau par un trait inférieur en `--hs-or` (1,8:1 sur la nacre), sous
  le seuil de 3:1 des indicateurs de focus ; partout ailleurs le focus est en or assombri.
- *Proposition* : `--hs-or-texte` pour ce trait, ou l'anneau commun.
- *Fichiers* : `app/src/lib/design/tokens.css` (`.glyphe:focus-visible`).
- *Commande* : `/impeccable audit`.

**14. Lecture : la ligne « Office » sans case alors que « Évangile » en a une.**
- *Problème* : dans Lectures du jour, le Petit bréviaire porte un compteur « 0/8 » en très petit corps dans la marge,
  le Bréviaire romain et l'Officium parvum rien, l'Évangile une case : trois traitements pour une même liste. Le « 0/8 »
  en italique minuscule est à peine visible.
- *Proposition* : une colonne d'état commune (case, ou compteur n/N dans le même cercle d'or que Dévotions) ; rien pour
  les lignes non comptées, mais alignées sur la même colonne.
- *Fichiers* : `app/src/routes/lecture/+page.svelte`.
- *Commande* : `/impeccable polish`.

**15. Bureau : le liseré de couleur liturgique ne suit pas le bandeau.**
- *Problème* : au bureau, le rinceau du bandeau court sur toute la largeur mais le liseré de couleur liturgique (vert
  ce jour) ne couvre que la colonne de contenu, de 308 à 1216 px : les deux filets du haut ne s'alignent pas.
- *Proposition* : étendre le liseré à toute la largeur, ou l'aligner exactement sur le cadre de 1200 px.
- *Fichiers* : `app/src/routes/+page.svelte` (liseré), `app/src/routes/+layout.svelte`.
- *Commande* : `/impeccable polish`.

### P3 — finition

**16. Office : « Recommandation » en italique parmi les heures.** L'annexe (`.heure.annexe`) passe en italique dans une
rangée de petites capitales ; la distinguer plutôt par sa place (après un filet) que par un changement de style.
*Fichiers* : `app/src/lib/Office.svelte`.

**17. Accueil : rang de perles plus large que l'arche et tronqué à droite.** Le motif `perles` sous le tableau dépasse
le cadre de chaque côté et se coupe au milieu d'un motif (« Oıı ı »). Le borner à la largeur de l'arche, en nombre
entier de motifs. *Fichiers* : `app/src/lib/design/Accueil.svelte`, `Ornement.svelte`.

**18. Pastille liturgique sans libellé accessible.** La couleur du jour n'est dite que par un `title` (survol) ; ajouter
un texte masqué (« couleur : vert ») ou `role="img"` avec `aria-label`. *Fichiers* : `app/src/routes/+page.svelte`.
**À voir avec `hortus-ux`** (accessibilité structurelle).

**19. Calendrier : nom du mois en Almendra.** C'est le seul titre de page dans une autre voix (Almendra rubis, 3 rem)
que les capitales de Cormorant ; voulu (« seul caractère d'accent de l'écran »), mais à confirmer par l'utilisateur, car
il ressemble plus à une enseigne qu'au titre courant du calendrier papier.

**20. Couche de jetons historique.** La première palette (ivoire, lapis `#304e85`, nuit `#141b2b`) reste en tête de
`tokens.css`, recouverte par les deux directions, et `--hs-lapis` désigne aujourd'hui le rubis ou le cobalt. Sans effet
visible, mais source d'erreurs pour qui ajoute un écran (voir `DESIGN.md`, « Couche historique »). Renommer en
`--hs-accent` lors d'une passe `extract`, avec l'accord de l'utilisateur.

## Personas

- **L'utilisateur, au téléphone, à l'église, la nuit** (PRODUCT.md, Users) : ouvre l'app → écran d'accueil à franchir →
  Aujourd'hui en nuit latine : l'arche bordeaux est belle mais il faut défiler pour atteindre la première case (constat
  1) ; ouvre le Chapelet : 7 400 px à faire défiler pour atteindre les mystères du jour (constat 6). La lecture
  elle-même est excellente.
- **Le même, au bureau, pour régler son profil** : l'accueil cache son bouton (constat 2) ; le Profil n'est trouvé que par
  le sommaire de gauche (au téléphone, par un lis sans libellé, constat 12) ; les dates sont en « mm/dd/yyyy » (constat
  7).
- **Un lecteur âgé ou à la vue faible** (persona du rubric) : corps de 19 px et contrastes AA partout ; gênes : compteurs
  de 13 px en Manrope (« 0/8 »), crédit du tableau à 3,3:1, fleurons éteints invisibles la nuit.

## Questions à se poser

- L'arche doit-elle garder la même taille tous les jours, ou grandir seulement les jours de fête (`solennel`), l'écran
  ordinaire restant compact ?
- L'écran d'accueil doit-il paraître à chaque session, ou une fois par jour ?
- Faut-il une seule façon de « choisir une variante » dans toute l'app ?

## Ordre de traitement proposé

1. `/impeccable typeset` : ordinaux (4), justification au téléphone (11).
2. `/impeccable polish` : fuite de la mosaïque (3), onglets (5), dates (7), `theme-color` (8), accueil (9, 17), icône du
   Profil (12), Lecture (14), liseré (15), Office (16).
3. `/impeccable layout` avec `hortus-ux` : hauteur de l'en-tête d'Aujourd'hui (1), sections de la page de pratique (6).
4. `/impeccable adapt` : accueil au bureau (2).
5. `/impeccable distill` avec `hortus-ux` : en-tête de Prières (10).
6. `/impeccable audit` : focus des glyphes (13), pastille (18).
7. `/impeccable polish` final, puis nouvelle critique.

Questions skipped: delegated run
