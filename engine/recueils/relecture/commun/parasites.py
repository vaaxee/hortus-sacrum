"""Mots coupés en fin de ligne avec un parasite entre les deux morceaux : « sain 1 teté », « in « ventions »,
« moin. dre », « commu-. niquant », « vi. vra ». Propositions au format de remplacer.py, à relire avant usage.

Usage : python3 -I parasites.py <recueil.json> > propositions.txt
Règle : deux morceaux séparés par un parasite court (chiffre d'appel de note, «, •, *, point, trait d'union)
dont la réunion est un mot connu (dictionnaire et ≥ 3 fois dans les recueils), l'un des deux au moins inconnu.
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
PAR = r"(?: ?(?:\d{1,2}|[«•*›>]|\.|-\.)\s?| ?\.\s)"
for e in d['entrees']:
    for k in ('sommaire', 'corps'):
        t = e.get(k)
        if not isinstance(t, str): continue
        for m in re.finditer(rf"(?<![\w'’])({MOT})({PAR})({MOT})(?![\w'’])", t):
            a, p, b = m.groups()
            if not re.search(r"[\d«•*›>.]", p) or not b[0].islower(): continue
            if fr(a) and fr(b): continue
            if not fr(a + b): continue
            s = m.group(0)
            if s in vus: continue
            vus.add(s)
            print(f'{s}\t{a + b}\t*')
