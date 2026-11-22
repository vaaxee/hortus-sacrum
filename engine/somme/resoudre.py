"""Somme (Lachat) : tranche les désaccords sûrs laissés par voter.py ; le reste va à l'image (decisions.txt).

Ordre :
 0. decisions.txt (relu sur l'image) : « page<TAB>signalement exact<TAB>texte retenu », appliqué en premier ;
    une ligne « *<TAB>lecture<TAB>texte » vaut pour tout signalement dont les lectures sont toutes dans la liste
    « lecture » (séparées par ⁞) ; elle est établie après vérification de plusieurs cas sur l'image.
 1. Numéros d'objection et de réponse (« 1° », lus « 4° », « I^ », « l» »…) : marqués ⟦°⟧, renumérotés par
    construire.py d'après la place dans l'article (vérifié : 1°, 2°… se suivent).
 2. Taches : signe sans lettre ni chiffre donné par une seule lecture → retiré.
 3. Lexique des mots retenus ailleurs dans le livre par accord Tesseract + ABBYY (orthographe de 1880 comprise :
    « connoître », « étoit ») : si une seule des lectures est attestée, elle ; si plusieurs, la plus fréquente quand
    elle l'est au moins 20 fois plus que la suivante.
 4. Sinon : laissé signalé pour l'image.

Usage : python3 -I resoudre.py <V.json> <sortie.json> [decisions.txt]
"""

import collections
import json
import re
import sys
import unicodedata

CLE = re.compile(r"[^\wÀ-ÿœŒæÆ'-]")
ORD = re.compile(r"^(\d{1,2}|[IlLi|!]|[IVX]{1,4})[°o\"'^»*«<>%®]{0,3}\W{0,2}$")


def cle(w):
    return CLE.sub('', unicodedata.normalize('NFC', w))


def lexique(V):
    lex = collections.Counter()
    for p in V:
        for l in p['lignes']:
            if l['sure']:
                for w in l['t'].split():
                    lex[cle(w)] += 1
    return lex


def main():
    V = json.load(open(sys.argv[1]))
    dec, gen = {}, []
    if len(sys.argv) > 3:
        for ligne in open(sys.argv[3], encoding='utf-8'):
            if ligne.strip() and not ligne.startswith('#'):
                pg, sig, txt = ligne.rstrip('\n').split('\t')
                if pg == '*':
                    gen.append((set(sig.split('⁞')), txt))
                else:
                    dec[(int(pg), sig)] = txt
    lex = lexique(V)
    stats = collections.Counter()
    for p in V:
        for l in p['lignes']:
            if l['sure']:
                continue

            def tranche(m):
                sig = m.group(0)
                if (p['page'], sig) in dec:
                    stats['décision'] += 1
                    return dec[(p['page'], sig)]
                f = m.group(1)
                if f == 'ligne':
                    return sig
                plus = f.startswith('+')
                vals = (f[1:] if plus else f).split('⁞')
                lus = [x for x in vals if x not in ('None', '')]
                for ens, txt in gen:
                    if lus and set(lus) <= ens:
                        stats['décision générale'] += 1
                        return txt
                if any(re.fullmatch(r'\d{1,2}°', x) for x in lus) and all(ORD.match(x) for x in lus):
                    stats['numéro'] += 1
                    return '⟦°⟧'
                if len(lus) == 1 and not re.search(r'\w', lus[0]):
                    stats['tache'] += 1
                    return ''
                if not plus and len(lus) == 1 and lus[0] == vals[0] and lex[cle(lus[0])] == 0:
                    stats['tache'] += 1
                    return ''  # C seul, mot inconnu : tache
                att = sorted(((lex[cle(x)], x) for x in dict.fromkeys(lus) if cle(x) and lex[cle(x)] > 0),
                             reverse=True)
                if len(att) == 1:
                    stats['un seul attesté'] += 1
                    return att[0][1]
                if len(att) > 1 and att[0][0] >= 20 * att[1][0]:
                    stats['le plus fréquent'] += 1
                    return att[0][1]
                stats['reste'] += 1
                return sig

            l['t'] = re.sub(r'\s+', ' ', re.sub(r'⟦([^⟧]*)⟧', tranche, l['t'])).strip()
            l['sure'] = not re.search(r'⟦(?!°⟧)', l['t'])
    json.dump(V, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
    print(dict(stats))


if __name__ == '__main__':
    main()
