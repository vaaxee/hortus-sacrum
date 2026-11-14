#!/bin/bash
# Chaignon : toute la relecture, de l'OCR d'archive.org au texte de l'app.
# Usage : chaine.sh <texte d'origine> <dossier archive.org (pagesNN.json, correctionsNN.json, decNN.txt)> <sortie>
set -e
H=$(dirname "$0"); R=$H/../hamon
cp "$1" "$3"
python3 -I $H/decouper_t2.py fusion "$3"
python3 -I $H/pages_manuelles.py "$2/pages02.json" "$3" --ecrire
python3 -I $H/decouper_t2.py couper "$3"
python3 -I $H/notes.py "$2" "$3" --ecrire
for v in 01 02 03; do python3 -I $R/appliquer.py "$2" $v "$3" --ecrire; done
python3 -I $H/ponctuel.py "$3"
python3 -I $H/appels.py "$3" --ecrire | head -1
