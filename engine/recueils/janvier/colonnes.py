"""Brouillon d'une page à deux colonnes (latin et français en regard), d'après la position des mots (pdftotext -bbox).
Usage : python3 -I colonnes.py <pdf> <première page> <dernière page>
Pour chaque page : la gouttière est le plus large intervalle vertical sans mot au milieu de la page ; chaque mot va à
gauche ou à droite selon son centre ; les lignes sont regroupées par hauteur. Sortie : « [[PDF n]] », puis la colonne
de gauche, « ---- », la colonne de droite. Le brouillon est relu sur l'image avant d'être recopié dans un .md."""
import re, subprocess, sys
from html import unescape

PDF, A, B = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

for p in range(A, B + 1):
    h = subprocess.run(['pdftotext', '-bbox', '-f', str(p), '-l', str(p), PDF, '-'], capture_output=True, text=True).stdout
    mots = [(float(a), float(b), float(c), float(d), unescape(t)) for a, b, c, d, t in
            re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', h)]
    largeur = float(re.search(r'<page width="([\d.]+)"', h).group(1))
    # couverture horizontale des mots du corps (on ignore le titre courant, en haut)
    corps = [m for m in mots if m[1] > 40]
    couvert = [0] * int(largeur + 1)
    for x0, y0, x1, y1, t in corps:
        for x in range(int(x0), int(x1) + 1):
            couvert[x] += 1
    milieu = int(largeur / 2)
    zone = range(milieu - 40, milieu + 40)
    gout = min(zone, key=lambda x: (couvert[x], abs(x - milieu)))
    cols = {0: [], 1: []}
    for m in corps:
        cols[0 if (m[0] + m[2]) / 2 < gout else 1].append(m)
    print(f'\n[[PDF {p}]] (gouttière x={gout}, {couvert[gout]} mots à cheval)')
    for c in (0, 1):
        lignes = []
        for m in sorted(cols[c], key=lambda m: (m[1], m[0])):
            if lignes and abs(lignes[-1][0] - m[1]) < 4:
                lignes[-1][1].append(m)
            else:
                lignes.append([m[1], [m]])
        for y, ms in lignes:
            print(' '.join(t for *_, t in sorted(ms)))
        if c == 0:
            print('----')
