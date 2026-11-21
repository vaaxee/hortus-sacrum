"""Vérifie data/office/parvum.json contre les fichiers de Divinum Officium eux-mêmes.

    python3 engine/office/test_parvum.py

Témoins des trois temps (Avent, Noël, reste de l'année) et de la Septuagésime : des sections lues telles quelles dans
les fichiers DO doivent se retrouver mot pour mot dans l'heure composée ; aucune section vide ; aucun renvoi DO resté
tel quel ; chaque jour du calendrier a ses huit heures ; le lecteur de conditions suit les exemples de SetupString.pl.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lire import LATIN, Contexte, conditions, getweek, lire_lignes, vero  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DONNEES = json.loads((ROOT / "data" / "office" / "parvum.json").read_text(encoding="utf-8"))
ECHECS: list[str] = []


def verifier(cond: bool, message: str) -> None:
    if not cond:
        ECHECS.append(message)


def heure(date: str, cle: str) -> str:
    d0 = dt.date.fromisoformat(DONNEES["jours"]["debut"])
    n = (dt.date.fromisoformat(date) - d0).days
    j = DONNEES["jours"]
    combi = j["combinaisons"][j["chiffres"].index(j["suite"][n])]
    i = [h["cle"] for h in DONNEES["heures"]].index(cle)
    t = DONNEES["textes"][combi["heures"][i]]
    return "\n\n".join(DONNEES["paragraphes"][k] for k in t["paragraphes"])


def brut(fichier: str, section: str) -> list[str]:
    """Les lignes d'une section, lues directement dans le fichier DO (sans aucun traitement)."""
    lignes, dedans = [], False
    for l in lire_lignes(LATIN / f"{fichier}.txt"):
        if l.startswith("["):
            if dedans:
                break
            dedans = l.strip() == f"[{section}]"
            continue
        if dedans:
            lignes.append(l)
    if not lignes:
        raise AssertionError(f"{fichier}:[{section}] introuvable")
    return lignes


def plat(s: str) -> str:
    """Forme de comparaison : sans balisage, sans sigles ℣ ℟ Ant., sans astérisques ni numéros de versets."""
    s = re.sub(r"\[/?r\]", "", s)
    s = re.sub(r"(?m)^\s*(?:℣\.|℟\.|Ant\.|v\.|r\.|V\.|R\.)\s*", "", s)
    s = re.sub(r"\s*\(Allel[uú]ja\.?\)", "", s)  # alléluias du temps pascal, ôtés hors de ce temps (webdia.pl)
    s = s.replace("∗", "").replace("*", "")
    s = s.replace("Génetrix", "Génitrix").replace("Genetrí", "Genitrí")
    s = re.sub(r"\bco(t[ií]d[ií])", r"quo\1", s)
    return re.sub(r"\s+", " ", s).strip()


def temoin(date: str, cle: str, fichier: str, section: str, lignes: slice | None = None) -> None:
    """Chaque ligne de texte de la section DO se retrouve dans l'heure (les renvois et macros sont exclus)."""
    texte = plat(heure(date, cle))
    for l in brut(fichier, section)[lignes or slice(None)]:
        if not l.strip() or l.startswith(("@", "$", "&", "!", "(", "#", "_", "/:")):
            continue
        l = re.sub(r";;.*", "", l)
        l = re.sub(r"^\d+\s+", "", l)  # numéro de verset d'une leçon
        verifier(plat(l) in texte, f"{date} {cle} : {fichier}:[{section}] « {l[:60]} » absent")


# --- conditions : exemples tirés des fichiers DO ------------------------------------------------------------------

