"""Brouillon de transcription d'un passage d'un livre scanné (couche texte, pdftotext -layout).
Usage : python3 -I brouillon.py <pdf> <première page du PDF> <dernière page du PDF> [lignes d'en-tête à sauter]
Sortie : texte en paragraphes (retrait = nouveau paragraphe), titre courant et numéros de page retirés, mots coupés
en fin de ligne recollés, et un repère « [[PDF n]] » au début de chaque page.
Ce brouillon n'est pas le texte publié : il est relu et corrigé à l'œil sur l'image de chaque page
(pdftoppm -r 110), et le texte relu est rangé dans un fichier .md à côté, d'où `inserer.py` le copie."""
import re, subprocess, sys

PDF, A, B = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
SAUT = int(sys.argv[4]) if len(sys.argv) > 4 else 1
COMPOSE = r"(?:même|mêmes|moi|toi|nous|vous|lui|leur|les|la|le|ci|là|puissant|y|en|t-il|t-elle|il|elle|je|on)\b"
REPERE = r"(\s*\n\[\[PDF \d+\]\]\n\s*\n)?\s*"

lignes = []
for p in range(A, B + 1):
    t = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), PDF, '-'],
                       capture_output=True, text=True).stdout
    L = [l.rstrip() for l in t.split('\n') if l.strip()]
    L = L[SAUT:]  # titre courant et numéro de page
    if L and re.fullmatch(r"\s*[\dIlO]{1,3}\s*", L[-1]):
        L = L[:-1]
    if not L:
        continue
    base = min(len(l) - len(l.lstrip()) for l in L)
    lignes += ['', f'[[PDF {p}]]', '']
    for l in L:
        s = l.strip()
        if re.fullmatch(r"[A-Z]\. ?S\.-?C\.\s*[\dIlO]*|[\dIlO]{1,3}", s):
            continue
        if len(l) - len(l.lstrip()) - base >= 2:
            lignes.append('')
        lignes.append(s)
texte = '\n'.join(lignes)


def recolle(m, trait):
    rep = (m.group(2) or '').strip()
    return m.group(1) + trait + m.group(3) + (' ' + rep + ' ' if rep else '')


texte = re.sub(r"(\w)-\n" + REPERE + "(" + COMPOSE + ")", lambda m: recolle(m, '-'), texte)
texte = re.sub(r"(\w)-\n" + REPERE + "([a-zàâçéèêëîïôûùüœ])", lambda m: recolle(m, ''), texte)
paras = [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", texte)]
paras = [re.sub(r"\s{2,}", " ", p) for p in paras if p]
texte = '\n\n'.join(paras)
texte = re.sub(r" ([,.)])", r"\1", texte)
print(texte)
