# Lot « Dimensions » : la matrice dévotionnelle

Cahier de conception, rédigé le 20 novembre 2026, à placer dans `docs/conception/LOT_DIMENSIONS.md`.
**À ne commencer qu'une fois le lot 4 (bascule de la liste) fusionné dans `main`.** Il ne touche à rien de ce que les
lots 0 à 4 modifient tant qu'ils sont en cours.

**Entrées**
- `docs/conception/REFONTE_2026-11-18.md` (§ 2 programme, § 2.10 réalisé) ;
- SPEC § 10 (cadre pratique : fins, objets, grâces, personnes, pratiques) ;
- `app/src/lib/etiquettes.ts` (étiquettes déduites par motifs, `bilanDuJour`) ;
- `app/src/lib/programme/{types,journee}.ts`, `data/programme/programme.json`.

---

## 1. Objet

Aujourd'hui le programme sait dire **quand** une pratique paraît (`Quand`). Il ne sait pas dire **pourquoi** elle est là,
ni **quelle fonction** elle remplit dans l'économie du jour. Ce lot ajoute cette seconde couche, sans changer la manière
dont la journée est calculée.

Principe directeur, à tenir dans tout le lot :

> **On compose à la conception ; la journée reste fixe à l'exécution.**
> La matrice sert à décrire, vérifier et proposer. Elle ne choisit jamais seule, au lancement de l'app, ce qui sera prié.

Raisons : le test d'unicité sur 365 jours suppose une journée déterministe ; une règle de vie se reçoit et reste stable ;
l'utilisateur doit voir ce qui est dit et pourquoi (« tout doit rester modifiable »).

## 2. Ce qui existe déjà et qu'on reprend

| Existant | Devient |
|---|---|
| `etiquettes.ts`, catégories `fin`, `objet`, `grace`, `personne`, `pratique` | les cinq **dimensions** ; `pratique` est renommée **`forme`** (litanie, chapelet, méditation, office, acte, jaculatoire, examen…) |
| étiquettes **déduites** par expressions régulières | **brouillon** seulement : chaque valeur déduite est marquée `devinee` jusqu'à relecture |
| `Texte.etiquettes?: string[]` (réglage de l'utilisateur, à plat) | lu à la migration, puis remplacé par `Texte.dimensions` (typé) ; l'ancien champ reste lisible |
| `bilanDuJour()` appelé par l'écran du jour | calculé **dans** `journee()` (champ `couverture`) ; l'écran ne fait plus qu'afficher |
| `Quand.semaines_du_mois`, `{ selon: 'quand' }` | suffisent pour le thème de la semaine (§ 4) ; aucun nouveau mécanisme de date |

## 3. Modèle

### 3.1 Vocabulaire fermé

`data/programme/dimensions.json` : la liste des valeurs admises, avec leur libellé et leur ordre d'affichage.

```json
{
  "fin":      ["adoration", "action-de-graces", "reparation", "propitiation", "demande", "intercession", "louange"],
  "objet":    ["trinite", "jesus-christ", "passion", "precieux-sang", "eucharistie", "sacre-coeur", "sainte-face",
               "sainte-vierge", "coeur-immacule", "saint-joseph", "saint-esprit", "anges", "saints", "ames-du-purgatoire"],
  "grace":    ["salut", "perseverance-finale", "sanctification", "charite", "vertus", "preservation-du-peche",
               "protection-et-sante", "devoir-d-etat", "graces-temporelles"],
  "personne": ["soi-meme", "famille", "amis", "ennemis", "pecheurs", "eglise-et-pretres", "dirigeants", "mourants", "defunts"],
  "forme":    ["oraison", "acte", "litanie", "chapelet", "office", "meditation", "lecture", "jaculatoire", "examen",
               "hymne", "neuvaine", "oeuvre"]
}
```

La liste est une donnée : l'utilisateur peut l'étendre dans l'app (ajout personnel), jamais en supprimer une valeur
livrée utilisée par un texte.

Distinctions à respecter (ne jamais les fusionner) :
- **fin** : ce que fait la prière (adorer, rendre grâce, réparer, demander…) ;
- **objet** : à qui ou à quoi elle s'adresse (Trinité, Sacré-Cœur, saint Joseph…) ;
- **grâce** : ce qui est demandé ;
- **personne** : pour qui l'on prie ;
- **forme** : sous quelle forme (litanie, chapelet, méditation…).

Les **intentions particulières** de l'utilisateur (« conversion de la France ») ne sont pas une dimension des textes :
elles restent le champ libre de la prière du matin, et peuvent tourner par une roue (§ 4.3).

### 3.2 Sur les textes

`data/prieres/dimensions-textes.json` (fichier séparé : on ne réécrit pas `sources.json`) :

```json
{
  "beringer:litanies-saint-joseph": {
    "fin": ["louange", "demande"], "objet": ["saint-joseph"], "forme": ["litanie"],
    "releve": "2026-11-21"
  },
  "jardin:chaque-vendredi-devant-le-crucifix": {
    "fin": ["reparation", "propitiation"], "objet": ["passion"], "forme": ["oraison"],
    "devinee": ["fin"]
  }
}
```

- `releve` : date de relecture humaine ; sans elle, toutes les valeurs comptent comme devinées ;
- `devinee` : dimensions encore issues des motifs de `etiquettes.ts`, affichées en gris dans la fiche ;
- un réglage de l'utilisateur (surcouche Dexie, comme aujourd'hui) remplace la donnée livrée, dimension par dimension.

