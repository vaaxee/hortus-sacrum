---
name: Hortus Sacrum
description: Prière quotidienne selon le calendrier romain de 1954, composée comme un livre d'église.
colors:
  latine-nacre: '#faf5ef'
  latine-nacre-rosee: '#f0e2d8'
  latine-nacre-douce: '#f6ece4'
  latine-encre: '#2a2620'
  latine-encre-douce: '#5d5647'
  latine-rubis: '#a83d49'
  latine-rubis-profond: '#7a1f2b'
  latine-rubrique: '#8f2a37'
  latine-filet: '#dcc5b8'
  latine-nuit-bordeaux: '#22080f'
  latine-nuit-surface: '#34101b'
  latine-nuit-encre: '#f3e9dc'
  latine-nuit-encre-douce: '#c9adaf'
  latine-nuit-rubis-vif: '#f08593'
  latine-nuit-rubrique: '#f4a1ab'
  latine-nuit-arche: '#6b1a2b'
  latine-nuit-filet: '#5a2230'
  grecque-ivoire: '#f6f2e7'
  grecque-surface: '#e6e2d6'
  grecque-encre: '#15154a'
  grecque-encre-douce: '#50527c'
  grecque-outremer: '#1a1a8f'
  grecque-cobalt: '#0047ab'
  grecque-cinabre: '#9c2f3c'
  grecque-filet: '#c4c2c9'
  grecque-nuit-outremer: '#0e0c52'
  grecque-nuit-surface: '#16137a'
  grecque-nuit-arche: '#1f1ca6'
  grecque-nuit-encre: '#f0e9d6'
  grecque-nuit-encre-douce: '#b3b3dc'
  grecque-nuit-cobalt: '#6f9df2'
  grecque-nuit-rubrique: '#ee8f8a'
  grecque-nuit-filet: '#2d2a94'
  or: '#d9b66d'
  or-texte: '#8a6a1f'
  or-arche: '#ecd08a'
  vert-coche: '#456b49'
  liturgique-blanc: '#f8f3e8'
  liturgique-rouge: '#a83d49'
  liturgique-vert: '#527b56'
  liturgique-violet: '#766294'
  liturgique-rose: '#b77d9b'
  liturgique-noir: '#1a1a1a'
typography:
  titre-page:
    fontFamily: "Cormorant Garamond, EB Garamond, serif"
    fontSize: '2.1875rem'
    fontWeight: 500
    lineHeight: 1.12
    letterSpacing: '0.08em'
  titre-section:
    fontFamily: "Cormorant Garamond, EB Garamond, serif"
    fontSize: '1.75rem'
    fontWeight: 500
    lineHeight: 1.2
  petites-capitales:
    fontFamily: "EB Garamond, Garamond, Times New Roman, serif"
    fontSize: '1.125rem'
    fontWeight: 400
    letterSpacing: '0.06em'
    fontFeature: 'all-small-caps'
  lecture:
    fontFamily: "EB Garamond, Garamond, Times New Roman, serif"
    fontSize: '1.1875rem'
    fontWeight: 400
    lineHeight: 1.55
    fontFeature: 'onum'
  interface:
    fontFamily: "Manrope, Helvetica Neue, sans-serif"
    fontSize: '0.8125rem'
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: '0.02em'
  accent:
    fontFamily: "Almendra, Cormorant Garamond, serif"
    fontWeight: 400
rounded:
  aucun: '0'
  tactile: '2px'
  arche: '1000px 1000px 0 0'
spacing:
  e1: '4px'
  e2: '8px'
  e3: '12px'
  e4: '16px'
  e5: '24px'
  e6: '32px'
  e7: '48px'
  e8: '72px'
  e9: '112px'
  marge-mobile: '20px'
  colonne: '680px'
  mesure: '34rem'
components:
  bouton:
    backgroundColor: 'transparent'
    textColor: '{colors.latine-rubis}'
    typography: '{typography.petites-capitales}'
    rounded: '{rounded.aucun}'
    padding: '0 16px 2px'
    height: '44px'
  bouton-principal:
    backgroundColor: '{colors.latine-rubis-profond}'
    textColor: '{colors.latine-nacre}'
    typography: '{typography.petites-capitales}'
    rounded: '{rounded.aucun}'
    padding: '0 16px 2px'
    height: '44px'
  puce:
    backgroundColor: '{colors.latine-nacre}'
    textColor: '{colors.latine-encre-douce}'
    rounded: '{rounded.aucun}'
    padding: '0 12px 2px'
    height: '36px'
  case:
    backgroundColor: '{colors.latine-nacre}'
    rounded: '{rounded.aucun}'
    size: '26px'
  case-cochee:
    backgroundColor: '{colors.vert-coche}'
    size: '26px'
  panneau:
    backgroundColor: '{colors.latine-nacre-rosee}'
    rounded: '{rounded.aucun}'
    padding: '24px'
  arche:
    backgroundColor: '{colors.latine-rubis-profond}'
    textColor: '{colors.latine-nacre}'
    rounded: '{rounded.arche}'
    width: '26rem'
