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
# lexique latin : mots de la Vulgate clémentine (si le fichier est là), pour les citations
LATIN = set()
try:
    import os
    _v = os.environ.get('VULGATE', '/tmp/claude-0/vul/v.json')
    for _b in json.load(open(_v))['books']:
        for _c in _b['chapters']:
            for _x in _c['verses']:
                for _w in re.findall(r"[a-zæœA-ZÆŒ]+", _x['text']): LATIN.add(_w.lower())
except Exception:
    pass
pages = json.load(open(f'{D}/pages{S}.json'))
BAD = re.compile(r"[\^£<>|\[\]{}~*#@&$§]|^'|'$|\d[a-zA-Z]|[a-zA-Z]\d")


def key(w):
    w = unicodedata.normalize('NFC', w).replace('’', "'").replace('‘', "'")
    w = re.sub(r"'+", "'", w)
    return re.sub(r"[^\wÀ-ÿœŒæ']|_", "", w).lower().strip("'")


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
sp.word_frequency.load_words(LATIN)
_cache = {}
def proche(a, b):
    """Mot connu le plus proche des deux lectures fautives a et b (distance d'édition), ou None."""
    ka_, kb_ = key(a), key(b)
    if (ka_, kb_) in _cache: return _cache[(ka_, kb_)]
    best = None
    if 2 <= len(ka_) <= 18 and ka_.isalpha() and kb_.replace("'", '').isalpha():
        cands = (sp.candidates(ka_) or set()) | (sp.candidates(kb_) or set())
        def ed(x, y):
            d = list(range(len(y) + 1))
            for i, cx in enumerate(x, 1):
                p_, d[0] = d[0], i
                for j, cy in enumerate(y, 1):
                    p_, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p_ + (cx != cy))
            return d[-1]
        sc = sorted((ed(c, ka_) + ed(c, kb_), -sp.word_frequency[c], c) for c in cands if c in sp)
        if sc and sc[0][0] <= 3 and (len(sc) == 1 or sc[0][0] < sc[1][0] or sc[0][1] < sc[1][1]): best = sc[0][2]
    _cache[(ka_, kb_)] = best
    return best
def casse(modele, mot):
    if modele[:1].isupper(): mot = mot[:1].upper() + mot[1:]
    pre = re.match(r"^[^\wÀ-ÿœæ]*", modele).group(0); suf = re.search(r"[^\wÀ-ÿœæ]*$", modele).group(0)
    return pre + mot + suf
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
    return all(x in sp or x in LATIN or agree[x] >= 2 for x in re.split(r"['\-]", k) if x)


def score(prev, words, nxt):
    ks = [k for k in (key(w) for w in words) if k]
    if not ks: return 0
    seq = ([prev] if prev else []) + ks + ([nxt] if nxt else [])
    return sum(big[(x, y)] for x, y in zip(seq, seq[1:]))


