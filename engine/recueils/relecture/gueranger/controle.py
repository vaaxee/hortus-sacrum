"""Guéranger : contrôle qu'une relecture n'a touché que des entrées en OCR (jamais une entrée à « source »).

Usage : python3 -I controle.py <NN> [<NN> ...]   (compare data/recueils/gueranger/vNN.json à la version de HEAD)
"""
import json, subprocess, sys
from pathlib import Path

RAC = Path(__file__).resolve().parents[4]
mal = 0
for nn in sys.argv[1:]:
    f = f'data/recueils/gueranger/v{nn}.json'
    A = json.loads(subprocess.run(['git', '-C', str(RAC), 'show', f'HEAD:{f}'], capture_output=True, text=True, check=True).stdout)['entrees']
    B = json.load(open(RAC / f))['entrees']
    p = sum(1 for a, b in zip(A, B) if a.get('source') and a != b)
    o = sum(1 for a, b in zip(A, B) if not a.get('source') and a != b)
    mal += p + (len(A) != len(B))
    print(f'v{nn} : entrées propres modifiées {p} ; entrées OCR modifiées {o}')
sys.exit(1 if mal else 0)
