"""Hamon : prépare les deux lectures d'une tranche de pages pour commun/aligner.py.

Usage : python3 prep.py <tome> <première page pdf> <dernière> <dossier de travail> <suffixe>
  - lecture A : la couche texte des PDF Google Livres (pdftotext -bbox-layout), mots avec leurs coordonnées ;
  - lecture B : Tesseract (fra, psm 6) sur l'image de la page rendue à 300 dpi.
Écrit pages<S>.json (pages → lignes → [mot, boîte]) et tess<S>/<i>.tsv, plus img<S>/<i>.png pour les planches.
"""
import json, os, subprocess, sys
from pathlib import Path
from bs4 import BeautifulSoup

tome, p0, p1, D, S = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4]), sys.argv[5]
import os
PDF = Path(os.environ['PDF']) if os.environ.get('PDF') else Path(__file__).resolve().parents[4] / 'vendor' / 'sources' / 'hamon' / f'bc{tome}.pdf'  # PDF= : autre livre (Guéranger)
D.mkdir(parents=True, exist_ok=True)
(D / f'tess{S}').mkdir(exist_ok=True); (D / f'img{S}').mkdir(exist_ok=True)
pages = []
for i, p in enumerate(range(p0, p1 + 1)):
    xml = subprocess.run(['pdftotext', '-bbox-layout', '-f', str(p), '-l', str(p), str(PDF), '-'], capture_output=True, text=True).stdout
    s = BeautifulSoup(xml, 'html.parser')
    pg = s.find('page'); W = float(pg['width']); H = float(pg['height'])
    img = D / f'img{S}' / f'{i}.png'
    if not img.exists():
        subprocess.run(['pdftoppm', '-f', str(p), '-l', str(p), '-r', '300', '-gray', '-png', '-singlefile', str(PDF), str(img)[:-4]], check=True)
    from PIL import Image
    iw, ih = Image.open(img).size
    sx, sy = iw / W, ih / H
    lignes = []
    for l in s.find_all('line'):
        mots = []
        for w in l.find_all('word'):
            x0, y0, x1, y1 = (float(w[k]) for k in ('xmin', 'ymin', 'xmax', 'ymax'))
            mots.append([w.get_text(), [round(x0 * sx), round(y0 * sy), round((x1 - x0) * sx), round((y1 - y0) * sy)]])
        if mots: lignes.append(mots)
    pages.append(lignes)
    tsv = D / f'tess{S}' / f'{i}'
    if not Path(str(tsv) + '.tsv').exists():
        subprocess.run(['tesseract', str(img), str(tsv), '-l', 'fra', '--psm', '6', 'tsv'], capture_output=True)
json.dump(pages, open(D / f'pages{S}.json', 'w'), ensure_ascii=False)
print('pages', len(pages))
