"""Stations romaines, d'après le Missale Romanum, éd. typique de 1920
(archive.org : 000missaleromanum-1920), texte copié tel qu'imprimé
(relevé fait pour le calendrier 2026-2027, rattaché ici à Pâques et à l'Avent)."""
from __future__ import annotations

import datetime as dt

from .liturgy import advent1, easter, ember_september

D = dt.date
TD = dt.timedelta


def S(x: str) -> str:
    return "Statio ad " + x


# décalages par rapport au 1er dimanche de l'Avent
ADVENT = [(0, "S. Mariam majorem"), (7, "S. Crucem in Jerusalem"), (14, "S. Petrum"),
          (17, "S. Mariam majorem"), (19, "Ss. duodecim Apostolos"), (20, "S. Petrum"),
          (21, "Ss. duodecim Apostolos")]
# dates fixes du temps de Noël
FIXED = {(12, 25): "Statio ad S. Mariam majorem ad Praesepe ; ad S. Anastasiam ; ad S. Mariam majorem",
         (12, 26): S("S. Stephanum in Cælio monte"), (12, 27): S("S. Mariam majorem"),
         (12, 28): S("S. Paulum"), (1, 1): S("S. Mariam trans Tiberim"), (1, 6): S("S. Petrum")}
# décalages par rapport à Pâques
EASTER = [(-63, 'S. Laurentium extra muros'), (-56, 'S. Paulum'), (-49, 'S. Petrum'), (-46, 'S. Sabinam'),
          (-45, 'S. Georgium'), (-44, 'Ss. Joannem et Paulum'), (-43, 'S. Tryphonem'), (-42, 'S. Joannem in Laterano'),
          (-41, 'S. Petrum ad Vincula'), (-40, 'S. Anastasiam'), (-39, 'S. Mariam majorem'),
          (-38, 'S. Laurentium in Panisperna'), (-37, 'Ss. duodecim Apostolos'), (-36, 'S. Petrum'),
          (-35, 'S. Mariam in Domnica'), (-34, 'S. Clementem'), (-33, 'S. Balbinam'), (-32, 'S. Caeciliam'),
          (-31, 'S. Mariam trans Tiberim'), (-30, 'S. Vitalem'), (-29, 'Ss. Marcellinum et Petrum'),
          (-28, 'S. Laurentium extra muros'), (-27, 'S. Marcum'), (-26, 'S. Pudentianam'), (-25, 'S. Xystum'),
          (-24, 'Ss. Cosmam et Damianum'), (-23, 'S. Laurentium in Lucina'), (-22, 'S. Susannam'),
          (-21, 'S. Crucem in Jerusalem'), (-20, 'Ss. Quatuor Coronatos'), (-19, 'S. Laurentium in Damaso'),
          (-18, 'S. Paulum'), (-17, 'Ss. Silvestrum et Martinum'), (-16, 'S. Eusebium'),
          (-15, 'S. Nicolaum in Carcere'), (-14, 'S. Petrum'), (-13, 'S. Chrysogonum'), (-12, 'S. Cyriacum'),
          (-11, 'S. Marcellum'), (-10, 'S. Apollinarem'), (-9, 'S. Stephanum in Cælio monte'),
          (-8, 'S. Joannem ante Portam Latinam'), (-7, 'S. Joannem in Laterano'), (-6, 'S. Praxedem'),
          (-5, 'S. Priscam'), (-4, 'S. Mariam majorem'), (-3, 'S. Joannem in Laterano'),
          (-2, 'S. Crucem in Jerusalem'), (-1, 'S. Joannem in Laterano'), (0, 'S. Mariam majorem'),
          (1, 'S. Petrum'), (2, 'S. Paulum'), (3, 'S. Laurentium extra muros'), (4, 'Ss. duodecim Apostolos'),
          (5, 'S. Mariam ad Martyres'), (6, 'S. Joannem in Laterano'), (7, 'S. Pancratium'),
          (36, 'S. Mariam majorem'), (37, 'S. Joannem in Laterano'), (38, 'S. Petrum'), (39, 'S. Petrum'),
          (48, 'S. Joannem in Laterano'), (49, 'S. Petrum'), (50, 'S. Petrum ad Vincula'), (51, 'S. Anastasiam'),
          (52, 'S. Mariam majorem'), (53, 'S. Laurentium extra muros'), (54, 'Ss. duodecim Apostolos'),
          (55, 'S. Petrum')]
SEPT = ["S. Mariam majorem", "Ss. duodecim Apostolos", "S. Petrum"]


def stations(year_of_advent: int) -> dict[D, str]:
    """Stations de l'année liturgique commençant à l'Avent de year_of_advent."""
    a = advent1(year_of_advent)
    y = year_of_advent + 1
    E = easter(y)
    st: dict[D, str] = {}
    for o, c in ADVENT:
        st[a + TD(o)] = S(c)
    for (m, dd), c in FIXED.items():
        st[D(year_of_advent if m == 12 else y, m, dd)] = c
    for o, c in EASTER:
        st[E + TD(o)] = S(c)
    # Litanies majeures (25 avril) ; reportées au mardi de Pâques si le 25 avril est le jour de Pâques
    lm = D(y, 4, 25)
    if lm == E:
        lm = E + TD(2)
    st[lm] = "Litaniæ majores : " + S("S. Petrum")
    for d, c in zip(ember_september(y), SEPT):
        st[d] = S(c)
    return st
