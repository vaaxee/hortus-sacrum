"""S. Alphonse de Liguori, Visites au Saint Sacrement et à la sainte Vierge pour chaque jour du mois
(trad. revue par le P. Baudrant, Lyon, Perisse, 1862 ; PDF Google de bibliotheque-catholique.com).

Usage : python3 -I visites.py <visites.pdf> <sortie.json>
Couche texte Google, pages 23 à 144 du PDF : titres courants et numéros de page retirés, mots coupés recollés,
découpage en une entrée par jour (J:1 … J:31), précédée de l'introduction (prières pour chaque visite).
"""
import json, re, subprocess, sys
from spellchecker import SpellChecker
SP = SpellChecker(language='fr')
PDF, OUT = sys.argv[1], sys.argv[2]
TESS = sys.argv[3] if len(sys.argv) > 3 else None  # dossier de la seconde lecture (hamon/prep.py) : traits d'union vus
import csv, glob, unicodedata
def nu(w): return ''.join(c for c in unicodedata.normalize('NFD', w.lower()) if not unicodedata.combining(c))
COUPES = set()
if TESS:
    for f in glob.glob(f"{TESS}/tess*/*.tsv"):
        lignes = {}
        for r in csv.DictReader(open(f, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
            if r['level'] == '5' and r['text'].strip():
                lignes.setdefault((int(r['block_num']), int(r['par_num']), int(r['line_num'])), []).append(r['text'].strip())
        cles = sorted(lignes)
        for a, b in zip(cles, cles[1:]):
            x, y = lignes[a][-1], lignes[b][0]
            if x.endswith(('-', '—', '¬')) and len(x) > 1:
                COUPES.add((nu(re.sub(r"\W+$", "", x).split("'")[-1].split("’")[-1]), nu(re.sub(r"\W+$", "", y))))
URL = ("https://pdfs.bibliotheque-catholique.com/pdfs/oeuvres-completes/saint-alphonse-de-liguori/"
       "Saint%20Alphonse%20de%20Liguori%20-%20Visites%20au%20Saint%20Sacrement%20et%20%C3%A0%20la%20Sainte%20Vierge"
       "%20pour%20tous%20les%20jours%20du%20mois.pdf")
COURANT = re.compile(r"^\s*(\d{1,3}|\.?\d{1,3}|VISITES? (AU|DU) SAINT SAC\w*\s*\.?(, etc\.)?|ET A LA SAINTE VIERGE\s*[.,]?|"
                     r"INTRODUC\w* POUR LES VISITES|AU SAINT SACREMENT\s*\.?|LA COMMUNION SPIRITUELLE\s*\.?)\s*$", re.I)
pages = []
for p in range(23, 145):
    t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), PDF, '-'], capture_output=True, text=True).stdout
    L = [l.replace('>>', '»').replace('<<', '«') for l in t.split('\n')]
    # titres courants : seulement dans les 4 premières lignes non vides de la page
    out, vus = [], 0
    for l in L:
        if l.strip() and vus < 4:
            vus += 1
            if COURANT.match(l): continue
        out.append(l)
    pages.append((p, '\n'.join(out)))
# saut de page : fin de phrase → nouveau paragraphe ; sinon la phrase continue
texte = ''
for _, t in pages:
    t = t.strip()
    if not texte: texte = t; continue
    texte += ('\n\n' if re.search(r"[.!?:»]\s*$", texte) and re.match(r"[A-ZÉÀÈÔ«]", t) else '\n') + t
