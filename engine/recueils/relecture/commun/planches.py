"""Planches de relecture : chaque désaccord restant, découpé sur l'image de la page, avec les deux lectures.
Usage : python3 planches.py <dossier> <suffixe> [par_planche]  →  <dossier>/planches<s>/sNNN.png"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
D, S = sys.argv[1], sys.argv[2]; per = int(sys.argv[3]) if len(sys.argv) > 3 else 16
F = json.load(open(f'{D}/flags{S}.json'))
# pages recopiées à la main (manuel<s>/<n>.txt) et table des matières : pas de relecture mot à mot
_man = {int(x[:-4]) for x in os.listdir(f'{D}/manuel{S}')} if os.path.isdir(f'{D}/manuel{S}') else set()
_P = json.load(open(f'{D}/pages{S}.json'))
_b = lambda p: ' '.join(w for l in p for w, _ in l)
_dt = next((i for i in range(len(_P) - 1, len(_P) // 2, -1) if 'TABLE' in _b(_P[i]) and 'MATI' in _b(_P[i]).upper()), len(_P))
F = [f for f in F if f['page'] not in _man and f['page'] < _dt]
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
os.makedirs(f'{D}/planches{S}', exist_ok=True)
W = 1100
def bande(f):
    im = Image.open(f"{D}/img{S}/{f['page']}.jpg").convert('L')
    pages = json.load(open(f'{D}/pages{S}.json')) if False else None
    if f['box']: x0, y0, x1, y1 = f['box']
    elif f['boxA']:
        cs = [list(map(int, c.split(','))) for c in f['boxA']]
        # coordonnées djvu (x0,y1,x1,y0) à l'échelle de l'image d'origine ; l'image est réduite
        x0 = min(c[0] for c in cs); x1 = max(c[2] for c in cs); y0 = min(c[3] for c in cs); y1 = max(c[1] for c in cs)
        s = im.width / ORIG[f['page']]; x0, x1, y0, y1 = [int(v * s) for v in (x0, x1, y0, y1)]
    else: x0, y0, x1, y1 = 0, 0, im.width, 60
    h = max(y1 - y0, 20); y0 = max(0, y0 - 30 - max(0, 90 - h) // 2); y1 = min(im.height, y1 + 30 + max(0, 90 - h) // 2)
    cr = im.crop((0, y0, im.width, min(y1, y0 + 300)))
    ImageDraw.Draw(cr).rectangle((max(0, x0 - 6), 2, x1 + 6, cr.height - 3), outline=0, width=2)
    return cr.resize((W, int(cr.height * W / cr.width)))
# largeur d'origine des pages (attribut width de l'OBJECT djvu), pour les cadres sans lecture Tesseract
ORIG = json.load(open(f'{D}/largeurs{S}.json'))
for n in range(0, len(F), per):
    parts = []
    for f in F[n:n + per]:
        lab = Image.new('L', (W, 24), 255)
        ImageDraw.Draw(lab).text((4, 2), f"#{f['id']} p{f['page']}  A=«{f['a']}»  B=«{f['b']}»"[:115], font=font, fill=0)
        parts += [lab, bande(f)]
    H = sum(p.height for p in parts); sh = Image.new('L', (W, H), 255); y = 0
    for p in parts: sh.paste(p, (0, y)); y += p.height
    sh.save(f'{D}/planches{S}/s{n // per:03d}.png')
print(len(F), 'désaccords,', (len(F) + per - 1) // per, 'planches')
