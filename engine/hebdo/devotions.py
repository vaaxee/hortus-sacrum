"""Dévotions à jours comptés, neuvaines et préparation de Montfort, pour toute année.

Le catalogue reprend les lignes « usage » du *Jardin de l'âme* (partie VIII).
Un plan explicite (data/plans/AAAA-AAAA.json) l'emporte sur le planificateur
automatique ; sans plan, le planificateur propose un enchaînement sans chevauchement.
"""
from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass
from pathlib import Path

from .liturgy import advent1, easter

D = dt.date
TD = dt.timedelta
ROOT = Path(__file__).resolve().parents[2]
PLANS = ROOT / "data" / "plans"

# pages du Jardin de l'âme
PG = {'stigmates': 62, 'berchmans': 63, 'gonzague': 63, 'thomas': 64, 'joseph7': 64, 'immaculee7': 65,
      'camille': 65, 'ignace': 66, 'stanislas': 66, 'antoine': 68, 'dominique': 68, 'mercredi': 68,
      'heure': 69, 'vendredi1': 69, 'crucifix': 71, 'paule': 72, 'douleurs7': 72, 'samedi1': 73,
      'douze': 73, 'rosaire': 74, 'merci': 76, 'montfort': 11, 'gabriel': 19, 'joseph': 34, 'veni': 56,
      'douleurs': 32, 'michel': 28, 'couronne': 21, 'mediatrice': 17, 'tejoseph': 60}


@dataclass
class Serie:
    key: str
    label: str
    weekday: int          # 0 = lundi … 6 = dimanche
    n: int
    anchor: tuple[int, int] | None   # (mois, jour) de la fête à préparer
    inclusive: bool = False          # la série peut finir le jour même de l'ancre
    strict: bool = False             # « avant le … » obligatoire (sinon : de préférence)
    passion: bool = False            # ancre alternative : vendredi de la Passion


# Ordre = priorité du planificateur (les séries rattachées à une fête d'abord).
CATALOGUE = [
    # dimanches
    Serie('joseph7', 'Sept dimanches de S. Joseph', 6, 7, (3, 19), strict=True),
    Serie('ignace', 'Dix dimanches de S. Ignace', 6, 10, (7, 31), strict=True),
    Serie('stigmates', 'Cinq dimanches des Stigmates de S. François', 6, 5, (9, 17), strict=True),
    Serie('immaculee7', 'Sept dimanches de l’Immaculée Conception', 6, 7, (12, 8)),
    Serie('thomas', 'Six dimanches de S. Thomas d’Aquin', 6, 6, (3, 7)),
    Serie('gonzague', 'Six dimanches de S. Louis de Gonzague', 6, 6, (6, 21)),
    Serie('berchmans', 'Cinq dimanches de S. Jean Berchmans', 6, 5, (8, 13), strict=True),
    Serie('stanislas', 'Dix dimanches de S. Stanislas Kostka', 6, 10, (11, 13), strict=True),
    Serie('camille', 'Sept dimanches de S. Camille de Lellis', 6, 7, None),
    # mardis
    Serie('antoine', 'Treize mardis de S. Antoine', 1, 13, (6, 13)),
    Serie('dominique', 'Quinze mardis de S. Dominique', 1, 15, (8, 4)),
    # vendredis
    Serie('paule', 'Treize vendredis de S. François de Paule', 4, 13, (4, 2), inclusive=True),
    Serie('douleurs7', 'Sept vendredis des Douleurs', 4, 7, (9, 15), passion=True),
    # samedis
    Serie('douze', 'Douze samedis avant l’Immaculée Conception', 5, 12, (12, 8), strict=True),
    Serie('merci', 'Sept samedis de N.-D. de la Merci', 5, 7, (9, 24), strict=True),
    Serie('rosaire', 'Quinze samedis du Rosaire', 5, 15, (10, 7)),
]
BYKEY = {s.key: s for s in CATALOGUE}


def _weekly(start: D, n: int) -> list[D]:
    return [start + TD(7 * i) for i in range(n)]


