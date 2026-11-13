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