---

# Design System: Hortus Sacrum

> Document descriptif du système **tel qu'il est dans le code** au 22 novembre 2026 (`app/src/lib/design/tokens.css`,
> `app/src/app.css`, `app/src/lib/design/*.svelte`, `app/src/routes/+layout.svelte`), rapproché de la charte
> (`docs/REPRISE.md` « Charte », `docs/cahier/CONTEXTE.md` § 3, `docs/charte/`, `docs/maquette/`). Il ne propose rien :
> les améliorations sont dans `docs/audits/ESTHETIQUE_2026-11-22.md`. **À relire par l'utilisateur**, en particulier le
> nom donné à l'ensemble et les règles nommées, qui sont des formulations de l'agent. Les valeurs de l'en-tête sont
> normatives ; la prose n'en redonne pas d'autres.

## Overview

**Creative North Star : « Le livre d'heures » (proposé, à confirmer).**

L'app se compose comme un livre d'église imprimé : une colonne de texte en EB Garamond, des titres en capitales
espacées de Cormorant, des petites capitales pour tout ce qui étiquette, la rubrique en rouge, les ℣ et ℟ en rouge,
beaucoup de blanc. Rien n'est arrondi : les cadres sont carrés, à double filet (le trait de la couleur, puis un filet
d'or en retrait, « comme sur une reliure »). Seule l'arche, en plein cintre roman, porte la fête du jour et l'ouverture
du mois. L'or est un **trait**, jamais un aplat. Un grain de papier très léger couvre la page.

Le système a **deux directions artistiques** et **deux moments** (jour, nuit), soit quatre jeux de couleurs :

- **Latine** (défaut) : nacre et rubis le jour, arche de rubis profond ; la nuit, bichromie de bordeaux profond et de
  rubis vif. Ornements : rinceau de vigne aux grains de rubis en bandeau, fleur de lys à la clef de l'arche, croix
  pattées aux angles.
- **Grecque** : ivoire froid et arche d'outremer le jour ; la nuit, outremer profond, cobalt éclairci pour ce qui se
  touche, or des tesselles. Ornements : mosaïque de tesselles en bandeau, grecque (méandre) en frise, chrisme à la clef
  de l'arche, palmettes aux angles, filet intérieur pointillé.

Le thème suit l'appareil, sauf choix explicite (`data-theme="jour" | "nuit"` sur `<html>`) ; la direction se pose par
`data-da="grecque"` (absence = latine). Les deux jeux d'ornements sont toujours dessinés, un seul est montré (classes
`da-latine`, `da-grecque`).

**Key Characteristics :**

- Typographie de livre : Garamond pour lire, Cormorant pour titrer, petites capitales pour étiqueter ; Manrope pour les
  seules indications d'interface (aide, compteurs, onglets internes).
- Angles vifs partout (rayon 0), sauf l'arche en plein cintre, les pastilles rondes et la zone de texte (2 px).
- Double filet (couleur + or en retrait) sur les boutons, les cases, les puces choisies.
- Ornements au trait fin, d'une seule couleur (`currentColor`), tirés de la tradition chrétienne.
- Mouvement lent et calme (240 à 400 ms, courbe douce), supprimé si l'appareil demande moins de mouvement.

## Colors

Une palette de manuscrit : un fond de papier (nacre, ivoire, ou leur nuit), une encre jamais noire, un seul accent de
couleur par direction, l'or au trait, le rouge de rubrique réservé au texte liturgique.

Les rôles sont des variables CSS (`--hs-*`), redéfinies pour chaque combinaison direction × thème. **Nom trompeur, hérité
d'une première palette** : `--hs-lapis` désigne l'accent interactif de la direction (rubis en latine, cobalt en grecque,
or en grecque nuit avant la bichromie), et non le bleu lapis.

### Primary

- **Rubis** (`latine-rubis`) : liens, boutons secondaires, cases non cochées, onglet actif, puces choisies (latine jour).
- **Rubis profond** (`latine-rubis-profond`) : fond de l'arche de la fête et du bouton principal (latine jour).
- **Rubis vif** (`latine-nuit-rubis-vif`) : même rôle que le rubis, la nuit, sur le bordeaux.
- **Outremer** (`grecque-outremer`, `grecque-nuit-outremer`) : arche et bouton principal le jour, fond de page la nuit
  (grecque). La charte du dépôt cite `#0E0C52`, qui est le fond de nuit.
