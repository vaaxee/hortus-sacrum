"""Hamon : sort les notes de bas de page du texte courant et les range en fin de méditation.

Usage : python3 -I notes.py <dossier des PDF> <hamon.json> [<journal.txt>] [--ecrire]
Le dossier contient bc1.pdf, bc2.pdf, bc3.pdf (Google Livres, vendor/sources/hamon/, non versionnés).

Même méthode que pour Chaignon (`../chaignon/notes.py`), adaptée à la couche texte des PDF de Google Livres
(`pdftotext -bbox-layout`) :
- une note se reconnaît à sa place (bas de page, après un blanc plus grand que l'interligne) et à son corps plus petit
  que le texte courant ; une note commence par une ligne en retrait (l'appel), ses lignes suivantes sont au fer ;
- la signature d'imprimeur du bas de page (« M. H. - T. I. », « Bl. H. – T. I. », « 9 »…) est reconnue à part ;
- on retrouve le texte de la note dans la méditation (caractères hors espaces ; à défaut, début et fin de la note,
  pour tolérer les mots déjà corrigés), dans la méditation de cette page ou dans la précédente, occurrence unique ;
- on l'enlève avec son appel, on recolle la phrase que la note avait coupée, et la note va sous « ### Notes » à la
  fin de la méditation, dans l'ordre des pages ; les signatures sont retirées du texte.
Rejouable : une méditation qui a déjà sa section « ### Notes » garde ses notes ; les nouvelles s'ajoutent à la suite,
et une note déjà rangée n'est plus retrouvée dans le texte courant.
"""
import collections, json, re, statistics, subprocess, sys
from bs4 import BeautifulSoup

D, F = sys.argv[1], sys.argv[2]
# appel d'une note tel que l'OCR le lit : astérisque, apostrophe, guillemet, puce, petit chiffre, point
APPEL = r"(?:[*'’‘\"“”•·°¹²³⁴⁵%>]{1,2}|\d{1,2}\.?|[.,]|[si](?=\s))"
SIGNATURE = re.compile(r"^(?:[A-ZÉ][A-Za-zéÉ]{0,3}\s?\.?\s*)?(?:[HIl]{1,2}|II)\s?\.?\s*[-–—.,]?\s*T\s?[.,]\s*(?:I{1,3}|[1l]{1,3}|IV|V)\s?\.?(?:\s+\d{1,2})?$")
FIN = re.compile(r"[.!?:;»…)]\s*$")


def lignes_du_pdf(pdf):
    """Par page : liste de (hauteur médiane, y, x, texte)."""
    xml = subprocess.run(['pdftotext', '-bbox-layout', pdf, '-'], capture_output=True, text=True).stdout
    s = BeautifulSoup(xml, 'html.parser')
    pages = []
    for pg in s.find_all('page'):
        L = []
        for l in pg.find_all('line'):
            ws = l.find_all('word')
            if not ws: continue
            h = statistics.median(float(w['ymax']) - float(w['ymin']) for w in ws)
            L.append((h, float(l['ymin']), float(l['xmin']), ' '.join(w.get_text() for w in ws).strip()))
        L.sort(key=lambda x: x[1])
        pages.append(L)
    return pages


def tete(L):
    """Les deux premières lignes du texte de la page, sans le titre courant ni le folio."""
    i = 0
    while i < min(3, len(L)) and not re.search(r"[a-zà-ÿ]{2}", L[i][3]): i += 1
    return ' '.join(t for _, _, _, t in L[i:i + 2])


