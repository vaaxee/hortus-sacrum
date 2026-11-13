"""Découpage de Chaignon, « La méditation, ou le fidèle sanctifié par la pratique de l'oraison mentale » (1872, 3 t.).

Entrée : vendor/sources/chaignon/f{1,2,3}.txt (texte OCR d'archive.org, `lamditationoulef0{1,2,3}chai`).
Sortie : data/recueils/chaignon.json.

Le livre a deux parties :
- un **parcours** (t. I et début du t. II) : méditations à suivre dans l'ordre (vie purgative, illuminative, unitive),
  clé « S:<rang> » ;
- l'**année liturgique** (fin du t. II et t. III) : méditations rattachées à un temps ou à une fête, clé T:/D: quand on
  la reconnaît, sinon « L:<rang> ».

Méthode : la table des matières de chaque tome donne, dans l'ordre, le numéro et le titre de chaque méditation ;
on retrouve chaque titre dans le texte (en capitales après « N. MÉDITATION. ») pour couper.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
SRC = RACINE / "vendor" / "sources" / "chaignon"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hamon import MOIS, ORD, JOURS, recoller, traits  # noqa: E402

DEBUT_TABLE = {1: "TABLE  DES  MATIÈRES", 2: "TABLE  DES  MATIÈRES", 3: "TABLE  DES  MATIERES"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.upper())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9 ]+", " ", s)).strip()


ENTREE = re.compile(r"^\s*([IVXLCYÏlU1J]{1,9})\s*[.,]?\s*M[ée]d\s*\.?\s*[—–-]+\s*(.*)$")


def table(n: int) -> list[dict]:
    """Entrées de la table : numéro, titre, section (parcours ou année liturgique)."""
    t = (SRC / f"f{n}.txt").read_text(encoding="utf-8")
    a = t.rfind("TABLE")
    a = t.find(DEBUT_TABLE[n].split()[0], t.rfind(DEBUT_TABLE[n][:10], 0, len(t)) - 5)
    lignes = t[a:].splitlines()
    out: list[dict] = []
    section = "parcours" if n == 1 else None
    cur = None
    for l in lignes:
        s = l.strip()
        if not s:
            continue
        if re.search(r"DIVERS\s+MYST[ÈE]RES|ANN[ÉE]E\s+LITURGIQUE", s):
            section = "liturgie"
        if re.match(r"SECTION|PREMI[ÈE]RE\s+PARTIE|SECONDE\s+PARTIE|CINQUI[ÈE]ME\s+SECTION", s) and section is None:
            section = "parcours"
        m = ENTREE.match(s)
        if m:
            cur = {"num": m.group(1), "titre": m.group(2).strip(), "section": section or "parcours", "fini": False}
            out.append(cur)
            continue
        if cur and not cur["fini"]:
            # le titre continue jusqu'aux points (« I. … ») ou au numéro de page
            if re.match(r"^[IVX1l]{1,4}\s*[.,]\s", s) or re.match(r"^\d{1,3}$", s):
                cur["fini"] = True
            else:
                cur["titre"] += " " + s
                if re.search(r"\.\s*\.\s*\.|\s\d{1,3}\s*$", s):
                    cur["fini"] = True
    for e in out:
        e["titre"] = re.sub(r"[\s.·•■\\]*\d{0,3}\s*$", "", re.sub(r"\s{2,}", " ", e["titre"])).strip(" .—–-")
        e["titre"] = re.sub(r"(\w)-\s+(\w)", r"\1\2", e["titre"])
    return out


def romain(s: str) -> str:
    """Numéro romain lu par l'OCR → forme normale (Y→V, l/1/Ï/J→I, U→II en fin, L1V→LIV)."""
    s = s.strip(" .,").upper().replace("Y", "V").replace("Ï", "I").replace("1", "I").replace("J", "I").replace("Í", "I")
    s = s.replace("CL", "CI") if s == "CL" else s
    if s.endswith("U") and len(s) > 1:
        s = s[:-1] + "II"
    s = s.replace("VL", "VI").replace("XLVL", "XLVI")
    return s if re.fullmatch(r"[IVXLC]+", s) else ""


def mots(s: str) -> list[str]:
    return [w for w in norm(s).split() if len(w) > 2]