def year_bounds(y: int) -> tuple[D, D]:
    """Année liturgique : du 1er dimanche de l'Avent de y à la veille de celui de y+1."""
    return advent1(y), advent1(y + 1) - TD(1)


def plan_series(y: int) -> list[tuple[str, D, int]]:
    """Planificateur : (clé, date de début, nombre) sans chevauchement d'un même jour de semaine."""
    a, b = year_bounds(y)
    used: set[D] = set()
    out = []
    for s in CATALOGUE:
        def occ_before(limit: D, inclusive: bool) -> list[D]:
            first = a + TD((s.weekday - a.weekday()) % 7)
            L = []
            d = first
            while d < limit or (inclusive and d == limit):
                L.append(d)
                d += TD(7)
            return L
        all_days = occ_before(b + TD(1), False)
        free = [d for d in all_days if d not in used]

        def window_ok(w: list[D]) -> bool:
            return len(w) == s.n and all(x not in used for x in w) and all(
                (w[i + 1] - w[i]).days == 7 for i in range(len(w) - 1))

        chosen = None
        anchors = []
        if s.anchor:
            m, dd = s.anchor
            for yy in (y, y + 1):
                t = D(yy, m, dd)
                if a <= t <= b + TD(30):
                    anchors.append(t)
        if s.passion:
            anchors.insert(0, easter(y + 1) - TD(9))
        if s.strict:
            # « les N … avant le … » : fenêtre la plus tardive avant la fête, puis on recule
            for t in anchors:
                cand = occ_before(t, s.inclusive)
                for end in range(len(cand), s.n - 1, -1):
                    w = cand[end - s.n:end]
                    if window_ok(w):
                        chosen = w
                        break
                if chosen:
                    break
        else:
            # « de préférence avant le … » : fenêtre libre la plus proche de la fête,
            # dans l'année liturgique (sans fête : la première fenêtre libre)
            wins = [all_days[i:i + s.n] for i in range(len(all_days) - s.n + 1)]
            wins = [w for w in wins if window_ok(w)]
            if wins:
                def dist(w):
                    def one(t):
                        before = w[-1] < t or (s.inclusive and w[-1] == t)
                        return (t - w[-1]).days if before else (w[-1] - t).days + 60
                    return min(one(t) for t in anchors)
                chosen = min(wins, key=dist) if anchors else wins[0]
        if chosen:
            used.update(chosen)
            out.append((s.key, chosen[0], s.n))
    return out


def load_plan(y: int) -> list[tuple[str, D, int]] | None:
    p = PLANS / f"{y}-{y + 1}.json"
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    return [(x["cle"], D.fromisoformat(x["debut"]), x["nombre"]) for x in data["series"]]


def series_items(y: int) -> list[tuple[D, str, str]]:
    plan = load_plan(y) or plan_series(y)
    _, b = year_bounds(y)
    out = []
    for key, start, n in plan:
        s = BYKEY[key]
        days = _weekly(start, n)
        inside = [d for d in days if d <= b]
        for i, d in enumerate(inside):
            lab = f"{s.label} — {i + 1}/{n}"
            if i == len(inside) - 1 and len(inside) < n:
                rest = ", ".join(f"{d2.day} {MOIS_ABR[d2.month]}" for d2 in days[len(inside):])
                lab += f" (le {len(inside) + 1}e : {rest})" if n - len(inside) == 1 else f" (suite : {rest})"
            out.append((d, key, lab))
    return out


MOIS_ABR = ['', 'janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juill.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']


def firsts(y: int) -> list[tuple[D, str, str]]:
    a, b = year_bounds(y)
    out = []
    d = a
    fri = sat = 0
    while d <= b:
        if d.day <= 7:
            if d.weekday() == 2:
                out.append((d, 'mercredi', 'Premier mercredi : S. Joseph'))
            if d.weekday() == 4:
                fri += 1
                out.append((d, 'vendredi1', 'Premier vendredi du mois' + (f' — {fri}/9' if fri <= 9 else '')))
                out.append((d - TD(1), 'heure', 'Heure sainte (veille du premier vendredi)'))
            if d.weekday() == 5:
                sat += 1
                out.append((d, 'samedi1', 'Premier samedi du mois' + (f' — {sat}/5' if sat <= 5 else '')))
        d += TD(1)
    return out


