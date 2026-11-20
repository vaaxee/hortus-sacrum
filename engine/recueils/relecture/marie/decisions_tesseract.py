"""Mois de Marie : cas non automatiques de hamon/decider.py tranchés sur la liste des deux lectures
(A = couche texte d'archive.org, B = Tesseract), seulement quand la bonne lecture est sans doute possible ;
les autres sont laissés. Écrit dec<S>.txt dans le dossier de travail, pour hamon/appliquer.py.

Usage : python3 -I decisions_tesseract.py <dossier>
"""
import sys

D = sys.argv[1]
B = 'B'
dec = {
    'a': {4: 'TRÈS-SAINTE', 6: "l'Archevêché.", 12: 'confiance', 19: B, 24: "l'Inviolata.", 25: B, 26: "l'oraison", 27: B, 34: B,
          36: B, 53: B, 59: 'attester', 64: B, 65: 'péché...', 68: B, 72: B, 74: 'diffidas...', 80: 'DEUXIÈME',
          86: 'ordinairement', 87: 'méditation', 91: B, 96: 'plus', 99: 'dulcedo,', 104: B, 109: 'diffidas', 110: B, 119: B,
          123: B, 124: 'caritate', 129: 'votre', 136: B, 147: 'saint', 154: B, 155: 'saint', 159: 'Cieux!...', 161: B, 164: B,
          167: B, 172: 'VIERGE.', 173: B, 189: B, 193: B, 201: "l'Homme-Dieu,", 205: 'étonnement', 208: B, 221: 'diebus',
          223: B, 225: B, 226: B, 229: B, 233: B, 240: B, 243: "l'Expectation", 255: B, 258: B, 260: B, 267: B,
          273: 'admirabilis,', 291: B, 297: B, 301: B, 308: B, 313: B, 320: B, 322: B, 326: B, 327: B, 330: B, 332: B,
          333: "l'obliger,", 339: B, 344: B, 346: 'enfant', 352: B, 365: B, 368: B, 369: 'NAZARETH', 381: B, 382: B, 387: B,
          388: B, 396: B, 401: 'potentissime...', 402: B, 413: B, 438: 'Jésus', 441: B, 442: B},
    'b': {0: B, 1: 'religieuse!', 16: 'nombre', 18: 'parole', 22: B, 35: B, 64: B, 71: B, 83: 'VINGT-DEUXIÈME', 86: B, 88: B,
          90: B, 99: 'priez', 100: 'Regina...', 103: B, 124: B, 125: B, 133: 'union', 144: B, 151: 'reconnaître', 154: B,
          166: 'célèbre', 170: B, 179: B, 181: B, 182: B, 192: B, 194: B, 196: 'vit,', 206: B, 215: B, 218: B, 219: 'Ciel.',
          222: B, 226: B, 232: B, 235: B, 241: B, 243: B, 247: B, 249: B, 253: "m'empêcher", 254: B, 256: B, 263: B,
          269: 'glorificant,', 276: B, 277: 'tuis!', 286: 'trouvera.', 290: "d'amour.", 302: 'cœur.', 303: B, 307: B, 316: B,
          325: B, 347: B, 355: B, 365: B, 367: B, 368: B, 375: B, 376: 'flammæ', 383: 'PURGATOIRE.', 384: B,
          394: "l'Incarnation", 409: B, 422: B, 440: 'soit-il.', 454: B, 457: B, 460: B, 461: 'entendre', 484: B, 489: B,
          493: 'quam', 505: 'cœur', 513: 'constantiam.', 515: B, 520: 'tormentis.', 529: 'supplions,', 533: B, 539: B, 544: B,
          553: B, 555: B, 558: B, 560: B, 572: B},
}
for s, m in dec.items():
    open(f'{D}/dec{s}.txt', 'w', encoding='utf-8').write(''.join(f'{k}\t{v}\n' for k, v in sorted(m.items())))
print('décisions :', sum(len(m) for m in dec.values()))
