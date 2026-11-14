"""Les quatre Évangiles, latin (Vulgate clémentine) et français (Crampon 1923), verset par verset.

Sources :
  - français : Wikisource, « Bible Crampon 1923/<livre> » (transcription relue sur le fac-similé Desclée 1923) ;
    pages téléchargées par l'API (action=parse) dans le dossier donné en argument (Matthieu.json, Marc.json…) ;
  - latin : Vulgate clémentine (scrollmapper/bible_databases, VulgClementine), fichier VULGATE.
Usage : python3 -I evangiles.py <dossier des pages> <vulgate.json> <sortie.json>
Les notes, sommaires de chapitre et intertitres de Crampon sont écartés : seul le texte des versets est gardé.
"""
import json, re, sys
from bs4 import BeautifulSoup

D, VUL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
LIVRES = [('mt', 'Matthieu', 'Matthew', 'Évangile selon saint Matthieu'), ('mc', 'Marc', 'Mark', 'Évangile selon saint Marc'),
          ('lc', 'Luc', 'Luke', 'Évangile selon saint Luc'), ('jn', 'Jean', 'John', 'Évangile selon saint Jean')]
vul = {b['name']: b for b in json.load(open(VUL))['books']}


def francais(page):
    html = json.load(open(f'{D}/{page}.json'))['parse']['text']
    s = BeautifulSoup(html, 'html.parser')
    for x in s.select('sup.reference, sup.verset-num, span.pagenum, .ws-pagenum, h1, h2, h3, h4, h5, h6, div.alineanegatif, .lettrine, ol.references, .mw-references-wrap, style, .headertemplate'):
        x.decompose()
    for a in s.select('a[href="#Sommaire"]'):  # numéro de chapitre en tête de chapitre
        (a.parent if a.parent.name == 'div' else a).decompose()
    # sommaires de Crampon (« 1. Chap. xxi, 1-22. L’entrée triomphale… », « Jésus retourne en Galilée… (1-4) ») :
    # paragraphes sans repère de verset, faits seulement d'italiques, de petites capitales et de numéros
    import copy
    for el in s.find_all('div'):  # dans cette édition, le texte des versets est toujours dans des <p>
        if el.parent and not el.find('span', id=re.compile(r'^\d+-\d+$')) and el.find_parent('p') is None: el.decompose()
    for el in s.find_all(['p', 'div']):
        if el.find('span', id=re.compile(r'^\d+-\d+$')) or not el.get_text(strip=True): continue
        c = copy.copy(el)
        for x in c.find_all(['i', 'span'], class_=lambda k: True): x.decompose()
        for x in c.find_all('i'): x.decompose()
        if len(re.sub(r'[\W\d_]|Chap|vers', '', c.get_text())) < 3: el.decompose()
    # la lettrine : la lettre est retirée avec .lettrine-lettre ? on la remet devant le mot en petites capitales
    html = str(s)
    # repère de verset : <span id="C-V">
    morceaux = re.split(r'<span id="(\d+)-(\d+)"></span>', html)
    vs = {}
    for i in range(1, len(morceaux) - 2, 3):
        c, v, corps = int(morceaux[i]), int(morceaux[i + 1]), morceaux[i + 2]
        t = BeautifulSoup(corps, 'html.parser').get_text()
        t = re.sub(r'\s+', ' ', t.replace('\xa0', ' ')).strip()
        vs[(c, v)] = t
    return vs


def lettrines(page):
    """Lettres des lettrines (début de chaque livre ou chapitre), à remettre devant les petites capitales."""
    html = json.load(open(f'{D}/{page}.json'))['parse']['text']
    return re.findall(r'<span id="(\d+)-(\d+)">.*?class="lettrine-lettre"[^>]*>([^<]+)<', html)


livres = []
for lid, page, nom_vul, titre in LIVRES:
    fr = francais(page)
    for c, v, l in lettrines(page):
        k = (int(c), int(v))
        if k in fr and not fr[k].startswith(l): fr[k] = l + fr[k]
    b = vul[nom_vul]
    chapitres = []
    for ch in b['chapters']:
        n = ch['chapter']
        # latin et français gardent chacun leur numérotation (Crampon suit le grec : Jn 6, 52-72 par ex.)
        chapitres.append({'n': n, 'la': [[x['verse'], x['text']] for x in ch['verses']],
                          'fr': [[v, t] for (c, v), t in sorted(fr.items()) if c == n]})
    print(lid, len(chapitres), 'chapitres ; versets la/fr :', sum(len(c['la']) for c in chapitres), sum(len(c['fr']) for c in chapitres),
          'écarts :', [(c['n'], len(c['la']), len(c['fr'])) for c in chapitres if len(c['la']) != len(c['fr'])])
    livres.append({'id': lid, 'titre': titre, 'chapitres': chapitres})

json.dump({
    'source': {
        'fr': {'ouvrage': 'La Sainte Bible, traduction d’après les textes originaux par l’abbé A. Crampon', 'edition': 'Desclée, 1923 (transcription Wikisource)',
               'url': 'https://fr.wikisource.org/wiki/Bible_Crampon_1923'},
        'la': {'ouvrage': 'Biblia Sacra Vulgatæ editionis (Clémentine)', 'url': 'https://github.com/scrollmapper/bible_databases'}},
    'livres': livres}, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
