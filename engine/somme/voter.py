"""Somme (Lachat) : vote entre quatre lectures du texte français principal, ligne à ligne puis mot à mot.

Deux exemplaires de la même composition (Vivès : mêmes pages, mêmes lignes, mêmes coupures) :
 - 1880 (4e éd., archive.org sommetheologique01thom) : C = Tesseract (selection.py), A = ABBYY d'archive.org ;
 - 1874 (archive.org sommethologique07lachgoog, Google/Harvard) : D = Tesseract (selection.py), B = ABBYY.
Deux moteurs différents sur deux scans différents : un mot est retenu quand au moins une lecture Tesseract (C, D) et
une lecture ABBYY (A, B) le donnent à l'identique (les fautes d'un même moteur sont corrélées : ABBYY lit « parolt »
pour « paroît » sur les deux scans, Tesseract « 4° » pour « 1° »). Sinon il est signalé ⟦c⁞d⁞a⁞b⟧ ; resoudre.py
tranche ce qui est sûr, le reste sur l'image (decisions.txt).

Lignes : C sert de trame ; une ligne de D absente de C (ligne courte perdue par la sélection) est insérée quand A ou B
l'ont aussi, et signalée ⟦ligne⟧.

Usage : python3 -I voter.py <Csel.json> <Dsel.json> <djvu 1880> <djvu 1874> <décalage 1874-1880> <sortie.json>
Sortie : [{page, pageB, lignes: [{t, sure, c, d, a, b, y, x, h}]}]
"""

import collections
import difflib
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abbyy import dechiffrer, pages  # noqa: E402


def norm(s):
    s = unicodedata.normalize('NFC', s or '')
    s = s.replace('’', "'").replace('‘', "'").replace('`', "'").replace('“', '"').replace('”', '"')
    s = s.replace('<<', '«').replace('>>', '»')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([,.;:?!»)])', r'\1', s)
    s = re.sub(r'([«(])\s+', r'\1', s)
    return s


def mots(s):
    s = norm(s)
    return s.split(' ') if s else []


def ratio(x, y):
    return difflib.SequenceMatcher(None, norm(x), norm(y), autojunk=False).ratio()


def apparier(lc, lx, seuil=0.45):
    """Lignes de C → indices des lignes de X (monotone, glouton avec fenêtre)."""
    out = []
    p = 0
    for c in lc:
        best, bj = 0, None
        for j in range(p, min(p + 10, len(lx))):
            r = ratio(c, lx[j])
            if r > best:
                best, bj = r, j
        if bj is not None and best >= seuil:
            out.append(bj)
            p = bj + 1
        else:
            out.append(None)
    return out


