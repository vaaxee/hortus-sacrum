"""Fillion : assemble les pages relues (pages/p<NNN>.txt) en data/office/breviaire-fr/psautier-fillion.json.

Usage : python3 -I assembler.py      (HEBDO_DO_DEPOT=<clone de Divinum Officium> si vendor/do n'est pas dans ce dépôt)

- Un titre « Psaume <romain> » ouvre un psaume (numérotation de la Vulgate) ; un titre de cantique ouvre le cantique
  désigné dans CANTIQUES (première ligne du titre → fichier PsalmNNN.txt de Divinum Officium).
- Une ligne « v| » commence un verset, « c| » le continue ; le texte d'un verset est rendu sur une seule ligne.
- Renvoi typographique « [fin » en bout de ligne : fin de la ligne précédente (mot coupé « pen- [sées » ressoudé).
- Les numéros des versets sont ceux du latin de Divinum Officium (Psalterium/Psalmorum/PsalmN.txt), pris dans l'ordre
  où le latin les donne ; le nombre de versets imprimés doit être égal, sinon l'assemblage s'arrête.
- Alignement avec le latin livré (data/office/breviaire/*/communs.json, une ligne par ligne de DO) : `lignes_la`
  (par psaume) = étiquettes des lignes latines de DO (« 2a », « 2b », « 3 »…) ; `ligne_la` (par verset) = étiquette de
  la ligne où le verset commence. Une ligne latine sans verset qui y commence continue le verset précédent.
"""
import json, os, re, sys
from pathlib import Path
from spellchecker import SpellChecker

ICI = Path(__file__).resolve().parent
ROOT = ICI.parents[3]
DO = Path(os.environ.get('HEBDO_DO_DEPOT', ROOT / 'vendor' / 'do'))
PSALMORUM = DO / 'web' / 'www' / 'horas' / 'Latin' / 'Psalterium' / 'Psalmorum'
SORTIE = ROOT / 'data' / 'office' / 'breviaire-fr' / 'psautier-fillion.json'
sp = SpellChecker(language='fr')

# titre imprimé (début) → (fichier DO, titre gardé, référence imprimée[, versets imprimés, note])
# (versets imprimés : quand DO ne numérote pas ses lignes par verset)
CANTIQUES = {
    'Cantique de la Bienheureuse Vierge Marie': (232, 'Cantique de la Bienheureuse Vierge Marie', 'Luc. i, 46-55'),
    'Cantique des trois jeunes gens. Dan. iii, 52': (220, 'Cantique des trois jeunes gens', 'Dan. iii, 52-57',
                                                   list(range(52, 58)),
                                                   "Divinum Officium numérote ses lignes 3:52 à 3:58 (le v. 52 "
                                                   "en deux lignes) : numéros de Fillion, sans alignement ligne à "
                                                   "ligne."),
    'Cantique des trois jeunes gens. Dan. iii, 57': (210, 'Cantique des trois jeunes gens', 'Dan. iii, 57-88 et 56',
                                       list(range(57, 89)) + [56],
                                       "Divinum Officium chante ce cantique deux versets par ligne (lignes numérotées "
                                       "3:57 à 3:74, puis la doxologie et le v. 56) : numéros de Fillion, sans "
                                       "alignement ligne à ligne ; la doxologie (« Bénissons le Père… ») est imprimée "
                                       "avec le v. 88."),
    'Cantique de Zacharie': (231, 'Cantique de Zacharie', 'Luc. i, 68-79'),
    "Cantique d'Isaïe. Is. xii": (221, "Cantique d'Isaïe", 'Is. xii, 1-6', list(range(1, 7)),
                                   "Divinum Officium chante ce cantique en 7 lignes numérotées 12:1 à 12:7, qui ne "
                                   "suivent pas les versets de la Vulgate (6 versets, comme chez Fillion) : numéros "
                                   "de Fillion, sans alignement ligne à ligne."),
    'Cantique de Tobie': (212, 'Cantique de Tobie', 'Tob. xiii, 1-10', list(range(1, 11)),
                          "Divinum Officium chante ce cantique en 11 lignes numérotées 13:1 à 13:11, coupées autrement "
                          "que les 10 versets de Fillion : numéros de Fillion, sans alignement ligne à ligne."),
    "Cantique d'Ézéchias": (222, "Cantique d'Ézéchias", 'Is. xxxviii, 10-20', list(range(10, 21)),
                            "Divinum Officium chante ce cantique en 15 lignes numérotées 38:10 à 38:24, coupées "
                            "autrement que les 11 versets de Fillion : numéros de Fillion, sans alignement ligne à "
                            "ligne."),
    'Cantique de David': (211, 'Cantique de David', 'I Par. xxix, 10-13'),
    'Cantique de Siméon': (233, 'Cantique de Siméon', 'Luc. ii, 29-32'),
}

