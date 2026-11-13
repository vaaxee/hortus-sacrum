"""Recueils des mois de dévotion, découpés par jour du mois.

Sources (archive.org) :
- mars : Lefebvre, S. J., Mois de saint Joseph (1890) — moisdesaintjosep00lefe
- mai : Lefebvre, S. J., Mois de Marie, contemplations sur trente mystères (1888) — moisdemarieconte00lefe
- juin : Lefebvre, S. J., Mois du Sacré-Cœur (1869) — moisdusacrecoeur00lefe
- juillet : Boylesve, S. J., Le mois du Précieux Sang (1882) — cihm_46390
- novembre : Berlioux, Mois des âmes du purgatoire (1888) — moisdesamesdupur00berl

Méthode : chaque page porte en en-tête le jour en cours (« 24 PREMIER JOUR. ») et chaque jour commence par
« PREMIER JOUR ». On repère toutes ces lignes, on lit l'ordinal (avec tolérance pour l'OCR) et l'on coupe là où
le jour change.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
SRC = RACINE / "vendor" / "sources" / "mois"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hamon import recoller, traits  # noqa: E402
from gueranger import casse  # noqa: E402

UNITES = ["", "UN", "DEUX", "TROIS", "QUATRE", "CINQ", "SIX", "SEPT", "HUIT", "NEUF"]
ORD: dict[str, int] = {"PREMIER": 1, "UNIEME": 1}
_noms = {1: "PREMIER", 2: "DEUXIEME", 3: "TROISIEME", 4: "QUATRIEME", 5: "CINQUIEME", 6: "SIXIEME", 7: "SEPTIEME",
         8: "HUITIEME", 9: "NEUVIEME", 10: "DIXIEME", 11: "ONZIEME", 12: "DOUZIEME", 13: "TREIZIEME", 14: "QUATORZIEME",
         15: "QUINZIEME", 16: "SEIZIEME", 17: "DIXSEPTIEME", 18: "DIXHUITIEME", 19: "DIXNEUVIEME", 20: "VINGTIEME",
         21: "VINGTETUNIEME", 22: "VINGTDEUXIEME", 23: "VINGTTROISIEME", 24: "VINGTQUATRIEME", 25: "VINGTCINQUIEME",
         26: "VINGTSIXIEME", 27: "VINGTSEPTIEME", 28: "VINGTHUITIEME", 29: "VINGTNEUVIEME", 30: "TRENTIEME",
         31: "TRENTEETUNIEME"}
for n, s in _noms.items():
    ORD[s] = n
ORD["VINGTUNIEME"] = 21
ORD["TRENTEUNIEME"] = 31
ORD["SECOND"] = 2

RECUEILS = {
    "mois-joseph": ("moisdesaintjosep00lefe", 3, "Mois de saint Joseph, composé de trois neuvaines et un triduum", "R. P. Alexis Lefebvre, S. J.", "1890"),
    "mois-marie": ("moisdemarieconte00lefe", 5, "Mois de Marie : contemplations sur trente mystères de la vie de la très sainte Vierge", "R. P. Alexis Lefebvre, S. J.", "1888"),
    "mois-sacre-coeur": ("moisdusacrecoeur00lefe", 6, "Mois du Sacré-Cœur, composé de trois neuvaines et un triduum", "R. P. Alexis Lefebvre, S. J.", "1869"),
    "mois-purgatoire": ("moisdesamesdupur00berl", 11, "Mois des âmes du Purgatoire, ou Méditations pratiques pour chaque jour", "Abbé Martin Berlioux", "1888"),
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.upper())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Z0-9 ]+", " ", s)


JOUR = re.compile(r"^\s*(\d{1,3}\s+)?([A-Z][A-Z -]{3,24}?)\s+JOUR\s*(\d{1,3})?\s*$")


def ordinal(mot: str) -> int | None:
    m = re.sub(r"[^A-Z]", "", mot)
    if m in ORD:
        return ORD[m]
    p = difflib.get_close_matches(m, list(ORD), n=1, cutoff=0.75)
    return ORD[p[0]] if p else None


def parasite(l: str) -> bool:
    """Ligne courte de bruit d'OCR (« ^5)+G/A », « — 130 — »)."""
    s = l.strip()
    if not s:
        return False
    lettres = sum(c.isalpha() for c in s)
    return (len(s) < 20 and lettres < 0.6 * len(s)) or bool(re.fullmatch(r"[—–-]\s*\d{1,3}\s*[—–-]", s))


