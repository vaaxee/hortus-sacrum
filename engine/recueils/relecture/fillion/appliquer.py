"""Fillion : applique les décisions prises sur l'image aux brouillons et écrit les pages relues (pages/p<NNN>.txt).

Usage : FILLION=<dossier> python3 -I appliquer.py [decisions.txt]

decisions.txt, un bloc par page :
  == p091                 page imprimée
  f: A T "Il" A …         un choix par désaccord du brouillon, dans l'ordre : T, A, ou "texte" ("" = rien) ;
                          « … » en dernier vide tous les désaccords restants (notes de bas de page, à supprimer par x:)
  v: 3 7                  lignes du brouillon (numérotées à partir de 1) qui commencent un verset
  c: 4                    lignes qui continuent le verset précédent
  x: 1 2 21-67            lignes à supprimer (parasites, notes prises avec le texte)
  h: 5 Psaume IV          la ligne 5 est un titre, de ce texte
  +: 5 c texte            ajoute après la ligne 5 une ligne (v, c ou h) de ce texte (0 = en tête)
  r: ancien => nouveau    remplacement dans le texte de la page relue (occurrence unique ; « \\n » = saut de ligne,
                          « \\nv| » coupe la ligne là où un verset commence au milieu)
  ?: mot — remarque       lecture douteuse, recopiée dans la note du verset qui contient « mot »
  ok                      page entièrement relue sur l'image

Page écrite : une ligne par ligne imprimée, « v| » (début de verset), « c| » (suite), « h| » (titre), « ?| » (doute).
"""
import os, re, shlex, sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
B = Path(os.environ['FILLION'])
FLAG = re.compile(r'\{(\d+) T:(.*?) / A:(.*?)\}')


def blocs(path):
    out, cur = {}, None
    for l in path.read_text(encoding='utf-8').splitlines():
        if not l.strip() or l.startswith('//'):
            continue
        m = re.match(r'==\s*p(\d+)', l)
        if m:
            cur = int(m.group(1))
            out[cur] = []
            continue
        out[cur].append(l)
    return out


def renvois(texte):
    """Renvoi typographique « [fin » imprimé au bout d'une ligne voisine : remis à la ligne qu'il complète.
    La ligne complétée est celle du dessus si elle finit par un trait d'union, sinon celle du dessous si elle en finit
    par un, sinon la plus longue des deux qui ne finissent pas par une ponctuation (la ligne coupée remplit la justification)."""
    L = texte.split('\n')
    for i, l in enumerate(L):
        m = re.search(r'\s\[(\S.*)$', l)
        if not m or l.startswith('h|'):
            continue
        frag = m.group(1).strip()
        L[i] = l[:m.start()].rstrip()
        def fin(j):
            return L[j].rstrip()[-1:] if 0 <= j < len(L) and not L[j].startswith('h|') else '.'
        P, N = i - 1, i + 1
        if fin(P) == '-':
            j = P
        elif fin(N) == '-':
            j = N
        else:
            cands = [k for k in (P, N) if fin(k) not in '.,;:?!']
            if not cands:
                raise SystemExit(f'renvoi « [{frag} » sans ligne à compléter : {l}')
            j = max(cands, key=lambda k: len(L[k]))   # la ligne coupée est la plus longue (pleine justification)
        L[j] = L[j][:-1] + frag if L[j].endswith('-') else L[j] + ' ' + frag
    return '\n'.join(L)


def appliquer(p, ops):
    br = (B / 'brouillon' / f'p{p:03d}.txt').read_text(encoding='utf-8').splitlines()
    choix = []
    for o in ops:
        if o.startswith('f:'):
            choix += shlex.split(o[2:])
    nflags = sum(len(FLAG.findall(l)) for l in br)
    if choix and choix[-1] == '…':      # « … » : les désaccords restants (notes prises avec le texte) sont vidés
        choix = choix[:-1] + [''] * (nflags - len(choix) + 1)
    if len(choix) != nflags:
        raise SystemExit(f'p{p} : {len(choix)} choix pour {nflags} désaccords')
    lignes = []
    for i, l in enumerate(br, 1):
        def rep(m):
            c = choix[int(m.group(1)) - 1]
            return m.group(2) if c == 'T' else m.group(3) if c == 'A' else c
        t = FLAG.sub(rep, l)
        if t.startswith('#'):
            k, t = 'h', t[1:]
        elif re.match(r'^(\d+|\?)\|', t):
            k, t = 'v', t.split('|', 1)[1]
        else:
            k, t = 'c', t[1:]
        lignes.append([k, re.sub(r'\s+', ' ', t).strip(), i])
    ajouts, doutes, relu = [], [], False
    for o in ops:
        tag, _, reste = o.partition(':')
        tag = tag.strip()
        if o.strip() == 'ok':
            relu = True
        elif tag in ('v', 'c', 'x'):
            for tok in reste.split():
                a, _, b = tok.partition('-')
                for n in range(int(a), int(b or a) + 1):
                    lignes[n - 1][0] = tag
        elif tag == 'h':
            n, txt = reste.strip().split(' ', 1)
            lignes[int(n) - 1][0:2] = ['h', txt.strip()]
        elif tag == '+':
            n, k, txt = reste.strip().split(' ', 2)
            ajouts.append((int(n), k, txt.strip()))
        elif tag == '?':
            doutes.append(reste.strip())
    for n, k, txt in sorted(ajouts, key=lambda a: -a[0]):
        lignes.insert(n if n == 0 else [l[2] for l in lignes].index(n) + 1, [k, txt, -1])
    lignes = [l for l in lignes if l[0] != 'x' and l[1]]
    texte = '\n'.join(f'{k}| {t}' for k, t, _ in lignes)
    for o in ops:
        if o.startswith('r:'):
            a, b = o[2:].split('=>')
            a, b = a.strip().replace('\\n', '\n'), b.strip().replace('\\n', '\n')
            if texte.count(a) != 1:
                raise SystemExit(f'p{p} : « {a} » trouvé {texte.count(a)} fois')
            texte = texte.replace(a, b)
    texte = renvois(texte)
    if not relu:
        raise SystemExit(f'p{p} : page non marquée « ok »')
    entete = f'# p{p} (image n{p + 13})\n'
    pied = ''.join(f'?| {d}\n' for d in doutes)
    (ICI / 'pages' / f'p{p:03d}.txt').write_text(entete + texte + '\n' + pied, encoding='utf-8')


if __name__ == '__main__':
    dec = Path(sys.argv[1]) if len(sys.argv) > 1 else ICI / 'decisions.txt'
    (ICI / 'pages').mkdir(exist_ok=True)
    for p, ops in blocs(dec).items():
        appliquer(p, ops)
    print(len(blocs(dec)), 'pages écrites')
