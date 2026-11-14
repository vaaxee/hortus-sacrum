"""Construit data/roues.json : les roues symboliques (1, 3, 4, 5, 7, 8, 9, 10, 12, 15…).

Chaque roue est une liste ordonnée d'éléments ; l'élément du jour est (jours écoulés depuis le premier dimanche de l'Avent)
modulo le nombre d'éléments. Les versets latins sont tirés de la Vulgate clémentine (fichier scrollmapper/bible_databases,
VulgClementine.json) ; les listes, de l'Écriture, du Catéchisme de saint Pie X, du Concile de Trente et des pièces déjà
recopiées dans l'app (Jardin de l'âme, Paroissien de 1890).
Usage : python3 engine/roues/construire.py chemin/VulgClementine.json
"""
import json, re, sys
from pathlib import Path

V = {b['name']: b for b in json.load(open(sys.argv[1]))['books']}
LIVRES = {'Dt': 'Deuteronomy', '1 Co': 'I Corinthians', 'Mt': 'Matthew', 'Tb': 'Tobit', '1 Jn': 'I John', 'Sg': 'Wisdom',
          'Si': 'Sirach', 'Ez': 'Ezekiel', 'Ap': 'Revelation of John', 'Is': 'Isaiah', 'Ga': 'Galatians', 'Pr': 'Proverbs',
          'Ex': 'Exodus', 'Lc': 'Luke', 'Jn': 'John', 'Ps': 'Psalms', 'Mc': 'Mark', 'Za': 'Zechariah'}

def vg(ref):
    """« Mt 2, 11 » ou « Is 11, 2-3 » → texte de la Vulgate."""
    livre, reste = ref.rsplit(' ', 1)[0], ref.rsplit(' ', 1)[1]
    livre, ch = ref.split(', ')[0].rsplit(' ', 1)
    vs = ref.split(', ')[1]
    a, _, b = vs.partition('-')
    c = V[LIVRES[livre]]['chapters'][int(ch) - 1]['verses']
    return ' '.join(x['text'] for x in c if int(a) <= x['verse'] <= int(b or a)).strip()

VULGATE = {'ouvrage': 'Biblia Sacra Vulgatæ editionis (Clémentine)', 'edition': 'texte de la Vulgate clémentine', 'page': '', 'url': 'https://github.com/scrollmapper/bible_databases'}
PIE_X = {'ouvrage': 'Catéchisme de saint Pie X', 'edition': 'Compendio della dottrina cristiana, 1905 (trad.)', 'page': '', 'url': 'https://www.ewtn.com/catholicism/library/catechism-of-st-pius-x-1286'}
JARDIN = {'ouvrage': 'Le Jardin de l’âme', 'edition': 'livret', 'page': '', 'url': ''}
PAROISSIEN = {'ouvrage': 'Paroissien romain', 'edition': 'Tours, A. Mame et fils, 1890', 'page': '7-12', 'url': 'https://archive.org/details/paroissienromain00tour'}
BREVIAIRE = {'ouvrage': 'Breviarium Romanum', 'edition': 'S. Grégoire, Hom. 34 in Evang., 29 septembre, IIe nocturne', 'page': '', 'url': 'https://github.com/DivinumOfficium/divinum-officium'}
TRENTE = {'ouvrage': 'Concile de Trente', 'edition': 'Session VII, canon 1 sur les sacrements', 'page': '', 'url': ''}

def el(fr, la='', ref='', texte=''):
    e = {'fr': fr}
    if la: e['la'] = la
    if ref: e['ref'] = ref
    if texte: e['texte'] = texte
    return e

def verset(ref):
    return {'ref': ref, 'la': vg(ref)}

R = []
def roue(id, nombre, titre, elements, source, verset_=None, actif=False, anneau=None, unite='jour', liste=False):
    assert len(elements) == nombre, (id, len(elements))
    R.append({'id': id, 'nombre': nombre, 'titre': titre, 'elements': elements, 'source': source,
              **({'verset': verset(verset_)} if verset_ else {}), 'actif': actif, 'unite': unite,
              **({'anneau': anneau} if anneau else {}), **({'liste': True} if liste else {})})

