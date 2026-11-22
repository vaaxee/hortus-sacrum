"""Somme théologique : construit data/somme/Ia-NN.json (français de Lachat, latin léonin) et data/somme/index.json.

Entrées :
 - R.json (resoudre.py) : lignes du texte français par page du scan de 1880, après vote ;
 - corrections_fr.txt : chaque ligne relue sur l'image (« page<TAB>ligne<TAB>texte », « n+ » ajoute, vide retire) ;
 - LA.json (latin_ct.py) : latin léonin d'après le Corpus Thomisticum, relu sur l'édition de 1888 ;
 - titres_la.json : intitulés latins des questions et des articles (édition léonine, relus sur l'image).

Mise en forme (présentation seulement, aucun mot touché) : coupures de fin de ligne recollées ; appels de notes « (1) »
retirés (les notes de Lachat ne sont pas reprises) ; espaces normalisées autour de la ponctuation ; le paragraphe
« (Conclusion. — …) », résumé ajouté par les éditeurs modernes et absent du latin léonin, n'est pas repris.

Usage : python3 -I construire.py <R.json> <corrections_fr.txt> <LA.json> <titres_la.json> <pages.json> <dossier data/somme>
pages.json : {"1": [6, 36], "2": [37, 50]} : pages du scan de chaque question.
"""

import collections
import json
import os
import re
import sys

GARDE_TRAIT = {'elle', 'elles', 'il', 'ils', 'on', 'même', 'mêmes', 'dessus', 'dessous', 'ci', 'là', 'unes', 'uns',
               'Christ', 'Esprit', 'Saint', 'dire'}


def charger_corrections(path):
    cor = collections.defaultdict(dict)
    for ligne in open(path, encoding='utf-8'):
        if not ligne.strip() or ligne.startswith('#'):
            continue
        p, n, t = (ligne.rstrip('\n').split('\t') + [''])[:3]
        cor[int(p)][n] = t
    return cor


def lignes_corrigees(page, cor):
    out = []
    c = cor.get(page['page'], {})
    for i, l in enumerate(page['lignes']):
        t = c.get(str(i), l['t'])
        if t.strip():
            out.append(dict(t=t.strip(), page=page['page']))
        if f'{i}+' in c:
            out.append(dict(t=c[f'{i}+'], page=page['page']))
    for l in out:
        if '⟦' in l['t']:
            raise SystemExit(f"page {l['page']} : signalement non tranché : {l['t']}")
    return out


def recoller(a, b):
    """Fin de ligne a (« cher- ») et début de ligne b (« cher à … »)."""
    if not a.endswith('-'):
        return a + ' ' + b
    suite = b.split(' ', 1)[0]
    nu = re.sub(r'[^\wÀ-ÿœæ-]', '', suite)
    if nu in GARDE_TRAIT or '-' in nu or (nu[:1].isupper() and not a[-2:-1].isupper()):
        return a + b
    return a[:-1] + b


def typo(s):
    s = re.sub(r'\s*\((\d)\)', '', s)  # appels de notes
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([,.;?!)])', r'\1', s)
    s = re.sub(r'\s*:\s*', ' : ', s)
    s = re.sub(r'«\s*', '« ', s)
    s = re.sub(r'\s*»', ' »', s)
    s = re.sub(r'\(\s+', '(', s)
    s = s.replace("'", '’')
    return s.strip()


INTITULE = re.compile(r'(ARTICLE|QUESTION)\b')
MARQUE = re.compile(r'(\d+°|Il paro[iî]t|Mais |\(Conclusion|Il faut dire|Je réponds|Ces observations|Disons donc)')
FIN = re.compile(r'[.?!:»)]$')


