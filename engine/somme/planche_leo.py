"""Somme : planche des intitulés latins de l'édition léonine (titres_leo.py) pour la relecture sur l'image.

Usage : python3 -I planche_leo.py <TL.json> <dossier images léonines> <sortie.jpg> <page0> <page1>
"""

import json
import sys

from PIL import Image, ImageDraw


def main():
    T = json.load(open(sys.argv[1]))
    src, dest, a, b = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    crops = []
    for t in T:
        if not a <= t['page'] <= b:
            continue
        im = Image.open(f"{src}/n{t['page']}.jpg")
        x0 = min(l[0] for l in t['lignes']) - 120
        y0 = min(l[1] for l in t['lignes']) - 20
        x1 = max(l[2] for l in t['lignes']) + 120
        y1 = max(l[3] for l in t['lignes']) + 25
        c = im.crop((max(0, x0), max(0, y0), min(im.size[0], x1), min(im.size[1], y1)))
        f = 1100 / c.size[0]
        crops.append(c.resize((1100, int(c.size[1] * f))))
    H = sum(c.size[1] + 10 for c in crops)
    out = Image.new('RGB', (1100, H), 'white')
    y = 0
    d = ImageDraw.Draw(out)
    for c in crops:
        out.paste(c, (0, y))
        y += c.size[1] + 10
        d.line([(0, y - 5), (1100, y - 5)], fill='red', width=2)
    out.save(dest, quality=85)


if __name__ == '__main__':
    main()
