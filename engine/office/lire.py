"""Lecture fidèle des fichiers de données de Divinum Officium (DO), sans exécuter son code.

Ce module reproduit en Python, ligne pour ligne quand c'est possible, les règles de lecture que le code Perl de DO
applique à ses fichiers texte ; le Perl n'est lu que comme une spécification :

- les conditions « (sed rubrica 1955 omittitur) », leurs forces et leurs portées :
  web/cgi-bin/DivinumOfficium/SetupString.pl, sub vero, parse_conditional, process_conditional_lines ;
- les sections, les en-têtes conditionnels, les inclusions « @Fichier:Section:substitutions » et l'héritage d'un
  fichier entier : setupstring_parse_file, setupstring, get_loadtime_inclusion, do_inclusion_substitutions ;
- le temps liturgique vu par les conditions (« tempore Adventus ») : get_tempus_id, get_dayname_for_condition ;
- les prières « $Nom » et les rubriques « $rubrica Nom » : DivinumOfficium/LanguageTextTools.pm, prayer, rubric.

Données : variable d'environnement HEBDO_DO, sinon vendor/do/web/www (dépôt DivinumOfficium/divinum-officium).
Version des rubriques : « Divino Afflatu - 1954 » (Tabulae/data.txt), comme le reste du moteur.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("HEBDO_DO", ROOT / "vendor" / "do" / "web" / "www"))
HORAS = BASE / "horas"
LATIN = HORAS / "Latin"
VERSION = "Divino Afflatu - 1954"

# --- Contexte ------------------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Contexte:
    """Ce que les conditions de DO interrogent (variables globales du Perl : $hora, $dayofweek, @dayname…)."""

    annee: int
    mois: int
    jour: int
    dayofweek: int  # 0 = dimanche
    dayname0: str  # clé du temporal DO : « Adv1 », « Quadp2 », « Pasc3 », « Pent05 », « Nat1 »…
    hora: str = ""  # « Matutinum », « Laudes », « Prima »… (vide : hors d'une heure)
    version: str = VERSION
    commune: str = ""
    votive: str = ""
    winner: str = ""  # fichier gagnant, ex. « Commune/C12 »
    officio: str = ""  # $dayname[1] (nom de l'office du jour) ; vide pour l'office votif


def _bissextile(a: int) -> bool:
    return a % 4 == 0 and (a % 100 != 0 or a % 400 == 0)


def _yday(j: int, m: int, a: int) -> int:
    """Date.pm, sub date_to_ydays."""
    return (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)[m - 1] + j + (1 if m > 2 and _bissextile(a) else 0)


def _dow(j: int, m: int, a: int) -> int:
    """Date.pm, sub day_of_week (0 = dimanche)."""
    return (a * 365 + (a - 1) // 4 - (a - 1) // 100 + (a - 1) // 400 - 1 + _yday(j, m, a)) % 7


def paques(a: int) -> tuple[int, int]:
    """Date.pm, sub geteaster (Date::Easter) : (jour, mois)."""
    g = a % 19
    c = a // 100
    h = (c - c // 4 - (8 * c + 13) // 25 + 19 * g + 15) % 30
    i = h - (h // 28) * (1 - (h // 28) * (29 // (h + 1)) * ((21 - g) // 11))
    j = (a + a // 4 + i + 2 - c + c // 4) % 7
    lune = i - j
    mois = 3 + (lune + 40) // 44
    return lune + 28 - 31 * (mois // 4), mois


def getweek(j: int, m: int, a: int, lendemain: bool = False) -> str:
    """Date.pm, sub getweek : $dayname[0] (« Adv1 », « Nat25 », « Epi3 », « Quadp2 », « Pasc0 », « Pent05 »…)."""
    t = _yday(j, m, a) + (1 if lendemain else 0)
    jj = j + 1 if lendemain else j
    noel = _yday(25, 12, a)
    dow_noel = _dow(25, 12, a) or 7
    avent1 = noel - dow_noel - 21
    if t >= avent1:
        if t < noel:
            n = 1 + (t - avent1) // 7
            if m == 11 or j < 25:
                return f"Adv{n}"
        return f"Nat{jj}"
    ordtime = 6 + 7 - _dow(6, 1, a)
    if m == 1 and t < ordtime:
        return f"Nat{jj:02d}"
    pj, pm = paques(a)
    p = _yday(pj, pm, a)
    if t < p - 63:
        return f"Epi{(t - ordtime) // 7 + 1}"
    if t < p - 56:
        return "Quadp1"
    if t < p - 49:
        return "Quadp2"
    if t < p - 42:
        return "Quadp3"
    if t < p:
        return f"Quad{1 + (t - (p - 42)) // 7}"
    if t < p + 56:
        return f"Pasc{(t - p) // 7}"
    n = (t - (p + 49)) // 7
    if n < 23:
        return f"Pent{n:02d}"
    wdist = (avent1 - t + 6) // 7
    if wdist < 2:
        return "Pent24"
    if n == 23:
        return "Pent23"
    return f"Epi{8 - wdist}"


def tempus_id(c: Contexte) -> str:
    """SetupString.pl, sub get_tempus_id (sans les augmentations GABC propres au chant)."""
    vesp_or_comp = c.hora in ("Vespera", "Completorium")
    oct_or_nov = c.mois in (10, 11)
    d, m, j, dow = c.dayname0, c.mois, c.jour, c.dayofweek
    if d.startswith("Adv"):
        return "Adventus"
    if d.startswith("Nat"):
        return "Epiphaniæ" if (m == 1 and (j >= 6 or (j == 5 and vesp_or_comp))) else "Nativitatis"
    if d.startswith("Epi"):
        if m == 1 and j <= 13:
            return "Epiphaniæ"
        if m == 1 or (m == 2 and (j == 1 or (j == 2 and not vesp_or_comp))):
            return "post Epiphaniam post partum"
        if m == 2:
            return "post Epiphaniam"
        return "post Pentecosten in hieme"
    mq = re.match(r"^Quadp(\d)", d)
    if mq and (int(mq.group(1)) < 3 or dow < 3):
        if m == 1 or (m == 2 and (j == 1 or (j == 2 and not vesp_or_comp))):
            return "Septuagesimæ post partum"
        return "Septuagesimæ"
    mq = re.match(r"^Quad(\d)", d)
    if mq and int(mq.group(1)) < 5:
        return "Quadragesimæ"
    if d.startswith("Quad"):
        return "Passionis"
    if d.startswith("Pasc0") and vesp_or_comp and dow == 6:
        return "Vigilia Paschalis"
    if d.startswith("Pasc0"):
        return "Octava Paschæ"
    mp = re.match(r"^Pasc(\d)", d)
    if mp and (int(mp.group(1)) < 5 or (int(mp.group(1)) == 5 and (dow < 3 or (not vesp_or_comp and dow == 3)))):
        return "post Octavam Paschæ"
    if re.match(r"^Pasc6-(5|6)", d):
        return "post Octavam Ascensionis"
    if mp and int(mp.group(1)) < 7:
        return "Octava Ascensionis"
    if d.startswith("Pasc"):
        return "Octava Pentecostes"
    if d.startswith("Pent01") and dow == 4:
        return "Corpus Christi post Pentecosten"
    mp = re.match(r"^Pent0(\d)", d)
    if (
        mp
        and ((int(mp.group(1)) == 1 and dow > 4 and not (dow == 6 and vesp_or_comp))
             or (int(mp.group(1)) == 2 and (dow < 5 or (dow == 6 and vesp_or_comp))))
        and not re.search(r"19(?:55|6)", c.version)
    ):
        return "Octava Corpus Christi post Pentecosten"
    if d.startswith("Pent02") and dow == 5 and "1570" not in c.version:
        return "SSmi Cordis post Pentecosten"
    if (
        mp
        and ((int(mp.group(1)) == 2 and dow > 5 and not (dow == 6 and vesp_or_comp))
             or (int(mp.group(1)) == 3 and (dow < 6 or (dow == 6 and vesp_or_comp))))
        and re.search("Divino", c.version, re.I)
    ):
        return "Octava SSmi Cordis post Pentecosten"
    if d.startswith("Pent") and not oct_or_nov:
        return "post Pentecosten"
    return "post Pentecosten in hieme"


def dayname_pour_condition(c: Contexte) -> str:
    """SetupString.pl, sub get_dayname_for_condition (les cas qui ne dépendent que de la date et du gagnant)."""
    vc = c.hora in ("Vespera", "Completorium")
    m, j = c.mois, c.jour
    if m == 1 and (j == 6 or (j == 5 and vc)):
        return "Epiphaniæ"
    if m == 1 and (j == 13 or (j == 12 and vc)):
        return "Baptismatis Domini"
    if re.search(r"Quad6\-[456]", c.winner):
        return "Tridui Sacri"
    if re.search(r"Pasc0\-0", c.winner) and vc and c.dayofweek == 6:
        return "Vigilia Paschalis"
    if re.search(r"10\-DU", c.winner):
        return "regis DNJC"
    if m == 11 and j == 2:  # (le cas du 1er au soir et du 3 dimanche demanderait l'année ; sans objet ici)
        return "Omnium Defunctorum"
    if m == 11 and j == 3:
        return "Malachiae"
    if m == 11 and j == 4:
        return "Caroli"
    if m == 12 and j == 6:
        return "Nicolai"
    if m == 12 and j == 28:
        return "Nat28"
    if m == 12 and j == 29:
        return "Nat29"
    if re.search("Doctor", c.officio, re.I):
        return "doctorum"
    if m == 8 and (j == 6 or (j == 5 and vc)):
        return "transfigurationis"
    if re.search(r"09-15$|09-DT|Quad5-5$", c.winner):
        return "septem doloris"
    if re.search(r"12-25", c.winner):
        return "Nativitatis"
    if re.search(r"Epi1-[1-6]", c.dayname0):
        return "post Dominicam infra Octavam Epiphaniæ"
    if re.search(r"08-20|00-VB", c.winner):
        return "Bernardi"
    return ""


# --- Conditions (SetupString.pl, sub vero, parse_conditional, process_conditional_lines) -------------------------

_POIDS = {"sed": 1, "vero": 1, "atque": 2, "attamen": 3, "si": 0, "deinde": 1}
_A_PORTEE_ARRIERE = {"sed", "vero", "atque", "attamen"}
_STOP = "(?:" + "|".join(_POIDS) + ")"
_PORTEE = (
    r"(?:\bloco\s+(?:hu[ij]us\s+versus|horum\s+versuum)\b)?\s*(?:\b(?:(?:dicitur|dicuntur)(?:\s+semper)?"
    r"|(?:hic\s+versus\s+)?omittitur|(?:hoc\s+versus\s+)?omittitur|(?:hæc\s+versus\s+)?omittuntur"
    r"|(?:hi\s+versus\s+)?omittuntur|(?:haec\s+versus\s+)?omittuntur)\b)?"
)
CONDITIONNEL = r"\(\s*(" + _STOP + r"\b)*(.*?)(" + _PORTEE + r")?\s*\)"
_LIGNE_COND = re.compile(r"^\s*" + CONDITIONNEL + r"\s*(.*)$", re.I)
_BLANCHE = re.compile(r"^\s*_?\s*$")

NUL, LIGNE, BLOC, NID = 0, 1, 2, 3
PAS_ENCORE, VRAI, FACTICE = 0, 1, 2

_PREDICATS = {
    "tridentina": lambda v: re.search("Trident", str(v)) is not None,
    "monastica": lambda v: re.search("Monastic", str(v)) is not None,
    "innovata": lambda v: re.search("2020 USA|NewCal", str(v), re.I) is not None,
    "innovatis": lambda v: re.search("2020 USA|NewCal", str(v), re.I) is not None,
    "paschali": lambda v: re.search("Paschæ|Ascensionis|Octava Pentecostes", str(v), re.I) is not None,
    "post septuagesimam": lambda v: re.search("Septua|Quadra|Passio", str(v), re.I) is not None,
    "prima": lambda v: str(v) == "1",
    "secunda": lambda v: str(v) == "2",
    "tertia": lambda v: str(v) == "3",
    "longior": lambda v: str(v) == "1",
    "brevior": lambda v: str(v) == "2",
    "summorum pontificum": lambda v: re.search(r"194[2-9]]|195[45]|196", str(v)) is not None,
    "feriali": lambda v: re.search("feria|vigilia", str(v), re.I) is not None,
    "in solemnitatibus": lambda v: re.search("solemnis|resurrectionis", str(v), re.I) is not None,
    "in hieme": lambda v: re.search("hieme|Adventus|Nativitatis|Epiphani|gesimæ|Passionis", str(v), re.I) is not None,
    "in æstate": lambda v: re.search("hieme|Adventus|Nativitatis|Epiphani|gesimæ|Passionis", str(v), re.I) is None,
}


def _sujets(c: Contexte) -> dict:
    bissextile = c.annee % 4 == 0 and (c.annee % 100 != 0 or c.annee % 400 == 0)
    return {
        "rubricis": lambda: c.version,
        "rubrica": lambda: c.version,
        "tempore": lambda: tempus_id(c),
        "missa": lambda: "",
        "communi": lambda: c.version,
        "die": lambda: dayname_pour_condition(c),
        "feria": lambda: c.dayofweek + 1,
        "commune": lambda: c.commune,
        "votiva": lambda: c.votive,
        "officio": lambda: c.officio,
        "ad": lambda: c.hora,
        "mense": lambda: c.mois,
        "anno": lambda: "bissextili" if bissextile else "communi",
        "dioecesis": lambda: "",
        "tonus": lambda: "",
        "toni": lambda: "",
    }


def vero(condition: str, c: Contexte) -> bool:
    """SetupString.pl, sub vero : « aut » lie plus fort que « et » ; « nisi » nie la suite jusqu'au « aut » suivant."""
    condition = condition.strip()
    if not condition:
        return True
    sujets = _sujets(c)
    for alternative in re.split(r"\baut\b", condition):
        negation = False
        ok = True
        for morceau in re.split(r"\b(et|nisi)\b", alternative):
            if "nisi" in morceau:
                negation = True
            # Le Perl écrit « next if /et|nisi/ », sans bornes de mot : tout morceau contenant « et » est sauté.
            if re.search("et|nisi", morceau):
                continue
            morceau = re.sub(r"\s+", " ", morceau.strip())
            parts = morceau.split(" ", 1)
            sujet, predicat = (parts + [""])[:2]
            if not predicat:
                predicat, sujet = sujet, ""
            if sujet and sujet.lower() not in sujets:
                predicat = f"{sujet} {predicat}"
                sujet = ""
            sujet = sujet or "tempore"
            f = _PREDICATS.get(predicat.lower())
            valeur = sujets[sujet.lower()]()
            r = f(valeur) if f else re.search(predicat, str(valeur), re.I) is not None
            if not (r != negation):
                ok = False
                break
        if ok:
            return True
    return False