def couper(n: int) -> list[dict]:
    """Retrouve chaque entrée de table dans le texte et coupe."""
    t = (SRC / f"f{n}.txt").read_text(encoding="utf-8")
    fin_corps = t.rfind("TABLE")
    lignes = t[:fin_corps].splitlines(keepends=True)
    pos_ligne = []
    p = 0
    for l in lignes:
        pos_ligne.append(p)
        p += len(l)
    nl = [norm(l) for l in lignes]
    ent = table(n)
    # lignes « N. MÉDITATION. » et leur numéro (lecture tolérante des coquilles de l'OCR)
    TETE = re.compile(r"^\s*(\S{1,10})\s*[.,•■]?\s*M\s*[ÉEÈ]\s*D\s*[I1lÏ]\s*T\s*A\s*T\s*[I1lÏ]\s*O\s*N\b")
    tetes = {}
    for i, l in enumerate(lignes):
        m = TETE.match(l)
        if m:
            tetes[i] = romain(m.group(1))
    # alignement global entre les titres de méditation du texte et les entrées de la table :
    # numéro identique (+0,6) et ressemblance du titre avec les lignes qui suivent (+0,7 × ratio)
    H = sorted(tetes)
    apres = {i: " ".join(x for x in nl[i:i + 5] if x) for i in H}
    NI, NJ = len(H), len(ent)

    def score(a: int, b: int) -> float:
        e = ent[b]
        s = 0.6 if tetes[H[a]] and tetes[H[a]] == romain(e["num"]) else 0.0
        cible = " ".join(mots(e["titre"])[:6])
        fen = apres[H[a]]
        s += 0.7 * max(difflib.SequenceMatcher(None, cible, fen[k:k + len(cible) + 10]).ratio() for k in (0, max(0, fen.find(" ") + 1)))
        return s

    V = [[0.0] * (NJ + 1) for _ in range(NI + 1)]
    C = [[""] * (NJ + 1) for _ in range(NI + 1)]
    for a in range(1, NI + 1):
        C[a][0] = "i"
    for b in range(1, NJ + 1):
        C[0][b] = "j"
    for a in range(1, NI + 1):
        for b in range(1, NJ + 1):
            V[a][b], C[a][b] = max((V[a - 1][b - 1] + score(a - 1, b - 1) - 0.55, "d"), (V[a - 1][b] - 0.05, "i"), (V[a][b - 1] - 0.05, "j"))
    debuts: list[int | None] = [None] * NJ
    a, b = NI, NJ
    while a > 0 or b > 0:
        c = C[a][b]
        if c == "d":
            debuts[b - 1] = H[a - 1]
            a, b = a - 1, b - 1
        elif c == "i":
            a -= 1
        else:
            b -= 1
    # entrées sans titre « N. MÉDITATION » reconnu : chercher leur intitulé entre les deux voisines placées
    for b in range(NJ):
        if debuts[b] is not None:
            continue
        lo = next((debuts[x] for x in range(b - 1, -1, -1) if debuts[x] is not None), 0) + 3
        hi = next((debuts[x] for x in range(b + 1, NJ) if debuts[x] is not None), len(lignes))
        cible = " ".join(mots(ent[b]["titre"])[:6])
        best, ou = 0.0, None
        for i in range(lo, hi):
            s = lignes[i].strip()
            if len(nl[i]) < 6 or s.upper() != s:
                continue
            r = difflib.SequenceMatcher(None, cible, " ".join(x for x in nl[i:i + 3] if x)[: len(cible) + 10]).ratio()
            if r > best:
                best, ou = r, i
        if ou is not None and best >= 0.6:
            debuts[b] = ou
    out = []
    pos = [d for d in debuts]
    for k, e in enumerate(ent):
        if pos[k] is None:
            continue
        suiv = next((pos[x] for x in range(k + 1, len(ent)) if pos[x] is not None), len(lignes))
        brut = "".join(lignes[pos[k]:suiv])
        out.append({**e, "tome": n, "texte": brut})
    return out


def nettoyer(brut: str) -> tuple[str, str]:
    """Retire l'intitulé, les en-têtes courants et les numéros de page ; renvoie (plan, corps)."""
    ls = brut.splitlines()
    # en-têtes courants : lignes isolées en capitales courtes ou numéros seuls
    garde = []
    for l in ls:
        s = l.strip()
        if re.fullmatch(r"[—–\-\s]*\d{1,3}[—–\-\s]*", s):
            continue
        if re.fullmatch(r"\d{1,3}\s+[A-ZÉÈ' .—–-]{4,60}", s) or re.fullmatch(r"[A-ZÉÈ' .—–-]{4,60}\s+\d{1,3}", s):
            continue
        garde.append(l)
    t = "\n".join(garde)
    t = re.sub(r"^.*?M\s*[ÉEÈ]\s*D\s*[I1lÏ]\s*T\s*A\s*T\s*[I1lÏ]\s*O\s*N\s*\.?\s*\n", "", t, count=1, flags=re.S)
    # intitulé en capitales répété en tête (le titre est déjà affiché)
    tl = t.lstrip("\n").split("\n")
    while tl and (not tl[0].strip() or (tl[0].strip().upper() == tl[0].strip() and re.search(r"[A-Z]{3}", tl[0]))):
        tl.pop(0)
    t = "\n".join(tl)
    t = re.sub(r"(?m)^\s*(Oraison\s+pr[ée]paratoire|Premier\s+pr[ée]lude|Second\s+pr[ée]lude|Deuxi[èe]me\s+pr[ée]lude|Troisi[èe]me\s+pr[ée]lude|Colloque|R[ée]solution|Bouquet\s+spirituel)\s*[.:]", r"\n\n## \1\n\n", t)
    t = re.sub(r"(?m)^\s*([IV]{1,3})\s*[.,]\s+([A-ZÉÈÀ][^\n]{3,})$", r"\n\n## \1. \2\n\n", t)
    corps = recoller(traits(t))
    return "", corps


