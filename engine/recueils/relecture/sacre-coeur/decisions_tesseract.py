"""Mois du Sacré-Cœur : cas non automatiques de hamon/decider.py tranchés sur la liste des deux lectures
(A = couche texte d'archive.org, B = Tesseract), seulement quand la bonne lecture est sans doute possible ;
les autres sont laissés. Écrit dec<S>.txt dans le dossier de travail, pour hamon/appliquer.py.

Usage : python3 -I decisions_tesseract.py <dossier>
"""
import sys

D = sys.argv[1]
B = 'B'
dec = {
    'a': {14: 'et', 18: 'semaines', 21: 'Visitation', 23: B, 29: 'Cœur!...', 39: 'CŒUR', 40: B, 41: B, 43: B, 47: B, 51: B, 56: B,
          57: "l'Homme-Dieu", 63: B, 65: B, 67: 'Jésus.', 71: 'CŒUR', 74: B, 76: B, 86: 'âme!', 95: 'Judæorum...', 96: B,
          111: B, 118: B, 121: 'habitare!', 125: B, 126: B, 129: B, 131: B, 141: B, 143: B, 144: B, 147: 'sanguinem...',
          149: B, 153: 'éternelles,', 154: B, 157: 'âme', 162: B, 169: B, 175: 'croix!', 179: 'Sudores', 187: 'zèle',
          196: "l'empressement naturel,", 199: B, 202: "l'avant-propos", 206: B, 210: 'Ciel.', 213: B, 222: 'Cœur', 236: B,
          242: 'reconnaîtrez', 243: B, 244: B, 249: B, 253: B, 255: B, 261: B, 268: B, 276: 'Ah!', 286: '(Suite)', 290: B,
          312: 'souffrances;', 318: B, 326: B, 334: 'JOUR.', 335: B, 336: B},
    'b': {3: 'JÉSUS.', 15: B, 19: B, 21: 'CONSÉCRATION', 24: B, 25: B, 27: B, 28: B, 32: B, 40: B, 55: 'Celles-ci', 69: B,
          73: 'œuvres', 74: 'miracles', 77: B, 86: B, 87: B, 90: B, 96: B, 97: B, 99: B, 103: 'MYSTÈRES', 105: B, 110: "C'est",
          123: 'moi;', 126: B, 129: B, 139: B, 140: B, 141: 'chagrin', 145: 'Est-il', 147: B, 156: B, 157: 'pas', 158: B,
          160: 'pouvons', 162: B, 166: 'VINGT-QUATRIÈME', 169: "c'est", 170: B, 172: 'sanguinis', 175: B, 178: B, 184: 'hominibus.',
          187: B, 190: B, 191: B, 203: B, 206: "l'étonnement.", 207: B, 208: "N'est-ce", 209: B, 216: B, 219: B, 221: B,
          223: B, 226: B, 227: B, 230: B, 234: B, 240: 'cœur', 254: "d'Autun.", 258: B, 259: B, 261: B, 266: 'COEURS.',
          269: B, 271: B, 273: B, 282: B, 283: B, 284: B, 286: B, 290: B, 298: B, 321: B, 322: B, 361: B, 365: B, 367: B,
          370: B, 382: B, 387: B, 396: B, 399: 'Christe,', 402: B, 403: B, 405: B, 407: B, 419: B, 425: B, 431: B,
          446: B, 476: 'Cœur', 512: B},
}
for s, m in dec.items():
    open(f'{D}/dec{s}.txt', 'w', encoding='utf-8').write(''.join(f'{k}\t{v}\n' for k, v in sorted(m.items())))
print('décisions :', sum(len(m) for m in dec.values()))
