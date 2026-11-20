"""Mois de saint Joseph : cas non automatiques de hamon/decider.py tranchés sur la liste des deux lectures
(A = couche texte d'archive.org, B = Tesseract), seulement quand la bonne lecture est sans doute possible ;
les autres sont laissés. Écrit dec<S>.txt dans le dossier de travail, pour hamon/appliquer.py.

Usage : python3 -I decisions_tesseract.py <dossier>
"""
import sys

D = sys.argv[1]
dec = {
    'a': {8: 'Dans', 13: 'fête', 14: 'obtenus', 15: 'dans', 20: 'B', 22: 'obtenir', 23: 'B', 26: 'Notre-Seigneur,', 32: 'B',
          37: 'B', 40: 'Hérode', 54: 'B', 70: 'TITRE', 76: 'chaque', 78: 'cette', 79: 'tout', 82: 'de', 87: 'B', 88: 'B',
          92: 'Domini;', 95: 'Ægyptum.', 96: 'trois', 99: 'tuer', 100: 'Mariæ...', 104: "l'Enfant-Dieu", 109: 'tibi!',
          117: 'DEUXIÈME', 120: "m'empêcher", 121: "d'Hérode,", 126: 'JÉSUS', 128: 'B', 139: 'B', 141: 'B', 142: 'grand',
          145: 'le', 146: 'B', 149: 'Joseph', 154: 'sujets', 158: 'patientiæ.', 159: 'B', 160: 'avait-il', 168: 'B', 179: 'B'},
    'b': {3: 'B', 9: 'B', 10: 'B', 17: 'B', 23: 'Égypte,', 29: 'B', 35: 'terre', 42: 'non-seulement', 43: 'votre', 48: 'B',
          49: 'votre', 60: 'B', 61: 'B', 72: 'B', 73: 'B', 75: 'B', 79: 'B', 80: 'B', 86: 'saintes', 87: 'væ', 96: 'B',
          101: 'sentiment!', 102: 'B', 109: 'B', 115: '(Rom.,', 118: 'æternum', 121: 'B', 122: 'B', 132: 'apôtre',
          135: 'Représentez-vous', 139: 'B', 140: 'B', 172: 'B', 174: 'Dieu', 177: 'B', 187: 'Deus', 188: 'maître',
          197: 'Paul;', 199: 'nous.', 202: 'B', 208: 'B', 214: 'fortitudinem', 215: 'omnes...', 222: 'B', 226: 'B',
          230: 'Quid', 232: 'B', 233: 'B', 239: 'saintes,', 240: 'B', 242: 'B', 247: 'B', 254: 'B', 263: 'luxuriæ,', 269: 'B',
          275: 'vertu', 277: "l'œuvre", 280: 'B', 287: "s'emporteront", 290: 'homo', 304: 'Esther;', 307: 'glorifier,'},
    'c': {3: 'enfante', 4: 'B', 5: 'protector', 6: 'B', 13: 'B', 27: 'B', 39: 'Je', 40: 'dans', 46: 'B', 48: 'B',
          49: 'Borgia,', 60: 'JOSEPH', 66: 'B', 86: 'B', 95: 'B', 100: 'touchants', 107: 'cieux,', 112: 'et',
          116: 'FAMILLE.', 122: 'de', 131: 'B', 135: 'B', 141: 'tabernaculo', 145: 'B', 146: 'B', 147: 'B', 148: 'B',
          150: 'PROTECTEUR', 160: 'B', 163: 'B', 167: 'protection', 168: 'PÉCHEURS.', 172: "l'honneur", 174: 'B',
          176: 'JOSEPH', 188: 'B', 190: 'Voici', 205: 'B', 208: 'libenter'},
    'd': {0: 'B', 1: "C'est", 2: 'B', 3: "N'est-ce", 5: 'Ecclesiæ', 13: 'B', 17: 'Nous', 22: 'B', 28: 'TRIDUUM', 30: 'B',
          32: 'lætificaverunt', 36: 'ALLÉGRESSES', 44: 'B', 47: 'TRIDUUM).', 51: 'consolationes', 52: 'lætificaverunt',
          57: 'Hérode,', 62: 'TRENTIÈME', 63: 'B', 64: 'Domini', 66: 'sanctorum', 71: 'B', 73: 'B', 77: 'B', 79: 'B',
          86: 'Hérode.', 87: 'MORT', 88: 'B', 100: 'B', 101: 'chrétien,', 109: 'Vierge,', 111: 'B', 117: 'B', 126: 'PSAUME',
          129: 'B', 130: 'æterna', 135: 'B', 136: 'B', 138: 'bienheureuse.', 158: 'B', 163: 'B', 170: 'hâtez-vous',
          172: 'hâtez-vous', 174: 'hâtez-vous', 176: 'B', 177: 'hâtez-vous', 180: 'B', 181: 'B', 185: 'B', 189: 'B',
          190: 'B', 198: 'B', 208: 'B', 209: 'B', 211: 'B', 225: 'B', 234: 'Herodis', 235: 'B', 244: 'B', 246: 'B',
          251: 'B', 253: 'B', 258: 'B', 263: 'B', 267: 'B', 274: 'B', 281: 'B', 282: 'B', 283: 'B', 285: 'B',
          286: 'faites', 289: 'REFUGE', 290: 'PÉCHEURS', 293: 'B', 308: 'B'},
}
for s, m in dec.items():
    open(f'{D}/dec{s}.txt', 'w', encoding='utf-8').write(''.join(f'{k}\t{v}\n' for k, v in sorted(m.items())))
print('décisions :', sum(len(m) for m in dec.values()))