def cle_liturgique(titre: str, ctx: dict) -> str | None:
    l = titre.lower().replace("’", "'")
    m = re.search(r"(\d{1,2})(?:er)?\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)", l)
    if m:
        return f"D:{MOIS[m.group(2)]:02d}-{int(m.group(1)):02d}"
    fixes = [
        (r"^noël|nativité de notre-seigneur", "D:12-25"), (r"circoncision", "D:01-01"), (r"épiphanie\b(?! .*dimanche)", "D:01-06"),
        (r"purification", "D:02-02"), (r"annonciation", "D:03-25"), (r"saint joseph\b(?!.*patronage)", "D:03-19"),
        (r"assomption", "D:08-15"), (r"nativité de la (sainte|très sainte) vierge", "D:09-08"), (r"toussaint|tous les saints", "D:11-01"),
        (r"(commémoraison|jour) des morts|fidèles trépassés", "D:11-02"), (r"immaculée", "D:12-08"), (r"présentation de la", "D:11-21"),
        (r"visitation", "D:07-02"), (r"saint pierre", "D:06-29"), (r"nativité de saint jean", "D:06-24"),
        (r"rameaux", "T:Quad6-0"), (r"lundi saint", "T:Quad6-1"), (r"mardi saint", "T:Quad6-2"), (r"mercredi saint", "T:Quad6-3"),
        (r"jeudi saint", "T:Quad6-4"), (r"vendredi saint", "T:Quad6-5"), (r"samedi saint", "T:Quad6-6"), (r"jour de pâques", "T:Pasc0-0"),
        (r"quasimodo", "T:Pasc1-0"), (r"ascension", "T:Pasc5-4"), (r"pentecôte\b(?!.*après)", "T:Pasc7-0"), (r"trinité", "T:Pent01-0"),
        (r"fête-dieu|saint-sacrement|saint sacrement", "T:Pent01-4"), (r"sacré-c[oœ]eur", "F:sacre-coeur"), (r"cendres", "T:Quadp3-3"),
        (r"septuagésime", "T:Quadp1-0"), (r"sexagésime", "T:Quadp2-0"), (r"quinquagésime", "T:Quadp3-0"),
        (r"patronage de saint joseph", "T:Pasc3-0"),
    ]
    for motif, k in fixes:
        if re.search(motif, l):
            return k
    m = re.search(r"(\d{1,2})e\s+dimanche\s+après\s+la\s+pentecôte", l)
    if m:
        return f"T:Pent{int(m.group(1)):02d}-0"
    m = re.search(r"([\w-]+)\s+dimanche\s+(de l'avent|après l'épiphanie|de carême|après pâques|après la pentecôte)", l)
    if m and m.group(1) in ORD:
        n = ORD[m.group(1)]
        t = {"de l'avent": "Adv", "après l'épiphanie": "Epi", "de carême": "Quad", "après pâques": "Pasc", "après la pentecôte": "Pent"}[m.group(2)]
        return f"T:Pent{n:02d}-0" if t == "Pent" else f"T:{t}{n}-0"
    m = re.search(r"(lundi|mardi|mercredi|jeudi|vendredi|samedi) de la semaine de la passion", l)
    if m:
        return f"T:Quad5-{JOURS[m.group(1)]}"
    if "dimanche de la passion" in l:
        return "T:Quad5-0"
    return None


def main() -> None:
    entrees = []
    rang = {"parcours": 0, "liturgie": 0}
    for n in (1, 2, 3):
        for e in couper(n):
            _, corps = nettoyer(e["texte"])
            sec = e["section"]
            rang[sec] += 1
            c = cle_liturgique(e["titre"], {}) if sec == "liturgie" else None
            entrees.append({
                "cle": c or (f"S:{rang[sec]}" if sec == "parcours" else f"L:{rang[sec]}"),
                "titre": traits(e["titre"]), "numero": e["num"], "partie": sec, "tome": n, "page": 0, "corps": corps,
            })
    doc = {
        "id": "chaignon",
        "titre": "La méditation, ou le fidèle sanctifié par la pratique de l’oraison mentale",
        "auteur": "R. P. Chaignon, S. J.",
        "editions": {"1": "Paris, 1872", "2": "Paris, 1872", "3": "Paris, 1872"},
        "provenance": "archive.org, lamditationoulef01chai, …02chai, …03chai ; texte reconnu par OCR, coquilles possibles",
        "entrees": entrees,
    }
    dest = RACINE / "data" / "recueils" / "chaignon.json"
    dest.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    par = sum(1 for e in entrees if e["partie"] == "parcours")
    lit = [e for e in entrees if e["partie"] == "liturgie"]
    print(f"{len(entrees)} méditations : parcours {par}, année liturgique {len(lit)} dont {sum(1 for e in lit if not e['cle'].startswith('L:'))} rattachées à un jour ; {dest}")


if __name__ == "__main__":
    if sys.argv[1:] == ["table"]:
        sys.stdout.reconfigure(encoding="utf-8")
        for n in (1, 2, 3):
            for e in table(n):
                print(n, e["section"], e["num"], "|", e["titre"][:90])
    else:
        main()
