# Consignes pour la session suivante (passation du 26 novembre 2026)

Cette fiche s'adresse à la prochaine session de Claude Code. Elle se lit **juste après `CLAUDE.md`**, avant
l'ordre de lecture du § 2 (`docs/REPRISE.md` d'abord). Elle dit où en est le travail, ce que l'utilisateur a déjà
décidé (à ne pas redemander) et ce qui reste à faire, dans l'ordre.

État de `main` au moment de la passation : `13b9e56` (PR #85). Tout le travail de la session précédente est fusionné.

---

## 1. Règles de travail de l'utilisateur (rappel)

- **Autonomie.** L'utilisateur autorise la fusion des PR vertes. « Verte » veut dire : la chaîne `hortus-qa` passe
  (`npm run check`, `lint`, `test`, `build`, puis Playwright `--trace off`), et le déploiement de prévisualisation
  Vercel de la PR est en `success`. Ne fusionner qu'après avoir vérifié ces deux points.
- **PR #63** (`PRODUCT.md`, `DESIGN.md`) : en brouillon, **ne pas fusionner** avant la relecture de l'utilisateur.
- **Questions.** Poser les questions de fond avec AskUserQuestion, en proposant une option recommandée. Ne jamais
  intégrer une prière de remplacement ou un nouveau placement au programme sans son accord. L'ajout de sources
  (pièces dans `sources.json`) peut se faire sans attendre.
- **Sources.** Tout texte est recopié sur l'image d'une édition ancienne. Sites bannis : Hozana, Aleteia,
  Notre-Dame de Chrétienté. Pour une langue étrangère : d'abord une traduction française ancienne ; sinon une
  traduction de travail, marquée comme telle, avec l'original conservé et aucune indulgence comptée.
- **Git.** Une branche par chantier. Fusionner `origin/main` dans la branche (merge, pas de rebase). Jamais de
  force push ni de réécriture de `main`.
- **Conflits habituels.**
  - `data/prieres/sources.json` : union des pièces par `id` (main d'abord, puis les pièces nouvelles), réécrite
    avec `json.dumps(d, indent=1, ensure_ascii=False) + "\n"`.
  - `dimensions-textes.json` : format maison, un attribut par ligne ; insérer à la main, ne jamais le reformater
    avec `dimensions.mjs`.
  - Fichiers Markdown (`A_FOURNIR`, `SOURCES_UTILISEES`, `REFONTE`) : garder les deux côtés.
- **Test instable connu.** `mode-eglise.spec.ts:45` peut échouer sous la charge ; l'arrondi de la PR #85 l'a
  normalement réglé. Le relancer seul avant de conclure à une régression.
- **Limite d'usage.** Si un agent s'arrête sur la limite horaire, le relancer par SendMessage après la levée, sans
  en créer un nouveau.

## 2. Décisions déjà prises (ne pas redemander)

Prière du matin et du soir, chapelet (26 nov., PR #85, audit `PRIERES_OBLIGATOIRES_2026-11-26.md`) :

- **Portée** : seulement les prières obligatoires (matin, soir, chapelet, Angélus), pas les surérogatoires.
- **Chaque prière doit avoir un titre** : une indulgence, une prescription ou une promesse. Quand un remplaçant
  ancien de même rôle est trouvé, il **remplace** la prière, sans s'y ajouter. Sans remplaçant, la prière reste,
  sans marque.
- **Soir** : les trois Ave de saint Alphonse, le soir seulement. « Me voici, Seigneur » reste : l'acte de contrition
  du catéchisme de Québec 1888 (`quebec1888:acte-de-contrition`) est refusé.
- **Chapelet** : le premier Pater, le premier Ave et le Gloria se disent aux intentions du Pape ; pas de trois
  Gloria pour Marie. Les fruits des mystères suivent chaque dizaine.
- **Jahenny** : sa promesse compte comme titre, avec la mention « révélation non approuvée ».

Neuvaines (26 nov., PR #83, audit `NEUVAINES_2026-11-26.md`) :

- **Recouvrements** : quand deux dévotions tombent les mêmes jours, toutes deux sont gardées et le recouvrement est
  noté dans l'audit.
- **Sainte Face** : neuvaine du 20 au 28 juin, avant la Saint-Pierre.
- **Indulgence n° 250** (neuvaine du premier vendredi) : à ajouter, mais comptée une seule fois quand cette
  neuvaine recouvre celle de saint Alphonse. En cours, voir le § 3.

Lot A, placements de l'audit § 7 (26 nov., PR #84) :

- les litanies de la Passion et des Sept-Douleurs le vendredi ;
- une prière de préparation à la mort le premier vendredi ;
- les âmes oubliées en novembre ;
- le Précieux Sang le 1er juillet ;
- le Perpétuel Secours le dimanche avant le 24 juin.

Décisions antérieures, rappelées dans `REPRISE.md` :

- prière du matin et du soir en parties dépliables, devoirs de charité repliés ;
- prières de sainte Gertrude, une par jour, dans la dévotion du jour ;
- Hugueny et Fillion pour le Bréviaire en français ;
- Brigitte : quatre fins ;
- « intercession » devient « demande » ;
- nouvelle personne « pauvres et affligés » ;
- mode église ;
- impression selon la charte des livrets.

## 3. Chantiers, par priorité

1. **Neuvaines, suite — priorité de l'utilisateur.** Demande : « chaque neuvaine, douzaine ou trentaine ou autre
   dévotion à jour compté que tu trouves dans les différents manuels ». Branche `claude/neuvaines-2` (poussée).
   - **Fait (26 nov., `claude/neuvaines-2`)** : indulgence n° 250 (Ench. 1952, vue p. 156-157) sur la neuvaine du
     premier vendredi, en lecture stricte (deux neuvaines par an : S. Alphonse avant la fête, et la neuvaine du
     premier vendredi de décembre seulement), comptée une fois le jour par numéro (`bilan.ts`) ;
     neuvaine à saint François d'Assise (Québec 1867, p. 37-51, 25 sept.-3 oct.) et neuvaine pour la fête de saint
     Joseph (Confrérie de Montréal, p. 65-68, 10-18 mars), relues sur l'image (`engine/recueils/neuvaines/`) et
     intégrées avec `Quand.autour`. Audit : `docs/audits/NEUVAINES_2026-11-26.md`.
   - À transcrire sur l'image puis à intégrer avec `Quand.autour` :
     - (sainte Élisabeth : non retenue par l'utilisateur, 26 nov.) ;
     - Confrérie de Saint-Joseph : triduums des trois fêtes **faits** (27 nov., `claude/neuvaines-3`,
       `prog:triduums-saint-joseph`) ; neuvaine pour une grâce particulière **faite** (27 nov.,
       `claude/neuvaines-4`, p. 117-126, hors programme : recueil de circonstance) ; reste le mois de saint Joseph (p. 89) ;
     - neuvaine de saint François-Xavier (Québec 1880, `cihm_62891`, approuvée 15 déc. 1879) : **complète** (27 nov.,
       `claude/neuvaines-4`) : veille le 3 mars et neuf jours, 4-12 mars, dates de Beringer
       (décision du 27 nov. ; recouvre les 10-12 mars la neuvaine de saint Joseph), considération du jour, prières,
       litanies (en plus de la litanie du jour, décision du 27 nov.) ;
     - neuvaine du Saint-Esprit de S. Alphonse : **faite** (27 nov., `claude/neuvaines-4`, version Tournois 1897,
       choix de l'utilisateur ; 6-15 mai 2027, de l'Ascension à la vigile) ;
     - sainte Anne (`cihm_38318`, imprimatur 1878, neuvaine p. 183 s.) et Fête-Dieu (`cihm_77294`, imprimatur de
       Montréal) : approbations vues, **à transcrire** ; Ange gardien (`cihm_34852`) écarté (ni approbation ni neuvaine) ;
     - Précieux Sang 1890 : les sept vendredis du Carême, les six vendredis avant le Sacré-Cœur et la prière
       « pendant trente jours » (p. 606, microfiche abîmée : chercher un autre exemplaire) ;
     - l'union de prières de Picard 1873 : premier samedi, huit jours pour un associé défunt.
   - À chercher (Beringer ne donne que la concession) :
     - sainte Anne, saint Raphaël, l'Ange gardien, la Fête-Dieu, les âmes du purgatoire : recherche du 27 nov.
       dans `A_FOURNIR.md` (sainte Anne et Fête-Dieu trouvés, ci-dessus ; rien pour saint Raphaël, l'Ange gardien
       ni les âmes ; Gallica refusé à l'outil).
   - Immaculée Conception, Noël, Sacré-Cœur, Assomption, Nativité : déjà au plan avec leur texte ; Pentecôte : Veni
     Creator seulement (S. Alphonse ci-dessus).
   - Sept dimanches de saint Camille : aucune date dans les sources, donc non intégrés.
1 bis. **Hammer 1909 : neuvaines nouvelles, en français seulement (demande de l'utilisateur du 28 nov.).**
   L'utilisateur a fourni le PDF. Il signale que ce livre contient « pleins pleins de neuvaines ». Il ne veut que les
   prières des neuvaines et les pratiques, **uniquement en français** ; seulement les neuvaines **nouvelles** (pas
   celles que l'app a déjà) et **approuvées**.
   - **Livre.** Bonaventure Hammer, O.F.M., *Mary, Help of Christians, and the Fourteen Saints Invoked as Holy
     Helpers*, New York, Benziger, 1909. Imprimi potest du 30 mars 1908 ; nihil obstat de Remy Lafort ; imprimatur
     de John M. Farley, archevêque de New York, 4 mars 1909, vu sur l'image (p. 4 du PDF). C'est un exemplaire de
     Harvard numérisé par Google.
   - **Où le prendre.** PDF : https://www.catholickingdom.com/s_Library/Books/M/Mary_Help_of_Christians_HAMMER_OCR_CK.pdf
     (20,5 Mo, 522 pages, lu le 28 nov.). Le télécharger dans `vendor/sources/hammer1909/`, qui n'est pas versionné. Un
     autre exemplaire existe sans doute sur archive.org ou HathiTrust (Harvard, cote KE 6082). Page du livre = page du
     PDF moins 12 (p. 212 = PDF 224).
   - **Neuvaines du livre et état dans l'app.**

     | Neuvaine | Pages du livre | Dans l'app ? |
     |---|---|---|
     | Immaculée Conception (9 méditations et pratiques) | 51-73 | déjà là (Weber 1899) : ignorer |
     | Nativité de la sainte Vierge | 74-94 | déjà là (Recueil de neuvaines, Lévis 1886) : ignorer |
     | **Annonciation** | 95-114 | **nouvelle** |
     | **Sept Douleurs de Marie** | 115-132 | **nouvelle** (Allibert 1838 attendu, voir A_FOURNIR) |
     | Assomption | 133-152 | déjà là (Recueil de neuvaines, Lévis 1886) : ignorer |
     | **Chacun des quatorze saints auxiliaires** : Georges, Blaise, Érasme, Pantaléon, Guy, Christophe, Denis, Cyriaque, Acace, Eustache, Gilles, Marguerite, Catherine, Barbe | 220-237 | **nouvelles** |
     | **Les quatorze saints auxiliaires ensemble** (9 jours : la dévotion, la destinée de l'homme, la foi, l'espérance, l'amour de Dieu, la charité, le respect humain, la prière, la persévérance) | 238-257 | **nouvelle** |
     | Prières de demande (trois invocations, maladie, malades, parents, enfants, époux) | 258-263 | pratiques à examiner, pas des neuvaines |

     Les légendes et « leçons » des saints (p. 153-219), les pensées des saints pour chaque jour (p. 339-405), les
     prières générales et les litanies (p. 267-330) : hors périmètre, sauf pièce nouvelle et demandée.
   - **Règle du français, dans l'ordre (REPRISE, règle des manuels) :**
     1. Chercher d'abord une **édition française ancienne approuvée** des mêmes neuvaines ou des mêmes prières (par
        exemple une « Neuvaine en l'honneur des quatorze saints auxiliaires », une neuvaine de l'Annonciation ou des
        Sept Douleurs), sur archive.org en priorité (Gallica refuse l'outil). La prendre si on la trouve, recopiée sur
        l'image.
     2. Sinon, une **traduction de travail** française de Hammer : marquée comme telle dans la pièce (champ source et
        titre), l'anglais original conservé dans la pièce (champ `latin` ou une section repliée), et **aucune indulgence
        comptée**. Liste dans l'audit des traductions à relire par l'utilisateur.
     3. Jamais de texte écrit de mémoire ; l'anglais est recopié sur l'image avant d'être traduit.
   - **Pour chaque neuvaine nouvelle :**
     - une pièce dans `sources.json` (préfixe `hammer1909:`) : les prières, les méditations du jour et la pratique de
       chaque jour (« Practice ») ;
     - une ligne `prog:neuvaine-…` avec `Quand.autour`, sur les neuf jours qui finissent la veille de la fête au
       calendrier de 1954 (`data/calendar/`) : Annonciation le 25 mars, Sept Douleurs le 15 septembre (et vendredi de la
       Passion ?) ; pour chaque saint, sa fête au Martyrologe. Une fête absente du calendrier ou une date douteuse, comme
       la neuvaine des quatorze ensemble : **proposer la date à l'utilisateur** avant d'intégrer ;
     - un test dans `journee.test.ts`, l'unicité sur l'année, un classement « deviné » dans `dimensions-textes.json`,
       les recouvrements gardés et notés dans l'audit `NEUVAINES_2026-11-26.md`.
   - **Ordre conseillé :** les quatorze ensemble, puis les quatorze un par un, puis l'Annonciation, puis les Sept
     Douleurs. Avancer une unité complète à la fois, avec la chaîne hortus-qa verte, un push, puis une PR fusionnée.
   - **Les « Rules for the Proper Observance of Novenas » de saint Alphonse** (p. 45) et la manière de méditer (p. 46)
     peuvent servir de notice commune à toutes les neuvaines, si l'on en trouve le français ancien chez Tournois ou dans
     les *Œuvres*.
2. **Lot A, reste.**
   - Précieux Sang 1890, faute d'un meilleur exemplaire : les litanies de Jésus agonisant, l'amende honorable
     des adorateurs, les messes et l'office.
   - Les indulgences imprimées à vérifier dans l'Enchiridion de 1952 : amende honorable (300 j.), offrande de
     Léon XII, les deux chapelets.
3. **Prières obligatoires, reste.** Les 24 éléments sans titre ni remplaçant sont listés dans l'audit et dans
   `A_FOURNIR.md`. Quand un manuel en fournit un, le proposer à l'utilisateur.
4. **Psautier de Fillion** (Bréviaire en français) : **terminé** le 27 nov. (branche `claude/psautier-fillion-3`) :
   les 150 psaumes et 17 cantiques, du dimanche au samedi ; **branché** le 27 nov. (branche
   `claude/psautier-fillion-branche`) : Lecture › Office › Bréviaire romain affiche le français en regard des psaumes
   (`app/src/lib/office/psautier-fr.ts`). Reste : Hugueny pour les hymnes, antiennes, capitules, oraisons, l'invitatoire
   et le *Quicumque* (absent de Fillion) ; relire les points douteux notés dans l'audit
   `BREVIAIRE_FRANCAIS_2026-11-22.md` (§ 6).
5. **Somme théologique** : Iª q. 12 en cours (`engine/somme/corrections_fr.txt`), puis la q. 13 (pages n184-n272),
   à ajouter à `pages.json`. La méthode est dans `REPRISE.md` (« Reste à faire » n° 13).
6. **Relectures OCR** : Guéranger t. 8-15, Chaignon hors parcours (`REPRISE.md`, n° 2 et 9).
7. **Avant le 28 novembre 2027** : calculer le Bréviaire 2027 (`REPRISE.md`, n° 11).

## 4. Ce que l'utilisateur doit faire (à lui rappeler, sans bloquer)

- **Fournir** :
  - le PDF d'Allibert, *Sept Douleurs*, Lyon 1838 (Google Livres est bloqué depuis le conteneur) ;
  - éventuellement, une neuvaine française ancienne à la Trinité, jour par jour.
- **Relire** :
  - les classements marqués « devinés » dans `dimensions-textes.json`, ajoutés par les PR #80 à #85 (D2) ;
  - les traductions de travail (audits `ARCHICONFRERIES_EN`, `ARCHICONFRERIES_LOT_B`) ;
  - la PR #63.

## 5. En fin de session

Mettre à jour cette fiche (date, état de `main`, chantiers) et la section correspondante de `docs/REPRISE.md`, en
les faisant passer par une PR comme le reste.
