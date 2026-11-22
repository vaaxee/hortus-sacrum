"""Somme (Lachat) : dans la lecture Tesseract d'une page (tess.py), garde le texte français principal.

Écarte : bruit en haut de page (marge, ombre de la reliure), titre courant, notes de Lachat (petit corps : hauteur des
minuscules < 0,8 × corps du texte, sur trois lignes), colonnes latines (grand blanc ou filet au milieu de la ligne).
Garde les intitulés « QUESTION … », « ARTICLE … » (capitales).

Usage : python3 -I selection.py <dossier tess> <n0> <n1> <sortie.json> [VOIR=1]
"""

import json
import os
import re
import statistics
import sys

CORPS0 = 40  # hauteur des minuscules du texte principal, en pixels, pour une page large de 1925 pixels
CORPS = CORPS0
INTITULE = re.compile(r"(ARTICLE|QUESTION)\s+[A-Z0-9ÈÉ]+\.?\s*$")


def colonnes(l, W):
    """Ligne des deux colonnes latines : des mots sûrs de part et d'autre d'un grand blanc (ou filet) au milieu."""
    ms = sorted(l['mots'], key=lambda m: m[1])
    gauche = [m for m in ms if m[1] + m[3] < 0.5 * W and m[0] not in ('|', '¦') and m[5] >= 50]
    droite = [m for m in ms if m[1] > 0.5 * W and m[0] not in ('|', '¦') and m[5] >= 50]
    if len(gauche) < 2 or len(droite) < 2:
        return False
    for a, b in zip(ms, ms[1:]):
        if b[1] - (a[1] + a[3]) > 50 * W / 1925 and 0.35 * W < b[1] < 0.65 * W:
            return True
    return any(m[0] in ('|', '¦') and 0.4 * W < m[1] < 0.6 * W for m in ms)


def lettres(t):
    return sum(c.isalpha() for c in t)


def corps_du_texte(l):
    conf = statistics.mean(m[5] for m in l['mots'])
    return (l['h'] >= 0.8 * CORPS and len(l['mots']) >= 2 and conf >= 55
            and lettres(l['t']) >= 0.6 * len(l['t'].replace(' ', '')))


def intitule(l):
    return INTITULE.search(l['t']) and 'PARTIE' not in l['t'] and statistics.mean(m[5] for m in l['mots']) >= 40


def choisir(d):
    global CORPS
    W = d['W']
    CORPS = CORPS0 * W / 1925
    L = []
    for l in d['lignes']:
        ms = list(l['mots'])
        # taches des marges : mots peu sûrs aux deux bouts de la ligne
        while ms and ms[0][5] < 50 and ms[0][1] < 0.12 * W:
            ms.pop(0)
        while ms and ms[-1][5] < 50 and ms[-1][1] + ms[-1][3] > 0.86 * W:
            ms.pop()
        if not ms:
            continue
        l = dict(l, mots=ms, t=' '.join(m[0] for m in ms), x=min(m[1] for m in ms if m[5] >= 50) if any(m[5] >= 50 for m in ms) else ms[0][1])
        if statistics.mean(m[5] for m in ms) >= 45 or intitule(l):
            L.append(l)
    # début : premier intitulé ou première ligne de texte courant (le titre courant est en capitales, h = 0)
    i0 = None
    for i, l in enumerate(L):
        if intitule(l) or (corps_du_texte(l) and 'PARTIE' not in l['t']):
            i0 = i
            break
    if i0 is None:
        return []
    garde = []
    for i in range(i0, len(L)):
        l = L[i]
        if colonnes(l, W) and i + 1 < len(L) and colonnes(L[i + 1], W):
            d['arret'] = 'colonnes : ' + l['t'][:40]
            break
        suite = [x['h'] for x in L[i:i + 4] if x['h'] and len(x['mots']) >= 3][:3]
        if l['h'] and len(l['mots']) >= 3 and l['h'] < 0.8 * CORPS and suite and statistics.median(suite) < 0.8 * CORPS:
            d['arret'] = 'petit corps : ' + l['t'][:40] + ' ' + str(suite)
            break
        garde.append(l)
    # titre courant resté (capitales : « DE LA THÉOLOGIE. 7 », « PARTIE I, QUESTION III, ARTICLE 2. »)
    def capitales(l):
        a = [c for c in l['t'] if c.isalpha()]
        return a and sum(c.isupper() for c in a) > 0.7 * len(a)
    garde = [l for l in garde if intitule(l) or not capitales(l)]
    # bruit isolé en fin de bloc (taches)
    while garde and lettres(garde[-1]['t']) < 4:
        garde.pop()
    return garde


if __name__ == '__main__':
    D, a, b, dest = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    res = []
    for n in range(a, b + 1):
        d = json.load(open(f'{D}/{n}.json'))
        g = choisir(d)
        res.append(dict(page=n, W=d['W'], H=d['H'], lignes=g))
        if os.environ.get('VOIR'):
            print(n, len(g), d.get('arret', 'fin'), '|', g[0]['t'][:45] if g else '', '…', g[-1]['t'][-45:] if g else '')
    json.dump(res, open(dest, 'w'), ensure_ascii=False)
