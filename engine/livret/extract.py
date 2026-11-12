"""Extraction des textes du *Jardin de l'âme* (docs/livret/source/*.tex) vers data/prieres/jardin.json.

Le texte est repris tel quel (aucune réécriture) ; seule la mise en forme LaTeX est
convertie en un balisage léger : *italique*, retours à la ligne, ℣/℟.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "docs" / "livret" / "source"
OUT = ROOT / "data" / "prieres" / "jardin.json"


# ------------------------------------------------------------------ lecture LaTeX
def expand_inputs(text: str) -> str:
    def rep(m):
        return expand_inputs((SRC / f"{m.group(1)}.tex").read_text(encoding="utf-8"))
    return re.sub(r"\\input\{([^}]+)\}", rep, text)


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def read_group(s: str, i: int) -> tuple[str, int]:
    """Lit {…} à partir de s[i] == '{' ; renvoie (contenu, indice après)."""
    assert s[i] == "{", s[i:i + 30]
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError("accolade non fermée")


def read_opt(s: str, i: int) -> tuple[str | None, int]:
    if i < len(s) and s[i] == "[":
        j = s.index("]", i)
        return s[i + 1:j], j + 1
    return None, i


def skip_ws(s: str, i: int) -> int:
    while i < len(s) and s[i] in " \t":
        i += 1
    return i


# ------------------------------------------------------------------ conversion du texte
INLINE_1 = {  # macros à un argument converties en balisage léger
    "textit": "*{}*", "emph": "*{}*", "latin": "*{}*", "textsc": "{}", "petitescaps": "{}",
    "textbf": "{}", "textsuperscript": "{}", "mbox": "{}", "text": "{}", "textup": "{}",
    "textrm": "{}", "chiffresalignes": "{}",
}


def tex2txt(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z@]+)\*?", s[i:])
            if not m:
                nxt = s[i + 1] if i + 1 < len(s) else ""
                if nxt == "\\":
                    out.append("\n")
                    i += 2
                    _, i = read_opt(s, i)
                    continue
                out.append({",": "\u202f", " ": " ", "&": "&", "%": "%", "-": ""}.get(nxt, nxt))
                i += 2
                continue
            name = m.group(1)
            i += len(m.group(0))
            if name in INLINE_1:
                i = skip_ws(s, i)
                if i >= len(s) or s[i] != "{":
                    continue          # employé comme bascule de police
                arg, i = read_group(s, i)
                out.append(INLINE_1[name].format(tex2txt(arg)))
            elif name == "ouverture":
                a, i = read_group(s, i)
                b, i = read_group(s, i)
                c3, i = read_group(s, i)
                out.append(ouverture(a, b, c3))
            elif name == "V":
                out.append("℣. ")
            elif name == "R":
                out.append("℟. ")
            elif name in ("par", "newline"):
                out.append("\n")
            elif name in ("pageref", "ref", "label", "index"):
                arg, i = read_group(s, i)
                if name in ("pageref", "ref"):
                    out.append(f"[{arg}]")
            elif name == "ier":
                out.append("er")
            elif name in ("enspace", "quad", "qquad", "thinspace"):
                out.append(" ")
            elif name in ("ldots", "dots"):
                out.append("…")
            elif name in ("hspace", "vspace", "rule", "fontsize", "color", "selectfont", "noindent",
                          "nopagebreak", "needspace", "hfill", "raggedright", "centering", "itshape",
                          "scshape", "smallskip", "medskip", "bigskip", "leftskip", "parindent", "hangindent",
                          "ebgsymb", "addfontfeature", "titrefont", "culdelampe", "fleuron", "fleuronpetit", "priere", "relax"):
                # arguments éventuels
                i, _ = (read_opt(s, i)[1], None)
                while i < len(s) and s[i] == "{" and name in ("hspace", "vspace", "rule", "fontsize", "color", "needspace", "addfontfeature"):
                    _, i = read_group(s, i)
                if name in ("leftskip", "parindent", "hangindent"):
                    mm = re.match(r"=?-?[\d.]+\w+", s[i:])
                    if mm:
                        i += len(mm.group(0))
            else:
                out.append(f"\\{name}")
        elif c == "~":
            out.append("\u00a0")
            i += 1
        elif c in "{}":
            i += 1
        else:
            out.append(c)
            i += 1
    t = "".join(out)
    t = t.replace("---", "—").replace("--", "–")
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n[ \t]+", "\n", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()


def ouverture(a: str, b: str, c: str) -> str:
    """\\ouverture{M}{on}{Dieu,} → « Mon Dieu, » ; \\ouverture{Ô}{}{Jésus,} → « Ô Jésus, »."""
    if b:
        return f"{a}{b} {tex2txt(c)}"
    return f"{a} {tex2txt(c)}"


# ------------------------------------------------------------------ découpage en pièces
def slug(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60]


def toc_pages() -> dict[str, int]:
    pages = {}
    for m in re.finditer(r"\\contentsline \{section\}\{(.*?)\}\{(\d+)\}", (SRC / "recueil.toc").read_text(encoding="utf-8")):
        pages.setdefault(tex2txt(m.group(1)), int(m.group(2)))
    return pages


BLOCK_MACROS = {"rubrique": "rubrique", "invocation": "invocation", "conclusion": "conclusion",
                "traduction": "traduction", "intertitre": "intertitre"}


def parse() -> list[dict]:
    text = strip_comments(expand_inputs((SRC / "recueil.tex").read_text(encoding="utf-8")))
    start = text.index("\\partie{")
    # fin des textes : avant la table, le colophon et la mise en page finale
    ends = [k for k in (text.find("\\backmatter"), text.find("@starttoc"), text.find("\\colophon")) if k > start]
    body = text[start:min(ends) if ends else len(text)]
    body = body[:body.rfind("{", 0, body.find("@starttoc"))] if "@starttoc" in body else body
    pages = toc_pages()

    pieces: list[dict] = []
    partie = None
    jour = None
    cur: dict | None = None
    parent: dict | None = None
    para: list[str] = []
    order = 0
    fruit_label = "Fruit :"

    def flush_para():
        nonlocal para, fruit_label
        t = "".join(para).strip()
        para = []
        if not t or cur is None:
            return
        for chunk in re.split(r"\n\s*\n", t):
            txt = tex2txt(chunk)
            if txt:
                cur["blocs"].append({"type": "texte", "texte": txt})

    def new_piece(title: str, kind: str, short: str | None = None):
        nonlocal cur, parent, order
        flush_para()
        order += 1
        t = tex2txt(title)
        p = {"id": None, "ordre": order, "titre": t, "titre_court": tex2txt(short) if short else None,
             "type": kind, "partie": partie, "jour_de_semaine": jour,
             "page_livret": pages.get(t) or (pages.get(tex2txt(short)) if short else None),
             "usage": None, "indulgence": None, "source": None, "parent": None, "blocs": []}
        if kind == "sousacte" and parent is not None:
            p["parent"] = parent["id"]
        base = slug(t) or f"piece-{order}"
        ids = {x["id"] for x in pieces}
        pid = base
        k = 2
        while pid in ids:
            pid = f"{base}-{k}"
            k += 1
        p["id"] = pid
        pieces.append(p)
        cur = p
        if kind == "acte":
            parent = p

    i = 0
    n = len(body)
    while i < n:
        if body[i] == "\\":
            m = re.match(r"\\([A-Za-z]+)\*?", body[i:])
            if not m:
                para.append(body[i:i + 2])
                i += 2
                continue
            name = m.group(1)
            j = i + len(m.group(0))
            if name == "partie":
                a, j = read_group(body, j)
                b, j = read_group(body, j)
                _, j = read_group(body, j)
                flush_para()
                partie = {"numero": tex2txt(a), "titre": tex2txt(b)}
                jour = None
                cur = None
                parent = None
            elif name == "jour":
                a, j = read_group(body, j)
                flush_para()
                jour = tex2txt(a)
            elif name in ("acte", "acterecto", "acteverso"):
                opt, j = read_opt(body, j)
                a, j = read_group(body, j)
                new_piece(a, "acte", opt)
            elif name == "sousacte":
                a, j = read_group(body, j)
                new_piece(a, "sousacte")
            elif name in ("usage", "indulg", "source"):
                a, j = read_group(body, j)
                flush_para()
                key = {"usage": "usage", "indulg": "indulgence", "source": "source"}[name]
                if cur is not None:
                    val = tex2txt(a)
                    cur[key] = val if cur[key] is None else cur[key] + " — " + val
            elif name in BLOCK_MACROS:
                a, j = read_group(body, j)
                flush_para()
                if cur is not None:
                    cur["blocs"].append({"type": BLOCK_MACROS[name], "texte": tex2txt(a)})
            elif name == "vr":
                a, j = read_group(body, j)
                b, j = read_group(body, j)
                flush_para()
                if cur is not None:
                    cur["blocs"].append({"type": "verset", "v": tex2txt(a), "r": tex2txt(b)})
            elif name in ("strophe", "strophew"):
                a, j = read_group(body, j)
                b, j = read_group(body, j)
                flush_para()
                if cur is not None:
                    cur["blocs"].append({"type": "strophe", "la": tex2txt(a), "fr": tex2txt(b)})
            elif name == "renewcommand":
                a, j = read_group(body, j)
                b, j = read_group(body, j)
                if a.strip() == "\fruitlabel":
                    fruit_label = tex2txt(b)
            elif name == "mystere":
                a, j = read_group(body, j)
                b, j = read_group(body, j)
                c, j = read_group(body, j)
                flush_para()
                if cur is not None:
                    cur["blocs"].append({"type": "mystere", "numero": tex2txt(a), "texte": tex2txt(b), "fruit_libelle": fruit_label, "fruit": tex2txt(c)})
            elif name == "salut":
                a, j = read_group(body, j)
                b, j = read_group(body, j)
                flush_para()
                if cur is not None:
                    cur["blocs"].append({"type": "numero", "numero": tex2txt(a), "texte": tex2txt(b)})
            elif name == "fiche":
                a, j = read_group(body, j)
                b, j = read_group(body, j)
                c, j = read_group(body, j)
                flush_para()
                if cur is not None:
                    cur["blocs"].append({"type": "fiche", "titre": tex2txt(a), "texte": tex2txt(b), "note": tex2txt(c)})
            elif name == "ouverture":
                a, j = read_group(body, j)
                b, j = read_group(body, j)
                c, j = read_group(body, j)
                para.append("\x00OUV" + json.dumps([a, b, c]) + "\x00")
            elif name == "begin":
                env, j = read_group(body, j)
                endtag = f"\\end{{{env}}}"
                k = body.index(endtag, j)
                inner = body[j:k]
                j = k + len(endtag)
                flush_para()
                if cur is None and env == "notice":
                    # notice d'ouverture de partie
                    if partie is not None:
                        partie.setdefault("notice", tex2txt(inner))
                elif env == "litanie":
                    items = [tex2txt(x) for x in re.split(r"\\item\s*", inner) if x.strip()]
                    cur["blocs"].append({"type": "litanie", "items": items})
                elif env == "notice":
                    cur["blocs"].append({"type": "notice", "texte": tex2txt(inner)})
                else:
                    cur["blocs"].append({"type": env, "texte": tex2txt(inner)})
            elif name in ("culdelampe", "fleuron", "fleuronpetit", "clearpage", "versgauche", "versdroite",
                          "mainmatter", "backmatter", "tableofcontents", "newpage", "filetdouble"):
                _, j = read_opt(body, j)
                flush_para()
            elif name == "priere":
                flush_para()
            else:
                para.append(m.group(0))
            i = j
        else:
            para.append(body[i])
            i += 1
    flush_para()

    # restaure les lettrines (\ouverture) en texte simple
    def fix(t: str) -> str:
        return re.sub("\x00OUV(.*?)\x00", lambda m: ouverture(*json.loads(m.group(1))), t)

    for p in pieces:
        # blocs résiduels de mise en page (commandes seules, sans texte)
        p["blocs"] = [b for b in p["blocs"]
                      if not (b["type"] == "texte" and not re.sub(r"\\[A-Za-z@]+|\s", "", b["texte"]))]
        for b in p["blocs"]:
            for k, v in list(b.items()):
                if isinstance(v, str):
                    b[k] = fix(v)
    return pieces


def main():
    pieces = parse()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = {"ouvrage": "Le Jardin de l’âme — Offrandes, couronnes et oraisons pour chaque jour",
           "edition": "livret 11 × 17 cm, 84 p., version validée (docs/livret)",
           "note": "Textes repris mot pour mot des sources LaTeX du livret ; chaque pièce garde sa ligne « source » telle qu’imprimée.",
           "pieces": pieces}
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"{len(pieces)} pièces → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
