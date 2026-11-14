"""Chaignon : sort les notes de bas de page du texte courant et les range en fin de méditation.

Usage : python3 -I notes.py <dossier archive.org> <chaignon.json> [--ecrire]
Le dossier contient pages0{1,2,3}.json (mots et coordonnées de la couche ABBYY d'archive.org, une liste de lignes
par page). Une note se reconnaît à sa place (bas de page) et à son corps plus petit que le texte courant ; on retrouve
son texte dans la méditation (caractères hors espaces, occurrence unique), on l'enlève, on recolle la phrase que le
saut de page avait coupée, et la note va sous « ### Notes » à la fin de la méditation, dans l'ordre des pages.
Les numéros de page et signatures restés seuls dans un paragraphe sont retirés de même.
"""
import json, re, statistics, sys

D, F = sys.argv[1], sys.argv[2]
MARQUE = re.compile(r"^(\d{1,2}|[*'’‘•¹²³]|[a-z])\s?\S")
FIN = re.compile(r"[.!?:;»…)]\s*$")


def boite(c):
    x0, y0, x1, y1 = map(int, c.split(','))
    return abs(y1 - y0), max(y0, y1)


def notes_du_tome(v):
    P = json.load(open(f'{D}/pages{v}.json'))
    toutes = []
    hs = [boite(c)[0] for p in P for l in p for _, c in l]
    corps_h = statistics.median(hs)
    for p in P:
        if len(p) < 6: continue
        L = []
        for l in p:
            if not l: continue
            h = statistics.median(boite(c)[0] for _, c in l); y = statistics.median(boite(c)[1] for _, c in l)
            L.append((h, y, ' '.join(w for w, _ in l).strip()))
        ymax = max(y for _, y, _ in L)
        k = len(L) - 1
        bas = []  # lignes courtes du bas : signature d'imprimeur, ou fin de la dernière note (« ii 18. »)
        while k >= 0 and len(L[k][2]) <= 10: bas.insert(0, L[k][2]); k -= 1
        pas = statistics.median(L[j][1] - L[j - 1][1] for j in range(1, len(L)))
        zone = []
        # le bloc des notes : séparé du texte par un blanc plus grand que l'interligne, en corps plus petit
        for j in range(max(1, k - 14), k + 1):
            t = L[j][2]
            if (MARQUE.match(t) and not re.match(r"^\d+\s?°", t) and L[j][1] - L[j - 1][1] > 1.2 * pas
                    and L[j][1] > 0.55 * ymax and statistics.mean(h for h, _, _ in L[j:k + 1]) < 0.9 * corps_h):
                zone = [x[2] for x in L[j:k + 1]]; break
        if not zone:
            while k > 0 and L[k][0] < 0.82 * corps_h and L[k][1] > 0.55 * ymax:
                zone.insert(0, L[k][2]); k -= 1
        if not zone or not MARQUE.match(zone[0]): continue
        suite = ' '.join(bas)
        notes = []
        for t in zone:  # une note commence par son appel en début de ligne
            if notes and (re.match(r"^\d{1,2}\s", t) or t[0] in "*'’‘"):
                notes.append([t])
            elif notes: notes[-1].append(t)
            else: notes.append([t])
        toutes.append(([' '.join(n) for n in notes], ' '.join(bas)))
    return toutes


def sans_blancs(s):
    """Texte sans espaces ni coupures en fin de ligne, et table des positions d'origine."""
    out, pos = [], []
    for i, ch in enumerate(s):
        if ch.isspace(): continue
        out.append(ch); pos.append(i)
    return ''.join(out), pos


d = json.load(open(F))
stats = {'notes': 0, 'trouvees': 0, 'absentes': 0, 'multiples': 0, 'pages': 0}
for v in ('01', '02', '03'):
    E = [e for e in d['entrees'] if e['tome'] == int(v)]
    N = notes_du_tome(v)
    coupes = {id(e): [] for e in E}
    def chercher(texte):
        for essai in (texte, re.sub(r'[-_¬]\s+', '', texte)):
            cle, _ = sans_blancs(essai)
            if len(cle) < 6: return []
            hits = []
            for e in E:
                s, pos = sans_blancs(e['corps'])
                i = s.find(cle)
                while i >= 0:
                    hits.append((e, pos[i], pos[i + len(cle) - 1] + 1)); i = s.find(cle, i + 1)
            if hits: return hits
        return []
    for notes, suite in N:
        # d'abord tout le bloc de la page (avec ou sans les lignes courtes du bas), sinon note par note
        essais = [(notes, ' '.join(notes) + ' ' + suite)] if suite else []
        essais += [(notes, ' '.join(notes))] + [([n], n) for n in notes] if len(notes) > 1 else [(notes, ' '.join(notes))]
        faits = set()
        for groupe, texte in essais:
            if set(groupe) <= faits: continue
            hits = chercher(texte)
            if len(hits) == 1:
                e, a, b = hits[0]
                coupes[id(e)].append((a, b, groupe, e['corps'][a:b])); faits |= set(groupe)
            elif hits: stats['multiples'] += 1
        stats['notes'] += len(notes); stats['trouvees'] += len(faits)
        stats['absentes'] += len(notes) - len(faits)
    for e in E:
        t = e['corps']; notes = []
        vus = []
        for a, b, groupe, txt in sorted(coupes[id(e)], key=lambda x: x[:2]):  # deux essais ne doivent pas se chevaucher
            if vus and a < vus[-1][1]: continue
            vus.append((a, b, txt))
        for a, b, txt in reversed(vus):
            t = t[:a] + '\x00' + t[b:]
            # le texte tel qu'il est dans la méditation, une note par paragraphe
            for g in reversed([x for x in txt.split('\n\n') if x.strip()]): notes.insert(0, (a, g))
        # numéros de page, signatures : paragraphes faits seulement de chiffres et de signes
        P = t.split('\n\n')
        for j, p in enumerate(P):
            q = p.strip()
            if q and len(q) <= 10 and not re.search(r"[A-Za-zÀ-ÿœ]{3}", q) and q not in ('«', '»') and not q.startswith('#'):
                P[j] = '\x00'; stats['pages'] += 1
        t = '\n\n'.join(P)
        # recoller autour des trous
        def joint(m):
            av, ap = m.group(1), m.group(2)
            if re.search(r"\w[-~]$", av) and re.match(r"[a-zà-ÿœ]", ap): return av[:-1] + ap
            if not FIN.search(av) and re.match(r"[a-zà-ÿœ,;:.!?)»]", ap): return av + ' ' + ap
            return av + '\n\n' + ap
        t = re.sub(r"(\S*)\s*(?:\x00\s*)+(\S?)", joint, t)
        t = t.replace('\x00', '')
        corps = []
        if notes:
            for _, txt in notes:
                txt = re.sub(r"\s+", " ", txt).strip()
                txt = re.sub(r"^(\d{1,2}|[*'’‘•¹²³])\s*", '', txt)
                if re.search(r"[A-Za-zÀ-ÿœæ]{2}", txt):  # pas les signatures restées collées au bloc
                    corps.append(f"{len(corps) + 1}. {txt}")
        if corps:
            t = t.rstrip() + '\n\n### Notes\n\n' + '\n\n'.join(corps)
        e['corps'] = t
print(stats)
if '--ecrire' in sys.argv: json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
