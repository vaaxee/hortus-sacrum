"""Une confusion de lettres propre à un scan, répétée dans tout le livre (ex. « t » lu « l » : « médilés »,
« servileurs », « parenls »). Propositions au format de remplacer.py, à relire avant usage.

Usage : python3 -I lettres.py <recueil.json> <lu> <voulu> > propositions.txt     (ex. : l t)
Un mot inconnu (ni dictionnaire, ni ≥ 3 fois dans les recueils) dont une seule façon de remplacer une ou
plusieurs occurrences de <lu> par <voulu> donne un mot courant (dictionnaire et ≥ 5 fois dans les recueils).
"""
import collections, glob, itertools, json, os, re, sys
from spellchecker import SpellChecker

F, A, B = sys.argv[1:4]
sp = SpellChecker(language='fr')
MOT = r"[A-Za-zÀ-ÿœŒæÆ]+"
corpus = collections.Counter()
for g in glob.glob(os.path.join(os.path.dirname(os.path.abspath(F)), '*.json')):
    for e in json.load(open(g)).get('entrees', []):
        for k in ('corps', 'sommaire', 'titre'):
            if isinstance(e.get(k), str): corpus.update(w.lower() for w in re.findall(MOT, e[k]))
d = json.load(open(F))
vus = set()
for e in d['entrees']:
    for k in ('titre', 'sommaire', 'corps'):
        t = e.get(k)
        if not isinstance(t, str): continue
        for m in re.finditer(rf"(?<![\w'’-]){MOT}(?![\w'’-])", t):
            w = m.group(0); x = w.lower()
            if x in sp or corpus[x] >= 3 or w in vus or A not in x: continue
            pos = [i for i in range(len(x)) if x.startswith(A, i)]
            out = set()
            for r in range(1, min(len(pos), 3) + 1):
                for c in itertools.combinations(pos, r):
                    y = list(x)
                    for i in sorted(c, reverse=True): y[i:i + len(A)] = B
                    y = ''.join(y)
                    if y in sp and corpus[y] >= 5: out.add(y)
            if len(out) == 1:
                y = out.pop()
                y = y[0].upper() + y[1:] if w[0].isupper() else y
                vus.add(w)
                print(f'{w}\t{y}\t*')
