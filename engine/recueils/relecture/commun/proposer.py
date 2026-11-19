"""Propose des corrections sûres de fautes d'OCR typiques, sous forme de décisions (format de remplacer.py).

Usage : python3 -I proposer.py <recueil.json> [vulgate.json] > decisions_auto.txt

Règles (le mot fautif doit être inconnu : ni dictionnaire, ni Vulgate, ni ≥ 3 fois dans data/recueils) :
  R1 recoller  « néces sité » → « nécessité » : deux morceaux séparés d'une espace dont l'un au moins est inconnu
               et dont la réunion est un mot connu (fréquent dans les recueils, ≥ 3) ;
  (R2, R3 : pas quand un mot voisin est inconnu, signe d'un mot coupé en morceaux ; pas d'accents, graphie du livre)
  R2 décoller  « dansla » → « dans la », « saintJoseph » → « saint Joseph » : une seule coupure donne deux mots
               courants (≥ 30 fois dans les recueils, dictionnaire) ;
  R3 lettres   « cngendre » → « engendre » : une seule substitution parmi les confusions d'OCR connues (c/e, n/u,
               rn/m, li/h, ii/u, l/t, f/t…) donne un mot connu, et une seule.
On s'abstient près du latin (mot voisin latin et non français) et sur les mots en capitale initiale pour R3.
Chaque proposition porte le mot d'avant et d'après pour être unique ; remplacer.py ignore les ambiguës.
"""
import collections, glob, json, os, re, sys
from spellchecker import SpellChecker

F = sys.argv[1]
VUL = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/vul/v.json'
sp = SpellChecker(language='fr')
L = r"A-Za-zÀ-ÿœŒæÆ"
MOT = rf"[{L}]+"
LAT = set()
try:
    for b in json.load(open(VUL))['books']:
        for c in b['chapters']:
            for v in c['verses']: LAT.update(w.lower() for w in re.findall(MOT, v['text']))
except Exception:
    pass
corpus = collections.Counter()
for g in glob.glob(os.path.join(os.path.dirname(os.path.abspath(F)), '*.json')):
    for e in json.load(open(g)).get('entrees', []):
        for k in ('corps', 'sommaire', 'titre'):
            if isinstance(e.get(k), str): corpus.update(w.lower() for w in re.findall(MOT, e[k]))


def connu(w):
    x = w.lower()
    return x in sp or x in LAT or corpus[x] >= 3


def francais(w):
    x = w.lower()
    return x in sp and corpus[x] >= 3


def latin(w):
    x = w.lower()
    return x in LAT and x not in sp


CONF = [('ceu', 'œu'), ('c', 'e'), ('e', 'c'), ('n', 'u'), ('u', 'n'), ('rn', 'm'), ('m', 'rn'), ('li', 'h'), ('h', 'li'), ('ii', 'u'),
        ('l', 't'), ('t', 'l'), ('f', 't'), ('t', 'f'), ('i', 'l'), ('l', 'i'), ('h', 'b'), ('b', 'h'), ('cl', 'd'),
        ('o', 'e'), ('e', 'o'), ('s', 'e'), ('a', 'e'), ('æ', 'œ'), ('cæ', 'cœ'), ('æu', 'œu'),
        ('r', 'n'), ('n', 'r'), ('v', 'y'), ('y', 'v'),
        ('in', 'm'), ('m', 'in'), ('ni', 'm'), ('fi', 'li'), ('ti', 'fi'), ('s', 'a'), ('o', 'c'), ('c', 'o'), ('q', 'g'), ('g', 'q')]


OUTILS = set('de la le les que qui et en du des ne se ce sa son ses lui me je il ils au aux par pour sur dans un une tout toute toutes tous nous vous est mon ma mes si plus sans avec comme mais ou on elle elles leur leurs notre nos votre vos y à ô a été être avoir fait dit peu bien même ces cette cet ton ta tes te pas point'.split())
FRAG = {'us', 'ment', 'ni', 'ai', 'ma', 'ne', 'ra', 'rai', 'ras', 'ront', 'rons', 'ez', 'ons', 'es', 'as', 'ait'}


def variantes(w):
    out = set()
    for a, b in CONF:
        i = w.find(a)
        while i >= 0:
            v = w[:i] + b + w[i + len(a):]
            if francais(v): out.add(v)
            i = w.find(a, i + 1)
    return out


