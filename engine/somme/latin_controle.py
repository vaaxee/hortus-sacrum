"""Somme : contrôle du latin (Corpus Thomisticum, LA.json) sur la lecture ABBYY de l'édition léonine (t. IV, 1888 ;
archive.org operaomniaiussui04thom). Les deux textes sont alignés mot à mot (minuscules, u/v et i/j confondus,
ponctuation ôtée) ; on garde les écarts où la lecture léonine donne un autre mot latin attesté ailleurs dans la
transcription (substitution plausible), avec la page du scan pour la relecture sur l'image. Seuls les écarts isolés
(trois mots identiques de part et d'autre) sont retenus : la lecture ABBYY mêle les deux colonnes et le commentaire
de Cajetan, si bien qu'un écart long ne dit rien. Les écarts « mot » (mot latin attesté) sont à voir sur l'image ;
les écarts « ocr » sont des fautes de lecture probables (à voir aussi quand le doute subsiste).

Usage : python3 -I latin_controle.py <LA.json> <leo4 djvu.xml> <q0> <q1> <sortie.tsv>
Sortie : question, article, partie, mot CT, mot léonin lu, contexte, page du scan léonin, mot|ocr.
"""

import difflib
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abbyy import dechiffrer, pages  # noqa: E402


def cle(w):
    w = unicodedata.normalize('NFD', w.lower())
    w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    w = w.replace('v', 'u').replace('j', 'i').replace('æ', 'ae').replace('œ', 'oe')
    return re.sub(r'[^a-z]', '', w)


def main():
    LA = json.load(open(sys.argv[1]))
    P = pages(sys.argv[2])
    q0, q1 = int(sys.argv[3]), int(sys.argv[4])
    mots, pg = [], []
    for i, p in enumerate(P):
        for l in p['lines']:
            for w in dechiffrer(l['t']).split():
                k = cle(w)
                if k:
                    mots.append(k)
                    pg.append(i)
    vocab = set()
    parts = []
    for q in range(q0, q1 + 1):
        Q = LA[str(q)]
        parts.append((q, 0, 'pr', Q['pr']))
        for a, A in Q['articles'].items():
            for j, t in enumerate(A['arg'], 1):
                parts.append((q, int(a), f'arg{j}', t))
            parts.append((q, int(a), 'sc', A['sc']))
            parts.append((q, int(a), 'co', A['co']))
            for j, t in enumerate(A['ad'], 1):
                parts.append((q, int(a), f'ad{j}', t))
    for *_, t in parts:
        vocab.update(cle(w) for w in t.split())
    index = {}
    for i in range(len(mots) - 3):
        index.setdefault(tuple(mots[i:i + 4]), []).append(i)
    out = open(sys.argv[5], 'w')
    n = 0
    for q, a, part, t in parts:
        ws = [w for w in t.split() if cle(w)]
        ks = [cle(w) for w in ws]
        # ancre : premier 4-gramme retrouvé dans la lecture léonine
        debut = None
        for i in range(len(ks) - 3):
            if tuple(ks[i:i + 4]) in index:
                debut = index[tuple(ks[i:i + 4])][0] - i
                break
        if debut is None:
            out.write(f'{q}\t{a}\t{part}\t?\t?\tnon retrouvé\t\n')
            continue
        debut = max(0, debut - 20)
        seg = mots[debut:debut + len(ks) + 400]
        sm = difflib.SequenceMatcher(None, ks, seg, autojunk=False)
        ops = sm.get_opcodes()
        for k, (op, i1, i2, j1, j2) in enumerate(ops):
            if op == 'equal':
                continue
            avant = ops[k - 1] if k else None
            apres = ops[k + 1] if k + 1 < len(ops) else None
            # écart isolé : au moins trois mots identiques de part et d'autre (sinon : colonnes ou commentaire mêlés)
            entoure = (avant and avant[0] == 'equal' and avant[2] - avant[1] >= 3
                       and apres and apres[0] == 'equal' and apres[2] - apres[1] >= 3)
            if not entoure or i2 - i1 > 2 or j2 - j1 > 3:
                continue
            lu = seg[j1:j2]
            if ''.join(lu) == ''.join(ks[i1:i2]):
                continue  # mot coupé en fin de ligne
            ctx = ' '.join(ws[max(0, i1 - 4):i2 + 4])
            p = pg[debut + j1] if debut + j1 < len(pg) else ''
            reel = all(w in vocab for w in lu) and lu
            out.write(f'{q}\t{a}\t{part}\t{" ".join(ws[i1:i2])}\t{" ".join(lu)}\t{ctx}\t{p}\t{"mot" if reel else "ocr"}\n')
            n += 1
    print(n, 'écarts')


if __name__ == '__main__':
    main()
