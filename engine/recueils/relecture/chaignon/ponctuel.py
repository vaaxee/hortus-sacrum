"""Chaignon : quelques corrections relues sur l'image qui ne passent pas par la liste mot à mot (plusieurs mots)."""
import json, sys
F = sys.argv[1]
R = [("ministres.il eri est", "ministres. Il en est"),
     ("servus, Jf. Vcti\\ 2.", "servus, II. Petr. 2."),
     ("Mon âme s3 est", "Mon âme s’est"),
     ("Vidi (urbain magnam quam", "Vidi turbam magnam quam")]
d = json.load(open(F))
for a, b in R:
    n = 0
    for e in d['entrees']:
        if a in e['corps']: e['corps'] = e['corps'].replace(a, b); n += 1
    print(n, a)
json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
