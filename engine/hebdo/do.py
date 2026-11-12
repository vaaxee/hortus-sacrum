"""Lecture des données de Divinum Officium (DO), version « Divino Afflatu - 1954 ».

On n'utilise que les fichiers de données de DO (pas son code Perl).
Chemin des données : variable d'environnement HEBDO_DO, sinon vendor/do/web/www.
"""
from __future__ import annotations

import functools
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("HEBDO_DO", ROOT / "vendor" / "do" / "web" / "www"))

# Version DO correspondant aux rubriques de 1954 (Tabulae/data.txt).
VERSION = "Divino Afflatu - 1954"
# Étiquettes des tables de translation applicables, par priorité décroissante.
TRANSFER_TAGS = ("1954", "DA")
KALENDARIA = ("1570", "1888", "1906", "1939", "1954")

# Alias de prédicats « rubrica X » (cf. DO, SetupString.pl, sub vero).
_ALIAS = {
    "tridentina": r"Trident",
    "monastica": r"Monastic",
    "innovata": r"2020|NC|Newcal",
    "cisterciensis": r"Cist",
    "altovadensis": r"Altovad",
    "praedicatorum": r"Praedicatorum|Dominican",
    "divino": r"Divino",
    "barroux": r"Barroux",
    "196": r"196",
}


def _atom(pred: str) -> bool:
    pred = pred.strip()
    m = re.match(r"(?:rubrica|rubricis)\s+(\S+)", pred, re.I)
    if not m:
        # « communi Summorum Pontificum », « tempore … » etc. : non applicables ici.
        return False
    key = m.group(1).lower()
    rx = _ALIAS.get(key, re.escape(m.group(1)))
    return re.search(rx, VERSION, re.I) is not None


def cond_true(cond: str) -> bool:
    """Évalue une condition DO du type « rubrica 1570 aut rubrica 1617 nisi rubrica X »."""
    c = cond.strip()
    c = re.sub(r"^(sed|vero|deinde|si|atque|attamen)\s+", "", c, flags=re.I)
    # retire les mots de portée en fin de condition
    c = re.sub(r"\s+(omittitur|omittuntur|dicitur|dicuntur|loco.*|hæc.*|haec.*)$", "", c, flags=re.I)
    nisi = None
    if " nisi " in c:
        c, nisi = c.split(" nisi ", 1)
    ok = any(all(_atom(p) for p in part.split(" et ")) for part in c.split(" aut "))
    if ok and nisi is not None:
        ok = not any(_atom(p) for p in nisi.split(" aut "))
    return ok


@functools.lru_cache(maxsize=None)
def parse(path: Path):
    """Renvoie (ligne d'en-tête, [(section, condition, lignes)])."""
    if not path.exists():
        return "", []
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    head = lines[0].strip() if lines else ""
    secs = []
    cur = None
    for ln in lines:
        m = re.match(r"^\[([^\]]+)\]\s*(?:\(([^)]*)\))?\s*$", ln)
        if m:
            cur = [m.group(1), m.group(2) or "", []]
            secs.append(cur)
            continue
        if cur is not None:
            cur[2].append(ln)
    return head, secs


