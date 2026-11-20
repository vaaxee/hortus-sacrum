"""Guéranger : prépare un dossier de travail pour les outils de commun/ (douteux, proposer, traits, parasites, trois,
accents), limité aux entrées encore en OCR d'un volume (les entrées reprises d'un texte propre, champ « source »,
ne sont jamais proposées).

Usage : python3 -I cible.py <NN> <dossier>
Écrit <dossier>/cible.json (entrées OCR du volume NN) et, à côté, les autres recueils et volumes, qui servent de
lexique (le volume NN lui-même n'y est pas, pour ne pas compter deux fois ses propres fautes).
"""
import glob, json, os, shutil, sys
from pathlib import Path

NN, D = sys.argv[1], Path(sys.argv[2])
R = Path(__file__).resolve().parents[4] / 'data' / 'recueils'
D.mkdir(parents=True, exist_ok=True)
for f in D.glob('*.json'): f.unlink()
for f in R.glob('*.json'): shutil.copy(f, D / f.name)
for f in (R / 'gueranger').glob('v*.json'):
    if f.stem != f'v{NN}': shutil.copy(f, D / f'g_{f.name}')
d = json.load(open(R / 'gueranger' / f'v{NN}.json'))
d['entrees'] = [e for e in d['entrees'] if not e.get('source')]
json.dump(d, open(D / 'cible.json', 'w'), ensure_ascii=False)
print(f'v{NN} : {len(d["entrees"])} entrées en OCR')
