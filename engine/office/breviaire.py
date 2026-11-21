"""Bréviaire romain, heures complètes, rubriques d'avant 1955 (REFONTE § 5, lot 9).

    python3 engine/office/breviaire.py 2026            # année liturgique 2026-2027 (premier dimanche de l'Avent 2026)
    python3 engine/office/breviaire.py 2026 --jours 3  # essai sur les premiers jours

Méthode (écart avec REFONTE § 5.3, voir le document) : au lieu de réécrire en Python les rubriques de l'office, on
**exécute le moteur de Divinum Officium lui-même** (`web/cgi-bin/horas/officium.pl`, Perl, celui qui produit le site),
hors ligne, sur le dépôt épinglé (`vendor/do`), version « Divino Afflatu - 1954 », latin seul. Chaque heure de chaque
jour est convertie du HTML de DO vers le balisage de l'app (markup.ts : `### titre`, `[r]rubrique[/r]`, ℣, ℟), coupée en
paragraphes, et les paragraphes communs à plusieurs jours (psautier, ordinaire, hymnes) sont mis en commun.

Sorties (data/office/breviaire/<AAAA-AAAA>/) :
- `communs.json`  : { source, heures, paragraphes: [texte…] } — paragraphes présents au moins deux jours ;
- `MM-JJ.json`    : { date, office, heures: [[réf…] ×8], propres: [texte…] } — réf. >= 0 : paragraphe commun ;
                    réf. < 0 : propres[-réf - 1].
Garde-fous : la version choisie par DO est relue dans chaque page ; une heure vide, un renvoi DO non résolu
(« &psalm », « $Pater », « @Commune ») ou une page d'erreur arrête la génération.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DO = Path(os.environ.get("HEBDO_DO_DEPOT", ROOT / "vendor" / "do"))
CGI = DO / "web" / "cgi-bin" / "horas"
VERSION = "Divino Afflatu - 1954"
HEURES = [
    ("matines", "Matines", "Ad Matutinum", "Matutinum"),
    ("laudes", "Laudes", "Ad Laudes", "Laudes"),
    ("prime", "Prime", "Ad Primam", "Prima"),
    ("tierce", "Tierce", "Ad Tertiam", "Tertia"),
    ("sexte", "Sexte", "Ad Sextam", "Sexta"),
    ("none", "None", "Ad Nonam", "Nona"),
    ("vepres", "Vêpres", "Ad Vesperas", "Vesperae"),
    ("complies", "Complies", "Ad Completorium", "Completorium"),
]


def rendre_do(date: dt.date, heure: str) -> str:
    """HTML d'une heure, produit par le moteur de DO (le même que le site)."""
    q = f"date1={date:%m-%d-%Y}&command=pray{heure}&version={VERSION.replace(' ', '%20')}&lang2=Latin"
    r = subprocess.run(["perl", "officium.pl", q], cwd=CGI, capture_output=True, timeout=120)
    return r.stdout.decode("utf-8", "replace")


# ------------------------------------------------------------------ HTML de DO → balisage de l'app

TITRE = re.compile(r"<FONT SIZE='\+1' COLOR=\"red\"><B><I>(.*?)</I></B></FONT>", re.S)
INITIALE = re.compile(r"<FONT SIZE='\+2' COLOR=\"red\"><B><I>(.*?)</I></B></FONT>", re.S)
NUMERO = re.compile(r"<FONT SIZE='1' COLOR=\"red\">[^<]*</FONT>\s*")
NOTE_DO = re.compile(r"<FONT SIZE='-1'\s*>.*?</FONT>", re.S)
CROIX = re.compile(r"<span style='color:red; font-size:1\.25em'>(.*?)</span>")
ROUGE = re.compile(r"<FONT COLOR=\"red\"><I>(.*?)</I></FONT>", re.S)
ROUGE_SEUL = re.compile(r"<FONT COLOR=\"red\">(.*?)</FONT>", re.S)
VERSICULES = {"℣.", "℟.", "℣", "℟", "R.br.", "℟.br."}


