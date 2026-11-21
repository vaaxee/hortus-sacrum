#!/bin/bash
# Hamon, 21 nov. : notes de bas de page en fin de méditation, appels, références, espaces parasites.
# Usage : bash chaine_21nov.sh <dossier des PDF (vendor/sources/hamon)> [journal]
# Rejouable : un second passage ne change plus rien.
set -e
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
J=$R/data/recueils/hamon.json
P=${1:-$R/vendor/sources/hamon}
L=${2:-/dev/null}
python3 -I "$H/notes.py" "$P" "$J" "$L" --ecrire
python3 -I "$H/appels.py" "$J" --ecrire | head -1
python3 -I "$H/references.py" "$J" "$R/data/ecriture" --ecrire | head -1
python3 -I "$R/engine/recueils/relecture/commun/remplacer.py" "$J" "$H/coupes_21nov.txt" --ecrire | tail -1
python3 -I "$R/engine/recueils/relecture/commun/remplacer.py" "$J" "$H/espaces_21nov.txt" --ecrire | tail -1
