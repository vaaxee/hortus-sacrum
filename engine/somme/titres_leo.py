"""Somme : intitulés latins (questions et articles) de l'édition léonine (t. IV, Rome 1888), d'après la lecture ABBYY
d'archive.org (operaomniaiussui04thom), avec la page et la position pour la relecture sur l'image.

Usage : python3 -I titres_leo.py <djvu.xml> <sortie.json>
Sortie : [{type: "q"|"a", rang, texte (capitales, tel que lu), page, y}]
Les intitulés sont relus sur l'image (planches) ; les corrections vont dans titres_la.json.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abbyy import dechiffrer, pages  # noqa: E402

ORDS = ['PRIMUS', 'SECUNDUS', 'TERTIUS', 'QUARTUS', 'QUINTUS', 'SEXTUS', 'SEPTIMUS', 'OCTAVUS', 'NONUS', 'DECIMUS',
        'UNDECIMUS', 'DUODECIMUS', 'DECIMUSTERTIUS']


def main():
    P = pages(sys.argv[1])
    out = []
    for n, p in enumerate(P[:330]):
        L = p['lines']
        for i, l in enumerate(L):
            t = dechiffrer(l['t']).strip()
            m = re.fullmatch(r'ARTICULUS\s+([A-Z]+)', t)
            q = re.fullmatch(r'QUAESTIO\s+([A-Z]+)', t)
            if (m and m.group(1) in ORDS) or (q and 'ARTICULUS' not in t):
                titre = []
                for x in L[i + 1:i + 5]:
                    s = dechiffrer(x['t']).strip()
                    if re.search(r'[a-z]{3}', s) or not s or len(titre) and x['y'] - L[i]['y'] > 300:
                        break
                    titre.append(s)
                    if s.endswith(('HABERI', 'EXTENDAT')):
                        pass
                out.append(dict(type='a' if m else 'q', rang=(m or q).group(1), texte=' '.join(titre), page=n,
                                y=l['y'], x1=l['x1'], lignes=[[x['x1'], x['y'] - x['h'], x['x2'], x['y']]
                                                              for x in L[i:i + 1 + len(titre)]]))
    json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    for o in out:
        print(o['page'], o['type'], o['rang'], '|', o['texte'])


if __name__ == '__main__':
    main()
