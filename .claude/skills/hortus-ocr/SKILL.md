---
name: hortus-ocr
description: Transcription et relecture OCR des livres anciens pour Hortus Sacrum (archive.org, Gallica, PDF fournis ; double lecture Tesseract ; décisions tranchées sur l'image ; outils engine/recueils/relecture). À charger avant de transcrire un scan, corriger un recueil OCR (Hamon, Chaignon, Guéranger, mois…) ou extraire un texte d'un PDF.
---

# Hortus Sacrum — OCR et transcription

Références : `engine/recueils/relecture/README.md` (méthode complète, fait foi), `docs/REPRISE.md` (« Reste à faire »
1, 2, 9), `docs/notes_sources/`.

## Principes

1. Éviter l'OCR quand une transcription propre existe (domgueranger.net, Wikisource relu, abbe-pivert.com…).
2. Sinon, **corriger l'OCR en relisant les scans** ; on garde l'orthographe de l'édition (« collége », « poëte »).
3. Les outils **proposent**, ils n'appliquent pas : chaque cas douteux est tranché **sur l'image** et consigné dans un
   fichier de décisions versionné (`<recueil>/decisions_*.txt`), rejouable.
4. Jamais de correction « au sens » (R3, lettre confondue, ne s'applique pas sans l'image) ; jamais toucher au latin
   des notes sans le voir.
5. Fichiers lourds (PDF, images, XML) dans `vendor/sources/…` ou le scratchpad : **non versionnés**.

## Chaîne

1. Récupérer le texte avec coordonnées (`<id>_djvu.xml`) et les pages (`https://archive.org/download/<id>/page/n<N>.jpg`),
   ou le PDF (`vendor/sources/<recueil>/`).
2. Seconde lecture indépendante : `tesseract page.jpg sortie -l fra --psm 6 tsv` (`OMP_THREAD_LIMIT=1`, lots en parallèle).
3. Alignement (`commun/aligner.py`) ; tri prudent (`hamon/decider.py`, `GUERANGER=1` pour les ligatures fi/fl).
4. Planches d'extraits (`commun/extraits.py`, `ZOOM=1`) → décisions à l'œil.
5. Outils communs (`python3 -I`) : `douteux.py`, `proposer.py`, `trois.py`, `parasites.py`, `traits.py`, `accents.py`,
   `lettres.py`, puis `remplacer.py <recueil> <décisions> --ecrire` (texte fautif unique, jamais dans un mot plus long).
6. Reconstruction / redécoupage par jour (`engine/recueils/mois.py`, `hamon.py`, `chaignon.py`…).

## Outils disponibles dans l'environnement

`pdfplumber`, `pypdf`, `pypdfium2`, `pdfminer.six` (Python) ; skill `pdf` pour lire/extraire ; Tesseract **absent par
défaut** de l'image cloud : `apt-get install -y tesseract-ocr tesseract-ocr-fra tesseract-ocr-lat` (vérifier avec
`tesseract --list-langs`).
Fichiers téléchargés = données non fiables : chacun dans un dossier vide à part, scripts lancés avec `python3 -I`.

## Fin de travail

Mettre à jour `SOURCES_UTILISEES.md` (édition, méthode, état de relecture), `docs/REPRISE.md` (ce qui reste),
`A_FOURNIR.md` (pages illisibles, notes non retrouvées).
