"""Hamon : chapitres des références bibliques mal lus par l'OCR (« (1 Cor., 117, 27.) » pour « (I Cor., xii, 27.) »).

Usage : python3 -I references.py <hamon.json> <dossier data/ecriture> [--ecrire]

Hamon note toujours le chapitre en chiffres romains (« Rom., vi, 5 », « Ps. cxxix »). Un chapitre en chiffres arabes,
ou un mélange de chiffres et de lettres (« 11 », « 117 », « 1v », « Ix », « XV1 », « ILIV »), est donc une faute de
lecture. On essaie les lectures possibles (1, l, 7, ! → i ; 0 → o puis rien…), et l'on garde le chapitre dont le
verset, dans la Vulgate clémentine (data/ecriture), contient la citation : au moins 60 % de ses mots, avec un écart
net sur les autres lectures. Rien n'est changé sans cet accord ; les cas restants sont listés (à voir sur le scan).
La casse du livre est gardée (« xii » si le livre imprime en minuscules, « XII » sinon) ; « 1 Cor. » devient « I Cor. »
quand le chiffre arabe est la même faute. Rejouable.
"""
import itertools, json, os, re, sys, unicodedata

F, ECR = sys.argv[1], sys.argv[2]
LIVRES = {
    'matth': 'mt', 'math': 'mt', 'mat': 'mt', 'marc': 'mc', 'luc': 'lc', 'joan': 'jn', 'jo': 'jn', 'act': 'ac',
    'rom': 'rm', 'cor': 'co', 'gal': 'ga', 'eph': 'ep', 'ephes': 'ep', 'philip': 'ph', 'philipp': 'ph', 'phil': 'ph',
    'col': 'col', 'coloss': 'col', 'colos': 'col', 'thess': 'th', 'tim': 'tm', 'tit': 'tt', 'hebr': 'he', 'heb': 'he',
    'jac': 'jc', 'petr': 'p', 'pet': 'p', 'apoc': 'ap', 'ps': 'ps', 'psalm': 'ps', 'prov': 'pr', 'eccles': 'qo',
    'eccle': 'qo', 'eccli': 'si', 'sap': 'sg', 'cant': 'ct', 'is': 'is', 'isai': 'is', 'jer': 'jr', 'thren': 'lm',
    'ezech': 'ez', 'dan': 'dn', 'os': 'os', 'joel': 'jl', 'amos': 'am', 'mich': 'mi', 'habac': 'ha', 'zach': 'za',
    'mal': 'ml', 'gen': 'gn', 'exod': 'ex', 'ex': 'ex', 'lev': 'lv', 'num': 'nb', 'deut': 'dt', 'tob': 'tb',
    'judith': 'jdt', 'job': 'jb', 'mach': 'm', 'bar': 'ba', 'sophon': 'so',
}
NUMEROTES = {'co', 'th', 'tm', 'p', 'm'}  # livres qui demandent I, II
ROM = [(100, 'c'), (90, 'xc'), (50, 'l'), (40, 'xl'), (10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')]


def romain(n):
    s = ''
    for v, r in ROM:
        while n >= v: s += r; n -= v
    return s


def valeur(r):
    r = r.lower()
    if not r or not re.fullmatch(r"[ivxlc]+", r): return None
    vals = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100}
    t = 0
    for a, b in itertools.zip_longest(r, r[1:]):
        t += -vals[a] if b and vals[b] > vals[a] else vals[a]
    return t if romain(t) == r else None


# confusions d'OCR sur un chiffre romain
CONF = {'1': 'ilx', 'l': 'ilx', 'I': 'ilx', '7': 'il', '5': 'v', '!': 'i', 'j': 'i', 'J': 'i', 'y': 'v', 'u': 'v', 'n': 'ii', 'm': 'iii',
        'L': 'li', 'X': 'x', 'x': 'x', 'V': 'v', 'v': 'v', 'C': 'c', 'c': 'c', 'G': 'c', 'W': 'x', 'S': 'x', 'Z': 'x'}


def lectures(tok):
    choix = [CONF.get(ch, '') or ch.lower() for ch in tok]
    res = set()
    for combo in itertools.product(*[list(c) for c in choix]):
        r = ''.join(combo); v = valeur(r)
        if v: res.add(v)
    return res


def norm(s):
    s = unicodedata.normalize('NFD', s.lower().replace('æ', 'ae').replace('œ', 'oe'))
    return [w for w in re.findall(r"[a-z]+", s.replace('j', 'i').replace('v', 'u')) if len(w) > 2]


BIBLE = {}


def verset(livre, c, v):
    if livre not in BIBLE:
        p = os.path.join(ECR, livre + '.json')
        BIBLE[livre] = json.load(open(p)) if os.path.exists(p) else None
    b = BIBLE[livre]
    if not b or c < 1 or c > len(b['chapitres']): return ''
    ch = b['chapitres'][c - 1]
    return ' '.join(t for n, t in ch['la'] if v - 1 <= n <= v + 1)


REF = re.compile(r"(?P<cit>[^()]{6,300}?)\(\s?(?P<num>[1I]{1,2}|[1I]{1,2}\s)?\s?(?P<livre>[A-Z][a-z]{1,8})\s?\.?\s?,?\s(?P<ch>[0-9IVXLCivxlc!jJymnWSZG]{1,7})\s?[,.]\s?(?P<v>\d{1,3})")
d = json.load(open(F))
faits, restes = [], []
for e in d['entrees']:
    c = e['corps']
    sortie, k = [], 0
    for m in REF.finditer(c):
        cle = m.group('livre').lower().rstrip('.')
        livre = LIVRES.get(cle)
        tok = m.group('ch')
        if not livre: continue
        if re.fullmatch(r"[ivxlc]+|[IVXLC]+", tok) and valeur(tok): continue  # déjà juste
        num = (m.group('num') or '').strip()
        if livre in NUMEROTES:
            if not num: continue
            livre = {'1': '1', 'I': '1', '11': '2', 'II': '2', 'Il': '2', '1I': '2', 'I1': '2'}.get(num, '') + livre
        mots = norm(re.sub(r".*[.!?:;]\s", '', m.group('cit').rstrip(' .!?;:,')))[-12:]  # la dernière phrase avant la référence
        if len(mots) < 2: continue
        v = int(m.group('v'))
        scores = sorted(((sum(w in set(norm(verset(livre, ch, v))) for w in mots) / len(mots), ch) for ch in lectures(tok)), reverse=True)
        ctx = c[m.start('livre') - 6:m.end('v') + 3]
        if scores and scores[0][0] >= 0.6 and (len(scores) == 1 or scores[0][0] - scores[1][0] >= 0.25):
            ch = scores[0][1]
            r = romain(ch) if (tok.islower() or not any(x in tok for x in 'IVXLC')) else romain(ch).upper()
            # le livre imprime en minuscules (« Rom., vi, 5 ») : on garde les minuscules
            r = romain(ch)
            sortie.append((m.start('ch'), m.end('ch'), r))
            if num and num != num.replace('1', 'I'):
                sortie.append((m.start('num'), m.start('num') + len(num), num.replace('1', 'I')))
            faits.append(f"{e['cle']}\t{ctx}\t→ {r}\t({scores[0][0]:.0%})")
        else:
            restes.append(f"{e['cle']}\t{ctx}\t{[(round(s, 2), romain(x)) for s, x in scores[:3]]}")
    for a, b, r in sorted(sortie, reverse=True):
        c = c[:a] + r + c[b:]
    e['corps'] = c
print('corrigées', len(faits), 'restent', len(restes))
print('\n'.join(faits[:40]))
if len(sys.argv) > 3 and sys.argv[3] != '--ecrire':
    open(sys.argv[3], 'w').write('# corrigées\n' + '\n'.join(faits) + '\n\n# restent (à voir sur le scan)\n' + '\n'.join(restes))
if '--ecrire' in sys.argv: json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1); open(F, 'a').write('\n')
