"""Planche d'extraits de scan, pour trancher à l'œil des mots douteux.

Usage : python3 -I extraits.py <pdf> <sortie.png> "<page>|<mot du texte PDF>|<étiquette>" ...
Pour chaque demande : la page est rendue à 200 dpi, la ligne où la couche texte du PDF porte le mot (ou le mot
le plus proche) est découpée avec la ligne d'avant et celle d'après, puis toutes les bandes sont empilées, chacune
précédée de son étiquette. Sans couche texte exploitable, on peut donner « page|@y » (y en fraction de la hauteur).
ZOOM=1 dans l'environnement : rendu à 300 dpi et bande resserrée autour du mot (pour juger lettre à lettre).
"""
import difflib, os, re, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
ZOOM = bool(os.environ.get('ZOOM'))
DPI = 300 if ZOOM else 200
try:
    FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
except OSError:
    FONT = None
n = 0
bandes = []
with tempfile.TemporaryDirectory() as T:
    for req in sys.argv[3:]:
        p, mot, *et = req.split('|')
        et = et[0] if et else mot
        png = Path(T) / f'p{p}'
        if not Path(str(png) + '.png').exists():
            subprocess.run(['pdftoppm', '-f', p, '-l', p, '-r', str(DPI), '-gray', '-png', '-singlefile', PDF, str(png)], check=True)
        im = Image.open(str(png) + '.png')
        W, H = im.size
        if mot.startswith('@'):
            y = float(mot[1:]) * H; y0, y1 = max(0, y - 90), min(H, y + 90)
        else:
            xml = subprocess.run(['pdftotext', '-bbox', '-f', p, '-l', p, PDF, '-'], capture_output=True, text=True).stdout
            pw = float(re.search(r'<page width="([\d.]+)"', xml).group(1))
            s = W / pw
            mots = [(m[4], [float(x) for x in m[:4]]) for m in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', xml)]
            if not mots:
                print('pas de texte', req); continue
            noms = [w for w, _ in mots]
            best = max(range(len(mots)), key=lambda i: difflib.SequenceMatcher(None, noms[i].lower(), mot.lower()).ratio())
            x0, ya, x1, yb = (v * s for v in mots[best][1])
            h = yb - ya
            y0, y1 = max(0, ya - 2.2 * h), min(H, yb + 2.2 * h)
            if ZOOM:
                y0, y1 = max(0, ya - 1.2 * h), min(H, yb + 1.2 * h)
        xa, xb = (max(0, int(x0) - 420), min(W, int(x1) + 420)) if ZOOM and not mot.startswith('@') else (0, W)
        b = im.crop((xa, int(y0), xb, int(y1)))
        lab = Image.new('L', (max(b.size[0], 900), 32), 255)
        ImageDraw.Draw(lab).text((6, 4), f'[{n}] p.{p} {et}', fill=0, font=FONT)
        bandes.append(lab); bandes.append(b); n += 1
Wm = max(b.size[0] for b in bandes)
out = Image.new('L', (Wm, sum(b.size[1] for b in bandes)), 255)
y = 0
for b in bandes:
    out.paste(b, (0, y)); y += b.size[1]
if out.size[0] > 1100 and not ZOOM:
    out = out.resize((1100, int(out.size[1] * 1100 / out.size[0])))
out.save(OUT)
print(OUT, out.size)
