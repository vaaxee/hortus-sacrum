"""Calendrier romain de 1954 pour n'importe quelle année liturgique.

Généralisation du moteur 2026-2027 (engine/legacy/build.py) : mêmes règles
de précédence (rangs numériques de DO), mais dates calculées pour toute année.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field

from . import do
from .names import FR, fixname

D = dt.date
TD = dt.timedelta
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
ORD = ["", "1er"] + [f"{i}e" for i in range(2, 30)]


# ------------------------------------------------------------------ dates mobiles
def easter(y: int) -> D:
    a = y % 19; b = y // 100; c = y % 100; d = b // 4; e = b % 4
    f = (b + 8) // 25; g = (b - f + 1) // 3; h = (19 * a + b - d - g + 15) % 30
    i = c // 4; k = c % 4; l = (32 + 2 * e + 2 * i - h - k) % 7; m = (a + 11 * h + 22 * l) // 451
    mo = (h + l - 7 * m + 114) // 31; da = ((h + l - 7 * m + 114) % 31) + 1
    return D(y, mo, da)


def advent1(y: int) -> D:
    """Premier dimanche de l'Avent de l'année civile y."""
    xmas = D(y, 12, 25)
    back = (xmas.weekday() + 1) % 7 or 7
    return xmas - TD(back) - TD(21)


def dow(d: D) -> int:
    """0 = dimanche … 6 = samedi (convention DO)."""
    return (d.weekday() + 1) % 7


def epiphany_sunday1(y: int) -> D:
    """Dimanche dans l'octave de l'Épiphanie (7-13 janvier)."""
    j7 = D(y, 1, 7)
    return j7 + TD((6 - j7.weekday()) % 7)


def ember_september(y: int) -> list[D]:
    """Quatre-Temps de septembre : mercredi, vendredi et samedi après le 14 septembre."""
    s = D(y, 9, 14)
    wed = s + TD((2 - s.weekday()) % 7 or 7)
    return [wed, wed + TD(2), wed + TD(3)]


def ember_days(year_of_advent: int) -> list[D]:
    """Les douze jours des Quatre-Temps de l'année liturgique commençant à l'Avent de year_of_advent."""
    a = advent1(year_of_advent)
    y = year_of_advent + 1
    E = easter(y)
    out = [a + TD(17), a + TD(19), a + TD(20)]          # après le 3e dim. de l'Avent
    out += [E - TD(39), E - TD(37), E - TD(36)]          # après le 1er dim. de Carême
    out += [E + TD(52), E + TD(54), E + TD(55)]          # semaine de la Pentecôte
    out += ember_september(y)
    return out


def temporal_key(d: D) -> str | None:
    """Clé DO du temporal (ex. « Adv1-0 », « Pent05-3 »), ou None pendant le temps de Noël."""
    y = d.year
    a = advent1(y)
    w_ = dow(d)
    if a <= d <= D(y, 12, 24):
        return f"Adv{(d - a).days // 7 + 1}-{w_}"
    if d >= D(y, 12, 25) or d <= D(y, 1, 13):
        s1 = epiphany_sunday1(y)
        if d == s1:
            return "Epi1-0"
        return None
    E = easter(y)
    sept = E - TD(63)
    if d < sept:
        s1 = epiphany_sunday1(y)
        return f"Epi{(d - s1).days // 7 + 1}-{w_}"
    if d < E - TD(42):
        return f"Quadp{(d - sept).days // 7 + 1}-{w_}"
    if d < E:
        return f"Quad{(d - (E - TD(42))).days // 7 + 1}-{w_}"
    pent = E + TD(49)
    if d < pent + TD(7):
        return f"Pasc{(d - E).days // 7}-{w_}"
    trin = pent + TD(7)
    w = (d - trin).days // 7 + 1
    n = (a - trin).days // 7          # nombre de dimanches après la Pentecôte
    if w >= n:
        return f"Pent24-{w_}"
    if w <= 23:
        return f"Pent{w:02d}-{w_}"
    return f"Epi{6 - (n - 1 - w)}-{w_}"


def season(d: D) -> str:
    """Temps liturgique, en clair."""
    k = temporal_key(d)
    if k is None:
        y = d.year
        if d >= D(y, 12, 25) or d <= D(y, 1, 5):
            return "Temps de Noël"
        return "Temps de l’Épiphanie"
    s = re.match(r"[A-Za-z]+", k).group(0)
    n = int(re.search(r"\d+", k).group(0))
    if s == "Adv":
        return "Temps de l’Avent"
    if s == "Epi":
        return "Temps après l’Épiphanie" if d.month < 6 else "Temps après la Pentecôte"
    if s == "Quadp":
        return "Temps de la Septuagésime"
    if s == "Quad":
        return "Temps de la Passion" if n >= 5 else "Temps du Carême"
    if s == "Pasc":
        return "Temps pascal"
    return "Temps après la Pentecôte"


# ------------------------------------------------------------------ noms
def tfrench(key: str, d: D) -> str:
    m = re.match(r"([A-Za-z]+)(\d+)-(\d)", key)
    s, w, dw = m.group(1), int(m.group(2)), int(m.group(3))
    jour = JOURS[d.weekday()].capitalize()
    if s == "Adv":
        if dw == 0:
            return f"{ORD[w]} dimanche de l’Avent" + (" (Gaudete)" if w == 3 else "")
        if w == 3 and dw in (3, 5, 6):
            return f"{jour} des Quatre-Temps de l’Avent"
        return "Férie de l’Avent"
    if s == "Epi":
        if d.month >= 6:
            if dw == 0:
                return f"{ORD[w]} dimanche après l’Épiphanie (repris après la Pentecôte)"
            return "Férie"
        if dw == 0:
            return f"{ORD[w]} dimanche après l’Épiphanie" if w > 1 else "Sainte Famille de Jésus, Marie et Joseph"
        return "Férie"
    if s == "Quadp":
        if dw == 0:
            return ["", "Dimanche de la Septuagésime", "Dimanche de la Sexagésime", "Dimanche de la Quinquagésime"][w]
        if w == 3 and dw == 3:
            return "Mercredi des Cendres"
        if w == 3 and dw > 3:
            return f"{jour} après les Cendres"
        return "Férie"
    if s == "Quad":
        if w == 5 and dw == 0:
            return "1er dimanche de la Passion"
        if w == 6:
            if dw == 0:
                return "Dimanche des Rameaux"
            return {1: "Lundi saint", 2: "Mardi saint", 3: "Mercredi saint", 4: "Jeudi saint",
                    5: "Vendredi saint", 6: "Samedi saint"}[dw]
        if dw == 0:
            return f"{ORD[w]} dimanche de Carême" + (" (Laetare)" if w == 4 else "")
        if w == 1 and dw in (3, 5, 6):
            return f"{jour} des Quatre-Temps de Carême"
        if w == 5:
            return f"{jour} de la Passion"
        return "Férie de Carême"
    if s == "Pasc":
        if w == 0:
            return "Dimanche de Pâques" if dw == 0 else f"{jour} de Pâques"
        if w == 1 and dw == 0:
            return "Dimanche in Albis (Quasimodo)"
        if w == 5 and dw == 4:
            return "Ascension de Notre-Seigneur"
        if w == 5 and dw in (1, 2, 3):
            return f"{jour} des Rogations" + (" (vigile de l’Ascension)" if dw == 3 else "")
        if w == 6 and dw == 0:
            return "Dimanche dans l’octave de l’Ascension"
        if w == 6 and dw == 6:
            return "Vigile de la Pentecôte"
        if (w == 5 and dw > 4) or (w == 6 and dw < 5):
            return "Octave de l’Ascension" if (w == 6 and dw == 4) else "Dans l’octave de l’Ascension"
        if w == 7:
            if dw == 0:
                return "Dimanche de la Pentecôte"
            return f"{jour} des Quatre-Temps de Pentecôte" if dw in (3, 5, 6) else f"{jour} de Pentecôte"
        if dw == 0:
            return f"{ORD[w]} dimanche après Pâques"
        return "Férie du temps pascal"
    if s == "Pent":
        if w == 1 and dw == 0:
            return "Très Sainte Trinité"
        if w == 1 and dw == 4:
            return "Fête-Dieu (Saint-Sacrement)"
        if w == 2 and dw == 5:
            return "Sacré-Cœur de Jésus"
        if dw == 0:
            return f"{ORD[w]} dimanche après la Pentecôte"
        if (w == 1 and dw > 4) or (w == 2 and dw < 4):
            return "Dans l’octave du Saint-Sacrement"
        if w == 2 and dw == 4:
            return "Octave du Saint-Sacrement"
        if (w == 2 and dw == 6) or (w == 3 and dw < 5):
            return "Dans l’octave du Sacré-Cœur"
        if w == 3 and dw == 5:
            return "Octave du Sacré-Cœur"
        return "Férie"
    return key


FERIAS = ("Férie", "Férie du temps pascal")


def tname(key: str, d: D) -> str:
    n = tfrench(key, d)
    if n in FERIAS and do.rank_value("Tempora/" + key) > 1.5:
        fr, _ = do.title("Tempora/" + key)
        if fr:
            return fr
    return n


def trank(key: str, d: D) -> float:
    r = do.rank_value("Tempora/" + key)
    if tname(key, d) in FERIAS:
        r = min(r, 1.0)
    return r


def frname(key: str) -> str:
    if key in FR:
        return FR[key]
    fr, la = do.title("Sancti/" + key)
    if fr and not re.search(r"(Confessoris|Martyris|Virginis|Episcopi|Papæ|infra|Infra|Octava |Vigilia)", fr):
        return fr
    return fr or la or key


RT = {"Duplex I classis": "1re cl.", "Duplex II classis": "2e cl.", "Duplex majus": "dbl maj.",
      "Duplex": "dbl", "Semiduplex": "semi-dbl", "Simplex": "simple", "Vigilia": "vigile",
      "Feria major": "fér. maj.", "Feria privilegiata": "fér. priv.", "Feria": "férie"}


def rlabel(path: str, istemp: bool, name: str, r: float) -> str:
    t = (do.rank_text(path) if path else "").lower()
    if istemp and "imanche" in name and name not in ("Dimanche de Pâques", "Dimanche de la Pentecôte"):
        if r >= 6.5:
            return "dim. 1re cl."
        if r >= 5.5:
            return "dim. 2e cl."
        return "dim."
    if "vigil" in t or name.startswith("Vigile"):
        return "vigile 1re cl." if r >= 6 else ("vigile 2e cl." if r >= 5 else "vigile")
    if re.search(r"\b(ii|2|2nd)\s*class", t):
        return "2e cl."
    if re.search(r"\b(i|1|1st)\s*class", t):
        return "1re cl."
    if "duplex majus" in t:
        return "dbl maj."
    if t.startswith("semiduplex"):
        return "semi-dbl"
    if t.startswith("duplex"):
        return "dbl"
    if "simplex" in t:
        return "simple"
    if "feria major" in t:
        return "fér. maj."
    if "privileg" in t:
        return "fér. priv."
    if "feria" in t:
        return "férie"
    if r >= 6:
        return "1re cl."
    if r >= 5:
        return "2e cl."
    if r >= 4:
        return "dbl maj."
    if r >= 3:
        return "dbl"
    if r >= 2:
        return "semi-dbl"
    return "simple" if not istemp else "férie"


def color(name: str, d: D, istemp: bool) -> str:
    n = name
    if n.startswith("Vigile") or "vigile" in n:
        if "Nativité de Notre" in n:
            return "violet"
        if "Épiphanie" in n or "Ascension" in n:
            return "blanc"
        if "Pentecôte" in n:
            return "rouge"
        return "violet"
    if "Vendredi saint" in n or "défunts" in n:
        return "noir"
    if re.search(r"Gaudete|Laetare", n):
        return "rose"
    if "Jeudi saint" in n:
        return "blanc"
    if istemp and re.search(r"Avent|Carême|Passion|Rameaux|Lundi saint|Mardi saint|Mercredi saint|Samedi saint|Cendres|gésime|Rogations|Quatre-Temps", n) and "Pentecôte" not in n:
        return "violet"
    if n == "Les Saints Innocents" and d.weekday() != 6:
        return "violet"
    if re.search(r"Pentecôte", n) and istemp and not re.search(r"après la Pentecôte", n):
        return "rouge"
    if re.search(r"Jean, Apôtre et Évangéliste|Conversion|Chaire|Dédicace|Pierre aux Liens|Stigmates", n):
        return "blanc"
    if re.search(r"Martyr|Apôtre|Évangéliste|Croix|Précieux Sang|Pierre et Paul|Décollation|Innocents|Étienne", n):
        return "rouge"
    if istemp and re.search(r"après la Pentecôte|après l’Épiphanie|^Férie$", n):
        return "vert"
    return "blanc"


SATBVM = "Office de la Sainte Vierge le samedi"
TEMPORA_NAMES = {"Nat1-0": "Dimanche dans l’octave de Noël", "Nat2-0": "Très Saint Nom de Jésus",
                 "Epi3-0": "3e dimanche après l’Épiphanie (anticipé au samedi)"}


# ------------------------------------------------------------------ lettre dominicale
_CUM = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def dominical_letter(d: D) -> str:
    """Lettre dominicale valable pour la date d (la seconde lettre après février des années bissextiles)."""
    doy_common = _CUM[d.month - 1] + d.day          # rang du jour dans une année commune
    if d.month == 2 and d.day == 29:
        doy_common = 60
    jan1 = (d.weekday() - (doy_common - 1)) % 7       # jour de la semaine du 1er janvier fictif
    return "abcdefg"[(6 - jan1) % 7]


def transfer_table(d: D) -> dict[str, str]:
    E = easter(d.year)
    return do.transfers(dominical_letter(d), f"{E.month}{E.day:02d}")


# ------------------------------------------------------------------ propres locaux
_LOCAL: dict[str, list[dict]] = {}


def register_local(md: str, entry: dict) -> None:
    """Ajoute une fête d'un propre local (ex. propre de France) : voir propres.py."""
    _LOCAL.setdefault(md, []).append(entry)


