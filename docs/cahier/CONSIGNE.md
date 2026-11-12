# Consigne pour Claude Code — « Hebdomada in Dei servitio »

Construire une **web app installable sur iPhone (PWA)** qui sert de compagnon quotidien de prière. Elle suit le calendrier liturgique traditionnel (rubriques de 1954) et rend interactifs le livret *Le Jardin de l’âme* et le calendrier papier 2026-2027 fournis ici.

À lire dans cet ordre : `CONSIGNE.md` (ce fichier), `CONTEXTE.md`, `SPEC.md`, `SOURCES.md`, `DECISIONS_ET_LIMITES.md`.

---

## 1. Règles non négociables

1. **Rien de mémoire.**
   - Tout texte de prière, de méditation, de vie de saint, d’indulgence ou de rubrique vient d’une **source officielle ou ancienne identifiée**, reproduite **mot pour mot**.
   - Chaque texte est stocké avec sa référence : ouvrage, édition, page ou numéro, et URL si elle existe.
   - Si un texte n’est pas trouvé : on ne l’invente pas. On le signale dans `A_FOURNIR.md` et on demande à l’utilisateur.
2. **Discipline d’avant 1955.**
   - Calendrier romain de 1954 (rubriques *Divino afflatu* et additions de Pie XII), sans la réforme de 1955 ni le Code de 1983.
   - Pour les indulgences : *Enchiridion indulgentiarum* de 1952, le dernier recueil officiel avant le concile.
   - Pour le jeûne et l’abstinence : Code de 1917, can. 1250-1254.
3. **Le vouvoiement** dans tous les textes adressés à Dieu, à la Vierge et aux saints, comme dans le livret.
4. **Aucune trace d’IA dans l’interface** : pas de « généré par », pas de note de travail visible. Les métadonnées de source sont visibles, discrètement (petit « source » dépliable).
5. **Sources tierces récentes** (blogs, sites modernes) :
   - on y renvoie par un **lien** ;
   - on ne recopie pas leurs textes ;
   - sauf s’ils publient une **édition ancienne du domaine public**, et dans ce cas on cite l’édition d’origine.
6. **Poser les questions** à l’utilisateur avant tout choix qui change ce qu’il verra : ajout ou retrait d’une prière, structure de la liste du jour, choix d’une source de méditation. Il préfère être consulté.

## 2. Choix déjà faits par l’utilisateur

| Sujet | Décision |
|---|---|
| Forme | Web app installable (PWA), pas d’App Store |
| Données | **Synchronisées entre téléphone et PC** : compte et base hébergée |
| Méditations | **Alternées selon le jour, le temps liturgique ou le mois** : Guéranger (*L’Année liturgique*), recueils anciens de méditations quotidiennes, recueils de « mois » (mois de S. Joseph, mois des morts, etc., avec les pratiques attachées à chaque méditation), et le blog Le Petit Sacristain cité par lien. Choisir à chaque fois ce qui est « le plus propice à la sainteté et à l’édification ». |
| Trentain | **Trentain de prières** (30 jours), avec compteur |
| Liste quotidienne | **Nouvelle structure à proposer** à partir de son modèle Notion (captures fournies). Une proposition figure dans `SPEC.md` §4, à valider avec lui. |
| Rappels | Matin et soir à heure fixe ; veille des fêtes et des neuvaines ; anniversaires spirituels ; heure fixe par dévotion (ex. 15 h le vendredi, Angélus) |
| Langue des prières | **Français d’abord, latin dépliable** quand il existe |
| Vie des saints | **Dépliable** : vie du ou des saints du jour |
| Martyrologe | **Micro-martyrologe** : tous les saints du jour, avec une **invocation** pour chacun, y compris les saints secondaires |

## 3. Pile technique recommandée

Elle est modifiable si tu as une bonne raison ; dans ce cas, explique-la à l’utilisateur.

- **Front** : SvelteKit ou React (Vite) en TypeScript, en PWA. Service worker pour le hors-ligne : textes, calendrier de l’année et prières en cache.
- **Données et comptes** : Supabase (Postgres, authentification par lien magique, règles RLS par utilisateur), sur l’offre gratuite.
- **Notifications** : Web Push (clés VAPID), envoyées par une tâche planifiée côté serveur (Supabase Edge Function + pg_cron, ou équivalent).
  - Sur iPhone, les notifications d’une PWA ne marchent que si l’app est **ajoutée à l’écran d’accueil**, avec iOS 16.4 ou plus récent.
  - Prévoir un écran d’aide qui l’explique.
- **Hébergement** : Vercel, Netlify ou Cloudflare Pages (gratuit).
- **Charte graphique** : celle du livret (voir `CONTEXTE.md` §3) : EB Garamond, rouge rubrique, ornements fins. Mode sombre soigné, car l’utilisateur utilise Notion en sombre.

## 4. Étapes de livraison

Après chaque étape : faire valider par l’utilisateur avant de passer à la suivante.

1. **Données**
   - Importer `donnees/calendrier_2026-2027.json` et `donnees/index_prieres_jardin.json`.
   - Extraire tous les textes du livret depuis `livret/source/*.tex` vers une base de prières structurée, avec titre, texte français, latin, usage, indulgence et source.
   - Rendre le moteur de calendrier (`moteur/`) capable de **générer n’importe quelle année** : réécrire en TypeScript ou garder Python côté build, et vérifier contre 2026-2027.
2. **Squelette de l’app**
   - Écran « Aujourd’hui » avec l’office du jour, la liste à cocher et le martyrologe.
   - Synchronisation et compte.
3. **Prières cliquables** : chaque élément de la liste ouvre sa prière, en français avec le latin dépliable, l’indulgence et la source.
4. **Suivis** : dévotions à jours comptés, neuvaines, trentains, préparation et consécrations, avec compteurs et détection des séries interrompues.
5. **Rappels** : notifications push.
6. **Méditations et vies de saints** : collecte des sources, découpage par jour, attribution (voir `SPEC.md` §6).
7. **Profil spirituel** : anniversaires (baptême, confirmation, première communion, consécrations, fête patronale) et saints favoris.

## 5. Livrables attendus à chaque étape

- Le code, dans un dépôt git propre.
- `A_FOURNIR.md` : la liste des textes introuvables ou à faire fournir par l’utilisateur.
- `SOURCES_UTILISEES.md` : chaque source réellement utilisée, avec édition et URL.
- Une courte note de ce qui a changé, en français.
