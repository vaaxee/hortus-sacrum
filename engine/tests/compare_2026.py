"""Compare le nouveau moteur au calendrier 2026-2027 validé (data/source/calendrier_2026-2027.json).

Écarts connus et acceptés (corrections du nouveau moteur) : voir KNOWN.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine"))

from hebdo import build  # noqa: E402

REF = json.loads((ROOT / "data/source/calendrier_2026-2027.json").read_text(encoding="utf-8"))
FIELDS = ["date", "jour", "office", "rang", "couleur", "commemoraisons", "temporal", "est_fete_sanctorale",
          "fichier_divinum_officium", "introit_incipit", "station", "notice_martyrologe", "jeune_abstinence"]
# 22 févr. : la condition DO « rubrica 1930 » (monastique) était prise à tort pour 1954.
KNOWN = {("2027-02-22", "office"), ("2027-02-22", "notice_martyrologe"),
         # jours dans l'octave de la Fête-Dieu : Introït de la fête (Cibavit), non celui de la Trinité
         ("2027-05-28", "introit_incipit"), ("2027-05-29", "introit_incipit")}


def introit_ok(ref, new):
    """Incipits complétés (un seul mot auparavant) ou ajoutés là où l'ancien moteur n'en trouvait pas."""
    if ref is None:
        return new is not None
    return new is not None and new.lower().startswith(ref.rstrip("…").lower())


def strip_dev(lst):
    return [{k: v for k, v in x.items() if k in ("type", "libelle", "page_jardin")} for x in lst]


def main():
    new = build.build_year(2026)
    assert len(new) == len(REF), (len(new), len(REF))
    bad = 0
    for r, n in zip(REF, new):
        for k in FIELDS:
            if k == "introit_incipit" and introit_ok(r[k], n[k]):
                continue
            if r[k] != n[k] and (r["date"], k) not in KNOWN:
                bad += 1
                print(r["date"], k, "| réf :", r[k], "| nouveau :", n[k])
        if sorted(map(json.dumps, r["devotions"])) != sorted(map(json.dumps, strip_dev(n["devotions"]))):
            bad += 1
            print(r["date"], "devotions | réf :", r["devotions"], "| nouveau :", strip_dev(n["devotions"]))
        if [(m["cle"], m["texte"]) for m in r["martyrologe"]] != [(m["cle"], m["texte"]) for m in n["martyrologe"]]:
            bad += 1
            print(r["date"], "martyrologe diffère")
    print(f"{bad} écart(s) sur {len(REF)} jours")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
