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
     - Confrérie de Saint-Joseph, reste : prières des trois jours avant chaque fête (Fiançailles, 19 mars,
       Patronage, p. 69-75), neuvaine pour une grâce particulière (p. 117), mois de saint Joseph (p. 89) ;
     - neuvaine de saint François-Xavier (Québec 1880, `cihm_62891`, approuvée 15 déc. 1879) : prières de tous les
       jours faites et intégrées (13-21 févr. 2027) ; restent les considérations de chaque jour (p. 29-129) et les
       litanies (p. 48 s.) ;
     - neuvaine du Saint-Esprit de S. Alphonse (*Œuvres*, 1876, t. XIV, p. 373-391, `07430208.1657.emory.edu`) ;
     - Précieux Sang 1890 : les sept vendredis du Carême, les six vendredis avant le Sacré-Cœur et la prière
       « pendant trente jours » (p. 606, microfiche abîmée : chercher un autre exemplaire) ;
     - l'union de prières de Picard 1873 : premier samedi, huit jours pour un associé défunt.
   - À chercher (Beringer ne donne que la concession) :
     - sainte Anne, saint Raphaël, l'Ange gardien, la Fête-Dieu, les âmes du purgatoire.
   - Immaculée Conception, Noël, Sacré-Cœur, Assomption, Nativité : déjà au plan avec leur texte ; Pentecôte : Veni
     Creator seulement (S. Alphonse ci-dessus).
   - Sept dimanches de saint Camille : aucune date dans les sources, donc non intégrés.
2. **Lot A, reste.**
   - Précieux Sang 1890, faute d'un meilleur exemplaire : les litanies de Jésus agonisant, l'amende honorable
     des adorateurs, les messes et l'office.
   - Les indulgences imprimées à vérifier dans l'Enchiridion de 1952 : amende honorable (300 j.), offrande de
     Léon XII, les deux chapelets.
3. **Prières obligatoires, reste.** Les 24 éléments sans titre ni remplaçant sont listés dans l'audit et dans
   `A_FOURNIR.md`. Quand un manuel en fournit un, le proposer à l'utilisateur.
4. **Psautier de Fillion** (Bréviaire en français) : jeudi, vendredi, samedi et cantiques de Laudes. Le travail
   déjà fait est dans `main` ; voir `SOURCES_UTILISEES.md` et l'audit `BREVIAIRE_FRANCAIS_2026-11-22.md`.
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
