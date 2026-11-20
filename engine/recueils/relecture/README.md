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