d = json.load(open(F))
props = []  # (règle, avant, après)
TOK = re.compile(rf"[{L}]+|[^{L}]")
for e in d['entrees']:
    for k in ('titre', 'sommaire', 'corps'):
        t = e.get(k)
        if not isinstance(t, str): continue
        ms = list(re.finditer(MOT, t))
        for j, m in enumerate(ms):
            w = m.group(0)
            prev = ms[j - 1] if j else None
            nxt = ms[j + 1] if j + 1 < len(ms) else None
            near_lat = any(x is not None and latin(x.group(0)) for x in (prev, nxt))
            # R1 : w et le mot suivant séparés par une seule espace
            if nxt and t[m.end():nxt.start()] == ' ' and not (w.lower() in sp and nxt.group(0).lower() in sp and corpus[w.lower()] >= 30 and corpus[nxt.group(0).lower()] >= 30):
                z = w + nxt.group(0)
                n2 = nxt.group(0)
                bloque = (len(w) < 2 or len(n2) < 2 or t[nxt.end():nxt.end() + 1] in "'’"
                          or (w.lower() in OUTILS and n2.lower() in sp) or (n2.lower() in OUTILS and w.lower() in sp))
                if not bloque and francais(z) and corpus[z.lower()] >= 3 and not near_lat and nxt.group(0)[0].islower():
                    a0 = prev.group(0) + t[prev.end():m.start()] if prev else ''
                    props.append(('R1', a0 + w + ' ' + nxt.group(0), a0 + z, (id(e), k, m.start(), nxt.end())))
                    continue
            if connu(w): continue
            # mot voisin inconnu : sans doute un mot coupé en morceaux, on laisse à l'œil
            if any(x is not None and not (x.group(0).lower() in sp or x.group(0).lower() in OUTILS) for x in (prev, nxt)): continue
            # R2
            cands = []
            for i in range(2, len(w) - 1):
                x, y = w[:i], w[i:]
                ok = lambda s: (s.lower() in sp and corpus[s.lower()] >= 30) or s.lower() in ('à', 'a', 'y', 'ô')
                if w[0].isupper() or y.lower() in FRAG: continue
                if not (x.lower() in OUTILS or y.lower() in OUTILS): continue
                if ok(x) and ok(y) and (y[0].islower() or y[0].isupper() and y[1:].islower()):
                    cands.append((x, y))
            if len(cands) == 1 and not near_lat:
                x, y = cands[0]
                a0 = (prev.group(0) + t[prev.end():m.start()]) if prev else ''
                a1 = (t[m.end():nxt.start()] + nxt.group(0)) if nxt else ''
                props.append(('R2', a0 + w + a1, a0 + x + ' ' + y + a1, (id(e), k, m.start(), m.end())))
                continue
            # R3
            if w[0].isupper() or near_lat or len(w) < 4: continue
            v = variantes(w)
            if len(v) == 1:
                b = v.pop()
                # morceau d'un mot coupé (« néces saire ») : la réunion avec un voisin serait un mot
                if any(francais(x) for x in ((prev.group(0) + b) if prev else '', (b + nxt.group(0)) if nxt else '',
                                              (prev.group(0) + w) if prev else '', (w + nxt.group(0)) if nxt else '')): continue
                if any(x is not None and len(x.group(0)) <= 4 and x.group(0).lower() not in OUTILS for x in (prev, nxt)): continue
                a0 = (prev.group(0) + t[prev.end():m.start()]) if prev else ''
                a1 = (t[m.end():nxt.start()] + nxt.group(0)) if nxt else ''
                props.append(('R3', a0 + w + a1, a0 + b + a1, (id(e), k, m.start(), m.end())))
# deux propositions sur des mots qui se touchent (« son der nier », « tra vail le ») : on laisse à l'œil
bord = collections.defaultdict(list)
for i, (_, _, _, (e_, k_, s0, s1)) in enumerate(props): bord[(e_, k_)].append((s0, s1, i))
exclus = set()
for v in bord.values():
    v.sort()
    for (a0, a1, i), (b0, b1, j) in zip(v, v[1:]):
        if b0 <= a1 + 1: exclus.update((i, j))
seen = set()
for n, (r, a, b, _) in enumerate(props):
    if n in exclus: continue
    if (a, b) in seen: continue
    seen.add((a, b))
    a, b = a.replace('\n', '\\n'), b.replace('\n', '\\n')
    print(f'{a}\t{b}\t# {r}')
