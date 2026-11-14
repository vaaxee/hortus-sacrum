"""Hamon : passe de nettoyage sûre sur data/recueils/hamon.json (sans toucher au sens).

Règles, chacune vérifiée sur un échantillon du scan :
 1. « cœur » mal lu (cæur, ceur, caur, cæurs…) → cœur(s) ; « ſ » → « s » long lu pour f/s : seulement « ſ » isolé → f ;
 2. mots coupés en fin de ligne restés en deux morceaux (« satisfac tion ») : recollés si l'un des morceaux n'est pas
    un mot et que le mot entier l'est (dictionnaire français + mots du livre lui-même) ;
 3. « a- t-il », « n'a -t-il » : trait d'union recollé ;
 4. débris d'une lettre isolée au milieu d'un mot coupé (« Incar T nation ») : retiré si le mot recollé est connu ;
 5. paragraphes faits seulement d'un numéro de page : retirés.
Usage : python3 -I nettoyer.py <hamon.json> [--ecrire]
"""
import collections, json, re, sys
from spellchecker import SpellChecker

F = sys.argv[1]
d = json.load(open(F))
sp = SpellChecker(language='fr')
MOT = r"[A-Za-zÀ-ÿœŒæÆ]+"
# vocabulaire du livre : mots qui reviennent souvent tels quels (noms propres, latin, mots rares)
voc = collections.Counter(w.lower() for e in d['entrees'] for w in re.findall(MOT, e.get('corps', '') + ' ' + e.get('sommaire', '')))
connu = lambda w: w.lower() in sp or voc[w.lower()] >= 4
stats = collections.Counter()
exemples = collections.defaultdict(list)

def note(regle, avant, apres):
    stats[regle] += 1
    if len(exemples[regle]) < 12: exemples[regle].append((avant, apres))

def coeur(m):
    note('cœur', m.group(0), m.group(1) + 'œur' + m.group(2))
    return m.group(1) + 'œur' + m.group(2)

def recoller(m):
    a, b = m.group(1), m.group(2)
    if (connu(a) and connu(b)) or not connu(a + b) or len(a + b) < 5: return m.group(0)
    note('recollé', f'{a} {b}', a + b)
    return a + b

def debris(m):
    a, x, b = m.group(1), m.group(2), m.group(3)
    if connu(a + b) and not connu(a) and len(a + b) >= 5:
        note('débris', f'{a} {x} {b}', a + b)
        return a + b
    return m.group(0)

def nettoyer(t):
    t = re.sub(r'\b([cC])(?:æ|ae|e|a)ur(s?)\b', coeur, t)
    t = re.sub(r'\bſ', 'f', t)
    t = re.sub(rf'\b({MOT}) ([A-Za-z]) ({MOT})\b', debris, t)
    t = re.sub(rf'\b({MOT}) ({MOT})\b', recoller, t)
    t2 = re.sub(r"(\w)- ?-?(t-(?:il|elle|on|ils|elles))\b", r'\1-\2', t)
    t2 = re.sub(r"(\w) -(t-(?:il|elle|on|ils|elles))\b", r'\1-\2', t2)
    if t2 != t: stats['-t-il'] += 1
    t = t2
    t3 = re.sub(r'\n\n\d{1,3}\n\n', '\n\n', t)
    if t3 != t: stats['numéro de page'] += 1
    return t3

for e in d['entrees']:
    for k in ('corps', 'sommaire'):
        if e.get(k): e[k] = nettoyer(e[k])
print(dict(stats))
for r, ex in exemples.items(): print(r, ex)
if '--ecrire' in sys.argv:
    json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
