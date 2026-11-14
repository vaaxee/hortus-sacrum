"""La Bible, latin (Vulgate clémentine) et français (Crampon 1923), livre par livre.

Sources :
  - français : Wikisource, « Bible Crampon 1923/<livre> » (transcription relue sur le fac-similé Desclée 1923),
    pages téléchargées par l'API (action=parse) dans le dossier donné en argument (<page>.json) ;
  - latin : Vulgate clémentine (scrollmapper/bible_databases, VulgClementine).
Usage : python3 -I bible.py <dossier des pages> <vulgate.json> <dossier de sortie data/ecriture> <livres-bible.ts>
Chaque texte garde sa numérotation : Crampon suit l'hébreu ou le grec, la Vulgate la sienne (psaumes, Siracide,
Jn 6…). Les notes, sommaires et intertitres de Crampon sont écartés : seul le texte des versets est gardé.
"""
import copy, json, os, re, sys
from bs4 import BeautifulSoup

D, VUL, OUT, TS = sys.argv[1:5]
# abréviation, pages Wikisource, nom dans la Vulgate, nom en français
LIVRES = [
    ('Gn', ['Genèse'], 'Genesis', 'La Genèse'), ('Ex', ['Exode'], 'Exodus', 'L’Exode'), ('Lv', ['Lévitique'], 'Leviticus', 'Le Lévitique'),
    ('Nb', ['Nombres'], 'Numbers', 'Les Nombres'), ('Dt', ['Deutéronome'], 'Deuteronomy', 'Le Deutéronome'), ('Jos', ['Josué'], 'Joshua', 'Josué'),
    ('Jg', ['Juges'], 'Judges', 'Les Juges'), ('Rt', ['Ruth'], 'Ruth', 'Ruth'), ('1 S', ['1 Samuel'], 'I Samuel', 'Premier livre de Samuel'),
    ('2 S', ['2 Samuel'], 'II Samuel', 'Deuxième livre de Samuel'), ('1 R', ['1 Rois'], 'I Kings', 'Premier livre des Rois'),
    ('2 R', ['2 Rois'], 'II Kings', 'Deuxième livre des Rois'), ('1 Ch', ['1 Chroniques'], 'I Chronicles', 'Premier livre des Chroniques'),
    ('2 Ch', ['2 Chroniques'], 'II Chronicles', 'Deuxième livre des Chroniques'), ('Esd', ['Esdras'], 'Ezra', 'Esdras'),
    ('Ne', ['Néhémie'], 'Nehemiah', 'Néhémie'), ('Tb', ['Tobie'], 'Tobit', 'Tobie'), ('Jdt', ['Judith'], 'Judith', 'Judith'),
    ('Est', ['Esther'], 'Esther', 'Esther'), ('Jb', ['Job'], 'Job', 'Job'), ('Ps', ['Psaumes 1', 'Psaumes 2', 'Psaumes 3', 'Psaumes 4', 'Psaumes 5'], 'Psalms', 'Les Psaumes'),
    ('Pr', ['Proverbes'], 'Proverbs', 'Les Proverbes'), ('Qo', ['Ecclésiaste'], 'Ecclesiastes', 'L’Ecclésiaste'),
    ('Ct', ['Cantique'], 'Song of Solomon', 'Le Cantique des cantiques'), ('Sg', ['Sagesse'], 'Wisdom', 'La Sagesse'),
    ('Si', ['Ecclésiastique'], 'Sirach', 'L’Ecclésiastique'), ('Is', ['Isaïe'], 'Isaiah', 'Isaïe'), ('Jr', ['Jérémie'], 'Jeremiah', 'Jérémie'),
    ('Lm', ['Lamentations'], 'Lamentations', 'Les Lamentations'), ('Ba', ['Baruch'], 'Baruch', 'Baruch'), ('Ez', ['Ézéchiel'], 'Ezekiel', 'Ézéchiel'),
    ('Dn', ['Daniel'], 'Daniel', 'Daniel'), ('Os', ['Osée'], 'Hosea', 'Osée'), ('Jl', ['Joël'], 'Joel', 'Joël'), ('Am', ['Amos'], 'Amos', 'Amos'),
    ('Ab', ['Abdias'], 'Obadiah', 'Abdias'), ('Jon', ['Jonas'], 'Jonah', 'Jonas'), ('Mi', ['Michée'], 'Micah', 'Michée'), ('Na', ['Nahum'], 'Nahum', 'Nahum'),
    ('Ha', ['Habacuc'], 'Habakkuk', 'Habacuc'), ('So', ['Sophonie'], 'Zephaniah', 'Sophonie'), ('Ag', ['Aggée'], 'Haggai', 'Aggée'),
    ('Za', ['Zacharie'], 'Zechariah', 'Zacharie'), ('Ml', ['Malachie'], 'Malachi', 'Malachie'),
    ('1 M', ['1 Machabées'], 'I Maccabees', 'Premier livre des Machabées'), ('2 M', ['2 Machabées'], 'II Maccabees', 'Deuxième livre des Machabées'),
    ('Mt', ['Matthieu'], 'Matthew', 'Saint Matthieu'), ('Mc', ['Marc'], 'Mark', 'Saint Marc'), ('Lc', ['Luc'], 'Luke', 'Saint Luc'),
    ('Jn', ['Jean'], 'John', 'Saint Jean'), ('Ac', ['Actes des Apôtres', 'Actes'], 'Acts', 'Les Actes des Apôtres'),
    ('Rm', ['Romains'], 'Romans', 'Épître aux Romains'), ('1 Co', ['1 Corinthiens'], 'I Corinthians', 'Première épître aux Corinthiens'),
    ('2 Co', ['2 Corinthiens'], 'II Corinthians', 'Deuxième épître aux Corinthiens'), ('Ga', ['Galates'], 'Galatians', 'Épître aux Galates'),
    ('Ep', ['Éphésiens'], 'Ephesians', 'Épître aux Éphésiens'), ('Ph', ['Philippiens'], 'Philippians', 'Épître aux Philippiens'),
    ('Col', ['Colossiens'], 'Colossians', 'Épître aux Colossiens'), ('1 Th', ['1 Thessaloniciens'], 'I Thessalonians', 'Première épître aux Thessaloniciens'),
    ('2 Th', ['2 Thessaloniciens'], 'II Thessalonians', 'Deuxième épître aux Thessaloniciens'), ('1 Tm', ['1 Timothée'], 'I Timothy', 'Première épître à Timothée'),
    ('2 Tm', ['2 Timothée'], 'II Timothy', 'Deuxième épître à Timothée'), ('Tt', ['Tite'], 'Titus', 'Épître à Tite'), ('Phm', ['Philémon'], 'Philemon', 'Épître à Philémon'),
    ('He', ['Hébreux'], 'Hebrews', 'Épître aux Hébreux'), ('Jc', ['Jacques'], 'James', 'Épître de saint Jacques'),
    ('1 P', ['1 Pierre'], 'I Peter', 'Première épître de saint Pierre'), ('2 P', ['2 Pierre'], 'II Peter', 'Deuxième épître de saint Pierre'),
    ('1 Jn', ['1 Jean'], 'I John', 'Première épître de saint Jean'), ('2 Jn', ['2 Jean'], 'II John', 'Deuxième épître de saint Jean'),
    ('3 Jn', ['3 Jean'], 'III John', 'Troisième épître de saint Jean'), ('Jude', ['Jude'], 'Jude', 'Épître de saint Jude'),
    ('Ap', ['Apocalypse'], 'Revelation of John', 'L’Apocalypse'),
]
vul = {b['name']: b for b in json.load(open(VUL))['books']}
VERSET = re.compile(r'^(\d+)-(\d+)$')


