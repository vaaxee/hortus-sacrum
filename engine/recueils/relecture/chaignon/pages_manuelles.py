"""Chaignon, t. 2 : pages que le scan rend illisibles à la machine (l'encre du verso transparaît), recopiées à l'œil
sur l'image (manuel_t2/<page>.txt, numéro de page du PDF compté depuis 0) et remises à leur place.

Usage : python3 -I pages_manuelles.py <pages02.json> <chaignon.json> [--ecrire]
Pour chaque suite de pages recopiées, on repère dans la méditation la fin de la page saine qui précède et le début
de la page saine qui suit (texte ABBYY, sans espaces ni traits d'union) ; ce qui est entre les deux est remplacé
par la copie. Les notes de la copie vont à la fin de la liste « Notes » de la méditation.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from hamon import recoller  # noqa: E402

PJ, F = sys.argv[1], sys.argv[2]
P = json.load(open(PJ))
d = json.load(open(F))
M = {int(f.stem): f.read_text(encoding='utf-8') for f in (Path(__file__).parent / 'manuel_t2').glob('*.txt')}


def cle(s):
    out, pos = [], []
    for i, ch in enumerate(s):
        if ch.isspace() or ch in '-¬': continue
        out.append(ch); pos.append(i)
    return ''.join(out), pos


def lignes(p):
    L = [' '.join(w for w, _ in l) for l in P[p] if l]
    if L and re.fullmatch(r"[—–\-\s\d]+", L[0]): L = L[1:]
    return L


def chercher(texte, s):
    k, _ = cle(texte)
    i = s.find(k)
    return i if i >= 0 and s.find(k, i + 1) < 0 else -1


def copie(t):
    """Corps et notes d'une page recopiée."""
    L = t.strip('\n').split('\n')
    if L and re.fullmatch(r"[—–\-\s\d]+", L[0]): L = L[1:]
    t = '\n'.join(L).strip('\n')
    corps, _, bas = t.rpartition('\n\n')
    if bas and re.match(r"^\s*\d{1,2}\s", bas) and corps:
        notes = [re.sub(r"\s+", " ", n).strip() for n in re.split(r"\n(?=\s*\d{1,2}\s)", bas)]
        notes = [re.sub(r"^\d{1,2}\s+", "", n) for n in notes]
    else:
        corps, notes = t, []
    # plan de la méditation (« I. Sur la terre… ») : intertitres, comme dans le reste du livre
    corps = re.sub(r"(?m)^(I{1,3}|IV)\.\s+(?=[A-ZÉÀ])(.*)$", lambda m: "\n\n## " + m.group(1) + ". " + re.sub(r"\s+", " ", m.group(2)) + "\n\n", corps)
    return corps, notes


groupes = []
for p in sorted(M):
    if groupes and groupes[-1][-1] == p - 1: groupes[-1].append(p)
    else: groupes.append([p])
fait = 0
for g in groupes:
    avant, apres = lignes(g[0] - 1), lignes(g[-1] + 1)
    ok = False
    for e in d['entrees']:
        if e['tome'] != 2: continue
        corps, sep, notes = e['corps'].partition('\n\n### Notes\n\n')
        s, pos = cle(corps)
        # fin de la page précédente : la dernière de ses lignes qui se lit dans la méditation (les notes n'y sont plus)
        a = -1
        for k in range(len(avant) - 1, -1, -1):
            if len(cle(avant[k])[0]) < 12: continue
            i0 = chercher(avant[k], s)
            if i0 >= 0:
                a = pos[i0 + len(cle(avant[k])[0]) - 1] + 1; break
        if a < 0: continue
        j = -1
        for k in range(1, 4):  # début de la page suivante (2 lignes, pour être sûr)
            j = chercher(' '.join(apres[:k + 1]), s)
            if j >= 0: break
        if j < 0 or pos[j] <= a: continue
        b = pos[j]
        # la page de faux-titre (« LE CHRÉTIEN sanctifié… ») n'entre pas dans la méditation
        textes = [copie(M[p]) if not M[p].lstrip().startswith('LE  CHRÉTIEN') else ('', []) for p in g]
        neuf = recoller('\n'.join(c for c, _ in textes))
        neuf = re.sub(r"\n\n(?=[a-zà-ÿœ])", " ", neuf)  # une page coupe une phrase, pas un paragraphe
        milieu = corps[a:b]
        neuf = neuf.strip()
        if not 0.5 < len(milieu) / max(1, len(neuf)) < 2.2 and not any(c == '' for c, _ in textes): continue
        if neuf.endswith('-') and re.match(r"[a-zà-ÿœ]", corps[b:b + 1]):
            neuf = neuf[:-1]; fin = ''
        else:
            fin = '\n\n' if re.match(r".*\n\n\s*$", milieu, re.S) else ' '
        debut = '\n\n' if re.match(r"^\s*\n\n", milieu) else ('' if not milieu[:1].isspace() else ' ')
        if re.match(r"[a-zà-ÿœ,;]", neuf): debut = " "  # phrase coupée par la page
        if re.match(r"\s*[a-zà-ÿœ,;]", corps[b:b + 3]): fin = ' '
        corps = corps[:a] + debut + neuf + fin + corps[b:].lstrip(' ')
        N = [x for x in notes.split('\n\n') if x] if sep else []
        N = [re.sub(r"^\d+\. ", "", x) for x in N] + [n for _, ns in textes for n in ns]
        e['corps'] = corps + ('\n\n### Notes\n\n' + '\n\n'.join(f"{i}. {x}" for i, x in enumerate(N, 1)) if N else '')
        print('pages', g, '→', e['cle'], f'({len(milieu)} car. remplacés par {len(neuf)})'); fait += 1; ok = True
        break
    if not ok: print('pages', g, ': place introuvable')
print(fait, 'suites remises sur', len(groupes))
if '--ecrire' in sys.argv: json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
