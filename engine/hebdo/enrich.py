"""Introït (incipit), notice du Martyrologe et entrées du martyrologe du jour (données DO)."""
from __future__ import annotations

import re
import unicodedata

from . import do

MOIS = {'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
        'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12}


def _vide(path: str) -> str | None:
    for sec in ("Rule", "Rank"):
        for l in do.missa("Latin", path, sec) or []:
            m = re.search(r"\b(?:vide|ex)\s+([A-Za-z0-9/\-]+)", l)
            if m:
                t = m.group(1)
                return t if "/" in t else "Commune/" + t
    return None


def introit_lines(path: str, lang: str = "Latin", depth: int = 0) -> list[str] | None:
    if path == "Sancti/12-25":
        path = "Sancti/12-25m3"
    if path == "Sancti/10-31v":          # vigile de la Toussaint anticipée
        path = "Sancti/10-31"
    b = do.missa(lang, path, "Introitus")
    if not b and path.startswith("Commune/"):
        # variantes de nommage DO : « C2-1b » → « C2b-1 » → « C2-1 »
        for alt in (re.sub(r"(C\d+)-(\d)([a-z])$", r"\1\3-\2", path), re.sub(r"[a-z]$", "", path)):
            if alt != path:
                b = do.missa(lang, alt, "Introitus")
                if b:
                    break
    if not b:
        v = _vide(path)
        if v and depth < 3 and v != path:
            return introit_lines(v, lang, depth + 1)
        return None
    return b


def incipit(path: str) -> str | None:
    b = introit_lines(path)
    for l in b or []:
        if l.startswith("v. "):
            parts = re.split(r"[:,;.!?]", l[3:])
            t = parts[0].strip()
            if len(t.split()) < 2 and len(parts) > 1:      # « Salve, sancta Parens »
                t = t + ", " + parts[1].strip()
            w = t.split()
            return " ".join(w[:5]) + ("…" if len(w) > 5 else "")
    return None


def office_incipit(office_name: str, path: str) -> str | None:
    if office_name.startswith("Office de la Sainte Vierge"):
        return "Salve, sancta Parens"
    inc = incipit(path) if path else None
    if not inc and path and path.startswith("Tempora/"):
        inc = incipit(path.rsplit("-", 1)[0] + "-0")
    return inc


def office_introit(office_name: str, path: str) -> dict | None:
    """Introït complet (latin, et français s'il existe dans DO), lignes brutes de DO :
    « !Ps 24:1 » = référence, « v. … » = antienne, « &Gloria » = Gloria Patri."""
    if not path or office_name.startswith("Office de la Sainte Vierge"):
        return None
    out = {}
    for cle, lang in (("la", "Latin"), ("fr", "Francais")):
        b = introit_lines(path, lang)
        if not b and path.startswith("Tempora/"):
            b = introit_lines(path.rsplit("-", 1)[0] + "-0", lang)
        out[cle] = b or None
    return out if out["la"] else None


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def keyname(fr: str) -> str | None:
    m = re.match(r"^(?:S\.|Ste|Ss\.|Stes)\s+([^,]+)", fr)
    if not m:
        return None
    n = re.split(r"\s+(?:et|de|d’|Ier|II|VII|le|la)\b", m.group(1))[0]
    return n.strip()


def notice(md: str, fr: str, depth: int = 0) -> str | None:
    kn = keyname(fr)
    if not kn or depth > 1:
        return None
    kk = norm(kn)
    for k, t in do.martyrology(md):
        if kk in norm(t):
            m = re.search(r"dont il est fait mention le [^()]*\((\d+)\s+(\w+)\)", t)
            if m and depth == 0 and m.group(2) in MOIS:
                r = notice(f"{MOIS[m.group(2)]:02d}-{int(m.group(1)):02d}", fr, 1)
                if r:
                    return r
            return t
    return None


STOP = set('bienheureuse vierge marie notre seigneur jesus christ octave saints saint sainte fete commemoraison '
           'apotre apotres confesseur martyr eveque docteur eglise pape apparition les des de la du le et'.split())


def kw(fr: str) -> list[str]:
    w = re.findall(r"[\w’-]+", norm(fr).replace("-", " "))
    return [x for x in w if len(x) > 3 and x not in STOP]


def notice2(md: str, fr: str) -> str | None:
    r = notice(md, fr.replace("-", " "))
    if r:
        return r
    ks = kw(fr)
    if not ks:
        return None
    for k, t in do.martyrology(md):
        nt = norm(t).replace("-", " ")
        if all(x in nt for x in ks):
            return t
    return None


def short(t: str, lim: int = 230) -> str:
    if len(t) <= lim:
        return t
    out = ""
    for s in re.split(r"(?<=[.;])\s+", t):
        if len(out) + len(s) > lim and out:
            break
        out += (" " if out else "") + s
    if len(out) > lim + 80:
        out = out[:lim].rsplit(" ", 1)[0]
    return out + (" […]" if out != t else "")


GRANDS = ("1re cl.", "2e cl.", "dbl maj.")


def notice_for(md: str, office_name: str, rank: str, isfeast: bool) -> str | None:
    """Notice abrégée (calendrier papier) pour les fêtes de 1re et 2e classe et les doubles majeurs."""
    if not isfeast or rank not in GRANDS:
        return None
    if office_name.startswith("Octave") or "jour dans" in office_name:
        return None
    name = office_name.replace("Toussaint", "tous les Saints")
    t = notice2(md, name)
    if not t or t.startswith("Le lendemain"):
        return None
    return short(t, 210)


def martyrology_entries(md: str) -> list[dict]:
    la = dict(do.martyrology(md, "Latin"))
    return [{"cle": k, "texte": t, "texte_la": la.get(k)} for k, t in do.martyrology(md)]
