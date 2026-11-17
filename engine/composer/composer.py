"""Pages composées (SPEC § 10) : plusieurs textes déjà sourcés, mis bout à bout dans une seule page, sans rien réécrire.
  - Triple Couronne d'or : une page par couronne (ordinaire + propre à sa place) ;
  - Offrande du matin : les actes du livret en une page ;
  - Chapelet : une page par série de mystères (manière de saint Dominique, méthode de Montfort, trois Ave de sainte Mechtilde).
Usage : python3 -I engine/composer/composer.py   (réécrit les pièces hortus:* composées dans data/prieres/sources.json)"""
import json, pathlib, re

RACINE = pathlib.Path(__file__).resolve().parents[2]
JARDIN = json.loads((RACINE / 'data/prieres/jardin.json').read_text())
SRC_P = RACINE / 'data/prieres/sources.json'
SRC = json.loads(SRC_P.read_text())
J = {p['id']: p for p in JARDIN['pieces']}
S = {p['id']: p for p in SRC['pieces']}


def bloc(b):
    """Même conversion que blocsVersCorps (app/src/lib/seed.ts)."""
    t = b.get('type')
    if t in ('texte', 'invocation'): return b.get('texte') or ''
    if t == 'conclusion': return f"*{b['texte']}*"
    if t in ('rubrique', 'notice'): return '[r]' + re.sub(r'\n+', ' ', b.get('texte') or '') + '[/r]'
    if t == 'intertitre': return f"## {b['texte']}"
    if t == 'traduction': return f"[{b['texte']}]"
    if t == 'verset': return f"℣. {b['v']}\n℟. {b['r']}"
    if t == 'mystere': return f"[r]{b['numero']}[/r] {b['texte']}\n*{b['fruit_libelle']}* {b['fruit']}"
    return b.get('texte') or ''


def corps(blocs, niveau=0):
    out = [bloc(b) for b in blocs]
    if niveau: out = [re.sub(r'^## ', '#' * (2 + niveau) + ' ', x) for x in out]
    return '\n\n'.join(x for x in out if x)


def jardin_source(*ids):
    pages = sorted({J[i]['page_livret'] for i in ids if J[i].get('page_livret')}, key=lambda x: int(x))
    return {'ouvrage': 'Le Jardin de l’âme (livret)', 'edition': 'Le Jardin de l’âme (livret)',
            'page': ('p. ' + ', '.join(str(p) for p in pages)) if pages else ''}


pieces = []

# --- Triple Couronne d'or : ordinaire + propre de la couronne, à leur place ---
ORD = J['la-triple-couronne-d-or-du-sacre-c-ur-de-jesus']['blocs']
COUR = ['premiere-couronne-le-sacre-c-ur-de-jesus-dans-son-incarnatio',
        'deuxieme-couronne-le-sacre-c-ur-de-jesus-dans-sa-passion',
        'troisieme-couronne-le-sacre-c-ur-de-jesus-dans-l-eucharistie']
NOMS = ['Première', 'Deuxième', 'Troisième']
for n, cid in enumerate(COUR):
    pr = J[cid]['blocs']
    jours = pr[0]
    invocation = [b for b in pr if b['type'] == 'texte'][0]
    mysteres = [b for b in pr if b['type'] == 'mystere']
    out = [jours]
    for b in ORD[1:]:  # la 1re rubrique (répartition des couronnes) est remplacée par les jours de celle-ci
        if b['type'] == 'rubrique' and b['texte'].startswith('On ajoute l’invocation propre'):
            out += [{'type': 'intertitre', 'texte': 'Invocation propre'}, invocation]
            continue
        if b['type'] == 'intertitre' and b['texte'] == 'Prières finales':
            out += [{'type': 'intertitre', 'texte': 'Mystères'}] + mysteres
        out.append(b)
    titre = J[cid]['titre'].split(' : ')[1]
    pieces.append({'id': f'hortus:triple-couronne-{n + 1}', 'titre': f'Triple Couronne d’or — {NOMS[n].lower()} couronne : {titre}',
                   'partie': 'Couronnes et chapelets', 'categorie': 'Sacré-Cœur',
                   'usage': 'Ordinaire et propre de la couronne du jour, en une seule page.',
                   'indulgence': '', 'latin': '', 'corps': corps(out), 'source': jardin_source('la-triple-couronne-d-or-du-sacre-c-ur-de-jesus', cid)})

