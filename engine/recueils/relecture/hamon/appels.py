"""Hamon : retire du texte courant les appels de note (les notes sont rangées en fin de méditation par notes.py).

Usage : python3 -I appels.py <hamon.json> [--ecrire]
Adapté de `../chaignon/appels.py`. L'OCR de Google Livres lit les petits appels de Hamon comme des signes : « ' »,
« " », « ” », « * », « • », « ¹ », ou un chiffre collé. Cas touchés, dans toutes les méditations (certaines
ont perdu leurs notes à la première lecture, mais gardé les appels), hors titres et hors section « ### Notes » :
- un signe isolé après un mot, suivi d'une espace, d'une ponctuation ou de la fin (« Jésus-Christ '; elle ») ;
- un signe collé à la fin d'un mot, suivi d'une ponctuation ou d'une espace (« servir”. ») ;
- un chiffre 1-9 collé à la fin d'un mot (« aplanis3 : ») ;
- un chiffre isolé après un mot et suivi d'une ponctuation (« peines 2. »), jamais après une abréviation de
  référence (Ps., chap., Matth. 5…).
Jamais « ° » (« 1 ° » est un ordinal), jamais à l'intérieur d'un mot. Rejouable : un second passage ne trouve plus rien.
"""
import json, re, sys
F = sys.argv[1]
REF = set("chap chapitre ch ps psaume liv livre lib tome t p page n no art serm sermon hom homil ép épître lettre c part partie sect section méd méditation v vers verset cap ep epist tract q qu dist l les des ces nos vos mes ses leurs".split())
# pas devant une majuscule : « en * Sic Deus… » est le début d'une note restée dans le texte, pas un appel
isole_signe = re.compile(r"(?<=[\wà-ÿœ»!?…,;:.)]) ['\"“”*•·¹²³]{1,2}(?=[.,;:!?)»]|\s(?![A-ZÀ-Ý])|$)")
colle_signe = re.compile(r"(?<=[a-zà-ÿœ»!?…])[*•¹²³\"”“](?=[\s.,;:!?)»]|$)")
colle = re.compile(r"(?<=[a-zà-ÿœ»!?…])([1-9¹²³])(?=[\s.,;:!?»)]|$)")
isole = re.compile(r"(\w+|[!?…»]) ([1-9])(?=[.,;:!?»)](?:\s|$))")
d = json.load(open(F)); n = 0; ex = []


def note(p, m):
    global n
    n += 1
    if len(ex) < 60: ex.append(p[max(0, m.start() - 30):m.end() + 12].replace('\n', ' '))


for e in d['entrees']:
    corps, sep, notes = e['corps'].partition('\n\n### Notes\n\n')
    P = corps.split('\n\n')
    for i, p in enumerate(P):
        if p.startswith('#'): continue
        def f(m, p=p):
            note(p, m); return ''
        def g(m, p=p):
            if m.group(1).lower() in REF or m.group(1)[0].isupper() or m.group(1).isdigit(): return m.group(0)
            note(p, m); return m.group(1)
        p = isole_signe.sub(f, p)
        p = colle_signe.sub(f, p)
        p = colle.sub(f, p)
        p = isole.sub(g, p)
        # « mot ; » : l'espace qui précédait l'appel reste devant la ponctuation haute, comme imprimé
        P[i] = re.sub(r" {2,}", " ", p).rstrip()
    e['corps'] = '\n\n'.join(P) + sep + notes
print('appels retirés', n); print('\n'.join(ex))
if '--ecrire' in sys.argv: json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1); open(F, 'a').write('\n')
