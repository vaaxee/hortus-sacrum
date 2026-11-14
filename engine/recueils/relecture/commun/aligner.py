"""Alignement de deux lectures OCR (archive.org djvu + Tesseract) d'un livre, page par page.

Usage : python3 aligner.py <dossier> <suffixe>   (lit pages<s>.json, tess<s>/<n>.tsv ; écrit merged<s>.json, flags<s>.json)
Décision par désaccord :
 1. lettres identiques (seule la ponctuation diffère) : lecture propre (sans ^ | < > …) ;
 2. une seule lecture faite de mots connus (dictionnaire fr + mots sur lesquels les deux lectures s'accordent ailleurs) : celle-là ;
 3. les deux connues ou inconnues : on compare les bigrammes avec les mots voisins, comptés dans le texte où les deux
    lectures s'accordent ; si l'une est attestée et l'autre jamais (ou 4 fois moins), elle l'emporte ;
 4. sinon : signalé pour relecture sur l'image.
"""
import collections, csv, difflib, json, math, re, sys, unicodedata
from spellchecker import SpellChecker

D, S = sys.argv[1], sys.argv[2]
sp = SpellChecker(language='fr')
pages = json.load(open(f'{D}/pages{S}.json'))
BAD = re.compile(r"[\^£<>|\[\]{}~*#@&$§]|^'|'$|\d[a-zA-Z]|[a-zA-Z]\d")


def key(w):
    w = unicodedata.normalize('NFC', w).replace('’', "'").replace('‘', "'")
    w = re.sub(r"'+", "'", w)
    return re.sub(r"[^\wÀ-ÿœŒæ']|_", "", w).lower()


def tess(i):
    ws = []
    try:
        with open(f'{D}/tess{S}/{i}.tsv', encoding='utf-8') as f:
            for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE):
                if r['level'] == '5' and r['text'].strip():
                    ws.append((r['text'].replace('’', "'"), (int(r['left']), int(r['top']), int(r['width']), int(r['height']))))
    except FileNotFoundError:
        pass
    return ws


agree = collections.Counter(); big = collections.Counter()
ops_all = {}
for i, p in enumerate(pages):
    A = [(w, li, c) for li, l in enumerate(p) for w, c in l]
    T = tess(i)
    ka = [key(w) for w, _, _ in A]; kb = [key(w) for w, _ in T]
    ops = difflib.SequenceMatcher(None, ka, kb, autojunk=False).get_opcodes()
    ops_all[i] = (A, T, ka, kb, ops)
    for tag, a1, a2, b1, b2 in ops:
        if tag == 'equal':
            seq = ka[a1:a2]
            for k in seq:
                for x in re.split(r"['\-]", k):
                    if x: agree[x] += 1
            for x, y in zip(seq, seq[1:]): big[(x, y)] += 1


def known(w):
    k = key(w)
    if not k: return True
    if k.isdigit(): return True
    if BAD.search(w): return False
    return all(x in sp or agree[x] >= 2 for x in re.split(r"['\-]", k) if x)


def score(prev, words, nxt):
    ks = [k for k in (key(w) for w in words) if k]
    if not ks: return 0
    seq = ([prev] if prev else []) + ks + ([nxt] if nxt else [])
    return sum(big[(x, y)] for x, y in zip(seq, seq[1:]))


merged = {}; flags = []
for i, (A, T, ka, kb, ops) in ops_all.items():
    out = []
    for tag, a1, a2, b1, b2 in ops:
        if tag == 'equal':
            for k, kb_ in zip(range(a1, a2), range(b1, b2)):
                aw, bw = A[k][0], T[kb_][0]
                out.append((bw if BAD.search(aw) and not BAD.search(bw) else aw, A[k][1], None))
            continue
        aw = [A[k][0] for k in range(a1, a2)]; bw = [T[k][0] for k in range(b1, b2)]
        line = A[a1][1] if a1 < len(A) else (A[-1][1] if A else 0)
        keep = lambda: [(w, A[k][1], None) for w, k in zip(aw, range(a1, a2))]
        while bw and not key(bw[0]): bw = bw[1:]
        while bw and not key(bw[-1]): bw = bw[:-1]
        ja = ''.join(key(w) for w in aw); jb = ''.join(key(w) for w in bw)
        if not bw: out += keep(); continue
        if not aw:
            if all(known(w) and len(key(w)) >= 2 for w in bw) and len(jb) >= 4 and score(ka[a1-1] if a1 else '', bw, ka[a1] if a1 < len(ka) else '') > 0:
                out += [(w, line, None) for w in bw]
            continue
        if ja == jb or ja.replace('â', 'a') == jb.replace('â', 'a'):
            out += [(w, line, None) for w in bw] if any(BAD.search(w) for w in aw) and not any(BAD.search(w) for w in bw) else keep(); continue
        if all(re.fullmatch(r"[\d—–\-| .]*", w) for w in aw): out += keep(); continue
        ak = all(known(w) for w in aw); bk = all(known(w) for w in bw)
        if bk and not ak: out += [(w, line, None) for w in bw]; continue
        if ak and not bk: out += keep(); continue
        prev = ka[a1 - 1] if a1 else ''; nxt = ka[a2] if a2 < len(ka) else ''
        sa, sb = score(prev, aw, nxt), score(prev, bw, nxt)
        if sb > 0 and sb >= 4 * max(sa, 0.5) and bk: out += [(w, line, None) for w in bw]; continue
        if sa > 0 and sa >= 4 * max(sb, 0.5) and ak: out += keep(); continue
        if ak and bk and len(ja) <= 2 and len(jb) <= 2 and sa >= sb: out += keep(); continue
        box = None
        if b1 < b2:
            xs = [T[k][1] for k in range(b1, b2)]
            box = (min(x[0] for x in xs), min(x[1] for x in xs), max(x[0] + x[2] for x in xs), max(x[1] + x[3] for x in xs))
        boxA = [A[k][2] for k in range(a1, min(a2, len(A)))]
        flags.append({'id': len(flags), 'page': i, 'a': ' '.join(aw), 'b': ' '.join(bw), 'box': box, 'boxA': boxA,
                      'ctx': ' '.join(x[0] for x in A[max(0, a1 - 5):a2 + 5])})
        out.append((f'⟦{len(flags) - 1}⟧', line, len(flags) - 1))
    merged[i] = out
json.dump(merged, open(f'{D}/merged{S}.json', 'w'), ensure_ascii=False)
json.dump(flags, open(f'{D}/flags{S}.json', 'w'), ensure_ascii=False)
print(S, 'pages', len(pages), 'désaccords à revoir', len(flags))
