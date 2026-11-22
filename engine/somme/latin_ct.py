"""Somme : texte latin (édition léonine, Rome 1888) d'après la transcription du Corpus Thomisticum (E. Alarcón),
découpé par question et article : prooemium, arg., s. c., co., ad.

Usage : python3 -I latin_ct.py <dossier des pages sth10NN.html> <q0> <q1> <sortie.json>
Sortie : {"1": {"pr": "...", "articles": {"1": {"arg": [...], "sc": "...", "co": "...", "ad": [...]}}}}
Le texte est gardé tel quel (orthographe léonine : « huius », « quae ») ; les italiques des citations sont rendues par
*…* (balisage du projet). Les numéros de paragraphe [28232] et les références « Iª q. 1 a. 1 arg. 1 » sont retirés.
"""

import glob
import html
import json
import re
import sys


def lire(dossier):
    paras = {}
    for f in sorted(glob.glob(f'{dossier}/sth10*.html')):
        s = open(f, encoding='utf-8', errors='replace').read()
        for title, body in re.findall(r'<P TITLE="([^"]+)">(.*?)</P>', s, re.S):
            body = re.sub(r'<A NAME="\d+"><SPAN CLASS="ref">.*?</SPAN></A>', '', body, flags=re.S)
            body = re.sub(r'</?I>', '*', body)
            body = re.sub(r'<[^>]+>', '', body)
            body = html.unescape(body)
            body = re.sub(r'\s+', ' ', body).strip()
            body = body.replace('* *', ' ').replace('**', '')
            paras[title] = body
    return paras


def main():
    d, q0, q1, dest = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    P = lire(d)
    out = {}
    for t, body in P.items():
        m = re.match(r'I q\. (\d+) (pr\.|a\. (\d+) (arg\. (\d+)|s\. c\.(?: \d)?|co\.|ad (\d+)|ad arg\.|ad))$', t)
        if not m:
            print('?', t, file=sys.stderr)
            continue
        q = int(m.group(1))
        if not q0 <= q <= q1:
            continue
        Q = out.setdefault(str(q), {'pr': '', 'articles': {}})
        if m.group(2) == 'pr.':
            Q['pr'] = body
            continue
        A = Q['articles'].setdefault(m.group(3), {'arg': [], 'sc': '', 'co': '', 'ad': []})
        k = m.group(4)
        if k.startswith('arg'):
            A['arg'].append(body)
            assert len(A['arg']) == int(m.group(5)), t
        elif k.startswith('s. c.'):
            A['sc'] = (A['sc'] + '\n\n' + body).strip()
        elif k == 'co.':
            A['co'] = (A['co'] + '\n\n' + body).strip()
        else:
            A['ad'].append(body)
    json.dump(out, open(dest, 'w'), ensure_ascii=False, indent=1)
    for q in sorted(out, key=int):
        print(q, {a: (len(x['arg']), len(x['ad'])) for a, x in out[q]['articles'].items()})


if __name__ == '__main__':
    main()
