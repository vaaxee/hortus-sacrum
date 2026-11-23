"""Fillion, *Le nouveau psautier du Bréviaire romain* (7e éd., 1917, archive.org `lenouveaupsautie00gl`) :
prépare les deux lectures des pages françaises (impaires).

Usage : FILLION=<dossier de travail> python3 -I prep.py <p1> <p2>   (pages imprimées, bornes comprises)

Dans <dossier de travail> (non versionné) :
  dl/hocr.html        couche ABBYY d'archive.org (`lenouveaupsautie00gl_hocr.html`) : lecture A
  img/n<N>.jpg        image de la page (`https://archive.org/download/lenouveaupsautie00gl/page/n<N>.jpg`, N = page + 13)
  crop/n<N>.y         ordonnée du filet qui sépare le texte des notes
  crop2/n<N>.png/.box zone du texte (colonne ABBYY, au-dessus du filet)
  tess2/n<N>.tsv      Tesseract fra --psm 6 sur la zone du texte : lecture B
"""
import json, os, re, subprocess, sys, html
from pathlib import Path
import numpy as np
from PIL import Image

B = Path(os.environ['FILLION'])
ID = 'lenouveaupsautie00gl'
_HOCR = None


def filet(im):
    """Premier trait horizontal (filet des notes) sous le haut de la page, ou None : plus longue suite de pixels
    sombres dans une bande de 5 lignes (le filet peut être un peu penché ou interrompu)."""
    g = np.asarray(im)
    a = g < (np.median(g) - 60)
    h, w = a.shape
    for y in range(int(h * 0.12), int(h * 0.97) - 5, 2):
        band = a[y:y + 5].any(axis=0)
        d = np.diff(np.concatenate(([0], band.astype(np.int8), [0])))
        s, e = np.where(d == 1)[0], np.where(d == -1)[0]
        if len(s) and (e - s).max() > w * 0.33:
            return y + 2
    return None


def abbyy(n, cut):
    """Lignes ABBYY de l'image n<N> au-dessus de `cut` : [{x, x2, y, y2, t}] (hOCR : page_<N+1>)."""
    global _HOCR
    if _HOCR is None:
        _HOCR = (B / 'dl' / 'hocr.html').read_text(encoding='utf-8')
    m = re.search(r'<div class="ocr_page" id="page_%06d"' % (n + 1), _HOCR)
    if not m:
        return []
    fin = _HOCR.find('<div class="ocr_page"', m.end())
    seg = _HOCR[m.start(): fin if fin > 0 else len(_HOCR)]
    out = []
    for p in re.split(r'(?=<span class="ocr_line")', seg):
        lm = re.match(r'<span class="ocr_line"[^>]*title="bbox (\d+) (\d+) (\d+) (\d+)', p)
        if not lm:
            continue
        x1, y1, x2, y2 = map(int, lm.groups())
        if y1 >= cut:
            continue
        mots = [html.unescape(re.sub(r'<[^>]+>', '', w)).strip()
                for w in re.findall(r'<span class="ocrx_word"[^>]*>(.*?)</span>', p, re.S)]
        out.append({'x': x1, 'x2': x2, 'y': y1, 'y2': y2, 't': ' '.join(w for w in mots if w)})
    out.sort(key=lambda l: l['y'])
    return out


def prep(p):
    n = p + 13
    img = B / 'img' / f'n{n}.jpg'
    if not img.exists() or img.stat().st_size == 0:
        subprocess.run(['curl', '-sL', '--retry', '3', '-o', str(img), f'https://archive.org/download/{ID}/page/n{n}.jpg'], check=True)
    im = Image.open(img).convert('L')
    y = filet(im) or im.size[1]
    (B / 'crop' / f'n{n}.y').write_text(str(y))
    L = [l for l in abbyy(n, y) if l['y'] > 150 and len(l['t']) > 3]
    x1 = max(0, min(l['x'] for l in L) - 70) if L else 0
    x2 = min(im.size[0], max(l['x2'] for l in L) + 50) if L else im.size[0]
    box = (x1, 0, x2, max(10, y - 8))
    im.crop(box).save(B / 'crop2' / f'n{n}.png')
    (B / 'crop2' / f'n{n}.box').write_text(json.dumps(box))
    subprocess.run(['tesseract', str(B / 'crop2' / f'n{n}.png'), str(B / 'tess2' / f'n{n}'), '-l', 'fra', '--psm', '6', 'tsv'],
                   capture_output=True, env={**os.environ, 'OMP_THREAD_LIMIT': '1'})


if __name__ == '__main__':
    for d in ('img', 'crop', 'crop2', 'tess2'):
        (B / d).mkdir(parents=True, exist_ok=True)
    p1, p2 = int(sys.argv[1]), int(sys.argv[2])
    for p in range(p1 | 1, p2 + 1, 2):
        prep(p)
