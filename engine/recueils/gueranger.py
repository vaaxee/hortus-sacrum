"""Dom Guéranger, L'Année liturgique (éd. 1911, 15 vol., archive.org lanneliturgiqu01gu … 15gu) découpée par jour.

Sortie : data/recueils/gueranger/index.json (clé → [volume, rang]) et gueranger/vNN.json (entrées d'un volume),
pour que l'app ne charge qu'un volume à la fois.

Intitulés reconnus :
- dates : « III DÉCEMBRE. » (puis le nom du saint) → D:12-03 ; « LE MÊME JOUR. » → même date, autre saint ;
- temporal : « LE LUNDI / DE LA PREMIÈRE SEMAINE DE L'AVENT. » → T:Adv1-1, « LE DIMANCHE DE LA SEPTUAGÉSIME » → T:Quadp1-0…
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
SRC = RACINE / "vendor" / "sources" / "gueranger"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hamon import recoller, traits  # noqa: E402

MOIS = {"JANVIER": 1, "FEVRIER": 2, "MARS": 3, "AVRIL": 4, "MAI": 5, "JUIN": 6, "JUILLET": 7, "AOUT": 8,
        "SEPTEMBRE": 9, "OCTOBRE": 10, "NOVEMBRE": 11, "DECEMBRE": 12}
ORDN = {"PREMIER": 1, "PREMIERE": 1, "DEUXIEME": 2, "SECOND": 2, "SECONDE": 2, "TROISIEME": 3, "QUATRIEME": 4,
        "CINQUIEME": 5, "SIXIEME": 6, "SEPTIEME": 7, "HUITIEME": 8, "NEUVIEME": 9, "DIXIEME": 10, "ONZIEME": 11,
        "DOUZIEME": 12, "TREIZIEME": 13, "QUATORZIEME": 14, "QUINZIEME": 15, "SEIZIEME": 16, "DIX SEPTIEME": 17,
        "DIX HUITIEME": 18, "DIX NEUVIEME": 19, "VINGTIEME": 20, "VINGT ET UNIEME": 21, "VINGT DEUXIEME": 22,
        "VINGT TROISIEME": 23, "VINGT QUATRIEME": 24}
JOURS = {"DIMANCHE": 0, "LUNDI": 1, "MARDI": 2, "MERCREDI": 3, "JEUDI": 4, "VENDREDI": 5, "SAMEDI": 6}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.upper())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9 ]+", " ", s)).strip()


def romain(s: str) -> int | None:
    s = s.replace("1", "I").replace("l", "I")
    if s == "PREMIER":
        return 1
    v = {"I": 1, "V": 5, "X": 10, "L": 50}
    if not re.fullmatch(r"[IVXL]+", s):
        return None
    n = 0
    for i, c in enumerate(s):
        n += -v[c] if i + 1 < len(s) and v[s[i + 1]] > v[c] else v[c]
    return n if 1 <= n <= 31 else None


DATE = re.compile(r"^(?:LE )?(PREMIER|[IVXL1]{1,7})\s+(" + "|".join(MOIS) + r")\s*$")


def cle_temporal(t: str) -> str | None:
    """Intitulé normalisé du temporal → clé."""
    if t.startswith("LA VIGILE DE NOEL"):
        return "D:12-24"
    if re.match(r"(LE JOUR DE |LA FETE DE )?NOEL\b|LA NATIVITE DE NOTRE SEIGNEUR", t):
        return "D:12-25"
    if t.startswith("LA VIGILE DE L EPIPHANIE"):
        return "D:01-05"
    if re.match(r"(LE JOUR DE |LA FETE DE )?L EPIPHANIE", t):
        return "D:01-06"
    m = re.match(r"LE (\w+) JOUR DANS L OCTAVE DE L EPIPHANIE", t)
    if m and m.group(1) in ORDN:
        return f"D:01-{5 + ORDN[m.group(1)]:02d}"
    if t.startswith("L OCTAVE DE L EPIPHANIE") or t.startswith("LE JOUR OCTAVE DE L EPIPHANIE"):
        return "D:01-13"
    m = re.match(r"LE (\w+(?: \w+)??) DIMANCHE DE L AVENT", t)
    if m and m.group(1) in ORDN:
        return f"T:Adv{ORDN[m.group(1)]}-0"
    m = re.match(r"LE (LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMEDI) DE LA (\w+(?: \w+)??) SEMAINE DE L AVENT", t)
    if m and m.group(2) in ORDN:
        return f"T:Adv{ORDN[m.group(2)]}-{JOURS[m.group(1)]}"
    m = re.match(r"LE (\w+(?: \w+)??) DIMANCHE APRES L EPIPHANIE", t)
    if m and m.group(1) in ORDN:
        return f"T:Epi{ORDN[m.group(1)]}-0"
    for nom, s in (("SEPTUAGESIME", 1), ("SEXAGESIME", 2), ("QUINQUAGESIME", 3)):
        if re.match(rf"LE DIMANCHE DE LA {nom}", t):
            return f"T:Quadp{s}-0"
        m = re.match(rf"LE (LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMEDI) DE LA {nom}", t)
        if m:
            return f"T:Quadp{s}-{JOURS[m.group(1)]}"
    if t.startswith("LE MERCREDI DES CENDRES"):
        return "T:Quadp3-3"
    if re.match(r"LE (JEUDI|VENDREDI|SAMEDI) APRES LES CENDRES", t):
        return f"T:Quadp3-{JOURS[t.split()[1]]}"
    m = re.match(r"LE (\w+(?: \w+)??) DIMANCHE DE CAREME", t)
    if m and m.group(1) in ORDN:
        return f"T:Quad{ORDN[m.group(1)]}-0"
    m = re.match(r"LE (LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMEDI) DE LA (\w+(?: \w+)??) SEMAINE DE CAREME", t)
    if m and m.group(2) in ORDN:
        return f"T:Quad{ORDN[m.group(2)]}-{JOURS[m.group(1)]}"
    if t.startswith("LE DIMANCHE DE LA PASSION"):
        return "T:Quad5-0"
    m = re.match(r"LE (LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMEDI) DE LA (SEMAINE DE LA )?PASSION", t)
    if m:
        return f"T:Quad5-{JOURS[m.group(1)]}"
    if t.startswith("LE DIMANCHE DES RAMEAUX"):
        return "T:Quad6-0"
    m = re.match(r"LE (LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMEDI) SAINT", t)
    if m:
        return f"T:Quad6-{JOURS[m.group(1)]}"
    if re.match(r"LE (SAINT )?(JOUR|DIMANCHE) DE PAQUES", t):
        return "T:Pasc0-0"
    m = re.match(r"LE (LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMEDI) DE PAQUES", t)
    if m:
        return f"T:Pasc0-{JOURS[m.group(1)]}"
    if t.startswith("LE SAMEDI IN ALBIS"):
        return "T:Pasc0-6"
    if "QUASIMODO" in t[:40] or t.startswith("LE DIMANCHE IN ALBIS") or t.startswith("LE DIMANCHE DE L OCTAVE DE PAQUES"):
        return "T:Pasc1-0"
    m = re.match(r"LE (\w+(?: \w+)??) DIMANCHE APRES PAQUES", t)
    if m and m.group(1) in ORDN:
        return f"T:Pasc{ORDN[m.group(1)]}-0"
    if re.match(r"(LA FETE DE L |L )ASCENSION", t):
        return "T:Pasc5-4"
    if t.startswith("LE DIMANCHE DANS L OCTAVE DE L ASCENSION"):
        return "T:Pasc6-0"
    if t.startswith("LA VIGILE DE LA PENTECOTE") or t.startswith("LE SAMEDI VEILLE DE LA PENTECOTE"):
        return "T:Pasc6-6"
    if re.match(r"(LE )?(SAINT )?(JOUR|DIMANCHE) DE LA PENTECOTE", t):
        return "T:Pasc7-0"
    m = re.match(r"LE (LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMEDI) DE LA PENTECOTE", t)
    if m:
        return f"T:Pasc7-{JOURS[m.group(1)]}"
    if re.match(r"(LA FETE DE LA |LE DIMANCHE DE LA )?(TRES )?SAINTE TRINITE", t):
        return "T:Pent01-0"
    if re.match(r"LA FETE DU (TRES )?SAINT SACREMENT|LA FETE DIEU", t):
        return "T:Pent01-4"
    if re.match(r"LA FETE DU (TRES )?SACRE COEUR", t):
        return "F:sacre-coeur"
    m = re.match(r"LE (\w+(?: \w+)*?) DIMANCHE APRES LA PENTECOTE", t)
    if m and m.group(1) in ORDN:
        return f"T:Pent{ORDN[m.group(1)]:02d}-0"
    return None


def bruit(l: str) -> bool:
    """Lignes d'ornement ou de bruit d'OCR (« CtiA ftlA CtiA »)."""
    s = l.strip()
    if not s:
        return False
    lettres = sum(c.isalpha() for c in s)
    return lettres < len(s) * 0.45 or bool(re.fullmatch(r"(\S{2,5}\s+){4,}\S{2,5}", s) and len(set(s.split())) <= 4)


PETITS = {"de", "des", "du", "la", "le", "les", "et", "en", "au", "aux", "dans", "sur", "à", "a", "l", "d", "ou", "pour", "par"}


def casse(t: str) -> str:
    """« SAINT FRANÇOIS XAVIER, APÔTRE DES INDES » → « Saint François Xavier, apôtre des Indes » (approché)."""
    mots = re.split(r"(\W+)", t.lower())
    out, debut = [], True
    for m in mots:
        if m and m[0].isalpha():
            if debut or (m not in PETITS and not re.fullmatch(r"(confesseur|martyr|martyrs|vierge|veuve|pape|évêque|eveque|abbé|abbe|docteur|apôtre|apotre|apôtres|archevêque|religieuse|prêtre|fondateur|fondatrice|roi|reine|diacre|patronne|ermite)", m)):
                m = m[0].upper() + m[1:]
            debut = False
        out.append(m)
    return "".join(out)


def volume(n: int) -> list[dict]:
    t = (SRC / f"g{n:02d}.txt").read_text(encoding="utf-8")
    L = t.splitlines()
    entetes: list[tuple[int, int, str | None, str]] = []  # (ligne début, ligne fin de l'intitulé, clé, titre)

    def capitales(x: str) -> bool:
        """Ligne d'intitulé : surtout des capitales (« Sainte FRANÇOISE, VEUVE ROMAINE. » compte)."""
        lettres = [c for c in x if c.isalpha()]
        return bool(lettres) and sum(c.isupper() for c in lettres) >= 0.7 * len(lettres) and len(x.strip()) < 90

    def bloc_suivant(i: int, maxi: int = 3) -> tuple[list[str], int]:
        """Les lignes d'intitulé à partir de i (en sautant les lignes vides), et la ligne qui suit."""
        k, bloc, vides = i, [], 0
        while k < len(L) and len(bloc) < maxi:
            x = L[k].strip()
            if not x:
                vides += 1
                if vides > 3:
                    break
            elif capitales(x) or "aVENT" in x:
                bloc.append(x)
                vides = 0
            else:
                break
            k += 1
        return bloc, k

    date_cour = None
    i = 0
    while i < len(L):
        s = L[i].strip()
        if not s or not capitales(s):
            i += 1
            continue
        ns = norm(s)
        m = DATE.match(re.sub(r"\b([IVXL]) (?=[IVXL]\b)", r"\1", re.sub(r"^(LE )?IER\b", r"\1PREMIER", ns)))
        if m:
            j = romain(m.group(1))
            if j:
                date_cour = f"D:{MOIS[m.group(2)]:02d}-{j:02d}"
                titre, k = bloc_suivant(i + 1)
                entetes.append((i, k, date_cour, " ".join(titre)))
                i = k
                continue
        if ns.startswith("LE MEME JOUR") and date_cour:
            titre, k = bloc_suivant(i + 1)
            entetes.append((i, k, date_cour, " ".join(titre)))
            i = k
            continue
        if re.match(r"^(LE|LA|L) ", ns) and len(ns) < 90:
            # intitulé du temporal, souvent sur deux ou trois lignes séparées de lignes vides
            bloc, k = bloc_suivant(i, 3)
            c = cle_temporal(norm(" ".join(bloc)))
            if c:
                entetes.append((i, k, c, " ".join(bloc).replace("L'aVENT", "L'AVENT")))
                i = k
                continue
        i += 1
    out = []
    for r, (a, b, c, titre) in enumerate(entetes):
        fin = entetes[r + 1][0] if r + 1 < len(entetes) else len(L)
        corps = "\n".join(l for l in L[b:fin] if not bruit(l))
        # en-têtes courants : « 312 L'AVENT. » / « SAINT FRANÇOIS XAVIER. 313 »
        corps = re.sub(r"(?m)^\s*\d{1,4}\s+[A-ZÉÈÊÀ' .,-]{3,60}$|^\s*[A-ZÉÈÊÀ' .,-]{3,60}\s+\d{1,4}\s*$|^\s*\d{1,4}\s*$", "", corps)
        corps = recoller(traits(corps))
        if len(corps) < 400:
            continue
        titre = re.sub(r"\s{2,}", " ", titre).strip(" .")
        titre = casse(titre)
        out.append({"cle": c, "titre": titre, "tome": n, "page": 0, "corps": corps})
    return out


def main() -> None:
    dest = RACINE / "data" / "recueils" / "gueranger"
    dest.mkdir(parents=True, exist_ok=True)
    index: dict[str, list[list[int]]] = {}
    total = 0
    for n in range(1, 16):
        ent = volume(n)
        for r, e in enumerate(ent):
            index.setdefault(e["cle"], []).append([n, r])
        (dest / f"v{n:02d}.json").write_text(json.dumps({"tome": n, "entrees": ent}, ensure_ascii=False), encoding="utf-8")
        total += len(ent)
        print(n, len(ent), sum(1 for e in ent if e["cle"].startswith("T:")), "temporal")
    doc = {
        "id": "gueranger",
        "titre": "L’Année liturgique",
        "auteur": "Dom Prosper Guéranger, abbé de Solesmes (continuée par Dom Lucien Fromage)",
        "editions": {str(n): f"Tours, Mame, 1911, t. {n}" for n in range(1, 16)},
        "provenance": "archive.org, lanneliturgiqu01gu … lanneliturgiqu15gu ; texte reconnu par OCR, coquilles possibles",
        "index": index,
    }
    (dest / "index.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    print(f"{total} lectures ; {len(index)} clés")


if __name__ == "__main__":
    main()
