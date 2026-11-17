"""Petit bréviaire du Sacré-Cœur de Jésus (Nancy, Le Chevallier, 13e éd., imprimatur 21 mars 1883) :
sept petits offices, un par jour de la semaine, extraits des œuvres de sainte Marguerite-Marie.
Usage : python3 -I extraire.py <pdf> → JSON sur la sortie standard : [{jour, titre, corps}].
Couche texte Google (mise en page conservée) : paragraphes repérés au retrait, titres courants, numéros de page et
signatures retirés, mots coupés recollés, ℣/℟ et intertitres (heures, Hymne, Antienne, Prions) balisés."""
import json, re, subprocess, sys

PDF = sys.argv[1]
DEBUT, FIN = 29, 131  # pages du PDF : de l'office du dimanche à l'exercice pendant la messe (exclu)
JOURS = ['DIMANCHE', 'LUNDI', 'MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI']
COURANT = re.compile(r"^(?:[\dIlO]{1,3}\s+)?OFFICE DU [A-Z]+\.?(?:\s+[\dIlO]{1,3})?$")
MARQUE = re.compile(r"^(V\.|v\.|R[.7]|\.\s|ANT\.|A [A-ZÉÊ]+\.?$|HYMNE|HYNNE|RECOMMANDATION|PRIONS|ORAISON|CANTIQUE|AVE MARIA)")


def page(p):
    """Lignes de la page ; '' avant chaque paragraphe (retrait) ; '@@X' pour le titre d'un office qui commence ici."""
    t = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), PDF, '-'], capture_output=True, text=True).stdout
    L = [l.rstrip() for l in t.split('\n') if l.strip()]
    if not L: return []
    base = min(len(l) - len(l.lstrip()) for l in L)
    out = []
    for i, l in enumerate(L):
        s = l.strip()
        m = re.fullmatch(r"OFFICE DU ([A-ZÈ]+)\.?", s)
        if m and m.group(1).replace('È', 'E') in JOURS:  # titre d'office : sans numéro de page (le titre courant en a un)
            out += ['', '@@' + m.group(1).replace('È', 'E'), '']; continue
        if i == 0 and (COURANT.match(s) or re.fullmatch(r"[\dIlO]{1,3}", s)): continue
        if re.fullmatch(r"B\. ?S\.-?C\.\s*\d*", s) or re.fullmatch(r"\d{1,3}", s): continue
        if re.fullmatch(r"PETIT BRÉVIAIRE|DU SACRÉ\s*-\s*CŒUR DE JÉSUS.*", s): continue
        ind = len(l) - len(l.lstrip()) - base
        if ind >= 2 or MARQUE.match(s): out.append('')
        out.append(s)
    return out


lignes = []
for p in range(DEBUT, FIN):
    lignes += page(p)
