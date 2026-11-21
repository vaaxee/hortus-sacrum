"""Traductions certifiées de Thésaurisons (1941) reportées dans le livret (demande du 21 nov. 2026).

Thésaurisons pour le ciel (Carmel de Montréal, 1941 ; numérotation des Preces et Pia Opera de 1938), traduction
certifiée fidèle selon le can. 934 § 2 (G. Chartier, vic. gén. de Montréal, 28 avril 1941). Chaque texte a été relu sur
l'image du scan (liberius.net, PDF) et comparé à la formule de l'Enchiridion de 1952 :
- n° 82 (p. 41) : « Doux Cœur de mon Jésus, faites que je vous aime de plus en plus » = Ench. n° 224, « Dolce Cuor del
  mio Gesù, fa' che io ti ami sempre più ». Le livret portait « Doux Cœur de Jésus, faites que je vous aime toujours de
  plus en plus ». Lieux : Triple Couronne d'or (livret) et les trois pages composées hortus:triple-couronne-1 à 3.
  (L'invocation de l'offrande de Ramière, « Cœur aimable de mon Jésus… », est une autre formule, citée par Ramière :
  non touchée.)
- n° 150 (p. 55-57) : Douleurs et allégresses de saint Joseph = Ench. n° 470 (sept prières, chacune suivie de Pater,
  Ave, Gloria ; antienne, verset, oraison). Thésaurisons garde les gloses de Beringer (« ami intime », « qu'il reçut
  alors », « celui qui était votre vie ») : c'est la traduction certifiée par l'Ordinaire, retenue telle quelle.
- n° 498 (p. 168) : prière pour les agonisants = Ench. n° 671 (O clementissime Iesu… ; ℣. Cor Iesu in agonia factum).

Les pièces du livret (data/prieres/jardin.json) prennent `revision` : l'app remplace le texte en base, sauf s'il a été
modifié par l'utilisateur (seed.ts, reviserLivret). Les pages composées (sources.json) aussi.
Ordre : composer.py, ench1952.py, verif1952.py, beringer1925.py, puis ce script (idempotent).
Usage : python3 -I engine/indulgences/thesaurisons_livret.py
"""
import json, pathlib

RACINE = pathlib.Path(__file__).resolve().parents[2]
PI = RACINE / 'data/prieres/indulgences.json'
PS = RACINE / 'data/prieres/sources.json'
PJ = RACINE / 'data/prieres/jardin.json'
THES = 'Thésaurisons pour le ciel (1941), traduction certifiée fidèle selon le can. 934 § 2'
TH_SOURCE = 'Thésaurisons pour le ciel (Carmel de Montréal, 1941), traduction certifiée fidèle selon le can. 934 § 2'
REVISION = 1  # révision de ce report ; à augmenter si le texte change encore

DOUX_AVANT = 'Doux Cœur de Jésus, faites que je vous aime toujours de plus en plus.'
DOUX = 'Doux Cœur de mon Jésus, faites que je vous aime de plus en plus.'  # n° 82, p. 41