def decouper(ident: str) -> list[dict]:
    t = (SRC / f"{ident}.txt").read_text(encoding="utf-8")
    L = t.splitlines()
    marques: list[tuple[int, int, bool]] = []  # (ligne, jour, intitulé ? — sinon en-tête courant)
    for i, l in enumerate(L):
        m = JOUR.match(norm(l).strip())
        if not m:
            continue
        n = ordinal(m.group(2))
        if n:
            marques.append((i, n, not (m.group(1) or m.group(3))))
    # premier repère de chaque jour, dans l'ordre (on ignore les retours en arrière dus à l'OCR)
    debuts: dict[int, int] = {}
    dernier = 0
    for i, n, intitule in marques:
        if n not in debuts and n >= dernier and n <= dernier + 2:
            debuts[n] = i
            dernier = n
    out = []
    jours = sorted(debuts)
    for k, n in enumerate(jours):
        a = debuts[n]
        b = debuts[jours[k + 1]] if k + 1 < len(jours) else len(L)
        bloc = L[a + 1:b]
        # en-têtes courants : « 24 PREMIER JOUR. », numéros de page isolés
        bloc = [l for l in bloc if not JOUR.match(norm(l).strip()) and not re.fullmatch(r"\s*\d{1,3}\s*", l) and not parasite(l)]
        corps = recoller(traits("\n".join(bloc)))
        if k == len(jours) - 1:
            # dernier jour : s'arrêter avant les annexes (recueil de prières, offices, messe des morts…)
            ps = corps.split("\n\n")
            fin = next((i for i, p in enumerate(ps) if re.search(r"FIN DU MOIS|RECUEIL DE PRI|DEUXI[EÈ]ME PARTIE|M?ESSE DES MORTS|^M\.M\.M", p)), len(ps))
            corps = "\n\n".join(ps[:fin])
        if len(corps) < 500:
            continue
        titre_l = next((x.strip() for x in bloc[:12] if re.fullmatch(r"[A-ZÀ-ÝŒ' ,.;:—–-]{6,}", x.strip())), "")
        out.append({"cle": f"J:{n}", "titre": f"{_titre_jour(n)} jour" + (f" — {casse(re.sub(r'[ 	]+', ' ', titre_l).strip(' .'))[:80]}" if titre_l else ""),
                    "tome": 1, "page": 0, "corps": corps})
    return out


def _titre_jour(n: int) -> str:
    return {1: "Premier", 2: "Deuxième", 3: "Troisième", 4: "Quatrième", 5: "Cinquième", 6: "Sixième", 7: "Septième",
            8: "Huitième", 9: "Neuvième", 10: "Dixième", 11: "Onzième", 12: "Douzième", 13: "Treizième",
            14: "Quatorzième", 15: "Quinzième", 16: "Seizième", 17: "Dix-septième", 18: "Dix-huitième",
            19: "Dix-neuvième", 20: "Vingtième", 21: "Vingt et unième", 22: "Vingt-deuxième", 23: "Vingt-troisième",
            24: "Vingt-quatrième", 25: "Vingt-cinquième", 26: "Vingt-sixième", 27: "Vingt-septième",
            28: "Vingt-huitième", 29: "Vingt-neuvième", 30: "Trentième", 31: "Trente et unième"}[n]


def main() -> None:
    dest = RACINE / "data" / "recueils"
    for rid, (ident, mois, titre, auteur, an) in RECUEILS.items():
        ent = decouper(ident)
        doc = {"id": rid, "mois": mois, "titre": titre, "auteur": auteur, "editions": {"1": an},
               "provenance": f"archive.org, {ident} ; texte reconnu par OCR, coquilles possibles", "entrees": ent}
        (dest / f"{rid}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        print(rid, len(ent), "jours :", [int(e["cle"][2:]) for e in ent], [len(e["corps"]) // 1000 for e in ent])


if __name__ == "__main__":
    main()
