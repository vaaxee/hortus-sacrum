"""Vérification, fiche par fiche, des indulgences contre le texte de l'Enchiridion indulgentiarum de 1952 (20 nov. 2026).

À lancer après ench1952.py : python3 -I engine/indulgences/verif1952.py (idempotent).

Chaque fiche de data/prieres/indulgences.json a été relue sur le texte de l'Enchiridion (Typis Polyglottis Vaticanis,
1952) : numéro, valeur partielle, fréquence, conditions, répétitions, valeurs saisonnières. Ce script consigne les
corrections et ajoute à chaque fiche la langue de la concession (`langue`) et, s'il y a lieu, la traduction approuvée
(`traduction`, can. 934 § 2 ; Praenotanda 3).

Les concessions faites pour « des prières quelconques » ou pour un acte « quelle qu'en soit la formule » (neuvaines,
mois, actes des vertus théologales, communion spirituelle) ne posent pas de question de traduction : `langue` y vaut
« français » et une note le dit.

Traductions : Thésaurisons pour le ciel (Carmel de Montréal, 1941 ; numérotation des Preces et Pia Opera de 1938),
certifié selon le can. 934 § 2 par G. Chartier, vic. gén. de Montréal, le 28 avril 1941. Les textes français remplacés
dans data/prieres/sources.json sont recopiés de Thésaurisons et relus sur le scan ; le champ `revision` de la pièce est
incrémenté pour que l'app remplace le texte (sauf s'il a été modifié par l'utilisateur).
"""
import json, pathlib

RACINE = pathlib.Path(__file__).resolve().parents[2]
PI = RACINE / 'data/prieres/indulgences.json'
PS = RACINE / 'data/prieres/sources.json'
d = json.loads(PI.read_text())
F = d['fiches']

THES = 'Thésaurisons pour le ciel (1941), traduction certifiée fidèle selon le can. 934 § 2'
LIBRE = ('Concession pour des prières quelconques (ou pour l’acte, quelle qu’en soit la formule) : '
         'la langue est indifférente.')


def thes(*n):
    return f"{THES} (n° {' et '.join(map(str, n))})"


def maj(id_, **champs):
    f = F[id_]
    for k, v in champs.items():
        if v is None:
            f.pop(k, None)
        else:
            f[k] = v


def libre(id_):
    f = F[id_]
    f['langue'] = 'français'
    f.pop('traduction', None)
    if LIBRE not in f.get('note', ''):
        f['note'] = (f.get('note', '') + ' ' + LIBRE).strip()


# ---------------------------------------------------------------------------------------------------------------
# 1. Corrections des fiches
# ---------------------------------------------------------------------------------------------------------------
ANGELUS = 'le matin, à midi et le soir (ou dès qu’on le peut ensuite)'
maj('paroissien:angelus', intention=ANGELUS,
    note='Au temps pascal, le Regina cæli avec son oraison ; à défaut de savoir ces prières, cinq Ave Maria (n° 331).')
maj('beringer:regina-caeli', intention=ANGELUS)
maj('paroissien:de-profundis',
    note='Le Pater et l’Ave avec le ℣. Requiem æternam, dits en suffrage pour les défunts, ont la même indulgence (n° 585).')

maj('beringer:litanies-sacre-coeur', ref='Ench. 1952, n° 245',
    partielles=[{'ans': 7, 'texte': '7 ans (avec le ℣. et l’oraison)'}])
maj('paroissien:litanies-saint-nom', partielles=[{'ans': 7, 'texte': '7 ans (avec les oraisons)'}])

# « Virginum custos et pater » est le n° 473 (le n° 478 est « Glorieux saint Joseph, modèle des travailleurs »)
maj('beringer:saint-joseph-purete', ref='Ench. 1952, n° 473 (Virginum custos et pater, sancte Joseph)')