def notes_du_tome(pdf):
    """Liste de (numéro de page PDF, [notes], [signatures], fin du texte de la page, début de la page suivante)."""
    P = lignes_du_pdf(pdf)
    corps_h = statistics.median(h for p in P for h, _, _, t in p if len(t) > 30)
    res = []
    for i, L in enumerate(P, start=1):
        if len(L) < 8: continue
        sig = []
        k = len(L) - 1
        while k >= 0 and (SIGNATURE.match(L[k][3]) or re.fullmatch(r"\d{1,2}|[.,'•]", L[k][3])):
            sig.insert(0, L[k][3]); k -= 1
        pas = statistics.median(L[j][1] - L[j - 1][1] for j in range(1, len(L)) if L[j][1] > L[j - 1][1]) or 1
        ymax = max(y for _, y, _, _ in L)
        zone = []
        for j in range(max(1, k - 20), k + 1):
            bloc = L[j:k + 1]
            if (L[j][1] - L[j - 1][1] > 1.25 * pas and L[j][1] > 0.4 * ymax
                    and max(h for h, _, _, _ in bloc) < 0.85 * corps_h
                    and statistics.mean(h for h, _, _, _ in bloc) < 0.8 * corps_h
                    and not bloc[0][3].isupper()):
                zone = bloc; break
        # l'en-tête d'un dimanche (« { Si l'on veut méditer… », « ÉVANGILE SELON… ») est aussi en petit corps :
        # ce n'est pas une note
        if zone and (zone[0][3].startswith('{') or any(re.search(r"[ÉE]VANGILE SELON", t) for _, _, _, t in zone)):
            zone = []
        if not zone:
            if sig: res.append((i, [], sig, '', ''))
            continue
        x0 = min(x for _, _, x, _ in zone)
        notes = []
        for h, y, x, t in zone:  # une note commence par une ligne en retrait (l'appel)
            if not notes or x > x0 + 2.5: notes.append([t])
            else: notes[-1].append(t)
        notes = [' '.join(n) for n in notes]
        # une signature collée à la dernière note
        m = re.search(r"\s((?:[A-ZÉ][A-Za-zé]{0,3}\s?\.?\s*)?(?:[HIl]{1,2}|II)\s?\.?\s*[-–—.,]?\s*T\s?[.,]\s*(?:I{1,3}|[1l]{1,3}|IV|V)\s?\.?(?:\s+\d{1,2})?)$", notes[-1])
        if m: sig.append(m.group(1)); notes[-1] = notes[-1][:m.start()]
        j0 = L.index(zone[0])
        queue = ' '.join(t for _, _, _, t in L[max(0, j0 - 2):j0])
        res.append((i, notes, sig, queue, tete(P[i]) if i < len(P) else ''))
    return res


def sans_blancs(s):
    """Lettres et chiffres seuls, en minuscules (l'OCR varie sur la ponctuation et les espaces), et table des
    positions d'origine."""
    out, pos = [], []
    for i, ch in enumerate(s):
        if not ch.isalnum(): continue
        out.append(ch.lower()); pos.append(i)
    return ''.join(out), pos


