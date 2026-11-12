"""Jeûne et abstinence d'après le Code de droit canonique de 1917 (can. 1247, 1250-1254).

Région par défaut : France, où, par indult, ne sont de précepte que Noël,
l'Ascension, l'Assomption et la Toussaint (cf. calendrier papier 2026-2027,
« Le jeûne et l'abstinence » ; référence de l'indult : voir A_FOURNIR.md).
"""
from __future__ import annotations

import datetime as dt

from .liturgy import advent1, easter, ember_days

D = dt.date
TD = dt.timedelta


def holy_days(y: int, region: str = "france") -> dict[D, str]:
    """Fêtes de précepte (can. 1247 §1) tombant dans l'année civile y."""
    E = easter(y)
    univ = {
        D(y, 12, 25): "Noël", D(y, 1, 1): "la Circoncision", D(y, 1, 6): "l’Épiphanie",
        E + TD(39): "l’Ascension", E + TD(60): "la Fête-Dieu", D(y, 12, 8): "l’Immaculée Conception",
        D(y, 8, 15): "l’Assomption", D(y, 3, 19): "la Saint-Joseph", D(y, 6, 29): "la Saint-Pierre-et-Paul",
        D(y, 11, 1): "la Toussaint",
    }
    if region == "universel":
        return univ
    keep = {D(y, 12, 25), E + TD(39), D(y, 8, 15), D(y, 11, 1)}
    return {d: n for d, n in univ.items() if d in keep}


def fasting(d: D, region: str = "france") -> tuple[str, str] | None:
    """Renvoie (code, libellé) : A = abstinence, J = jeûne, JA = jeûne et abstinence."""
    y = d.year
    E = easter(y)
    ash = E - TD(46)
    lent = ash <= d < E
    if d.weekday() == 6:
        return None                                   # can. 1252 §4
    if d == E - TD(1):
        return ("JA", "Jeûne et abstinence jusqu’à midi")
    # Quatre-Temps de l'année liturgique en cours
    ly = y if d >= advent1(y) else y - 1
    ember = set(ember_days(ly))
    vigils = {D(y, 12, 24), E + TD(48), D(y, 8, 14), D(y, 10, 31)}   # can. 1252 §2
    oblig_local = holy_days(y, region)
    oblig_univ = holy_days(y, "universel")
    if d in oblig_local and not lent:
        return None                                   # cessent les jours de précepte hors Carême
    if d == ash or (lent and d.weekday() in (4, 5)) or d in ember or d in vigils:
        return ("JA", "Jeûne et abstinence")
    if lent:
        return ("J", "Jeûne")
    if d.weekday() == 4:
        if d in oblig_univ and d not in oblig_local:
            fete = oblig_univ[d]
            return ("A", f"Abstinence (sauf là où {fete} est fête de précepte)")
        return ("A", "Abstinence")
    return None
