# Audit des consignes (20 novembre 2026)

Cet audit vérifie que chaque demande de l'utilisateur a été traitée, depuis la reprise du 13 novembre. Les décisions
d'avant le 13 novembre sont reprises de `docs/cahier/*` et de `A_FOURNIR.md`.

**Méthode**
- **Demandes** : 66 messages tapés par l'utilisateur et 13 réponses à des questions interactives. Ils ont été extraits
  du transcript par un script (`/tmp/claude-0/audit-consignes/scripts/extract.py`, sortie `demandes.txt`), sans les
  résultats d'outils, les notifications ni les messages d'agents. S'y ajoutent les 11 captures jointes.
- **Rapports** : SPEC § 9 à 11, `PLAN_GENERAL.md`, `REPRISE.md`, `A_FOURNIR.md`, `docs/audits/*` et
  `docs/conception/REFONTE_2026-11-18.md`.
- **App** : elle a été vérifiée sur `main` (a8d8205, PR n° 37).
  - Construction : `npm run build` et `vite preview`.
  - Navigation : Playwright en 390 × 844, base remplie après « Entrer au jardin ».
  - Dates testées : 15 au 21 novembre 2026, 5 et 8 décembre, 5 mars 2027 (Carême), 5 avril 2027 (temps pascal), 1er mai et
    15 septembre 2027.
  - Captures et textes : `/tmp/claude-0/audit-consignes/`.
  - Contrôles : `eslint .` (0 erreur, 74 avertissements) ; `vitest run` (131 tests sur 131).

**Statuts** : *appliqué*, *corrigé*, *abandonné*, *en cours*, *oublié* et *contredit*.
- Une demande dont un lot planifié n'est pas encore commencé est classée « en cours (planifié) ».
- Une demande traitée sur une branche de travail non fusionnée est classée « en cours (non fusionné) ».

## 1. Reprise, roue, indulgences, accueil (13 et 14 novembre)