# Triple Couronne d'or : le n° 221 est « Domine Iesu Christe, qui de caelis » ; « Iesu, mitis et humilis corde » est le
# n° 227. L'invocation « Dulce Cor Jesu, fac ut te magis ac magis diligam », dite sur chaque grain des dizaines, est
# indulgenciée seule (n° 224, en italien) ; le n° 248 (avec Pater, Ave et Gloria devant une image) est une autre œuvre.
# « Amatum sit ubique Sacratissimum Cor Jesu » : n° 223, concédé en français.
COURONNE = dict(
    ref='Ench. 1952, n° 287 (Veni, Sancte Spiritus), 223 (Aimé soit partout), 227 (Iesu, mitis), 224 (Dolce Cuor '
        'del mio Gesù), 386 (Dolce Cuore di Maria) et 70 (Gesù mio, misericordia)',
    partielles=[
        {'ans': 5, 'texte': '5 ans (Veni, Sancte Spiritus, avec le ℣. Emitte et l’oraison)'},
        {'jours': 300, 'repetitions': 5, 'texte': '5 × 300 jours (Aimé soit partout le Sacré-Cœur de Jésus)'},
        {'jours': 500, 'repetitions': 5, 'texte': '5 × 500 jours (Jesu, mitis et humilis Corde, à chaque mystère)'},
        {'jours': 300, 'repetitions': 50, 'texte': '50 × 300 jours (Dulce Cor Jesu, sur chaque grain des dizaines)'},
        {'jours': 300, 'repetitions': 5, 'texte': '5 × 300 jours (Dulce Cor Mariæ, à chaque mystère)'},
        {'jours': 300, 'repetitions': 5, 'texte': '5 × 300 jours (Mon Jésus, miséricorde !, cinq fois)'},
    ],
    langue='latin',
    traduction=f'{THES}, pour « Jésus, doux et humble de cœur, rendez mon cœur semblable au vôtre » (n° 85), '
               '« Doux Cœur de Marie, soyez mon salut » (n° 134) et « Mon Jésus, miséricorde » (n° 33)',
    note='Dulce Cor Jesu et Dulce Cor Mariæ sont concédés en italien (n° 224 et 386) : leur forme latine n’est pas une '
         'traduction approuvée. Dire l’italien ou le français de Thésaurisons : « Doux Cœur de mon Jésus, faites que je '
         'vous aime de plus en plus » (n° 82 ; le livret porte « faites que je vous aime toujours de plus en plus ») et '
         '« Doux Cœur de Marie, soyez mon salut » (n° 134). « Aimé soit partout le Sacré-Cœur de Jésus » est concédé en '
         'français (n° 223). Le ℟. latin du livret « fac cor meum sicut Cor tuum » s’écarte du texte de l’Enchiridion '
         '(« fac cor nostrum secundum Cor tuum ») ; sa traduction française entre crochets est celle de Thésaurisons.')
for k in ['jardin:la-triple-couronne-d-or-du-sacre-c-ur-de-jesus']:  # lot 6 : plus de pages hortus:* composées
    maj(k, **COURONNE)

maj('jardin:acte-d-intention-de-communion-spirituelle-perpetuelle',
    ref='Ench. 1952, n° 164 (acte de communion spirituelle, quelle qu’en soit la formule)')
libre('jardin:acte-d-intention-de-communion-spirituelle-perpetuelle')

# Vendredi devant le crucifix : n° 196 (sept Pater, Ave, Gloria, le vendredi) et n° 201 (En ego, 10 ans)
maj('jardin:chaque-vendredi-devant-le-crucifix',
    ref='Ench. 1952, n° 196 (sept Pater, Ave et Gloria le vendredi) et n° 201 (En ego, o bone et dulcissime Iesu)',
    intention='devant une image de Jésus crucifié',
    partielles=[
        {'ans': 7, 'texte': '7 ans le vendredi (sept Pater, Ave et Gloria)', 'quand': {'jours_semaine': [5]}},
        {'ans': 10, 'texte': '10 ans (En ego, devant une image de Jésus crucifié)'},
    ],
    langue='latin',
    note='La traduction française d’En ego donnée par le livret n’est pas celle, approuvée, de Thésaurisons (n° 2 : '
         '« Me voici, ô bon et très doux Jésus, prosterné en votre présence… »).')

maj('jardin:a-saint-gabriel-archange', ref='Ench. 1952, n° 449 (Deus, qui inter ceteros Angelos)',
    note='Neuvaine de prières quelconques à saint Gabriel : 5 ans une fois le jour (n° 448), non comptée ici.')
maj('jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph',
    ref='Ench. 1952, n° 470 (O Sposo purissimo di Maria ; le livret indiquait n° 410)')
