# Hebdomada in Dei servitio

Compagnon quotidien de prière (PWA), selon le calendrier romain de 1954 et le livret
*Le Jardin de l'âme*. Cahier des charges : `docs/cahier/`.

## Arborescence
| Dossier | Contenu |
|---|---|
| `engine/hebdo/` | moteur du calendrier (Python 3) : `liturgy` (temps, précédence), `fasting` (CIC 1917), `stations`, `enrich` (Introït, Martyrologe), `devotions` (séries, neuvaines, Montfort), `build` |
| `engine/livret/extract.py` | extraction des textes du livret → `data/prieres/jardin.json` |
| `engine/tests/compare_2026.py` | contrôle du moteur contre le calendrier papier 2026-2027 |
| `data/calendar/` | années générées (`AAAA-AAAA.json`) |
| `data/plans/` | plans de dévotions acceptés (prioritaires sur le planificateur) |
| `data/prieres/` | base de prières |
| `data/source/` | données d'origine (calendrier 2026-2027, index du livret) |
| `docs/` | livret, calendrier papier, notes de sources, charte, `LISTE_DU_JOUR.md` |
| `engine/legacy/` | ancien moteur 2026-2027, gardé pour référence |

## Générer une année
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/DivinumOfficium/divinum-officium vendor/do
cd vendor/do && git sparse-checkout set web/www/Tabulae web/www/horas web/www/missa && cd ../..
cd engine && python -m hebdo.build 2027 2028
python tests/compare_2026.py      # doit afficher « 0 écart(s) »
```

`AAAA` = année du premier dimanche de l'Avent : `2026` produit l'année liturgique 2026-2027.
