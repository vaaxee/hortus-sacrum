---
name: hortus-liturgie
description: Offices et textes liturgiques d'Hortus Sacrum (Bréviaire romain d'avant 1955, Officium parvum B.M.V., Petit bréviaire du Sacré-Cœur, leçons du Bréviaire, Martyrologe et invocations, Introït, Guéranger). À charger pour tout travail dans engine/office, engine/recueils/breviaire*, data/office, Lecture › Office, la page du saint ou les invocations du Martyrologe.
---

# Hortus Sacrum — liturgie et office

Références : `docs/conception/REFONTE_2026-11-18.md` § 5 (format DO, import hors ligne, sortie), § 6 lots 8-9 ;
`docs/cahier/SPEC.md` § 1, § 5, § 10-11 ; skill `hortus-calendar` (épinglage de `vendor/do`).

## Décisions fixées

- Rubriques **d'avant 1955** : version DO « Divino Afflatu - 1954 » (`rubrica 1955 … omittitur` gardé) ; ni 1955 ni 1960.
- **Résolution hors ligne en Python** (`engine/office/lire.py`, `parvum.py`, futur `heures.py`), sortie JSON livrée
  (`data/office/…`) : pièces partagées + plan léger par jour, chargé à la demande. Pas de moteur d'office dans l'app.
- **Latin d'abord.** Le français seulement quand sa source ancienne est identifiée ; les fichiers `Francais` de DO ne
  disent pas leur édition → Bréviaire romain en latin seul tant qu'une édition bilingue ancienne n'est pas trouvée.
- Composants communs réutilisés (psaumes, hymnes, prières `$Pater noster`…), jamais recopiés 365 fois.
- Office compté dans « Lectures du jour » : le Petit bréviaire du Sacré-Cœur ; Bréviaire romain et Officium parvum
  proposés sans être comptés. Aucun rappel aux heures canoniales par défaut.
- Leçons IV-VI du sanctoral : rubriques de 1911, leçon abrégée de 1960 écartée (`data/recueils/breviaire.json`).
- Martyrologe : lu la veille à Prime (vue « lecture de Prime ») ; invocations françaises générées au vouvoiement ;
  invocations latines chantées **sans le lieu** (sauf « Sancta Barbara, virgo Nicomediæ… ») ; contrôle
  `app/scripts/controle-martyrologe.mjs`, `martyrologe-controle.test.ts`.
- Fin de l'office du saint : prière de sainte Gertrude selon la catégorie du saint (`gertrude.ts`, `selon: 'saint_du_jour'`).

## Bréviaire romain (lot 9, fait)

`engine/office/breviaire.py <année>` exécute le moteur Perl de DO (`vendor/do/web/cgi-bin/horas/officium.pl`) : ne pas
réécrire de rubriques. Prérequis : `perl`, `apt-get install -y libcgi-pm-perl`, `git sparse-checkout add web/cgi-bin`
dans `vendor/do`. Sortie `data/office/breviaire/<AAAA-AAAA>/` ; chargeur `app/src/lib/office/breviaire.ts`
(`ANNEES_CALCULEES` à compléter pour une nouvelle année).

## Contrôles

```bash
python3 engine/office/test_parvum.py        # « 93 textes vérifiés, témoins des temps conformes »
python3 engine/office/test_breviaire.py     # 0 faute, 0 écart d'oraison (calendrier ↔ moteur DO)
cd app && npx vitest run src/lib/programme/heures.test.ts
```

Le témoin du Bréviaire est croisé : l'oraison de l'office de notre calendrier doit se retrouver dans les Laudes de DO,
chaque jour de l'année.

## Interdits

Pas de traduction faite par le modèle ; pas de rubrique « simplifiée » ; pas de second lecteur DO (réutiliser `do.py` /
`lire.py`) ; pas de modification de la précédence sans passer par `hortus-calendar`.
