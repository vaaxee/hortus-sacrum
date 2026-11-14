"""Hamon : planches des cas à trancher, chacun découpé sur l'image (300 dpi) avec les deux lectures.
Usage : python3 -I planches.py <dossier> <suffixe> [par_planche]  →  <dossier>/planches<S>/sNNN.png
Chaque cas porte son numéro (rang dans corrections<S>.json) : la décision se note dans dec<S>.txt
(« numéro<TAB>texte », ou « numéro<TAB>A » pour garder la lecture Google, « B » pour Tesseract)."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
D, S = sys.argv[1], sys.argv[2]; per = int(sys.argv[3]) if len(sys.argv) > 3 else 12
C = json.load(open(f'{D}/corrections{S}.json'))
cas = [(i, c) for i, c in enumerate(C) if not c['auto']]
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
os.makedirs(f'{D}/planches{S}', exist_ok=True)
W = 1100
for n in range(0, len(cas), per):
    parts = []
    for i, c in cas[n:n + per]:
        im = Image.open(f"{D}/img{S}/{c['page']}.png").convert('L')
        x, y, w, h = c['box']
        y0, y1 = max(0, y - 45), min(im.height, y + h + 45)
        x0, x1 = max(0, x - 450), min(im.width, x + w + 450)
        cr = im.crop((x0, y0, x1, y1))
        ImageDraw.Draw(cr).rectangle((x - x0 - 5, y - y0 - 5, x - x0 + w + 5, y - y0 + h + 5), outline=0, width=3)
        cr = cr.resize((W, int(cr.height * W / cr.width)))
        lab = Image.new('L', (W, 26), 255)
        ImageDraw.Draw(lab).text((4, 3), f"#{i}  A=«{c['a']}»  B=«{c['b']}»   ({c['avant']} … {c['apres']})"[:110], font=font, fill=0)
        parts += [lab, cr]
    H = sum(p.height for p in parts); sh = Image.new('L', (W, H), 255); yy = 0
    for p in parts: sh.paste(p, (0, yy)); yy += p.height
    sh.save(f'{D}/planches{S}/s{n // per:03d}.png')
print(len(cas), 'cas,', (len(cas) + per - 1) // per, 'planches')