JOSEPH = [  # n° 150, p. 55-57
    'Ô très chaste époux de Marie, glorieux saint Joseph, quelles ne furent pas l’affliction et l’angoisse de votre cœur, '
    'dans la perplexité où vous étiez de savoir s’il fallait abandonner votre épouse sans tache ! Mais aussi quelle ne '
    'fut pas votre allégresse, quand l’ange vous révéla le grand mystère de l’Incarnation ! Nous vous prions, par cette '
    'douleur et par cette allégresse, de consoler notre cœur à présent et dans nos dernières douleurs, par la joie d’une '
    'bonne vie et d’une sainte mort, semblable à la vôtre, entre Jésus et Marie. Pater, Ave et Gloria Patri.',
    'Ô bienheureux patriarche, glorieux saint Joseph, choisi pour être le père putatif du Verbe fait homme, la douleur '
    'que vous avez ressentie en voyant naître l’Enfant Jésus dans une si grande pauvreté, se changea subitement en une '
    'joie céleste, devant l’harmonie des concerts angéliques et la contemplation des merveilles de cette nuit '
    'resplendissante. Nous vous supplions, par cette douleur et par cette allégresse, de nous obtenir, après cette vie, '
    'd’aller entendre les louanges angéliques et jouir des splendeurs de la gloire céleste. Pater, Ave et Gloria Patri.',
    'Ô très obéissant observateur des lois divines, glorieux saint Joseph, le Sang précieux que le Rédempteur enfant '
    'versa dans la circoncision, vous transperça le cœur ; mais le nom de Jésus qu’il reçut alors vous rendit la vie, en '
    'vous comblant de joie. Obtenez-nous, par cette douleur et par cette allégresse, de vivre éloignés de tout péché, '
    'afin d’expirer joyeux avec le très saint Nom de Jésus dans le cœur et sur les lèvres. Pater, Ave et Gloria Patri.',
    'Ô Saint très fidèle, le confident des mystères de notre rédemption, glorieux saint Joseph, si la prophétie de '
    'Siméon, concernant les souffrances que devaient endurer Jésus et Marie, vous occasionna une douleur mortelle, elle '
    'vous combla aussi de joie, en annonçant en même temps le salut et la glorieuse résurrection qui devaient en résulter '
    'pour un grand nombre d’âmes. Obtenez-nous, par cette douleur et par cette allégresse, d’être du nombre de ceux qui, '
    'en considération des mérites de Jésus et de l’intercession de la bienheureuse Vierge Marie, doivent ressusciter '
    'glorieusement. Pater, Ave et Gloria.',
    'Ô gardien très vigilant, ami intime du Fils de Dieu incarné, glorieux saint Joseph, combien n’avez-vous pas souffert '
    'pour nourrir et servir le Fils du Très-Haut, particulièrement dans votre fuite en Égypte ! mais aussi quelle ne fut '
    'point votre joie d’avoir toujours ce Dieu avec vous et de voir renversées les idoles d’Égypte ! Par cette douleur et '
    'par cette allégresse, obtenez-nous d’éloigner à jamais de nous le tyran des enfers, surtout par la fuite des '
    'occasions dangereuses, et de renverser dans notre cœur toute idole des affections terrestres, afin qu’entièrement '
    'occupés à servir Jésus et Marie, nous vivions uniquement pour eux et mourions dans la joie de leur amour. Pater, Ave '
    'et Gloria Patri.',
    'Ô Ange de la terre, glorieux saint Joseph, qui avez pu admirer, soumis à vos moindres volontés, le Roi du ciel ; si '
    'la joie de le ramener d’Égypte fut troublée par la crainte d’Archélaüs, bientôt, rassuré par l’Ange, vous fûtes '
    'heureux de demeurer à Nazareth avec Jésus et Marie. Obtenez-nous, par cette douleur et par cette allégresse, '
    'd’écarter de notre cœur toute crainte nuisible, de posséder la paix de la conscience, de vivre contents avec Jésus et '
    'Marie et de mourir aussi avec eux. Pater, Ave et Gloria Patri.',
    'Ô modèle de toute sainteté, glorieux saint Joseph, ayant perdu sans votre faute l’Enfant Jésus, vous l’avez cherché '
    'pendant trois jours, plongé dans une douleur profonde, jusqu’au moment où, plein de joie, vous avez retrouvé dans le '
    'temple, au milieu des docteurs, celui qui était votre vie. Par cette douleur et par cette allégresse, nous vous '
    'supplions, de cœur et de bouche, d’intercéder en notre faveur, afin qu’il ne nous arrive plus de perdre Jésus par '
    'quelque faute grave. Si nous avions cet immense malheur, faites que nous le cherchions avec une douleur qui ne nous '
    'laisse pas de repos jusqu’à ce que nous le retrouvions favorable, surtout à notre mort, afin d’aller le posséder au '
    'ciel et d’y chanter éternellement avec vous ses divines miséricordes. Pater, Ave et Gloria Patri.',
]
JOSEPH_ANTIENNE = 'Jésus avait environ trente ans, et passait pour être fils de Joseph.'
JOSEPH_VERSET = ('Priez pour nous, saint Joseph.', 'Afin que nous devenions dignes des promesses de Jésus-Christ.')
JOSEPH_ORAISON = ('Ô Dieu, qui, par une providence admirable, avez daigné choisir le bienheureux Joseph pour être l’époux '
                  'de votre très sainte Mère, faites, nous vous en supplions, que, le vénérant sur la terre comme notre '
                  'protecteur, nous méritions de l’avoir pour intercesseur dans les cieux. Vous qui vivez et régnez dans '
                  'les siècles des siècles. Ainsi soit-il.')
AGONISANTS = ('Ô très miséricordieux Jésus, vous qui brûlez d’amour pour les âmes, je vous en supplie, par l’agonie de '
              'votre Cœur très saint et par les douleurs de votre Mère immaculée, purifiez dans votre Sang les pécheurs du '
              'monde entier qui sont en ce moment à l’agonie et qui doivent mourir aujourd’hui. Ainsi soit-il.')  # n° 498
AGONISANTS_INV = 'Cœur agonisant de Jésus, ayez pitié des mourants.'

# ---------------------------------------------------------------------------------------------------------------
# 1. Livret
# ---------------------------------------------------------------------------------------------------------------
jardin = json.loads(PJ.read_text())
J = {p['id']: p for p in jardin['pieces']}


def mention(p, texte):
    if texte not in (p.get('source') or ''):
        p['source'] = ((p.get('source') or '') + ' ; ' + texte).strip(' ;')
    p['revision'] = max(p.get('revision', 0), REVISION)