- **Cobalt** (`grecque-cobalt`, `grecque-nuit-cobalt`) : « artefacts » de la grecque : liens, boutons, cases, icônes de
  la barre d'onglets.

### Secondary

- **Or** (`or`) : filets, ornements, niche de l'onglet actif, losange des bascules ; jamais en aplat, jamais en texte
  courant sur fond clair.
- **Or assombri** (`or-texte`) : anneau de focus, losange des bascules, cartouche « Livret » : l'or là où il doit rester
  lisible sur le clair.
- **Or de l'arche** (`or-arche`) : nom de la fête et filet sur l'arche (les deux directions).

### Tertiary

- **Rubrique** (`latine-rubrique`, `grecque-cinabre`, et leurs nuits) : ℣, ℟, titres de rubrique, lettrine, intitulés
  de section en lecture, messages d'erreur, jeûne et abstinence.
- **Vert de la coche** (`vert-coche`) : case cochée, heure d'office dite, barre de progression.
- **Couleurs liturgiques** (`liturgique-*`) : pastille ronde cerclée d'or et liseré sous le bandeau du haut ; la nuit,
  chacune a sa variante éclaircie dans `tokens.css`. Les livrets imprimés en ont d'autres valeurs (violet `#603078`,
  rouge `#B01E24`…), non reprises dans l'app.

### Neutral

- **Nacre**, **nacre rosée**, **nacre douce** (latine jour) ; **bordeaux profond** et ses surfaces (latine nuit) ;
  **ivoire froid** (grecque jour) ; **outremer profond** et ses surfaces (grecque nuit) : fond de page, panneaux,
  barre d'onglets.
- **Encre** et **encre douce** : texte courant et texte secondaire (dates, aides, onglets inactifs).
- **Filet** : séparateurs de listes, bords des puces et des panneaux (pierre chaude, rose de nacre, ou bleu de nuit).

### Couche historique

`tokens.css` garde en tête une première palette (ivoire `#f8f3e8`, lapis `#304e85`, nuit d'encre de lapis `#141b2b`).
Elle est entièrement recouverte par les deux directions, mais sert encore aux méta `theme-color` de `app.html` et au
`background_color` du manifeste.

### Named Rules

**La règle de l'or au trait.** L'or dessine (filets, ornements, focus), il ne remplit jamais une surface.

**La règle de la rubrique.** Le rouge de rubrique est réservé à ce que le livre imprimé mettrait en rouge : ℣, ℟,
rubriques, lettrines, intitulés liturgiques, jeûne. L'accent interactif a sa propre variable.

**La règle de l'encre.** Jamais de noir pur : l'encre est un brun très sombre (latine) ou une encre d'outremer
(grecque) ; la nuit, une encre d'ivoire.

## Typography

**Display Font :** Cormorant Garamond (repli EB Garamond)
**Body Font :** EB Garamond (repli Garamond, Times New Roman)
**Label Font :** Manrope (interface), EB Garamond en petites capitales (étiquettes)
**Accent :** Almendra (nom du mois du calendrier, marque « Hortus Sacrum » au bureau) ; IM Fell English (classe
`imprime`, peu employée)

**Character :** Un Garamond de livre de prières, servi en chiffres elzéviriens, avec un Cormorant aux capitales
largement espacées pour les titres ; le sans-serif Manrope ne sert qu'aux indications de mécanique (compteurs, aide).

Échelle de rapport 1,25 ancrée sur 18 px (t1 à t6 : 18, 22,5, 28, 35, 44, 55 px) ; corps de lecture 19 px, interligne
1,55, rythme vertical 28 px, mesure 34 rem (60 à 68 signes).

### Hierarchy

- **Titre de page** (Cormorant 500, 28 px au téléphone, 35 px dès 700 px, capitales, chasse 0,08 em) : « PRIÈRES »,
  « CHAPELET », nom de la fête dans l'arche.
- **Titre de section** (Cormorant italique 500, 28 px ; 22,5 px en tête de section) : « Matin », « Au fil du jour »,
  « En cours ».
- **Petites capitales** (EB Garamond, toutes petites capitales, chasse 0,06 em) : sous-titres h3, étiquettes, date,
  temps liturgique, boutons, onglets.
- **Lecture** (EB Garamond 19 px / 1,55) : justifiée et césurée ; versets, psaumes et offices au fer à gauche ; latin en
  italique (`[lang='la']`) ; lettrine de rubrique sur deux lignes au premier paragraphe d'une prière.
- **Interface** (Manrope 500, 13 px) : aides, compteurs (« 0 / 9 · 1 h 37 restantes »), onglets internes (mystères,
  bréviaires), lien « retour ».

### Named Rules

**La règle des petites capitales.** Tout ce qui étiquette (date, rang, bouton, onglet, légende) est en petites capitales
de Garamond, pas en capitales tapées ni en gras.

**La règle du fer à gauche.** Un paragraphe qui contient ℣/℟ ou des retours de ligne (psaume, hymne, litanie) n'est
jamais justifié.

## Layout

- **Téléphone** : une colonne de 680 px au plus, marges de 20 px, en-tête de page centré (titre, fleuron sur filet),
  barre d'onglets fixe en bas (cinq onglets : Aujourd'hui, Lecture, Prières, Dévotions, Calendrier), Profil en icône
  ronde en haut à droite. Bandeau ornemental en tête, sous la zone de l'encoche (`safe-area-inset-top`) ; une bande de
  couleur de fond masque l'heure du téléphone pendant le défilement. La barre d'onglets réserve la zone de
  l'indicateur d'accueil (`safe-area-inset-bottom`).
