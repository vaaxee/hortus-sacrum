"""Hamon : trie les désaccords entre les deux lectures, prudemment.

Usage : python3 -I decider.py <dossier> <suffixe> <hamon.json>
Lecture A = couche texte Google (pages<S>.json), lecture B = Tesseract (tess<S>/<i>.tsv).
Pour chaque mot où A et B diffèrent (alignement mot à mot, remplacements un pour un seulement) :
  - A est un mot connu (dictionnaire, Vulgate, ou mot fréquent du livre)  → on garde A ;
  - A est un morceau de mot coupé en fin de ligne (trait d'union)          → on garde A (recollé ailleurs) ;
  - A inconnu, B connu, mêmes signes autour, distance d'édition ≤ 2, B fait de lettres
                                                                           → correction automatique ;
  - sinon, A inconnu                                                       → signalé, à trancher sur l'image.
Écrit corrections<S>.json : [{page, avant, a, b, apres, auto, box}] (avant/apres : mots voisins de A, pour retrouver
l'endroit dans hamon.json).
"""
import collections, csv, difflib, json, os, re, sys, unicodedata
from spellchecker import SpellChecker

D, S, HAMON = sys.argv[1], sys.argv[2], sys.argv[3]
sp = SpellChecker(language='fr')
LATIN = set()
try:
    for b in json.load(open(os.environ.get('VULGATE', '/tmp/claude-0/vul/v.json')))['books']:
        for c in b['chapters']:
            for v in c['verses']:
                LATIN.update(w.lower() for w in re.findall(r'[a-zæœA-ZÆŒ]+', v['text']))
except Exception:
    pass
MOT = r"[A-Za-zÀ-ÿœŒæÆ]+"
voc = collections.Counter(w.lower() for e in json.load(open(HAMON))['entrees'] for w in re.findall(MOT, e.get('corps', '') + ' ' + e.get('sommaire', '')))


def cle(w):
    w = unicodedata.normalize('NFC', w).replace('’', "'")
    return re.sub(r"[^\wÀ-ÿœŒæÆ']|_", '', w).lower().strip("'")


ROMAIN = re.compile(r"^\(?[IVXLCivxlc]+[,.;)]*$")
def connu(w):
    if ROMAIN.match(w.strip()) or re.fullmatch(r"\d+[ºo°]?[,.;:]?", w.strip()): return True
    w = re.sub(r"[\d*†‘’\u00b9\u00b2\u00b3]+([.,;:!?»]*)$", r"\1", w)  # appel de note collé au mot
    k = cle(w)
    if not k or k.isdigit(): return True
    parts = [x for x in re.split(r"['\-]", k) if x]
    return all(x in sp or x in LATIN or voc[x] >= 4 for x in parts)


def lettres(w): return re.sub(r"[^A-Za-zÀ-ÿœŒæÆ'’\-]", '', w)


def bords(w):
    m = re.match(r"^(\W*)(.*?)(\W*)$", w)
    return m.group(1), m.group(3)


def dist(x, y):
    d = list(range(len(y) + 1))
    for i, cx in enumerate(x, 1):
        p, d[0] = d[0], i
        for j, cy in enumerate(y, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (cx != cy))
    return d[-1]


def tess(i):
    out = []
    try:
        with open(f'{D}/tess{S}/{i}.tsv', encoding='utf-8') as f:
            for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE):
                if r['level'] == '5' and r['text'].strip():
                    out.append((r['text'], (int(r['left']), int(r['top']), int(r['width']), int(r['height']))))
    except FileNotFoundError:
        pass
    return out


pages = json.load(open(f'{D}/pages{S}.json'))
corr = []
for i, p in enumerate(pages):
    A = []  # (mot, boîte, fragment ?)
    for li, l in enumerate(p):
        for k, (w, bx) in enumerate(l):
            frag = (k == len(l) - 1 and w.endswith('-')) or (k == 0 and li and p[li - 1][-1][0].endswith('-'))
            A.append((w, bx, frag))
    B = tess(i)
    ka, kb = [cle(w) for w, _, _ in A], [cle(w) for w, _ in B]
    for tag, a1, a2, b1, b2 in difflib.SequenceMatcher(None, ka, kb, autojunk=False).get_opcodes():
        if tag != 'replace' or a2 - a1 != b2 - b1: continue
        for ia, ib in zip(range(a1, a2), range(b1, b2)):
            a, bx, frag = A[ia]; b = B[ib][0]
            if frag or connu(a) or not cle(a): continue
            if b.rstrip().endswith('-'): continue  # mot coupé en fin de ligne : A le recolle avec la ligne suivante
            avant = A[ia - 1][0] if ia else ''
            apres = A[ia + 1][0] if ia + 1 < len(A) else ''
            ba, bb = bords(a), bords(b)
            coeur = re.sub(r'^\W+|\W+$', '', b)
            auto = (connu(b) and ba == bb and re.fullmatch(r"[A-Za-zÀ-ÿœŒæÆ'’\-]+", coeur) is not None
                    and len(cle(b)) >= 3 and len(cle(a)) == len(cle(b)) and dist(cle(a), cle(b)) <= 2
                    and not ROMAIN.match(b.strip()))
            corr.append({'page': i, 'avant': avant, 'a': a, 'b': b, 'apres': apres, 'auto': bool(auto), 'box': B[ib][1]})
json.dump(corr, open(f'{D}/corrections{S}.json', 'w'), ensure_ascii=False)
n = collections.Counter(c['auto'] for c in corr)
print(f'{S} : {len(pages)} pages ; corrections automatiques {n[True]} ; à trancher sur l\'image {n[False]}')
