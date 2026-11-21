"""Officium parvum Beatæ Mariæ Virginis, composé depuis les fichiers de Divinum Officium (latin seul).

Sortie : data/office/parvum.json — chaque heure du Petit Office, pour chaque jour des années du calendrier
(app/static/data/calendar), rédigée au balisage léger de l'application, les textes identiques mis en commun.

Le Petit Office est dans DO l'office votif « C12 » (Commune/C12.txt, « Officium parvum Beatæ Mariæ Virginis ») ;
horascommon.pl (sub precedence, « C12: Officium parvum BMV ») le redirige vers Commune/C12A.txt pendant l'Avent (et à
l'Annonciation), vers Commune/C12N.txt de la veille de Noël aux Vêpres jusqu'au 2 février, vers Commune/C12Q.txt de la
Septuagésime au Samedi saint ; le reste de l'année, Commune/C12.txt. Le commun « ex C11 » complète ce qui manque.

Prime, Tierce, Sexte, None et Complies sont écrites en entier dans ces fichiers (sections « Special <Heure> »,
specials.pl : « return loadspecial(...) »). Matines, Laudes et Vêpres suivent le canevas Ordinarium/<Heure>.txt, rempli
comme le fait specials.pl et ses modules (psalmi.pl, capitulis.pl, hymni.pl, orationes.pl, specmatins.pl, horas.pl,
horasscripts.pl) : chaque règle reprise ici cite sa source ; le Perl n'est pas exécuté, il est lu comme une
spécification.

Choix fixés (ce que DO laisse à l'utilisateur ou tire de l'office du jour) :
- rubriques « Divino Afflatu - 1954 » ; récitant qui n'est pas prêtre (« Domine, exaudi » au lieu de
  « Dominus vobiscum ») ;
- aux Vêpres, les éléments « 1 » du Petit Office (Ant 1, Versum 1, Oratio 1, Capitulum Vespera), que C12 et ses
  variantes définissent pour elles ; DO prend « 1 » ou « 3 » selon la concurrence des offices du jour, que l'office
  votif ignore ;
- le samedi, Vêpres et Complies prennent le temps du dimanche (voir dayname0) ;
- numéros de versets des psaumes et des leçons omis (option « nonumbers » de DO).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lire import (  # noqa: E402
    VERSION,
    Contexte,
    Lecteur,
    SectionManquante,
    depot,
    dayname_pour_condition,
    lire_lignes,
    ordinarium,
    getweek,
    psaume_brut,
    tempus_id,
    LATIN,
)

ROOT = Path(__file__).resolve().parents[2]
CALENDRIER = ROOT / "data" / "calendar"
SORTIE = ROOT / "data" / "office" / "parvum.json"

HEURES = [
    ("matines", "Matines", "Matutinum", "Ad Matutinum"),
    ("laudes", "Laudes", "Laudes", "Ad Laudes"),
    ("prime", "Prime", "Prima", "Ad Primam"),
    ("tierce", "Tierce", "Tertia", "Ad Tertiam"),
    ("sexte", "Sexte", "Sexta", "Ad Sextam"),
    ("none", "None", "Nona", "Ad Nonam"),
    ("vepres", "Vêpres", "Vespera", "Ad Vesperas"),
    ("complies", "Complies", "Completorium", "Ad Completorium"),
]

TEMPS = {
    "adventus": "Temps de l’Avent (Commune/C12A)",
    "annuntiatio": "Annonciation (Commune/C12A)",
    "nativitatis": "De Noël à la Purification (Commune/C12N)",
    "septuagesimae": "De la Septuagésime au Samedi saint (Commune/C12Q)",
    "post-epiphaniam": "Après l’Épiphanie (Commune/C12)",
    "paschale": "Temps pascal (Commune/C12)",
    "post-pentecosten": "Après la Pentecôte (Commune/C12)",
}

CODE_LU = [
    "web/cgi-bin/DivinumOfficium/SetupString.pl",
    "web/cgi-bin/DivinumOfficium/LanguageTextTools.pm",
    "web/cgi-bin/horas/horascommon.pl",
    "web/cgi-bin/horas/horas.pl",
    "web/cgi-bin/horas/horasscripts.pl",
    "web/cgi-bin/horas/specials.pl",
    "web/cgi-bin/horas/specmatins.pl",
    "web/cgi-bin/horas/specials/psalmi.pl",
    "web/cgi-bin/horas/specials/capitulis.pl",
    "web/cgi-bin/horas/specials/hymni.pl",
    "web/cgi-bin/horas/specials/orationes.pl",
    "web/cgi-bin/horas/specials/preces.pl",
    "web/cgi-bin/horas/webdia.pl",
]


# --- Le jour --------------------------------------------------------------------------------------------------------


def fichier_du_petit_office(mois: int, jour: int, hora: str, dayname0: str, annonciation: bool) -> str:
    """horascommon.pl, sub precedence : redirection de C12 (« unless ($version =~ /cist/i) »)."""
    if (mois == 12 and ((jour == 24 and hora in ("Vespera", "Completorium")) or jour > 24)) or mois == 1 or (
        mois == 2 and jour < 3
    ):
        return "Commune/C12N"
    if re.search("adv", dayname0, re.I) or annonciation:
        return "Commune/C12A"
    if re.search("(Quadp|Quad)", dayname0, re.I):
        return "Commune/C12Q"
    return "Commune/C12"


def temps_nomme(fichier: str, c: Contexte) -> str:
    """Le nom du temps, pour nommer les textes (la composition, elle, ne dépend que du contexte)."""
    if fichier.endswith("C12A"):
        return "adventus" if c.dayname0.startswith("Adv") else "annuntiatio"
    if fichier.endswith("C12N"):
        return "nativitatis"
    if fichier.endswith("C12Q"):
        return "septuagesimae"
    t = tempus_id(c)
    if c.dayname0.startswith("Pasc") or re.search("Paschæ|Ascensionis|Octava Pentecostes", t):
        return "paschale"
    if "post Epiphaniam" in t:
        return "post-epiphaniam"
    return "post-pentecosten"


def dayname0(date: dt.date, hora: str) -> str:
    """$dayname[0] de DO pour la date et l'heure (horascommon.pl : « @dayname = (getweek(...)) »).

    DO le remplace par celui du lendemain quand les Vêpres du lendemain l'emportent, ce qui dépend de l'office du jour.
    L'office votif n'a pas de concurrence : on retient la règle que DO applique au temps (horascommon.pl, sub
    gettempora : « getweek($day, $month, $year, $dayofweek == 6 && $hora =~ /Vespera|Completorium/) ») — le samedi,
    Vêpres et Complies sont du dimanche qui suit (premières Vêpres de l'Avent, de la Septuagésime, de Pâques)."""
    dow = (date.weekday() + 1) % 7
    return getweek(date.day, date.month, date.year, dow == 6 and hora in ("Vespera", "Completorium"))


# --- La composition -------------------------------------------------------------------------------------------------


class Heure:
    """Le script d'une heure (lignes DO), puis son développement en texte."""

    def __init__(self, c: Contexte, lecteur: Lecteur):
        self.c = c
        self.lec = lecteur
        self.winner = c.winner
        self.w = lecteur.fichier(c.winner)
        self.commune = lecteur.fichier("Commune/C11")  # horascommon.pl : $commune = C11, $communetype = 'ex'
        self.rule = self.w.get("Rule", "")
        self.s: list[str] = []
        self.vespera = 1

    # specials.pl, sub getproprium : le gagnant, puis le commun (« ex »)
    def proprium(self, nom: str) -> str:
        if self.w.get(nom):
            return self.w[nom]
        if self.commune.get(nom):
            return self.commune[nom]
        substitut = {"Nocturn 1 Versum": "Versum 1", "Versum Nona": "Versum 2"}.get(nom)
        if substitut and self.commune.get(substitut):
            return self.commune[substitut]
        return ""

    # specials.pl, sub getantvers
    def antvers(self, item: str, ind: int) -> str:
        w = self.proprium(f"{item} {ind}")
        if not w and ind > 1:
            w = self.proprium(f"{item} {4 - ind}")
        if not w:
            raise SectionManquante(f"{item} {ind}")
        return w

    def translate(self, nom: str) -> str:
        return self.lec.fichier("Psalterium/Common/Translate").get(nom, nom).strip() or nom

    def titre(self, item: str) -> None:
        self.s.append(self.translate(item))

    # ---- psalmodie (psalmi.pl, sub antetpsalm)
    def antetpsalm(self, psalmi: list[str]) -> None:
        derniere = ""
        for ligne in psalmi:
            ant, _, psaumes = ligne.partition(";;")
            if ant:
                if derniere:
                    self.s.pop()
                    self.s += [f"Ant. {derniere}", "\n"]
                ant = re.sub(r"~?\n", " ", ant)
                antp = re.sub(r"\s+\*.*", "", ant)  # duplexf faux : C12 est exclu (psalmi.pl, « $winner !~ /C12/ »)
                antp = re.sub(r",$", ".", antp)
                self.s.append(f"Ant. {antp}")
                derniere = ant.replace("* ", "", 1) if "* " in ant else ant
            p = psaumes.split(";")
            for i, n in enumerate(p):
                n = n.strip()
                n = re.sub(r"[\(\-]", ",", n).replace(")", "")
                if i < len(p) - 1:
                    n = "-" + n
                self.s += [f"&psalm({n})", "\n"]
        if derniere:
            self.s[-1] = f"Ant. {derniere}"

    # ---- Matines (specmatins.pl)
    def invitatorium(self) -> None:
        ant = self.proprium("Invit")  # le gagnant a [Invit] : getproprium l'emporte sur le psautier
        ant = re.sub(r"^.*?=\s*", "", ant.strip()).strip()
        ant = f"Ant. {ant}"
        moities = ant.split("*")
        ant2 = f"Ant. {moities[1]}" if len(moities) > 1 else ant
        texte = "\n".join(lire_lignes(LATIN / "Psalterium" / "Invitatorium.txt"))
        texte = re.sub(r"[+*^=_] ", "", texte)
        texte = texte.replace("$ant2", ant2).replace("$ant", ant)
        self.s.append(texte)

    def hymnus(self, nom: str, section: str) -> None:
        """hymni.pl, sub gethymn (Matines, Laudes, Vêpres)."""
        hymne = self.proprium(nom)
        if not hymne:
            raise SectionManquante(nom)
        if "*" in hymne:  # doxologie : « Doxology=Nat » (hymni.pl, sub doxology)
            m = re.search(r"Doxology=([a-z]+)", self.rule, re.I)
            dox = self.lec.fichier("Psalterium/Doxologies").get(m.group(1)) if m else None
            if dox:
                hymne = re.sub(r"\*.*", lambda _: dox, hymne, count=1, flags=re.S)
        hymne = re.sub(r"^(?:v\.\s*)?([A-ZÀ-ÖØ-ÞÆŒ])", r"v. \1", hymne, count=1)
        hymne = re.sub(r"\*\s*", "", hymne)
        hymne = re.sub(r"_\n(?!!)", "_\nr. ", hymne)
        self.s.append(f"{section}\n{hymne}")

    def psalmi_matutinum(self) -> None:
        # specmatins.pl, sub getantmatutinum : antiennes du commun, versets des nocturnes intercalés
        w = self.proprium("Ant Matutinum").rstrip("\n").split("\n")
        lignes: list[str] = []
        for noc in (1, 2, 3):
            n = min(3, len(w))
            lignes += w[:n]
            w = w[n:]
            lignes += self.proprium(f"Nocturn {noc} Versum").rstrip("\n").split("\n")
        # « Votive nocturn » : trois psaumes selon le jour (dayofweek2i), verset du 3e nocturne
        i = self.c.dayofweek or 1
        if i > 3:
            i -= 3
        debut = (i - 1) * 5
        vers = [lignes[13], lignes[14]]
        if self.c.mois == 12 and self.c.jour == 24:
            vers = self.lec.fichier("Psalterium/Psalmi/Psalmi matutinum")["Nat24 Versum"].rstrip("\n").split("\n")
        self.s.append("!" + self.translate("Ad Nocturnum"))
        self.antetpsalm(lignes[debut:debut + 3])
        self.s += ["\n", *vers, "\n"]
        self.lectiones()

    def tedeum_requis(self, num: int) -> bool:
        """specmatins.pl, sub tedeum_required (office votif de trois leçons)."""
        return num == 3 and not re.search("no Te Deum", self.rule)

    def lectiones(self) -> None:
        # specmatins.pl, sub get_absolutio_et_benedictiones : « BMV special cases », Commune/C12:[Benedictio]
        ben = self.lec.fichier("Commune/C12")["Benedictio"].rstrip("\n").split("\n")
        self.s += ["$rubrica Pater secreto", "$Pater noster Et", f"Absolutio. {ben[0]}", "$Amen", "\n"]
        for i in (1, 2, 3):
            self.s += [self.lec.priere("Jube domne"), f"Benedictio. {ben[i]}", "$Amen", f"&lectio({i})", "\n"]

    def lectio(self, num: int) -> str:
        """specmatins.pl, sub lectio, responsory_gloria, format_lectio (cas du Petit Office)."""
        lect = self.w.get(f"Lectio{num}", "")
        if not lect:
            raise SectionManquante(f"Lectio{num}")
        lect = re.sub(r"&teDeum\n*", "", lect)
        lect = re.sub(r"~?\s*$", "\n$Tu autem", lect, count=1)
        resp = ""
        if not self.tedeum_requis(num):
            resp = self.w.get(f"Responsory{num}") or self.commune.get(f"Responsory{num}", "")
            resp = re.sub(r"&Gloria1?", "&Gloria1", resp)
            if num % 3 == 0 or (num % 3 == 2 and self.tedeum_requis(num + 1)):
                if "&gloria" not in resp.lower():
                    resp = re.sub(r"[\s_]*$", "", resp)
                    resp = re.sub(r"(R\..*?)$", lambda m: f"{m.group(1)}\n&Gloria1\n{m.group(1)}", resp, count=1)
            else:
                resp = re.sub(r".&Gloria.*", "", resp, flags=re.S)
        if resp:
            lect = re.sub(r"\s*$", lambda _: f"\n_\n{resp}", lect, count=1)
        lect = re.sub(r"^_", "", lect)
        if not re.search(r"^!", lect, re.M):
            lect = re.sub(r"^(?=[^\W\d_])", "v. ", lect, count=1)
        elif not re.search(r"^\d", lect, re.M):
            lect = re.sub(r"^!.*?\n(?=[^\W\d_])", lambda m: m.group(0) + "v. ", lect, flags=re.M)
        lignes = ["_", f"!{self.translate('Lectio')} {num}"]
        # format_lectio avec $nonumbers : les versets numérotés, sans leur numéro, forment un seul paragraphe
        initiale = True
        for l in re.split(r"\n+", lect):
            m = re.match(r"^([0-9]+)\s+(.*)", l, re.S)
            if m:
                if initiale:
                    lignes.append("v. " + m.group(2))
                    initiale = False
                else:
                    lignes[-1] += " " + m.group(2)
            else:
                if l.startswith("!"):
                    initiale = True
                lignes.append(l)
        if self.tedeum_requis(num):
            lignes += ["_", "&teDeum"]
        return "\n".join(lignes)

    # ---- Laudes et Vêpres (psalmi.pl, capitulis.pl, hymni.pl, horas.pl, orationes.pl)
    def psalmi_major(self) -> None:
        hora = self.c.hora
        majeurs = self.lec.fichier("Psalterium/Psalmi/Psalmi major")
        if hora == "Vespera" and self.w.get("Ant Vespera"):
            w = self.w["Ant Vespera"]
        elif self.w.get(f"Ant {hora}"):
            w = self.w[f"Ant {hora}"]
        else:
            w = self.proprium(f"Ant {hora}")  # « ex C11 »
        antiennes = w.rstrip("\n").split("\n")
        dominica = re.search("Psalmi Dominica", self.rule, re.I) or re.search(
            "Psalmi Dominica", self.commune.get("Rule", ""), re.I
        )
        if dominica and antiennes and not re.search(r";;\s*[0-9]+", antiennes[0]) and not re.search(
            "Psalmi Feria|Psalmi ex Psalterio", self.rule, re.I
        ):
            p = majeurs["Day0 " + ("Laudes1" if hora == "Laudes" else hora)].rstrip("\n").split("\n")
        else:
            nom = hora + ("1" if hora == "Laudes" else "")
            p = majeurs[f"Day{self.c.dayofweek} {nom}"].rstrip("\n").split("\n")
        psalmi = []
        for i in range(5):
            m = re.search(r";;(.*)", p[i], re.S)
            ps = m.group(1) if m else "missing"
            a = antiennes[i]
            if re.search(r";;[0-9;\n]+", a):
                psalmi.append(a)
            elif ";;" in a:
                psalmi.append(a.split(";;")[0] + ";;" + ps)
            else:
                psalmi.append(f"{a};;{ps}")
        self.antetpsalm(psalmi)

    def capitulum_major(self) -> str:
        nom = "Capitulum Vespera" if self.c.hora == "Vespera" else "Capitulum Laudes"
        capit = self.proprium(nom).rstrip("\n")
        if not capit:
            raise SectionManquante(nom)
        lignes = capit.split("\n")
        lignes[1] = re.sub(r"^(?:[vV]\.\s*)?", "v. ", lignes[1], count=1)
        if not lignes[-1].startswith("$Deo gratias"):
            lignes.append("$Deo gratias")
        return "\n".join(lignes)

    def canticum(self, item: str) -> None:
        self.s.append(self.translate(item))
        cle = 2 if self.c.hora == "Laudes" else self.vespera
        ant = self.antvers("Ant", cle).rstrip("\n")
        self.antetpsalm([f"{ant};;{229 + (2 if self.c.hora == 'Laudes' else 3)}"])

    def oratio(self, item: str) -> None:
        """orationes.pl, sub oratio : prélude, oraison, commémoraison (Laudes et Vêpres)."""
        self.s.append(self.translate(item))
        ind = self.vespera if self.c.hora == "Vespera" else 2
        w = self.w.get("Oratio", "")
        if not w or self.w.get(f"Oratio {ind}"):
            w = self.w.get(f"Oratio {ind}", "")
        if not w:
            i = ind
            w = self.commune.get(f"Oratio {i}") or self.commune.get(f"Oratio {4 - i}") or self.commune.get("Oratio", "")
        if not w:
            raise SectionManquante("Oratio")
        self.s.append("$Kyrie")  # « elsif ($winner =~ /C12/ && $version !~ /19[56]|cist/i) »
        self.s.append("&Dominus_vobiscum")
        self.s.append("v. " + self.translate("Oremus"))
        w = w.rstrip("\n")
        if not re.match(r"^[\$&#/!{]", w):
            w = re.sub(r"^(?:v\. )?", "v. ", w, count=1)
        self.s.append(w)
        if self.c.hora in ("Laudes", "Vespera") and self.w.get("Commemoratio"):
            c = self.w["Commemoratio"].rstrip("\n")
            c = re.sub(r"\$Oremus\s*\n(v\. )?", "$Oremus\nv. ", c)
            if len(self.s[-1]) > 3:
                self.s.append("_")
            self.s.append(c)

    def antiphona_finalis(self) -> None:
        """specials.pl, « Antiphona finalis » (Laudes)."""
        self.s.append("#" + self.translate("Antiphona finalis BMV"))
        m, j, d = self.c.mois, self.c.jour, self.c.dayname0
        if re.search("Adv|Nat", d, re.I) or m == 1 or (m == 2 and j < 2) or (m == 2 and j == 2):
            self.s.append("$ant Alma Redemptoris Mater")
        elif (m in (2, 3) or re.search("Quad", d, re.I)) and not re.search("Pasc", d, re.I):
            self.s.append("$ant Ave Regina caelorum")
        elif "Pasc" in d:
            self.s.append("$ant Regina caeli")
        else:
            self.s.append("$ant Salve Regina")
        self.s.append("&Divinum_auxilium")

    def ordinaire(self) -> list[str]:
        """specials.pl, sub specials : le canevas de l'heure, rubrique par rubrique."""
        t = ordinarium(self.c.hora, self.c)
        sauter = False
        k = 0
        while k < len(t):
            item = t[k].rstrip()
            k += 1
            if not re.match(r"^\s*#", item):
                if not sauter:
                    self.s.append(item)
                continue
            if sauter:
                self.s.append("\n")
            sauter = False
            ite = re.match(r"#(.+?)(\s|$)", item).group(1)
            if re.search(rf"Omit.*? {re.escape(ite)}", self.rule, re.I):
                # « Omit Suffragium mute » : omis sans mention
                sauter = True
                continue
            if re.search("Ave only", self.rule, re.I) and re.search("incipit", item, re.I):
                self.titre(item)
                while k < len(t) and not re.match(r"^\s*#", t[k]):
                    if not re.search("(Pater|Credo)", t[k]):
                        self.s.append(t[k])
                    elif "Ave" in t[k]:
                        self.s.append("$Ave Maria")
                    k += 1
                continue
            if re.search("preces", item, re.I):
                sauter = True  # preces.pl : « return 0 if $winner =~ /C12/i »
                continue
            if re.search("invitatorium", item, re.I):
                self.titre(item)
                self.invitatorium()
                continue
            if re.search("psalm", item, re.I):
                self.titre(item)
                if self.c.hora == "Matutinum":
                    self.psalmi_matutinum()
                else:
                    self.psalmi_major()
                continue
            if re.search("Capitulum", item, re.I) and self.c.hora in ("Laudes", "Vespera"):
                self.titre(item)
                self.s.append(self.capitulum_major())
            if "Hymnus" in item:
                if self.c.hora == "Matutinum":
                    self.titre(item)
                    self.hymnus("Hymnus Matutinum", "")
                else:
                    self.hymnus(f"Hymnus {self.c.hora}", "_\n!" + self.translate("Hymnus"))
                    ind = 2 if self.c.hora == "Laudes" else self.vespera
                    self.s.append("_\n" + self.antvers("Versum", ind).rstrip("\n"))
                continue
            if "Canticum" in item:
                self.canticum(item)
                continue
            if "Oratio" in item:
                self.oratio(item)
                continue
            if re.search("Antiphona finalis", item):
                self.antiphona_finalis()
                continue
            self.titre(item)
        return self.s

    def script(self) -> list[str]:
        if self.c.hora in ("Matutinum", "Laudes", "Vespera"):
            return self.ordinaire()
        special = self.w.get(f"Special {self.c.hora}")
        if not special:
            raise SectionManquante(f"Special {self.c.hora}")
        # specials.pl, sub loadspecial : la première antienne « doublée » est réduite à son intonation
        special = re.sub(r"^(Ant\. .*?) \* .*?$", r"\1", special, count=1, flags=re.M | re.S)
        return special.split("\n")

    # ---- Développement des « $ » et « & » (webdia.pl, sub expand ; horas.pl, sub resolve_refs, adjust_refs)
    def triduum_sans_gloria(self) -> bool:
        return bool(re.search("Quad6", self.c.dayname0, re.I)) and self.c.dayofweek > 3 and self.vespera != 1

    def psalm(self, arg: str) -> list[str]:
        """horasscripts.pl, sub psalm (latin, sans chant)."""
        parts = [a.strip() for a in arg.split(",")]
        num = parts[0].lstrip("-")
        v1 = v2 = None
        if len(parts) >= 3:
            v1, v2 = int(parts[1]), int(parts[2])
        lignes = psaume_brut(num)
        titre = f"Psalmus {num}"
        source = ""
        n = int(re.match(r"\d+", num).group(0))
        if 150 < n < 300 and lignes:
            m = re.match(r"\(?(?P<t>.*?) \* (?P<s>.*?)\)?\s*$", lignes.pop(0))
            titre, source = m.group("t"), m.group("s")
        if v1:
            titre += f"({v1}-{v2})"
            lignes = [l for l in lignes if (m := re.match(r"^(?:\d+:)?(\d+)", l)) and v1 <= int(m.group(1)) <= v2]
        sortie = [f"!{titre}"] + ([f"!{source}"] if source else [])
        for l in lignes:
            l = re.sub(r"^(?:\d+:)?\d+[a-z]?\s*", "", l)  # $nonumbers
            l = re.sub(r"\s*\(\d+[a-z]?\)", "", l)
            l = re.sub(r"(\(.*?\))", r"/:\1:/", l)
            l = re.sub(r"\s‡\s", " † ", l)
            sortie.append(l)
        if n != 210:
            sortie.append("&Gloria")
        return sortie

    def fonction(self, nom: str, args: str) -> list[str]:
        p = self.lec.priere
        if nom == "psalm":
            return self.psalm(args)
        if nom == "Deus_in_adjutorium":
            return p("Deus in adjutorium").rstrip("\n").split("\n")
        if nom == "Alleluia":
            t = p("Alleluia").rstrip("\n").split("\n")
            return [t[1] if re.search("Quad", self.c.dayname0, re.I) else t[0]]
        if nom == "Gloria":
            return [] if self.triduum_sans_gloria() else p("Gloria").rstrip("\n").split("\n")
        if nom == "Gloria1":
            if re.search("Quad5|Quad6", self.c.dayname0, re.I):
                return []
            return p("Gloria1").rstrip("\n").split("\n")
        if nom == "Dominus_vobiscum":
            t = p("Dominus").rstrip("\n").split("\n")
            return [t[2], t[3]]
        if nom == "Benedicamus_Domino":
            t = p("Benedicamus Domino")
            if self.c.hora in ("Laudes", "Vespera") and re.search("Pasc0", self.c.dayname0, re.I):
                alleluia = p("Alleluia Duplex").rstrip("\n").split("\n")[0]
                alleluia = re.sub(r"^v\.\s*", "", alleluia).lower()
                t = re.sub(r"\.\s*\n", lambda _: ", " + alleluia + "\n", t)
            return t.rstrip("\n").split("\n")
        if nom == "teDeum":
            return ["!Te Deum", *p("Te Deum").rstrip("\n").split("\n")]
        if nom == "Divinum_auxilium":
            t = p("Divinum auxilium").rstrip("\n").split("\n")
            t[-2] = f"V. {t[-2]}"
            t[-1] = "R. " + re.sub(r".*\. ", "", t[-1], count=1)
            return t
        if nom == "Domine_labia":
            return p("Domine labia").rstrip("\n").split("\n")
        if nom == "lectio":
            return self.lectio(int(args)).split("\n")
        raise SectionManquante(f"&{nom}")

    def developper(self, lignes: list[str], profondeur: int = 0) -> list[str]:
        if profondeur > 8:
            raise SectionManquante("développement trop profond")
        out: list[str] = []
        for brut in lignes:
            for ligne in brut.split("\n") if brut != "\n" else ["\n"]:
                l = ligne.strip()
                if l.startswith("&Gloria") and l in ("&Gloria",) and self.triduum_sans_gloria():
                    out.append("/:" + self.translate("Gloria omittitur") + ":/")
                    continue
                if re.match(r"&Gloria[12]", l) and re.search("Quad[56]", self.c.dayname0, re.I):
                    out.append("/:" + self.translate("Gloria omittitur") + ":/")
                    continue
                if l[:1] in ("$", "&"):
                    nom = l.replace(".", "")
                    if nom.startswith("$rubrica "):
                        out += self.developper(self.lec.rubrique(nom[9:]).rstrip("\n").split("\n"), profondeur + 1)
                    elif nom.startswith("$"):
                        out += self.developper(self.lec.priere(nom[1:]).rstrip("\n").split("\n"), profondeur + 1)
                    else:
                        m = re.match(r"&(.*?)(?:\((.*)\))?$", nom)
                        out += self.developper(self.fonction(m.group(1), m.group(2) or ""), profondeur + 1)
                else:
                    out.append(ligne)
        return out


# --- Rendu au balisage de l'application ----------------------------------------------------------------------------


def _ligne(l: str) -> str:
    l = re.sub(r"\{:.*?:\}", "", l).strip()
    l = re.sub(r"\[([æaeiou]m?)\]", r"\1", l)  # voyelles muettes des hymnes (italique chez DO)
    l = re.sub(r" (\+{1,3}) ", lambda m: " ✙ " if m.group(1) == "+++" else (" + " if m.group(1) == "++" else " ✠ "), l)
    if l.count("*") > 1:  # deux astérisques sur une ligne : le balisage y verrait de l'italique
        l = l.replace("*", "∗")
    l = re.sub(r"/:(.*?):/", r"[r]\1[/r]", l)
    l = re.sub(r"%(.*?)%", r"\1", l)  # liens de DO vers une autre heure (webdia.pl, activate_links)
    if l.startswith("!"):
        return f"[r]{l.lstrip('!').strip()}[/r]"
    if re.match(r"^[vr]\.\s*", l):
        return re.sub(r"^[vr]\.\s*", "", l)
    m = re.match(r"^(R\.br\.|R\.|V\.|Ant\.|Benedictio\.|Absolutio\.|Responsorium\.)\s*(.*)", l)
    if m:
        tete, reste = m.groups()
        if tete == "Ant." and re.search(r"\w$", reste):
            reste += "."
        tete = {"V.": "℣.", "R.": "℟.", "R.br.": "℟. br."}.get(tete, f"[r]{tete}[/r]")
        return f"{tete} {reste}"
    return l


ALLELUIA = re.compile(r"(?:allelúja|allel[uú][ij]a)", re.I)


def apres(lignes: list[str], c: Contexte) -> list[str]:
    """webdia.pl, sub setcell (texte non chanté) : alléluias entre parenthèses, alléluias du temps de la Septuagésime
    et du Carême, variantes d'orthographe (horascommon.pl, sub spell_var), « _ » et « {:…:} »."""
    texte = "\n".join(lignes)
    if re.search("Pasc", c.dayname0):
        texte = re.sub(r"\((" + ALLELUIA.pattern + r".*?)\)", r" \1 ", texte, flags=re.I | re.S)
    else:
        texte = re.sub(r"\(" + ALLELUIA.pattern + r".*?\)", "", texte, flags=re.I | re.S)
    if re.search(r"Quadp|Quad[1-5]|Quad6-[0-5]", c.dayname0, re.I):
        texte = re.sub(r"[,.]?\s*" + ALLELUIA.pattern, "", texte, flags=re.I)
    texte = texte.replace("Génetrix", "Génitrix").replace("Genetrí", "Genitrí")
    texte = re.sub(r"\bco(t[ií]d[ií])", r"quo\1", texte)
    texte = re.sub(r"\{:.*?:\}", "", texte, flags=re.S)
    return texte.split("\n")


def rendre(lignes: list[str]) -> str:
    """Les lignes développées → paragraphes (ligne vide), intertitres « ### », rubriques [r]…[/r], ℣. ℟."""
    paras: list[list[str]] = [[]]
    fusion = ""
    for brut in lignes:
        l = brut.rstrip()
        if l.endswith("~"):
            fusion += l[:-1].rstrip() + " "
            continue
        if fusion:
            l, fusion = fusion + l.lstrip(), ""
        s = l.strip()
        if s in ("", "_", "\n"):
            paras.append([])
            continue
        if s.startswith("#"):
            paras.append([f"### {s.lstrip('#').strip()}"])
            paras.append([])
            continue
        paras[-1].append(_ligne(s))
    blocs = ["\n".join(p) for p in paras if p and any(x.strip() for x in p)]
    return "\n\n".join(blocs)


# --- Calendrier, génération ---------------------------------------------------------------------------------------


def jours_du_calendrier() -> list[dict]:
    jours = []
    for f in sorted(CALENDRIER.glob("*.json")):
        jours += json.loads(f.read_text(encoding="utf-8"))
    vus, out = set(), []
    for j in sorted(jours, key=lambda x: x["date"]):
        if j["date"] not in vus:
            vus.add(j["date"])
            out.append(j)
    return out


_LECTEURS: dict[tuple, Lecteur] = {}


def lecteur(c: Contexte) -> Lecteur:
    """Un lecteur par signature de condition (tout ce que vero() peut interroger)."""
    bissextile = c.annee % 4 == 0 and (c.annee % 100 != 0 or c.annee % 400 == 0)
    cle = (
        tempus_id(c), dayname_pour_condition(c), c.dayofweek, c.hora, c.mois, bissextile, c.winner,
        "Pasc" in c.dayname0,
    )
    if cle not in _LECTEURS:
        _LECTEURS[cle] = Lecteur(c)
    return _LECTEURS[cle]


def contexte(date: dt.date, hora: str, annonciation: bool) -> Contexte:
    d0 = dayname0(date, hora)
    dow = (date.weekday() + 1) % 7
    winner = fichier_du_petit_office(date.month, date.day, hora, d0, annonciation)
    return Contexte(
        annee=date.year, mois=date.month, jour=date.day, dayofweek=dow, dayname0=d0, hora=hora,
        commune="Commune/C11", votive="C12", winner=winner,
    )


def composer(c: Contexte) -> str:
    h = Heure(c, lecteur(c))
    return rendre(apres(h.developper(h.script()), c))


def fichiers_consultes() -> list[str]:
    out = set()
    for l in _LECTEURS.values():
        out |= l.consultes
    return sorted(out)


def generer() -> dict:
    jours = jours_du_calendrier()
    textes: dict[str, str] = {}  # empreinte → corps
    temps_du_texte: dict[str, set[str]] = {}
    heure_du_texte: dict[str, str] = {}
    index: dict[str, list[str]] = {}
    temps_du_jour: dict[str, str] = {}
    for j in jours:
        date = dt.date.fromisoformat(j["date"])
        annonciation = (j.get("office") or "").startswith("Annonciation")
        empreintes = []
        for cle, _nom, hora, _latin in HEURES:
            c = contexte(date, hora, annonciation)
            corps = composer(c)
            e = hashlib.sha1(f"{cle}\n{corps}".encode()).hexdigest()
            textes[e] = corps
            heure_du_texte[e] = cle
            temps_du_texte.setdefault(e, set()).add(temps_nomme(c.winner, c))
            empreintes.append(e)
            if hora == "Laudes":
                temps_du_jour[j["date"]] = temps_nomme(c.winner, c)
        index[j["date"]] = empreintes
    # identifiants lisibles : heure + temps où le texte est dit
    ordre = list(TEMPS)
    noms: dict[str, str] = {}
    pris: set[str] = set()
    for e in textes:
        base = heure_du_texte[e] + "." + "+".join(sorted(temps_du_texte[e], key=ordre.index))
        n, nom = 1, base
        while nom in pris:
            n += 1
            nom = f"{base}.{n}"
        pris.add(nom)
        noms[e] = nom
    # paragraphes mis en commun (les psaumes reviennent d'une variante à l'autre)
    paragraphes: list[str] = []
    numero: dict[str, int] = {}
    sortie_textes = {}
    for e in sorted(textes, key=lambda x: noms[x]):
        refs = []
        for para in textes[e].split("\n\n"):
            if para not in numero:
                numero[para] = len(paragraphes)
                paragraphes.append(para)
            refs.append(numero[para])
        sortie_textes[noms[e]] = {"temps": sorted(temps_du_texte[e], key=ordre.index), "paragraphes": refs}
    # les jours : une combinaison des huit heures par jour, à la suite depuis le premier jour du calendrier
    combinaisons: list[dict] = []
    rang: dict[tuple, int] = {}
    suite = []
    dates = sorted(index)
    for a, b in zip(dates, dates[1:]):
        if dt.date.fromisoformat(b) - dt.date.fromisoformat(a) != dt.timedelta(days=1):
            raise ValueError(f"calendrier discontinu entre {a} et {b}")
    for d in dates:
        k = (temps_du_jour[d], *(noms[e] for e in index[d]))
        if k not in rang:
            rang[k] = len(combinaisons)
            combinaisons.append({"temps": k[0], "heures": list(k[1:])})
        suite.append(rang[k])
    if len(combinaisons) > len(CHIFFRES):
        raise ValueError("trop de combinaisons pour l'alphabet de « suite »")
    return {
        "titre": "Officium parvum Beatæ Mariæ Virginis",
        "source": {
            **depot(),
            "version": VERSION,
            "note": (
                "Composé par engine/office/parvum.py depuis les fichiers de données de Divinum Officium ; le code Perl "
                "de DO (fichiers « code_lu ») a servi de spécification, il n’est pas exécuté."
            ),
            "fichiers": fichiers_consultes(),
            "code_lu": CODE_LU,
        },
        "heures": [{"cle": k, "nom": n, "latin": lat} for k, n, _h, lat in HEURES],
        "temps": TEMPS,
        "jours": {
            "debut": dates[0],
            "fin": dates[-1],
            "note": "suite : un caractère par jour depuis « debut », rang de la combinaison du jour (« chiffres »)",
            "chiffres": CHIFFRES,
            "combinaisons": combinaisons,
            "suite": "".join(CHIFFRES[i] for i in suite),
        },
        "textes": sortie_textes,
        "paragraphes": paragraphes,
    }


CHIFFRES = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def main() -> None:
    data = generer()
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    taille = SORTIE.stat().st_size
    print(
        f"{SORTIE.relative_to(ROOT)} : {len(data['jours']['suite'])} jours, {len(data['textes'])} textes, "
        f"{len(data['paragraphes'])} paragraphes, {taille // 1024} Kio"
    )


if __name__ == "__main__":
    main()