# psaumes dont le latin de DO ne suit pas la division de Fillion : numéros imprimés par Fillion (premier, et note)
SANS_DO = {
    94: (1, "Psaume invitatoire : Divinum Officium donne à Matines le texte du psautier romain (« Quia in manu ejus "
            "sunt omnes fines terræ »), en 10 versets ; Fillion traduit le psaume 94 de la Vulgate, en 11 versets. "
            "Numérotation de Fillion gardée ; pas d'alignement ligne à ligne avec le latin de l'invitatoire."),
}

# remarques sur la numérotation imprimée
NOTES = {
    9: "Fillion numérote les parties III et IV (Vulgate 9, 22-39 ; psaume 10 de l'hébreu) de 1 à 18 ; numérotation "
       "de la Vulgate (22-39) donnée ici, comme dans le latin.",
    113: "Fillion numérote la seconde partie (« Non nobis, Domine », Vulgate 113, 9-26 ; psaume 115 de l'hébreu) de 1 "
         "à 18 ; numérotation de la Vulgate (9-26) donnée ici, comme dans le latin.",
    115: "Fillion numérote ce psaume de 10 à 19, à la suite du Ps 114 (l'hébreu en fait un seul psaume, 116) ; "
         "numérotation de la Vulgate (1-10) donnée ici, comme dans le latin.",
}

# psaumes dont DO numérote les lignes autrement que les versets de la Vulgate : verset → ligne latine où il commence
# (les étiquettes `lignes_la` restent celles de DO ; une ligne sans verset qui y commence continue le précédent)
DECOUPE = {
    42: ({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'},
         "Divinum Officium coupe ce psaume en 6 lignes numérotées 1-6 (« Confitebor tibi in cithara » = 5, « Spera in "
         "Deo » = 6) ; Fillion suit les 5 versets de la Vulgate (v. 4 jusqu'à « Deus meus », v. 5 « Quare tristis "
         "es… »). Le v. 5 commence au milieu de la ligne latine « 5 »."),
}

ROMAINS = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}


def romain(s):
    s = s.upper().replace('J', 'I')
    v = 0
    for i, c in enumerate(s):
        x = ROMAINS[c]
        v += -x if i + 1 < len(s) and ROMAINS[s[i + 1]] > x else x
    return v


def latin(fichier):
    """Latin de DO (Psalterium/Psalmorum/Psalm<fichier>.txt) : (versets dans l'ordre, étiquettes des lignes, verset →
    étiquette de la ligne où il commence). Une ligne peut porter plusieurs versets (« ‡ (4a) », « (9) ») ou un demi-verset
    (« 2a », « 2b ») : DO coupe le psaume pour le chant, pas toujours au verset."""
    ordre, etiquettes, debut = [], [], {}
    for l in (PSALMORUM / f'Psalm{fichier}.txt').read_text(encoding='utf-8').splitlines():
        m = re.match(r'^\d+:(\d+)([a-z]?)\s', l)
        if not m:
            continue
        lab = m.group(1) + m.group(2)
        if '(Fit reverentia' in l:
            lab = 'doxologie'   # Benedicite : « Benedicamus Patrem… », imprimé par Fillion avec le v. 88
        etiquettes.append(lab)
        vs = [] if lab == 'doxologie' else [int(m.group(1))]
        vs += [int(x) for x in re.findall(r'\((\d+)[a-z]?\)', l)]
        for v in vs:
            if v not in debut:
                debut[v] = lab
                ordre.append(v)
    # verset que DO laisse au milieu d'une ligne sans le marquer (Ps 76, 16 dans « 76:15 … redemisti ») :
    # rattaché à la ligne qui le contient
    if fichier < 200:
        for v in range(min(ordre), max(ordre) + 1):
            if v not in debut:
                debut[v] = debut[max(x for x in debut if x < v)]
        ordre = sorted(debut)
    return ordre, etiquettes, debut


def souder(a, b):
    """Recolle une ligne terminée par un trait d'union à la suivante."""
    if not a.endswith('-'):
        return a + ' ' + b
    m1 = re.search(r"([\wÀ-ÿœæ'-]+)-$", a)
    m2 = re.match(r"([\wÀ-ÿœæ]+)", b)
    if m1 and m2:
        mot = (m1.group(1).split("'")[-1] + m2.group(1)).lower()
        if mot in sp or mot.replace('œ', 'oe') in sp:
            return a[:-1] + b
        COUPES.append(f'{a[-20:]}|{b[:20]}')
        if (m1.group(1).split("'")[-1] + '-' + m2.group(1)).lower() in sp:
            return a + b
    return a[:-1] + b


COUPES = []


def lignes():
    for f in sorted((ICI / 'pages').glob('p*.txt')):
        p = int(f.stem[1:])
        for l in f.read_text(encoding='utf-8').splitlines():
            if l.startswith('#'):
                continue
            k, _, t = l.partition('| ')
            yield p, k, t.strip()


