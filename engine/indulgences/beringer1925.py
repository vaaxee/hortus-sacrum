"""Traductions de Beringer 1925 tenues pour approuvées (décision de l'utilisateur, 20 nov. 2026).

Beringer, *Les Indulgences, leur nature et leur usage*, trad. Ph. Mazoyer, 4e éd. française, Paris, Lethielleux, 1925,
t. I (archive.org `lesindulgences0001beri`) : décret de la S. Pénitencerie du 11 juillet 1925 (t. I, p. v-vi), qui
reconnaît la fidélité de la traduction. Selon la décision, ce français vaut traduction approuvée (can. 934 § 2 ;
Ench. 1952, Praenotanda 3) **seulement quand il répond mot pour mot à la formule de l'Enchiridion de 1952** ; les hymnes
en vers (Veni Creator, Ave maris stella, Stabat) en sont exclues.

Chaque texte ci-dessous a été lu sur l'image du scan (archive.org, PDF), l'OCR relu, puis comparé, phrase par phrase,
à la formule latine ou italienne de l'Enchiridion de 1952 (édition vaticane). Pièce par pièce :
- appliqués : Angélus et Regina cæli (n° 428, p. 221-223 ; Ench. n° 331), De profundis (n° 614, p. 322 ; Ench.
  n° 585), Magnificat (n° 437, p. 228-229 ; Ench. n° 320), En ego (n° 384, p. 202 ; Ench. n° 201), « En l'honneur du
  Cœur affligé de Marie » (n° 450, p. 237-238 ; Ench. n° 383 : c'est lui, et non les n° 447 ou 887, qui répond à
  « Vi compatisco, Addolorata Maria »), trois prières à N.-D. du Perpétuel Secours (n° 459, p. 243-244 ; Ench. n° 427,
  avec les trois Ave que l'Enchiridion fait dire après chacune et que Beringer ne marque pas) ;
- non appliqués (le français ne répond pas mot pour mot à la formule de 1952) : litanies de Lorette (n° 439,
  p. 229-232 : sans « Regina in caelum assumpta », ajoutée en 1950), « Doux Cœur de Jésus » (n° 333, p. 170 : « de
  Jésus » pour « del mio Gesù »), Douleurs et allégresses de saint Joseph (n° 485, p. 255-257 : ajouts « ami intime »,
  « celui qui était votre vie », « qu'il reçut alors »), litanies du saint Nom (n° 305, p. 154-157 : « pardonnez-nous
  nos péchés », « exaucez nos prières », oraison paraphrasée). Détail dans A_FOURNIR.md.
- Pater, Ave, Gloria usuels : fidélité « notoire » (L'Ami du clergé, 9 avril 1931, p. 252-253) ; le chapelet compte.

Les textes remplacés dans data/prieres/sources.json prennent une `revision` de plus : l'app remplace le texte en base,
sauf s'il a été modifié par l'utilisateur (seed.ts, reviser). Les pièces du livret (jardin.json) donnent déjà, mot pour
mot, le français de Beringer : elles ne sont pas touchées ; le script le vérifie.

Ordre : composer.py, ench1952.py, verif1952.py, puis ce script (verif1952.py remet `traduction` à zéro pour ces fiches).
Usage : python3 -I engine/indulgences/beringer1925.py   (idempotent)
"""
import json, pathlib, re, unicodedata

RACINE = pathlib.Path(__file__).resolve().parents[2]
PI = RACINE / 'data/prieres/indulgences.json'
PS = RACINE / 'data/prieres/sources.json'
PJ = RACINE / 'data/prieres/jardin.json'

BERINGER = 'Beringer, Les Indulgences (1925), traduction reconnue fidèle par la S. Pénitencerie (décret du 11 juillet 1925)'
USUELS = 'Pater, Ave, Gloria usuels : fidélité notoire (L’Ami du clergé, 9 avril 1931, p. 252-253)'
B_OUVRAGE = 'Beringer, Les Indulgences, leur nature et leur usage, t. I'
B_EDITION = 'trad. Ph. Mazoyer, 4e éd. française, Paris, P. Lethielleux, 1925'
B_URL = 'https://archive.org/details/lesindulgences0001beri'