| Date | Demande | Statut | Preuve | Remarque |
|---|---|---|---|---|
| 13/11 | Reprendre `REPRISE.md`, les 4 chantiers « tout à la suite » | appliqué | `docs/REPRISE.md` § Reste à faire, points 1 à 9 | — |
| 13/11 | Guéranger d'après abbe-pivert.com / domgueranger.net | en cours | REPRISE pt 1 : 202 lectures sur 423 en texte propre ; t. 8-15 relus : 1c2d621, 5a7710f (branche non fusionnée) | Agent « relecture de Guéranger » |
| 13/11 | Roue symbolique (1, 3, 4, 7, 12… toutes les symboliques) | appliqué | `data/roues.json` : 28 roues ; `/roue` (capture `p-roue.png`) | — |
| 13/11 | Un onglet « sublime » pour la roue | appliqué | `/roue`, reliée depuis Dévotions | La roue a quitté la barre d'onglets (REFONTE § 4.1) |
| 13/11 | Départ au 1er dimanche de l'Avent | appliqué | `/calendrier/annee` : « Du premier dimanche de l'Avent… » | — |
| 13/11 | Sources : Isidore, bibliotheque-catholique.com, recherche approfondie | appliqué | Hamon `vendor/sources/hamon/bc{1,2,3}.pdf` ; liberius.net ; archive.org | — |
| 14/11 | Thèmes interchangeables pour chaque nombre de la roue | appliqué | Déjà en place, d'après l'utilisateur (message de 05:38) | — |
| 14/11 | Barre qui totalise les indulgences et les promesses selon les coches | appliqué | Jauges « Indulgences » (`jour-2026-11-18.png`) | Le lot 2 les replie derrière un bouton |
| 14/11 | Intention affichée **avant** la prière, selon le jour du calendrier (ex. Salve Regina) | appliqué | `p-salve.png` : usage, « Selon le jour », note sur l'intention, en tête ; `p-angelus.png` : « intention : » en tête | Principe généralisé : Angélus, prière du matin. Depuis 1952, l'intention de Pie VI n'est plus une condition (c'est indiqué sur la page) |
| 14/11 | Versets du Salve Regina : « Dignare me » ? | appliqué | Page Salve : ℣. Dignare me, Ench. 1952 n° 293 | — |
| 14/11 | Lignes non cliquables (ex. chapelet) | corrigé | `links-2026-11-18.txt` : chaque ligne ouvre sa page (Chapelet → `hortus:chapelet-glorieux`) | Autres occurrences : les 27 lignes ont un lien, sauf le champ « Intentions particulières » |
| 14/11 | Indulgences non signalées (ex. actes de foi, d'espérance et de charité du matin) | corrigé | `p-matin` : « 3 ans (acte de foi) + 3 ans… » (n° 36) | Autres occurrences : Credo et Confiteor comptés matin et soir. La prière du soir n'a pas d'actes |
| 14/11 | Travail d'archiviste : « constituer une grande bibliothèque » | appliqué | `sources.json` : 173 pièces de 18 sources ; livret : 62 pièces | — |
| 14/11 | Écran d'accueil : Vierge, introït, invocation, avancement discret, titre | appliqué | `00-accueil.png` ; `Accueil.svelte` (trois fleurons d'avancement) | — |
| 14/11 | Le tableau d'origine si la gravure n'est pas assez belle | appliqué | `Accueil.svelte:16` : `'tableau'` par défaut | — |
| 14/11 | Plus de décor sur l'accueil | appliqué | Frises, coins, chérubins (`00-accueil.png`) | — |
| 14/11 | Remplir la roue ; ex. les évangélistes doivent ouvrir le chapitre du jour | appliqué | 0 élément sans lecture sur les 28 roues ; `/ecriture` (Crampon 1923 et Vulgate) ; Lecture › Évangile « Saint Jean, chapitre 21 » | Principe appliqué à toutes les roues (verset de l'Écriture) |
| 14/11 | Vue de l'année : temporal, mois, dévotions personnelles, dates de vie ; frise et roue, départ à l'Avent, toucher = ouvrir le jour, rappel la veille, action de grâces | appliqué | `/calendrier/annee` (capture `p-annee.png`), `annee.ts` testé, `anniversaires.ts` | — |
| 14/11 | Renvoyer le lien de l'app | appliqué | Réponse de 04:47 (hortus-sacrum.vercel.app) | — |
| 14/11 | Litanies des défunts (FSSPX Canada, salve-regina.com, Petit Sacristain) | appliqué | Lundi 16 nov. : « Litanies pour la délivrance des âmes du purgatoire » | — |
| 14/11 | Cordon : improviser une formule de consécration à la chasteté | appliqué | `hortus:renouvellement-cordon-saint-joseph`, marquée « composée pour Hortus Sacrum » | — |
| 14/11 | Décor : « les décorations ne sont pas mobiles comme le reste » | corrigé | Commit 2af80a6 : « frises et coins défilent avec le contenu » | — |
| 14/11 | « Succès » sobres (couronnes) ; réponses : ton liturgique, quêtes, série qui recommence, rien de partagé | appliqué | `couronnes.ts` (testé), Profil › Couronnes (`page-profil.png`) | — |
| 14/11 | PDF de Hamon | appliqué | REPRISE pt 2 : Hamon relu en entier le 14 nov. | — |
| 14/11 | Source du compteur : Enchiridion, puis Beringer, puis Thésaurisons | abandonné | Remplacé par la décision du 19/11 (Ench. 1952 seul, SPEC § 11) | Décision de l'utilisateur |
| 14/11 | Plénières : compter seulement les partielles | appliqué | « indulgences partielles seulement » sur l'écran du jour | — |
| 14/11 | Promesses : seulement les approuvées | appliqué | SPEC § 11, arbitrages : promesses sans source retirées | — |
| 14/11 | Roue : les lignes viennent « par la roue » (litanies) | en cours | SPEC § 11 : une seule litanie, celle de la roue ; `programme.json` | Le mercredi, l'app montre encore deux fois les litanies de saint Joseph (§ 4) |
| 14/11 | Chaignon : notes en fin de méditation, tout le livre, chercher une meilleure édition | appliqué | 196 sections « ### Notes » ; commits d5449b3 et 73f6767 ; aucune autre édition en ligne (REPRISE) | **Principe non généralisé** : Hamon garde environ 141 notes au milieu du texte (§ À traiter) |

## 2. Viabilité et bug des coches (15 novembre)

| Date | Demande | Statut | Preuve | Remarque |
|---|---|---|---|---|
| 15/11 | Bug : prières cochées d'avance les jours suivants, impossibles à décocher | corrigé | Commit e4dab5b. Test Playwright : une coche du 20 n'apparaît ni le 21 ni le 27 ; elle se retire et se remet | — |
| 15/11 | Mettre les « devoirs » dans l'office du matin, tous ensemble | appliqué | `hortus:offrande-du-matin` : « Actes des devoirs de charité » (5 devoirs) | — |

## 3. Critique du 17 novembre (SPEC § 10)

| Date | Demande | Statut | Preuve | Remarque |
|---|---|---|---|---|
| 17/11 | Martyrologe : invocations latines chantables pour tous les saints | appliqué | Écran du jour, section Martyrologe (`txt-jour-*.txt`) | **Défauts à reprendre** : français et latin en désaccord le 18/11 (« Saint Pierre, priez pour nous » / « Sancti Petre et Paule ») ; découpage faux le 20/11 (« Sancti Octávi, Solutor, Adventor et Thebána ») |
| 17/11 | Dévotions combinées (ex. les 3 Ave de sainte Gertrude au début du chapelet) | appliqué | `hortus:chapelet-*` : « Les trois Ave de sainte Mechtilde » dans l'ouverture | Principe repris dans `programme.json` (insertions) |
| 17/11 | Méthode de Montfort et 30 clausules en latin et en français, toutes de Montfort | **contredit** | `hortus:chapelet-glorieux` : pour chaque mystère, l'offrande et « Grâce du mystère… » en **français seulement** | Aucun latin, et aucune décision écrite qui y renonce |
| 17/11 | Regina cæli à la place de l'Angélus au temps pascal | appliqué | 5/4/2027 : « Angélus / Regina Cæli » | — |
| 17/11 | Cordon : une invocation (Litanies de saint Joseph) avant chaque Gloria | appliqué | `hortus:cordon-sept-gloria` (latin et français) | Le mercredi, le programme retire ces invocations, déjà dites dans les litanies (arbitrage écrit) |
| 17/11 | Sub tuum : invocations « Domina nostra… » en latin et en français | appliqué (latin) / abandonné (français) | `p-sub-tuum` ; SPEC § 11 : « on garde le latin seul » faute de source | — |
| 17/11 | Méditations pleines de fautes : tout relire | en cours | Commits Berlioux (bf449f3), Hamon, Chaignon, Visites (aba0678), Joseph (0d9e22a), Marie (75182bc), Sacré-Cœur (173f7f3) ; Guéranger en cours | Hamon (12 janv.) : « 1 Cor., 117, 27 », « en semble », « c'est-à - dire », en-tête courant « Bl. H. – T. I. » (21 occurrences) |
| 17/11 | Invocation répétée : la compter autant de fois qu'elle est dite | corrigé | Triple Couronne : « 5 × 300 jours » ; Jahenny : « 5 × 500 jours » | Généralisé |
| 17/11 | Dévotions « terminées » sans avoir été commencées | corrigé | `devotions/+page.svelte:109-110` : « passée, non commencée » | **Cas voisin** : « Douze samedis avant l'Immaculée Conception, à partir du 19 sept., 0/12 » apparaît « En cours » alors que rien n'est coché (`pratiques.ts:145-148`) |
| 17/11 | Triple Couronne : invocation propre et mystères de la couronne du jour | corrigé | `p-tc1` : sections « Invocation propre » et « Mystères » | — |
| 17/11 | Petit bréviaire du Sacré-Cœur | appliqué | 12 pièces `breviaire-sc:*` (offices, messe, litanies, neuvaine) ; Lecture › Office | — |
| 17/11 | Prières et promesses de sainte Gertrude | appliqué / en cours | 26 pièces `gertrude:*` ; pièces hors liste : 13866b2 (non fusionné) | Agent « Gertrude » |
| 17/11 | Jaculatoires « les plus rentables » : un recueil classé et une ligne du jour | appliqué / en cours | `thesaurisons:jaculatoires-classees` et 40 jaculatoires | La ligne « Jaculatoires du jour » doit laisser place à la jaculatoire d'ouverture (lot 2) |
| 17/11 | Apostolat de la prière | appliqué | `ramiere:offrande-quotidienne`, `ramiere:pratiques-apostolat` | Reste la prière du Cœur agonisant (A_FOURNIR) |
| 17/11 | Sainte Face | appliqué | 9 pièces `janvier:*` (neuvaine, chemin de croix, rosaire, petit office) | — |
| 17/11 | Scapulaire de Marie-Julie Jahenny | appliqué | `jahenny:scapulaire-benediction-protection` | Son intégration au matin et au soir est en cours (§ 4) |
| 17/11 | Durée de chaque prière et total du jour, calculés et modifiables | appliqué | « ≈ 13 min », total « 2 h 34 » ; champ durée dans `liste/+page.svelte:284` | — |
| 17/11 | Cadre pratique : étiquettes et bilan du jour | appliqué | `etiquettes.ts` ; « Bilan du jour… 4 manquent » | Le lot Dimensions doit le reprendre (§ 6) |
| 17/11 | Mettre les consignes dans la fiche de conception | appliqué | SPEC § 10 | — |
| 17/11 soir | Triple Couronne : trois pages, seule celle du jour | appliqué | Lun. et mer. : 1re ; mar. et ven. : 2e (relevés des 16, 17, 18 et 20 nov.) | — |
| 17/11 soir | Offrande du matin en une page, sans ce qui répète la prière du matin | appliqué | `hortus:offrande-du-matin` | Le programme fond l'offrande dans la prière du matin (lot 4) |
| 17/11 soir | Invocations chantées sans le lieu (sauf sainte Barbara) | appliqué | 4/12 : « Sancta Bárbara, virgo Nicomedíæ » ; les autres saints n'ont pas de lieu | — |
| 17/11 soir | Une page par chapelet, méthode de Montfort, note de saint Dominique, boutons vers les autres mystères | appliqué | `p-chapelet` : boutons « Mystères joyeux » et « Mystères douloureux » | — |
| 17/11 soir | Lint et nettoyage complet | appliqué | ESLint et Prettier (PLAN_GENERAL) ; `eslint .` : 0 erreur | 74 avertissements, surtout `require-each-key` |
| 17/11 soir | Bilan et audit de la mise à jour, avec corrections | appliqué | `docs/audits/*` | — |
| 17/11 soir | Reprendre ce qui a été mis en pause | appliqué | PLAN_GENERAL « Chantiers » ; REPRISE | — |
| 17/11 | Plan général, plugins et connecteurs, 4 à 8 agents | appliqué | `docs/PLAN_GENERAL.md` (rôles, outils, A11y Enforcer) | — |
| 17/11 | Gertrude : les prières avec promesse, sur les sujets choisis | appliqué | A_FOURNIR (19 nov.) | — |
| 17/11 | « L'écran Aujourd'hui est un poil long » | en cours | Lots 2 et 4 | Le 20 nov., l'écran mesure 5 332 px, soit 6,3 écrans |

## 4. Refonte du 18 novembre (SPEC § 11)

| Date | Demande | Statut | Preuve | Remarque |
|---|---|---|---|---|
| 18/11 | Un onglet à part pour les bréviaires (Sacré-Cœur, romain, Officium parvum) | appliqué / en cours (planifié) | Lecture › Office (`page-lecture.png`) | Bréviaire romain et Officium parvum « en préparation » : lots 8 et 9, pas encore commencés |
| 18/11 | Heures canoniales en boutons | en cours (planifié) | REFONTE § 4.3, lots 4, 8 et 9 | — |
| 18/11 | Abaisser les bandeaux sous l'encoche (grecque) | appliqué | Commit 01187e1 ; `safe-area-inset-top` dans `+layout.svelte:92-98` | Impossible à voir sans encoche dans l'émulateur |
| 18/11 | Un bandeau pour la direction latine | appliqué | Rinceau de vigne (`planche1.jpg`) | — |
| 18/11 | Ornements autour de l'arche du saint | appliqué | Les deux directions (`jour-grecque-2026-11-18.png`) | — |
| 18/11 | Jauges et jardin du jour derrière un bouton | en cours | Lot 2 (branche a4e9c58, be46302) | Sur `main`, les jauges restent visibles |
| 18/11 | Doublons de la liste (ex. mercredi : pureté et Gloria en double) | en cours | Lot 3 : `unicite.test.ts` passe sur l'année ; branchement au lot 4 | **L'exemple n'est pas encore corrigé dans l'app** : voir le détail sous ce tableau |
| 18/11 | Redondances entre méditation du jour et dévotion du mois | en cours | Programme : contrôle d'inclusion (REFONTE § 2.10) | — |
| 18/11 | Mercredi : une page (renouvellement et Gloria) ; autres jours : une page de Gloria | en cours | `prog:devotion-mercredi`, `prog:cordon-gloria` | Sur `main`, le mercredi a encore deux lignes « Cordon… » et une « Dévotion du mercredi » |
| 18/11 | Audit des fusions et intégrations | appliqué | `AUDIT_DEVOTIONS_2026-11-18.md` | — |
| 18/11 | Trois invocations en fin de dizaine | en cours (partiel) | `prog:fin-dizaine-o-marie` (Weber 1899) | « Ô mon Jésus, pardonnez-nous » et « Cœur immaculé de Marie » restent sans source. Elles figurent dans `programme.json` › `a_fournir`, mais **pas dans `A_FOURNIR.md`** |
| 18/11 | Scapulaire Jahenny sans ligne propre (réparti matin et soir) | en cours | `prog:scapulaire-jahenny` (insertions) | La ligne propre est toujours affichée |
| 18/11 | Les oraisons de sainte Brigitte tiennent lieu de méditation | appliqué | Aucune tâche de méditation en plus ; `prog:brigitte` | — |
| 18/11 | Pages explicatives hors de la liste | en cours (planifié) | Lot 7 (Dévotions en sections) | — |
| 18/11 | « Internal Error » de Profil vers Historique | corrigé | Lot 0 ; `+error.svelte` ; test Réglages → Historique avec coches, sans erreur | — |
| 18/11 | Prière de sainte Gertrude selon la catégorie du saint, avec son nom | appliqué | `/saint?date=2026-11-25` : « sainte Catherine d'Alexandrie » ; le 20/11 : confesseur | — |
| 18/11 | Somme théologique, un article par jour (Lachat) | en cours (planifié) | Lecture › Doctrine « en préparation » ; lot 10 | — |
| 18/11 | Onglet Lecture (doctrine, spirituel, Écriture, bréviaires) | appliqué | Lot 1 (2916e24) | La ligne récapitulative « Lectures du jour » est en cours (lots 4 et 5). La méditation, la roue et l'office du saint sont encore dans la liste |
| 18/11 | Profil en haut à droite | appliqué | Icône en haut à droite | Elle ouvre `/reglages`, et `/profil` reste à part : REFONTE § 4.1 voulait une seule page |
| 18/11 | Jaculatoire différente à chaque ouverture, plus de tâche | en cours | Lot 2 (be46302) | Elle n'est encore ni sur l'accueil ni sur l'écran du jour |
| 18/11 | Filtres par thème et par type | en cours (planifié) | Lot 7 | Prières : 86 écrans ; parties qui se recouvrent (« Couronnes et chapelets », « Chapelet et Rosaire », « Rosaire » ; « Sainte Vierge », « Prières à la Sainte Vierge ») |
| 18/11 | Agents spécialisés 1, 2 et 3 | appliqué | `AUDIT_DEVOTIONS`, `AUDIT_CORPUS`, `ergonomie-2026-11-18.md` | — |
| 18/11 | Boucle de vérification (lint, tests, revue) | appliqué | ESLint : 0 erreur ; vitest : 131/131 | — |
| 18/11 | Questions interactives, puis la fiche de conception | appliqué | Questions de 09:54 et 09:56 ; SPEC § 11 | — |
| 18/11 | Refondre sans préserver l'architecture | en cours | Programme unique (lots 3 et 4) | — |
| 18/11 | Navigation : 5 onglets, bréviaires dans Lecture | appliqué | Barre : Aujourd'hui, Lecture, Prières, Dévotions, Calendrier | — |
| 18/11 | Lectures : une ligne récapitulative dans la liste | en cours | Lots 4 et 5 | — |
| 18/11 | Bréviaire romain complet, rubriques d'avant 1955 ; Officium parvum de Divinum Officium | en cours (planifié) | Lots 8 et 9 | — |
| 18/11 | Remplacer la liste en gardant les ajouts | en cours | Lot 4 (branche a4e9c58) | — |
| 18/11 | Installer graphify | appliqué | `/usr/local/bin/graphify`, `.graphifyignore`, PLAN_GENERAL § Outils | — |

**Doublons relevés dans l'app** (même prière ouverte deux fois dans la journée, `doublons-liens.txt`) : on en trouve
sur 12 des 13 jours testés. Tous viennent de la superposition entre la « Dévotion du jour », les litanies de la roue et
des lignes propres.

| Jour | Prières en double |
|---|---|
| Lundi | chapelet des Morts ; De profundis |
| Mardi | chapelet de saint Michel |
| Mercredi | prière pour la pureté ; litanies de saint Joseph |
| Vendredi | « Devant le Crucifix » ; litanies du Sacré-Cœur, ou de N.-D. des Sept Douleurs |
| Samedi | litanies de la sainte Vierge |
| Dimanche | litanies des Saints |
| 8 décembre | litanies de la sainte Face |

## 5. Indulgences, traductions et décisions des 19 et 20 novembre

| Date | Demande | Statut | Preuve | Remarque |
|---|---|---|---|---|
| 19/11 | Relancer les agents sans attendre de feu vert | appliqué | Commits du 19 et du 20 nov. | — |
| 19/11 | Seules comptent les œuvres de l'Enchiridion de 1952 | appliqué | SPEC § 11 ; `indulgences.json` vérifié (766e173, 6233ace) ; pages : « Ench. 1952, n° … » | — |
| 19/11 | Trouver les traductions approuvées (can. 934 § 2) | en cours | A_FOURNIR, tableau ; e652a2c (Beringer 1925, *Ami du clergé* 1931) | Agent « traductions » |
| 20/11 | Latin en premier sans traduction approuvée | en cours (non fusionné) | 0a33f5b sur `claude/magical-franklin-3m4y2s` | Sur `main`, l'Angélus s'ouvre encore en français (`p-angelus`) |
| 20/11 | Chercher soi-même un recueil approuvé | en cours | e652a2c | — |
| 20/11 | Gertrude : toutes les prières, hors de la liste | en cours (non fusionné) | 13866b2, ea18b12 | — |
| 20/11 | Sainte Face, IVe station : garder « ces » | appliqué | A_FOURNIR | — |
| 20/11 | Envoyer `A_FOURNIR.md` et poser les questions en parallèle | appliqué | Questions de 08:25 | — |
| 20/11 | Lancer l'agent d'audit des consignes | appliqué | Ce document | — |
| 20/11 | Lot « Dimensions » (`docs/conception/LOT_DIMENSIONS.md`), après le lot 4 | en cours | 8a0c2fb, 2b81473 (branche non fusionnée) | À lancer quand le lot 4 sera fusionné |
| 20/11 | Beringer 1925 vaut traduction approuvée, sauf les hymnes en vers | en cours | 32caae6 (SPEC, non fusionné) | — |
| 20/11 | Pater, Ave et Gloria usuels indulgenciés ; le chapelet en français compte | en cours | 32caae6 | — |

## 6. Décisions antérieures et règles permanentes

| Règle ou décision | Statut | Preuve | Remarque |
|---|---|---|---|
| Aucun texte de mémoire ; chaque pièce a sa source | appliqué (avec réserves) | Champ `source` de chaque pièce | Exceptions déclarées : formule du cordon composée à la demande ; actes du livret « composés pour le livret ». **29 pièces du livret n'ont pas de ligne « source »** (A_FOURNIR) |
| Sites bannis (Hozana, Aleteia, Notre-Dame de Chrétienté) | appliqué | Aucune occurrence dans `data/`, `app/`, `engine/` ni `docs/`, hors de l'énoncé de la règle (REPRISE:9, PLAN_GENERAL:14) | — |
| Pas d'OCR brut quand une transcription propre existe | appliqué | Guéranger : le texte propre passe d'abord, l'OCR n'est jamais appliqué dessus | Hamon s'affiche avec « texte reconnu par OCR, coquilles possibles » |
| Tout reste modifiable dans l'app | appliqué / **oublié** pour les recueils | Prières, liste, pratiques et fêtes ont leurs éditeurs | **Éditeur de recueils** (SPEC § 9 : ajouter, découper, affecter) **absent** : `/recueils` est en lecture seule, et aucun lot ne le prévoit. Le programme (lot 4) devra rester modifiable (`/programme`) |
| Aucun secret dans le dépôt | appliqué | Seule la clé VAPID publique (`config.ts:10`) ; service role lue par `Deno.env` | — |
| Indulgences : Enchiridion de 1952 seul, can. 934 § 2 | appliqué / en cours | Note du can. 934 sur les pages ; latin en premier non fusionné | — |
| Une PR fusionnée après chaque lot | appliqué | PR n° 34 à 37 (lots 0, 1 et 3) | Branche `claude/magical-franklin-3m4y2s` en avance sur `main` (latin en premier, décisions Beringer et Pater, Gertrude, Guéranger, Dimensions) : à fusionner |
| Synchronisation entre téléphone et PC (CONSIGNE § 2) | appliqué (code) | `app/src/lib/sync.ts` | Pas éprouvée ici |
| « Ave Maria de la mort » retiré ; propre de France ; modèle d'e-mail Supabase | abandonné | A_FOURNIR n° 1 et 7 ; REPRISE pt 5 | Décisions écrites |

## À traiter

Par ordre de priorité.

**1. Contredit**
- **Rosaire, clausules de Montfort en latin et en français.** Seules les deux formules françaises de Montfort sont en
  place (offrande et « Grâce du mystère »), sans latin. Deux issues :
  - trouver une édition latine ancienne des formules ;
  - ou faire décider l'utilisateur et l'écrire dans la SPEC § 10.3.

**2. Oublié**
- **Éditeur de recueils** (SPEC § 9 ; PLAN_ETAPES, étape 9) : `/recueils` ne permet ni ajout, ni découpage, ni
  affectation. Aucun lot ne le couvre.
- **Fin de dizaine** : les deux invocations sans source (« Ô mon Jésus, pardonnez-nous », « Cœur immaculé de Marie »)
  manquent dans `A_FOURNIR.md`. Elles ne sont notées que dans `programme.json`.

**3. Exemples dont le principe n'est pas généralisé**
- **Notes de bas de page** : réglées pour Chaignon (en fin de méditation). Hamon garde environ 141 notes au milieu des
  phrases et 21 en-têtes courants « Bl. H. – T. I. ». Exemple : 12 janvier, « avec la * Vos estis corpus Christi…
  (1 Cor., 117, 27.) vigne ».
- **Fautes des méditations** : il reste des coquilles dans Hamon (« 1 Cor., 117, 27 », « en semble », « c'est-à -
  dire »).
- **« Terminée sans être commencée »** : le cas est corrigé pour les dévotions passées. Une série entamée en septembre
  sans aucune coche (« Douze samedis… 0/12 ») s'affiche pourtant « En cours ».
- **Martyrologe chanté** :
  - le français et le latin ne nomment pas les mêmes saints (18/11 : « Saint Pierre » / « Sancti Petre et Paule ») ;
  - un nom est mal découpé (20/11 : « Sancti Octávi, Solutor, Adventor et Thebána »).

  Il faut un contrôle sur toute l'année.
- **Prières : parties qui se recouvrent** :
  - « Couronnes et chapelets », « Chapelet et Rosaire » et « Rosaire » ;
  - « Sainte Vierge », « Prières à la Sainte Vierge » et « Antiennes… ».

  C'est le même problème de doublons que dans la liste, côté bibliothèque. À prendre avec le lot 7.

**4. En cours : à surveiller à la fusion**
- **Doublons de la liste** : l'exemple du mercredi n'est toujours pas corrigé dans l'app. Douze jours sur treize ont des
  doublons (§ 4). Il faut vérifier, après le lot 4, que `unicite.test.ts` et l'écran réel s'accordent.
- **Lot 2** : jauges repliées, jaculatoire d'ouverture, martyrologe replié, seuils en français, étiquettes ORD./PIA
  retirées.
- **Lot 4** : Jahenny, agonisants et Flèche d'or sans ligne propre ; une page par jour pour le cordon ; ligne « Lectures
  du jour ».
- **À fusionner** : la branche `claude/magical-franklin-3m4y2s` (latin en premier, décisions sur Beringer et sur le
  Pater, Gertrude hors liste, Guéranger, lot Dimensions).
- **Profil** : réunir `/profil` et `/reglages` derrière l'icône, comme le prévoit REFONTE § 4.1.
- **Planifiés, pas encore commencés** :
  - lot 5 : ligne récapitulative « Lectures du jour » ;
  - lot 7 : filtres et Dévotions ;
  - lot 8 : Officium parvum ;
  - lot 9 : Bréviaire romain ;
  - lot 10 : Somme ;
  - lot Dimensions.
- **Temps liturgique** : chemin de croix et Miserere en Carême, Adoro te à la Fête-Dieu, Ad te beate Ioseph en
  octobre. Ils sont absents le 5 mars 2027 et en attente de textes sourcés.
- **Sources** : 29 pièces du livret sans ligne « source ».

## Chiffres

Les tableaux comptent 111 lignes. Une ligne à double statut est comptée « en cours » quand une partie reste à faire. La
ligne « tout reste modifiable » est comptée « oublié », pour l'éditeur de recueils.

| Statut | Nombre |
|---|---|
| appliqué | 69 |
| corrigé | 8 |
| abandonné | 2 |
| en cours | 30, dont 6 planifiés et non commencés |
| oublié | 1 |
| contredit | 1 |

Le statut « en cours » couvre aussi des travaux faits sur des branches non fusionnées : latin en premier, Gertrude, lot
Dimensions, décisions sur Beringer et sur le Pater, Guéranger.

Restent hors des tableaux :
- une omission dans `A_FOURNIR.md` : les deux invocations de fin de dizaine ;
- 6 exemples dont le principe n'est pas généralisé :
  - notes de Hamon ;
  - coquilles de Hamon ;
  - série « en cours » jamais commencée ;
  - martyrologe ;
  - parties de Prières qui se recouvrent ;
  - doublons de la liste, en cours.