def cellules(page: str) -> list[str]:
    """Le contenu des cellules de l'heure (une cellule = une partie de l'heure chez DO)."""
    corps = page.split("<TABLE BORDER='1'", 1)
    if len(corps) < 2:
        return []
    table = corps[1].split("</TABLE>", 1)[0]
    return re.findall(r"<TD VALIGN='TOP'[^>]*>(.*?)</TD>", table, re.S)


def en_balisage(cellule: str) -> str:
    # les retours à la ligne du HTML ne comptent pas : seuls <br/> coupent les lignes
    c = cellule.replace("\r", "").replace("\n", " ")
    c = re.sub(r"<DIV ALIGN='right'>.*?</DIV>", "", c, flags=re.S)
    # libellés des liens « Ante / Post Divinum officium » (prières facultatives repliées chez DO)
    c = re.sub(r"<FONT SIZE='1'>[^<]*</FONT>", "", c)
    c = NOTE_DO.sub("", c)
    c = NUMERO.sub("", c)

    def titre(m: re.Match) -> str:
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        suite = c[m.end() : m.end() + 1]
        # même balise chez DO pour la lettrine d'une strophe (« M » + « ens jam… ») : collée au mot qui suit
        if len(t) <= 2 and suite.isalpha():
            return t
        return "<br/>### " + t + "<br/>"

    c = TITRE.sub(titre, c)
    c = INITIALE.sub(lambda m: m.group(1), c)
    c = CROIX.sub(lambda m: m.group(1), c)

    def rouge(m: re.Match) -> str:
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if not t:
            return ""
        return t if t in VERSICULES else f"[r]{t}[/r]"

    c = ROUGE.sub(rouge, c)
    c = ROUGE_SEUL.sub(rouge, c)
    c = re.sub(r"<br\s*/?>", "\n", c, flags=re.I)
    c = re.sub(r"</?(?:p|div)[^>]*>", "\n", c, flags=re.I)
    c = re.sub(r"<[^>]+>", "", c)
    c = html.unescape(c).replace(" ", " ")
    lignes = [re.sub(r"[ \t]+", " ", l).strip() for l in c.split("\n")]
    out: list[str] = []
    for l in lignes:
        if l or (out and out[-1]):
            out.append(l)
    return "\n".join(out).strip()


COUPE = re.compile(r"^(?:### |\[r\](?:Ant\.|Psalmus|Canticum|Hymnus|Lectio|Responsorium|Absolutio|Benedictio|Capitulum|Oratio|Commemoratio|Versus|Preces|Te Deum|Martyrologium)\b)")


def paragraphes(texte: str) -> list[str]:
    """Coupe une partie de l'heure aux titres et aux rubriques qui ouvrent une pièce (antienne, psaume, leçon…)."""
    blocs: list[list[str]] = []
    for l in texte.split("\n"):
        if not blocs or (COUPE.match(l) and any(x.strip() for x in blocs[-1])):
            blocs.append([])
        blocs[-1].append(l)
    return [b for b in ("\n".join(x).strip() for x in blocs) if b]


RESTES_DO = re.compile(r"&psalm|&[a-zA-Z_]+\(|\$[A-Z][a-z]+ [a-z]|@[A-Z][a-z]+[:/]|\{:H-")


def heure(date: dt.date, cle_do: str) -> tuple[list[str], str]:
    page = rendre_do(date, cle_do)
    if f'<OPTION SELECTED VALUE="{VERSION}">' not in page:
        raise SystemExit(f"{date} {cle_do} : DO n'a pas pris la version « {VERSION} »")
    # le nom de l'office, au-dessus de l'heure (couleur liturgique en attribut, absente pour le blanc)
    titre = re.search(r"<P ALIGN=CENTER><FONT[^>]*>(.*?)</FONT>", page, re.S)
    office = html.unescape(re.sub(r"<[^>]+>", " ", titre.group(1))).split("~")[0].strip() if titre else ""
    office = re.sub(r"\s+", " ", office)
    ps: list[str] = []
    for c in cellules(page):
        ps.extend(paragraphes(en_balisage(c)))
    if not ps:
        raise SystemExit(f"{date} {cle_do} : heure vide")
    for p in ps:
        if RESTES_DO.search(p):
            raise SystemExit(f"{date} {cle_do} : renvoi DO non résolu : {p[:120]!r}")
    return ps, office


