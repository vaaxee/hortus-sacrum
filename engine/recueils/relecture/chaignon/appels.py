"""Chaignon : retire du texte courant les appels de note (les notes sont rangées en fin de méditation, renumérotées).
Usage : python3 -I appels.py <chaignon.json> [--ecrire]
Seuls cas touchés : un chiffre 1-9 collé à la fin d'un mot (« terre3. ») ou isolé après un mot et suivi d'une
ponctuation (« point 2. »), jamais après une abréviation de référence (Ps., chap., Matth. 5…) ni dans les notes."""
import json, re, sys
F = sys.argv[1]
REF = set("chap chapitre ch ps psaume liv livre lib tome t p page n no art serm sermon hom homil ép épître lettre c part partie sect section méd méditation v vers verset cap ep epist tract q qu dist l les des ces nos vos mes ses leurs".split())
colle = re.compile(r"(?<=[a-zà-ÿœ»!?…])([1-9¹²³])(?=[\s.,;:!?»)]|$)")
isole = re.compile(r"(\w+|[!?…»]) ([1-9])(?=[.,;:!?»)](?:\s|$))")
d = json.load(open(F)); n = 0; ex = []
for e in d['entrees']:
    corps, sep, notes = e['corps'].partition('\n\n### Notes\n\n')
    if not sep: continue
    P = corps.split('\n\n')
    for i, p in enumerate(P):
        if p.startswith('#'): continue
        def f(m):
            global n
            n += 1
            if len(ex) < 40: ex.append(p[max(0, m.start() - 25):m.end() + 10])
            return ''
        def g(m):
            if m.group(1).lower() in REF or m.group(1)[0].isupper() or m.group(1).isdigit(): return m.group(0)
            f(m); return m.group(1)
        P[i] = isole.sub(g, colle.sub(f, p))
    e['corps'] = '\n\n'.join(P) + sep + notes
print('appels retirés', n); print('\n'.join(ex))
if '--ecrire' in sys.argv: json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