Type, dans `app/src/lib/programme/types.ts` :

```ts
export type Dimension = 'fin' | 'objet' | 'grace' | 'personne' | 'forme';
export type Dimensions = Partial<Record<Dimension, string[]>>;
```

Ce sont des **classements**, pas des textes : la règle « rien de mémoire » ne s'y applique pas au sens strict, mais
chaque classement livré doit être relu (champ `releve`) avant d'entrer dans un test bloquant.

### 3.3 Sur les entrées du programme

Un champ **descriptif**, sans effet sur le calcul :

```ts
interface EntreeProgramme {
	// …
	/** Pourquoi cette entrée est là : fonction dans l'économie du jour. Ne filtre rien. */
	motif?: { fins?: string[]; objets?: string[]; note?: string };
}
```

Exemple, `prog:devotion-vendredi` : `motif: { fins: ["reparation", "propitiation"], objets: ["passion"] }`.
Les dimensions de l'entrée se **calculent** aussi à partir de ses textes ; `motif` dit l'intention de l'auteur, et un test
vérifie que les deux ne se contredisent pas (§ 5).

## 4. Cycles dévotionnels

Le calendrier liturgique (temporal, sanctoral, ordinaire) reste celui de `data/calendar`. Les cycles dévotionnels sont
déclarés à part, dans `data/programme/cycles.json`, et ne font que **qualifier** le jour :

```json
{
  "jour_semaine": { "0": { "objets": ["trinite"] }, "1": { "objets": ["ames-du-purgatoire"] }, "2": { "objets": ["anges"] },
                    "3": { "objets": ["saint-joseph"] }, "4": { "objets": ["eucharistie"] }, "5": { "objets": ["passion"] },
                    "6": { "objets": ["sainte-vierge"] } },
  "mois": { "3": { "objets": ["saint-joseph"] }, "6": { "objets": ["sacre-coeur"] }, "7": { "objets": ["precieux-sang"] },
            "9": { "objets": ["sainte-vierge"], "note": "Sept Douleurs" }, "11": { "objets": ["ames-du-purgatoire"] } },
  "semaine_du_mois": { "1": { "fins": ["action-de-graces"] }, "2": { "fins": ["reparation"] },
                       "3": { "fins": ["demande"] }, "4": { "fins": ["intercession"] } }
}
```

**Les valeurs de `semaine_du_mois` ci-dessus sont un exemple, pas une décision** : question 1 (§ 8).

### 4.1 Contexte du jour

`journee()` reçoit déjà le jour liturgique. Il calcule en plus un `contexte` lisible :

```ts
interface ContexteDevotionnel {
	temps: string;            // temporal (« Temps du Carême »)
	sanctoral?: string;       // fête ou saint du jour, catégorie (gertrude.ts)
	objets: string[];         // réunion : jour de semaine, mois, fête, pratiques du plan en cours
	fins: string[];           // thème de la semaine du mois, temps (Carême → réparation)
	sources: { dimension: Dimension; valeur: string; de: string }[]; // traçabilité : « passion ← vendredi »
}
```

### 4.2 Ce que le contexte fait, et ne fait pas

- il **est affiché** (une ligne sous la date : « Vendredi · Passion · semaine de réparation ») ;
- il **sert aux tests** (§ 5) et au **compositeur** (§ 6) ;
- il **ne retire ni n'ajoute** aucune ligne. Ce qui varie selon la semaine ou le mois s'écrit, comme aujourd'hui, en
  `{ selon: 'quand' }` ou en section `quand` dans `programme.json`.

### 4.3 Roues

Les roues restent ce qu'elles sont (`rotation`). Une roue peut déclarer la dimension qu'elle nourrit
(`"nourrit": "objet"` pour la roue des mystères, `"personne"` pour une roue des intentions) : son élément du jour entre
alors dans le `contexte`.

## 5. Sortie de `journee()` et tests

`Journee` reçoit :

```ts
couverture: Record<Dimension, { valeur: string; par: string[] }[]>; // valeur couverte ← ids des lignes
manques: { dimension: Dimension; valeur: string; proposition?: string }[]; // reprise de bilanDuJour
contexte: ContexteDevotionnel;
```