# ---------------------------------------------------------------- 1
roue('un-dieu', 1, 'Un seul Dieu', [el('Un seul Dieu', 'Dominus unus est')], VULGATE, 'Dt 6, 4', actif=True, anneau=1)

# ---------------------------------------------------------------- 3
roue('vertus-theologales', 3, 'Les trois vertus théologales', [
    el('La foi', 'Fides', texte='paroissien:acte-de-foi'), el('L’espérance', 'Spes', texte='paroissien:acte-d-esperance'),
    el('La charité', 'Caritas', texte='paroissien:acte-de-charite')], VULGATE, '1 Co 13, 13', actif=True, anneau=3)
roue('trinite', 3, 'Les trois Personnes divines', [el('Le Père', 'Pater'), el('Le Fils', 'Verbum'), el('Le Saint-Esprit', 'Spiritus Sanctus')], VULGATE, '1 Jn 5, 7')
roue('presents-mages', 3, 'Les trois présents des Mages', [
    el('L’or', 'Aurum'), el('L’encens', 'Thus'), el('La myrrhe', 'Myrrha')], VULGATE, 'Mt 2, 11')
roue('oeuvres-satisfaction', 3, 'La prière, le jeûne et l’aumône', [el('La prière', 'Oratio'), el('Le jeûne', 'Jejunium'), el('L’aumône', 'Eleemosyna')], VULGATE, 'Tb 12, 8')
roue('concupiscences', 3, 'Les trois concupiscences à combattre', [
    el('La concupiscence de la chair', 'Concupiscentia carnis'), el('La concupiscence des yeux', 'Concupiscentia oculorum'),
    el('L’orgueil de la vie', 'Superbia vitæ')], VULGATE, '1 Jn 2, 16')

# ---------------------------------------------------------------- 4
roue('fins-dernieres', 4, 'Les quatre fins dernières', [el('La mort', 'Mors'), el('Le jugement', 'Judicium'), el('L’enfer', 'Infernus'), el('Le paradis', 'Paradisus')],
     VULGATE, 'Si 7, 40', actif=True, anneau=4)
roue('evangelistes', 4, 'Les quatre évangélistes', [
    el('Saint Matthieu, l’homme', 'Facies hominis'), el('Saint Marc, le lion', 'Facies leonis'),
    el('Saint Luc, le bœuf', 'Facies bovis'), el('Saint Jean, l’aigle', 'Facies aquilæ')], VULGATE, 'Ez 1, 10')
roue('vertus-cardinales', 4, 'Les quatre vertus cardinales', [
    el('La prudence', 'Prudentia'), el('La justice', 'Justitia'), el('La force', 'Virtus'), el('La tempérance', 'Sobrietas')], VULGATE, 'Sg 8, 7')

# ---------------------------------------------------------------- 5
roue('saintes-plaies', 5, 'Les cinq plaies de Notre-Seigneur', [
    el('La main droite'), el('La main gauche'), el('Le pied droit'), el('Le pied gauche'), el('Le côté', 'Latus ejus aperuit')],
    JARDIN, 'Jn 19, 34')
for e in R[-1]['elements']: e['texte'] = 'jardin:chapelet-des-saintes-plaies'

# ---------------------------------------------------------------- 7
roue('douleurs-marie', 7, 'Les sept douleurs de Notre-Dame', [
    el('La prophétie de Siméon'), el('La fuite en Égypte'), el('Jésus perdu au Temple'), el('La rencontre sur le chemin du Calvaire'),
    el('Le crucifiement'), el('Le coup de lance'), el('La sépulture')], JARDIN, actif=True, anneau=7)
for e in R[-1]['elements']: e['texte'] = 'jardin:les-sept-douleurs-de-marie'
DONS = [('La sagesse', 'Sapientia', 'sagesse'), ('L’intelligence', 'Intellectus', 'intelligence'), ('Le conseil', 'Consilium', 'conseil'),
        ('La force', 'Fortitudo', 'force'), ('La science', 'Scientia', 'science'), ('La piété', 'Pietas', 'piete'), ('La crainte de Dieu', 'Timor Domini', 'crainte')]
