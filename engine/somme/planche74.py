"""Somme (Lachat) : planche de relecture d'une page sur l'exemplaire de 1874 (archive.org sommethologique07lachgoog,
même composition que 1880, scan plus net), avec les lignes retenues (R.json, après corrections_fr.txt) numérotées.
Marques : « * » ligne corrigée sur l'image ; « ? » ligne sans accord d'une lecture Tesseract et d'une lecture ABBYY
(V.json) : resoudre.py a pu y retirer un mot (cas vu : « saint Jean Damascène … I, 1-3 » réduit) ; à relire mot à mot ;
la lecture Tesseract de 1874 (D) est donnée en regard.

Usage : python3 -I planche74.py <R.json> <V.json> <Dsel.json> <corrections_fr.txt> <images 1874> <sortie> <page>…
Écrit <sortie>/p<page>.jpg (texte français) et affiche les lignes.
"""

import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from construire import charger_corrections  # noqa: E402


def main():
    R = {p['page']: p for p in json.load(open(sys.argv[1]))}
    VV = {p['page']: p for p in json.load(open(sys.argv[2]))}
    V = {n: p['pageB'] for n, p in VV.items()}
    D = {p['page']: p for p in json.load(open(sys.argv[3]))}
    cor = charger_corrections(sys.argv[4])
    src, out = sys.argv[5], sys.argv[6]
    for n in map(int, sys.argv[7:]):
        m = V[n]
        im = Image.open(f'{src}/n{m}.jpg')
        W, H = im.size
        L = D.get(m, {'lignes': []})['lignes']
        y0 = max(0, min(l['y'] for l in L) - 260) if L else 0
        y1 = min(H, max(l['y'] + 90 for l in L) + 60) if L else H
        c = im.crop((int(W * 0.06), y0, int(W * 0.96), y1))
        f = 1500 / c.size[0]
        c.resize((1500, int(c.size[1] * f))).save(f'{out}/p{n}.jpg', quality=80)
        c = cor.get(n, {})
        print(f'=== page {n} (1874 : n{m})')
        for i, l in enumerate(R[n]['lignes']):
            t = c.get(str(i), l['t'])
            v = VV[n]['lignes'][i]
            marque = '*' if str(i) in c else (' ' if v['sure'] else '?')
            print(f'{i:2d}{marque} {t}')
            if marque == '?' and v.get('d') and v['d'] != t:
                print(f'   D {v["d"]}')
            if f'{i}+' in c:
                print(f'{i}+* {c[str(i) + "+"]}')


if __name__ == '__main__':
    main()
