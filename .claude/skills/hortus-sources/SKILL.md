---
name: hortus-sources
description: Règles de provenance des textes d'Hortus Sacrum. À charger AVANT d'ajouter, corriger, citer ou chercher tout texte religieux (prière, méditation, vie de saint, indulgence, litanie, traduction), toute recherche web de source, et toute mise à jour de SOURCES_UTILISEES.md ou A_FOURNIR.md.
---

# Hortus Sacrum — sources

Références qui font foi (les relire, elles priment sur ce résumé) : `docs/REPRISE.md` (« Règles absolues »),
`docs/PLAN_GENERAL.md` (« Consignes communes »), `SOURCES_UTILISEES.md`, `A_FOURNIR.md`, `docs/cahier/SPEC.md` § 6, § 10, § 11.

## Règle absolue

**Aucun** texte de prière, méditation, vie de saint ou indulgence écrit de mémoire, reconstitué, traduit ou complété par
le modèle. Seulement des sources anciennes identifiées, recopiées **mot pour mot**, orthographe de l'édition gardée.
Texte introuvable → une entrée dans `A_FOURNIR.md` (sujet, ce qui a été cherché, pistes) et rien dans les données.

## Provenance admise

| Cas | Admis |
|---|---|
| Recueils, méditations, manuels | éditions anciennes (antérieures à 1955, domaine public) : archive.org, Gallica, Google Livres, bibliotheque-catholique.com (`docs/notes_sources/inventaire_bibliotheque_catholique.md`) |
| Prières courantes | sites sédévacantistes ou FSSPX (La Porte Latine…), Catholique de France |
| Exception nommée | Guéranger, *L'Année liturgique*, transcription de l'abbaye Saint-Benoît de Port-Valais (domgueranger.net) |
| Liturgie | Divinum Officium (version « Divino Afflatu - 1954 »), Missel typique 1920, Martyrologe |
| Écriture | Crampon 1923 (Wikisource relu), Vulgate clémentine |
| Fourni par l'utilisateur | gardé avec sa source exacte ; source ancienne à trouver si le site est hors liste |

**Bannis, ne jamais utiliser ni citer** : Hozana, Aleteia, Notre-Dame de Chrétienté.
Le Petit Sacristain : lien seulement, jamais recopié (SPEC § 6), sauf textes explicitement donnés par l'utilisateur.

## Indulgences (SPEC § 11, décision du 19 nov.)

- Seule l'*Enchiridion indulgentiarum* de **1952** fait foi pour le compte ; les concessions générales absentes sont abrogées.
- Confréries, objets bénits, lieux : signalés, non comptés.
- Traduction française indulgenciée seulement si déclarée fidèle (can. 934 § 2) : Beringer 1925 quand il rend la formule
  de 1952 mot pour mot (hymnes en vers exclus), *Thésaurisons pour le ciel* 1941, Pater/Ave/Gloria usuels.
  Sinon : **latin d'abord**, français en regard, note du can. 934.
- Données : `data/prieres/indulgences.json` ; scripts `engine/indulgences/*`.

## Chaque texte ajouté porte

`source: { ouvrage, edition, page, url }` dans `data/prieres/sources.json` (ou le recueil), et une ligne dans
`SOURCES_UTILISEES.md` (texte, source, pages, accès). Une correction d'un texte livré **incrémente `revision`** : l'app
le remplace seulement si l'utilisateur ne l'a pas modifié.

## Recherche web

- Outils : `mcp__Parallel_Search__web_search` / `web_fetch` (ou WebSearch) pour trouver une **édition** ; archive.org
  (`https://archive.org/advancedsearch.php`, `…/download/<id>/<id>_djvu.txt`) pour le texte ; Context7 pour la doc
  technique uniquement.
- La recherche sert à **localiser et vérifier** une édition, jamais à produire un texte. Un extrait trouvé sur un site
  récent ne remplace pas la lecture du scan.
- Noter dans `A_FOURNIR.md` ce qui a été cherché et où, même sans résultat.

## Avant de conclure

Audit des consignes (PLAN_GENERAL) : grep des sites bannis, textes sans `source`, secrets, textes de mémoire.
`grep -rniE "hozana|aleteia|chr[ée]tient[ée]" data docs app/src` doit ne rien renvoyer d'autre que les règles elles-mêmes.
