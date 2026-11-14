"""Hamon : applique les corrections (automatiques et tranchées sur l'image) au texte de data/recueils/hamon.json.
Usage : python3 -I appliquer.py <dossier> <suffixe> <hamon.json> [--ecrire]
Une correction est appliquée seulement si « mot avant + A + mot après » se trouve une seule fois dans le livre
(le texte de l'app a déjà été nettoyé : « cæur » y est déjà « cœur », etc.)."""
import json, re, sys
D, S, F = sys.argv[1], sys.argv[2], sys.argv[3]
C = json.load(open(f'{D}/corrections{S}.json'))
dec = {}
try:
    for l in open(f'{D}/dec{S}.txt', encoding='utf-8'):
        if '\t' in l:
            k, v = l.rstrip('\n').split('\t', 1); dec[int(k)] = v
except FileNotFoundError:
    pass
d = json.load(open(F))
champs = [(e, k) for e in d['entrees'] for k in ('corps', 'sommaire') if e.get(k)]
ok = absent = multiple = garde = 0
for i, c in enumerate(C):
    if c['auto']: b = c['b']
    elif i in dec: b = {'A': c['a'], 'B': c['b']}.get(dec[i], dec[i])
    else: continue
    if b == c['a']: garde += 1; continue
    av, ap = re.escape(c['avant']), re.escape(c['apres'])
    motif = re.compile(rf"({av}\s+){re.escape(c['a'])}(\s+{ap})" if c['avant'] and c['apres'] else rf"(\s){re.escape(c['a'])}(\s)")
    trouves = [(e, k) for e, k in champs if motif.search(e[k])]
    n = sum(len(motif.findall(e[k])) for e, k in trouves)
    if n == 0: absent += 1; continue
    if n > 1: multiple += 1; continue
    e, k = trouves[0]
    e[k] = motif.sub(lambda m: m.group(1) + b + m.group(2), e[k])
    ok += 1
print(f'appliquées {ok} ; gardées telles quelles {garde} ; introuvables {absent} (déjà corrigées ou coupées) ; ambiguës {multiple}')
if '--ecrire' in sys.argv: json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
