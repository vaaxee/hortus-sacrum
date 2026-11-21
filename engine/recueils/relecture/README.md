# Relecture d'un recueil OCR sur les scans

Méthode suivie pour Berlioux, *Mois des âmes du purgatoire* (novembre), à reprendre pour Hamon, Chaignon et les autres mois.

1. Télécharger le texte d'archive.org avec ses coordonnées (`<id>_djvu.xml`) et les images des pages
   (`https://archive.org/download/<id>/page/n<N>.jpg`).
2. Refaire une seconde lecture indépendante : `tesseract page.jpg sortie -l fra --psm 6 tsv`.
3. `align.py` : aligner les deux lectures mot à mot (difflib). Accord → mot gardé. Désaccord où une seule
   lecture donne des mots du dictionnaire (pyspellchecker `fr`, plus les mots sur lesquels les deux lectures
   s'accordent ailleurs) → celle-là. Le reste est signalé (`flags.json`).
4. `sheets.py` : planches de 14 extraits du scan, chacun avec les deux lectures ; chaque désaccord est tranché à
   l'œil et noté dans `dec.txt` (`numéro<TAB>texte`, `A`/`B` = l'une des lectures ; sans ligne = lecture A).
   Une page trop abîmée est recopiée à la main dans `over/<page>.txt`.
5. `apply.py` : reconstruit le texte (alinéas d'après les `<PARAGRAPH>` du XML) et le redécoupe par jour avec
   `engine/recueils/mois.py`.
6. `post.py` : règles sûres (traits d'union perdus en fin de ligne, « -t-il », mots collés, « F »/« T » lus pour
   « l' », « 2° », « PREMIER POINT » des lettrines).
7. `fixes.py` : corrections ponctuelles vérifiées sur l'image (coquilles restantes, intitulés, titres des jours).

Les scripts de `berlioux/` lisent et écrivent dans un dossier de travail (`B=` en tête de chaque script) ;
les images et les fichiers intermédiaires n'y sont pas versionnés.

## Seconde relecture (18-20 nov.) : outils communs

Tous dans `commun/`, à lancer avec `python3 -I`. Ils proposent, ils n'appliquent pas : chaque liste est relue, et les
cas douteux sont tranchés sur l'image avant d'entrer dans un fichier de décisions (`<recueil>/*_<date>.txt`).

- `douteux.py <recueil.json>` : mots inconnus (dictionnaire, Vulgate, mots fréquents de tous les recueils) et motifs
  suspects (« cæur », chiffres collés, « (c » pour « « », « 11 » pour « Il »…).
- `proposer.py` : R1 mots coupés (« néces sité »), R2 mots collés (« dansla »), R3 une lettre confondue. **R3 ne
  s'applique jamais sans l'image** : « entrenait », imprimé ainsi dans Hamon, serait devenu « entrerait ».
  `RELAX=1` donne aussi les cas dont un voisin est inconnu.
- `trois.py`, `parasites.py` : mots coupés en trois morceaux, ou avec un parasite entre les morceaux (« sain 1 teté »).
- `traits.py <recueil> [apostrophe]` : traits d'union et apostrophes perdus (« estelle », « quils »), seulement vers
  des formes attestées dans les recueils.
- `accents.py` : accents parasites (« éntendons ») ; ne touche jamais une graphie attestée (« collége », « poëte »).
- `lettres.py <recueil> l t` : une confusion répétée dans un livre (le Mois de saint Joseph lit « t » comme « l »).
- `extraits.py` (`ZOOM=1`) et `hamon/planches_cas.py` : planches d'extraits du scan pour trancher.
- `remplacer.py <recueil> <décisions> --ecrire` : applique une liste (« fautif<TAB>corrigé[<TAB>*] »), seulement si
  le texte fautif est unique (ou partout avec `*`), jamais à l'intérieur d'un mot plus long. Rejouable.

Pour un recueil d'OCR brut (mois de Lefebvre), on fait d'abord la seconde lecture Tesseract comme pour Hamon :
`PDF=<scan> hamon/prep.py 1 <p0> <p1> <dossier> <lot>`, puis `GUERANGER=1 hamon/decider.py` et `hamon/appliquer.py`.

## Hamon : notes de bas de page, appels, références (21 nov.)

Méthode de Chaignon (`chaignon/notes.py`, `appels.py`) adaptée aux PDF de Google Livres. Tout se rejoue par
`bash hamon/chaine_21nov.sh vendor/sources/hamon [journal]` (un second passage ne change plus rien) :

1. `hamon/notes.py` : coupe d'abord la table des matières et l'index restés dans la dernière méditation de chaque
   tome (25 mars, 10 août, 30 novembre). Puis, page par page, repère les notes dans la couche texte du PDF
   (`pdftotext -bbox-layout` : bas de page, corps plus petit, une note par ligne en retrait). Dans la méditation, le
   bloc des notes est entre la fin du texte de la page et le début de la page suivante (25 lettres de chaque côté) ;
   il part sous « ### Notes », découpé aux débuts des notes du PDF, avec le titre courant, le folio et la signature
   (« M. H. - T. I. », « Bl. H. – T. I. ») qui sont jetés, et la phrase est recollée (mot coupé ressoudé s'il est
   attesté). Ensuite, note par note, celles qui restent (recherche sur les lettres, tolérante, occurrence unique ; une
   note courte exige son appel). Enfin, une seconde passe sur le texte seul : citation latine précédée d'un appel et
   suivie de sa référence. Résultat : 1 046 notes rangées par saut de page, puis 60 par la seconde passe ; 351
   méditations ont leur section « Notes ». Une partie des notes du PDF manquaient déjà dans le texte (perdues à la
   première lecture) : elles ne sont pas recréées.
2. `hamon/appels.py` : retire les appels lus comme signes (« Jésus-Christ '; », « servir”. », « aplanis3 : »).
3. `hamon/references.py` : chapitres mal lus (« (1 Cor., 117, 27.) » → « (I Cor., xii, 27.) », vérifié sur le scan,
   t. I, p. 143) ; une lecture n'est retenue que si le verset de la Vulgate clémentine contient la citation (121
   corrigées). Les 46 autres sont listées dans le journal, à voir sur le scan.
4. `hamon/coupes_21nov.txt` (R1 de `commun/proposer.py`) et `hamon/espaces_21nov.txt` (`hamon/espaces.py`, relu) :
   mots coupés (« en semble », « mûre ment ») et traits d'union espacés (« c'est-à - dire », « Jésus- Christ »). Les
   coupes dont la forme séparée existe aussi en français (« de gré », « quel que », « bien heureux »…) sont écartées.
