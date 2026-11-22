# Product

<!-- impeccable:product-schema 1 -->

> Fiche rédigée le 22 novembre 2026 par l'agent Esthétique, **à relire par l'utilisateur** (décision du 22 nov. : « je
> rédige, vous relisez »). Tout vient des documents du dépôt (`docs/cahier/SPEC.md`, `docs/cahier/CONTEXTE.md`,
> `docs/REPRISE.md`, `CLAUDE.md`) ; rien n'a été obtenu par questionnaire. Ce que ces documents ne disent pas est posé en
> **question ouverte** (dernière section), jamais deviné. En cas de désaccord, la SPEC et les décisions explicites de
> l'utilisateur priment sur cette fiche (CLAUDE.md § 21).

## Platform

web

Application web progressive (PWA, SvelteKit avec adapter-static, local-first avec Dexie), installée sur l'écran d'accueil
du téléphone ; consultée aussi au bureau. Pas d'application native.

## Users

- **Utilisateur principal : un seul, connu.** Un catholique attaché à la liturgie traditionnelle, qui veut une vie de
  prière ordonnée : une liste quotidienne fixe (l'« Ordinaire ») et un « Propre » qui suit le temps liturgique, le
  sanctoral, le mois, les neuvaines, trentains et dévotions à jours comptés en cours (CONTEXTE § 1).
- Il est aussi **le bêta-testeur** de l'app : chaque exemple qu'il signale illustre un principe à corriger partout
  (SPEC § 11).
- Il a des exigences de lettré : textes anciens mot pour mot, latin, références d'édition et de page, indulgences d'après
  l'Enchiridion de 1952 ; « tolérance zéro pour l'approximatif » (CONTEXTE § 2).
- Avant l'app, il utilisait une page Notion (« Hebdomada in Dei servitio », jugée « médiocre » : statique, sans rappels,
  prières qui ne s'ouvrent pas) et deux livrets imprimés validés avec lui : *Le Jardin de l'âme* (84 p., 11 × 17 cm) et le
  *Calendrier liturgique 2026-2027* (136 p.).

## Product Purpose

Donner chaque jour, sur le téléphone, **ce qu'il y a à prier aujourd'hui et pourquoi**, selon le calendrier romain de
1954, et ouvrir chaque prière à son texte sourcé.

- La journée est **calculée** (`journee(date, contexte)`) à partir d'un programme unique livré comme donnée, et non
  stockée comme une liste (CLAUDE.md § 3).
- Écrans : Aujourd'hui (bandeau liturgique, vie du saint, méditation, liste à cocher, martyrologe), Lecture (Office,
  Écriture, Doctrine, Spirituel), Prières (bibliothèque), Dévotions (suivis en cours et à venir), Calendrier (mois,
  semaine, année), Profil (anniversaires spirituels, saints favoris, rappels, recueils) (SPEC § 1, § 11).
- Réussite : une journée de prière ordonnée, « le plus de dévotion avec le moins d'actes séparés, pour garder du temps
  pour le devoir d'état » (SPEC § 10).

## Positioning

- **Le calendrier de 1954 et l'Office d'avant 1955**, calculés (moteur fondé sur les données de Divinum Officium), et non
  un calendrier générique.
- **Uniquement des sources anciennes identifiées**, recopiées mot pour mot avec ouvrage, édition et page ; aucun texte de
  mémoire, aucun texte généré ; ce qui manque va dans `A_FOURNIR.md` (CLAUDE.md § 13).
- **Indulgences** comptées seulement d'après l'Enchiridion de 1952, avec la règle des traductions approuvées (SPEC § 11,
  « Indulgences »).
- **Une composition traçable** : chaque ligne du jour sait pourquoi elle est là (règle, dimension, source, priorité)
  (CLAUDE.md § 8).

## Operating Context

- **Téléphone d'abord** : lecture de prières longues, souvent debout ou à genoux, à l'église, le matin, à midi
  (Angélus), le soir, la nuit. Le thème de nuit existe pour cela ; la zone sûre de l'encoche de l'iPhone est une exigence
  explicite (SPEC § 11, « Décor »).
- **Lecture longue, latin et français** : offices (Petit bréviaire du Sacré-Cœur, Bréviaire romain en latin seul,
  Officium parvum), méditations (Hamon, Chaignon, Guéranger, livres de mois), Écriture (Vulgate et Crampon 1923), latin
  en premier quand la concession est latine (SPEC § 11, décision du 20 nov.).
- **Liste à cocher** : chaque élément coché est horodaté ; lignes « selon le jour » (chapelet, Triple Couronne, litanies,
  couronnes) ; durées estimées et total du jour.
- **Rappels** (push via Supabase, sans compte) : matin, soir, veilles, anniversaires, heures fixes (Angélus, 15 h le
  vendredi).
- **Impression** : livret 110 × 170, fiche du jour A5, calendrier A4 (`/imprimer`), héritiers des livrets papier.
- **Bureau** : même app, navigation en colonne de gauche « comme la table d'un beau livre ».

## Capabilities and Constraints

- **Tout est modifiable par l'utilisateur** : prières, pratiques, liste, recueils, calendrier ; trois saisies (clavier,
  copier-coller nettoyé, PDF ou photo avec OCR) ; badges d'origine (« Livret », « Source officielle vérifiée », « Ajout
  personnel »), « Restaurer l'original », corbeille, export JSON (SPEC § 9).