def resolve_lines(lines: list[str]) -> list[str]:
    """Applique les conditions « (sed …) » en ligne : la ligne suivante remplace la précédente."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^\((sed|vero|deinde)\s+([^)]*)\)\s*(.*)$", ln.strip(), re.I)
        if m:
            scope_omit = re.search(r"omittitur|omittuntur", m.group(2), re.I)
            if cond_true(m.group(1) + " " + m.group(2)):
                if out:
                    out.pop()
                if scope_omit:
                    i += 1
                    continue
                if m.group(3):
                    out.append(m.group(3))
                    i += 1
                    continue
                # la ligne suivante remplace
                if i + 1 < len(lines):
                    out.append(lines[i + 1])
                i += 2
                continue
            # condition fausse : on saute la ligne de remplacement (sauf omission)
            i += 1 if (scope_omit or m.group(3)) else 2
            continue
        out.append(ln)
        i += 1
    return out


def _file(kind: str, lang: str, path: str) -> Path:
    return BASE / kind / lang / f"{path}.txt"


def section(kind: str, lang: str, path: str, sec: str, _depth: int = 0) -> list[str] | None:
    """Corps d'une section (lignes non vides), en suivant les renvois @ d'en-tête."""
    if _depth > 5:
        return None
    p = _file(kind, lang, path)
    head, secs = parse(p)
    if not secs and not head:
        return None
    cands = [s for s in secs if s[0] == sec]
    pick = None
    for s in cands:
        if s[1] and cond_true(s[1]):
            pick = s
    if pick is None:
        plain = [s for s in cands if not s[1]]
        pick = plain[0] if plain else None
    if pick is not None:
        body = [l for l in resolve_lines(pick[2]) if l.strip()]
        if body and body[0].startswith("@"):
            ref = body[0][1:].strip()
            tgt, _, s2 = ref.partition(":")
            return section(kind, lang, tgt or path, s2 or sec, _depth + 1)
        return body
    if head.startswith("@"):
        return section(kind, lang, head[1:].split(":")[0], sec, _depth + 1)
    return None


def first(kind, lang, path, sec):
    b = section(kind, lang, path, sec)
    return b[0].strip() if b else None


# ------------------------------------------------------------------ rangs, titres
def rank(path: str) -> tuple[str, float] | None:
    r = first("horas", "Latin", path, "Rank")
    if not r:
        return None
    if r.startswith("@"):
        return rank(r[1:].split(":")[0])
    f = r.split(";;")
    txt = f[1] if len(f) > 1 else ""
    try:
        val = float(f[2])
    except (IndexError, ValueError):
        val = 1.0
    return txt, val


def rank_value(path: str, default: float = 1.0) -> float:
    r = rank(path)
    return r[1] if r else default


def rank_text(path: str) -> str:
    r = rank(path)
    return r[0] if r else ""


def title(path: str) -> tuple[str | None, str | None]:
    fr = first("horas", "Francais", path, "Officium")
    la = first("horas", "Latin", path, "Officium")
    fr = fr.split(";;")[0].strip() if fr else None
    la = la.split(";;")[0].strip() if la else None
    if fr is None:
        head, _ = parse(_file("horas", "Latin", path))
        if head.startswith("@"):
            fr = title(head[1:].split(":")[0])[0]
    return fr, la


def exists(path: str) -> bool:
    return _file("horas", "Latin", path).exists()


# ------------------------------------------------------------------ kalendarium
@functools.lru_cache(maxsize=None)
def kalendarium() -> dict[str, list[str]]:
    K: dict[str, list[str]] = {}
    for v in KALENDARIA:
        p = BASE / "Tabulae" / "Kalendaria" / f"{v}.txt"
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line[0] in "#*":
                continue
            parts = line.split("=")
            K[parts[0]] = parts[1].split("~")
    return K


def _transfer_file(name: str) -> dict[str, str]:
    """Lit une table de translation et garde la valeur de plus haute priorité pour 1954."""
    p = BASE / "Tabulae" / "Transfer" / f"{name}.txt"
    T: dict[str, tuple[int, str]] = {}
    if not p.exists():
        return {}
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line[0] == "#" or not re.match(r"^(\d\d-\d\d|Tempora/[^=]+)=", line):
            continue
        k, rest = line.split("=", 1)
        val, _, vers = rest.partition(";;")
        tags = vers.split()
        for prio, tag in enumerate(TRANSFER_TAGS):
            if tag in tags:
                if k not in T or T[k][0] > prio:
                    T[k] = (prio, val)
                break
    return {k: v for k, (_, v) in T.items()}


def transfers(letter: str, easter_md: str) -> dict[str, str]:
    """Translations pour une lettre dominicale et une date de Pâques (ex. « 328 »)."""
    T = dict(_transfer_file(letter))
    T.update(_transfer_file(easter_md))
    return T


# ------------------------------------------------------------------ messe, martyrologe
def missa(lang: str, path: str, sec: str, _depth: int = 0) -> list[str] | None:
    if _depth > 5:
        return None
    p = _file("missa", lang, path)
    if path.startswith("Commune/") and not p.exists():
        p = _file("horas", lang, path)
    head, secs = parse(p)
    if not secs:
        if head.startswith("@"):
            return missa(lang, head[1:].split(":")[0], sec, _depth + 1)
        return None
    cands = [s for s in secs if s[0] == sec]
    pick = None
    for s in cands:
        if s[1] and cond_true(s[1]):
            pick = s
    if pick is None:
        plain = [s for s in cands if not s[1]]
        pick = plain[0] if plain else None
    if pick is not None:
        body = [l for l in resolve_lines(pick[2]) if l.strip()]
        refs = [l for l in body if not l.startswith("!")]
        if refs and refs[0].startswith("@"):
            ref = refs[0][1:]
            tgt, _, s2 = ref.partition(":")
            return missa(lang, tgt or path, s2 or sec, _depth + 1)
        return body
    if head.startswith("@"):
        return missa(lang, head[1:].split(":")[0], sec, _depth + 1)
    return None


def martyrology(md: str, lang: str = "Francais") -> list[tuple[str, str]]:
    p = BASE / "horas" / lang / "Martyrologium" / f"{md}.txt"
    head, secs = parse(p)
    return [(k, " ".join(l.strip() for l in b if l.strip())) for k, c, b in secs if k != "Titulus"]


def martyrology_title(md: str, lang: str = "Francais") -> str | None:
    p = BASE / "horas" / lang / "Martyrologium" / f"{md}.txt"
    head, secs = parse(p)
    for k, c, b in secs:
        if k == "Titulus":
            t = [l.strip() for l in b if l.strip()]
            return t[0] if t else None
    return None