def parse_conditional(stopwords: str, condition: str, portee: str, c: Contexte):
    mots = stopwords.lower().split()
    force = sum(_POIDS.get(m, 0) for m in mots)
    resultat = vero(condition, c)
    implicite = any(m in _A_PORTEE_ARRIERE for m in mots)
    if re.search("versuum|omittuntur", portee, re.I):
        arriere = NID
    elif re.search("versus|omittitur", portee, re.I):
        arriere = BLOC
    elif not re.search("semper", portee, re.I) and implicite:
        arriere = LIGNE
    else:
        arriere = NUL
    if re.search("omittitur|omittuntur", portee, re.I):
        avant = NUL
    elif re.search("dicuntur", portee, re.I):
        avant = BLOC if arriere == BLOC else NID
    else:
        avant = BLOC if arriere in (BLOC, NID) else LIGNE
    return force, resultat, arriere, avant


def conditions(lignes: list[str], c: Contexte) -> list[str]:
    """SetupString.pl, sub process_conditional_lines, transcrite pas à pas."""
    sortie: list[str] = []
    pile = [[VRAI, NID]]
    reperes = [-1]
    for ligne in lignes:
        m = _LIGNE_COND.match(ligne)
        if m:
            force, resultat, arriere, avant = parse_conditional(m.group(1) or "", m.group(2) or "", m.group(3) or "", c)
            ligne = m.group(4)
            dernier = len(reperes) - 1
            if pile[-1][0] == VRAI or force >= dernier:
                if force >= dernier:
                    pile = []
                elif force >= dernier - (len(pile) - 1):
                    del pile[dernier - force:]
                if resultat:
                    cloture = reperes[force] if dernier >= force else -1
                    if arriere == LIGNE:
                        if len(sortie) - 1 > cloture:
                            sortie.pop()
                    elif arriere == BLOC:
                        while len(sortie) - 1 > cloture and not _BLANCHE.match(sortie[-1]):
                            sortie.pop()
                        while len(sortie) - 1 > cloture and _BLANCHE.match(sortie[-1]):
                            sortie.pop()
                    elif arriere == NID:
                        del sortie[cloture + 1:]
                if avant == NUL:
                    avant = NID
                    resultat = True
                if resultat:
                    while len(reperes) <= force:
                        reperes.append(-1)
                    for i in range(force + 1):
                        reperes[i] = len(sortie) - 1
                while force < (len(reperes) - 1) - (len(pile) - 1) - 1:
                    pile.append([FACTICE, avant])
                pile.append([VRAI if resultat else PAS_ENCORE, avant])
            if not ligne:
                continue
        ligne = re.sub(r"^~", "", ligne)
        if pile[-1][0] == VRAI:
            sortie.append(ligne)
        while pile[-1][1] == LIGNE or (pile[-1][1] == BLOC and _BLANCHE.match(ligne)):
            pile.pop()
            while pile and pile[-1][0] == FACTICE:
                pile.pop()
            if not pile:
                pile.append([VRAI, NID])
    return sortie