def projeter(base, autre):
    """Pour chaque mot de base : le mot de l'autre lecture ('' si fondu, None si absent) ; insertions par position."""
    res = [None] * len(base)
    ins = {}
    sm = difflib.SequenceMatcher(None, base, autre, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal' or (op == 'replace' and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                res[i1 + k] = autre[j1 + k]
        elif op == 'replace':
            res[i1] = ' '.join(autre[j1:j2])
            for k in range(i1 + 1, i2):
                res[k] = ''
        elif op == 'insert':
            ins[i1] = ' '.join(autre[j1:j2])
    return res, ins


TESS, ABBYY = (0, 1), (2, 3)  # indices dans (c, d, a, b)


def choix(vals):
    """vals : 4 lectures (ou None). Valeur donnée par une lecture Tesseract et une lecture ABBYY."""
    sup = collections.defaultdict(set)
    for i, v in enumerate(vals):
        if v is not None:
            sup[v].add(i)
    bons = [(len(s), v) for v, s in sup.items() if s & set(TESS) and s & set(ABBYY)]
    if bons:
        bons.sort(key=lambda x: (-x[0], x[1]))
        return bons[0][1]
    return None


def voter(c, d, a, b):
    kc, kd, ka, kb = norm(c), norm(d), norm(a), norm(b)
    lignes = [kc, kd, ka, kb]
    # ligne entière : une lecture Tesseract = une lecture ABBYY
    v = choix([x if x else None for x in lignes])
    if v is not None:
        return v, True
    wc = mots(c)
    proj = [projeter(wc, mots(x)) for x in (d, a, b)]
    out, sure = [], True

    def insertion(i):
        nonlocal sure
        vals = [None] + [p[1].get(i) for p in proj]
        v = choix(vals)
        if v:
            out.append(v)
        elif any(x and re.search(r'\w', x) for x in vals[1:]):
            out.append('⟦+' + '⁞'.join(str(x) for x in vals[1:]) + '⟧')
            sure = False

    for i, w in enumerate(wc):
        insertion(i)
        vals = [w] + [p[0][i] for p in proj]
        if all(x == '' for x in vals[1:] if x is not None) and any(x == '' for x in vals[1:]):
            continue  # mot fondu dans le précédent par les autres lectures
        v = choix([x if x != '' else None for x in vals])
        if v is not None:
            out.append(v)
        else:
            out.append('⟦' + '⁞'.join(str(x) for x in vals) + '⟧')
            sure = False
    insertion(len(wc))
    return ' '.join(out), sure


def trigrammes(s):
    w = re.findall(r'\w{3,}', s.lower())
    return set(zip(w, w[1:], w[2:]))


def main():
    Csel, Dsel = json.load(open(sys.argv[1])), {p['page']: p for p in json.load(open(sys.argv[2]))}
    A, B = pages(sys.argv[3]), pages(sys.argv[4])
    dec = int(sys.argv[5])
    res = []
    for p in Csel:
        n = p['page']
        m = n + dec
        lc = [l['t'] for l in p['lignes']]
        dl = Dsel.get(m, {'lignes': []})['lignes']
        ld = [l['t'] for l in dl]
        la = [dechiffrer(l['t']) for l in A[n]['lines']]
        lb = [dechiffrer(l['t']) for l in B[m]['lines']]
        pd, pa, pb = apparier(lc, ld), apparier(lc, la), apparier(lc, lb)
        lignes = []
        utilisees = {j for j in pd if j is not None}
        # lignes de D absentes de C, à leur place
        avant = collections.defaultdict(list)
        k = 0
        for j, t in enumerate(ld):
            while k < len(pd) and (pd[k] is None or pd[k] < j):
                k += 1
            if j not in utilisees and re.search(r'[a-zà-ÿ]{3}', t):
                aa = max(la, key=lambda x: ratio(t, x)) if la else ''
                bb = max(lb, key=lambda x: ratio(t, x)) if lb else ''
                if ratio(t, aa) >= 0.6 or ratio(t, bb) >= 0.6:
                    avant[k].append((t, aa, bb, dl[j]))
        for i, l in enumerate(p['lignes']):
            for t, aa, bb, ldj in avant.get(i, []):
                v, s = voter(t, t, aa, bb)
                lignes.append(dict(t='⟦ligne⟧ ' + v, sure=False, c='', d=t, a=aa, b=bb, y=ldj['y'], x=ldj['x'],
                                   h=ldj['h'], source='D'))
            g = lambda L, P: L[P[i]] if P[i] is not None else None  # noqa: E731
            t, sure = voter(l['t'], g(ld, pd), g(la, pa), g(lb, pb))
            lignes.append(dict(t=t, sure=sure, c=l['t'], d=g(ld, pd), a=g(la, pa), b=g(lb, pb), y=l['y'], x=l['x'],
                               h=l['h']))
        for t, aa, bb, ldj in avant.get(len(p['lignes']), []):
            v, s = voter(t, t, aa, bb)
            lignes.append(dict(t='⟦ligne⟧ ' + v, sure=False, c='', d=t, a=aa, b=bb, y=ldj['y'], x=ldj['x'],
                               h=ldj['h'], source='D'))
        res.append(dict(page=n, pageB=m, lignes=lignes))
    json.dump(res, open(sys.argv[6], 'w'), ensure_ascii=False, indent=0)
    tot = sum(len(p['lignes']) for p in res)
    nsure = sum(1 for p in res for l in p['lignes'] if not l['sure'])
    nflag = sum(l['t'].count('⟦') for p in res for l in p['lignes'])
    print(f'{tot} lignes, {nsure} avec un doute, {nflag} signalements')


if __name__ == '__main__':
    main()
