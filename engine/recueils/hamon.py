"""Découpage des Méditations de Hamon (3 tomes, PDF Google Livres) en une entrée par jour.

Entrée : vendor/sources/hamon/t{1,2,3}.pdf (texte extrait par pdftotext).
Sortie : data/recueils/hamon.json — une entrée par méditation : clé liturgique, tome, page, titre, sommaire, corps.

Méthode : chaque méditation commence par « SOMMAIRE POUR LA VEILLE AU SOIR ». On aligne ces débuts, dans l'ordre,
sur les lignes de la table des matières, qui donnent le jour (dimanche, férie, date fixe) et la page.
"""
from __future__ import annotations

import difflib
import json
import unicodedata
import re
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
SRC = RACINE / "vendor" / "sources" / "hamon"

ORD = {"premier": 1, "première": 1, "deuxième": 2, "second": 2, "seconde": 2, "troisième": 3, "quatrième": 4, "cinquième": 5,
       "sixième": 6, "septième": 7, "huitième": 8, "neuvième": 9, "dixième": 10, "onzième": 11, "douzième": 12,
       "treizième": 13, "quatorzième": 14, "quinzième": 15, "seizième": 16, "dix-septième": 17, "dix-huitième": 18,
       "dix-neuvième": 19, "vingtième": 20, "vingt et unième": 21, "vingt-et-unième": 21, "vingt-unième": 21,
       "vingt-deuxième": 22, "vingt-troisième": 23, "vingt-quatrième": 24}
