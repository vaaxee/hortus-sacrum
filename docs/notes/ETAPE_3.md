# Étape 3 — Import PDF et photo : ce qui a changé

## Nouvel écran : Prières → Ajouter → PDF ou photo
1. **Choix** du fichier (PDF ou image) et, pour un PDF, de la plage de pages (40 pages au plus à la fois).
2. **Extraction**, entièrement dans le navigateur : le fichier n'est envoyé nulle part.
   - PDF avec texte : lecture par pdf.js. Les lettrines sont remises en tête de leur mot, les titres et les lignes en petit corps (« usage ») sont détachés, le folio est retiré.
   - PDF scanné ou photo : reconnaissance du texte par Tesseract.js, en français et en latin. Une case permet de forcer la reconnaissance sur un PDF dont le texte est mal lu.
   - Les ornements (encadrements, bords de page) sont écartés d'après la confiance et la position de chaque mot. Un mot au milieu d'une ligne n'est jamais retiré.
3. **Correction et découpage** :
   - le texte extrait est modifiable, avec les débuts de page marqués ⟦p. N⟧ ;
   - le bouton « Couper ici » commence une nouvelle pièce (ligne `=== Titre`) ;
   - la liste des pièces se met à jour, avec un aperçu de chacune ;
   - la source commune (ouvrage, édition) est pré-remplie avec le titre du PDF, et la page de chaque pièce se remplit seule.
4. **Enregistrement** en une ou plusieurs pièces, marquées « Ajout personnel ».

Les pages lues par reconnaissance sont signalées avec leur taux de confiance et une invitation à relire contre l'original.

## Vérifié
- Tests automatiques : 10 sur 10. Contrôle de types : 0 erreur. Compilation : réussie.
- Dans le navigateur :
  - PDF du livret, pages 12-13 : texte lu, coupé en deux pièces, enregistré avec la source « Le Jardin de l'âme », p. 12 et p. 12-13 ;
  - une vraie page scannée du *Paroissien romain* de 1890 (« Prière du matin », image basse définition) : texte lu en 3 secondes, encadrement décoratif écarté ;
  - une page du livret passée de force par la reconnaissance : 94 % de confiance.

## Limites connues
- La reconnaissance se trompe encore sur des lettres : accents (« trés », « gráce »), lettrines ornées perdues, un mot parasite en bord de page de temps en temps. La relecture contre l'original reste nécessaire ; l'écran le rappelle.
- Les modèles de langue de Tesseract se téléchargent depuis Internet au premier usage. Ils seront à embarquer dans l'app pour un usage hors ligne (étape 6).
- Le numéro de page enregistré est celui du fichier, pas la numérotation imprimée du livre ; il se corrige dans la fiche.
- Pas encore testé sur iPhone (appareil photo direct, mémoire limitée pour les gros PDF).