maj('jardin:veni-creator-spiritus', ref='Ench. 1952, n° 283',
    partielles=[{'ans': 5, 'texte': '5 ans, avec le ℣. Emitte et l’oraison'}])
maj('jardin:ave-maris-stella', ref='Ench. 1952, n° 321')
maj('jardin:magnificat', ref='Ench. 1952, n° 320')
maj('jardin:te-joseph-celebrent', ref='Ench. 1952, n° 463')
maj('jardin:auguste-reine-des-cieux', ref='Ench. 1952, n° 345')

for k in ['paroissien:acte-de-foi', 'paroissien:acte-d-esperance', 'paroissien:acte-de-charite']:
    libre(k)
maj('paroissien:priere-du-matin', langue='latin',
    note='Le Credo et le Confiteor y sont en latin, langue de la concession ; les actes des vertus théologales valent '
         'quelle qu’en soit la formule d’un catéchisme approuvé (n° 36).')
maj('paroissien:priere-du-soir', langue='latin',
    note='Le Credo et le Confiteor y sont en français : aucune traduction approuvée n’a été trouvée pour ces textes ; '
         'pour l’indulgence, les dire en latin (comme dans la prière du matin).')

CHAPELET = ('10 ans, une fois le jour, si on le récite avec d’autres, en public ou en privé (n° 395 b) : non compté ici. '
            'L’indulgence est attachée à la récitation du Rosaire (Pater, Ave, Gloria, en méditant les mystères) ; '
            'les prières ajoutées (clausules, oraisons de Montfort) ne sont pas indulgenciées pour elles-mêmes.')
for k in ['sambucy:chapelet-saint-dominique', 'hortus:chapelet-joyeux', 'hortus:chapelet-douloureux',
          'hortus:chapelet-glorieux']:
    maj(k, langue='latin', note=CHAPELET)

maj('weber:priere-saint-louis-de-gonzague', note=None)
maj('weber:priere-tres-saint-coeur-de-marie', note='Weber citait l’ancienne concession de Pie VII (60 jours).')
maj('weber:petit-chapelet-immaculee-conception',
    ref='Ench. 1952, n° 357 (O Maria concepita senza peccato), n° 636 (Jésus, Marie, Joseph, je vous donne mon cœur) '
        'et n° 339 (Souvenez-vous)',
    partielles=[
        {'jours': 300, 'repetitions': 12, 'texte': '12 × 300 jours (Ô Marie conçue sans péché…)'},
        {'ans': 7, 'texte': '7 ans (Jésus, Marie, Joseph, je vous donne mon cœur…)'},
        {'ans': 3, 'texte': '3 ans (Souvenez-vous)'},
    ],
    langue='italien', traduction=thes(129, 490, 123),
    note='Les mots de l’invocation sont ceux de Thésaurisons (n° 129). Le Souvenez-vous à dire est celui de '
         'Thésaurisons (n° 123), repris dans la pièce « Souvenez-vous ».')

# langue et traduction des autres fiches
LANGUES = {
    'beringer:salve-regina': ('latin', thes(192, 106)), 'beringer:sub-tuum': ('latin', thes(193, 106)),
    'paroissien:angelus': ('latin', None), 'beringer:regina-caeli': ('latin', None),
    'paroissien:de-profundis': ('latin', None), 'beringer:litanies-sacre-coeur': ('latin', None),
    'beringer:litanies-saint-joseph': ('latin', None), 'paroissien:litanies-sainte-vierge': ('latin', None),
    'paroissien:litanies-saint-nom': ('latin', None), 'paroissien:litanies-des-saints': ('latin', None),
    'beringer:saint-joseph-purete': ('latin', thes(151)), 'jardin:priere-pour-les-agonisants': ('latin', None),
    'jardin:a-saint-gabriel-archange': ('latin', None), 'jardin:les-sept-douleurs-de-marie': ('italien', None),
    'jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph': ('italien', None),
    'jardin:veni-creator-spiritus': ('latin', None), 'jardin:ave-maris-stella': ('latin', None),
    'jardin:magnificat': ('latin', None), 'jardin:te-joseph-celebrent': ('latin', None),
    'jardin:auguste-reine-des-cieux': ('français', None), 'montfort:petite-couronne': ('latin', None),
    'weber:alma-redemptoris': ('latin', None), 'weber:ave-regina-caelorum': ('latin', None),
    'weber:souvenez-vous': ('latin', thes(123)), 'weber:stabat-mater': ('latin', None),
    'weber:priere-saint-louis-de-gonzague': ('latin', thes(125)), 'weber:priere-du-p-zucchi': ('latin', thes(124)),
    'weber:demande-d-une-bonne-mort': ('latin', thes(492)),
    'weber:priere-tres-saint-coeur-de-marie': ('italien', thes(137)),
    'weber:priere-notre-dame-du-bon-conseil': ('italien', thes(298)),
    'weber:trois-prieres-perpetuel-secours': ('italien', None), 'paroissien:te-deum': ('latin', None),
    'thesaurisons:action-de-graces': ('latin', thes(500)), 'jahenny:scapulaire-benediction-protection': ('latin', thes(70)),
}
for k, (langue, trad) in LANGUES.items():
    maj(k, langue=langue, traduction=trad)
