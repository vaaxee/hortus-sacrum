"""Chaignon relu : garde les coupures du découpage d'origine (fait sur l'OCR d'archive.org) et les reporte sur le
texte corrigé, page par page, grâce aux numéros de page imprimés dans les deux textes.

Usage : python3 reporter.py <dossier_ocr_origine> <dossier_texte_corrigé>
Chaque coupure d'origine est un numéro de ligne dans f<n>.txt d'origine ; on la convertit en (page, rang du mot dans la
page), puis on retrouve ce mot dans la même page du texte corrigé (alignement des mots de la page)."""
import difflib, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import chaignon

SRC0, SRC1 = Path(sys.argv[1]), Path(sys.argv[2])
RACINE = Path(__file__).resolve().parents[4]
key = lambda w: re.sub(r"[^\wÀ-ÿœæ]", "", w).lower()


def pages(t):
    """Le texte d'un tome, découpé en pages (séparées par le saut de page de djvu.txt, « \f », ou par nos doubles sauts)."""
    return t.split('\f') if '\f' in t else None


def main():
    entrees = []
    rang = {"parcours": 0, "liturgie": 0}
    for n in (1, 2, 3):
        chaignon.SRC = SRC0
        ent0 = chaignon.couper(n)
        t0 = (SRC0 / f"f{n}.txt").read_text(encoding="utf-8")
        t1 = (SRC1 / f"f{n}.txt").read_text(encoding="utf-8")
        # alignement global des mots des deux versions du tome
        w0 = t0.split(); w1 = t1.split()
        k0 = [key(w) for w in w0]; k1 = [key(w) for w in w1]
        sm = difflib.SequenceMatcher(None, k0, k1, autojunk=False)
        carte = {}
        for a, b, size in sm.get_matching_blocks():
            for i in range(size): carte[a + i] = b + i
        def vers1(i0):
            while i0 not in carte and i0 < len(w0): i0 += 1
            return carte.get(i0, len(w1))
        # positions (en mots) du début de chaque entrée dans t0
        idx = []
        cherche = 0
        for e in ent0:
            p = t0.find(e["texte"], cherche)
            cherche = p + 1
            idx.append(len(t0[:p].split()))
        fins = idx[1:] + [len(t0[:t0.rfind("TABLE")].split())]
        for e, a0, b0 in zip(ent0, idx, fins):
            a1, b1 = vers1(a0), vers1(b0)
            # reconstituer le texte corrigé de l'entrée avec ses sauts de ligne : on coupe t1 sur les positions des mots
            pos = [m.start() for m in re.finditer(r"\S+", t1)]
            debut = pos[a1] if a1 < len(pos) else len(t1)
            fin = pos[b1] if b1 < len(pos) else len(t1)
            _, corps = chaignon.nettoyer(t1[debut:fin])
            sec = e["section"]; rang[sec] += 1
            c = chaignon.cle_liturgique(e["titre"], {}) if sec == "liturgie" else None
            entrees.append({"cle": c or (f"S:{rang[sec]}" if sec == "parcours" else f"L:{rang[sec]}"),
                            "titre": chaignon.traits(e["titre"]), "numero": e["num"], "partie": sec, "tome": n, "page": 0,
                            "corps": corps})
        print('tome', n, len(ent0), 'méditations')
    doc = {"id": "chaignon", "titre": "La méditation, ou le fidèle sanctifié par la pratique de l’oraison mentale",
           "auteur": "R. P. Chaignon, S. J.", "editions": {"1": "Paris, 1872", "2": "Paris, 1872", "3": "Paris, 1872"},
           "provenance": ("archive.org, lamditationoulef01chai, …02chai, …03chai ; deux lectures OCR (archive.org et Tesseract) "
                          "comparées mot à mot, désaccords restants tranchés sur l'image, 18 pages du t. II abîmées par le verso "
                          "recopiées à la main ; coquilles résiduelles possibles"),
           "entrees": entrees}
    (RACINE / "data" / "recueils" / "chaignon.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(entrees), 'méditations écrites')


if __name__ == "__main__":
    main()