roue('dons-saint-esprit', 7, 'Les sept dons du Saint-Esprit', [el(f, l, texte=f'beringer:don-{c}') for f, l, c in DONS], VULGATE, 'Is 11, 2-3')
roue('sacrements', 7, 'Les sept sacrements', [el(x) for x in ['Le baptême', 'La confirmation', 'L’eucharistie', 'La pénitence', 'L’extrême-onction', 'L’ordre', 'Le mariage']],
     TRENTE, 'Pr 9, 1')
roue('vices-capitaux', 7, 'Les sept péchés capitaux et leurs vertus contraires', [
    el('L’orgueil, vaincu par l’humilité'), el('L’avarice, vaincue par la libéralité'), el('La luxure, vaincue par la chasteté'),
    el('La colère, vaincue par la patience'), el('La gourmandise, vaincue par l’abstinence'), el('L’envie, vaincue par la charité fraternelle'),
    el('La paresse, vaincue par la diligence et la ferveur au service de Dieu')], PIE_X)
roue('misericorde-corporelle', 7, 'Les sept œuvres de miséricorde corporelle', [el(x) for x in [
    'Donner à manger à ceux qui ont faim', 'Donner à boire à ceux qui ont soif', 'Vêtir ceux qui sont nus', 'Loger les pèlerins',
    'Visiter les malades', 'Visiter les prisonniers', 'Ensevelir les morts']], PIE_X)
roue('misericorde-spirituelle', 7, 'Les sept œuvres de miséricorde spirituelle', [el(x) for x in [
    'Conseiller ceux qui doutent', 'Enseigner les ignorants', 'Reprendre les pécheurs', 'Consoler les affligés',
    'Pardonner les offenses', 'Supporter patiemment les personnes importunes', 'Prier Dieu pour les vivants et pour les morts']], PIE_X)
roue('demandes-pater', 7, 'Les sept demandes du Pater', [
    el('Que votre nom soit sanctifié', 'Sanctificetur nomen tuum'), el('Que votre règne arrive', 'Adveniat regnum tuum'),
    el('Que votre volonté soit faite', 'Fiat voluntas tua'), el('Donnez-nous notre pain', 'Panem nostrum da nobis hodie'),
    el('Pardonnez-nous nos offenses', 'Dimitte nobis debita nostra'), el('Ne nous laissez pas succomber à la tentation', 'Ne nos inducas in tentationem'),
    el('Délivrez-nous du mal', 'Libera nos a malo')], VULGATE, 'Mt 6, 9-13')
PAROLES = [('Père, pardonnez-leur', 'Lc 23, 34'), ('Aujourd’hui vous serez avec moi en paradis', 'Lc 23, 43'), ('Femme, voilà votre fils', 'Jn 19, 26-27'),
           ('Mon Dieu, pourquoi m’avez-vous abandonné ?', 'Mt 27, 46'), ('J’ai soif', 'Jn 19, 28'), ('Tout est consommé', 'Jn 19, 30'),
           ('Mon Père, je remets mon esprit entre vos mains', 'Lc 23, 46')]
LIVRES.update({'Lc': 'Luke'})
roue('sept-paroles', 7, 'Les sept paroles du Christ en croix', [el(f, vg(r), r) for f, r in PAROLES], VULGATE)
roue('psaumes-penitence', 7, 'Les sept psaumes de la pénitence', [el(f'Psaume {n}', re.sub(r'^(Ipsi David intellectus\.|Canticum graduum\.|Psalmus David[^.]*\.)\s*', '', vg(f'Ps {n}, {v}')).split(':')[0], f'Ps {n}') for n, v in [(6, 2), (31, 1), (37, 2), (50, 3), (101, 2), (129, 1), (142, 1)]], VULGATE)
R[-1]['elements'][5]['texte'] = 'paroissien:de-profundis'
roue('douleurs-joseph', 7, 'Les sept douleurs et allégresses de saint Joseph', [el(f'{i}e douleur et allégresse' if i > 1 else '1re douleur et allégresse') for i in range(1, 8)], JARDIN)
for e in R[-1]['elements']: e['texte'] = 'jardin:les-sept-douleurs-et-les-sept-allegresses-de-saint-joseph'

