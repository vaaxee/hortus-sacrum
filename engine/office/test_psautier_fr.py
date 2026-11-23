"""Vérifie data/office/breviaire-fr/psautier-fillion.json (français des psaumes et cantiques, Fillion 1917).

    python3 engine/office/test_psautier_fr.py

1. Forme : chaque pièce a ses versets numérotés (numéros de la Vulgate, croissants pour un psaume), un texte et une page
   de l'édition ; aucun reste de la relecture (« {T: », « [ » de renvoi, « | » de structure).
2. Alignement avec le latin livré : pour chaque paragraphe « [r]Psalmus N[/r] » ou « [r]Psalmus N(a-b)[/r] » de
   data/office/breviaire/*/communs.json et des jours, le nombre de lignes latines (hors rubriques, Gloria, antiennes)
   doit être égal au nombre d'étiquettes `lignes_la` du psaume comprises entre a et b ; chaque verset commence sur une
   ligne connue (`ligne_la`), dans l'ordre.
3. Si le dépôt de Divinum Officium est là (vendor/do ou HEBDO_DO_DEPOT), `lignes_la` est comparé au fichier
   Psalterium/Psalmorum/PsalmN.txt.
4. Couverture : psaumes du latin livré encore sans français (information, pas un échec).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FR = json.loads((ROOT / "data" / "office" / "breviaire-fr" / "psautier-fillion.json").read_text(encoding="utf-8"))
DO = Path(os.environ.get("HEBDO_DO_DEPOT", ROOT / "vendor" / "do")) / "web" / "www" / "horas" / "Latin" / "Psalterium" / "Psalmorum"

echecs: list[str] = []
for k in ("source", "methode", "alignement"):
    if not FR.get(k):
        echecs.append(f"en-tête : « {k} » manque")
for k in ("ouvrage", "edition", "approbation", "url", "page"):
    if not FR.get("source", {}).get(k):
        echecs.append(f"source : « {k} » manque")


def cle(lab: str) -> tuple[int, str]:
    m = re.fullmatch(r"(\d+)([a-z]?)", lab)
    return (int(m.group(1)), m.group(2)) if m else (10**6, "")


# 1. Forme
psaumes = {}
for p in FR["psaumes"]:
    n = p["numero"]
    if n in psaumes:
        echecs.append(f"psaume {n} en double")
    psaumes[n] = p
pieces = [(f"Ps {p['numero']}", p) for p in FR["psaumes"]] + [(c["do"], c) for c in FR.get("cantiques", [])]
for nom, p in pieces:
    vs = p["versets"]
    if not vs:
        echecs.append(f"{nom} : aucun verset")
        continue
    ns = [v["n"] for v in vs]
    if len(set(ns)) != len(ns):
        echecs.append(f"{nom} : numéros de versets en double")
    if "numero" in p and ns != sorted(ns):
        echecs.append(f"{nom} : versets hors d'ordre")
    if "numero" in p and ns != list(range(ns[0], ns[0] + len(ns))):
        echecs.append(f"{nom} : versets non consécutifs ({ns[0]}-{ns[-1]}, {len(ns)} versets)")
    for v in vs:
        t = v.get("fr") or ""
        if not t.strip():
            echecs.append(f"{nom}, v. {v['n']} : texte vide")
        if re.search(r"\{\d+ T:|\[|\||\s{2}", t):
            echecs.append(f"{nom}, v. {v['n']} : reste de relecture : {t[:60]}")
        if not (isinstance(v.get("page"), int) and v["page"] % 2 == 1 and 13 <= v["page"] <= 531):
            echecs.append(f"{nom}, v. {v['n']} : page {v.get('page')}")
    labels = p.get("lignes_la")
    if labels:
        idx = [labels.index(v["ligne_la"]) if v.get("ligne_la") in labels else -1 for v in vs]
        if -1 in idx:
            echecs.append(f"{nom} : verset sans ligne latine connue")
        elif idx != sorted(idx) or idx[0] != 0:
            echecs.append(f"{nom} : lignes latines hors d'ordre")

# 2. Alignement avec le latin livré (communs + jours)
TETE = re.compile(r"^\[r\]Psalmus (\d+)(?:\((\d+[a-z]?)-(\d+[a-z]?)\))?\[/r\]$")
vus: set[int] = set()
controles = 0
for dossier in sorted((ROOT / "data" / "office" / "breviaire").iterdir()):
    fichiers = [dossier / "communs.json"] + sorted(dossier.glob("[0-9][0-9]-[0-9][0-9].json"))
    deja: set[str] = set()
    for f in fichiers:
        d = json.loads(f.read_text(encoding="utf-8"))
        paras = d.get("paragraphes") or []
        if isinstance(paras, dict):
            paras = list(paras.values())
        for para in paras:
            if not isinstance(para, str) or "[r]Psalmus" not in para or para in deja:
                continue
            deja.add(para)
            lignes = para.split("\n")
            for i, l in enumerate(lignes):
                m = TETE.match(l.strip())
                if not m:
                    continue
                n = int(m.group(1))
                vus.add(n)
                p = psaumes.get(n)
                if not p or not p.get("lignes_la"):
                    continue
                corps = []
                for x in lignes[i + 1:]:
                    if x.startswith("[r]Psalmus") or x.startswith("###") or (corps and not x.strip()):
                        break
                    if x.strip() and not x.startswith(("[r]", "℣.", "℟.", "&", "$")):
                        corps.append(x)
                labs = [lab for lab in p["lignes_la"] if lab != "doxologie"]
                if m.group(2):
                    a, b = cle(m.group(2)), cle(m.group(3))
                    sel = [lab for lab in labs
                           if a <= cle(lab) and (cle(lab)[0] < b[0] or (cle(lab)[0] == b[0] and (not b[1] or cle(lab)[1] <= b[1])))]
                    # « 13a » en fin : la ligne « 13 » entière n'y est pas
                    if b[1] == "a":
                        sel = [lab for lab in sel if cle(lab) != (b[0], "")]
                else:
                    sel = labs
                controles += 1
                if len(corps) != len(sel):
                    echecs.append(f"{f.name} : {l.strip()} : {len(corps)} lignes latines, {len(sel)} étiquettes "
                                  f"({sel[:1]}…{sel[-1:]})")

# 3. Latin de DO, si présent
if DO.is_dir():
    for n, p in psaumes.items():
        if not p.get("lignes_la"):
            continue
        labs = []
        for l in (DO / f"Psalm{n}.txt").read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\d+:(\d+[a-z]?)\s", l)
            if m:
                labs.append(m.group(1))
        if labs != p["lignes_la"]:
            echecs.append(f"Ps {n} : lignes_la ≠ Psalm{n}.txt de DO")

# 4. Couverture
manquent = sorted(vus - set(psaumes))
nv = sum(len(p["versets"]) for _, p in pieces)
print(f"{len(psaumes)} psaumes, {len(FR.get('cantiques', []))} cantiques, {nv} versets ; "
      f"{controles} paragraphes latins contrôlés ; DO {'présent' if DO.is_dir() else 'absent'}")
print(f"psaumes du latin livré encore sans français ({len(manquent)}) : {', '.join(map(str, manquent))}")
if echecs:
    print("\n".join(echecs))
    sys.exit(1)
print("ok")