ROMAIN = re.compile(r"^[IVXL]+[eè]r?[.,]?$|^1(er|re)$|^[IVXL]+\.?$")
def garderA(aw, bw):
    """Cas où la seconde lecture est un piège : appel de note (« Seigneur1. » / « Seigneur!. »), numéro romain
    (« IIe » / « Ile »), chiffre parasite inséré, mot plus court qui n'est qu'une amputation."""
    ja = ''.join(key(w) for w in aw); jb = ''.join(key(w) for w in bw)
    if re.sub(r'\d+$', '', ja) and re.sub(r'\d+$', '', ja) == re.sub(r'\d+$', '', jb): return True
    if re.sub(r'\d', '', ja) == jb and re.search(r'[a-zà-ÿœæ]\d', ja): return True
    if any(ROMAIN.match(w.strip()) for w in aw): return True
    if any(re.fullmatch(r'\d+', key(w)) for w in bw) and not any(re.search(r'\d', w) for w in aw): return True
    if re.search(r'[a-zà-ÿœæ]\d+$', ja) and not re.search(r'\d$', jb): return True  # appel de note perdu
    if len(jb) < 0.85 * len(ja): return True  # lecture amputée
    if any(re.search(r'[|/\\]', w) for w in bw): return True  # signe parasite
    return False

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
        # débris de marge (lettre ou signe isolé) que Tesseract colle au début ou à la fin de la ligne
        while len(bw) > 1 and len(key(bw[0])) <= 2 and (not aw or key(bw[0]) != key(aw[0])) and not known(bw[0] + 'x'*0) or (len(bw) > 1 and len(key(bw[0])) == 1 and key(bw[0]) not in ('a', 'à', 'y', 'o', 'ô') and (not aw or key(bw[0]) != key(aw[0]))):
            bw = bw[1:]
        while len(bw) > 1 and len(key(bw[-1])) == 1 and key(bw[-1]) not in ('a', 'à', 'y', 'o', 'ô') and (not aw or key(bw[-1]) != key(aw[-1])):
            bw = bw[:-1]
        ja = ''.join(key(w) for w in aw); jb = ''.join(key(w) for w in bw)
        if not bw: out += keep(); continue
        if not aw:
            if all(known(w) and len(key(w)) >= 2 for w in bw) and len(jb) >= 4 and score(ka[a1-1] if a1 else '', bw, ka[a1] if a1 < len(ka) else '') > 0:
                out += [(w, line, None) for w in bw]
            continue
        base = lambda x: ''.join(c for c in unicodedata.normalize('NFD', x) if not unicodedata.combining(c)).replace("'", '')
        if base(ja) == base(jb) and ja != jb:
            ak0 = all(known(w) for w in aw); bk0 = all(known(w) for w in bw)
            if bk0 and not ak0: out += keep() if garderA(aw, bw) else [(w, line, None) for w in bw]; continue
            if ak0 or not bk0: out += keep(); continue
        if all(re.fullmatch(r"[IVXLC]+\.?", w) for w in aw) and len(aw) == 1: out += keep(); continue
        if ja == jb or ja.replace('â', 'a') == jb.replace('â', 'a'):
            out += [(w, line, None) for w in bw] if any(BAD.search(w) for w in aw) and not any(BAD.search(w) for w in bw) else keep(); continue
        if all(re.fullmatch(r"[\d—–\-| .]*", w) for w in aw): out += keep(); continue
        ak = all(known(w) for w in aw); bk = all(known(w) for w in bw)
        if bk and not ak: out += keep() if garderA(aw, bw) else [(w, line, None) for w in bw]; continue
        if ak and not bk: out += keep(); continue
        prev = ka[a1 - 1] if a1 else ''; nxt = ka[a2] if a2 < len(ka) else ''
        sa, sb = score(prev, aw, nxt), score(prev, bw, nxt)
        if sb > 0 and sb >= 4 * max(sa, 0.5) and bk: out += keep() if garderA(aw, bw) else [(w, line, None) for w in bw]; continue
        if sa > 0 and sa >= 4 * max(sb, 0.5) and ak: out += keep(); continue
        if ak and bk and len(ja) <= 2 and len(jb) <= 2 and sa >= sb: out += keep(); continue
        if ak and bk: out += keep(); continue  # deux mots valides, aucun indice : on garde la lecture d'archive.org
        # mêmes nombres de mots : correction mot à mot vers le mot connu le plus proche des deux lectures
        if len(aw) == len(bw):
            res = []
            for x, y in zip(aw, bw):
                if key(x) == key(y) or known(x): res.append(x); continue
                if known(y) and not garderA([x], [y]): res.append(y); continue
                if known(y): res.append(x); continue
                c = proche(x, y)
                if not c: res = None; break
                res.append(casse(x, c))
            if res: out += [(w, line, None) for w in res]; continue
        # lecture d'archive.org sans caractère parasite (souvent un fragment de mot coupé en fin de ligne) : on la garde
        if not any(BAD.search(w) or re.search(r"[^\s\wÀ-ÿœŒæ'’,.;:!?()«»\-—]", w) for w in aw): out += keep(); continue
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
