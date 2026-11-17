"""Copie dans data/prieres/sources.json les pièces relues d'un dossier de transcription.
Usage : python3 -I inserer.py <dossier> [sources.json]
Le dossier contient `pieces.json` : une liste de pièces au format de sources.json, où « corps » est remplacé par
« fichier » (le texte relu, en balisage de l'app, à côté). Une pièce déjà présente sous le même id n'est remplacée que
si elle a la même source et la même partie (pièce ajoutée par ce même manifeste, relue de nouveau) ; sinon le script
s'arrête sans rien écrire. Les nouvelles pièces vont après la dernière pièce de même préfixe."""
import json, os, re, sys

dossier = sys.argv[1]
cible = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'prieres', 'sources.json')
manifeste = json.load(open(os.path.join(dossier, 'pieces.json'), encoding='utf-8'))
d = json.load(open(cible, encoding='utf-8'))
P = d['pieces']
ids = {p['id']: i for i, p in enumerate(P)}
ORDRE = ['id', 'titre', 'partie', 'categorie', 'usage', 'indulgence', 'latin', 'corps', 'source']

for m in manifeste:
    corps = open(os.path.join(dossier, m['fichier']), encoding='utf-8').read().strip()
    corps = re.sub(r"\n{3,}", "\n\n", corps)
    piece = {k: (corps if k == 'corps' else m.get(k, '')) for k in ORDRE}
    if m['id'] in ids:
        ancien = P[ids[m['id']]]
        if ancien.get('source') != m['source'] or ancien.get('partie') != m['partie']:
            sys.exit(f"{m['id']} existe déjà et ne vient pas de ce dossier : on n'y touche pas")
        P[ids[m['id']]] = piece
        continue
    prefixe = m['id'].split(':')[0] + ':'
    apres = max([i for i, p in enumerate(P) if p['id'].startswith(prefixe)], default=len(P) - 1)
    P.insert(apres + 1, piece)
    ids = {p['id']: i for i, p in enumerate(P)}
    print('ajoutée :', m['id'])

with open(cible, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write('\n')
