"""Mots coupés en trois morceaux (« son der nier », « tra vail le ») : propositions à relire.

Usage : python3 -I trois.py <recueil.json> > propositions.txt
Trois morceaux séparés d'une espace, celui du milieu inconnu du dictionnaire, dont la réunion des trois est un mot
connu (dictionnaire et ≥ 3 fois dans les recueils) ; on propose aussi la réunion de deux morceaux seulement quand
c'est elle qui donne le mot. Sortie au format de remplacer.py, une ligne par cas, à relire avant usage.
"""
import collections, glob, json, os, re, sys
from spellchecker import SpellChecker

F = sys.argv[1]
sp = SpellChecker(language='fr')
MOT = r"[A-Za-zÀ-ÿœŒæÆ]+"
corpus = collections.Counter()
for g in glob.glob(os.path.join(os.path.dirname(os.path.abspath(F)), '*.json')):
    for e in json.load(open(g)).get('entrees', []):
        for k in ('corps', 'sommaire', 'titre'):
            if isinstance(e.get(k), str): corpus.update(w.lower() for w in re.findall(MOT, e[k]))
fr = lambda w: w.lower() in sp and corpus[w.lower()] >= 3
d = json.load(open(F))
vus = set()
for e in d['entrees']:
    for k in ('sommaire', 'corps'):
        t = e.get(k)
        if not isinstance(t, str): continue
        for m in re.finditer(rf"(?<![\w'’])({MOT}) ({MOT}) ({MOT})(?![\w'’])", t):
            a, b, c = m.groups()
            if b.lower() in sp or not c[0].islower(): continue
            s = m.group(0)
            if fr(a + b + c): r = a + b + c
            elif fr(a + b) and not fr(b + c): r = a + b + ' ' + c
            elif fr(b + c) and not fr(a + b): r = a + ' ' + b + c
            else: continue
            if s in vus: continue
            vus.add(s)
            print(f'{s}\t{r}\t*')