# ---------------------------------------------------------------------------------------------------------------
# Textes de Beringer 1925, recopiés sur l'image du scan
# ---------------------------------------------------------------------------------------------------------------
# n° 428, p. 221-222. L'édition imprime une première fois « Je vous salue, Marie etc... » : virgule et point rétablis
# comme aux deux autres versets.
ANGELUS = '\n\n'.join([
    '℣. L’ange du Seigneur annonça à Marie,\n℟. Et elle conçut par l’opération du Saint-Esprit.\nJe vous salue, Marie, etc.',
    '℣. Voici la servante du Seigneur.\n℟. Qu’il me soit fait selon votre parole.\nJe vous salue, Marie, etc.',
    '℣. Et le Verbe s’est fait chair.\n℟. Et il a habité parmi nous.\nJe vous salue, Marie, etc.',
    '℣. Priez pour nous, sainte Mère de Dieu,\n℟. Afin que nous devenions dignes des promesses de Jésus-Christ.',
    'Prions. Seigneur, nous vous supplions de répandre votre grâce dans nos âmes, afin qu’ayant connu, par la voix de '
    'l’Ange, l’incarnation de votre Fils Jésus-Christ, nous arrivions, par sa passion et par sa croix, à la gloire de sa '
    'résurrection. Par le même Jésus-Christ Notre-Seigneur. Ainsi soit-il.',
    '*Au temps pascal, au lieu de l’Angelus, on récite debout le Regina cœli.*',
])
ANGELUS_LA = '\n\n'.join([
    '℣. Angelus Domini nuntiavit Mariæ.\n℟. Et concepit de Spiritu Sancto.\nAve, Maria, etc.',
    '℣. Ecce ancilla Domini.\n℟. Fiat mihi secundum verbum tuum.\nAve Maria, etc.',
    '℣. Et Verbum caro factum est.\n℟. Et habitavit in nobis.\nAve Maria, etc.',
    '℣. Ora pro nobis, sancta Dei Genitrix.\n℟. Ut digni efficiamur promissionibus Christi.',
    'Oremus. Gratiam tuam, quæsumus, Domine, mentibus nostris infunde ; ut qui Angelo nuntiante Christi Filii tui '
    'incarnationem cognovimus, per passionem ejus et crucem ad resurrectionis gloriam perducamur. Per eumdem Christum '
    'Dominum nostrum. Amen.',
])
# n° 428, p. 222-223 (déjà dans la pièce beringer:regina-caeli : vérifié)
REGINA = ('Reine du ciel, réjouissez-vous, alleluia : Parce que celui que vous avez mérité de porter dans votre sein, '
          'alleluia : Est ressuscité comme il l’avait dit, alleluia. Priez Dieu pour nous, alleluia. ℣. Soyez dans la '
          'joie et l’allégresse, ô Vierge Marie, alleluia ; ℟. Parce que le Seigneur est vraiment ressuscité, alleluia. '
          'Prions. O Dieu qui avez daigné réjouir le monde par la résurrection de Notre-Seigneur Jésus-Christ, votre '
          'Fils ; faites, nous vous en prions, que, par le secours de sa Mère la Vierge Marie, nous obtenions les joies '
          'de la vie éternelle. Par ce même Jésus-Christ Notre-Seigneur. Ainsi soit-il.')
# n° 614, p. 322 : le psaume seul (Ench. 1952, n° 585, ne concède que le psaume)
DE_PROFUNDIS = [
    'Des profondeurs de l’abîme j’ai crié vers vous, Seigneur : Seigneur, écoutez ma voix.',
    'Que vos oreilles soient attentives à la voix de ma prière !',
    'Si vous tenez compte de nos iniquités, Seigneur, Seigneur, qui pourra subsister devant vous ?',
    'Mais vous êtes plein de miséricorde ; et j’espère en vous, Seigneur, à cause de votre loi.',
    'Mon âme s’est appuyée sur votre parole ; mon âme a mis toute sa confiance dans le Seigneur.',
    'Depuis le matin jusqu’au soir, Israël espère dans le Seigneur.',
    'Car dans le Seigneur est la miséricorde, et une abondante rédemption.',
    'C’est lui qui rachètera Israël de toutes ses iniquités.',
]
# n° 437, p. 228-229
MAGNIFICAT = ('Mon âme glorifie le Seigneur. Et mon esprit tressaille de joie en Dieu mon Sauveur. Il a regardé la bassesse '
              'de sa servante : désormais toutes les nations m’appelleront bienheureuse, Car le Tout-Puissant a fait en moi '
              'de grandes choses, et son nom est saint. Sa miséricorde se répand de génération en génération sur ceux qui '
              'le craignent. Il a déployé la force de son bras, et il a dispersé les superbes qui s’élevaient dans les '
              'pensées de leur cœur. Il a déposé les puissants de leur trône, et il a exalté les humbles. Il a comblé de '
              'biens les affamés, et renvoyé vides ceux qui vivaient dans l’opulence. Se souvenant de sa miséricorde, il a '
              'accueilli Israël son serviteur. Comme il l’avait promis à nos pères, à Abraham et à sa postérité pour tous '
              'les siècles.')
