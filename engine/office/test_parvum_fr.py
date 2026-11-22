"""Vérifie que data/office/parvum-fr.json (français du Petit office, Montréal 1905) reste aligné sur data/office/parvum.json.

    python3 engine/office/test_parvum_fr.py

L'alignement se fait par indice de paragraphe ; chaque entrée garde l'empreinte (SHA-1, 12 caractères) du latin auquel
elle répond. Si parvum.py régénère parvum.json et que les indices bougent, ce contrôle échoue : il faut réaligner le
français (le texte français lui-même ne change pas).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LATIN = json.loads((ROOT / "data" / "office" / "parvum.json").read_text(encoding="utf-8"))["paragraphes"]
FR = json.loads((ROOT / "data" / "office" / "parvum-fr.json").read_text(encoding="utf-8"))

STATUTS = {"aligné", "aligné en partie", "sans équivalent", "à transcrire"}
echecs: list[str] = []
paragraphes = FR["paragraphes"]
if len(paragraphes) != len(LATIN):
    echecs.append(f"{len(paragraphes)} entrées pour {len(LATIN)} paragraphes latins")
for i, e in enumerate(paragraphes):
    if e["i"] != i:
        echecs.append(f"entrée {i} : indice {e['i']}")
        continue
    if i < len(LATIN) and hashlib.sha1(LATIN[i].encode("utf-8")).hexdigest()[:12] != e["la_sha1"]:
        echecs.append(f"paragraphe {i} : le latin a changé (réaligner)")
    if e["statut"] not in STATUTS:
        echecs.append(f"paragraphe {i} : statut inconnu « {e['statut']} »")
    if e["statut"].startswith("aligné") and not (e.get("fr") and e.get("page")):
        echecs.append(f"paragraphe {i} : aligné sans texte ou sans page")
    if not e["statut"].startswith("aligné") and e.get("fr"):
        echecs.append(f"paragraphe {i} : texte présent mais statut « {e['statut']} »")

if echecs:
    print("\n".join(echecs))
    sys.exit(1)
faits = sum(1 for e in paragraphes if e["statut"].startswith("aligné"))
print(f"{faits} paragraphes français alignés sur {len(LATIN)} ; empreintes du latin conformes")