# --- Offrande du matin : les actes du livret, en une page ---
ACTES = ['intention-d-indulgences', 'acte-de-soumission-a-la-volonte-de-dieu',
         'acte-d-intention-de-communion-spirituelle-perpetuelle', 'acte-de-recommandation-des-ames-rencontrees']
DEVOIRS = ['devoir-envers-l-eglise-et-ses-ministres', 'devoir-envers-la-famille', 'devoir-envers-la-patrie',
           'devoir-envers-les-pauvres-les-persecutes-les-affliges', 'devoir-envers-moi-meme']
parts = []
for a in ACTES:
    parts += [f"## {J[a]['titre']}", corps(J[a]['blocs'], 1)]
parts.append('## Actes des devoirs de charité')
for a in DEVOIRS:
    parts += [f"### {J[a]['titre']}", corps(J[a]['blocs'], 2)]
pieces.append({'id': 'hortus:offrande-du-matin', 'titre': 'Offrande du matin', 'partie': 'Offrande du matin',
               'categorie': 'Matin', 'usage': 'Les actes de l’offrande du matin, à la suite de la prière du matin.',
               'indulgence': '', 'latin': '', 'corps': '\n\n'.join(parts), 'source': jardin_source(*ACTES, *DEVOIRS)})

# --- Chapelet : une page par série de mystères ---
M = S['montfort:methode-rosaire']['corps']
debut, reste = M.split('## Mystères joyeux', 1)
series = {'joyeux': reste.split('## Mystères douloureux')[0],
          'douloureux': reste.split('## Mystères douloureux')[1].split('## Mystères glorieux')[0],
          'glorieux': reste.split('## Mystères glorieux')[1].split('## Dieu seul')[0]}
fin = '## Dieu seul' + M.split('## Dieu seul')[1]
dominique = S['sambucy:chapelet-saint-dominique']['corps'].replace('## ', '### ')
ave = S['gertrude:trois-ave-bonne-mort']['corps']
for nom, m in series.items():
    c = '\n\n'.join([
        '## Le chapelet de saint Dominique', dominique,
        '## Ouverture (méthode de saint Louis-Marie de Montfort)', debut.strip(),
        '### Les trois Ave de sainte Mechtilde', '*On peut dire les trois Ave sous cette forme :*', ave,
        f'## Mystères {nom}', m.strip(), fin.strip()])
    pieces.append({'id': f'hortus:chapelet-{nom}', 'titre': f'Chapelet — mystères {nom}', 'partie': 'Rosaire',
                   'categorie': 'Chapelets',
                   'usage': 'Une page par chapelet : manière de saint Dominique, méthode de saint Louis-Marie de Montfort, trois Ave de sainte Mechtilde. Sources : '
                            + ' ; '.join(f"{S[i]['source']['ouvrage']} ({S[i]['source'].get('page', '')})" for i in
                                         ['sambucy:chapelet-saint-dominique', 'montfort:methode-rosaire', 'gertrude:trois-ave-bonne-mort']) + '.',
                   'indulgence': '', 'latin': '', 'corps': c, 'source': S['montfort:methode-rosaire']['source']})

ids = {p['id'] for p in pieces}
SRC['pieces'] = [p for p in SRC['pieces'] if p['id'] not in ids] + pieces
SRC_P.write_text(json.dumps(SRC, ensure_ascii=False, indent=1) + '\n')
print('\n'.join(f"{p['id']} : {len(p['corps'])}" for p in pieces))

# --- indulgences : les pages composées reprennent la fiche du texte principal ---
IND_P = RACINE / 'data/prieres/indulgences.json'
IND = json.loads(IND_P.read_text())
for n in (1, 2, 3):
    IND['fiches'][f'hortus:triple-couronne-{n}'] = IND['fiches']['jardin:la-triple-couronne-d-or-du-sacre-c-ur-de-jesus']
for nom in series:
    IND['fiches'][f'hortus:chapelet-{nom}'] = IND['fiches']['sambucy:chapelet-saint-dominique']
IND_P.write_text(json.dumps(IND, ensure_ascii=False, indent=1) + '\n')
