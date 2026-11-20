"""Traits d'union et apostrophes perdus par l'OCR : « estelle » → « est-elle », « pourraitil » → « pourrait-il »,
« vousmêmes » → « vous-mêmes », « quils » → « qu’ils ». Propositions au format de remplacer.py, à relire.

Usage : python3 -I traits.py <recueil.json> [apostrophe] > propositions.txt
Un mot inconnu (dictionnaire, ≥ 3 fois dans les recueils) qui se coupe en un mot connu suivi d'un pronom
(je, tu, il, elle, on, nous, vous, ils, elles, ce, le, la, les, lui, leur, moi, toi, y, en) ou de « même(s) »,
ou en « t » + pronom après une voyelle (pourrait-il, a-t-elle), ou en « qu/l/d/j/n/s » + mot connu.
Seuls sont proposés les découpages dont la forme à trait d'union se trouve déjà dans les recueils, ou un composé
attesté (bien-être, sur-le-champ…).
"""
import collections, glob, json, os, re, sys
from spellchecker import SpellChecker

F = sys.argv[1]
AP = sys.argv[2] if len(sys.argv) > 2 else '’'
sp = SpellChecker(language='fr')
MOT = r"[A-Za-zÀ-ÿœŒæÆ]+"
corpus = collections.Counter()
traits = collections.Counter()
for g in glob.glob(os.path.join(os.path.dirname(os.path.abspath(F)), '*.json')):
    for e in json.load(open(g)).get('entrees', []):
        for k in ('corps', 'sommaire', 'titre'):
            if isinstance(e.get(k), str):
                corpus.update(w.lower() for w in re.findall(MOT, e[k]))
                traits.update(w.lower() for w in re.findall(rf"{MOT}(?:-{MOT})+", e[k]))
connu = lambda w: w.lower() in sp or corpus[w.lower()] >= 3
PRON = ['elles', 'elle', 'ils', 'il', 'on', 'nous', 'vous', 'je', 'tu', 'ce', 'le', 'la', 'les', 'lui', 'leur', 'moi',
        'toi', 'y', 'en', 'mêmes', 'même']
ELID = ['qu', 'l', 'd', 'j', 'n', 's', 'm', 't', 'c']
d = json.load(open(F))
vus = set()
for e in d['entrees']:
    for k in ('sommaire', 'corps'):
        t = e.get(k)
        if not isinstance(t, str): continue
        for m in re.finditer(rf"(?<![\w'’-]){MOT}(?![\w'’-])", t):
            w = m.group(0)
            if connu(w) or w in vus: continue
            cands = set()
            for p in PRON:
                if w.lower().endswith(p) and len(w) > len(p) + 1:
                    x = w[:-len(p)]
                    if x.lower().endswith('t') and x[:-1] and x[-2].lower() in 'aeiou' and connu(x[:-1]) and not connu(x):
                        c = f'{x[:-1]}-t-{p}' if x[-1] == 't' else None
                        if c and traits[c.lower()] >= 1: cands.add(c)
                    if connu(x) and traits[f'{x}-{p}'.lower()] >= 1:
                        cands.add(f'{x}-{w[-len(p):]}')
            for el in ELID:
                if w.lower().startswith(el) and len(w) > len(el) + 1:
                    y = w[len(el):]
                    if y.lower() in sp and corpus[y.lower()] >= 20 and y[0].lower() in 'aeiouyéèêàâhœ':
                        cands.add(w[:len(el)] + AP + y)
            for z in traits:
                if z.replace('-', '') == w.lower() and traits[z] >= 2:
                    cands.add(z if w.islower() else z[0].upper() + z[1:])
            if len(cands) == 1:
                vus.add(w)
                print(f'{w}\t{cands.pop()}\t*')
