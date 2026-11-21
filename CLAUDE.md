# CLAUDE.md

## 1. Rôle

Tu travailles sur Hortus Sacrum (Hebdomada in Dei servitio), application PWA de prière quotidienne fondée sur le
calendrier romain de 1954, les sources liturgiques traditionnelles et des ouvrages de piété anciens identifiés.

Tu es l'agent d'implémentation du projet.

Le dépôt Git est la source de vérité du projet. Les décisions déjà documentées dans le dépôt priment sur toute
reconstruction personnelle du projet.

Tu dois travailler par évolution incrémentale, jamais par réécriture arbitraire.

---

## 2. Ordre de lecture obligatoire

Avant toute modification substantielle, lire :

1. docs/REPRISE.md
2. docs/PLAN_ETAPES.md
3. docs/LISTE_DU_JOUR.md
4. SOURCES_UTILISEES.md
5. A_FOURNIR.md
6. docs/cahier/SPEC.md
7. docs/conception/REFONTE_2026-11-18.md
8. docs/conception/LOT_DIMENSIONS.md
9. les audits pertinents dans docs/audits/
10. le code réellement concerné par la tâche.

Ne jamais supposer qu'une ancienne description du projet est encore exacte : vérifier l'état de main.

Les PR et commits antérieurs sont utiles pour comprendre les décisions, mais le code et la documentation actuellement
présents dans main constituent l'état de référence.

Outillage du projet : skills `.claude/skills/hortus-*` (sources, liturgie, ordo, dimensions, calendar, content, ocr,
qa) et sous-agents `.claude/agents/hortus-*` (architecte, frontend, qa, sources, liturgie). Les charger selon la tâche.

---

## 3. Architecture actuelle à préserver

Hortus Sacrum possède désormais une architecture de programme unique.

Le programme est livré comme donnée et la journée est calculée par :

```
journee(date, contexte)
```

La journée n'est pas une liste statique stockée en base.

Le principe actuel est :

```
programme livré
        ↓
contexte du jour
        ↓
journee(date, contexte)
        ↓
résolution des règles
        ↓
pages / sections / insertions
        ↓
liste du jour
```

Préserver cette architecture.

Ne pas revenir à une succession de migrations dans seed.ts.

Ne pas recréer une liste quotidienne persistée lorsque le système sait déjà la calculer.

Ne pas supprimer journee() pour introduire un nouveau moteur concurrent.

---

## 4. La matrice dévotionnelle existe déjà

Le projet possède désormais une première matrice dévotionnelle.

Les dimensions actuelles sont :

- fin
- objet
- grâce
- personne
- forme

Elles sont définies dans data/programme/dimensions.json et utilisées par le système de classement des textes.

Le système actuel doit être considéré comme la base officielle de la future matrice.

Ne pas créer un second système de tags ou de dimensions parallèle.

Toute extension de la matrice doit prolonger les types, vocabulaires, chargeurs, tests et mécanismes existants.

---

## 5. Distinction fondamentale des dimensions

Ne pas confondre :

### Fin

Ce que l'acte cherche à accomplir :

- adoration
- louange
- action de grâces
- demande
- intercession
- propitiation
- réparation
- expiation
- contrition
- satisfaction
- offrande
- etc.

### Objet

Ce vers quoi porte l'acte :

- Dieu
- Trinité
- Jésus-Christ
- Passion
- Sacré-Cœur
- Très Saint Sacrement
- Précieux Sang
- Sainte Vierge
- Cœur Immaculé
- saint Joseph
- un saint
- anges
- âmes du Purgatoire
- etc.

### Personne

Pour qui ou en faveur de qui l'acte est offert :

- soi-même
- famille
- enfants
- époux/épouse
- prêtres
- vocations
- conversion
- Église
- France
- défunts
- personne particulière
- etc.

### Forme

La manière concrète dont l'acte est accompli :

- oraison
- méditation
- prière vocale
- litanie
- chapelet
- office
- lecture
- examen
- acte
- jeûne
- abstinence
- aumône
- œuvre de miséricorde
- visite
- communion
- etc.

### Grâce

Conserver le sens actuellement défini par le projet. Ne pas renommer ou fusionner cette dimension avec une autre sans
décision explicite.

---

## 6. Ne pas confondre calendrier et thème

Le numéro de semaine du mois et le thème de la semaine sont deux choses différentes.

Exemple :

```
semaine_du_mois = 3
theme_semaine = réparation
```

Le premier est une propriété calendaire.

