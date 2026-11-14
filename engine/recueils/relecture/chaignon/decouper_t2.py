"""Chaignon, t. 2 : le découpage de 2026 avait laissé dans « S:95 » (Conformité… ce que l'âme y trouve) la
méditation LI (L'amour de Dieu, ses motifs), l'entrée de l'Avent et les méditations des 1er et 2e dimanches de
l'Avent, dont les titres étaient illisibles à la machine (pages où l'encre du verso transparaît).

Usage : python3 -I decouper_t2.py fusion|couper <chaignon.json>
  fusion : met T:Adv3-0 à la suite de S:95 (la page recopiée 289 est à cheval sur les deux) ;
  couper : une fois les pages recopiées remises (pages_manuelles.py), coupe aux intitulés « N. MÉDITATION. ».
"""
import json, re, sys

MODE, F = sys.argv[1], sys.argv[2]
d = json.load(open(F))
E = d['entrees']
cle = {e['cle']: i for i, e in enumerate(E)}
if MODE == 'fusion':
    s, t = E[cle['S:95']], E[cle['T:Adv3-0']]
    s['corps'] = s['corps'].rstrip() + '\n\n' + t['corps'].lstrip()
    t['corps'] = ''
    t['_fusionne'] = True
else:
    i = cle['S:95']
    s = E[i]
    c = s['corps']
    NOUVELLES = [
        ('LI', {'cle': 'S:96', 'titre': 'L’amour de Dieu. — Ses motifs', 'numero': 'LI', 'partie': 'parcours'}),
        ('I', {'cle': 'T:Adv1-0', 'titre': 'Premier dimanche de l’Avent. — Devoirs du chrétien par rapport au triple avénement de Jésus-Christ', 'numero': 'I', 'partie': 'liturgie'}),
        ('II', {'cle': 'T:Adv2-0', 'titre': 'Deuxième dimanche de l’Avent. — La prédication de saint Jean-Baptiste. — Elle s’adresse principalement aux pécheurs', 'numero': 'II', 'partie': 'liturgie'}),
        ('III', None),
    ]
    coupes = []
    for num, meta in NOUVELLES:
        m = re.search(rf"(?:^|\n\n)(?:## )?{num}\.\s+MÉDITATION\.?\s*\n\n", c)
        assert m, num
        coupes.append((m.start(), m.end(), meta))
    # l'entrée de l'Avent (« SECTION PREMIÈRE… ») ouvre la méditation du 1er dimanche
    sec = c.find('SECTION PREMIÈRE')
    assert coupes[0][0] < sec < coupes[1][0]
    morceaux = []
    bornes = [0] + [x[0] for x in coupes] + [len(c)]
    for k in range(len(bornes) - 1):
        morceaux.append(c[bornes[k]:bornes[k + 1]])
    # morceau 0 : S:95 ; 1 : LI (jusqu'à la section) + section ; 2 : I ; 3 : II ; 4 : III
    li = morceaux[1]
    j = li.find('SECTION PREMIÈRE')
    entree_avent = li[j:]
    morceaux[1] = li[:j]
    morceaux[2] = morceaux[2]  # garde l'intitulé pour le nettoyage ci-dessous
    def nettoie(m, prefixe=''):
        m = re.sub(r"^\s*(?:## )?[IVXL]+\.\s+MÉDITATION\.?\s*\n\n", '', m)
        # l'intitulé en capitales (déjà dans le titre)
        P = [p for p in m.split('\n\n')]
        while P and (not P[0].strip() or (P[0].upper() == P[0] and re.search(r"[A-Z]{4}", P[0]))):
            P.pop(0)
        return prefixe + '\n\n'.join(P).strip()
    avent = entree_avent
    avent = re.sub(r"^SECTION PREMIÈRE\.\s*\n\nL\s?AVENT ET NOËL\.\s*\n\n§ I\. PROPRE DU TEMPS\.\s*\n\n", '', avent)
    s['corps'] = re.sub(r"^l’âme y TROUVE\.\s*", '', morceaux[0].strip())
    s['titre'] = 'Conformité à la volonté de Dieu. — Ce que l’âme y trouve'
    nouvelles = [dict(NOUVELLES[0][1], tome=2, page=0, corps=nettoie(morceaux[1])),
                 dict(NOUVELLES[1][1], tome=2, page=0, corps=nettoie(morceaux[2], avent.strip() + '\n\n')),
                 dict(NOUVELLES[2][1], tome=2, page=0, corps=nettoie(morceaux[3]))]
    t = E[cle['T:Adv3-0']]
    t.pop('_fusionne', None)
    t['corps'] = nettoie(morceaux[4])
    E[i + 1:i + 1] = nouvelles[:1]
    j = [k for k, e in enumerate(E) if e['cle'] == 'T:Adv3-0'][0]
    E[j:j] = nouvelles[1:]
    for e in [s] + nouvelles + [t]:
        print(e['cle'], len(e['corps']), repr(e['corps'][:120]))
json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