JOURS = {"dimanche": 0, "lundi": 1, "landi": 1, "mardi": 2, "mercredi": 3, "jeudi": 4, "vendredi": 5, "samedi": 6}
MOIS = {"janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7, "août": 8, "aout": 8,
        "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12}


def texte(tome: int, layout: bool) -> str:
    out = SRC / f"{'u' if layout else 'r'}{tome}.txt"
    if not out.exists():
        args = ["pdftotext", "-enc", "UTF-8"] + (["-layout"] if layout else []) + [str(SRC / f"t{tome}.pdf"), str(out)]
        subprocess.run(args, check=True)
    return out.read_text(encoding="utf-8")


def table(tome: int) -> list[tuple[str, int]]:
    """Lignes de la table des matières : (libellé, page). Les libellés coupés sur deux lignes sont recollés."""
    t = texte(tome, True)
    debut = t.find("TABLE DES MATI", len(t) - 80000)
    lignes = [l.strip() for l in t[debut:].splitlines()]
    out: list[tuple[str, int]] = []
    attente = ""
    for l in lignes:
        if "TABLE ANALYTIQUE" in l:
            break
        if not l or "TABLE DES MATI" in l or l.startswith("DE PREMIER") or l.startswith("DU "):
            continue
        m = re.match(r"^(.*?)[\s.·•,-]*(\d{1,3})\s*$", l)
        if m and len(m.group(1)) > 3:
            out.append(((attente + " " + m.group(1)).strip(), int(m.group(2))))
            attente = ""
        elif re.match(r"^\d{1,3}$", l):
            continue
        else:
            attente = (attente + " " + l).strip()
    return eclater(out)


# début d'une entrée de table : un jour de la semaine (avec les coquilles de l'OCR), un dimanche numéroté, une date
DEBUT = re.compile(
    r"(?:(?<=\s)|^)(?:\.\s*)?(?:O\s+)?("
    r"(?:Premier|Deuxième|Second|Troisième|Quatrième|Cinquième|Sixième|Septième|Huitième|Neuvième|Dixième|Onzième|Douzième|"
    r"Treizième|Quatorzième|Quinzième|Seizième|Dix\s*-\s*\w+|Vingt[\w -]*?)\s+Dim\s*anche"
    r"|(?:Lundi|Landi|Mardi|Marci|Dlardi|Mercredi|Vercredi|Jeudi|Vendredi|Samedi)\b(?!\s+saint\s+jour)"
    r"|\d{1,2}(?:er)?\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre)\b"
    r"|La\s+Septuagésime|Sexagésime|Quinquagésime|Dimanche\s+d[eu]s?\s+\w+"
    r")", re.I)


def eclater(entrees: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Sépare deux entrées collées sur une ligne (« Mercredi. Sa Vie de victime. Jeudi. Sa Vie de mérites 76 »)."""
    out: list[tuple[str, int]] = []
    for lib, p in entrees:
        lib = re.sub(r"^.*?(?=Premier Dimanche de l'Avent)", "", lib)  # préface et prières en tête du tome I
        lib = re.sub(r"^SAINTS DONT LES FÊTES.*?LITURGIE\s*\.?\s*", "", lib)
        coupes = [m.start(1) for m in DEBUT.finditer(lib)]
        # une coupe commence par une capitale ou un chiffre (« de la Septuagésime » n'est pas une entrée)
        coupes = [c for c in coupes if c == 0 or (lib[c - 1] in " .—-–•·" and (lib[c].isupper() or lib[c].isdigit()))] or [0]
        if coupes[0] != 0:
            coupes = [0] + coupes
        morceaux = [lib[a:b] for a, b in zip(coupes, coupes[1:] + [len(lib)])]
        for k, m in enumerate(morceaux):
            m = m.strip(" .")
            pm = re.search(r"\s(\d{1,3})\s*$", m) if k < len(morceaux) - 1 else None
            if pm:
                out.append((m[: pm.start()].strip(" ."), int(pm.group(1))))
            else:
                out.append((m, p if k == len(morceaux) - 1 else 0))
    return [(l, p) for l, p in out if l]


MARQUE = re.compile(r"SOMMAIRE\s+[PF]OUR\s*[.']*\s*(?:LA\s+)?V[EÉ]?I?LL?E\s+AU\s+SOIR|SOMMAIRE\s+POUR\s*$", re.M)


def pages_livre(pages: list[str]) -> list[int]:
    """Numéro de page imprimé de chaque page du PDF (en-tête courant), complété par le décalage dominant."""
    vus = []
    for k, pg in enumerate(pages):
        ls = [l.strip() for l in pg.splitlines() if l.strip()]
        n = None
        if ls:
            m = re.match(r"^(\d{1,3})\s", ls[0]) or re.search(r"\s(\d{1,3})$", ls[0])
            n = int(m.group(1)) if m else None
        vus.append(n)
    out = []
    for k in range(len(pages)):
        # décalage local : le plus fréquent dans une fenêtre de 15 pages
        fen = [j - vus[j] for j in range(max(0, k - 7), min(len(pages), k + 8)) if vus[j]]
        dec = max(set(fen), key=fen.count) if fen else 0
        out.append(k - dec)
    return out


def entete(ligne: str) -> bool:
    l = ligne.strip()
    return bool(re.match(r"^\d{1,3}\s+\S", l) and l.upper() == l) or bool(re.search(r"\S\s+\d{1,3}$", l) and l.upper() == l)


NOTE = re.compile(r"^\s*[\d*•°'\"«»¹²³⁴⁵⁶⁷⁸⁹]{1,3}\s*\S")
REF = re.compile(r"\(\s*[A-ZÉ][\w.]*\s*[.,]?.*\d.*\)\s*\.?\s*\d?$")


def nettoyer_page(pg: str) -> str:
    """Retire l'en-tête courant et les notes de bas de page (lignes de références en fin de page)."""
    ls = pg.splitlines()
    # en-tête courant : lignes de tête vides, en capitales (titre courant) ou réduites au numéro de page
    for _ in range(4):
        while ls and not ls[0].strip():
            ls.pop(0)
        if ls and (re.fullmatch(r"\s*\d{1,3}\s*", ls[0]) or (ls[0].strip().upper() == ls[0].strip() and len(ls[0].strip()) < 80
                                                           and re.search(r"[A-Z]{3}", ls[0]) and not MARQUE.search(ls[0])
                                                           and not re.match(r"\s*(PREMIER|SECOND|DEUXI|TROISI|QUATRI|M[EÉ]DITATION|R[EÉ]SOLUTION)", ls[0]))):
            ls.pop(0)
        else:
            break
    # notes de bas de page : lignes finales portant une référence entre parenthèses (« (Luc., I, 47.) »)
    while ls and (not ls[-1].strip() or NOTE_REF.search(ls[-1])):
        ls.pop()
    return "\n".join(ls)


NOTE_REF = re.compile(r"\(\s*[A-ZÉ][\w.]*\s*[.,]?[^()]*(?:\d|[IVXLC]{2,})[^()]*\)?\s*\.?\s*\d?\s*$")


def traits(t: str) -> str:
    """« Jésus - Christ », « ici -bas », « Notre - Seigneur » → mots composés recollés."""
    return re.sub(r"(?<=[A-Za-zÀ-ÿ])[ \t]*-[ \t]*(?=(?:Christ|Seigneur|Dame|Esprit|bas|haut|même|mêmes|là|ci|il|elle|ils|elles|on|nous|vous|je|tu|moi|toi|lui|leur|y|en|le|la|les|t-il|t-elle)\b)", "-", t)


def recoller(t: str) -> str:
    """Recolle les mots coupés en fin de ligne et les lignes d'un même paragraphe ; garde les intertitres."""
    t = re.sub(r"(\w)[-¬]\s*\n\s*([a-zàâçéèêëîïôûùüœ])", r"\1\2", t)
    t = traits(t)
    paras = [p.strip() for p in re.split(r"\n\s*\n", t)]
    out = []
    for p in paras:
        if not p:
            continue
        p = re.sub(r"\s*\n\s*", " ", p)
        p = re.sub(r"\s{2,}", " ", p)
        p = re.sub(r"\s+([,.;:!?»)])", lambda m: m.group(1) if m.group(1) in ",.)" else " " + m.group(1), p)
        out.append(p)
    # un paragraphe qui ne finit pas une phrase et le suivant qui commence en minuscule : même paragraphe
    fus: list[str] = []
    for p in out:
        if fus and not re.search(r"[.!?»:…]$", fus[-1]) and re.match(r"^[a-zàâçéèêîôûœ,;]", p):
            fus[-1] += " " + p
        else:
            fus.append(p)
    return "\n\n".join(fus)


INTERTITRES = [
    (r"M[EÉ]DITATION\s+POUR\s+LE\s+MATIN", "## Méditation pour le matin"),
    (r"PREMIER\s+POINT\s*\.?", "## Premier point"),
    (r"(?:SECOND|DEUXI[EÈ]ME)\s+POINT\s*\.?", "## Second point"),
    (r"TROISI[EÈ]ME\s+POINT\s*\.?", "## Troisième point"),
    (r"QUATRI[EÈ]ME\s+POINT\s*\.?", "## Quatrième point"),
    (r"R[EÉ]SOLUTIONS?\s+ET\s+BOUQUET\s+SPIRITUEL\s*\.?", "## Résolutions et bouquet spirituel"),
]


def baliser(t: str) -> str:
    for motif, titre in INTERTITRES:
        t = re.sub(r"(?m)^\s*" + motif + r"\s*$", "\n\n" + titre + "\n\n", t)
    return t


def _jour(mot: str) -> int | None:
    import difflib
    m = difflib.get_close_matches(mot, list(JOURS), n=1, cutoff=0.6)
    return JOURS[m[0]] if m else None


def cle(lib: str, ctx: dict) -> str | None:
    """Clé d'une entrée de table : T:<temporal> (Adv1-0, Pent05-3…), D:<MM-JJ> (date fixe), F:<fête mobile>, O:<dimanche d'octobre>."""
    l = re.sub(r"^(?:[^\wÀ-ÿ]+|o\s+)+", "", lib.lower().replace("’", "'"))
    l = re.sub(r"\s+", " ", l).replace("dim anche", "dimanche").replace("for ", "1er ")
    m = re.match(r"(\d{1,2})(?:er)?\s+(\w+)", l)
    if m and m.group(2) in MOIS:
        ctx["date"] = f"D:{MOIS[m.group(2)]:02d}-{int(m.group(1)):02d}"
        return ctx["date"]
    if re.match(r"(deuxième|troisième|quatrième) méditation", l) and ctx.get("date"):
        return ctx["date"]  # suite des méditations d'une même fête
    if re.match(r"pentecôte\s*[.—–-]", l) and ctx.get("temps") == "Pent":
        ctx["sem"] = ctx.get("sem", 1) + 1  # dimanche dont l'intitulé a été coupé par un en-tête de page
        return _k(ctx, 0)
    if l.startswith("sacré-c"):
        ctx["date"] = "F:sacre-coeur"
        return ctx["date"]
    if "septuagésime" in l[:20]:
        ctx.update(temps="Quadp", sem=1); return "T:Quadp1-0"
    if l.startswith("sexagésime"):
        ctx.update(temps="Quadp", sem=2); return "T:Quadp2-0"
    if l.startswith("quinquagésime"):
        ctx.update(temps="Quadp", sem=3); return "T:Quadp3-0"
    if l.startswith("mercredi des cendres"):
        return "T:Quadp3-3"
    if "dimanche de la passion" in l[:30]:
        ctx.update(temps="Quad", sem=5); return "T:Quad5-0"
    if "rameaux" in l[:30]:
        ctx.update(temps="Quad", sem=6); return "T:Quad6-0"
    if re.match(r"(saint )?jour de pâques", l):
        ctx.update(temps="Pasc", sem=0); return "T:Pasc0-0"
    if "quasimodo" in l[:30]:
        ctx.update(temps="Pasc", sem=1); return "T:Pasc1-0"
    if re.match(r"ascension\b", l):
        return "T:Pasc5-4"
    if "octave de l'ascension" in l[:50]:
        ctx.update(temps="Pasc", sem=6); return "T:Pasc6-0"
    if re.match(r"(saint jour de (la )?)?pentecôte\b", l):
        ctx.update(temps="Pasc", sem=7); return "T:Pasc7-0"
    if re.match(r"(dimanche de la )?trinité\b", l):
        ctx.update(temps="Pent", sem=1); return "T:Pent01-0"
    if l.startswith("fête-dieu") or l.startswith("fête du saint sacrement"):
        return "T:Pent01-4"
    m = re.match(r"([\w -]+?)\s+dimanche(.*)", l)
    ordinal = None
    if m:
        o = re.sub(r"\s*-\s*", "-", m.group(1).strip())
        proche = difflib.get_close_matches(o, list(ORD), n=1, cutoff=0.8)
        ordinal = ORD.get(o) or (ORD[proche[0]] if proche else None)
    if m and ordinal:
        n, reste = ordinal, m.group(2)
        if "octobre" in reste:
            ctx.update(temps="Oct")
        elif "avent" in reste: ctx.update(temps="Adv")
        elif "épiphanie" in reste: ctx.update(temps="Epi")
        elif "carême" in reste: ctx.update(temps="Quad")
        elif "pâques" in reste: ctx.update(temps="Pasc")
        elif "pentecôte" in reste or "pentecôie" in reste: ctx.update(temps="Pent")
        ctx["sem"] = n
        if ctx["temps"] == "Oct":
            return f"O:10-{n}"
        return _k(ctx, 0)
    j = _jour(re.split(r"[\s.,;:'-]+", l)[0])
    if j is not None and ctx.get("temps") and ctx["temps"] != "Oct":
        return _k(ctx, j)
    return None


def _k(ctx: dict, j: int) -> str:
    t, s = ctx["temps"], ctx.get("sem", 1)
    return f"T:{t}{s:02d}-{j}" if t == "Pent" else f"T:{t}{s}-{j}"


def sujet_de(lib: str) -> str:
    """« Vendredi. — Règne de Jésus-Christ en nous » → « Règne de Jésus-Christ en nous »."""
    if not lib:
        return ""
    s = re.sub(r"^.*?(?:Dimanche[^.—–]*|\d{1,2}(?:er)?\s+\w+|Lundi|Landi|Mardi|Marci|Dlardi|Mercredi|Vercredi|Jeudi|Vendredi|Samedi)\s*[.,]?\s*[-—–·•C]*\s*", "", lib, count=1)
    return s.strip(" .-—–·•") or lib


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.upper())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Z ]+", " ", s).strip()