# titres des visites : « N VISITE » seul sur sa ligne (ou « VISITE AU SAINT SACRE… »), en alternance
# Saint Sacrement / sainte Vierge ; la ligne suivante (« AU SAINT SACREMENT. », « A LA SAINTE VIERGE. ») est retirée
L = texte.split('\n'); out = []; n = 0; sauter = False
for l in L:
    if sauter:
        sauter = False
        if re.match(r"^\s*(A|AU|DU)?\s*(LA )?SAINT[E ]?\s*(VIERGE|SACRE\w*|Vierge|vierge)\s*[.,]?\s*$", l, re.I): continue
    if re.match(r"^\s*(PREMIÈRE|[IVXL]+\s*[e•·°.]?)?\s*VISITE(\s+AU SAINT SACRE\w*)?\s*[.,]?\s*$", l):
        out += ['', '@@SS@@' if n % 2 == 0 else '@@SV@@', '']; n += 1; sauter = True; continue
    # intertitres et rubriques : paragraphes à part
    if re.match(r"^\s*([OG]RAISON|PRIÈRE|ACTE|Oraison d|Prière d)", l):
        out += ['', l.strip(), '']; continue
    out.append(l)
texte = '\n'.join(out)
print(n, 'titres de visite')
# guillemets de continuation (« » » en tête de chaque ligne d'une citation) : retirés tant que la citation est ouverte
L = texte.split('\n'); ouvert = 0
for i, l in enumerate(L):
    if ouvert > 0 and re.match(r"^\s*»\s?D?\s*(?=\S)", l) and not re.match(r"^\s*»\s*$", l):
        L[i] = re.sub(r"^\s*»\s?D?\s*", "", l)
    ouvert += L[i].count('«') - L[i].count('»')
    ouvert = max(ouvert, 0)
# mots coupés en fin de ligne dont la couche texte a perdu le trait d'union (« coû / té ») : recollés si les deux
# morceaux ne sont pas des mots et que le mot entier en est un
def mot(w): return w.lower().strip("'’") in SP
for i in range(len(L) - 1):
    a = re.search(r"([A-Za-zÀ-ÿœæ'’]+)\s*$", L[i]); b = re.match(r"^\s*([a-zà-ÿœæ]+)(.*)$", L[i + 1])
    if not a or not b or L[i].rstrip().endswith('-'): continue
    x, y = a.group(1).split("'")[-1].split("’")[-1], b.group(1)
    if (mot(x + y) and not (mot(x) and mot(y))) or (nu(x), nu(re.sub(r"\W+$", "", y))) in COUPES:
        L[i] = L[i][:a.end(1)]  + y; L[i + 1] = b.group(2).lstrip()
texte = '\n'.join(L)
# mots coupés en fin de ligne, puis paragraphes
texte = re.sub(r"(\w)-\n\s*([a-zàâçéèêëîïôûùüœ])", r"\1\2", texte)
paras = [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", texte)]
paras = [re.sub(r"\s{2,}", " ", p) for p in paras if p]
# guillemets de continuation « » » en début de ligne recollés
paras = [re.sub(r"(?<=\S) » (?=[a-zà-ÿ])", " ", p) for p in paras]
corps = '\n\n'.join(paras)
# typographie de la couche texte (espaces avant la virgule, autour des traits d'union) ; lettrine en capitales
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[1]))
from hamon import traits  # noqa: E402
corps = traits(corps)
corps = re.sub(r"\bJésus\s?Christ\b", "Jésus-Christ", corps)
corps = re.sub(r"^INTRODUCTION POUR LES VISITES\s*", "", corps)
corps = re.sub(r"\s+([,.)])", r"\1", corps)
corps = re.sub(r"\(\s+", "(", corps)
corps = re.sub(r"(\w)-\s+(nous|vous|moi|toi|lui|en|y|le|la|les|je|il|elle|on)\b", r"\1-\2", corps)
corps = re.sub(r"(\w)\s+-(nous|vous|moi|toi|lui|en|y|le|la|les|je|il|elle|on)\b", r"\1-\2", corps)
corps = re.sub(r"(?m)^([A-ZÉÈÀ][A-ZÉÈÀ']+)(?= [a-zà-ÿ])", lambda m: m.group(1)[0] + m.group(1)[1:].lower(), corps)
corps = re.sub(r"(?m)^([A-Z]')([A-ZÉÈ]+)(?= [a-zà-ÿ])", lambda m: m.group(1) + m.group(2).lower(), corps)
# mots collés ou coupés par la couche texte, d'après le dictionnaire (graphies anciennes gardées : ame, sentimens…)
LAT = set()
try:
    for b in json.load(open('/tmp/claude-0/vul/v.json'))['books']:
        for ch in b['chapters']:
            for v in ch['verses']: LAT.update(w.lower() for w in re.findall(r"[a-zæœA-ZÆŒ]+", v['text']))