# n° 384, p. 202
EN_EGO = ('O bon et très doux Jésus, je me prosterne à genoux en votre présence. Je vous prie et vous conjure avec toute '
          'la ferveur de mon âme de daigner graver dans mon cœur de vifs sentiments de foi, d’espérance et de charité, un '
          'vrai repentir de mes fautes et un ferme propos de ne plus vous offenser ; tandis qu’avec un grand amour et une '
          'grande douleur je considère et contemple en esprit vos cinq plaies, ayant devant les yeux ces paroles que le '
          'prophète David vous appliquait déjà en les mettant dans votre bouche, ô bon Jésus : « Ils ont percé mes mains '
          'et mes pieds, ils ont compté tous mes os ».')
# n° 450, p. 237-238 (Ench. 1952, n° 383)
AFFLIGE = [
    'Je m’afflige avec vous, ô Marie, Mère de douleurs, pour la peine que ressentit votre tendre Cœur, à la prophétie du '
    'saint vieillard Siméon. Mère chérie, par votre Cœur si affligé, obtenez-moi la vertu d’humilité et le don salutaire '
    'de la crainte de Dieu.',
    'Je m’afflige avec vous, ô Marie, Mère de douleurs, pour les angoisses que votre Cœur très sensible ressentit dans '
    'votre fuite et votre séjour en Egypte. Mère chérie, par votre Cœur rempli de tristesse, obtenez-moi la vertu de '
    'libéralité, particulièrement envers les pauvres, et le don de piété.',
    'Je m’afflige avec vous, ô Marie, Mère de douleurs, pour la tristesse et l’inquiétude que votre Cœur a éprouvées à la '
    'perte de votre bien-aimé Jésus. Mère chérie, par votre Cœur si vivement agité, obtenez-moi la vertu de chasteté et '
    'le don de la science.',
    'Je m’afflige avec vous, ô Marie, Mère de douleurs, pour la consternation qui frappa votre Cœur maternel dans la '
    'rencontre de Jésus portant sa croix. Mère chérie, par votre Cœur si cruellement éprouvé, obtenez-moi la vertu de '
    'patience et le don de force.',
    'Je m’afflige avec vous, ô Marie, Mère de douleurs, pour le martyre que souffrit votre Cœur généreux en assistant à '
    'l’agonie de Jésus. Mère chérie, par votre Cœur ainsi martyrisé, obtenez-moi la vertu de tempérance et le don de '
    'conseil.',
    'Je m’afflige avec vous, ô Marie, Mère de douleurs, pour la blessure que fit à votre Cœur compatissant la lance qui '
    'ouvrit le côté de Jésus et blessa son très aimable Cœur. Mère chérie, par votre Cœur ainsi transpercé, obtenez-moi '
    'la vertu de charité fraternelle et le don d’intelligence.',
    'Je m’afflige avec vous, ô Marie, Mère de douleurs, pour les souffrances excessives qu’endura votre Cœur très aimant, '
    'lors de la sépulture de Jésus. Mère chérie, par votre Cœur sacré, abreuvé d’amertumes, obtenez-moi la vertu de '
    'diligence et le don de sagesse.',
]
AFFLIGE_DEBUT = '℣. O Dieu, venez à mon aide. ℟. Hâtez-vous, Seigneur, de me secourir.'
AFFLIGE_FIN = ['℣. Priez pour nous, Vierge très affligée. ℟. Afin que nous devenions dignes des promesses de Jésus-Christ.',
               'Nous vous en supplions, ô Seigneur Jésus-Christ, que la bienheureuse Vierge Marie, votre Mère, dont '
               'l’âme très sainte a été percée d’un glaive de douleur pendant votre passion, intercède pour nous auprès de '
               'votre clémence, maintenant et à l’heure de notre mort. Par vous, Jésus-Christ, Sauveur du monde, qui vivez '
               'et régnez avec le Père et le Saint-Esprit']