Le bilan affiché sur Aujourd'hui lit `couverture` et `manques` ; `bilanDuJour` est retiré de l'écran.

**Tests de matrice** (`app/src/lib/programme/matrice.test.ts`, même année que `unicite.test.ts`) :
1. chaque texte du programme a des dimensions déclarées ; tant que `releve` manque, le test **avertit** sans bloquer ;
2. chaque valeur citée existe dans `dimensions.json` ;
3. chaque jour, les `objets` du contexte sont couverts par au moins une ligne (le vendredi a un texte sur la Passion) ;
4. chaque semaine couvre les cinq fins principales (adoration, action de grâces, réparation, demande, intercession) ;
5. le `motif` d'une entrée est compatible avec les dimensions de ses textes (au moins une fin commune) ;
6. le thème de la semaine du mois, s'il est adopté, est **dominant** cette semaine-là (plus de lignes qui portent cette fin
   que les autres semaines). Ce test reste désactivé tant que la question 1 n'est pas tranchée.

Les tests 3 à 6 ne modifient rien : ils signalent un trou dans `programme.json`, que l'on comble à la main ou avec le
compositeur.

## 6. Le compositeur (hors ligne, lot suivant)

`engine/ordo/composer.py` (Python, comme les autres moteurs ; ne remplace pas `engine/composer/`, qui disparaît au
lot 6) :

- entrée : un jour ou une période, le contexte (§ 4.1), `programme.json`, les dimensions des textes ;
- sortie : un **rapport** (`docs/audits/ORDO_<période>.md`) : manques par jour, et pour chacun des textes candidats
  déjà dans la bibliothèque, classés par dimensions communes, forme voulue, durée, sans doublon avec la journée ;
- l'utilisateur choisit ; la décision est écrite dans `programme.json` avec `source: "ordo <date> : …"`.

Le compositeur **n'écrit jamais lui-même** dans `programme.json`, et ne propose que des textes déjà sourcés.

## 7. Lots

| Lot | Contenu | Fichiers | Risque | Tests | Dépend de |
|---|---|---|---|---|---|
| **D1. Vocabulaire et classement** | `dimensions.json` ; `dimensions-textes.json` prérempli par les motifs (`devinee`), pour les seuls textes du programme ; types `Dimension`, `Dimensions` ; renommage `pratique` → `forme` dans `etiquettes.ts` (correspondance gardée pour les réglages existants) | `data/programme/`, `data/prieres/dimensions-textes.json`, `lib/etiquettes.ts`, `lib/programme/types.ts`, `scripts/seed.mjs` | faible | tests 1-2 ; `etiquettes.test.ts` inchangé dans ses résultats | lot 4 |
| **D2. Relecture** | relecture humaine des classements, texte par texte, dans la fiche (`FicheTexte.svelte` : cinq rangées de pastilles, valeurs devinées en gris, « Relu ») | `lib/FicheTexte.svelte`, surcouche Dexie | faible | réglage utilisateur prioritaire ; migration de `Texte.etiquettes` | D1 |
| **D3. Contexte et couverture** | `cycles.json` ; `contexte`, `couverture`, `manques` dans `journee()` ; ligne de contexte sous la date ; bilan lu de `journee()` | `data/programme/cycles.json`, `lib/programme/journee.ts`, `routes/+page.svelte` | moyen : `+page.svelte` | `journee.test.ts` (vendredi → passion, juillet → précieux sang, traçabilité) ; tests 3-5 | D1 |
| **D4. Motifs** | `motif` sur chaque entrée de `programme.json` | `data/programme/programme.json` | faible | test 5 | D3 |
| **D5. Compositeur** | `engine/ordo/composer.py`, rapport | `engine/ordo/` | faible (n'écrit pas dans les données) | rapport sur l'Avent 2026 : aucun candidat déjà dit ce jour-là | D3 |

Chaque lot se termine comme les autres : lint, `check`, tests, build, revue critique, audit des consignes.

## 8. Questions pour l'utilisateur

1. **Thème de la semaine du mois** : l'adopter ? Avec quelle correspondance (I action de grâces, II réparation,
   III demande, IV intercession est un exemple) ? Que faire de la 5e semaine (jours 29-31) ? *Par défaut : non adopté ;
   le test 6 reste désactivé.*
2. **Fins** : garder les cinq de la SPEC, ou ajouter `propitiation` et `louange` comme valeurs distinctes ?
   *Par défaut : ajoutées, mais seules les cinq de la SPEC comptent pour le test 4.*
3. **Temps liturgique → fins** : le Carême et le temps de la Passion qualifient-ils le jour en « réparation »,
   le temps pascal en « action de grâces » ? *Par défaut : oui, dans `cycles.json`, modifiable.*
4. **Roue des intentions** (personnes et causes qui tournent par jour) : la créer ? *Par défaut : non.*