# ------------------------------------------------------------------ office du jour
@dataclass
class Office:
    date: D
    office: str
    rank: str
    color: str
    comms: list[str]
    temporal: str | None
    isfeast: bool
    path: str
    rank_value: float
    local: dict | None = None
    origin_md: str | None = None   # date d'origine d'une fête transférée


def is_leap(y: int) -> bool:
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def kal_key(d: D) -> str:
    """Clé du kalendarium. Années bissextiles : le 24 février est le jour bissexte
    (vigile de S. Matthias, clé DO « 02-29 ») et les fêtes du 24 au 28 février sont
    reportées d'un jour (S. Matthias le 25)."""
    if d.month == 2 and is_leap(d.year) and d.day >= 24:
        return "02-29" if d.day == 24 else f"02-{d.day - 1:02d}"
    return f"{d.month:02d}-{d.day:02d}"


def _cands(d: D):
    md = kal_key(d)
    T = transfer_table(d)
    moved = set()
    for k, v in T.items():
        if not v.startswith("Tempora/"):
            for f in v.split("~"):
                if f != k:
                    moved.add(f)
    cands = []   # [rang, nom, latin, temporal?, chemin, local]
    tk = temporal_key(d)
    E = easter(d.year)
    sept = ember_september(d.year)
    if d in sept:
        cands.append([2.1, f"{JOURS[d.weekday()].capitalize()} des Quatre-Temps de septembre", "", True,
                      f"Tempora/093-{dow(d)}", None])
    elif tk:
        cands.append([trank(tk, d), tname(tk, d), do.title("Tempora/" + tk)[1] or "", True, "Tempora/" + tk, None])
    origin = None
    if md in T:
        val = T[md]
        if val.startswith("Tempora/"):
            k = val.split("/")[1]
            nm = TEMPORA_NAMES.get(k, do.title(val)[0] or k)
            cands = [[do.rank_value(val, 5), nm, do.title(val)[1] or "", True, val, None]]
            files = []
        else:
            files = val.split("~")
            if files and files[0] != md and re.match(r"\d\d-\d\d$", files[0]):
                origin = files[0]
    else:
        files = [f for f in do.kalendarium().get(md, []) if f not in moved]
        if md == "02-23" and is_leap(d.year):
            files = [f for f in files if f != "02-23o"]   # la vigile passe au jour bissexte
    for i, f in enumerate(files):
        if f.startswith("X"):
            continue
        r = do.rank_value("Sancti/" + f) if i == 0 else min(do.rank_value("Sancti/" + f), 1.1)
        cands.append([r, fixname(frname(f)), do.title("Sancti/" + f)[1] or "", False, "Sancti/" + f, None])
    for loc in _LOCAL.get(md, []):
        if loc.get("years") and d.year not in loc["years"]:
            continue
        cands.append([loc["rank_value"], loc["office"], loc.get("latin", ""), False, loc.get("path", ""), loc])
    if not cands:
        cands = [[1.0, "Férie", "", True, "", None]]
    return cands, origin