# ---------------------------------------------------------------- 8, 9, 10
roue('beatitudes', 8, 'Les huit béatitudes', [el(x, l) for x, l in [
    ('Les pauvres d’esprit', 'Beati pauperes spiritu'), ('Les doux', 'Beati mites'), ('Ceux qui pleurent', 'Beati qui lugent'),
    ('Ceux qui ont faim et soif de la justice', 'Beati qui esuriunt et sitiunt justitiam'), ('Les miséricordieux', 'Beati misericordes'),
    ('Les cœurs purs', 'Beati mundo corde'), ('Les pacifiques', 'Beati pacifici'), ('Ceux qui souffrent persécution pour la justice', 'Beati qui persecutionem patiuntur propter justitiam')]],
     VULGATE, 'Mt 5, 3-10')
roue('choeurs-anges', 9, 'Les neuf chœurs des Anges', [el(f, l) for f, l in [
    ('Les Anges', 'Angeli'), ('Les Archanges', 'Archangeli'), ('Les Vertus', 'Virtutes'), ('Les Puissances', 'Potestates'), ('Les Principautés', 'Principatus'),
    ('Les Dominations', 'Dominationes'), ('Les Trônes', 'Throni'), ('Les Chérubins', 'Cherubim'), ('Les Séraphins', 'Seraphim')]], BREVIAIRE)
roue('commandements', 10, 'Les dix commandements de Dieu', [el(f, l) for f, l in [
    ('Un seul Dieu tu adoreras', 'Non habebis deos alienos coram me'), ('Le nom de Dieu tu ne prendras pas en vain', 'Non assumes nomen Domini Dei tui in vanum'),
    ('Le jour du Seigneur tu sanctifieras', 'Memento ut diem sabbati sanctifices'), ('Tes père et mère tu honoreras', 'Honora patrem tuum et matrem tuam'),
    ('Tu ne tueras point', 'Non occides'), ('Tu ne commettras point d’impureté', 'Non mœchaberis'), ('Tu ne voleras point', 'Non furtum facies'),
    ('Tu ne porteras point de faux témoignage', 'Non loqueris contra proximum tuum falsum testimonium'), ('Tu ne désireras point la femme de ton prochain', 'Non desiderabis uxorem ejus'),
    ('Tu ne désireras point le bien d’autrui', 'Non concupisces domum proximi tui')]], VULGATE)

# ---------------------------------------------------------------- 12
roue('articles-credo', 12, 'Les douze articles du Symbole', [el(f, l, texte='paroissien:priere-du-matin') for f, l in [
    ('Dieu le Père tout-puissant, créateur', 'Credo in Deum, Patrem omnipotentem, Creatorem cœli et terræ'),
    ('Jésus-Christ, son Fils unique', 'Et in Jesum Christum, Filium ejus unicum, Dominum nostrum'),
    ('Conçu du Saint-Esprit, né de la Vierge Marie', 'Qui conceptus est de Spiritu sancto, natus ex Maria Virgine'),
    ('Sa passion, sa mort et sa sépulture', 'Passus sub Pontio Pilato, crucifixus, mortuus, et sepultus'),
    ('Sa descente aux enfers et sa résurrection', 'Descendit ad inferos, tertia die resurrexit a mortuis'),
    ('Son ascension', 'Ascendit ad cœlos, sedet ad dexteram Dei Patris omnipotentis'),
    ('Son retour pour juger les vivants et les morts', 'Inde venturus est judicare vivos et mortuos'),
    ('Le Saint-Esprit', 'Credo in Spiritum sanctum'), ('La sainte Église catholique, la communion des saints', 'Sanctam Ecclesiam catholicam, sanctorum communionem'),
    ('La rémission des péchés', 'Remissionem peccatorum'), ('La résurrection de la chair', 'Carnis resurrectionem'), ('La vie éternelle', 'Vitam æternam')]],
     PAROISSIEN, actif=True, anneau=12)
