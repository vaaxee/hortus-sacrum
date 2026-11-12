"""Noms français des offices (repris du moteur 2026-2027) et normalisation."""
import re

FR={
'01-00':'Saint Nom de Jésus','01-01':'Circoncision de Notre-Seigneur et octave de Noël','01-05':'Vigile de l’Épiphanie','01-06':'Épiphanie de Notre-Seigneur',
'01-07':'2e jour dans l’octave de l’Épiphanie','01-08':'3e jour dans l’octave de l’Épiphanie','01-09':'4e jour dans l’octave de l’Épiphanie','01-10':'5e jour dans l’octave de l’Épiphanie','01-11':'6e jour dans l’octave de l’Épiphanie','01-12':'7e jour dans l’octave de l’Épiphanie','01-13':'Octave de l’Épiphanie (Baptême du Seigneur)',
'02-02':'Purification de la Bienheureuse Vierge Marie','02-11':'Apparition de la Bienheureuse Vierge Marie Immaculée (Lourdes)',
'03-09':'Ste Françoise Romaine, Veuve','03-10':'Les Quarante Martyrs','03-12':'S. Grégoire le Grand, Pape, Confesseur et Docteur','03-19':'S. Joseph, Époux de la Bienheureuse Vierge Marie, Confesseur',
'03-21':'S. Benoît, Abbé','03-25':'Annonciation de la Bienheureuse Vierge Marie','03-27':'S. Jean Damascène, Confesseur et Docteur','03-28':'S. Jean de Capistran, Confesseur',
'04-02':'S. François de Paule, Confesseur','04-04':'S. Isidore, Évêque, Confesseur et Docteur','04-05':'S. Vincent Ferrier, Confesseur','04-11':'S. Léon le Grand, Pape, Confesseur et Docteur','04-13':'S. Herménégilde, Martyr','04-14':'S. Justin, Martyr','04-17':'S. Anicet, Pape et Martyr','04-21':'S. Anselme, Évêque, Confesseur et Docteur','04-23':'S. Georges, Martyr','04-24':'S. Fidèle de Sigmaringen, Martyr','04-28':'S. Paul de la Croix, Confesseur','04-30':'Ste Catherine de Sienne, Vierge',
'05-03':'Invention de la Sainte Croix','05-05':'S. Pie V, Pape et Confesseur','05-07':'S. Stanislas, Évêque et Martyr','05-15':'S. Jean-Baptiste de La Salle, Confesseur','05-18':'S. Venance, Martyr','05-20':'S. Bernardin de Sienne, Confesseur','05-29':'Ste Marie-Madeleine de Pazzi, Vierge','05-31':'Bienheureuse Vierge Marie Reine',
'06-02':'Ss. Marcellin, Pierre et Érasme, Martyrs','06-04':'S. François Caracciolo, Confesseur','07-02':'Visitation de la Bienheureuse Vierge Marie','07-16':'Notre-Dame du Mont-Carmel','08-05':'Dédicace de Sainte-Marie-aux-Neiges','08-06':'Transfiguration de Notre-Seigneur','08-14':'Vigile de l’Assomption','08-15':'Assomption de la Bienheureuse Vierge Marie','08-18':'4e jour dans l’octave de l’Assomption','08-22':'Cœur Immaculé de Marie',
'09-08':'Nativité de la Bienheureuse Vierge Marie','09-12':'Saint Nom de Marie','09-14':'Exaltation de la Sainte Croix','09-15':'Les Sept Douleurs de la Bienheureuse Vierge Marie','09-24':'Notre-Dame de la Merci','10-07':'Très Saint Rosaire de la Bienheureuse Vierge Marie','11-02':'Commémoraison de tous les fidèles défunts','11-09':'Dédicace de l’Archibasilique du Très-Saint-Sauveur','11-18':'Dédicace des Basiliques des Ss. Pierre et Paul','11-21':'Présentation de la Bienheureuse Vierge Marie',
'12-08':'Immaculée Conception de la Bienheureuse Vierge Marie','12-09':'2e jour dans l’octave de l’Immaculée Conception','12-10':'3e jour dans l’octave de l’Immaculée Conception','12-12':'5e jour dans l’octave de l’Immaculée Conception','12-14':'7e jour dans l’octave de l’Immaculée Conception','12-15':'Octave de l’Immaculée Conception','12-24':'Vigile de la Nativité de Notre-Seigneur','12-25':'Nativité de Notre-Seigneur Jésus-Christ',
'10-DU':'Notre-Seigneur Jésus-Christ Roi','10-31v':'Vigile de la Toussaint (anticipée)','09-sab-oct':'Samedi dans l’octave de la Nativité de la Sainte Vierge','05-31o':'Ste Pétronille, Vierge','03-20':'S. Joachim, Père de la B. V. Marie','08-16':'S. Joachim, Père de la B. V. Marie',
}
FR.update({'01-04':'Octave des Saints Innocents','04-14t':'Ss. Tiburce, Valérien et Maxime, Martyrs','05-19o':'Ste Pudentienne, Vierge',
'06-26oct':'3e jour dans l’octave de S. Jean-Baptiste','06-28oct':'5e jour dans l’octave de S. Jean-Baptiste','06-30oct':'7e jour dans l’octave de S. Jean-Baptiste',
'08-17bmv':'3e jour dans l’octave de l’Assomption','08-18bmv':'4e jour dans l’octave de l’Assomption','08-19bmv':'5e jour dans l’octave de l’Assomption','08-20bmv':'6e jour dans l’octave de l’Assomption','08-21bmv':'7e jour dans l’octave de l’Assomption',
'12-09bmv':'2e jour dans l’octave de l’Immaculée Conception','12-10bmv':'3e jour dans l’octave de l’Immaculée Conception','12-11bmv':'4e jour dans l’octave de l’Immaculée Conception','12-12bmv':'5e jour dans l’octave de l’Immaculée Conception','12-13bmv':'6e jour dans l’octave de l’Immaculée Conception','12-14bmv':'7e jour dans l’octave de l’Immaculée Conception'})


