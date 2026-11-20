#!/bin/bash
# Guéranger : toutes les propositions des outils de commun/ pour un volume, sur ses seules entrées en OCR.
# Usage : proposer_vol.sh <NN> <dossier de travail>   →   <dossier>/propositions.txt (à relire, rien n'est appliqué)
set -eu
NN="$1"; T="$2"
[ -n "$NN" ] && [ -n "$T" ] || exit 1
H=$(cd "$(dirname "$0")" && pwd); C="$H/../commun"
python3 -I "$H/cible.py" "$NN" "$T"
{
  python3 -I "$C/proposer.py" "$T/cible.json"
  python3 -I "$C/traits.py" "$T/cible.json" "'" | sed 's/$/\t# T/'
  python3 -I "$C/parasites.py" "$T/cible.json" | sed 's/$/\t# P/'
  python3 -I "$C/trois.py" "$T/cible.json" | sed 's/$/\t# 3/'
  python3 -I "$C/accents.py" "$T/cible.json" | sed 's/$/\t# A/'
  python3 -I "$C/lettres.py" "$T/cible.json" ti fi | sed 's/$/\t# L/'
} > "$T/propositions.txt"
wc -l < "$T/propositions.txt"