# --- Fichiers, sections, inclusions -------------------------------------------------------------------------------

INCLUSION = re.compile(
    r"^\s*@([^\n:]+)?(?::([^\n:]+?))?[^\S\n\r]*(?::(.*))?$\n?", re.M
)
_EN_TETE = re.compile(r"^\s*\[([\w #,:-]+)\](?:\s*" + CONDITIONNEL + r")?", re.I)
RIEN, FICHIER, TOUT = 0, 1, 2

_brut: dict[Path, list[str]] = {}


def lire_lignes(chemin: Path) -> list[str]:
    """DivinumOfficium/FileIO.pm, do_read : le fichier en lignes, sans fins de ligne."""
    if chemin not in _brut:
        _brut[chemin] = chemin.read_text(encoding="utf-8").replace("\r\n", "\n").replace("﻿", "").split("\n")
        if _brut[chemin] and _brut[chemin][-1] == "":
            _brut[chemin].pop()
    return _brut[chemin]


def perl_sub(texte: str, motif: str, remplacement: str, drapeaux: str) -> str:
    """Une substitution Perl « s/motif/remplacement/drapeaux » (remplacement interpolé comme une chaîne Perl)."""
    f = 0
    if "i" in drapeaux:
        f |= re.I
    if "s" in drapeaux:
        f |= re.S
    if "m" in drapeaux:
        f |= re.M

    def rempl(m: re.Match) -> str:
        out, i = [], 0
        while i < len(remplacement):
            ch = remplacement[i]
            if ch == "\\" and i + 1 < len(remplacement):
                n = remplacement[i + 1]
                out.append("\n" if n == "n" else n)
                i += 2
            elif ch == "$" and i + 1 < len(remplacement) and remplacement[i + 1].isdigit():
                k = int(remplacement[i + 1])
                out.append(m.group(k) or "")
                i += 2
            else:
                out.append(ch)
                i += 1
        return "".join(out)

    return re.sub(motif, rempl, texte, count=0 if "g" in drapeaux else 1, flags=f)