for k in ['weber:priere-notre-dame-sept-douleurs', 'weber:priere-saint-bonaventure-mere-des-douleurs', 'weber:o-quot-undis',
          'weber:neuvaine-immaculee-conception', 'liguori:neuvaine-sacre-coeur', 'neuvaines-1886:nativite',
          'neuvaines-1886:assomption', 'liguori:neuvaine-de-noel']:
    libre(k)
maj('jardin:priere-pour-les-agonisants',
    note='Le livret suit de près la traduction de Thésaurisons (n° 498), sans la reproduire mot pour mot '
         '(« dans ce moment », « sang »).')
maj('weber:trois-prieres-perpetuel-secours',
    note='Trois prières, chacune suivie de trois Ave Maria dans l’Enchiridion (Weber en met cinq). Thésaurisons ne '
         'donne pas leur traduction. Weber indiquait l’ancienne concession de Pie IX.')

# Abrogations prononcées à tort par ench1952.py : ces œuvres figurent dans l'Enchiridion de 1952.
ABROGEE = 'Indulgence abrogée'
RETABLIES = {
    'thesaurisons:jac-244': dict(
        ref='Ench. 1952, n° 234 (Tutto per voi, Cuore sacratissimo di Gesù ; Thésaurisons, n° 244 ; Preces 1938, n° 203)',
        frequence='chaque fois', partielles=[{'jours': 300, 'texte': '300 jours'}], langue='italien',
        traduction=thes(244)),
    'thesaurisons:jac-232': dict(
        ref='Ench. 1952, n° 199 (O bone Iesu, intra tua vulnera absconde me ; Thésaurisons, n° 232 ; Preces 1938, n° 169)',
        frequence='chaque fois', partielles=[{'jours': 300, 'texte': '300 jours'}], langue='latin',
        traduction=thes(232)),
    # « En l'honneur du Cœur affligé de Marie » (Pie VII, 14 janv. 1815) est l'exercice « Vi compatisco, Addolorata
    # Maria » du n° 383, repris en 1952.
    'beringer:coeur-afflige-de-marie': dict(
        ref='Ench. 1952, n° 383 (Vi compatisco, Addolorata Maria ; Pie VII, 14 janv. 1815)', frequence='chaque fois',
        partielles=[{'ans': 5, 'texte': '5 ans'},
                    {'ans': 7, 'texte': '7 ans chaque jour de septembre', 'quand': {'mois': [9]}, 'remplace': 0}],
        langue='italien',
        note='L’indulgence est attachée à l’exercice entier (℣. Deus, in adiutorium, Gloria, les sept douleurs suivies '
             'chacune d’un Ave, ℣. Ora pro nobis et l’oraison). La traduction de Beringer n’est pas une traduction '
             'approuvée ; Thésaurisons ne donne pas cet exercice.'),
}
for k, fiche in RETABLIES.items():
    if k not in F:
        F[k] = fiche
    else:
        F[k].update(fiche)
    d['sans_compte'].pop(k, None)
PARTIE = ('Une des sept douleurs de l’exercice « Vi compatisco, Addolorata Maria » (Ench. 1952, n° 383 ; Pie VII, '
          '14 janv. 1815) : l’indulgence (5 ans ; 7 ans en septembre) est attachée à l’exercice entier, non à une '
          'douleur seule. Non comptée.')
for k in [x for x in d['sans_compte'] if x.startswith('beringer:don-')]:
    d['sans_compte'][k] = PARTIE
