"""Neuvaines de la Notice sur le Tiers-Ordre (Québec, 1867), relues page à page sur l'image (archive.org cihm_29653).
Usage : python3 -I engine/recueils/francois1867/inserer.py
Ajoute ou remplace dans data/prieres/sources.json les pièces décrites dans pieces.json (corps = fichiers .md joints).
Le bloc « A la fin de chaque exercice », imprimé après la prière du 1er jour, est rangé à la fin de la pièce."""
import json, pathlib

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parents[2] / 'data/prieres/sources.json'
d = json.loads(SRC.read_text(encoding='utf-8'))
for p in json.loads((ICI / 'pieces.json').read_text(encoding='utf-8')):
    p['corps'] = '\n\n'.join((ICI / f).read_text(encoding='utf-8').strip() for f in p.pop('fichiers'))
    i = next((k for k, x in enumerate(d['pieces']) if x['id'] == p['id']), None)
    if i is None:
        d['pieces'].append(p)
    else:
        d['pieces'][i] = p
    print(p['id'], len(p['corps']))
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
