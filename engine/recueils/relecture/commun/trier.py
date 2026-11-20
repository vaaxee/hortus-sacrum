"""Après hamon/decider.py : écarte des corrections automatiques jugées fausses à la relecture de la liste, et
ramène l'apostrophe de Tesseract (’) à celle du livre.

Usage : python3 -I trier.py <dossier> <suffixes, ex. abcd> <exclus.txt> [apostrophe du livre, défaut ']
exclus.txt : une ligne « lu A<TAB>lu B » par correction automatique à ne pas faire (elle repasse « à trancher »).
Réécrit corrections<S>.json.
"""
import json, sys

D, SUF, EX = sys.argv[1:4]
AP = sys.argv[4] if len(sys.argv) > 4 else "'"
ex = {tuple(l.rstrip('\n').split('\t')[:2]) for l in open(EX, encoding='utf-8') if '\t' in l and not l.startswith('#')}
n = 0
for s in SUF:
    f = f'{D}/corrections{s}.json'
    C = json.load(open(f))
    for c in C:
        c['b'] = c['b'].replace('’', AP).replace("'", AP)
        if c['auto'] and (c['a'], c['b']) in ex:
            c['auto'] = False; n += 1
    json.dump(C, open(f, 'w'), ensure_ascii=False)
print('écartées :', n)
