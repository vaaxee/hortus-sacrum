"""Somme (Lachat) : planche de relecture d'une page — l'image du texte français (scan de 1880) et le texte retenu,
ligne à ligne, pour la relecture mot à mot sur l'image.

Usage : python3 -I planche.py <R.json> <dossier images> <dossier sortie> <page> [<page>…]
Écrit <sortie>/p<page>.jpg et affiche les lignes numérotées.
"""

import json
import sys

from PIL import Image


def main():
    R = {p['page']: p for p in json.load(open(sys.argv[1]))}
    src, out = sys.argv[2], sys.argv[3]
    for n in map(int, sys.argv[4:]):
        p = R[n]
        L = p['lignes']
        im = Image.open(f'{src}/n{n}.jpg')
        W, H = im.size
        if L:
            y0 = max(0, min(l['y'] for l in L) - 30)
            y1 = min(H, max(l['y'] + max(l['h'], 40) for l in L) + 40)
        else:
            y0, y1 = 0, H
        c = im.crop((int(W * 0.04), y0, int(W * 0.96), y1))
        f = 1150 / c.size[0]
        c = c.resize((1150, int(c.size[1] * f)))
        c.save(f'{out}/p{n}.jpg', quality=85)
        print(f'=== page {n} ({len(L)} lignes)')
        for i, l in enumerate(L):
            print(f'{i:2d} {l["t"]}')


if __name__ == '__main__':
    main()
