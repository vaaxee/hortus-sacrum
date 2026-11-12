# Moteur du calendrier (Python 3)

Le moteur lit les données de Divinum Officium.

1. Cloner le dépôt : `git clone https://github.com/DivinumOfficium/divinum-officium do`.
2. Régler le chemin `B` dans `engine.py` et `enrich.py` (aujourd’hui `/home/claude/do/web/www`).
3. Lancer `python3 build.py`. Il produit `days.json` : l’office, le rang, la couleur et les commémoraisons de chaque jour, du 29 nov. 2026 au 27 nov. 2027 (bornes `START` et `END`).

Les autres fichiers :

- `devo.py` : plan des dévotions et des neuvaines, et jeûne et abstinence selon le CIC de 1917. Les dates y sont codées en dur pour 2026-2027 : à généraliser.
- `enrich.py` : incipit de l’Introït, notices du Martyrologe et entrées du martyrologe du jour.
- `stations.py` : stations romaines tirées du Missale Romanum de 1920. Les dates sont rattachées à Pâques 2027 : à généraliser par rapport à Pâques et à l’Avent.
- `gen.py` : génère la partie semaines du calendrier papier en LaTeX.

Ce code est une base. Il est à réécrire proprement (en TypeScript ou en Python) avec des tests sur 2026-2027.