def office(d: D) -> Office:
    md = f"{d.month:02d}-{d.day:02d}"
    cands, origin = _cands(d)
    cands.sort(key=lambda c: -c[0])
    win = cands[0]
    comms = [c[1] for c in cands[1:] if not (c[3] and c[0] <= 1.0) and c[1] not in FERIAS]
    E = easter(d.year)
    holy = (E - TD(7) <= d <= E + TD(7)) or (E + TD(49) <= d <= E + TD(55))
    if holy and d.weekday() != 6:
        comms = []
    if holy and d == E:
        comms = []
    if md in ("12-29", "12-31") and not win[3]:
        comms = comms + ["Octave de Noël"]
    if md == "12-24":
        comms = []
    # dimanches dans les octaves privilégiées du temps pascal et après la Pentecôte
    extra = {E + TD(21): "Octave de S. Joseph", E + TD(63): "Octave du Saint-Sacrement",
             E + TD(70): "Octave du Sacré-Cœur"}
    if d in extra and d.weekday() == 6:
        comms = comms + [extra[d]]
    comms = [fixname(c) for c in comms]
    name = win[1]
    if win[3] and win[0] <= 1.0 and d.weekday() == 5 and not cands[1:]:
        name, lab, col = SATBVM, "simple", "blanc"
    elif win[5] is not None:
        lab, col = win[5]["rank"], win[5]["color"]
    else:
        lab = rlabel(win[4], win[3], name, win[0])
        col = color(name, d, win[3])
        if win[3] and win[4].startswith("Tempora/Quadp"):
            col = "violet"   # féries du temps de la Septuagésime
    if d.weekday() == 6 and any(x in ("Octave du Saint-Sacrement", "Octave du Sacré-Cœur") for x in comms):
        col = "blanc"
    tempname = next((c[1] for c in cands if c[3]), None)
    return Office(d, name, lab, col, comms, tempname, not win[3], win[4], win[0], win[5], origin)