def fixname(n):
    n=n.replace('’',"’").replace("'", "’")
    rep={'SAINT ATHANASE, ÉVÊQUE, CONFES. ET DOCT. DE L’ÉGLISE':'S. Athanase, Évêque, Confesseur et Docteur de l’Église',
    'S. Gabrielis Archangeli':'S. Gabriel, Archange','S. Joannis Apostoli ante Portam Latinam':'S. Jean devant la Porte Latine',
    'S. Marc Evangeliste':'S. Marc, Évangéliste','Saints Soter et Caius, Souverains Pontifs et Martyrs':'Ss. Soter et Caius, Papes et Martyrs',
    'Sts Clet et Marcellin Souverin Pontifes et Martyrs':'Ss. Clet et Marcellin, Papes et Martyrs','Sts Philippe et Jacques':'Ss. Philippe et Jacques, Apôtres',
    'S. Philippe Beniti, Confesseur':'S. Philippe Benizi, Confesseur','Les saints Sept Frères Martys, et les saintes Rufine et Seconde, Vierges et Martyres':'Les Sept Frères Martyrs, et Stes Rufine et Seconde, Vierges et Martyres',
    'Ss, Hippolyte et Cassien, Martyrs':'Ss. Hippolyte et Cassien, Martyrs','Ss Tiburce et Suzanne, Vierge, Martyrs':'S. Tiburce et Ste Suzanne, Vierge, Martyrs',
    'S. Pierre Canisius Confesseur et Docteur de l’Eglise':'S. Pierre Canisius, Confesseur et Docteur de l’Église','S. Pierre Martyr':'S. Pierre, Martyr',
    'S. Pierre Celestin Pape et Confesseur':'S. Pierre Célestin, Pape et Confesseur','S. Gregoire VII Pape et Confesseur':'S. Grégoire VII, Pape et Confesseur',
    'Ss. Gordien et Êpimaque Martyrs':'Ss. Gordien et Épimaque, Martyrs','Ss. Faustin et Jovite, Martyr':'Ss. Faustin et Jovite, Martyrs',
    'Ss. Tryphon, Respice et Nymphe, Vierge, Martyrs':'Ss. Tryphon, Respice et Ste Nymphe, Vierge, Martyrs','S. Gabriel de l’Addolorata, Confesseur':'S. Gabriel de l’Addolorata (de N.-D. des Douleurs), Confesseur',
    'Ste. Dorothée, Vierge et Martyre':'Ste Dorothée, Vierge et Martyre','Stes. Perpétue et Félicité, Martyres':'Stes Perpétue et Félicité, Martyres',
    'St Augustin de Cantorbéry, évêque et confesseur':'S. Augustin de Cantorbéry, Évêque et Confesseur','S. Rémi, Evêque et Confesseur':'S. Remi, Évêque et Confesseur',
    'S. Norbert Evêque et Confesseur':'S. Norbert, Évêque et Confesseur','Vigile de St Laurent, Martyr':'Vigile de S. Laurent, Martyr',
    'Saint Nom de Marie':'Saint Nom de Marie','Fête de Tous les Saints':'Toussaint','Commémoraison de tous les fidèles défunts':'Commémoraison de tous les fidèles défunts',
    'Invention de S. Étienne, Premier Martyr':'Invention de S. Étienne, premier Martyr','S. Marguerite, Reine et Veuve':'Ste Marguerite, Reine et Veuve',
    'Saints Douze Frères, Martyrs':'Les Douze Saints Frères, Martyrs','Saints Nérée, Achille, la Vierge Domitille et Pancrace, Martyrs':'Ss. Nérée, Achille, Domitille, Vierge, et Pancrace, Martyrs',
    'S. Nom de Marie':'Saint Nom de Marie','Ste Anne, mère de la T.S. Vierge Marie':'Ste Anne, Mère de la Bienheureuse Vierge Marie',
    'Les Saints Anges Gardiens':'Les Saints Anges gardiens','S. Grégoire le Grand, Pape, Confesseur et Docteur':'S. Grégoire le Grand, Pape, Confesseur et Docteur de l’Église',
    }
    n=rep.get(n,n)
    n=n.replace('Premier, Martyr','premier Martyr')
    if not n.startswith('Saint Nom'): n=re.sub(r'^Saint ','S. ',n); n=re.sub(r'^Sts? ','Ss. ',n) if n.startswith('Sts ') else n
    n=re.sub(r'^Ss ','Ss. ',n)
    n=n.replace('Ss ','Ss. ').replace('Ss.. ','Ss. ')
    n=n.replace('S. Francois','S. François').replace('S. Felix','S. Félix').replace('Evêque','Évêque').replace('Eglise','Église').replace('Evangéliste','Évangéliste')
    # insert missing commas before titles
    n=re.sub(r'(?<=[a-zàâçéèêëîïôûüœ]) (?=(?:Évêque|Pape|Confesseur|Martyrs?|Martyres?|Vierge|Veuve|Abbé|Reine|Empereur|Apôtres?)\b)',', ',n)
    n=re.sub(r'\b(et|de|la|du|le|Bienheureuse|Bse|T\.S\.|Sainte|et les|ses), ',lambda m:m.group(1)+' ',n)
    if re.match(r'^S\. ',n) and re.search(r', (?:Vierge|Veuve|Martyre)\b',n.split(' et ')[0]+n) and not re.search(r'^S\. [^,]+ et ',n):
        if re.search(r', (Vierge|Veuve|Reine|Martyre)',n) and not re.search(r'Confesseur|Évêque|Pape|Abbé|Martyr\b|Martyrs',n):
            n='Ste '+n[3:]
    n=n.replace('S. Marguerite, Reine','Ste Marguerite, Reine').replace('Quarante, Martyrs','Quarante Martyrs').replace('Frères, Martyrs','Frères Martyrs').replace('couronnés, Martyrs','couronnés, Martyrs')
    return n
