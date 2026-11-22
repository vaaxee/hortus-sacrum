"""Somme (Lachat, Vivès) : repère, page par page, le texte français principal dans la lecture ABBYY d'archive.org.

Mise en page de l'édition : titre courant ; texte français (gros corps) ; notes de Lachat (petit corps) ; filet ;
texte latin sur deux colonnes ; notes latines. On garde le seul texte français principal.

Usage : python3 -I extraire.py <djvu.xml> <première page> <dernière page> <sortie.json>
Sortie : [{page, W, H, box: [y0, y1], lignes: [{t, x1, x2, y, h}]}]
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abbyy import dechiffrer, pages  # noqa: E402


def francais(p):
    W = p['W']
    L = p['lines']
    out = []
    for i, l in enumerate(L):
        # titre courant : première ligne, haut de page, petit corps
        if i == 0 and l['y'] < 280 and l['h'] <= 37:
            continue
        petits = [x['h'] for x in L[i:i + 3]]
        if l['h'] <= 34 and sorted(petits)[len(petits) // 2] <= 32:
            break  # notes de Lachat (ou latin en petit corps)
        def etroite(x):
            return x['x1'] < 0.16 * W and x['x2'] < 0.53 * W or x['x1'] > 0.45 * W and x['x2'] > 0.8 * W and x['x1'] < 0.56 * W
        prec = out[-1]['y'] if out else 0
        if etroite(l) and i + 1 < len(L) and etroite(L[i + 1]) and l['y'] - prec > 90:
            break  # colonnes latines
        if l['h'] < 30:
            break
        out.append(dict(l, t=dechiffrer(l['t'])))
    return out


if __name__ == '__main__':
    src, a, b, dest = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    P = pages(src)
    res = []
    for n in range(a, b + 1):
        p = P[n]
        f = francais(p)
        box = [int(min(x['y'] - x['h'] for x in f)) - 25, int(max(x['y'] for x in f)) + 22] if f else None
        res.append(dict(page=n, W=p['W'], H=p['H'], box=box, lignes=f))
    json.dump(res, open(dest, 'w'), ensure_ascii=False, indent=0)
    if os.environ.get('VOIR'):
        for r in res:
            f = r['lignes']
            print(r['page'], len(f), '|', f[0]['t'][:50] if f else '', '…', f[-1]['t'][-50:] if f else '')