c_pa = Contexte(annee=2026, mois=11, jour=24, dayofweek=2, dayname0="Pent25", hora="Laudes")
c_sept = Contexte(annee=2027, mois=2, jour=10, dayofweek=3, dayname0="Quadp1", hora="Laudes")
verifier(vero("rubrica cisterciensis", c_pa) is False, "vero : cisterciensis")
verifier(vero("tempore post septuagesimam", c_sept) is True, "vero : post septuagesimam")
verifier(vero("rubrica 1955 aut rubrica 196", c_pa) is False, "vero : 1955 aut 196")
regle = ["Feria Te Deum", "(sed tempore post septuagesimam)", "no Te Deum"]
verifier(conditions(regle, c_pa) == ["Feria Te Deum"], f"conditions per annum : {conditions(regle, c_pa)}")
verifier(conditions(regle, c_sept) == ["no Te Deum"], f"conditions Septuagésime : {conditions(regle, c_sept)}")
bloc = ["$Pater noster", "(sed rubrica 1955 aut rubrica 196 omittitur)", "$Ave Maria"]
verifier(conditions(bloc, c_pa) == ["$Pater noster", "$Ave Maria"], "conditions : omittitur faux")
verifier(getweek(30, 11, 2025) == "Adv1" and getweek(5, 4, 2026) == "Pasc0", "getweek")

# --- témoins des trois temps --------------------------------------------------------------------------------------

# Avent : Commune/C12A
temoin("2026-12-02", "vepres", "Sancti/03-25", "Ant Vespera")
temoin("2026-12-02", "laudes", "Commune/C12A", "Commemoratio")
temoin("2026-12-02", "matines", "Commune/C12A", "Lectio1")
temoin("2026-12-02", "complies", "Psalterium/Common/Prayers", "ant Alma Redemptoris Mater", slice(0, 6))
# Noël : Commune/C12N, qui renvoie à la Circoncision (Sancti/01-01)
temoin("2026-12-28", "laudes", "Sancti/01-01", "Ant Laudes")
temoin("2026-12-28", "complies", "Sancti/01-01", "Oratio")
temoin("2026-12-28", "prime", "Sancti/01-01", "Ant Vespera", slice(0, 1))
# Reste de l'année : Commune/C12 et le commun C11
temoin("2026-11-24", "laudes", "Commune/C12", "Ant Laudes")
temoin("2026-11-24", "laudes", "Commune/C12", "Commemoratio")
temoin("2026-11-24", "prime", "Commune/C12", "Oratio Prima")
temoin("2026-11-24", "matines", "Commune/C12", "Lectio1")
temoin("2026-11-24", "matines", "Commune/C11", "Hymnus Matutinum", slice(1, 20))
temoin("2026-11-24", "vepres", "Commune/C11", "Hymnus Vespera")
temoin("2026-11-24", "complies", "Commune/C12", "Oratio Completorium")
temoin("2026-11-24", "complies", "Psalterium/Common/Prayers", "ant Salve Regina")
# Septuagésime : Commune/C12Q (« no Te Deum », « Laus tibi »)
verifier("Te Deum" not in heure("2027-02-10", "matines"), "Septuagésime : pas de Te Deum")
verifier("Laus tibi" in heure("2027-02-10", "prime"), "Septuagésime : Laus tibi")
verifier("Te Deum" in heure("2026-11-24", "matines"), "per annum : Te Deum")

# --- intégrité ----------------------------------------------------------------------------------------------------

for ident, t in DONNEES["textes"].items():
    texte = "\n\n".join(DONNEES["paragraphes"][k] for k in t["paragraphes"])
    verifier(not re.search(r"(?m)^[@$&]|\bmissing\b|est absente", texte), f"{ident} : renvoi non résolu")
    blocs = texte.split("\n\n")
    for i, b in enumerate(blocs):
        if b.startswith("### "):
            suite = blocs[i + 1] if i + 1 < len(blocs) else ""
            verifier(bool(suite) and not suite.startswith("### "), f"{ident} : section vide « {b} »")
verifier(len(DONNEES["jours"]["suite"]) >= 365, "au moins une année de jours")
verifier(all(len(c["heures"]) == 8 for c in DONNEES["jours"]["combinaisons"]), "huit heures par jour")
verifier(bool(DONNEES["source"]["commit"]) and DONNEES["source"]["fichiers"], "source citée")

if ECHECS:
    print("\n".join(ECHECS))
    sys.exit(1)
print(f"parvum : {len(DONNEES['textes'])} textes vérifiés, témoins des temps conformes aux fichiers DO")