d['sans_compte']['thesaurisons:au-christ-roi'] = (
    'Indulgence plénière une fois le jour, seulement (Ench. 1952, n° 272, concédé en français) : les plénières ne sont '
    'pas comptées.')
assert all(ABROGEE not in v for k, v in d['sans_compte'].items() if k in RETABLIES)

# toutes les fiches ont une langue
sans = [k for k, f in F.items() if 'langue' not in f]
assert not sans, sans
PI.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')

# ---------------------------------------------------------------------------------------------------------------
# 2. Textes français remplacés par ceux de Thésaurisons (relus sur le scan)
# ---------------------------------------------------------------------------------------------------------------
TH_OUVRAGE = ('Thésaurisons pour le ciel. Recueil reproduisant la plupart des prières et œuvres indulgenciées des '
              '« Preces et Pia Opera » (1938)')
TH_EDITION = 'Carmel de Montréal, 1941 ; préface du R. P. Louis C. de Léry, S. J.'
TH_URL = 'http://www.liberius.net/livres/Thesaurisons_pour_le_Ciel_000001335.pdf'

SALVE = ('Salut, ô Reine, mère de miséricorde, notre vie, notre douceur et notre espérance, salut. Nous élevons nos '
         'cris vers vous, pauvres exilés, malheureux enfants d’Eve ; nous soupirons vers vous, gémissant et pleurant '
         'dans cette vallée de larmes. Ah ! nous vous en supplions, ô notre avocate, tournez vers nous vos regards '
         'compatissants et au sortir de cet exil, montrez-nous Jésus, le fruit béni de vos entrailles. Ô clémente, ô '
         'charitable, ô douce Vierge Marie !')
SUB = ('Nous nous réfugions sous votre protection, sainte Mère de Dieu : ne méprisez pas les prières que nous vous '
       'adressons dans nos besoins ; mais délivrez-nous toujours de tous les périls, Vierge comblée de gloire et de '
       'bénédiction.')
DIGNARE = '℣. Rendez-moi digne de vous louer, Vierge sainte ;\n℟. donnez-moi la force contre vos ennemis.'

