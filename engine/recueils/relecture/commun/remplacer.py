"""Applique une liste de décisions de relecture à un recueil JSON (data/recueils/*.json).

Usage : python3 -I remplacer.py <recueil.json> <decisions.txt> [--ecrire]

Format des décisions, une par ligne (lignes vides et « # … » ignorées) :
    texte fautif<TAB>texte corrigé            → remplacé s'il se trouve une seule fois dans le recueil
    texte fautif<TAB>texte corrigé<TAB>*      → remplacé partout (fautes répétées sans ambiguïté)
Le texte fautif contient assez de contexte pour être unique ; « \\n » y désigne un saut de ligne. Il n'est
jamais cherché à l'intérieur d'un mot plus long.
Les champs relus : titre, sommaire, corps. Une décision déjà appliquée (texte fautif absent, texte corrigé
présent) est comptée « déjà faite », ce qui permet de rejouer la liste.
"""
import json, re, sys
L = 'A-Za-zÀ-ÿœŒæÆ'


def motif(a):
    """Le texte fautif, sans déborder sur un mot plus long (« nai » ne doit pas toucher « connaissance »)."""
    return re.compile((f'(?<![{L}])' if a[:1].isalpha() else '') + re.escape(a) + (f'(?![{L}])' if a[-1:].isalpha() else ''))

F, DEC = sys.argv[1], sys.argv[2]
d = json.load(open(F, encoding='utf-8'))
champs = [(e, k) for e in d['entrees'] for k in ('titre', 'sommaire', 'corps') if isinstance(e.get(k), str)]
ok = deja = absent = multiple = 0
for n, l in enumerate(open(DEC, encoding='utf-8'), 1):
    l = l.rstrip('\n')
    if not l.strip() or l.startswith('#'): continue
    parts = l.split('\t')
    if len(parts) < 2:
        print(f'ligne {n} mal formée : {l!r}'); continue
    a, b = parts[0].replace('\\n', '\n'), parts[1].replace('\\n', '\n')
    partout = len(parts) > 2 and parts[2] == '*'
    rx = motif(a)
    ou = [(e, k) for e, k in champs if a in e[k]]
    tot = sum(len(rx.findall(e[k])) for e, k in ou)
    if tot == 0:
        if any(b in e[k] for e, k in champs): deja += 1
        else: absent += 1; print(f'introuvable (l. {n}) : {a!r}')
        continue
    if tot > 1 and not partout:
        multiple += 1; print(f'ambiguë ×{tot} (l. {n}) : {a!r}'); continue
    for e, k in ou:
        e[k] = rx.sub(lambda _: b, e[k])
    ok += tot
print(f'{F} : {ok} remplacements ; déjà faits {deja} ; introuvables {absent} ; ambiguës {multiple}')
if '--ecrire' in sys.argv:
    json.dump(d, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