- **Une correction livrée n'écrase jamais une modification de l'utilisateur** (surcouche, `revision`) (CLAUDE.md § 12).
- **Déterminisme** : même date et même contexte, même journée (CLAUDE.md § 9).
- **Une prière n'apparaît qu'une fois par jour**, y compris dans une page composée ; un test le garantit (SPEC § 11.1).
- **Le texte religieux n'est jamais réécrit pour la mise en page** ; la présentation est séparée du contenu sourcé
  (CLAUDE.md § 11).
- Hors ligne : données livrées dans l'app (`static/data`), base locale ; le Bréviaire romain est résolu hors ligne pour
  2026-2027.
- Pas de propre de France (calendrier romain universel) ; fêtes personnelles ajoutées dans l'app (SPEC § 9).
- Terminologie à garder : Ordinaire, Propre, office, rang, commémoraison, Introït, station, Quatre-Temps, rubrique, ℣/℟,
  neuvaine, trentain, couronne, jaculatoire, indulgence, « usage » (en minuscules).

## Brand Commitments

- **Nom** : *Hortus Sacrum* ; devise de la page Notion d'origine : *Hebdomada in Dei servitio*.
- **Voix** : française, sobre, liturgique ; vouvoiement dans les invocations ; pas de ton « gamifié » (les couronnes sont
  des « cartes enluminées », pas des « succès débloqués » ; REPRISE, point 8).
- **Charte héritée des livrets** (CONTEXTE § 3) : EB Garamond, petites capitales, chiffres elzéviriens, rouge rubrique,
  ℣ et ℟ en rouge, mise en page sobre et typographique. Ornements de la charte : croix en gloire avec anges hérauts,
  ange héraut, chérubin du calendrier (`docs/charte/`).
- **Deux directions artistiques** choisies par l'utilisateur : latine (nacre et rubis ; bordeaux la nuit) et grecque
  (outremer et cobalt). Leur détail visuel est dans `DESIGN.md`.
- **Décor catholique seulement** : aucun symbole étranger à la tradition catholique ; aucune image générée présentée
  comme une œuvre ancienne. L'écran d'accueil montre une œuvre ancienne identifiée (Velázquez, *Le Couronnement de la
  Vierge*, v. 1635, Prado, domaine public).

## Evidence on Hand

- Textes : `data/prieres/sources.json`, `data/recueils/`, `data/ecriture/`, `data/office/`, `data/calendar/`, avec leurs
  sources dans `SOURCES_UTILISEES.md` ; manques dans `A_FOURNIR.md`.
- Livrets : `docs/livret/`, `docs/calendrier/` (sources LaTeX, dont le chérubin `cherub.tex`).
- Charte : `docs/charte/gloire.pdf`, `angelot.pdf`, `cherubin.pdf`.
- Maquettes validées : `docs/maquette/` (Aujourd'hui, liste, prière, mois ; jour et nuit ; outremer).
- Audits : `docs/audits/` (ergonomie du 18 nov., dévotions, corpus, consignes, esthétique du 22 nov.).
- **Absences à ne pas combler** : aucun témoignage, aucune statistique d'usage, aucune promesse de dévotion sans source
  ancienne (elles sont retirées de l'affichage tant qu'aucune source n'est trouvée).

## Product Principles

1. **Le texte sourcé est intouchable.** Mot pour mot, avec sa source ; ce qui manque se demande, ne s'invente pas.
2. **Intégrer plutôt qu'ajouter.** Une petite prière se glisse dans une séquence hôte (fin de dizaine, Angélus, matin,
   soir, fin de l'office du saint) au lieu de devenir une tâche (SPEC § 11.2).
3. **Écran du jour sobre.** Les jauges et le bilan se dévoilent par un bouton ; ce qui se lit sort de la liste vers
   Lecture (SPEC § 11.3 et 11.5).
4. **Une prière, une fois par jour ; une page par pratique**, en sections dépliables (SPEC § 11.1 et 11.4).
5. **Tout reste modifiable**, et la décision du programme reste explicable (pourquoi cette ligne aujourd'hui).

## Accessibility & Inclusion

- Lisibilité longue au téléphone, de jour comme de nuit : contrastes WCAG AA dans les quatre combinaisons
  (deux directions × jour/nuit).
- Zone sûre de l'encoche et de l'indicateur d'accueil respectée ; cibles tactiles de 44 px.
- Libellés ARIA des boutons-icônes ; l'état d'une bascule ne tient pas qu'à la couleur.
- Mouvement réduit respecté (`prefers-reduced-motion`).

## Questions ouvertes pour l'utilisateur

Les documents ne répondent pas à ces points ; ils sont laissés ouverts plutôt que devinés.

1. **Autres utilisateurs** : l'app est-elle pour vous seul, ou destinée à être partagée (famille, fidèles d'une
   chapelle) ? Cela change le ton des textes d'aide et l'accueil d'un nouveau venu.
2. **Direction par défaut** : la latine est le défaut dans le code, mais le manifeste de l'app installée annonce
   l'outremer de la grecque. Laquelle doit être la « vraie » couleur de l'app installée ?
3. **Lecture à l'église** : faut-il une présentation dédiée (plus grand corps, écran qui reste allumé, luminosité
   réduite) pour prier sans toucher le téléphone ?
4. **Âge et vue** : une taille de texte réglable dans l'app est-elle souhaitée, au-delà du zoom du système ?
5. **Impression** : les pages imprimables doivent-elles suivre la direction choisie, ou toujours la charte des livrets
   (encre et rubrique sur blanc) ?
6. **Langue de l'interface** : le français seul, ou un jour le latin pour les libellés (onglets, mois) ?