except Exception:
    pass
def connu(w):
    k = w.lower().split("'")[-1].split("’")[-1]
    return not k or k in SP or k in LAT
PRON = r"(moi|toi|nous|vous|les|le|la|lui|en|y|leur|je|il|on)"
COURTS = {'à', 'a', 'y', 'ô', 'o', 'je', 'il', 'me', 'te', 'se', 'le', 'la', 'un', 'de', 'du', 'ne', 'en', 'et', 'ou', 'où'}
def ancien(w):
    """Graphie ancienne ou forme rare mais juste : enfans, tourmens ; vécussent, fûtes ; pluriels."""
    k = w.lower()
    return (k in ('ame', 'ames', 'separez', 'desire', 'demeuve') or (k.endswith('ns') and connu(k[:-2] + 'nts')) or (k.endswith('s') and connu(k[:-1]))
            or re.search(r"(ssent|sse|ssions|ssiez|ât|ît|ût|ûtes|îtes|âtes)$", k) is not None)
def decoller(m):
    w = m.group(0)
    suiv = m.string[m.end():m.end() + 1]
    if connu(w) or len(w) < 4 or w[0].isupper() or suiv == '.' or ancien(w): return w
    p = re.fullmatch(rf"(.+?){PRON}", w)
    if p and connu(p.group(1)) and p.group(1).lower().endswith(('ez', 'ons', 'ais', 'ait', 'it')) and len(p.group(1)) > 2:
        return p.group(1) + '-' + p.group(2)
    if re.fullmatch(r"(moi|toi|lui|nous|vous|soi|eux|elle)(même|mêmes)", w): return re.sub(r"(même)", r"-\1", w)
    if re.fullmatch(r"(les|le|la)(moi|nous|lui|leur)", w): return re.sub(r"^(les|le|la)", r"\1-", w)
    cands = [(w[:i], w[i:]) for i in range(1, len(w))
             if (len(w[:i]) > 2 or w[:i].lower() in COURTS) and (len(w[i:]) > 2 or w[i:] in COURTS)
             and w[:i].lower() in SP and w[i:].lower() in SP]
    return ' '.join(cands[0]) if len(cands) == 1 else w
def recoller(m):
    a, b = m.group(1), m.group(2)
    if (not connu(a) or not connu(b)) and connu(a + b) and len(a + b) > 3: return a + b
    return m.group(0)
for _ in range(2):
    corps = re.sub(r"\b([A-Za-zÀ-ÿœæ]+) ([a-zà-ÿœæ]+)\b", recoller, corps)
# titres courants restés dans le texte, ordinal de visite isolé
corps = re.sub(r"(?:\b\S{1,4} )?\b(?:ET )?A L[AÀ] [A-ZÉÈ]{3,} VI[A-Za-zÉ]{3,}\.?\s*", " ", corps)
corps = re.sub(r"\s*\d*\s*VISITES? (?:AU|DU) [A-ZİÉ]+ [A-ZÉ]+\.?\s*", " ", corps)
corps = re.sub(r"\n\n[IVXL]+\s*$", "", corps)
# mot coupé par un signe parasite (« tou. te », « Sa» crement ») : recollé si le mot entier est connu
def signe(m):
    a, b = m.group(1), m.group(2)
    return a + b if connu(a + b) and (not connu(a) or not connu(b)) else m.group(0)
corps = re.sub(r"\b([A-Za-zÀ-ÿœæ]+)[-.,»«▪•❤☛◄、·]\s*([a-zà-ÿœæ]+)\b", signe, corps)
# trait d'union suivi d'une espace : mot coupé (recollé) ou mot composé (par-dessus, long-temps)
def trait(m):
    a, b = m.group(1), m.group(2)
    if connu(a + b) and not (connu(a) and connu(b)): return a + b
    return a + '-' + b