def norm_chiffres(s: str) -> str:
    s = unicodedata.normalize("NFD", s.upper())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Z0-9 ]+", " ", s)


def tome(n: int) -> list[dict]:
    brut = texte(n, False)
    pages = brut.split("\f")
    pl = pages_livre(pages)
    # position (page du PDF) de chaque début de méditation
    debuts = []
    for k, pg in enumerate(pages):
        for m in MARQUE.finditer(pg):
            debuts.append((k, m.start()))
    toc = table(n)
    # remplit les pages manquantes de la table par la précédente
    for i, (l, p) in enumerate(toc):
        if not p and i:
            toc[i] = (l, toc[i - 1][1])
    ctx: dict = {1: {"temps": "Adv", "sem": 1}, 2: {"temps": "Quad", "sem": 5}, 3: {"temps": "Pent", "sem": 8}}[n]
    toc_k = [(l, p, cle(l, ctx)) for l, p in toc]
    # entrées de table qui sont des méditations (avec une clé ou un sujet), et leur sujet normalisé
    sujets = [norm(sujet_de(l)) for l, p, c in toc_k]
    # score de ressemblance entre chaque début de méditation et chaque entrée de table :
    # sujet comparé aux en-têtes courants des pages (qui le reprennent), plus un bonus si la page imprimée concorde
    def entetes_de(i: int) -> list[str]:
        k, pos = debuts[i]
        k2 = debuts[i + 1][0] if i + 1 < len(debuts) else min(len(pages) - 1, k + 4)
        out_ = []
        for kk in range(k, min(k2, k + 3) + 1):
            ls = [x.strip() for x in pages[kk].splitlines() if x.strip()]
            out_ += [norm(x) for x in ls[:2] if x.upper() == x]
        out_ += [norm(x) for x in pages[k][:pos].splitlines()[-3:] if x.strip()]
        return [e for e in out_ if e]

    ent = [entetes_de(i) for i in range(len(debuts))]
    NI, NJ = len(debuts), len(toc_k)

    def score(i: int, j: int) -> float:
        s = max((difflib.SequenceMatcher(None, sujets[j], e).ratio() for e in ent[i]), default=0) if sujets[j] else 0
        if abs(pl[debuts[i][0]] - toc_k[j][1]) <= 2:
            s += 0.3
        return s

    # alignement global (programmation dynamique) : apparier dans l'ordre, sauter au besoin d'un côté ou de l'autre
    SAUT = 0.15
    V = [[0.0] * (NJ + 1) for _ in range(NI + 1)]
    C = [[""] * (NJ + 1) for _ in range(NI + 1)]
    for i in range(1, NI + 1):
        C[i][0] = "i"
    for j in range(1, NJ + 1):
        C[0][j] = "j"
    for i in range(1, NI + 1):
        for j in range(1, NJ + 1):
            choix = [(V[i - 1][j - 1] + score(i - 1, j - 1) - 0.35, "d"), (V[i - 1][j] - SAUT, "i"), (V[i][j - 1] - SAUT, "j")]
            V[i][j], C[i][j] = max(choix)
    paire: dict[int, int] = {}
    i, j = NI, NJ
    while i > 0 or j > 0:
        c = C[i][j]
        if c == "d":
            paire[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif c == "i":
            i -= 1
        else:
            j -= 1

    out = []
    for i, (k, pos) in enumerate(debuts):
        P = pl[k]
        j = paire.get(i)
        # texte : de ce début au suivant
        k2, pos2 = debuts[i + 1] if i + 1 < len(debuts) else (len(pages) - 1, None)
        morceaux = []
        for kk in range(k, k2 + 1):
            pg = pages[kk]
            a = pos if kk == k else 0
            b = pos2 if (kk == k2 and pos2 is not None) else len(pg)
            if kk == k2 and pos2 is not None:
                # s'arrêter avant l'intitulé du jour suivant (lignes en capitales juste avant la marque)
                avant = pg[:b].rstrip().splitlines()
                while avant and (not avant[-1].strip() or avant[-1].strip().upper() == avant[-1].strip()):
                    avant.pop()
                b = len("\n".join(avant))
            morceaux.append(nettoyer_page(pg[a:b]) if kk != k else pg[a:b] if False else nettoyer_page(pg[a:b]))
        t = "\n\n".join(morceaux)
        t = re.sub(r"^.*?\n", "", t, count=1)  # la ligne « SOMMAIRE POUR LA VEILLE AU SOIR »
        corps = recoller(baliser(t))
        sommaire, _, reste = corps.partition("## Méditation pour le matin")
        lib, p, c = toc_k[j] if j is not None else ("", P, None)
        # la date imprimée dans l'intitulé, juste avant le sommaire (« 3 NOVEMBRE »), fait foi
        tete = norm_chiffres(" ".join(pages[k][:pos].splitlines()[-4:]))
        md = re.search(r"\b(\d{1,2})\s*(?:ER)?\s+(" + "|".join(norm(m) for m in MOIS) + r")\b", tete)
        if md:
            mois = {norm(m): v for m, v in MOIS.items()}[md.group(2)]
            c = f"D:{mois:02d}-{int(md.group(1)):02d}"
            if not lib or not lib.startswith(md.group(1)):
                # l'entrée de table appariée ne correspond pas : on garde le titre imprimé
                lib = " ".join(x.strip() for x in pages[k][:pos].splitlines()[-3:] if x.strip())
        else:
            tete_n = norm(" ".join(pages[k][:pos].splitlines()[-4:]))
            # « DIX-HUITIÈME LUNDI APRÈS LA PENTECÔTE », « MERCREDI DE LA PASSION » : l'intitulé imprimé fait foi
            mp = re.search(r"((?:DIX|VINGT(?: ET)?)?\s*[A-Z]*IEME|PREMIER)\s+(DIMANCHE|LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMEDI)\s+APRES\s+LA\s+PENTECOTE", tete_n)
            if mp:
                o = mp.group(1).lower().replace(" ", "").replace("-", "").replace("ieme", "ième")
                o = difflib.get_close_matches(o, [x.replace(" ", "").replace("-", "") for x in ORD], n=1, cutoff=0.8)
                if o:
                    nn = {x.replace(" ", "").replace("-", ""): v for x, v in ORD.items()}[o[0]]
                    c = f"T:Pent{nn:02d}-{JOURS[mp.group(2).lower()]}"
            mq = re.search(r"\b(LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMEDI)\s+DE\s+LA\s+PASSION", tete_n)
            if mq:
                c = f"T:Quad5-{JOURS[mq.group(1).lower()]}"
            if "DEDICACE" in tete_n:
                c = "F:dedicace"
            elif not c and re.search(r"(DEUXIEME|SECONDE|TROISIEME)\s+MEDITATION", tete_n) and out:
                c = out[-1]["cle"]
        sujet = traits(sujet_de(lib))
        out.append({"cle": c, "table": lib, "titre": sujet or lib, "tome": n, "page": p, "page_pdf": k + 1,
                    "sommaire": sommaire.strip(), "corps": ("## Méditation pour le matin" + reste).strip() if reste else corps})
    return out


EDITIONS = {
    1: "Paris, Victor Lecoffre ; Lyon, 1879 (10e éd.)",
    2: "Paris, Victor Lecoffre ; Lyon, 1894",
    3: "Paris, Victor Lecoffre ; Lyon",
}


def main(argv: list[str]) -> None:
    if argv and argv[0] == "table":
        for lib, p in table(int(argv[1])):
            print(p, "|", lib[:110])
        return
    entrees = []
    for n in (1, 2, 3):
        entrees += tome(n)
    # trou isolé entre deux jours du temporal : c'est le jour qui suit le précédent (ex. dimanche dont l'intitulé manque)
    for i, e in enumerate(entrees):
        if e["cle"] or not i:
            continue
        m = re.match(r"T:([A-Za-z]+)(\d+)-(\d)$", entrees[i - 1]["cle"] or "")
        if m:
            t, s, j = m.group(1), int(m.group(2)), int(m.group(3))
            s, j = (s + 1, 0) if j == 6 else (s, j + 1)
            e["cle"] = f"T:{t}{s:02d}-{j}" if t == "Pent" else f"T:{t}{s}-{j}"
    doc = {
        "id": "hamon",
        "titre": "Méditations à l’usage du clergé et des fidèles pour tous les jours de l’année",
        "auteur": "M. Hamon, curé de Saint-Sulpice",
        "editions": EDITIONS,
        "provenance": "Google Livres (PDF fournis par l’utilisateur) ; texte reconnu par OCR, coquilles possibles",
        "entrees": entrees,
    }
    dest = RACINE / "data" / "recueils" / "hamon.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    sans = [e for e in entrees if not e["cle"]]
    print(f"{len(entrees)} méditations ; {len(sans)} sans clé ; {dest}")


if __name__ == "__main__":
    main(sys.argv[1:])
