# Méditations de l'Avent de saint Alphonse (28 novembre 2026)

Demande de l'utilisateur du 28 nov. (urgente, l'Avent commence le 29 nov. 2026) : une méditation de saint Alphonse de
Liguori par jour, du 1er dimanche de l'Avent jusqu'à Noël. Branche `claude/meditations-avent`.

## 1. Source retenue

Tournois, *Le divin Sauveur, méditations et neuvaines tirées de saint Alphonse de Liguori*, t. I, Paris, Douniol
(P. Téqui), 1897 ; imprimatur de Paris du 6 juillet 1897 ; archive.org `ledivinsauveurm01ligu`. C'est le livre de la
neuvaine de Noël déjà au plan (`liguori:neuvaine-de-noel`) et de la neuvaine au Saint-Esprit
(`liguori:neuvaine-saint-esprit`, t. II). L'introduction du P. Tournois (p. XII) dit que ses « Méditations sur
l'Incarnation sont la simple et fidèle traduction des Méditations de saint Alphonse pour le temps de l'Avent, de Noël et
de l'Épiphanie » et propose ce volume « du premier dimanche de l'Avent jusqu'à Pâques ». Les *Œuvres* (Vivès) n'ont
donc pas été nécessaires.

Plan du livre (table, p. 361-362) :

| Partie | Jours | Pages |
|---|---|---|
| Temps de l'Avent | 1er dimanche → 3e mercredi (18 méditations, une par jour du temporal) | 1-55 |
| Neuvaine de Noël | 1re-9e méditation, datées du 16 au 24 décembre | 56-83 |
| Noël et la suite | 25 décembre, 26 décembre… | 83 s. |

Chaque méditation : titre, verset latin et sa traduction, considération, puis « Affections et prières ».

## 2. Articulation avec la neuvaine de Noël (pas de doublon)

- La neuvaine de Noël du plan (`liguori:neuvaine-de-noel`, p. 56-83) ne contient que les **affections et prières** des
  neuf méditations (« après la méditation du jour (dans le livre) »). Les considérations de ces neuf jours ne sont pas
  livrées. Elles ne sont pas reprises dans la nouvelle pièce : elles appartiennent à la neuvaine (voir § 5).
- La nouvelle pièce `liguori:meditations-avent` ne prend que la partie « Temps de l'Avent » (p. 1-55), qui précède la
  neuvaine dans le livre ; aucun texte commun avec `liguori:neuvaine-de-noel`.
- La ligne `prog:meditations-avent` suit le temporal (`code_tempora` Adv1-0, Adv1-1…, comme le livre : « 1er
  Dimanche », « 1er Lundi »…) et s'arrête le 16 décembre (`sauf` : dates 12-16 à 12-24), où la neuvaine datée prend la
  suite. Selon la date de l'Avent, les dernières méditations du temporal tombent donc ou non : en 2026, Adv3-3
  (3e mercredi) est le 16 décembre, premier jour de la neuvaine ; la méditation du 3e mercredi n'est pas dite cette
  année-là. Quand l'Avent commence le 27 novembre, le 3e mercredi est le 14 décembre et le 15 n'a pas de méditation
  du temporal (le livre n'en donne pas).

## 3. Placement

Dans la journée (`moment: "journee"`, `ordre: 76`), comme la neuvaine au Saint-Esprit du même livre, une section par
jour (`extrait.section`) choisie par `code_tempora`. **Choix à confirmer par l'utilisateur** : la Lecture › Spirituel
garde sa « Méditation du jour » (Hamon, Chaignon) ; on aurait pu y proposer saint Alphonse en tête pendant l'Avent
(comme les livres des mois), mais cela demande du code dans `meditations.ts` et un recueil `data/recueils/` distinct,
alors que la demande vise une ligne `prog:` du programme.

Recouvrement (gardé, décision du 26 nov.) : du 29 novembre au 7 décembre, la neuvaine de l'Immaculée Conception court
les mêmes jours.

## 4. Transcription

Recopiée sur l'image des pages (archive.org, `page/n<N>.jpg`, page imprimée N = vue N + 31), à partir du texte OCR
d'archive.org, puis seconde lecture Tesseract (fra+lat) et alignement mot à mot (`difflib`) : tous les écarts relevés
sont des fautes d'OCR. Orthographe et ponctuation du livre gardées (« A » sans accent, « Eglise », « Eclairez ») ;
espaces de la ponctuation double à la française, comme pour la neuvaine au Saint-Esprit ; notes de bas de page en fin de
partie, avec leur page. Fautes d'impression gardées : « commis par nul homme » (1er samedi), « est dissolvat » (note,
1er vendredi). Lettre abîmée lue comme son mot : « auss: » → « aussi » (1er jeudi, p. 17) ; point parasite
« Convertimini·ad » → « Convertimini ad » (p. 3).

| Unité | Méditations | Pages | État |
|---|---|---|---|
| 1 | 1er dimanche → 1er samedi | 1-23 | relue sur l'image (28 nov.) |

## 5. Reste

- 2e dimanche → 3e mercredi (p. 23-55).
- Considérations des neuf méditations de la neuvaine de Noël (p. 56-83) : absentes de `liguori:neuvaine-de-noel`, qui
  n'a que les affections. À proposer à l'utilisateur (compléter la pièce avec `revision` + 1, ou une pièce à part).

## 6. Tests

`journee.test.ts` : « méditations de l'Avent de saint Alphonse » (une méditation par jour du temporal, dans l'ordre,
avec ses affections ; rien du 16 au 24 décembre). `unicite.test.ts` passe sur toute l'année 2026-2027.