# (id, [(ancien, nouveau)] ou texte entier, mention de source)
REMPLACEMENTS = [
    ('beringer:salve-regina', [
        ('Salut, ô notre Reine, mère de miséricorde, notre vie, notre douceur et notre espérance, salut. Nous élevons '
         'nos cris vers vous, pauvres exilés, malheureux enfants d’Eve ; nous soupirons vers vous, gémissants et '
         'pleurants dans cette vallée de larmes. Allons donc, ô notre avocate, tournez vers nous vos yeux '
         'compatissants, et, après cet exil, montrez-nous Jésus, le fruit béni de votre sein, ô clémente, ô '
         'miséricordieuse, ô douce Vierge Marie.', SALVE),
        ('℣. Daignez agréer mes louanges, ô Vierge sainte.\n℟. Donnez-moi force et courage contre vos ennemis.',
         DIGNARE)],
     'traduction française du Salve Regina et du ℣. Dignare me : Thésaurisons pour le ciel (Montréal, 1941), n° 192 '
     '(p. 82-83) et n° 106 (p. 45), traduction certifiée fidèle selon le can. 934 § 2'),
    ('beringer:sub-tuum', [
        ('Nous nous réfugions sous votre protection, sainte Mère de Dieu ; ne méprisez pas les prières que nous vous '
         'adressons dans nos besoins ; mais délivrez-nous toujours de tous les périls, Vierge comblée de gloire et de '
         'bénédiction.', SUB),
        ('℣. Daignez agréer mes louanges, ô Vierge sainte.\n℟. Donnez-moi force et courage contre vos ennemis.',
         DIGNARE)],
     'traduction française du Sub tuum et du ℣. Dignare me : Thésaurisons pour le ciel (Montréal, 1941), n° 193 '
     '(p. 83) et n° 106 (p. 45), traduction certifiée fidèle selon le can. 934 § 2'),
    ('weber:ave-regina-caelorum', [('__DIGNARE_WEBER__', DIGNARE)],
     'traduction du ℣. Dignare me : Thésaurisons pour le ciel (Montréal, 1941), n° 106 (p. 45), traduction certifiée '
     'fidèle selon le can. 934 § 2'),
    ('beringer:saint-joseph-purete',
     'Ô glorieux saint Joseph, père et protecteur des vierges, gardien fidèle, à qui Dieu confia Jésus, l’innocence '
     'même, et Marie, la Vierge des vierges, je vous en supplie et je vous en conjure par Jésus et Marie, ce double '
     'dépôt qui vous fut si cher, faites que, préservé de toute souillure, pur d’esprit et de cœur, et chaste de corps, '
     'je serve constamment Jésus et Marie dans une chasteté parfaite. Ainsi soit-il.',
     ('n° 151 (Preces 1938, n° 435), p. 58 ; latin : Beringer 1925, t. I, n° 480, p. 252 ; texte français '
      'antérieur : Beringer')),
    ('weber:souvenez-vous',
     'Souvenez-vous, ô très douce Vierge Marie, qu’on n’a jamais entendu dire qu’aucun de ceux qui ont eu recours à '
     'votre protection, imploré votre assistance et réclamé vos suffrages, ait été abandonné. Animé d’une pareille '
     'confiance, ô Vierge des vierges, ô ma Mère, je cours vers vous, je viens à vous, et gémissant sous le poids de '
     'mes fautes, je me prosterne à vos pieds. Veuillez, ô Mère du Verbe, ne point mépriser mes prières, mais '
     'écoutez-les favorablement et daignez les exaucer. Ainsi soit-il.',
     'n° 123 (Preces 1938, n° 309), p. 48 ; latin : Enchiridion indulgentiarum, 1952, n° 339 ; texte français '
     'antérieur : Weber, p. 467'),
    ('weber:priere-du-p-zucchi',
     'Ave Maria, etc.\n\nÔ ma Souveraine, ô ma Mère ! je m’offre à vous tout entier, et pour vous donner une preuve de '
     'mon dévouement, je vous consacre aujourd’hui mes yeux, mes oreilles, ma bouche, mon cœur, tout moi-même. '
     'Puisque je vous appartiens, ô bonne Mère, gardez-moi, défendez-moi, comme votre bien et votre propriété.',
     'n° 124 (Preces 1938, n° 310), p. 49 ; indulgence : Enchiridion indulgentiarum, 1952, n° 340 ; texte français '
     'antérieur : Weber, p. 474-475'),
    ('weber:priere-saint-louis-de-gonzague',
     'Ô ma Souveraine, sainte Marie, je viens me jeter dans le sein de votre miséricorde et mettre dès ce moment et '
     'pour toujours, et pour l’heure de mon trépas, mon âme et mon corps sous votre sauvegarde et sous votre spéciale '
     'protection. Je vous confie et je remets entre vos mains toutes mes espérances et mes consolations, et le terme '
     'de ma vie, afin que par votre très sainte intercession et par vos mérites, toutes mes œuvres soient réglées et '
     'déterminées selon votre volonté et celle de votre divin Fils. Ainsi soit-il.',
     'n° 125 (Preces 1938, n° 313), p. 49 ; indulgence : Enchiridion indulgentiarum, 1952, n° 343 (O Domina mea, '
     'sancta Maria) ; texte français antérieur : Weber, p. 473'),
    ('weber:priere-tres-saint-coeur-de-marie',
     'Ô Cœur de Marie, Mère de Dieu et notre Mère, Cœur le plus aimable, objet des complaisances de l’adorable '
     'Trinité, digne de toute la vénération et de l’amour des anges et des hommes ; Cœur le plus ressemblant à celui '
     'de Jésus, dont vous êtes la plus parfaite image ; Cœur plein de bonté et de compassion pour nos misères, '
     'daignez fondre la glace de nos propres cœurs, et faites qu’ils se donnent entièrement à celui du divin Sauveur. '
     'Répandez en eux l’amour de vos vertus, et enflammez-les du feu dont vous brûlez constamment vous-même. Couvrez '
     'de votre protection la sainte Église, et soyez toujours son refuge et son invincible défense contre toutes les '
     'attaques de ses ennemis. Soyez notre voie pour aller à Jésus, et le canal qui nous transmette toutes les grâces '
     'nécessaires à notre salut. Soyez notre secours dans nos besoins, notre soulagement dans les afflictions, notre '
     'force dans les tentations, notre refuge dans les persécutions. Soyez notre secours dans tous les périls, mais '
     'surtout dans les derniers combats de notre vie, à l’heure de la mort lorsque, pour ravir nos âmes, tout l’enfer '
     'se déchaînera contre nous, en ce moment formidable, à cet instant terrible, d’où dépend notre éternelle '
     'destinée. Ah ! faites-nous alors, Vierge compatissante, ressentir la tendresse de votre Cœur maternel et la '
     'force de votre puissance sur le Cœur de Jésus, en nous ouvrant, dans la source même de la miséricorde, un '
     'refuge assuré d’où nous puissions aller le bénir avec vous en paradis pendant tous les siècles des siècles. '
     'Ainsi soit-il.',
     'n° 137 (Preces 1938, n° 358), p. 52 ; indulgence : Enchiridion indulgentiarum, 1952, n° 393 ; texte français '
     'antérieur (abrégé) : Weber, p. 405-406'),
    ('weber:priere-notre-dame-du-bon-conseil',
     'Ô très glorieuse Vierge, choisie par le Conseil éternel pour être la Mère du Verbe éternel fait chair, la '
     'trésorière des grâces divines et l’avocate des pécheurs, moi, le plus indigne de vos serviteurs, j’ai recours à '
     'vous, afin que vous daigniez être mon guide et mon conseil dans cette vallée de larmes. Obtenez-moi, par le très '
     'précieux Sang de votre Fils, le pardon de mes péchés, le salut de mon âme et les moyens nécessaires pour y '
     'parvenir. Obtenez à la sainte Église le triomphe sur ses ennemis et la propagation du règne de Jésus-Christ par '
     'toute la terre. Ainsi soit-il.',
     'n° 298 (Preces 1938, n° 394), p. 105 ; indulgence : Enchiridion indulgentiarum, 1952, n° 429 ; texte français '
     'antérieur : Weber, p. 455'),
    ('weber:demande-d-une-bonne-mort',
     'Ô Marie conçue sans péché, priez pour nous qui avons recours à vous. Refuge des pécheurs, Mère des agonisants, '
     'veuillez ne pas nous abandonner à l’heure de notre mort ; mais obtenez-nous une douleur parfaite, une sincère '
     'contrition, la rémission de nos péchés, la grâce de recevoir dignement le saint Viatique, et de puiser la force '
     'dans le sacrement de l’Extrême-Onction, afin que nous puissions être présentés en toute assurance, devant le '
     'trône du Juge équitable, mais plein de miséricorde, notre Dieu et notre Rédempteur. Ainsi soit-il.',
     'n° 492 (Preces 1938, n° 595), p. 167 (l’édition imprime « le grâce » et « topte assurance » : coquilles '
     'corrigées) ; indulgence : Enchiridion indulgentiarum, 1952, n° 642 ; texte français antérieur : Weber, p. 477'),
]