def jour(date: dt.date) -> dict:
    heures, office = [], ""
    for _, _, _, cle_do in HEURES:
        ps, o = heure(date, cle_do)
        heures.append(ps)
        office = office or o
    return {"date": date.isoformat(), "office": office, "heures": heures}


def premier_dimanche_avent(annee: int) -> dt.date:
    noel = dt.date(annee, 12, 25)
    dim_avant_noel = noel - dt.timedelta(days=(noel.weekday() + 1) % 7 or 7)
    return dim_avant_noel - dt.timedelta(weeks=3)


def depot() -> dict:
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=DO, capture_output=True, text=True).stdout.strip()
    return {
        "depot": "https://github.com/DivinumOfficium/divinum-officium",
        "commit": commit,
        "version": VERSION,
        "langue": "latin",
        "note": "Produit en exécutant hors ligne le moteur de Divinum Officium (web/cgi-bin/horas/officium.pl), le même que "
        "le site, sur le dépôt épinglé ; HTML converti au balisage de l'app sans changer le texte (numéros de versets et "
        "notes de source de DO retirés). Latin seul : aucune traduction française ancienne identifiée (REFONTE § 5.5).",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("annee", type=int, help="année du premier dimanche de l'Avent")
    ap.add_argument("--jours", type=int, default=0, help="essai : nombre de jours")
    ap.add_argument("--processus", type=int, default=4)
    a = ap.parse_args()
    debut = premier_dimanche_avent(a.annee)
    fin = premier_dimanche_avent(a.annee + 1) - dt.timedelta(days=1)
    dates = [debut + dt.timedelta(days=i) for i in range((fin - debut).days + 1)]
    if a.jours:
        dates = dates[: a.jours]
    with cf.ProcessPoolExecutor(a.processus) as ex:
        jours = list(ex.map(jour, dates, chunksize=4))

    # paragraphes communs : présents au moins deux jours
    vus: dict[str, set[str]] = {}
    for j in jours:
        for h in j["heures"]:
            for p in h:
                vus.setdefault(p, set()).add(j["date"])
    communs = sorted((p for p, d in vus.items() if len(d) >= 2), key=lambda p: (-len(vus[p]), p))
    index = {p: i for i, p in enumerate(communs)}

    sortie = ROOT / "data" / "office" / "breviaire" / f"{a.annee}-{a.annee + 1}"
    sortie.mkdir(parents=True, exist_ok=True)
    for f in sortie.glob("*.json"):
        f.unlink()
    (sortie / "communs.json").write_text(
        json.dumps(
            {
                "titre": "Breviarium Romanum (Divino afflatu, rubriques de 1954)",
                "source": depot(),
                "heures": [{"cle": c, "nom": n, "latin": l} for c, n, l, _ in HEURES],
                "jours": {"debut": dates[0].isoformat(), "fin": dates[-1].isoformat()},
                "paragraphes": communs,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    for j in jours:
        propres: list[str] = []
        refs = []
        for h in j["heures"]:
            r = []
            for p in h:
                if p in index:
                    r.append(index[p])
                else:
                    propres.append(p)
                    r.append(-len(propres))
            refs.append(r)
        (sortie / f"{j['date'][5:]}.json").write_text(
            json.dumps({"date": j["date"], "office": j["office"], "heures": refs, "propres": propres}, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
    taille = sum(f.stat().st_size for f in sortie.glob("*.json"))
    print(f"{len(jours)} jours, {len(communs)} paragraphes communs, {taille / 1e6:.1f} Mo dans {sortie.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