# n° 459, p. 243-244. L'édition imprime « Voici à vos pieds; ô Mère » : coquille (point-virgule pour virgule) corrigée.
SECOURS = [
    'Voici à vos pieds, ô Mère du Perpétuel Secours, un misérable pécheur qui a recours à vous et qui met en vous sa '
    'confiance. O Mère de miséricorde, ayez pitié de moi ! Je vous entends appeler par tous le refuge et l’espérance des '
    'pécheurs ; soyez donc mon refuge et mon espérance. Pour l’amour de Jésus-Christ, secourez-moi ; tendez les mains à '
    'un malheureux qui est tombé, mais qui se recommande à vous et qui se consacre pour toujours à votre service. Je '
    'bénis et je remercie Dieu de ce que, dans sa miséricorde, il m’a donné cette confiance en vous que je considère '
    'comme le gage de mon salut éternel. Lorsque, par le passé, j’ai eu le malheur de faire tant de chutes, c’est que je '
    'n’ai pas eu recours à vous. Je sais qu’avec votre secours je serai vainqueur ; je sais que vous viendrez à mon aide '
    'si je me recommande à vous ; mais, dans les occasions de péché, je crains de cesser d’invoquer votre assistance et '
    'ainsi de me perdre. Aussi la grâce que je vous conjure, autant qu’il est en moi, de me donner, c’est qu’au milieu '
    'des assauts de l’enfer je sache toujours recourir à vous et vous dire : « Marie, aidez-moi : Mère du Perpétuel '
    'Secours, ne permettez pas que je perde mon Dieu ! »',
    'O Mère du Perpétuel Secours, accordez-moi de pouvoir invoquer sans cesse votre nom tout-puissant, car votre nom est '
    'notre secours durant la vie et notre salut au moment de la mort. O Marie très pure, Marie très douce, faites que '
    'votre nom soit désormais comme la respiration de ma vie. Ne tardez pas, ô ma souveraine, de venir à mon aide toutes '
    'les fois que je vous appellerai. Dans toutes les tentations qui viendront m’assaillir, dans tous les besoins où je '
    'pourrai me trouver, je ne veux jamais cesser de vous invoquer, en répétant à chaque instant : Marie ! Marie ! Quel '
    'encouragement, quelle douceur, quelle confiance, quelle tendresse ne réveille pas dans mon âme votre seul nom, '
    'votre seule pensée ! Je remercie le Seigneur de ce qu’il vous a donné pour mon bien un nom si doux, si aimable, si '
    'puissant, je ne me contente pas de le prononcer ; je veux le prononcer avec amour, je veux que cet amour m’excite à '
    'vous appeler sans cesse : Mère du Perpétuel Secours.',
    'O Mère du Perpétuel Secours, vous êtes la dispensatrice de toutes les grâces que Dieu nous accorde, à nous '
    'infortunés pécheurs ; et, s’il vous a faite aussi puissante, aussi riche et aussi bienveillante, c’est afin que vous '
    'nous secouriez dans nos misères. Vous êtes l’avocate des coupables les plus malheureux et les plus abandonnés qui '
    'recourent à vous : secourez-moi donc moi-même, qui me recommande à vous. Je remets entre vos mains mon salut '
    'éternel ; je vous confie mon âme. Admettez-moi au nombre de vos serviteurs les plus dévoués ; prenez-moi sous votre '
    'protection, et cela me suffit. Car si vous m’accordez votre secours, je ne crains rien : ni mes péchés, parce que '
    'vous m’en obtenez le pardon ; ni les démons, parce que vous êtes plus puissante que l’enfer ; ni même Jésus, mon '
    'juge, parce qu’à votre seule prière il s’apaisera. Je ne crains qu’une chose : c’est que, par négligence, je ne cesse '
    'de me recommander à vous, et ainsi que je ne vienne à me perdre. Obtenez-moi, ô ma Souveraine, le pardon de mes '
    'péchés, l’amour de Jésus, la persévérance finale et la grâce de recourir toujours à vous, ô Mère du Perpétuel '
    'Secours !',
]
TROIS_AVE = 'Trois *Ave Maria*.'


