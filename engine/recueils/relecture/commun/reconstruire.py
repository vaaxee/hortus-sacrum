"""Reconstruit le texte d'un tome au format djvu.txt d'archive.org (mots séparés par deux espaces, paragraphes par une
ligne vide) à partir de la fusion des deux lectures et des décisions de relecture.
Usage : python3 reconstruire.py <dossier> <suffixe> <sortie.txt>
Décisions : <dossier>/dec<s>.txt, une ligne « numéro<TAB>texte » ; « A » ou « B » = l'une des lectures ; absent = lecture A."""
import json, os, sys
D, S, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
pages = json.load(open(f'{D}/pages{S}.json')); ends = json.load(open(f'{D}/ends{S}.json'))
merged = json.load(open(f'{D}/merged{S}.json')); flags = json.load(open(f'{D}/flags{S}.json'))
dec = {}
if os.path.exists(f'{D}/dec{S}.txt'):
    for l in open(f'{D}/dec{S}.txt', encoding='utf-8'):
        l = l.rstrip('\n')
        if l: k, _, v = l.partition('\t'); dec[int(k)] = v
def choix(f):
    v = dec.get(f['id'])
    return f['b'] if v == 'B' else f['a'] if v in (None, 'A') else v
txt = []
for i, p in enumerate(pages):
    lignes = {}
    for w, li, fid in merged.get(str(i), []):
        if fid is not None: w = choix(flags[fid])
        if w: lignes.setdefault(li, []).append(w)
    n = max([len(p)] + [k + 1 for k in lignes])
    page = []
    for li in range(n):
        page.append('  '.join(lignes.get(li, [])))
        if li in ends[i]: page.append('')
    txt.append('\n'.join(page))
open(OUT, 'w', encoding='utf-8').write('\n\n'.join(txt))
print(OUT, sum(len(t) for t in txt))
