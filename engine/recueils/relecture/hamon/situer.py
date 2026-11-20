"""Hamon : situe des passages du recueil dans les PDF (bc1-3.pdf) pour les planches d'extraits.

Usage : python3 -I situer.py <hamon.json> <dossier des pdf> "<passage>" ...
Pour chaque passage (texte actuel du recueil), trouve l'entrée, puis la page du PDF (de page_pdf à page_pdf + 12)
dont la couche texte recoupe le mieux les mots du passage ; imprime « tome<TAB>page<TAB>mot repère<TAB>passage ».
"""
import json, re, subprocess, sys
from functools import lru_cache

H, DOS = sys.argv[1], sys.argv[2]
d = json.load(open(H))


@lru_cache(maxsize=None)
def texte(tome, p):
    return subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), f'{DOS}/bc{tome}.pdf', '-'], capture_output=True, text=True).stdout


for q in sys.argv[3:]:
    es = [e for e in d['entrees'] if q in (e.get('corps') or '') or q in (e.get('sommaire') or '')]
    if not es:
        print('?\t?\t?\t' + q); continue
    e = es[0]
    mots = re.findall(r'\w+', q.lower())
    best = None
    for p in range(max(1, e['page_pdf'] - 1), e['page_pdf'] + 13):
        t = texte(e['tome'], p).lower()
        sc = sum(m in t for m in mots if len(m) > 2)
        if best is None or sc > best[0]: best = (sc, p)
    rep = max((m for m in re.findall(r'\w+', q) if len(m) > 3), key=len, default=q)
    print(f"{e['tome']}\t{best[1]}\t{rep}\t{q}")
