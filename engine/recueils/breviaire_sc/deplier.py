"""Petit bréviaire du Sacré-Cœur : déplie les renvois de chaque heure avec le texte des Matines du même jour.

Le livre (Nancy, 1883) abrège les petites heures : « Gloire soit au Père, etc. », « ℣. O Cœur d'amour, etc. »
et « Le reste comme à Matines ». Consigne de l'utilisateur (21 nov. 2026) : produire tout le texte à chaque heure.
Chaque renvoi est remplacé par le texte imprimé aux Matines du même jour, recopié tel quel ; rien n'est ajouté.
Rejouable : un second passage ne change rien.  Usage : python3 engine/recueils/breviaire_sc/deplier.py [--ecrire]
"""
import json, re, sys, unicodedata

CHEMIN = 'data/prieres/sources.json'
JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']


def norm(s):
	s = s.replace('œ', 'oe').replace('Œ', 'Oe').lower()
	s = unicodedata.normalize('NFKD', s)
	return re.sub(r'[^a-z ]', '', ''.join(c for c in s if not unicodedata.combining(c))).split()


def deplier(corps):
	secs = re.split(r'(?m)^(?=## )', corps)
	mat_i = next(i for i, s in enumerate(secs) if s.startswith('## À Matines'))
	mat = secs[mat_i].rstrip('\n').split('\n')
	gloire = next(l for l in mat if l.startswith('Gloire soit au Père, et au Fils'))
	sortie = []
	for s in secs:
		if not s.startswith('## À ') or s.startswith('## À Matines'):
			sortie.append(s)
			continue
		lignes = s.rstrip('\n').split('\n')
		fin = s[len(s.rstrip('\n')):]
		res, reste_de = [], None
		for l in lignes:
			if l.strip() == 'Gloire soit au Père, etc.':
				res.append(gloire)
				continue
			m = re.match(r'℣\. (.*?),? etc\.\s*"?\s*$', l)
			if m:
				cle = norm(m.group(1))
				idx = next((i for i, x in enumerate(mat) if x.startswith('℣.') and norm(x[2:])[: len(cle)] == cle), None)
				if idx is None:
					raise SystemExit(f'℣ introuvable aux Matines : {l!r}')
				j = next(k for k in range(idx + 1, len(mat)) if mat[k].startswith('℟.'))
				res.extend(mat[idx : j + 1])
				reste_de = j + 1
				continue
			if l.strip() == '*Le reste comme à Matines.*':
				if reste_de is None:
					raise SystemExit('« Le reste » sans ℣ repris avant')
				suite = mat[reste_de:]
				while suite and not suite[0].strip():
					suite = suite[1:]
				res.extend(suite)
				continue
			res.append(l)
		sortie.append('\n'.join(res) + fin)
	return ''.join(sortie)


if __name__ == '__main__':
	doc = json.load(open(CHEMIN, encoding='utf-8'))
	pieces = doc['pieces']
	liste = pieces.values() if isinstance(pieces, dict) else pieces
	change = 0
	for p in liste:
		if not any(p['id'] == f'breviaire-sc:office-{j}' for j in JOURS):
			continue
		neuf = deplier(p['corps'])
		if neuf != p['corps']:
			p['corps'] = neuf
			p['revision'] = (p.get('revision') or 0) + 1
			change += 1
		print(p['id'], 'renvois restants :', len(re.findall(r'etc\.|Le reste comme', neuf)))
	if '--ecrire' in sys.argv and change:
		with open(CHEMIN, 'w', encoding='utf-8') as f:
			json.dump(doc, f, ensure_ascii=False, indent=1)
			f.write('\n')
	print('pièces changées :', change)
