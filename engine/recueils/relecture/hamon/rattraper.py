"""Hamon : rattrape les décisions non placées par appliquer.py (voisinage différent dans le texte de l'app).
Une décision n'est rattrapée partout que si le mot d'origine n'est pas un mot (ni dictionnaire, ni Vulgate, ni mot
fréquent du livre) : son remplacement ne peut alors toucher que la même faute.
Usage : python3 -I rattraper.py <hamon.json> <decisions.txt> <dossier> [--ecrire]"""
import collections, json, re, sys
from spellchecker import SpellChecker
F, DEC, D = sys.argv[1], sys.argv[2], sys.argv[3]
sp = SpellChecker(language='fr')
d = json.load(open(F))
MOT = r"[A-Za-zÀ-ÿœŒæÆ]+"
voc = collections.Counter(w.lower() for e in d['entrees'] for w in re.findall(MOT, e.get('corps', '') + ' ' + e.get('sommaire', '')))
fix = {}
for l in open(DEC, encoding='utf-8'):
    if '\t' not in l: continue
    k, v = l.rstrip('\n').split('\t', 1); s, i = k.split(':')
    a = json.load(open(f'{D}/corrections{s}.json'))[int(i)]['a']
    mots = re.findall(MOT, a)
    if v in ('A', a) or not mots: continue
    if any(m.lower() in sp or voc[m.lower()] >= 4 for m in mots if len(m) > 1): continue
    fix[a] = v
n = 0
for e in d['entrees']:
    for k in ('corps', 'sommaire'):
        t = e.get(k)
        if not t: continue
        for a, b in fix.items():
            t, m = re.subn(r'(?<![\w’\'])' + re.escape(a) + r'(?![\w])', b, t); n += m
        e[k] = t
print('rattrapées', n)
if '--ecrire' in sys.argv: json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