Le second est une dimension dévotionnelle.

Ne jamais les fusionner.

Le thème de la semaine du mois n'est actuellement pas adopté dans cycles.json. Ne pas l'activer spontanément : il faut
d'abord une décision explicite et une source/conception correspondante.

---

## 7. Dimensions temporelles

Le système doit pouvoir distinguer indépendamment :

- date civile
- année liturgique
- jour de la semaine
- semaine du mois
- mois
- temps liturgique
- tempora
- sanctoral
- propre
- office
- fêtes
- cycles dévotionnels
- roues
- pratiques personnelles
- consécrations.

Une dimension nouvelle doit être ajoutée comme dimension indépendante lorsqu'elle possède une sémantique propre.

Ne pas transformer toutes les dimensions en simples chaînes de caractères ou en tags génériques.

---

## 8. Principe de composition

L'objectif à long terme est de pouvoir représenter :

```
CONTEXTE DU JOUR
        ↓
FACTEURS ACTIFS
        ↓
RÈGLES DE COMPOSITION
        ↓
ACTIONS CANDIDATES
        ↓
PRIORITÉS / CONFLITS / COMPLÉMENTARITÉS
        ↓
ORDO DU JOUR
```

Mais ce principe doit être introduit progressivement.

La matrice ne doit pas devenir un système opaque qui décide arbitrairement des prières à afficher.

Une règle doit être traçable :

```
action
→ pourquoi elle est active
→ quelles dimensions la justifient
→ quelle source ou décision l'établit
→ quelle priorité elle possède
→ avec quoi elle est compatible ou redondante
```

Le contexte doit pouvoir expliquer une décision.

---

## 9. Déterminisme

Le programme quotidien doit rester déterministe.

Pour une date et un contexte identiques :

```
journee(date, contexte)
```

doit produire le même résultat.

Ne pas introduire de sélection aléatoire dans la journée sans mécanisme explicitement conçu, documenté et testé.

Les roues et rotations existantes doivent être traitées comme des dimensions/règles déterministes du programme, pas
comme un hasard libre.

---

## 10. Unicité

Une même prière ou un même texte ne doit pas apparaître deux fois dans la journée sans raison explicitement déclarée.

Le test d'unicité existant doit continuer à protéger cette règle.

Toute nouvelle composition doit être testée sur l'ensemble de l'année liturgique pertinente.

Ne jamais corriger un doublon simplement en masquant une ligne à l'interface : corriger la cause dans la composition.

---

## 11. Programme, textes et compositions

Une pratique est déclarée une seule fois.

Les pages peuvent être composées de :

- textes entiers ;
- extraits ;
- sections ;
- points d'insertion ;
- contenus conditionnels ;
- rotations ;
- textes du jour.

Le texte religieux lui-même ne doit jamais être réécrit pour des raisons de mise en page.

La présentation est séparée du contenu sourcé.

Les pages composées à l'affichage doivent continuer à être couvertes par des tests mot pour mot lorsque le projet
l'exige.

---

## 12. Surcouche utilisateur

Les données livrées par le projet et les réglages de l'utilisateur sont distincts.

Une correction livrée ne doit pas écraser une modification explicitement effectuée par l'utilisateur.

Inversement, une modification de classement/dimension ne doit pas automatiquement faire considérer le texte comme
entièrement modifié si le système actuel prévoit qu'il puisse continuer à recevoir des corrections éditoriales.

Respecter les mécanismes existants de :

- revision
- surcouche utilisateur
- migration unique
- archivage
- restauration
- réglages personnels.

Ne jamais écrire une migration destructive sans protection.

---

## 13. Sources religieuses

Règle absolue :

aucun texte de prière, méditation, vie de saint ou indulgence ne doit être inventé ou reconstitué de mémoire.

Utiliser uniquement les sources anciennes identifiées par le projet.

Pour chaque texte :

- source ;
- ouvrage ;
- édition ;
- page ou numéro lorsque disponible ;
- provenance vérifiable.

Si le texte demandé est introuvable :

→ l'ajouter à A_FOURNIR.md.

Ne jamais combler silencieusement un manque par un texte moderne ou généré.

Respecter les interdictions et préférences documentées dans docs/REPRISE.md.

---

## 14. Calendrier liturgique

Le calendrier romain de référence du projet est celui défini dans le cahier des charges et les données existantes.

Ne pas modifier une règle liturgique simplement parce qu'une autre tradition paraît plus pratique.

