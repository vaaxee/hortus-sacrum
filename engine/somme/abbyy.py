"""Lecture des lignes d'un fichier <id>_djvu.xml d'archive.org (ABBYY) : texte et coordonnées par page.

Usage de contrôle : python3 -I engine/somme/abbyy.py <fichier_djvu.xml> <page> [<page>…]
"""

import re
import statistics
import sys


def pages(path):
    s = open(path, encoding='utf-8').read()
    out = []
    for o in s.split('<OBJECT')[1:]:
        m = re.search(r'width="(\d+)" height="(\d+)"', o)
        W, H = int(m.group(1)), int(m.group(2))
        lines = []
        for L in re.findall(r'<LINE>(.*?)</LINE>', o, re.S):
            ws = re.findall(r'<WORD coords="(\d+),(\d+),(\d+),(\d+)"[^>]*>([^<]*)</WORD>', L)
            if not ws:
                continue
            words = [w[4].strip() for w in ws]
            x1 = min(int(w[0]) for w in ws)
            x2 = max(int(w[2]) for w in ws)
            yb = statistics.median(int(w[1]) for w in ws)
            hs = sorted(int(w[1]) - int(w[3]) for w in ws)
            lines.append(dict(x1=x1, x2=x2, y=yb, h=statistics.median(hs), t=' '.join(w for w in words if w)))
        out.append(dict(W=W, H=H, lines=lines))
    return out


def dechiffrer(t):
    return (t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            .replace('&quot;', '"').replace('&apos;', "'"))


if __name__ == '__main__':
    P = pages(sys.argv[1])
    for i in map(int, sys.argv[2:]):
        p = P[i]
        print('PAGE', i, p['W'], p['H'])
        for l in p['lines']:
            print(f"{l['x1']:5}{l['x2']:5}{l['y']:6.0f}{l['h']:4.0f} {dechiffrer(l['t'])[:90]}")
