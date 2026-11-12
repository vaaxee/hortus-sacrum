"""Génère le calendrier d'une année liturgique (de l'Avent de Y à la veille de l'Avent de Y+1).

Usage : python -m hebdo.build 2027 [2028 …]   (depuis le dossier engine/)
Sortie : data/calendar/Y-(Y+1).json, même schéma que data/source/calendrier_2026-2027.json,
enrichi de quelques champs (temps, introït latin complet, martyrologe latin).
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

from . import devotions, enrich, fasting, liturgy, stations

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "calendar"
TD = dt.timedelta


def build_year(y: int, region: str = "france") -> list[dict]:
    a, b = devotions.year_bounds(y)
    st = stations.stations(y)
    dev = devotions.all_items(y, liturgy.office)
    out = []
    d = a
    while d <= b:
        o = liturgy.office(d)
        md = o.origin_md or liturgy.kal_key(d)
        f = fasting.fasting(d, region)
        loc = o.local or {}
        out.append({
            "date": d.isoformat(),
            "jour": liturgy.JOURS[d.weekday()],
            "temps": liturgy.season(d),
            "office": o.office,
            "rang": o.rank,
            "couleur": o.color,
            "commemoraisons": o.comms,
            "temporal": o.temporal,
            "est_fete_sanctorale": o.isfeast,
            "propre": loc.get("propre"),
            "fichier_divinum_officium": o.path or None,
            "introit_incipit": loc.get("introit_incipit") or enrich.office_incipit(o.office, o.path),
            "introit": enrich.office_introit(o.office, o.path),
            "station": st.get(d),
            "notice_martyrologe": enrich.notice_for(md, o.office, o.rank, o.isfeast),
            "jeune_abstinence": {"code": f[0], "libelle": f[1]} if f else None,
            "devotions": dev.get(d.isoformat(), []),
            "martyrologe": enrich.martyrology_entries(liturgy.kal_key(d)),
        })
        d += TD(1)
    return out


def main(argv: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    years = [int(x) for x in argv] or [dt.date.today().year]
    for y in years:
        data = build_year(y)
        p = OUT / f"{y}-{y + 1}.json"
        p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{p.relative_to(ROOT)} : {len(data)} jours")


if __name__ == "__main__":
    main(sys.argv[1:])