Toute modification du calendrier, de la précédence, des Quatre-Temps, stations, jeûnes, vigiles ou offices doit être :

1. documentée ;
2. sourcée ;
3. testée ;
4. compatible avec les données existantes.

---

## 15. Bréviaire et Office

Le Bréviaire romain et l'Officium parvum sont désormais intégrés dans l'architecture.

Leur traitement suit les décisions existantes :

- résolution hors ligne lorsque prévu ;
- sources Divinum Officium ;
- latin prioritaire ;
- français uniquement lorsqu'une source ancienne approuvée est disponible ;
- composants communs réutilisables ;
- tests mot pour mot lorsque requis.

Ne pas réinventer un moteur parallèle.

---

## 16. Règles de développement

Avant une modification architecturale :

1. examiner le code existant ;
2. examiner le graphe si nécessaire ;
3. identifier les dépendances ;
4. vérifier les documents de conception ;
5. déterminer si la fonctionnalité existe déjà partiellement ;
6. proposer la migration minimale ;
7. préserver les données existantes ;
8. écrire ou mettre à jour les tests ;
9. seulement ensuite modifier le code.

Pour une refonte importante, utiliser graphify comme prévu par les documents du projet.

---

## 17. Ne pas faire

Ne pas :

- repartir de zéro ;
- supprimer une architecture fonctionnelle parce qu'une autre semble plus élégante ;
- créer un deuxième système de dimensions ;
- créer un deuxième moteur de calendrier ;
- créer un deuxième système de règles Quand ;
- déplacer arbitrairement les données dans une nouvelle base ;
- remplacer les textes sourcés par des textes générés ;
- écraser les modifications utilisateur ;
- modifier une décision théologique ou liturgique silencieusement ;
- introduire une abstraction générale sans vérifier son impact sur le système actuel.

---

## 18. Tests obligatoires

Après toute modification substantielle :

```
npm run check
npm run lint
npm run test
npm run build
```

et les tests Python concernés lorsque le moteur Python est touché.

Pour les modifications d'interface ou de parcours :

- Playwright (`npm run test:e2e`, après `npm run build`) ;
- vérification clair/sombre si pertinent ;
- vérification mobile ;
- contrôle de la console.

Pour le calendrier :

```
python tests/compare_2026.py
```

doit rester conforme lorsque le changement concerne le moteur correspondant (`vendor/do` épinglé au commit `454a86ea` :
voir `.claude/skills/hortus-calendar`).

---

## 19. Git

Ne jamais réécrire l'historique de main.

Ne jamais faire de force push.

Travailler dans une branche dédiée lorsque le travail est destiné à une PR.

Une PR doit avoir :

- un titre explicite ;
- un périmètre clair ;
- les tests effectués ;
- les décisions importantes documentées ;
- les fichiers de conception mis à jour si l'architecture change.

Ne pas fusionner plusieurs travaux sans rapport simplement pour réduire le nombre de PR.

---

## 20. Documentation vivante

Lorsque le comportement ou l'architecture change, mettre à jour le document correspondant.

En particulier :

- docs/REPRISE.md pour les décisions de reprise ;
- docs/conception/REFONTE_2026-11-18.md pour la refonte ;
- docs/conception/LOT_DIMENSIONS.md pour la matrice ;
- A_FOURNIR.md pour les contenus manquants ;
- SOURCES_UTILISEES.md pour les sources ;
- les audits lorsque le travail répond à un audit.

La documentation doit refléter le code réellement présent dans main.

---

## 21. Priorité des décisions

En cas de contradiction :

1. décision explicite récente de l'utilisateur ;
2. cahier des charges / SPEC ;
3. documents de conception actuels ;
4. docs/REPRISE.md ;
5. code actuel ;
6. anciennes PR et anciens commits ;
7. interprétation personnelle.

Une ancienne PR ne constitue pas à elle seule une autorisation de revenir à son architecture.

---

## 22. Principe général

Hortus Sacrum n'est pas seulement une liste de prières.

C'est un système qui doit progressivement être capable de représenter :

```
CALENDRIER LITURGIQUE
        +
CYCLES DÉVOTIONNELS
        +
DIMENSIONS SÉMANTIQUES
        +
PRATIQUES PERSONNELLES
        +
CONSÉCRATIONS
        +
RÈGLES DE COMPOSITION
        ↓
ORDO QUOTIDIEN
```

Mais cette évolution doit être incrémentale, déterministe, sourcée, testable et réversible.

Le système existant est la fondation.

Ne pas le remplacer.