src = json.loads(PS.read_text())
P = {p['id']: p for p in src['pieces']}
for id_, quoi, mention in REMPLACEMENTS:
    p = P[id_]
    avant = p['corps']
    if isinstance(quoi, str):
        nouveau = quoi
    else:
        nouveau = avant
        for ancien, neuf in quoi:
            if ancien == '__DIGNARE_WEBER__':
                lignes = nouveau.split('\n')
                i = next((n for n, l in enumerate(lignes) if l.startswith('℣. Agréez, Vierge sainte')), None)
                if i is not None:
                    lignes[i:i + 2] = DIGNARE.split('\n')
                nouveau = '\n'.join(lignes)
            elif ancien in nouveau:
                nouveau = nouveau.replace(ancien, neuf)
            else:
                assert neuf in nouveau, (id_, ancien[:40])
    if nouveau != avant:
        p['corps'] = nouveau
        p['revision'] = p.get('revision', 0) + 1
    s = p['source']
    if isinstance(quoi, str):
        if s.get('ouvrage') != TH_OUVRAGE:
            p['source'] = {'ouvrage': TH_OUVRAGE, 'edition': TH_EDITION, 'page': mention, 'url': TH_URL}
    elif mention not in s.get('page', ''):
        s['page'] = (s.get('page', '') + ' ; ' + mention).strip(' ;')
PS.write_text(json.dumps(src, ensure_ascii=False, indent=1) + '\n')
print(len(F), 'fiches vérifiées ;', len(REMPLACEMENTS), 'textes rapportés à Thésaurisons')
