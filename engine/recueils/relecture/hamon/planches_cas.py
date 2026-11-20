"""Hamon : planches d'extraits du scan pour une liste de cas à trancher (format de commun/remplacer.py).

Usage : python3 -I planches_cas.py <hamon.json> <dossier pdf> <cas.txt> <sortie/prefixe> [par planche=12]
Chaque cas « texte fautif<TAB>texte proposé » est situé (entrée, tome, page du PDF), le mot qui change sert de
repère dans la couche texte ; les planches portent le numéro du cas et la proposition.
"""
import difflib, json, re, subprocess, sys
from functools import lru_cache
from pathlib import Path

H, DOS, CAS, OUT = sys.argv[1:5]
N = int(sys.argv[5]) if len(sys.argv) > 5 else 12
d = json.load(open(H))
EX = str(Path(__file__).resolve().parents[1] / 'commun' / 'extraits.py')


@lru_cache(maxsize=None)
def texte(tome, p):
    return subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), f'{DOS}/bc{tome}.pdf', '-'], capture_output=True, text=True).stdout


cas = [l.rstrip('\n').split('\t') for l in open(CAS, encoding='utf-8') if '\t' in l and not l.startswith('#')]
reqs = {}
for i, c in enumerate(cas):
    a, b = c[0].replace('\\n', '\n'), c[1].replace('\\n', '\n')
    wa, wb = a.split(), b.split()
    diff = [x for x in wa if x not in wb] or wa[:1]
    mot = diff[0]
    es = [e for e in d['entrees'] if a in (e.get('corps') or '') or a in (e.get('sommaire') or '')]
    if not es:
        print(f'{i}\tintrouvable\t{a!r}'); continue
    e = es[0]
    cle = re.sub(r'\W+$', '', mot)
    best = max(range(max(1, e['page_pdf'] - 1), e['page_pdf'] + 13),
               key=lambda p: (cle in texte(e['tome'], p)) * 10 + sum(w in texte(e['tome'], p) for w in wa))
    et = f"#{i} {a.replace(chr(10), ' ')} -> {b.replace(chr(10), ' ')}"
    reqs.setdefault(e['tome'], []).append((i, f"{best}|{cle}|{et}"))
k = 0
for t, l in sorted(reqs.items()):
    for j in range(0, len(l), N):
        part = l[j:j + N]
        out = f'{OUT}_{k:02d}.png'
        subprocess.run(['python3', '-I', EX, f'{DOS}/bc{t}.pdf', out] + [r for _, r in part], check=True, capture_output=True)
        print(out, [i for i, _ in part])
        k += 1