texte = '\n'.join(lignes)
texte = re.sub(r"\(1\) Tous les versets en italiques.*?1876\.\)\.?", "", texte, flags=re.S)
texte = re.sub(r"\(1\) La dévotion au Sacré-Cœur\.", "", texte)
# mot coupé en fin de ligne : recollé, sauf trait d'union de composé (« moi-même », « tout-puissant », « adressez-vous »)
COMPOSE = r"(?:même|mêmes|moi|toi|nous|vous|lui|leur|les|la|le|ci|là|puissant|y|en)\b"
texte = re.sub(r"(\w)-\n\s*(?=" + COMPOSE + ")", r"\1-", texte)
texte = re.sub(r"(\w)-\n\s*([a-zàâçéèêëîïôûùüœ])", r"\1\2", texte)
# l'office du dimanche commence en haut de la 1re page (son titre y est sur la 1re ligne)
texte = '@@DIMANCHE\n\n' + texte if not texte.lstrip().startswith('@@') else texte
out = []
for bloc in re.split(r"\n?@@(?=[A-Z])", texte)[1:]:
    jour, _, corps = bloc.partition('\n')
    paras = [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", corps)]
    paras = [re.sub(r"\s{2,}", " ", p) for p in paras if p]
    c = '\n\n'.join(paras)
    # titres courants restés dans le fil (« 82 - OFFICE DU JEUDI », « OFFICE DU MARDI SI ») : retirés, phrase recollée
    c = re.sub(r"\n*[ \t]*(?:[\dIlOΙ$]{1,3}\s*-?\s*)?OFFICE DU [A-ZÈ]+(?:\s+[\dIlOSΙ$]{1,3})?[ \t]*\n*(?=\S)",
               lambda m: ' ' if not m.group(0).startswith('\n') or not re.search(r"\n\n", m.group(0)) else '\n\n', c)
    c = re.sub(r"[ \t]+([,.)])", r"\1", c)
    c = re.sub(r"\.,(?=\n|$)", ".", c)
    c = re.sub(r"(?m)^(?:\.|V\.|v\.|Ý\.|y\.)\s*", "℣. ", c)
    c = re.sub(r"(?m)^R[.7]\s*", "℟. ", c)
    c = re.sub(r"(?m)^(℣\.|℟\.) (?:℣\.|℟\.) ", r"\1 ", c)
    c = re.sub(r"(?m)^AVE MARIA\.\.?\s*(?=\S)", "AVE MARIA.\n\n℣. ", c)
    c = re.sub(r"(?m)^A (MATINES|LAUDES|PRIME|TIERCE|SEXTE|NONE|V[ÊE]PRES|COMPLIES)\.?$", lambda m: "## À " + m.group(1).capitalize().replace('Vepres', 'Vêpres'), c)
    c = re.sub(r"(?m)^(HYMNE|HYNNE|PRIONS|ORAISON|CANTIQUE)\.?$", lambda m: "### " + m.group(1).capitalize().replace('Hynne', 'Hymne'), c)
    c = re.sub(r"(?m)^RECOMMANDATION(?: \( ?1\))?$", "## Recommandation", c)
    c = re.sub(r"\n\n(?:JJEL|-a)\s*$", "", c)
    c = c.replace("TOUT POUR LA PLUS GRANDE GLOIRE\n\nDU SACRÉ - CŒUR DE JÉSUS", "*Tout pour la plus grande gloire du Sacré-Cœur de Jésus.*")
    c = re.sub(r"(?m)^ANT\. ", "*Ant.* ", c)
    c = re.sub(r"(?m)^(?:7|ỹ|◊|✯)\.\s*", "℣. ", c)  # ℣ mal lu
    c = re.sub(r"℣\. ℣\. ", "℣. ", c)
    c = re.sub(r"(?m)^(\(1\) [^\n]+)$", r"*\1*", c)  # notes de bas de page : ne se disent pas
    for a, b in [("n'y C a", "n'y a"), ("Notre- Seigneur", "Notre-Seigneur"), ("sacrifierpour", "sacrifier pour"),
                 ("épargnéjusqu", "épargné jusqu"), ("suggessions", "suggestions"), ("vous vouiez", "vous vouliez"), ("captifpar", "captif par")]:
        c = c.replace(a, b)
    c = re.sub(r"(?m)^[ΟΙIlO$\d]{1,3}\n\n", "", c)  # numéro de page isolé (« ΟΙ » en grec par l'OCR)
    c = re.sub(r"au\n\nSaint-Esprit", "au Saint-Esprit", c)
    c = re.sub(r"(?m)^(Le reste comme à [^\n]*)$", r"*\1*", c)
    # note de bas de page coupée au milieu de la Recommandation : la fin de la prière revient à sa place
    c = re.sub(r"glorifier\n\n\*\(1\) (Les mots entre crochets.*?Notre-Seigneur\.) (devant votre Père.*?Ainsi soit-il\.)\*",
               r"glorifier \2\n\n*(1) \1*", c, flags=re.S)
    c = re.sub(r" \( 1\)", " (1)", c)
    c = re.sub(r"(?m)^\*Le reste comme à Matines, pages? \d+\.\*$", "*Le reste comme à Matines.*", c)
    # le sous-titre de l'office (en capitales, avant « À Matines ») devient le titre
    tete, _, reste = c.partition('## À Matines')
    titre = re.sub(r"\s+", " ", tete.replace('\n', ' ')).strip().capitalize()
    out.append({'jour': jour.lower(), 'titre': titre, 'corps': ('## À Matines' + reste).strip()})
# les autres jours renvoient à la Recommandation du dimanche (« page 32 ») : on la recopie
reco = out[0]['corps'][out[0]['corps'].index('## Recommandation'):]
for o in out[1:]:
    o['corps'] = re.sub(r"## Recommandation\n\n\(page 32\.\)", lambda m: reco, o['corps'])
json.dump(out, sys.stdout, ensure_ascii=False)