def francais(page):
    """Versets de la page : {(chapitre, verset): texte}."""
    f = f'{D}/{page}.json'
    if not os.path.exists(f): return {}
    try: d = json.load(open(f))
    except ValueError: return {}  # téléchargement incomplet
    if 'parse' not in d: return {}
    html = d['parse']['text']
    lettres = {(int(c), int(v)): l for c, v, l in re.findall(r'<span id="(\d+)-(\d+)">.*?class="lettrine-lettre"[^>]*>([^<]+)<', html)}
    s = BeautifulSoup(html, 'html.parser')
    for x in s.select('sup.reference, sup.verset-num, span.pagenum, .ws-pagenum, h1, h2, h3, h4, h5, h6, div.alineanegatif, .lettrine, ol.references, .mw-references-wrap, style, .headertemplate'):
        x.decompose()
    for a in s.select('a[href="#Sommaire"]'):  # numéro de chapitre en tête de chapitre
        (a.parent if a.parent.name == 'div' else a).decompose()
    for el in s.find_all('div'):  # le texte des versets est dans des <p> (ou des <div> qui contiennent un repère)
        if el.parent and not el.find('span', id=VERSET) and el.find_parent('p') is None: el.decompose()
    # sommaires : paragraphes sans repère de verset, faits seulement d'italiques, de petites capitales et de numéros
    for el in s.find_all('p'):
        if el.find('span', id=VERSET) or not el.get_text(strip=True): continue
        c = copy.copy(el)
        for x in c.find_all(['i', 'span']): x.decompose()
        if len(re.sub(r'[\W\d_]|Chap|vers', '', c.get_text())) < 3: el.decompose()
    morceaux = re.split(r'<span id="(\d+)-(\d+)"></span>', str(s))
    vs = {}
    for i in range(1, len(morceaux) - 2, 3):
        c, v = int(morceaux[i]), int(morceaux[i + 1])
        t = BeautifulSoup(morceaux[i + 2], 'html.parser').get_text()
        t = re.sub(r'\s+', ' ', t.replace('\xa0', ' ')).strip()
        if (c, v) in lettres and not t.startswith(lettres[(c, v)]): t = lettres[(c, v)] + t
        if (c, v) in vs: vs[(c, v)] += ' ' + t  # repère répété (verset coupé par une page)
        else: vs[(c, v)] = t
    return vs