- **Bureau (≥ 900 px)** : colonne de gauche de 220 px, collante, séparée d'un filet (« la table d'un beau livre »),
  marque « Hortus Sacrum » en Almendra avec le chrisme, puis les cinq rubriques et le Profil ; le contenu garde sa
  colonne de 680 px (980 px pour les pages `large` comme l'année).
- **Rythme** : espacements en base 8 (4 à 112 px) ; listes réglées à lignes de 56 px au moins, séparées d'un cheveu.
- **Impression** : sans navigation ni grain, encre sur blanc.

## Elevation & Depth

Système **plat**, à profondeur tonale : le fond, une surface (« parchemin », nacre rosée, ou surface de nuit) pour les
panneaux et l'arche, et des filets. Les seules ombres sont des filets intérieurs (`inset`) qui dessinent le double filet
des boutons, des cases et des puces, et une ombre très douce au-dessus de la barre d'onglets.

### Shadow Vocabulary

- **Double filet** (`box-shadow: inset 0 0 0 2px var(--hs-fond), inset 0 0 0 2.75px var(--hs-or-trait)`) : le filet
  d'or en retrait des boutons, des cases et des bascules.
- **Barre d'onglets** (`box-shadow: 0 -6px 14px -12px` encre à 40 %) : sépare la barre du texte qui défile dessous.

### Named Rules

**La règle du papier.** La profondeur vient du papier et des filets, pas d'ombres portées ni de flou.

## Shapes

- **Angles vifs** (0) pour tout : boutons, puces, cases, panneaux, cartouches, champs (filet en pied seulement).
- **Plein cintre** pour l'arche de la fête et l'ouverture du mois (arc roman, 26 rem au plus) ; la niche de l'onglet
  actif reprend le même arc, une croisette d'or à la clef.
- **Ronds** : pastille liturgique (11 px, cerclée d'or), compteur n/N des dévotions (cercle d'or), icône du Profil.
- **Losange d'or** (6 px) : marque de l'état choisi des bascules et des puces.
- Ornements : fleuron (fleur de lys entre deux croisettes en latine), rinceau de vigne, grecque (méandre), mosaïque,
  laurier, perles, palmette, coin (quart de rosace), médaillon, chrisme, lis, croix, croix pattée, chérubin du calendrier
  papier (`cherub.tex`, retranscrit trait pour trait), brin (qui se dessine dans la case cochée). Tous au trait,
  `currentColor`, `aria-hidden` sauf titre.

## Components

### Buttons

Un seul système, d'après les livres d'église.

- **Forme :** carré (0), hauteur et largeur 44 px au moins, petites capitales d'EB Garamond 17 px, chasse 0,07 em.
- **Secondaire (défaut) :** cadre de l'accent, texte de l'accent, filet d'or intérieur ; au survol, fond teinté de
  l'accent à 8 % et or plein.
- **Principal :** aplat de l'arche (rubis profond ou outremer), texte nacre, filet d'or de l'arche en retrait.
- **Danger :** cadre et texte de rubrique, sans or. **Discret :** texte seul, souligné d'un cheveu d'or au survol.
  **Icône :** carré de 44 px sans cadre.
- **Bascule** (`aria-pressed`) : enfoncée, fond teinté à 12 %, or plein, et un losange d'or apparaît avant le libellé.
  **Segments :** bascules jointives (Mois / Semaine / Année ; Toutes / Favoris / Mes ajouts).
- **Focus :** anneau de 2 px en or assombri, décalé de 3 px. **Désactivé :** opacité 0,42.

### Chips

- **Puce de filtre :** cartouche carré de petites capitales, 36 px de haut (zone tactile portée à 44 px), cheveu de
  filet ; choisie, cadre de l'accent, fond teinté à 9 %, losange d'or. Rangées de thèmes et de types défilant à
  l'horizontale (Prières).
- **Cartouche (badge) :** petites capitales 13 px, cheveu de `currentColor` : « Livret » (or assombri), « Source
  officielle vérifiée » (vert), « Ajout personnel » (accent), indulgence (rubrique).

### Cards / Containers

- **Panneau :** carré, surface, cheveu de filet, 24 px de marge intérieure ; variante à filet d'or en tête ; double
  filet d'or pour les grandes fêtes.
- **Arche** (`Arche.svelte`) : plein cintre, aplat de l'arche, filet d'or de l'arche, nom de la fête en capitales
  Cormorant, rameau de laurier sous le nom ; ornements de la direction à la clef et aux angles ; `solennel` ajoute les
  coins.
- **Carte de couronne** (`CarteCouronne.svelte`) : carte enluminée à quatre coins, couronne dessinée, verset latin et
  français en exergue, promesse sourcée.

### Inputs / Fields

- **Champ :** fond transparent, un seul filet en pied, Garamond ; au focus, le filet prend l'accent.
- **Zone de texte :** cheveu de filet tout autour, surface douce, rayon de 2 px.
- **Étiquette :** petites capitales de Garamond 16 px en encre douce ; légende de `fieldset` en rubrique.
- **Case à cocher :** même dessin que la case de la liste du jour (22 px pour les cases natives, 26 px pour `Case`).

### Navigation

- **Barre d'onglets (téléphone) :** fond surface douce mêlée au fond, double filet en tête (or puis pierre), grain
  propre ; icône 22 px et nom en petites capitales 14 px ; l'onglet actif se loge dans une **niche** en plein cintre
  cerclée d'or, croisette à la clef, nom en accent et en gras.
- **Sommaire (bureau) :** liens en petites capitales, l'actif en accent avec un trait d'or à gauche.
- **Onglets internes** (bréviaires, séries de mystères) : texte Manrope souligné d'un trait sous l'actif.
- **Heures d'un office :** bascules de petites capitales comme les puces ; l'heure dite en vert, l'heure ouverte avec le
  losange d'or.

### La case de la liste du jour (signature)

Case carrée à double filet (`Case.svelte`), cadre de l'accent ; cochée, elle se remplit de vert et un **brin** s'y
dessine trait après trait, jamais une coche ordinaire.

### L'écran d'accueil (signature)

`Accueil.svelte` : nom de l'app en capitales d'or, fleuron, le *Couronnement de la Vierge* de Velázquez (v. 1635, Prado)
dans une arche filetée d'or sous une croix pattée de rubis, chérubins de part et d'autre, rang de perles, Introït du
jour, invocation au saint du jour, trois fleurons d'avancement (matin, jour, soir), bouton « Entrer au jardin ». Une
fois par session d'onglet ; la barre d'onglets est masquée pendant ce temps.

### Icônes

`Icone.svelte` : icônes au trait « comme une gravure », trait principal 1,5 px, tailles et hachures 0,75 px, tirées de
symboles chrétiens (le Profil est une fleur de lys).

## Do's and Don'ts

### Do:

- **Do** passer par les variables `--hs-*` : une couleur écrite en dur ne suit ni la nuit ni l'autre direction.
- **Do** dessiner chaque ornement dans les deux directions (`da-latine` / `da-grecque`) quand il est propre à l'une.
- **Do** garder l'or au trait et les angles vifs ; l'arche est la seule courbe de structure.
- **Do** composer le texte liturgique au fer à gauche dès qu'il porte ℣/℟ ou des retours de ligne.
- **Do** vérifier chaque écran dans les quatre combinaisons (latine/grecque × jour/nuit), au téléphone et au bureau.

### Don't:

- **Don't** modifier un texte religieux (prière, rubrique, office, méditation) pour la mise en page.
- **Don't** introduire un symbole étranger à la tradition catholique, ni une image générée présentée comme ancienne.
- **Don't** arrondir les boutons, puces ou panneaux, ni ajouter des ombres portées.
- **Don't** utiliser l'or en aplat, ni le rouge de rubrique comme simple couleur d'accent d'interface.
- **Don't** utiliser du noir pur pour l'encre.
