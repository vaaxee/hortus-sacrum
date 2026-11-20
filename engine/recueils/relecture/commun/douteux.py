"""Repérage des mots douteux d'un recueil (fautes d'OCR probables), à trancher ensuite sur le scan.

Usage : python3 -I douteux.py <recueil.json> [vulgate.json] > douteux.tsv
Un mot est douteux s'il n'est ni dans le dictionnaire français (pyspellchecker), ni dans la Vulgate (latin des
citations), ni fréquent dans l'ensemble des recueils de data/recueils (≥ 3 fois : graphies de l'époque, noms).
Sont aussi signalés les motifs typiques : « cæur », chiffres collés aux mots, « (c » pour « « », « 11 » pour
« Il », lettre isolée inattendue, mot coupé non recollé (« xxx- yyy »), signes étrangers (€, ^, |, /).
Sortie : mot, nombre, clé, contexte (une ligne par mot ou motif).
"""
import collections, glob, json, os, re, sys
from spellchecker import SpellChecker

F = sys.argv[1]
VUL = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/vul/v.json'
sp = SpellChecker(language='fr')
MOT = r"[A-Za-zÀ-ÿœŒæÆ]+"
LAT = set()
try:
    for b in json.load(open(VUL))['books']:
        for c in b['chapters']:
            for v in c['verses']: LAT.update(w.lower() for w in re.findall(MOT, v['text']))
except Exception:
    pass
corpus = collections.Counter()
for g in glob.glob(os.path.join(os.path.dirname(os.path.abspath(F)), '*.json')):
    for e in json.load(open(g)).get('entrees', []):
        for k in ('corps', 'sommaire', 'titre'):
            if isinstance(e.get(k), str): corpus.update(w.lower() for w in re.findall(MOT, e[k]))
d = json.load(open(F))
MOTIFS = [r"c[æa]eur", r"\b\d+[a-zà-ÿ]{2,}|\b[a-zà-ÿ]{2,}\d+\b", r"\(c ", r"\b1[1l] (?=[a-zé])", r"[€^|/\\]",
          r"\b[a-zé]{2,}- [a-zé]{2,}\b", r"\b[bcfghkmpqrtvwxzBCFGHKMPQRTVWXZ]\b(?![.'’])", r"[a-zé][A-Z][a-z]"]
out = collections.defaultdict(list)
for e in d['entrees']:
    for k in ('titre', 'sommaire', 'corps'):
        t = e.get(k)
        if not isinstance(t, str): continue
        for m in re.finditer(MOT, t):
            w = m.group(0); x = w.lower()
            if x in sp or x in LAT or corpus[x] >= 3: continue
            if w[0].isupper() and corpus[x] >= 2: continue
            out[w].append((e['cle'], t[max(0, m.start() - 40):m.end() + 40]))
        for p in MOTIFS:
            for m in re.finditer(p, t):
                out['~' + m.group(0)].append((e['cle'], t[max(0, m.start() - 40):m.end() + 40]))
for w, l in sorted(out.items(), key=lambda x: x[0].lower()):
    print(f"{w}\t{len(l)}\t{l[0][0]}\t{l[0][1]!r}")