def slug(abr): return abr.replace(' ', '').lower()


os.makedirs(OUT, exist_ok=True)
index = []
for abr, pages, nom_vul, titre in LIVRES:
    fr = {}
    for p in pages:  # psaumes : les cinq livres à la suite ; Actes : la première page qui a le texte
        x = francais(p)
        if x and abr != 'Ps': fr = x; break
        fr.update(x)
    b = vul[nom_vul]
    nfr = max([c for c, _ in fr] or [0])
    chapitres = []
    for n in range(1, max(len(b['chapters']), nfr) + 1):
        ch = next((c for c in b['chapters'] if c['chapter'] == n), None)
        chapitres.append({'n': n, 'la': [[x['verse'], x['text']] for x in ch['verses']] if ch else [],
                          'fr': [[v, t] for (c, v), t in sorted(fr.items()) if c == n]})
    vides = [c['n'] for c in chapitres if not c['fr']]
    print(f"{abr:5} ch. {len(chapitres):3}  la {sum(len(c['la']) for c in chapitres):5}  fr {sum(len(c['fr']) for c in chapitres):5}  sans français : {vides[:12]}{'…' if len(vides) > 12 else ''}")
    json.dump({'id': slug(abr), 'abr': abr, 'titre': titre, 'chapitres': chapitres}, open(f'{OUT}/{slug(abr)}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    index.append((abr, slug(abr), titre, len(chapitres), bool(fr)))

json.dump({
    'fr': {'ouvrage': 'La Sainte Bible, traduction d’après les textes originaux par l’abbé A. Crampon', 'edition': 'Desclée, 1923 (transcription Wikisource)',
           'url': 'https://fr.wikisource.org/wiki/Bible_Crampon_1923'},
    'la': {'ouvrage': 'Biblia Sacra Vulgatæ editionis (Clémentine)', 'url': 'https://github.com/scrollmapper/bible_databases'}},
    open(f'{OUT}/source.json', 'w'), ensure_ascii=False)

lignes = ',\n'.join(f"\t'{a}': {{ id: '{i}', nom: {json.dumps(t, ensure_ascii=False)}, chapitres: {n}{'' if f else ', latinSeul: true'} }}" for a, i, t, n, f in index)
open(TS, 'w').write(f"""// Généré par engine/ecriture/bible.py : livres de la Bible présents dans data/ecriture (ne pas modifier à la main).
export interface LivreBible {{ id: string; nom: string; chapitres: number; latinSeul?: boolean }}
export const LIVRES: Record<string, LivreBible> = {{
{lignes}
}};
""")