def paragraphes(lignes):
    """Paragraphes d'après la mise en page : intitulés ; « ¶ » en tête d'une ligne corrigée (alinéa relu sur l'image) ;
    sinon, après une ligne finie par une ponctuation forte, une ligne plus courte que la justification (fin d'alinéa)
    ou une marque de la structure de l'article (« 2° », « Mais », « Je réponds »…)."""
    longueurs = sorted(len(l['t']) for l in lignes) or [0]
    pleine = longueurs[len(longueurs) // 2]
    paras = []
    prec = None
    for l in lignes:
        t = l['t']
        force = t.startswith('¶')
        t = t.lstrip('¶ ')
        neuf = (force or not paras or INTITULE.match(t) or INTITULE.match(paras[-1])
                or (prec is not None and FIN.search(prec) and (len(prec) < 0.88 * pleine or MARQUE.match(t))))
        if not neuf and len(paras) >= 2 and INTITULE.match(paras[-2]) and FIN.search(prec or ''):
            neuf = True  # après le titre (une ligne ou deux) d'une question ou d'un article
        if neuf:
            paras.append(t)
        else:
            paras[-1] = recoller(paras[-1], t)
        prec = t
    return [typo(p) for p in paras]


NUM = re.compile(r'^\d+(°|\. )')  # « 2. » : faute d'impression pour « 2° » (Iª q. 3 a. 4)


def decouper_article(ps, ref):
    """ps : paragraphes d'un article, après « ARTICLE … » et le titre."""
    obj, sc, co, rep = [], [], [], []
    etat = 'obj'
    for p in ps:
        if p.startswith('(Conclusion'):
            # un seul alinéa, fermé d'ordinaire par « .) » (une fois par « » » : Iª q. 3 a. 1, faute d'impression)
            etat = 'apres-concl'
            continue
        if p.startswith(('Je réponds aux', 'Ces observations renferment la réponse')):
            etat = 'rep'
            rep.append(p)
            continue
        if etat == 'obj':
            if p.startswith('Mais '):
                etat = 'sc'
                sc.append(p)
            elif (NUM.match(p) and not (len(obj) == 1 and p.startswith('1°') and '1°' not in obj[0])) or not obj:
                obj.append(p)
            else:
                obj[-1] += '\n\n' + p
        elif etat == 'sc':
            sc.append(p)
        elif etat == 'apres-concl' or etat == 'co':
            etat = 'co'
            co.append(p)
        elif etat == 'rep':
            if NUM.match(p):
                rep.append(p)
            else:
                rep[-1] += '\n\n' + p
    if not co:
        raise SystemExit(f'{ref} : pas de corps de l’article')
    return obj, '\n\n'.join(sc), '\n\n'.join(co), rep


def latin_titre(s):
    return s


def main():
    R = {p['page']: p for p in json.load(open(sys.argv[1]))}
    cor = charger_corrections(sys.argv[2])
    LA = json.load(open(sys.argv[3]))
    TL = json.load(open(sys.argv[4]))
    PAGES = json.load(open(sys.argv[5]))
    dest = sys.argv[6]
    os.makedirs(dest, exist_ok=True)
    index = []
    source = {
        'fr': {'ouvrage': 'Somme théologique de S. Thomas d’Aquin, traduite en français et annotée par F. Lachat',
               'edition': 'Paris, Louis Vivès, 4e édition, 1880, tome premier (même composition que l’édition de 1874)',
               'url': 'https://archive.org/details/sommetheologique01thom',
               'controle': 'https://archive.org/details/sommethologique07lachgoog'},
        'la': {'ouvrage': 'Sancti Thomae Aquinatis Opera omnia iussu impensaque Leonis XIII P. M. edita, t. IV : '
                          'Pars prima Summae theologiae a quaestione I ad quaestionem XLIX',
               'edition': 'Romae, ex Typographia Polyglotta S. C. de Propaganda Fide, 1888',
               'url': 'https://archive.org/details/operaomniaiussui04thom',
               'transcription': 'https://www.corpusthomisticum.org/sth1001.html (E. Alarcón, d’après l’édition léonine)'},
    }
    for q in sorted(PAGES, key=int):
        p0, p1 = PAGES[q]
        lignes = []
        for n in range(p0, p1 + 1):
            lignes += [dict(l, page=n) for l in lignes_corrigees(R[n], cor)]
        # une question commence sur sa page, une autre peut finir avant : on coupe aux intitulés
        debut = next(i for i, l in enumerate(lignes) if re.match(r'QUESTION\b', l['t']))
        lignes = lignes[debut:]
        fin = next((i for i, l in enumerate(lignes) if i > 0 and re.match(r'QUESTION\b', l['t'])), len(lignes))
        lignes = lignes[:fin]
        pages_art = collections.OrderedDict()
        ps = paragraphes(lignes)
        # pages : première page de chaque article (pour la référence)
        cur = None
        for l in lignes:
            if re.match(r'ARTICLE\b', l['t']):
                cur = len(pages_art) + 1
                pages_art[cur] = [l['page'] - 3, l['page'] - 3]
            elif cur:
                pages_art[cur][1] = l['page'] - 3
        titre_fr = ps[1]
        i = 2
        pro = []
        while not ps[i].startswith('ARTICLE'):
            pro.append(ps[i])
            i += 1
        arts = []
        bloc = None
        for p in ps[i:]:
            if p.startswith('ARTICLE'):
                bloc = []
                arts.append(bloc)
            else:
                bloc.append(p)
        Q = LA[q]
        tq = TL[q]
        if len(arts) != len(Q['articles']):
            raise SystemExit(f'q. {q} : {len(arts)} articles en français, {len(Q["articles"])} en latin')
        articles = []
        for k, bloc in enumerate(arts, 1):
            ref = f'Iª q. {q} a. {k}'
            la = Q['articles'][str(k)]
            titre = bloc[0]
            obj, sc, co, rep = decouper_article(bloc[1:], ref)
            if len(obj) != len(la['arg']):
                raise SystemExit(f'{ref} : {len(obj)} objections en français, {len(la["arg"])} en latin')
            if len(rep) != len(la['ad']) and not (len(rep) == 1 and len(la['ad']) <= 1):
                print(f'{ref} : {len(rep)} réponses en français, {len(la["ad"])} en latin', file=sys.stderr)
            n = max(len(rep), len(la['ad']))
            reponses = [{'la': la['ad'][j] if j < len(la['ad']) else '', 'fr': rep[j] if j < len(rep) else ''}
                        for j in range(n)]
            articles.append({
                'ref': ref,
                'titre': {'la': tq['articles'][str(k)], 'fr': titre},
                'objections': [{'la': a, 'fr': f} for a, f in zip(la['arg'], obj)],
                'sed_contra': {'la': la['sc'], 'fr': sc},
                'respondeo': {'la': la['co'], 'fr': co},
                'reponses': reponses,
                'pages': {'fr': pages_art[k]},
            })
            index.append({'ref': ref, 'fichier': f'Ia-{int(q):02d}.json', 'question': int(q), 'article': k})
        doc = {
            'ref': f'Iª q. {q}',
            'partie': 'Ia',
            'question': int(q),
            'titre': {'la': tq['titre'], 'fr': titre_fr},
            'prooemium': {'la': Q['pr'], 'fr': '\n\n'.join(pro)},
            'articles': articles,
            'source': dict(source, pages_fr=[p0 - 3, p1 - 3]),
            'revision': 1,
        }
        json.dump(doc, open(f'{dest}/Ia-{int(q):02d}.json', 'w'), ensure_ascii=False, indent=1)
        print(f'q. {q} : {len(articles)} articles')
    json.dump({'note': 'Ordre de lecture de la Somme théologique (un article par jour, à la suite).',
               'articles': index}, open(f'{dest}/index.json', 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
