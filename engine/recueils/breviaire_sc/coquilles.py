"""Petit bréviaire du Sacré-Cœur : coquilles d'OCR relues sur le scan (PDF de l'utilisateur, p. 29-46).
- « misère ĺ » : le scan porte « misère ! » (p. 31).
- « amourpropre » : « amour-propre » (p. 36, coupure de ligne).
- trait d'union de fin de ligne suivi d'une espace (« recevez- moi », « Saint- Sacrement », « ici- bas ») : mot composé rejoint.
- point parasite entre deux mots en minuscules (« vos. plus pures », « chair. criminelle ») : retiré.
- « HYMNE O très » (lundi, Complies) : intertitre rétabli comme aux autres heures.
Rejouable ; usage : python3 engine/recueils/breviaire_sc/coquilles.py [--ecrire]
"""
import json, re, sys

CHEMIN = 'data/prieres/sources.json'
REGLES = [
	(r'misère ĺ', 'misère !'),
	(r'amourpropre', 'amour-propre'),
	(r'(?<=[a-zA-Zéèêàâîôûç])- (?=(moi|vous|bas|Sacrement|toi|nous|lui)\b)', '-'),
	(r'\b(vos|plus|chair|source)\. (?=[a-zé])', r'\1 '),
	(r'(?m)^HYMNE (?=O très amoureux)', '### Hymne\n\n'),
]
doc = json.load(open(CHEMIN, encoding='utf-8'))
change = 0
for p in doc['pieces']:
	if not p['id'].startswith('breviaire-sc:'):
		continue
	avant = p['corps']
	for a, b in REGLES:
		for m in re.finditer(a, p['corps']):
			print(p['id'], '|', p['corps'][max(0, m.start() - 25) : m.end() + 15].replace('\n', '⏎'))
		p['corps'] = re.sub(a, b, p['corps'])
	if p['corps'] != avant:
		change += 1
		if not p.get('revision'):
			p['revision'] = 1
if '--ecrire' in sys.argv and change:
	with open(CHEMIN, 'w', encoding='utf-8') as f:
		json.dump(doc, f, ensure_ascii=False, indent=1)
		f.write('\n')
print('pièces changées :', change)