def assembler():
    pieces, cur, doutes = [], None, []
    prec = None          # dernière ligne de texte : [verset, indice de ligne]
    page_prec = None
    for p, k, t in lignes():
        if page_prec is not None and p not in (page_prec, page_prec + 2):
            cur, prec = None, None      # pages non relues entre deux : pas de suite possible
        page_prec = p
        if k == '?':
            doutes.append((p, t))
            continue
        if k == 'h':
            m = re.match(r'^Psaume\s+([IVXLCJ]+)\b', t, re.I)
            c = next((v for c_, v in CANTIQUES.items() if t.startswith(c_)), None)
            if m:
                n = romain(m.group(1))
                if not (cur and cur.get('numero') == n):
                    cur = {'numero': n, 'titre': f'Psaume {m.group(1).upper()}', 'versets': []}
                    pieces.append(cur)
            elif c:
                cur = {'do': f'Psalm{c[0]}', 'titre': c[1], 'reference': c[2], 'versets': []}
                if len(c) > 3:
                    cur['_ordre'], cur['note'] = c[3], c[4]
                pieces.append(cur)
            continue
        if cur is None:
            continue
        # renvoi « [fin » : rejoint la ligne précédente
        m = re.search(r'\s\[(\S.*)$', t)
        if m and prec is not None:
            t = t[:m.start()].rstrip()
            v, i = prec
            v['_l'][i] = souder(v['_l'][i], m.group(1)) if v['_l'][i].endswith('-') else v['_l'][i] + ' ' + m.group(1)
        if k == 'v':
            cur['versets'].append({'page': p, '_l': [t]})
        else:
            if not cur['versets']:
                raise SystemExit(f'p{p} : suite de verset sans verset : {t}')
            cur['versets'][-1]['_l'].append(t)
        prec = (cur['versets'][-1], len(cur['versets'][-1]['_l']) - 1)
    erreurs = []
    for pc in list(pieces):
        fichier = pc['numero'] if 'numero' in pc else int(pc['do'][5:])
        if '_ordre' in pc:
            ordre, etiq, debut = pc.pop('_ordre'), None, {}
        elif pc.get('numero') in SANS_DO:
            premier, note = SANS_DO[pc['numero']]
            ordre, etiq, debut = list(range(premier, premier + len(pc['versets']))), None, {}
            pc['note'] = note
        elif pc.get('numero') in DECOUPE:
            debuts, note = DECOUPE[pc['numero']]
            _, etiq, _ = latin(fichier)
            ordre, debut = list(debuts), dict(debuts)
            pc['note'] = note
        else:
            ordre, etiq, debut = latin(fichier)
        if os.environ.get('PARTIEL') and len(pc['versets']) < len(ordre):
            print(f"(en cours : {pc['titre']}, {len(pc['versets'])}/{len(ordre)} versets, omis)")
            pieces.remove(pc)
            continue
        if len(ordre) != len(pc['versets']):
            erreurs.append(f"{pc['titre']} : {len(pc['versets'])} versets imprimés, {len(ordre)} dans le latin de DO"
                           f" ({ordre[0]}-{ordre[-1]})")
            continue
        for v, n in zip(pc['versets'], ordre):
            txt = v.pop('_l')
            s = txt[0]
            for x in txt[1:]:
                s = souder(s, x)
            v['n'], v['fr'], v['ligne_la'] = n, re.sub(r'\s+', ' ', s).strip(), debut.get(n)
            if '[' in v['fr']:
                erreurs.append(f"{pc['titre']}, v. {n} : renvoi « [ » non résolu")
        pc['versets'] = [{k: v[k] for k in ('n', 'fr', 'page', 'ligne_la') if v.get(k) is not None} for v in pc['versets']]
        if etiq:
            pc['lignes_la'] = etiq
        if pc.get('numero') in NOTES:
            pc['note'] = NOTES[pc['numero']]
        pc['pages'] = sorted({v['page'] for v in pc['versets']})
    for p, d in doutes:
        mot = d.split(' — ')[0].strip()
        cible = [v for pc in pieces for v in pc['versets'] if isinstance(v, dict) and 'fr' in v and v['page'] in (p, p - 2) and mot in v['fr']]
        if not cible and os.environ.get('PARTIEL'):
            print(f'(doute p{p} « {mot} » : psaume en cours, gardé pour plus tard)')
        elif not cible:
            erreurs.append(f'p{p} : doute « {mot} » sans verset')
        else:
            cible[0].setdefault('lecture', []).append(f'p. {p} : {d}')
    if erreurs:
        print('\n'.join(erreurs))
        sys.exit(1)
    return pieces


if __name__ == '__main__':
    pieces = assembler()
    ancien = json.loads(SORTIE.read_text(encoding='utf-8')) if SORTIE.exists() else {}
    tete = {k: v for k, v in ancien.items() if k not in ('psaumes', 'cantiques')}
    psaumes = sorted([p for p in pieces if 'numero' in p], key=lambda p: p['numero'])
    cantiques = [p for p in pieces if 'do' in p]
    out = {**tete, 'psaumes': psaumes, 'cantiques': cantiques}
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(len(psaumes), 'psaumes,', sum(len(p['versets']) for p in psaumes), 'versets ;',
          len(cantiques), 'cantiques,', sum(len(p['versets']) for p in cantiques), 'versets')
    if COUPES:
        print('coupes à vérifier :', *COUPES, sep='\n  ')
