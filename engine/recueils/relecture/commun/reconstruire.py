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
# pages de table des matières (fin du tome) : lecture d'archive.org telle quelle, le découpage s'y appuie
brut = lambda p: ' '.join(w for l in p for w, _ in l)
debut_table = next((i for i in range(len(pages) - 1, len(pages) // 2, -1) if 'TABLE' in brut(pages[i]) and 'MATI' in brut(pages[i]).upper()), len(pages))
txt = []
for i, p in enumerate(pages):
    man = f'{D}/manuel{S}/{i}.txt'
    if os.path.exists(man):
        txt.append(open(man, encoding='utf-8').read().rstrip('\n')); continue
    if i >= debut_table:
        page = []
        for li, l in enumerate(p):
            page.append('  '.join(w.strip() for w, _ in l if w.strip()))
            if li in ends[i]: page.append('')
        txt.append('\n'.join(page)); continue
    lignes = {}
    for w, li, fid in merged.get(str(i), []):
        if fid is not None: w = choix(flags[fid])
        w = w.strip()
        if w: lignes.setdefault(li, []).append(w)
    n = max([len(p)] + [k + 1 for k in lignes])
    page = []
    for li in range(n):
        page.append('  '.join(lignes.get(li, [])))
        if li in ends[i]: page.append('')
    txt.append('\n'.join(page))
t = '\n\n'.join(txt)
# corrections ponctuelles de la table (lecture d'archive.org), dans <dossier>/table<s>.txt : « avant<TAB>après »
if os.path.exists(f'{D}/table{S}.txt'):
    for l in open(f'{D}/table{S}.txt', encoding='utf-8'):
        if '\t' in l: a, b = l.rstrip('\n').split('\t', 1); t = t.replace(a, b)
open(OUT, 'w', encoding='utf-8').write(t)
print(OUT, sum(len(t) for t in txt))