corps = re.sub(r"\b([A-Za-zÀ-ÿœæ]+)- ([a-zà-ÿœæ]+)\b", trait, corps)
corps = re.sub(r"\b([A-Za-zÀ-ÿœæ]+) -([a-zà-ÿœæ]+)\b", trait, corps)
corps = re.sub(r"\s*\n\nVISITES\n\nET\n\n\s*,\s*POUR CHAQUE JOUR DU MOIS\.\s*$", "", corps, flags=re.M)

corps = re.sub(r"[A-Za-zÀ-ÿœæ]+(?:['’][A-Za-zÀ-ÿœæ]+)?", decoller, corps)
corps = re.sub(r"(?m)^[OG]RAISON JACULATOIRE\s*\.*$", "### Oraison jaculatoire", corps)
corps = re.sub(r"(?m)^([OG]RAISON|PRIÈRE|ACTE)( [^\n]{0,60})$", lambda m: "### " + m.group(0).strip(), corps)
corps = re.sub(r" (La communion spirituelle\.)\s*$", r"\n\n*\1*", corps, flags=re.M)
corps = re.sub(r"(?m)^(La communion spirituelle\.|Faites la communion spirituelle[^\n]*)$", r"*\1*", corps)
ORD = r"(?:PREMIÈRE|[IVXL1]+\s*[e•·°]?\.?)?"
TETE = lambda qui: re.compile(rf"(?:^|\n\n|(?<=\.) ){ORD}\s*VISITE\s*(?:\n\n|\s)\s*{qui}\s*[.,]?\s*")
SS, SV = TETE(r"(?:AU|DU) SAINT SAC\w*"), TETE(r"A LA SAINTE VIERGE")
# corrections relues (mot de la couche texte → mot du livre)
CORR = json.load(open(__import__('pathlib').Path(__file__).with_name('visites_corrections.json')))
for a, b in CORR:
    corps = corps.replace(a, b)
manque = [a for a, b in CORR if a in corps]
if manque: print('corrections non appliquées :', manque)
coupe = list(re.finditer(r"@@SS@@", corps))
print(len(coupe), 'jours')
E = [{'cle': 'I:0', 'titre': 'Introduction : prières pour chaque visite, communion spirituelle', 'corps': corps[:coupe[0].start()]}]
NOMS = ['Premier', 'Deuxième', 'Troisième', 'Quatrième', 'Cinquième', 'Sixième', 'Septième', 'Huitième', 'Neuvième', 'Dixième',
        'Onzième', 'Douzième', 'Treizième', 'Quatorzième', 'Quinzième', 'Seizième', 'Dix-septième', 'Dix-huitième', 'Dix-neuvième',
        'Vingtième', 'Vingt et unième', 'Vingt-deuxième', 'Vingt-troisième', 'Vingt-quatrième', 'Vingt-cinquième', 'Vingt-sixième',
        'Vingt-septième', 'Vingt-huitième', 'Vingt-neuvième', 'Trentième', 'Trente et unième']
for k, m in enumerate(coupe):
    fin = coupe[k + 1].start() if k + 1 < len(coupe) else len(corps)
    c = corps[m.end():fin].strip()
    c = '## Visite au saint Sacrement\n\n' + c
    c, n = re.subn(r"\s*@@SV@@\s*", "\n\n## Visite à la sainte Vierge\n\n", c)
    if n != 1: print('jour', k + 1, ':', n, 'titres de visite à la sainte Vierge')
    E.append({'cle': f'J:{k + 1}', 'titre': f'{NOMS[k]} jour', 'corps': c})
json.dump({'id': 'liguori-visites', 'titre': 'Visites au Saint Sacrement et à la sainte Vierge pour chaque jour du mois',
           'auteur': 'S. Alphonse de Liguori (traduction revue par le P. Baudrant)',
           'editions': {'1': 'Lyon, Perisse frères, 1862'},
           'provenance': 'bibliotheque-catholique.com (scan Google) ; couche texte relue', 'url': URL, 'entrees': E},
          open(OUT, 'w'), ensure_ascii=False, indent=1)
