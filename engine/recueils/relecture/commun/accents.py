"""Accents parasites de l'OCR : « éntendons » → « entendons », « véritablé » → « véritable », « fôndement ».
Propositions au format de remplacer.py, à relire.

Usage : python3 -I accents.py <recueil.json> > propositions.txt
Un mot inconnu (ni dictionnaire, ni ≥ 3 fois dans les recueils, donc jamais une graphie de l'édition comme
« collége » ou « poëte ») dont une seule variante, obtenue en changeant ou ôtant un seul signe diacritique, est un
mot courant (dictionnaire et ≥ 20 fois dans les recueils).
"""
import collections, glob, json, os, re, sys, unicodedata
from spellchecker import SpellChecker

F = sys.argv[1]
sp = SpellChecker(language='fr')
MOT = r"[A-Za-zÀ-ÿœŒæÆ]+"
corpus = collections.Counter()
for g in glob.glob(os.path.join(os.path.dirname(os.path.abspath(F)), '*.json')):
    for e in json.load(open(g)).get('entrees', []):
        for k in ('corps', 'sommaire', 'titre'):
            if isinstance(e.get(k), str): corpus.update(w.lower() for w in re.findall(MOT, e[k]))
VAR = {'a': 'aàâä', 'e': 'eéèêë', 'i': 'iîï', 'o': 'oô', 'u': 'uùûü', 'c': 'cç'}
base = lambda ch: unicodedata.normalize('NFD', ch)[0].lower()
d = json.load(open(F))
vus = set()
for e in d['entrees']:
    for k in ('sommaire', 'corps'):
        t = e.get(k)
        if not isinstance(t, str): continue
        for m in re.finditer(rf"(?<![\w'’-]){MOT}(?![\w'’-])", t):
            w = m.group(0)
            x = w.lower()
            if x in sp or corpus[x] >= 3 or w in vus or w[0].isupper(): continue
            out = set()
            for i, ch in enumerate(x):
                b = base(ch)
                if b not in VAR: continue
                for v in VAR[b]:
                    if v == ch: continue
                    y = x[:i] + v + x[i + 1:]
                    if y in sp and corpus[y] >= 20: out.add(y)
            if len(out) == 1:
                vus.add(w)
                print(f'{w}\t{out.pop()}\t*')