_SUBST = re.compile(r"(?:s/(?P<s>[^/]*)/(?P<r>[^/]*)/(?P<f>[gism]*))|(?:(?P<n>!?)(?P<b>\d+)(-(?P<e>\d+))?)")


def substitutions(texte: str, subs: str) -> str:
    """SetupString.pl, sub do_inclusion_substitutions : choix de lignes (numérotées depuis 1) ou s///."""
    for m in _SUBST.finditer(subs or ""):
        if m.group("b"):
            s = int(m.group("b")) - 1
            n = int(m.group("e")) - s if m.group("e") else 1
            t = texte.split("\n")
            # split de Perl : les champs vides de fin sont supprimés
            while t and t[-1] == "":
                t.pop()
            pris = t[s:s + n]
            reste = t[:s] + t[s + n:]
            texte = "\n".join(reste if m.group("n") else pris) + "\n"
        else:
            texte = perl_sub(texte, m.group("s"), m.group("r"), m.group("f"))
    return texte


class SectionManquante(Exception):
    pass


@dataclass
class Lecteur:
    """Un jeu de fichiers DO lus dans un contexte donné (le Perl met en cache par version ; nous, par contexte)."""

    c: Contexte
    _caches: dict = field(default_factory=dict)
    consultes: set = field(default_factory=set)

    def _parse(self, fname: str) -> dict[str, str]:
        """SetupString.pl, sub setupstring_parse_file."""
        chemin = LATIN / f"{fname}.txt"
        if not chemin.exists():
            return {}
        self.consultes.add(f"web/www/horas/Latin/{fname}.txt")
        sections: dict[str, list[str]] = {}
        cle = "__preamble"
        sections[cle] = []
        utiliser = True
        for ligne in lire_lignes(chemin):
            m = _EN_TETE.match(ligne) if ligne[:1] == "[" else None
            if m:
                cond = m.group(3)
                if not cond or vero(cond, self.c):
                    utiliser = True
                    cle = m.group(1)
                    sections[cle] = []
                else:
                    utiliser = False
            elif utiliser:
                if ligne[:1] == "@" and cle != "__preamble":
                    ligne = INCLUSION.sub(
                        lambda mm, k=cle: "@" + (mm.group(1) or fname) + ":" + (mm.group(2) or k)
                        + (":" + mm.group(3) if mm.group(3) else ""),
                        ligne,
                    )
                sections[cle].append(ligne)
        return {k: "\n".join(conditions(v, self.c) + [""]) for k, v in sections.items()}

    def fichier(self, fname: str, resoudre: int = TOUT) -> dict[str, str]:
        """SetupString.pl, sub setupstring (latin seul)."""
        fname = fname.removesuffix(".txt")
        if ("brut", fname) not in self._caches:
            self._caches[("brut", fname)] = self._parse(fname)
        sections = dict(self._caches[("brut", fname)])
        if not sections:
            return {}
        if resoudre != RIEN:
            for m in INCLUSION.finditer(sections.get("__preamble", "")):
                inc = m.group(1)
                if inc.strip() == fname:
                    break
                for k, v in self.fichier(inc.strip(), FICHIER).items():
                    if not sections.get(k):
                        sections[k] = v
            sections.pop("__preamble", None)
        if resoudre == TOUT:
            cle_cache = ("tout", fname)
            if cle_cache in self._caches:
                return dict(self._caches[cle_cache])
            cles = (["Rule"] if "Rule" in sections else []) + list(sections)
            for cle in cles:
                if "Commemoratio" in cle:
                    continue
                if not (("LectioE" not in cle and "Evangelium" not in cle) or "Commune" in sections[cle]):
                    continue
                n = 0
                while "@" in sections[cle]:
                    nouveau, k = INCLUSION.subn(
                        lambda m, cle=cle: self._inclusion(m.group(1), m.group(2) or cle, m.group(3), fname),
                        sections[cle],
                    )
                    if not k:
                        break
                    sections[cle] = nouveau
                    n += 1
                    if n > 6:
                        raise SectionManquante(f"{fname}:{cle} : inclusions trop imbriquées")
            self._caches[cle_cache] = dict(sections)
        return sections

    def _inclusion(self, ftitre: str | None, section: str, subs: str | None, appelant: str) -> str:
        """SetupString.pl, sub get_loadtime_inclusion."""
        ftitre = (ftitre or "").strip()
        if "Pasc" in self.c.dayname0 and not re.search(r"C[123]", appelant) and not re.search(
            r"Hymnus|Oratio|Lectio|Secreta|Postcommunio|Versum", section, re.I
        ):
            ftitre = re.sub(r"(C[123][abcd]*)(?![p\d])", r"\1p", ftitre)
        source = self.fichier(ftitre, FICHIER) if ftitre else {}
        texte = source.get(section)
        if texte:
            texte = re.sub(r"\n+$", "\n", texte)
            texte = substitutions(texte, subs or "")
            if texte:
                return texte
        raise SectionManquante(f"{ftitre}:{section} est absente")

    def section(self, fname: str, nom: str) -> str | None:
        return self.fichier(fname).get(nom)

    # LanguageTextTools.pm : prayer, rubric
    def priere(self, nom: str) -> str:
        return self.fichier("Psalterium/Common/Prayers").get(nom) or nom

    def rubrique(self, nom: str) -> str:
        return self.fichier("Psalterium/Common/Rubricae").get(nom) or nom


def ordinarium(nom: str, c: Contexte) -> list[str]:
    """horas.pl, sub getordinarium : le canevas d'une heure, conditions appliquées."""
    chemin = HORAS / "Ordinarium" / f"{nom}.txt"
    return conditions(list(lire_lignes(chemin)), c)


def psaume_brut(numero: str) -> list[str]:
    return list(lire_lignes(LATIN / "Psalterium" / "Psalmorum" / f"Psalm{numero}.txt"))


def depot() -> dict:
    """Le dépôt DO utilisé : URL et commit (vendor/do est un clone du dépôt public)."""
    tete = BASE.parent.parent / ".git"
    commit = ""
    try:
        h = (tete / "HEAD").read_text().strip()
        if h.startswith("ref: "):
            ref = tete / h[5:]
            commit = ref.read_text().strip() if ref.exists() else ""
            if not commit and (tete / "packed-refs").exists():
                for ligne in (tete / "packed-refs").read_text().splitlines():
                    if ligne.endswith(h[5:]):
                        commit = ligne.split()[0]
        else:
            commit = h
    except OSError:
        pass
    return {"depot": "https://github.com/DivinumOfficium/divinum-officium", "commit": commit}
