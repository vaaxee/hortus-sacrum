"""Fillion : brouillon d'une page française, les deux lectures alignées ligne à ligne et mot à mot.

Usage : FILLION=<dossier> python3 -I brouillon.py <p1> [<p2> ...]     (pages imprimées impaires)
Sortie : <dossier>/brouillon/p<NNN>.txt, une ligne imprimée par ligne :
  « 12| texte »  ligne au bord gauche (début de verset ; numéro lu par l'OCR, ou « ? »)
  « |  texte »   ligne en retrait (suite du verset)
  « #  texte »   ligne centrée (titre) ; le titre courant et le folio sont omis
  {3 T:… / A:…}  désaccord n° 3 entre Tesseract (T) et ABBYY (A), à trancher sur l'image (decisions.txt)
Accord automatique : mêmes mots (ponctuation comprise) ; ou ABBYY seul fait de mots inconnus du dictionnaire
(pyspellchecker fr) en face d'autant de mots connus chez Tesseract.
"""
import json, os, re, sys, difflib, unicodedata, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prep import B, abbyy
from spellchecker import SpellChecker

sp = SpellChecker(language='fr')
PONCT = re.compile(r'^[;:?!.,]+$')


def key(w):
    w = unicodedata.normalize('NFC', w).replace('’', "'")
    return re.sub(r"[^\wÀ-ÿœŒæÆ']|_", "", w).lower().strip("'")


def connu(w):
    k = key(w)
    return bool(k) and all((p in sp) for p in re.split(r"['-]", k) if p)


def mots(t):
    """Normalise une ligne : apostrophes droites, ponctuation haute précédée d'une espace."""
    t = unicodedata.normalize('NFC', t).replace('’', "'").replace('‘', "'")
    t = re.sub(r'\s*([;:?!])', r' \1', t)
    ws = t.split()
    out = []
    for w in ws:
        if out and re.fullmatch(r'[.,]+', w):
            out[-1] += w
        else:
            out.append(w)
    return out


def tess(n, dx):
    rows = list(csv.DictReader(open(B / 'tess2' / f'n{n}.tsv', encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
    lines = {}
    for r in rows:
        if r['level'] == '5' and r['text'].strip():
            lines.setdefault((int(r['block_num']), int(r['par_num']), int(r['line_num'])), []).append(r)
    out = []
    for ws in lines.values():
        out.append({'mots': [(int(w['left']) + dx, w['text']) for w in ws], 'x': min(int(w['left']) for w in ws) + dx, 'y': min(int(w['top']) for w in ws),
                    'y2': max(int(w['top']) + int(w['height']) for w in ws), 't': ' '.join(w['text'] for w in ws)})
    return sorted(out, key=lambda l: l['y'])


def xmot(l):
    """Abscisse du premier mot (lettre ou chiffre) d'une ligne."""
    if not l:
        return None
    if 'mots' not in l:
        return l['x']
    for x, w in l['mots']:
        if re.search(r'[A-Za-zÀ-ÿ0-9]', w) and w not in ('l', 'I', '|'):
            return x
    return None


def tete(s):
    """Titre courant et folio (« COMPLIES. 91 », « 92 OFFICE DU DIMANCHE. »)."""
    s = re.sub(r'[^\wÀ-ÿ. ]', ' ', s).strip()
    return bool(re.fullmatch(r'(\d+\s+)?[A-ZÀ-Ü0-9 .\-]{4,}(\s+\d+)?|\d+', s))


def page(p):
    n = p + 13
    cut = int((B / 'crop' / f'n{n}.y').read_text())
    box = json.loads((B / 'crop2' / f'n{n}.box').read_text())
    T = tess(n, box[0])
    A = abbyy(n, cut)
    paires, prisA = [], set()
    for t in T:
        best, bo = None, 0
        for i, a in enumerate(A):
            o = min(t['y2'], a['y2']) - max(t['y'], a['y'])
            if o > bo and i not in prisA:
                best, bo = i, o
        a = A[best] if best is not None and bo > 15 else None
        if a is not None:
            prisA.add(best)
        paires.append((t, a))
    paires += [(None, a) for i, a in enumerate(A) if i not in prisA]
    paires.sort(key=lambda ta: (ta[1] or ta[0])['y'])
    corps = sorted(min(v for v in (xmot(t), xmot(a)) if v is not None) for t, a in paires if a and t and len(a['t']) > 12)
    m = corps[len(corps) // 10] if corps else 0
    sortie, nf = [], 0
    for t, a in paires:
        tw, aw = mots(t['t']) if t else [], mots(a['t']) if a else []
        y = (a or t)['y']
        if y < 300 and (tete(' '.join(aw)) or tete(' '.join(tw))):
            continue
        if not re.search(r'[A-Za-zÀ-ÿ]{2}', ' '.join(aw + tw)):
            continue
        x = min(v for v in (xmot(t), xmot(a)) if v is not None)
        bord = x <= m + 45
        num, na, nt = '?', None, None
        if x > m + 330:
            sortie.append('#  ' + ' '.join(aw or tw))
            continue
        if bord:
            # numéro de verset en tête (ou parasite) : retiré des deux lectures
            def tetenum(ws):
                if ws and not re.search(r'[A-Za-zÀ-ÿ]{2}', ws[0]) and len(ws[0]) <= 4 and not PONCT.match(ws[0]):
                    return ws[0], ws[1:]
                return None, ws
            nt, tw = tetenum(tw)
            na, aw = tetenum(aw)
        # parasites en tête de ligne (marge, numéro mal lu) : ni lettre ni chiffre, hors « et (
        while tw and not re.search(r'[\wÀ-ÿ«(]', tw[0]):
            tw = tw[1:]
        while aw and not re.search(r'[\wÀ-ÿ«(]', aw[0]):
            aw = aw[1:]
        if bord:
            for c in (na, nt):
                if c and re.fullmatch(r'\d{1,3}', c):
                    num = c
                    break
        kt, ka = [key(w) or w for w in tw], [key(w) or w for w in aw]
        res = []
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, kt, ka, autojunk=False).get_opcodes():
            if op == 'equal':
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    if tw[i] == aw[j]:
                        res.append(tw[i])
                    else:
                        nf += 1
                        res.append('{%d T:%s / A:%s}' % (nf, tw[i], aw[j]))
            else:
                ts, as_ = ' '.join(tw[i1:i2]), ' '.join(aw[j1:j2])
                if ts and (i2 - i1) == (j2 - j1) and all(connu(w) for w in tw[i1:i2]) and not any(connu(w) for w in aw[j1:j2]) \
                        and not any(re.search(r'\b[aà]\b', w) for w in tw[i1:i2]):
                    res.append(ts)
                else:
                    nf += 1
                    res.append('{%d T:%s / A:%s}' % (nf, ts, as_))
        s = ' '.join(res)
        if bord:
            sortie.append(f'{num}| {s}')
        else:
            sortie.append('|  ' + s)
    return sortie


if __name__ == '__main__':
    (B / 'brouillon').mkdir(exist_ok=True)
    for p in map(int, sys.argv[1:]):
        (B / 'brouillon' / f'p{p:03d}.txt').write_text('\n'.join(page(p)) + '\n')