p = J['la-triple-couronne-d-or-du-sacre-c-ur-de-jesus']
for b in p['blocs']:
    if b.get('texte') == DOUX_AVANT: b['texte'] = DOUX
assert sum(b.get('texte') == DOUX for b in p['blocs']) == 1
mention(p, f'« {DOUX[:-1]} » : {TH_SOURCE}, n° 82, p. 41')

p = J['les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph']
num = [b for b in p['blocs'] if b['type'] == 'numero']
assert [b['numero'] for b in num] == ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
for b, t in zip(num, JOSEPH): b['texte'] = t
types = [b['type'] for b in p['blocs']]
assert types[-5:] == ['rubrique', 'texte', 'verset', 'rubrique', 'texte'], types
p['blocs'][-4]['texte'] = JOSEPH_ANTIENNE
p['blocs'][-3]['v'], p['blocs'][-3]['r'] = JOSEPH_VERSET
p['blocs'][-1]['texte'] = JOSEPH_ORAISON
mention(p, f'texte français : {TH_SOURCE}, n° 150, p. 55-57')

p = J['priere-pour-les-agonisants']
types = [b['type'] for b in p['blocs']]
assert types in (['rubrique', 'texte', 'verset', 'traduction'], ['rubrique', 'texte', 'texte', 'traduction']), types
p['blocs'][1]['texte'] = AGONISANTS
p['blocs'][2] = {'type': 'texte', 'texte': AGONISANTS_INV}  # Thésaurisons l'imprime d'une ligne, sans ℣. ni ℟.
mention(p, f'texte français : {TH_SOURCE}, n° 498, p. 168')
PJ.write_text(json.dumps(jardin, ensure_ascii=False, indent=1) + '\n')

# ---------------------------------------------------------------------------------------------------------------
# 2. Pages composées de la Triple Couronne (composer.py les tire du livret)
# ---------------------------------------------------------------------------------------------------------------
src = json.loads(PS.read_text())
P = {q['id']: q for q in src['pieces']}
for n in (1, 2, 3):
    # lot 6 : les pages composées ne sont plus livrées (le programme les compose à l'affichage, depuis le livret)
    if f'hortus:triple-couronne-{n}' not in P:
        continue
    q = P[f'hortus:triple-couronne-{n}']
    q['corps'] = q['corps'].replace(f'[{DOUX_AVANT}]', f'[{DOUX}]')
    assert f'[{DOUX}]' in q['corps'] and DOUX_AVANT not in q['corps']
    q['revision'] = max(q.get('revision', 0), REVISION)
PS.write_text(json.dumps(src, ensure_ascii=False, indent=1) + '\n')

# ---------------------------------------------------------------------------------------------------------------
# 3. Fiches
# ---------------------------------------------------------------------------------------------------------------
d = json.loads(PI.read_text())
F = d['fiches']
for k in [x for x in ['jardin:la-triple-couronne-d-or-du-sacre-c-ur-de-jesus', 'hortus:triple-couronne-1',
          'hortus:triple-couronne-2', 'hortus:triple-couronne-3'] if x in F]:
    F[k]['traduction'] = (f'{THES}, pour « Jésus, doux et humble de cœur, rendez mon cœur semblable au vôtre » (n° 85), '
                          f'« {DOUX[:-1]} » (n° 82), « Doux Cœur de Marie, soyez mon salut » (n° 134) et « Mon Jésus, '
                          'miséricorde » (n° 33)')
    F[k]['note'] = (
        'Dulce Cor Jesu et Dulce Cor Mariæ sont concédés en italien (n° 224 et 386) : leur forme latine n’est pas une '
        'traduction approuvée ; le français de la page est celui de Thésaurisons (n° 82 et 134). « Aimé soit partout le '
        'Sacré-Cœur de Jésus » est concédé en français (n° 223). Le ℟. latin du livret « fac cor meum sicut Cor tuum » '
        's’écarte du texte de l’Enchiridion (« fac cor nostrum secundum Cor tuum ») ; sa traduction française entre '
        'crochets est celle de Thésaurisons.')
F['jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph']['traduction'] = f'{THES} (n° 150)'
F['jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph']['note'] = (
    'Texte français de Thésaurisons (n° 150), qui suit Beringer et en garde les gloses (« ami intime », « qu’il reçut '
    'alors », « celui qui était votre vie ») : traduction certifiée par l’Ordinaire, retenue telle quelle.')
F['jardin:priere-pour-les-agonisants']['traduction'] = f'{THES} (n° 498)'
F['jardin:priere-pour-les-agonisants'].pop('note', None)
PI.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
print('livret : 3 pièces ; pages composées : 3 ; fiches : 6')
