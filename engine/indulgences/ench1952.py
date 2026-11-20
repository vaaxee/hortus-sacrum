"""Mise en conformité des indulgences avec l'Enchiridion indulgentiarum de 1952 (demande du 19 nov. 2026).

Décret de la S. Pénitencerie du 3 mars 1952 (en tête de l'Enchiridion) : « obrogatis ceteris omnibus generalibus
indulgentiarum concessionibus, quae in hoc enchiridion non sint relatae » ; Praenotanda 2 : les œuvres reprises avec
changement suivent la nouvelle forme ; celles qui n'y sont pas « indulgentias amittunt ». Praenotanda 3 : les prières sont
données dans la langue de la concession ; pour les traductions, can. 934 § 2 (fidélité déclarée par la S. Pénitencerie
ou par un Ordinaire du lieu où la langue est en usage).

Les fiches tirées de « Thésaurisons pour le ciel » (1941, numérotation des Preces et Pia Opera de 1938) sont rapportées
ici à leur numéro de 1952, vérifié dans le texte de l'Enchiridion (édition vaticane 1952). Les traductions de
Thésaurisons sont certifiées fidèles selon le can. 934 § 2 (G. Chartier, vic. gén. de Montréal, 28 avril 1941).
Usage : python3 -I engine/indulgences/ench1952.py, puis verif1952.py (vérification fiche par fiche, 20 nov.).
"""
import json, pathlib

RACINE = pathlib.Path(__file__).resolve().parents[2]
P = RACINE / 'data/prieres/indulgences.json'
d = json.loads(P.read_text())
F = d['fiches']

# id → (n° Ench. 1952, langue de la concession, condition éventuelle)
NUMEROS = {
    'thesaurisons:jac-100': (274, 'latin', None), 'thesaurisons:jac-44': (113, 'latin', None),
    'thesaurisons:jac-105': (292, 'latin', None), 'thesaurisons:jac-19': (38, 'latin', None),
    'thesaurisons:jac-33': (70, 'italien', None), 'thesaurisons:jac-57': (154, 'latin', None),
    'thesaurisons:jac-206': (22, 'latin', None), 'thesaurisons:jac-71': (188, 'latin', None),
    'thesaurisons:jac-273': (302, 'latin', None),
    'thesaurisons:jac-199': (8, 'latin', 'chaque fois que l’on entend blasphémer contre Dieu'),
    'thesaurisons:jac-35': (73, 'latin', None),
    'thesaurisons:jac-37': (79, 'latin', 'devant le très saint Sacrement, même renfermé dans le tabernacle'),
    'thesaurisons:jac-70': (187, 'latin', None), 'thesaurisons:jac-90': (242, 'latin', None),
    'thesaurisons:jac-198': (5, 'latin', None), 'thesaurisons:jac-207': (39, 'français', None),
    'thesaurisons:jac-205': (15, 'italien', None), 'thesaurisons:jac-72': (191, 'latin', None),
    'thesaurisons:jac-12': (19, 'latin', None), 'thesaurisons:jac-204': (14, 'latin', None),
    'thesaurisons:jac-38': (85, 'latin', None), 'thesaurisons:jac-87': (236, 'français', None),
    'thesaurisons:jac-134': (386, 'italien', None), 'thesaurisons:jac-246': (237, 'latin', None),
    'thesaurisons:jac-275': (304, 'italien', None), 'thesaurisons:jac-85': (227, 'latin', None),
    'thesaurisons:jac-7': (11, 'latin', None),
    'thesaurisons:jac-14': (21, 'latin', 'le matin ou le soir'),
    'thesaurisons:jac-39': (84, 'latin', None), 'thesaurisons:jac-84': (226, 'français', None),
    'thesaurisons:jac-239': (228, 'français', None), 'thesaurisons:jac-242': (231, 'français', None),
    'thesaurisons:jac-274': (303, 'italien', None), 'thesaurisons:jac-132': (375, 'latin', None),
    'thesaurisons:jac-13': (20, 'latin', None), 'thesaurisons:jac-108': (305, 'latin', None),
    'thesaurisons:jac-215': (72, 'latin', None), 'thesaurisons:jac-491': (637, 'latin', None),
    'thesaurisons:sainte-face-therese': (208, 'italien', None),
}
# absentes de l'Enchiridion 1952 : indulgence abrogée
# Seul le chapelet de saint Michel est absent de l'Enchiridion. (« Tout pour vous, Cœur sacré », « Ô bon Jésus, cachez-moi
# dans vos plaies » et « le Cœur affligé de Marie » avaient été déclarés abrogés à tort : ce sont les n° 234, 199 et 383 ;
# voir verif1952.py.)
ABROGEES = {
    'jardin:chapelet-de-saint-michel-archange': 'chapelet de saint Michel (Pie IX, 8 août 1851)',
}
THES = 'Thésaurisons pour le ciel (1941), traduction certifiée fidèle selon le can. 934 § 2'

for k, (n, langue, cond) in NUMEROS.items():
    f = F[k]
    ancien = f['ref']
    if not ancien.startswith('Ench. 1952'):  # déjà appliqué : rejouable sans doubler la référence
        f['ref'] = f'Ench. 1952, n° {n} (auparavant : {ancien})'
    f['langue'] = langue
    if cond: f['intention'] = cond
    if langue != 'français': f['traduction'] = THES
for k, quoi in ABROGEES.items():
    F.pop(k, None)
    d['sans_compte'][k] = f'Indulgence abrogée : {quoi} ne figure pas dans l’Enchiridion indulgentiarum de 1952 (décret du 3 mars 1952 : « obrogatis ceteris omnibus generalibus indulgentiarum concessionibus, quae in hoc enchiridion non sint relatae »).'
# les dons du Saint-Esprit (une douleur seule du n° 383) : voir verif1952.py

# numéros corrigés après vérification sur le texte de l'Enchiridion (audit du corpus, 19 nov.)
F['jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph']['ref'] = 'Ench. 1952, n° 470 (vérifié sur le texte de l’Enchiridion ; le livret indiquait n° 410)'

d['regle'] = ('Seules comptent les œuvres de l’Enchiridion indulgentiarum de 1952 : le décret de la S. Pénitencerie du 3 mars 1952 '
              'abroge toutes les concessions générales qui n’y sont pas reprises, et celles qui y sont reprises avec changement suivent '
              'la forme nouvelle (Praenotanda 2). Indulgences partielles seulement. Une prière indulgenciée en latin ou en italien ne '
              'garde son indulgence en français que si la traduction est approuvée (can. 934 § 2 ; Praenotanda 3) : traductions '
              'certifiées de Thésaurisons pour le ciel (Montréal, 1941). « remplace » : valeur qui remplace la valeur ordinaire aux jours indiqués.')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
print(len(F), 'fiches ;', len(d['sans_compte']), 'sans compte')