FRUITS = [('La charité', 'Caritas'), ('La joie', 'Gaudium'), ('La paix', 'Pax'), ('La patience', 'Patientia'), ('La bénignité', 'Benignitas'), ('La bonté', 'Bonitas'),
          ('La longanimité', 'Longanimitas'), ('La mansuétude', 'Mansuetudo'), ('La foi', 'Fides'), ('La modestie', 'Modestia'), ('La continence', 'Continentia'), ('La chasteté', 'Castitas')]
roue('fruits-saint-esprit', 12, 'Les douze fruits du Saint-Esprit', [el(f, l) for f, l in FRUITS], VULGATE, 'Ga 5, 22-23')
APOTRES = [('Saint Pierre', 'Simon, qui dicitur Petrus'), ('Saint André', 'Andreas'), ('Saint Jacques le Majeur', 'Jacobus Zebedæi'), ('Saint Jean', 'Joannes'),
           ('Saint Philippe', 'Philippus'), ('Saint Barthélemy', 'Bartholomæus'), ('Saint Thomas', 'Thomas'), ('Saint Matthieu', 'Matthæus'),
           ('Saint Jacques le Mineur', 'Jacobus Alphæi'), ('Saint Jude Thaddée', 'Thaddæus'), ('Saint Simon', 'Simon Chananæus'), ('Saint Matthias', 'Matthias')]
roue('apotres', 12, 'Les douze apôtres', [el(f, l) for f, l in APOTRES], VULGATE, 'Ap 12, 1')

# ---------------------------------------------------------------- 15
MYST = ['L’Annonciation', 'La Visitation', 'La Nativité', 'La Présentation au Temple', 'Jésus retrouvé au Temple', 'L’Agonie au jardin des Oliviers',
        'La Flagellation', 'Le Couronnement d’épines', 'Le Portement de la croix', 'Le Crucifiement et la mort de Notre-Seigneur', 'La Résurrection',
        'L’Ascension', 'La Descente du Saint-Esprit', 'L’Assomption de la très sainte Vierge', 'Le Couronnement de la très sainte Vierge']
roue('mysteres-rosaire', 15, 'Les quinze mystères du Rosaire', [el(m, texte='jardin:quinze-samedis-du-rosaire') for m in MYST], JARDIN)

# trois chapelets du Rosaire (pour la ligne « Chapelet » ; mystères d'après le Jardin, méthode d'après Sambucy 1837)
GROUPES = [('Mystères joyeux', MYST[0:5]), ('Mystères douloureux', MYST[5:10]), ('Mystères glorieux', MYST[10:15])]
roue('chapelets-rosaire', 3, 'Les trois chapelets du Rosaire', [el(n, ' · '.join(m), texte='sambucy:chapelet-saint-dominique') for n, m in GROUPES],
     JARDIN, actif=True, liste=True)

# ---------------------------------------------------------------- lecture des Évangiles : un chapitre par jour
CH = []
for nom, livre in [('Saint Matthieu', 'Matthew'), ('Saint Marc', 'Mark'), ('Saint Luc', 'Luke'), ('Saint Jean', 'John')]:
    for c in range(1, len(V[livre]['chapters']) + 1):
        CH.append(el(f'{nom}, chapitre {c}', ref=f'{ {"Matthew":"Mt","Mark":"Mc","Luke":"Lc","John":"Jn"}[livre]} {c}'))
roue('lecture-evangiles', len(CH), 'Lecture des quatre Évangiles, un chapitre par jour', CH, VULGATE, actif=True)

dest = Path(__file__).resolve().parents[2] / 'data' / 'roues.json'
dest.write_text(json.dumps({'depart': 'Premier dimanche de l’Avent', 'roues': R}, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(R), 'roues', sorted({r['nombre'] for r in R}))
