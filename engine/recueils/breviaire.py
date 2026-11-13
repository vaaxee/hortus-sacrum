"""Leçons du IIe nocturne (Bréviaire romain, Divino Afflatu) pour le sanctoral, en latin et en français.

Entrée : vendor/do/web/www/horas/{Latin,Francais}/Sancti/*.txt (données Divinum Officium, déjà utilisées pour le
calendrier). Sortie : data/recueils/breviaire.json — une entrée par office : clé « O:Sancti/MM-JJ… » (le fichier
de l'office, comme dans le calendrier), titre latin et français, leçons IV, V, VI.

Seules les leçons IV à VI sont prises ; la leçon « 94 » (abrégé de 1960) est écartée.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
HORAS = RACINE / "vendor" / "do" / "web" / "www" / "horas"


def sections(chemin: Path) -> dict[str, str]:
    if not chemin.exists():
        return {}
    out: dict[str, str] = {}
    cle = None
    for l in chemin.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\[([^\]]+)\]\s*$", l)
        if m:
            cle = m.group(1)
            out[cle] = ""
        elif cle is not None:
            out[cle] += l + "\n"
    return out


def lire(langue: str, fichier: str, section: str, profondeur: int = 0) -> str:
    """Texte d'une section, en suivant les renvois « @Fichier:Section »."""
    if profondeur > 4:
        return ""
    s = sections(HORAS / langue / f"{fichier}.txt")
    t = s.get(section, "")
    if not t and profondeur == 0:
        # fichier entier renvoyé ailleurs (« @Sancti/12-25 » en tête)
        tete = (HORAS / langue / f"{fichier}.txt")
        if tete.exists():
            m = re.match(r"\s*@([\w/-]+)\s*$", tete.read_text(encoding="utf-8").splitlines()[0] if tete.read_text(encoding="utf-8") else "")
            if m:
                return lire(langue, m.group(1), section, profondeur + 1)
    m = re.match(r"\s*@([\w/-]+)?(?::([\w ]+?))?(?:\s+in\s+\d+\s+loco)?\s*$", t.strip()) if t.strip().startswith("@") else None
    if m:
        return lire(langue, m.group(1) or fichier, (m.group(2) or section).strip(), profondeur + 1)
    return t


def propre(t: str) -> str:
    lignes = []
    for l in t.splitlines():
        s = l.strip()
        if not s or s == "_" or s.startswith(("&", "$", "#", "(", "@")):
            continue
        if s.startswith("!"):
            lignes.append(f"[r]{s[1:].strip()}[/r]")
            continue
        s = re.sub(r"^v\.\s*", "", s)
        lignes.append(s)
    return "\n\n".join(lignes)


def main() -> None:
    entrees = []
    for f in sorted((HORAS / "Latin" / "Sancti").glob("*.txt")):
        nom = f.stem
        fichier = f"Sancti/{nom}"
        la = [propre(lire("Latin", fichier, f"Lectio{i}")) for i in (4, 5, 6)]
        fr = [propre(lire("Francais", fichier, f"Lectio{i}")) for i in (4, 5, 6)]
        if not any(la):
            continue
        titre_la = (sections(f).get("Officium") or "").strip()
        titre_fr = (sections(HORAS / "Francais" / "Sancti" / f.name).get("Officium") or "").strip()
        corps = "\n\n".join(f"## Leçon {r}\n\n{t}" for r, t in zip(("IV", "V", "VI"), fr) if t) if any(fr) else ""
        latin = "\n\n".join(f"## Lectio {r}\n\n{t}" for r, t in zip(("IV", "V", "VI"), la) if t)
        entrees.append({"cle": f"O:{fichier}", "titre": titre_fr or titre_la, "titre_la": titre_la, "tome": 0, "page": 0,
                        "corps": corps or latin, "latin": latin if corps else ""})
    doc = {
        "id": "breviaire",
        "titre": "Bréviaire romain — leçons du IIe nocturne",
        "auteur": "Breviarium Romanum (rubriques de 1911, Divino Afflatu)",
        "editions": {"0": "texte latin et traduction française des données Divinum Officium"},
        "provenance": "github.com/DivinumOfficium/divinum-officium, horas/Latin et horas/Francais, Sancti",
        "entrees": entrees,
    }
    dest = RACINE / "data" / "recueils" / "breviaire.json"
    dest.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(entrees)} offices avec leçons ; {sum(1 for e in entrees if e['latin'])} avec traduction française ; {dest}")


if __name__ == "__main__":
    main()