def annunciation_date(y: int, offices) -> D:
    """Date où l'Annonciation est célébrée (transférée après l'octave de Pâques si besoin)."""
    for i in range(0, 30):
        d = D(y, 3, 25) + TD(i)
        o = offices(d)
        if o.path == "Sancti/03-25" or o.origin_md == "03-25":
            return d
    return D(y, 3, 25)


def novenas(y: int, offices) -> list[tuple[D, str | None, str]]:
    """Neuvaines préparatoires aux grandes fêtes de l'année liturgique (y = année de l'Avent)."""
    E = easter(y + 1)
    pent = E + TD(49)
    sh = E + TD(68)
    yy = y + 1
    L = [('Neuvaine à l’Immaculée Conception', D(y, 12, 8), None),
         ('Neuvaine de Noël', D(y, 12, 25), None),
         ('Neuvaine à S. Joseph', D(yy, 3, 19), 'joseph'),
         ('Neuvaine à S. Gabriel', D(yy, 3, 24), 'gabriel'),
         ('Neuvaine à S. Louis-Marie Grignion de Montfort (28 avr.)', D(yy, 4, 28), None),
         ('Neuvaine au Saint-Esprit, avant la Pentecôte', pent, 'veni'),
         ('Neuvaine au Sacré-Cœur', sh, None),
         ('Neuvaine de l’Assomption', D(yy, 8, 15), None),
         ('Neuvaine de la Nativité de Notre-Dame', D(yy, 9, 8), None),
         ('Neuvaine à S. Michel', D(yy, 9, 29), 'michel'),
         ('Neuvaine du Rosaire', D(yy, 10, 7), None),
         ('Neuvaine de la Toussaint', D(yy, 11, 1), None)]
    a, b = year_bounds(y)
    out = []
    for lab, feast, k in L:
        s = feast - TD(9)
        if s < a:
            continue
        for i in range(9):
            out.append((s + TD(i), k, f"{lab} — {'1er' if i == 0 else str(i + 1) + 'e'} jour"))
    return out


def montfort(y: int, offices) -> list[tuple[D, str, str]]:
    c = annunciation_date(y + 1, offices)
    s = c - TD(33)
    out = []
    for i in range(33):
        d = s + TD(i)
        if i < 12:
            ph = f'douze jours : se vider de l’esprit du monde — {i + 1}/12'
        elif i < 19:
            ph = f'1re semaine : connaissance de soi — {i - 11}/7'
        elif i < 26:
            ph = f'2e semaine : connaissance de la sainte Vierge — {i - 18}/7'
        else:
            ph = f'3e semaine : connaissance de Jésus-Christ — {i - 25}/7'
        out.append((d, 'montfort', 'Montfort, ' + ph))
    out.append((c, 'montfort', 'Consécration (renouvellement) à Jésus par Marie — communion de ce jour'))
    return out


def fixed(y: int) -> list[tuple[D, str, str]]:
    yy = y + 1
    pent = easter(yy) + TD(49)
    return [(D(yy, 3, 24), 'gabriel', 'Prière à S. Gabriel'),
            (D(yy, 3, 19), 'joseph', 'Douleurs et Allégresses de S. Joseph ; hymne Te, Joseph, celebrent (p. 60)'),
            (pent, 'veni', 'Veni Creator'),
            (D(yy, 9, 15), 'douleurs', 'Les sept Douleurs de Marie')]


def all_items(y: int, offices) -> dict[str, list[dict]]:
    by: dict[str, list[dict]] = {}
    L = series_items(y) + firsts(y) + montfort(y, offices) + fixed(y)
    for d, k, l in L:
        by.setdefault(d.isoformat(), []).append({"type": "jours_comptes", "cle": k, "libelle": l, "page_jardin": PG.get(k)})
    for d, k, l in novenas(y, offices):
        by.setdefault(d.isoformat(), []).append({"type": "neuvaine", "cle": k, "libelle": l, "page_jardin": PG.get(k) if k else None})
    return by
