"""Somme (Lachat, Vivès) : seconde lecture Tesseract du texte français principal, page par page.

Pour chaque image : le filet qui sépare le français du latin est repéré (ligne horizontale sombre sur plus de la moitié
de la largeur) ; la partie au-dessus est lue par Tesseract (fra, --psm 6).

Usage : OMP_THREAD_LIMIT=1 python3 -I tess.py <dossier images> <dossier sortie> <n0> <n1> [processus]
Écrit <sortie>/<n>.json : {page, filet, lignes: [{t, x, y, h, mots: [[texte, x, y, w, h, conf]]}]} ;
le tri (titre courant, notes, colonnes latines) est fait par selection.py.
"""

import csv
import io
import json
import os
import re
import statistics
import subprocess
import sys
from multiprocessing import Pool

from PIL import Image



def filet(im):
    """Ordonnée du filet : longue suite continue de pixels sombres, sur une ligne mince (voisines claires)."""
    g = im.convert('L')
    W, H = g.size
    px = g.load()
    fond = sorted(px[x, H // 2] for x in range(0, W, 7))[int(W / 7 * 0.8)]
    seuil = fond - 45

    def course(y, e=10):
        # bande de e lignes (filet un peu penché sur les scans)
        best = run = trou = 0
        for x in range(0, W, 2):
            if min(px[x, yy] for yy in range(y, min(y + e, H))) < seuil:
                run += 1 + trou
                trou = 0
                best = max(best, run)
            elif run and trou < 4:
                trou += 1
            else:
                run = trou = 0
        return best

    for y in range(int(H * 0.15), H - 34, 2):
        c = course(y)
        if c > 0.5 * W / 2 and course(y - 12, 10) < c / 3 and course(y + 22, 10) < c / 3:
            return y
    return H


def lire(img, dest, n):
    im = Image.open(img)
    W, H = im.size
    y0 = filet(im)
    haut = im.crop((0, 0, W, max(y0 - 4, 50)))
    buf = io.BytesIO()
    haut.save(buf, format='PNG')
    r = subprocess.run(['tesseract', 'stdin', 'stdout', '-l', 'fra', '--psm', '6', 'tsv'],
                       input=buf.getvalue(), capture_output=True, check=True)
    rows = list(csv.DictReader(io.StringIO(r.stdout.decode('utf-8')), delimiter='\t', quoting=csv.QUOTE_NONE))
    lignes = {}
    for w in rows:
        if w['level'] != '5' or not w['text'].strip():
            continue
        k = (int(w['block_num']), int(w['par_num']), int(w['line_num']))
        lignes.setdefault(k, []).append([w['text'], int(w['left']), int(w['top']), int(w['width']), int(w['height']),
                                         float(w['conf'])])
    L = []
    for k in sorted(lignes, key=lambda k: statistics.median(m[2] for m in lignes[k])):
        ms = lignes[k]
        hs = [m[4] for m in ms if re.search(r'[a-zà-ÿ]', m[0]) and not re.search(r'[A-ZÀ-Ý]{2}', m[0])]
        L.append(dict(t=' '.join(m[0] for m in ms), x=min(m[1] for m in ms), y=int(statistics.median(m[2] for m in ms)),
                      xmax=max(m[1] + m[3] for m in ms), h=statistics.median(hs) if hs else 0, mots=ms))
    json.dump(dict(page=n, W=W, H=H, filet=y0, lignes=L), open(dest, 'w'), ensure_ascii=False)


def tache(a):
    src, out, n = a
    d = f'{out}/{n}.json'
    if not os.path.exists(d):
        lire(f'{src}/n{n}.jpg', d, n)
    return n


if __name__ == '__main__':
    src, out, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    k = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    os.makedirs(out, exist_ok=True)
    with Pool(k) as p:
        for n in p.imap_unordered(tache, [(src, out, n) for n in range(a, b + 1)]):
            pass
