"""Hamon : espaces parasites que proposer.py (R1) ne voit pas, parce que les deux morceaux sont des mots connus.

Usage : python3 -I espaces.py <hamon.json> > propositions.txt
Sortie au format de commun/remplacer.py, **à relire** avant d'appliquer :
  A. « en semble » → « ensemble » : deux mots connus dont la réunion est un mot du recueil au moins 8 fois plus
     fréquent que la paire séparée, et la paire séparée elle-même rare ;
  B. traits d'union espacés : « c'est-à - dire », « Jésus- Christ », « ci -dessus » → forme à trait d'union, quand
     elle est attestée au moins 3 fois dans les recueils (au moins 5 fois pour « X - Y », qui peut être un tiret).
"""
import collections, glob, json, os, re, sys

F = sys.argv[1]
MOT = r"[A-Za-zÀ-ÿœŒæÆ]+"
mots, paires, traits = collections.Counter(), collections.Counter(), collections.Counter()
for g in glob.glob(os.path.join(os.path.dirname(os.path.abspath(F)), '*.json')) + [F]:
    try: d = json.load(open(g))
    except Exception: continue
    for e in d.get('entrees', []):
        t = e.get('corps', '')
        ws = re.findall(MOT, t)
        mots.update(w.lower() for w in ws)
        paires.update(f"{a} {b}".lower() for a, b in re.findall(rf"(?=\b({MOT}) ({MOT})\b)", t))
        traits.update(m.lower() for m in re.findall(rf"{MOT}(?:-{MOT})+", t))
d = json.load(open(F))
vus = set()
for e in d['entrees']:
    t = e['corps'].split('\n\n### Notes')[0]
    # A
    for m in re.finditer(rf"(?=(?<![\w'’-])({MOT}) ({MOT})(?![\w'’-]))", t):
        a, b = m.group(1), m.group(2)
        j = (a + b).lower()
        if len(a) < 2 or len(b) < 3 or a[0].isupper() != (a + b)[0].isupper() or b[0].isupper(): continue
        if mots[j] >= 3 and mots[j] >= 8 * paires[f"{a} {b}".lower()]:
            k = f"{a} {b}"
            if k not in vus: vus.add(k); print(f"{k}\t{a + b}\t*\t# A {mots[j]}")
    # B
    for m in re.finditer(rf"(?<![\w-])((?:{MOT}['’])?{MOT}(?:-{MOT})*)( -|- | - )((?:{MOT})(?:-{MOT})*)(?![\w])", t):
        a, s, b = m.groups()
        j = f"{a}-{b}".lower()
        seuil = 5 if s == ' - ' else 3
        if traits[j] >= seuil:
            k = f"{a}{s}{b}"
            if k not in vus: vus.add(k); print(f"{k}\t{a}-{b}\t*\t# B {traits[j]}")
