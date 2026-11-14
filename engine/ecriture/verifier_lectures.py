"""Imprime, pour chaque élément de roue qui a une lecture, le passage en français (Crampon) et en latin (Vulgate),
pour relire que la référence tombe juste dans les deux textes.  Usage : python3 -I verifier_lectures.py [id de roue…]"""
import json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2] / 'data'
roues = json.load(open(R / 'roues.json'))['roues']
livres = {}
def livre(abr):
    f = R / 'ecriture' / (abr.replace(' ', '').lower() + '.json')
    if abr not in livres: livres[abr] = json.load(open(f)) if f.exists() else None
    return livres[abr]
def lieu(s):
    m = re.match(r'^(\d+)(?:\s*,\s*(\d+)(?:\s*-\s*(\d+))?)?$', s.strip())
    c, de, a = int(m[1]), int(m[2]) if m[2] else None, int(m[3]) if m[3] else None
    return c, de, a or de
def extrait(b, langue, c, de, a):
    ch = next((x for x in b['chapitres'] if x['n'] == c), None)
    if not ch: return '∅'
    vs = [t for v, t in ch[langue] if not de or de <= v <= a]
    return (' '.join(vs) or '∅')[:400]
manque = 0
for r in roues:
    if sys.argv[1:] and r['id'] not in sys.argv[1:]: continue
    for e in r['elements']:
        l = e.get('lecture')
        if not l or re.fullmatch(r'\S+', l): continue
        fr, _, la = l.partition('|')
        m = re.match(r'^(.+?)\s+(\d.*)$', fr.strip())
        b = livre(m[1])
        if not b: print('  LIVRE ABSENT', l); manque += 1; continue
        cf = lieu(m[2]); cl = lieu(la) if la else cf
        tf, tl = extrait(b, 'fr', *cf), extrait(b, 'la', *cl)
        if '∅' in (tf, tl): manque += 1
        print(f"{r['id']} · {e['fr']} · {l}\n   FR {tf}\n   LA {tl}")
print('passages vides :', manque)