def mots(t):
    """Suite des mots, sans balisage, ponctuation, accents ni majuscules : pour comparer deux textes mot pour mot."""
    t = re.sub(r'\[/?r\]|##[^\n]*|[*℣℟]', ' ', t)
    t = unicodedata.normalize('NFD', t.replace('’', "'").replace('œ', 'oe').replace('Œ', 'oe'))
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower()
    return re.findall(r"[a-z]+", t)


def contient(texte, extrait):
    """L'extrait figure-t-il mot pour mot (aux accents et à la ponctuation près) dans le texte ?"""
    return ' '.join(mots(extrait)) in ' '.join(mots(texte))


src = json.loads(PS.read_text())
P = {p['id']: p for p in src['pieces']}
J = {f"jardin:{p['id']}": p for p in json.loads(PJ.read_text())['pieces']}


def jardin_fr(id_):
    """Français de la pièce du livret (strophes et blocs), comme le voit l'app."""
    out = []
    for b in J[id_]['blocs']:
        if b['type'] == 'strophe': out.append(b.get('fr') or '')
        elif b['type'] == 'verset': out.append(f"{b['v']} {b['r']}")
        elif b['type'] not in ('rubrique', 'notice', 'intertitre'): out.append(b.get('texte') or '')
    return '\n'.join(out)


def remplacer(id_, corps, source=None, latin=None):
    p = P[id_]
    change = p['corps'] != corps or (latin is not None and p.get('latin') != latin)
    p['corps'] = corps
    if latin is not None: p['latin'] = latin
    if source: p['source'] = source
    if change: p['revision'] = p.get('revision', 0) + 1


# ---------------------------------------------------------------------------------------------------------------
# 1. Textes : vérifier ceux qui donnent déjà Beringer, remplacer les autres
# ---------------------------------------------------------------------------------------------------------------
# déjà Beringer, mot pour mot
assert contient(P['beringer:regina-caeli']['corps'], REGINA)
assert contient(jardin_fr('jardin:magnificat'), MAGNIFICAT)
assert contient(jardin_fr('jardin:chaque-vendredi-devant-le-crucifix'), EN_EGO)
for t in [AFFLIGE_DEBUT, *AFFLIGE, *AFFLIGE_FIN]:
    assert contient(P['beringer:coeur-afflige-de-marie']['corps'], t), t[:50]
    assert contient(jardin_fr('jardin:les-sept-douleurs-de-marie'), t), t[:50]

# Angélus : texte du Paroissien (Mame, 1890) remplacé par celui de Beringer
ANCIEN = 'texte français et latin antérieurs : Paroissien romain, Tours, Mame, 1890, p. 16-17'
remplacer('paroissien:angelus', ANGELUS, latin=ANGELUS_LA, source={
    'ouvrage': f'{B_OUVRAGE}, n° 428', 'edition': B_EDITION,
    'page': f'221-222 ; indulgence : Enchiridion indulgentiarum, 1952, n° 331 ; {ANCIEN}', 'url': B_URL})

# De profundis : les huit versets du psaume (seuls indulgenciés) ; les versets et l'oraison du Paroissien restent
p = P['paroissien:de-profundis']
tete, reste = p['corps'].split('## Psaume 129\n\n', 1)
blocs = reste.split('\n\n')
i = next(n for n, b in enumerate(blocs) if b.startswith('℣.'))
remplacer('paroissien:de-profundis', tete + '## Psaume 129\n\n' + '\n\n'.join(DE_PROFUNDIS + blocs[i:]))
MENTION = f'psaume : {B_OUVRAGE}, n° 614, p. 322 ({B_EDITION}), traduction reconnue fidèle (décret du 11 juillet 1925)'
if MENTION not in p['source']['page']:
    p['source']['page'] += ' ; ' + MENTION