def placer(cle, s):
    """Débuts possibles de `cle` dans `s` : exact, sinon vote de cinq tronçons de 10 caractères (tolère quelques
    lettres corrigées depuis la couche texte du PDF). Rend des couples (début, fin) dans `s`."""
    hits = []
    i = s.find(cle)
    while i >= 0:
        hits.append((i, i + len(cle))); i = s.find(cle, i + 1)
    if hits or len(cle) < 30: return hits
    n = len(cle); T = 10
    offs = sorted({0, n // 4, n // 2, 3 * n // 4, n - T})
    votes = {}
    for o in offs:
        c = cle[o:o + T]; j = s.find(c)
        while j >= 0:
            votes.setdefault(round((j - o) / 6), []).append((j - o, o, j)); j = s.find(c, j + 1)
    for k, v in votes.items():
        if len({o for _, o, _ in v}) >= 3:
            # le début : le premier tronçon s'il est retrouvé tel quel ; sinon le plus précoce, reculé lettre à lettre
            # tant que le texte concorde encore avec la note (jamais au-delà : « avec » ne doit pas perdre son « c »)
            _, o, j = min(v, key=lambda x: x[1])
            debut, k = j, o
            while debut > 0 and k > 0 and s[debut - 1] == cle[k - 1]: debut -= 1; k -= 1
            # la fin : le dernier tronçon retrouvé, jamais une longueur supposée (elle déborderait sur le texte
            # quand la note a été tronquée à la première lecture)
            if max(o for _, o, _ in v) < n // 2: continue
            _, o, j = max(v, key=lambda x: x[2])
            fin, k = j + T, o + T
            while fin < len(s) and k < n and s[fin] == cle[k]: fin += 1; k += 1  # la suite qui concorde encore
            hits.append((max(0, debut), min(len(s), fin)))
    return sorted(set(hits))


def nettoyer_note(txt):
    """Texte d'une note rangée : sans son appel, sans les restes d'appels devant (« t 4. Omne… », « e • Sperantem… »)
    ni derrière (« (Rom., vi, 5.) * »), et vide si ce n'est qu'une ligne de fin de volume (« FIN DU TROISIÈME… »)."""
    txt = sans_appel(txt.strip())
    txt = re.sub(r"^(?:(?:[a-zA-Z]|\d{1,2})?[\s.,;:!?*•·'\"“”^%>+]+)+(?=[A-ZÆŒ])", "", txt)
    txt = re.sub(r"(?:\s+(?:[*•·+<>]|[sS]))+\s*$", "", txt).strip()
    txt = re.sub(r"(?<=[).])\s+\d{1,2}\.?$", "", txt).strip()  # appel de la note suivante : « (Gal., ii, 19.) 24. »
    if re.match(r"FIN D[UE]", txt) or not re.search(r"[A-Za-zÀ-ÿœæ]{2}", txt): return ''
    return txt


def sans_appel(n):
    return re.sub(rf"^{APPEL}\s*", '', n.strip())


FRANCAIS = re.compile(r"\b(?:le|la|les|des|du|une|un|nous|vous|pour|dans|sur|avec|cette|ces|qu'|c'est|il|elle|ne|pas|à|où|être|être)\b", re.I)
REFERENCE = r"\(\s?(?:[1I]{1,3}\s?)?[A-Z][A-Za-zæ'. ]{1,20}[.,]?[^()\n]{0,40}\)"
# seconde passe, sur le texte seul : une citation latine précédée d'un appel et suivie de sa référence entre
# parenthèses (« • Exemplum dedi vobis... (Joan., XIII, 15.) ») ; jamais une phrase française
NOTE_EN_TEXTE = re.compile(rf"(?:(?<=\s)|^)(?:[*•·]{{1,2}}|[*'\"“”•·]\s?(?=[A-Z])|\d{{1,2}}\.?(?=\s[A-Z]))\s?([A-Z][^()\n]{{2,400}}?{REFERENCE})\.?")
SIG_TEXTE = re.compile(r"(?:(?<=\s)|^)(?:M|Bl|N|Méd)\s?\.\s?(?:H|II|I)\s?\.?\s?[-–—]?\s?T\s?\.\s?I{1,3}\s?\.?(?:\s\d{1,2})?(?=\s|$)")


def en_texte(corps, deja):
    """Coupes de la seconde passe (notes latines que la couche du PDF n'a pas permis de situer) et des signatures."""
    pris = [(a, b) for a, b, _ in deja]
    libre = lambda a, b: all(b <= x or a >= y for x, y in pris)
    res = []
    for m in SIG_TEXTE.finditer(corps):
        if libre(m.start(), m.end()): res.append((m.start(), m.end(), None)); pris.append((m.start(), m.end()))
    for m in NOTE_EN_TEXTE.finditer(corps):
        cit = m.group(1)
        if FRANCAIS.search(re.sub(REFERENCE, '', cit)): continue
        if libre(m.start(), m.end()):
            res.append((m.start(), m.end(), cit)); pris.append((m.start(), m.end()))
            journal.append(cit[:100])
    return res


MOTS = collections.Counter()


def recoller(t):
    """Recolle la phrase autour des trous laissés par les notes (\\x00). Un mot coupé en fin de ligne dont le trait
    d'union s'est perdu (« ren » + « dre ») est ressoudé quand la forme entière est attestée dans le recueil et que
    les deux morceaux ne le sont pas."""
    def joint(m):
        av, ap = m.group(1), m.group(2)
        if re.search(r"[a-zà-ÿœ][-~¬]$", av) and re.match(r"[a-zà-ÿœ]", ap): return av[:-1] + ap
        g, dr = re.search(r"[a-zà-ÿœ]+$", av), re.match(r"[a-zà-ÿœ]+", ap)
        if g and dr and MOTS[(g.group(0) + dr.group(0)).lower()] >= 2 and not (MOTS[g.group(0).lower()] >= 3 and MOTS[dr.group(0).lower()] >= 3):
            return av + ap
        if av and not FIN.search(av) and re.match(r"[a-zà-ÿœ,;:.!?)»]", ap): return av + ' ' + ap
        if av and re.match(r"[,;:.!?)»]", ap): return av + ap
        if not av or not ap: return av + ap
        return av + ('\n\n' if '\n' in m.group(0) else ' ') + ap
    t = re.sub(r"(\S*)\s*(?:\x00\s*)+(\S*)", joint, t)
    t = t.replace('\x00', '')
    t = re.sub(r"[ \t]+\n", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


journal = []
d = json.load(open(F))
for e in d['entrees']: MOTS.update(w.lower() for w in re.findall(r"[A-Za-zÀ-ÿœæ]+", e['corps']))
CACHE = {}
# fin de volume : la dernière méditation de chaque tome avait reçu la table des matières et l'index (D:03-25,
# D:08-10, D:11-30). Ils commencent après la dernière « Résolutions et bouquet spirituel… » : coupés là.
for v in (1, 2, 3):
    e = max((e for e in d['entrees'] if e['tome'] == v), key=lambda e: e['page_pdf'])
    corps, sep, rangees = e['corps'].partition('\n\n### Notes\n\n')
    i = corps.rfind('Résolutions et bouquet spirituel')
    j = corps.find('\n\n', i) if i >= 0 else -1
    if j > 0 and re.search(r"TABLE DES MATI|Imprimerie", corps[j:]):
        print('fin de volume coupée', e['cle'], len(corps) - j, 'caractères')
        # les notes déjà rangées qui venaient de la table (titres de jours) partent aussi
        garder = [x for x in rangees.split('\n\n') if x.strip() and re.sub(r"^\d+\.\s*", '', x)[:30] not in corps[j:]] if sep else []
        garder = [re.sub(r"^\d+\.", f"{k + 1}.", x) for k, x in enumerate(garder)]
        e['corps'] = corps[:j] + ('\n\n### Notes\n\n' + '\n\n'.join(garder) if garder else '')
# dernière page où chercher les notes d'une méditation : la page où commence la suivante ; pour la dernière du tome,
# six pages (au-delà commence la table des matières, en petit corps elle aussi)
FIN_PAGE = {}
for v in (1, 2, 3):
    E_ = sorted([e for e in d['entrees'] if e['tome'] == v], key=lambda e: e['page_pdf'])
    for e, f in zip(E_, E_[1:] + [None]):
        FIN_PAGE[id(e)] = f['page_pdf'] if f and f['page_pdf'] >= e['page_pdf'] else e['page_pdf'] + 6


def passe():
    """Un passage sur les trois tomes ; rend le nombre de notes rangées."""
    for v in (1, 2, 3):
        E = sorted([e for e in d['entrees'] if e['tome'] == v], key=lambda e: e['page_pdf'])
        coupes = {id(e): [] for e in E}

        def candidates(p):
            # la méditation de la page et la précédente (FIN_PAGE)
            av = [e for e in E if e['page_pdf'] <= p <= FIN_PAGE[id(e)]]
            return av[-2:]

        def chercher(texte, C):
            cle, _ = sans_blancs(texte)
            if len(cle) < 6: return []
            hits = []
            for e in C:
                corps, _, rangees = e['corps'].partition('\n\n### Notes\n\n')
                if cle in sans_blancs(rangees)[0]: return []  # déjà rangée (second passage)
                S, pos = sans_blancs(corps)
                for i, j in placer(cle, S):
                    hits.append((e, pos[i], pos[j - 1] + 1))
            return hits

        debut = E[0]['page_pdf']
        if v not in CACHE: CACHE[v] = notes_du_tome(f'{D}/bc{v}.pdf')
        for p, notes, sig, _, _ in CACHE[v]:
            if p < debut: continue
            C = candidates(p)
            for s_ in sig:
                if not SIGNATURE.match(s_): continue
                hits = chercher(s_, C) if len(sans_blancs(s_)[0]) >= 8 else []
                if len(hits) == 1:
                    e, a, b = hits[0]; coupes[id(e)].append((a, b, None)); stats['signatures'] += 1
            for n in notes:
                stats['notes'] += 1
                t = sans_appel(n)
                hits = chercher(t, C)
                if len(hits) == 1:
                    e, a, b = hits[0]
                    corps = e['corps']
                    # l'appel de la note, juste avant
                    m = re.search(rf"(?:^|\s){APPEL}\s*$", corps[max(0, a - 6):a])
                    debut_alinea = a == 0 or corps[max(0, a - 2):a] == '\n\n'
                    # une note courte (« Cum ipso. ») peut aussi être citée dans le texte : on exige alors son appel
                    if len(sans_blancs(t)[0]) < 25 and not m and not debut_alinea:
                        stats['absentes'] += 1; absentes.append(f"t. {v}, p. {p} : courte, sans appel : {n[:90]}"); continue
                    if m: a = max(0, a - 6) + m.start() + (1 if m.group(0)[0].isspace() else 0)
                    # la ponctuation qui ferme la note (« 27.) »), que la recherche sur les lettres laisse de côté
                    while b < len(corps) and corps[b] in '.,;:)]}!?»': b += 1
                    # un reste de la note tronquée avant la fin de l'alinéa (« ani. » pour « animabus… »)
                    r = re.match(r"[^\n]{1,6}?(?=\n\n)", corps[b:])
                    if r and len(re.findall(r"\w", r.group(0))) <= 3: b += r.end()
                    coupes[id(e)].append((a, b, t)); stats['trouvees'] += 1
                else:
                    stats['multiples' if hits else 'absentes'] += 1
                    absentes.append(f"t. {v}, p. {p} : {'plusieurs' if hits else 'absente'} : {n[:90]}")
        for e in E:
            corps, sep, anciennes = e['corps'].partition('\n\n### Notes\n\n')
            coupes[id(e)] += en_texte(corps, coupes[id(e)])
            vus = []
            for a, b, txt in sorted(coupes[id(e)], key=lambda x: x[:2]):
                if vus and a < vus[-1][1]: continue
                vus.append((a, b, txt))
            if not vus: continue
            t = corps; notes = []
            for a, b, txt in reversed(vus):
                t = t[:a] + '\x00' + t[b:]
                if txt is not None: notes.insert(0, corps[a:b])
            t = recoller(t)
            liste = [x for x in anciennes.split('\n\n') if x.strip()] if sep else []
            for txt in notes:
                txt = re.sub(r"\s+", " ", txt).strip()
                txt = nettoyer_note(txt)
                if txt:
                    liste.append(f"{len(liste) + 1}. {txt}")
            e['corps'] = t + ('\n\n### Notes\n\n' + '\n\n'.join(liste) if liste else '')
    return stats['trouvees'] + len(journal)


def par_saut_de_page():
    """Première méthode, la plus sûre : dans la méditation, les notes d'une page sont entre la fin du texte de cette
    page et le début du texte de la page suivante (c'est là que la première lecture les a laissées). On situe ces
    deux bornes (25 dernières et 25 premières lettres), et tout ce qui est entre elles est le bloc des notes, avec le
    titre courant, le folio et la signature. Le bloc est découpé aux débuts des notes du PDF ; les morceaux qui ne
    sont que titre courant, folio ou signature sont jetés. Garde-fou : le bloc ne doit pas être beaucoup plus long
    que les notes du PDF."""
    n = 0
    for v in (1, 2, 3):
        E = sorted([e for e in d['entrees'] if e['tome'] == v], key=lambda e: e['page_pdf'])
        if v not in CACHE: CACHE[v] = notes_du_tome(f'{D}/bc{v}.pdf')
        for p, notes, sig, queue, suite in CACHE[v]:
            if not notes or p < E[0]['page_pdf']: continue
            C = [e for e in E if e['page_pdf'] <= p <= FIN_PAGE[id(e)]][-2:]
            q, _ = sans_blancs(queue); q = q[-25:]
            longueur = sum(len(sans_blancs(x)[0]) for x in notes)
            if len(q) < 15: continue
            for e in C:
                corps, sep, rangees = e['corps'].partition('\n\n### Notes\n\n')
                S, pos = sans_blancs(corps)
                i = S.find(q)
                if i < 0 or S.find(q, i + 1) >= 0: continue
                a = pos[i + len(q) - 1] + 1
                while a < len(corps) and corps[a] in '.,;:!?»)-': a += 1
                t, _ = sans_blancs(suite); t = t[:25]
                j = S.find(t, i + len(q)) if len(t) >= 15 else -1
                if j >= 0:
                    b = pos[j]
                    while b > a and corps[b - 1] in '«(': b -= 1
                else:  # dernière page de la méditation : les alinéas qui suivent, tant qu'ils tiennent dans les notes
                    b, total = a, 0
                    for m in re.finditer(r"[^\n]+(?:\n(?!\n)[^\n]*)*", corps[a:]):
                        x = m.group(0)
                        if x.startswith('#'): break
                        total += len(sans_blancs(x)[0])
                        if total > 1.2 * longueur + 20: break
                        b = a + m.end()
                blocs = corps[a:b]
                L = len(sans_blancs(blocs)[0])
                if L < 0.6 * longueur or L > 1.4 * longueur + 60: continue
                # découpe aux débuts des notes du PDF (8 premières lettres, dans l'ordre)
                Sb, posb = sans_blancs(blocs)
                coupes, k = [], 0
                for x in notes:
                    c = sans_blancs(sans_appel(x))[0][:8]
                    if len(c) < 4: continue
                    h = Sb.find(c, k)
                    if h < 0: continue
                    coupes.append(posb[h]); k = h + len(c)
                # le bloc doit commencer par la première note (à quelques signes près) : sinon les bornes sont fausses
                if not coupes or len(sans_blancs(blocs[:coupes[0]])[0]) > 6: continue
                coupes[0] = 0
                morceaux = [blocs[x:y] for x, y in zip(coupes, coupes[1:] + [len(blocs)])]
                garder = []
                for m_ in morceaux:
                    m_ = '\n\n'.join(x for x in m_.split('\n\n') if not x.strip().startswith('#'))
                    # titre courant (« QUATRIÈME DIMANCHE DE CARÊME. »), folio, signature : jetés
                    m_ = SIG_TEXTE.sub(' ', m_)
                    m_ = '\n\n'.join(x for x in m_.split('\n\n') if re.search(r"[a-zà-ÿ]{2}", x))
                    m_ = re.sub(r"\s+", " ", m_).strip()
                    m_ = nettoyer_note(m_)
                    if m_: garder.append(m_)
                liste = [x for x in rangees.split('\n\n') if x.strip()] if sep else []
                debut = len(liste)
                liste += [f"{debut + k + 1}. {x}" for k, x in enumerate(garder)]
                # un intertitre (« ## Premier point ») tombé entre les deux bornes reste dans le texte
                titres = [x.strip() for x in blocs.split('\n\n') if x.strip().startswith('#')]
                milieu = '\x00\n\n' + '\n\n'.join(titres) + '\n\n' if titres else '\x00'
                e['corps'] = recoller(corps[:a] + milieu + corps[b:]) + '\n\n### Notes\n\n' + '\n\n'.join(liste)
                n += len(garder)
                break
    return n


print('par saut de page', par_saut_de_page())
# des notes qui se recouvraient ne sont rangées qu'au passage suivant : on repasse jusqu'à ce que rien ne change
for tour in range(4):
    stats = {'notes': 0, 'trouvees': 0, 'absentes': 0, 'multiples': 0, 'signatures': 0}
    absentes = []
    avant = len(journal)
    n = passe()
    print('passage', tour + 1, stats, 'seconde passe', len(journal) - avant)
    if stats['trouvees'] == 0 and len(journal) == avant: break
print('seconde passe', len(journal))
if len(sys.argv) > 3 and sys.argv[3] != '--ecrire':
    open(sys.argv[3], 'w').write('\n'.join(absentes) + '\n\n# seconde passe\n' + '\n'.join(journal))
if '--ecrire' in sys.argv: json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1); open(F, 'a').write('\n')
