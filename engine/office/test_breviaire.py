"""Contrôle du Bréviaire romain livré (data/office/breviaire/2026-2027), produit par engine/office/breviaire.py.

    python3 engine/office/test_breviaire.py

1. Chaque jour du calendrier 2026-2027 a son fichier, huit heures non vides, et chaque référence se résout.
2. **Témoin croisé** entre deux moteurs indépendants : pour chaque jour, l'oraison de l'office que donne *notre*
   calendrier (data/calendar, champ `fichier_divinum_officium`, section [Oratio] du fichier latin de DO) doit se
   retrouver dans les Laudes produites par le moteur de DO. Un désaccord signale une erreur de précédence de l'un des
   deux. Les écarts connus sont listés dans CONNUS avec leur raison.
3. Aucun renvoi DO non résolu (« &psalm », « $Pater », « @Commune ») ni balise HTML ne reste dans le texte.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "data" / "office" / "breviaire" / "2026-2027"
LATIN = ROOT / "vendor" / "do" / "web" / "www" / "horas" / "Latin"
CONNUS: dict[str, str] = {}


def norm(s: str) -> str:
    # variantes que le moteur de DO applique lui-même (spell_var : Genetrix → Genitrix hors 1960)
    s = re.sub(r"^v\.\s*", "", s.strip()).replace("Genetr", "Genitr").replace("genetr", "genitr")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = s.replace("j", "i").replace("æ", "ae").replace("œ", "oe")
    return re.sub(r"[^a-z]+", " ", s).strip()


def oraison(fichier: str) -> str | None:
    """Première ligne de [Oratio] du fichier DO (en suivant un renvoi @Fichier simple)."""
    for _ in range(4):
        p = LATIN / f"{fichier}.txt"
        if not p.exists():
            return None
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^\[Oratio\]\s*\n(.+)$", t, re.M)
        if not m:
            return None
        ligne = m.group(1).strip()
        r = re.match(r"@([^:\s]+)(?::Oratio)?\s*$", ligne)
        if r:
            fichier = r.group(1)
            continue
        return None if ligne.startswith(("@", "$", "&")) else ligne
    return None


def main() -> int:
    communs = json.loads((DOSSIER / "communs.json").read_text(encoding="utf-8"))
    cal = json.loads((ROOT / "data" / "calendar" / "2026-2027.json").read_text(encoding="utf-8"))
    P = communs["paragraphes"]
    fautes: list[str] = []
    ecarts: list[str] = []
    non_verifiees: list[str] = []
    for j in cal:
        f = DOSSIER / f"{j['date'][5:]}.json"
        if not f.exists():
            fautes.append(f"{j['date']} : fichier absent")
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        if d["date"] != j["date"]:
            fautes.append(f"{j['date']} : le fichier porte la date {d['date']}")
            continue
        if len(d["heures"]) != 8:
            fautes.append(f"{j['date']} : {len(d['heures'])} heures")
            continue
        heures = []
        for i, h in enumerate(d["heures"]):
            if not h:
                fautes.append(f"{j['date']} heure {i} vide")
            try:
                heures.append("\n".join(P[r] if r >= 0 else d["propres"][-r - 1] for r in h))
            except IndexError:
                fautes.append(f"{j['date']} heure {i} : référence introuvable")
                heures.append("")
        tout = "\n".join(heures)
        if re.search(r"<[A-Za-z/][^>]*>|&psalm|\$[A-Z][a-z]+ [a-z]|@[A-Z][a-z]+[:/]", tout):
            fautes.append(f"{j['date']} : reste de HTML ou de renvoi DO")
        o = oraison(j.get("fichier_divinum_officium") or "")
        if o:
            # jusqu'au premier « N. » (le nom du saint, que DO remplace), huit mots au plus
            mots = norm(o.split(" N.")[0]).split()[:8]
            debut = " ".join(mots)
            if len(mots) < 4:
                # trop court pour comparer (oraison qui commence par le nom du saint) : compté, jamais tenu pour bon
                non_verifiees.append(j["date"])
            elif debut not in norm(heures[1]) and j["date"] not in CONNUS:
                ecarts.append(f"{j['date']} {j['office']} ({j['fichier_divinum_officium']}) — DO : {d['office']}")
    print(
        f"{len(cal)} jours ; {len(P)} paragraphes communs ; {len(fautes)} faute(s) ; {len(ecarts)} écart(s) d'oraison ;"
        f" {len(non_verifiees)} oraison(s) trop courte(s) pour comparer {non_verifiees}"
    )
    for x in fautes[:30] + ecarts[:60]:
        print("  ", x)
    return 1 if fautes or ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