# Perpétuel Secours : texte de Weber remplacé par celui de Beringer ; les trois Ave après chaque prière (Ench. n° 427)
corps = '\n\n'.join(f'[r]{n}.[/r] {t}\n\n{TROIS_AVE}' for n, t in enumerate(SECOURS, 1))
remplacer('weber:trois-prieres-perpetuel-secours', corps, source={
    'ouvrage': f'{B_OUVRAGE}, n° 459', 'edition': B_EDITION,
    'page': '243-244 (l’édition imprime « Voici à vos pieds; ô Mère » : coquille corrigée) ; les trois Ave après '
            'chaque prière sont ceux de l’Enchiridion indulgentiarum, 1952, n° 427 (« Tre Ave, Maria ») ; texte '
            'français antérieur : Weber, Notre Mère, 3e éd., 1899, p. 457-462 (avec cinq Ave, un verset et une oraison)',
    'url': B_URL})
P['weber:trois-prieres-perpetuel-secours']['usage'] = ('Trois prières, chacune suivie de trois Ave Maria (Enchiridion '
                                                       'de 1952, n° 427).')

# Cœur affligé : l'édition n'imprime pas « etc. » après le 5e Ave
p = P['beringer:coeur-afflige-de-marie']
remplacer('beringer:coeur-afflige-de-marie', p['corps'].replace(
    'conseil. — *Je vous salue, Marie*, etc.', 'conseil. — *Je vous salue, Marie*.'))

for t in [ANGELUS, *DE_PROFUNDIS, *SECOURS]:
    assert any(contient(P[k]['corps'], t) for k in
               ['paroissien:angelus', 'paroissien:de-profundis', 'weber:trois-prieres-perpetuel-secours'])
PS.write_text(json.dumps(src, ensure_ascii=False, indent=1) + '\n')

# ---------------------------------------------------------------------------------------------------------------
# 2. Fiches d'indulgence
# ---------------------------------------------------------------------------------------------------------------
d = json.loads(PI.read_text())
F = d['fiches']
TRADUCTIONS = {
    'paroissien:angelus': BERINGER,
    'beringer:regina-caeli': BERINGER,
    'paroissien:de-profundis': BERINGER,
    'jardin:magnificat': BERINGER,
    'jardin:chaque-vendredi-devant-le-crucifix': f'{BERINGER} ; {USUELS}',
    'beringer:coeur-afflige-de-marie': BERINGER,
    'jardin:les-sept-douleurs-de-marie': BERINGER,
    'weber:trois-prieres-perpetuel-secours': f'{BERINGER} ; {USUELS}',
    'sambucy:chapelet-saint-dominique': USUELS,
    'hortus:chapelet-joyeux': USUELS,
    'hortus:chapelet-douloureux': USUELS,
    'hortus:chapelet-glorieux': USUELS,
}
for k, t in TRADUCTIONS.items():
    assert F[k]['langue'] in ('latin', 'italien'), k
    F[k]['traduction'] = t
F['jardin:chaque-vendredi-devant-le-crucifix']['note'] = (
    'Le français d’En ego donné par le livret est, mot pour mot, celui de Beringer (1925, n° 384, p. 202), dont la '
    'traduction est reconnue fidèle par la S. Pénitencerie.')
F['beringer:coeur-afflige-de-marie']['note'] = (
    'L’indulgence est attachée à l’exercice entier (℣. Deus, in adiutorium, Gloria, les sept douleurs suivies chacune '
    'd’un Ave, ℣. Ora pro nobis et l’oraison).')
F['weber:trois-prieres-perpetuel-secours']['note'] = (
    'Trois prières, chacune suivie de trois Ave Maria (Enchiridion de 1952, n° 427). Beringer (1925, n° 459) donne les '
    'prières sans les Ave, selon l’ancienne concession de Pie IX (100 jours pour chacune).')
PI.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
print(len(TRADUCTIONS), 'fiches avec traduction ;', 'textes :',
      ', '.join(f"{k} (révision {P[k].get('revision', 0)})" for k in
                ['paroissien:angelus', 'paroissien:de-profundis', 'weber:trois-prieres-perpetuel-secours',
                 'beringer:coeur-afflige-de-marie']))
