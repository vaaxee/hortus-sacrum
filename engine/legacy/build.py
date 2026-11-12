import re,datetime as dt,json
from engine import *
from names import FR
D=dt.date; TD=dt.timedelta
START=D(2026,11,29); END=D(2027,11,27)
JOURS=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
def frname(key):
    if key in FR: return FR[key]
    fr,la=title('Sancti/'+key)
    if fr and not re.search(r'(Confessoris|Martyris|Virginis|Episcopi|Papæ|infra|Infra|Octava |Vigilia)',fr): return fr
    return fr or la or key
def srank(key):
    r=rankof('Sancti/'+key)
    return r if r is not None else 1.0
def latname(key):
    fr,la=title('Sancti/'+key); return la or ''
# ---------------- temporal
def temporal(d):
    y=d.year
    E=easter(2027) if d>=D(2027,1,1) else easter(2026)
    # Advent 2026
    adv1=D(2026,11,29)
    if adv1<=d<=D(2026,12,24):
        w=(d-adv1).days//7+1; dow=(d.weekday()+1)%7
        return f'Adv{w}-{dow}'
    if d==D(2027,1,10): return 'Epi1-0'
    if D(2026,12,25)<=d<=D(2027,1,13): return None
    sept=E-TD(63)
    if d<sept:
        # after Epiphany: Sunday after Jan 6
        s1=D(2027,1,10); w=(d-s1).days//7+1; dow=(d.weekday()+1)%7
        return f'Epi{w}-{dow}'
    if d<E-TD(42):
        w=(d-sept).days//7+1; dow=(d.weekday()+1)%7; return f'Quadp{w}-{dow}'
    if d<E:
        q1=E-TD(42); w=(d-q1).days//7+1; dow=(d.weekday()+1)%7; return f'Quad{w}-{dow}'
    pent=E+TD(49)
    if d<pent+TD(7):
        w=(d-E).days//7; dow=(d.weekday()+1)%7; return f'Pasc{w}-{dow}'
    # after Pentecost; trinity = pent+7 -> Pent01
    w=(d-(pent+TD(7))).days//7+1; dow=(d.weekday()+1)%7
    last=D(2027,11,21)  # 24th, before Advent 2027
    if d>=last: return f'Pent24-{dow}'
    if w>=24:   # resumed Epiphany sundays: Oct31->Epi4, Nov7->Epi5, Nov14->Epi6
        k=(d-D(2027,10,31)).days//7+4
        return f'Epi{k}-{dow}' 
    return f'Pent{w:02d}-{dow}'
SUNFR={}
def tname(key,d):
    fr,la=title('Tempora/'+key)
    return fr,la
ORD=['','1er','2e','3e','4e','5e','6e','7e','8e','9e','10e','11e','12e','13e','14e','15e','16e','17e','18e','19e','20e','21e','22e','23e','24e']
def tfrench(key,d):
    m=re.match(r'([A-Za-z]+)(\d+)-(\d)',key); s,w,dow=m.group(1),int(m.group(2)),int(m.group(3))
    jour=JOURS[d.weekday()].capitalize()
    E=easter(2027)
    if s=='Adv':
        if dow==0: return f'{ORD[w]} dimanche de l’Avent'+(' (Gaudete)' if w==3 else '')
        if w==3 and dow in (3,5,6): return f'{jour} des Quatre-Temps de l’Avent'
        return f'Férie de l’Avent'
    if s=='Epi':
        if d>D(2027,6,1):
            if dow==0: return f'{ORD[w]} dimanche après l’Épiphanie (repris après la Pentecôte)'
            return 'Férie'
        if dow==0: return f'{ORD[w]} dimanche après l’Épiphanie' if w>1 else 'Sainte Famille de Jésus, Marie et Joseph'
        return 'Férie'
    if s=='Quadp':
        if dow==0: return ['','Dimanche de la Septuagésime','Dimanche de la Sexagésime','Dimanche de la Quinquagésime'][w]
        if w==3 and dow==3: return 'Mercredi des Cendres'
        if w==3 and dow>3: return f'{jour} après les Cendres'
        return 'Férie'
    if s=='Quad':
        if w==5 and dow==0: return '1er dimanche de la Passion'
        if w==6:
            if dow==0: return 'Dimanche des Rameaux'
            return {1:'Lundi saint',2:'Mardi saint',3:'Mercredi saint',4:'Jeudi saint',5:'Vendredi saint',6:'Samedi saint'}[dow]
        if dow==0: return f'{ORD[w]} dimanche de Carême'+(' (Laetare)' if w==4 else '')
        if w==1 and dow in (3,5,6): return f'{jour} des Quatre-Temps de Carême'
        if w==5: return f'{jour} de la Passion'
        return f'Férie de Carême'
    if s=='Pasc':
        if w==0: return 'Dimanche de Pâques' if dow==0 else f'{jour} de Pâques'
        if w==1 and dow==0: return 'Dimanche in Albis (Quasimodo)'
        if w==5 and dow==4: return 'Ascension de Notre-Seigneur'
        if w==5 and dow in (1,2,3): return f'{jour} des Rogations'+(' (vigile de l’Ascension)' if dow==3 else '')
        if w==6 and dow==0: return 'Dimanche dans l’octave de l’Ascension'
        if w==6 and dow==6: return 'Vigile de la Pentecôte'
        if (w==5 and dow>4) or (w==6 and dow<5): return 'Dans l’octave de l’Ascension' if not (w==6 and dow==4) else 'Octave de l’Ascension'
        if w==7: return 'Dimanche de la Pentecôte' if dow==0 else (f'{jour} des Quatre-Temps de Pentecôte' if dow in (3,5,6) else f'{jour} de Pentecôte')
        if dow==0: return f'{ORD[w]} dimanche après Pâques'
        return 'Férie du temps pascal'
    if s=='Pent':
        if w==1 and dow==0: return 'Très Sainte Trinité'
        if w==1 and dow==4: return 'Fête-Dieu (Saint-Sacrement)'
        if w==2 and dow==5: return 'Sacré-Cœur de Jésus'
        if dow==0: return f'{ORD[w]} dimanche après la Pentecôte'
        if (w==1 and dow>4) or (w==2 and dow<4): return 'Dans l’octave du Saint-Sacrement'
        if w==2 and dow==4: return 'Octave du Saint-Sacrement'
        if (w==2 and dow==6) or (w==3 and dow<5): return 'Dans l’octave du Sacré-Cœur'
        if w==3 and dow==5: return 'Octave du Sacré-Cœur'
        return 'Férie'
    return key
def tname2(key,d):
    n=tfrench(key,d)
    r=rankof('Tempora/'+key) or 1.0
    if n in ('Férie','Férie du temps pascal') and r>1.5:
        fr,la=title('Tempora/'+key)
        if fr: return fr
    return n
def trank(key,d):
    r=rankof('Tempora/'+key)
    name=tname2(key,d)
    if r is None: r=1.0
    # Ember Saturday etc fine; corrections
    if name=='Férie' or name=='Férie du temps pascal': r=min(r,1.0)
    return r

RT={'Duplex I classis':'1re cl.','Duplex II classis':'2e cl.','Duplex majus':'dbl maj.','Duplex':'dbl','Semiduplex':'semi-dbl',
'Simplex':'simple','Vigilia':'vigile','Feria major':'fér. maj.','Feria privilegiata':'fér. priv.','Feria':'férie'}
def rlabel(path,istemp,name,r):
    t=(ranktext(path) if path else '').lower()
    if istemp and 'imanche' in name and name not in ('Dimanche de Pâques','Dimanche de la Pentecôte'):
        if r>=6.5: return 'dim. 1re cl.'
        if r>=5.5: return 'dim. 2e cl.'
        return 'dim.'
    if 'vigil' in t or name.startswith('Vigile'): return 'vigile 1re cl.' if r>=6 else ('vigile 2e cl.' if r>=5 else 'vigile')
    if re.search(r'\b(ii|2|2nd)\s*class',t): return '2e cl.'
    if re.search(r'\b(i|1|1st)\s*class',t): return '1re cl.'
    if 'duplex majus' in t: return 'dbl maj.'
    if t.startswith('semiduplex'): return 'semi-dbl'
    if t.startswith('duplex'): return 'dbl'
    if 'simplex' in t: return 'simple'
    if 'feria major' in t: return 'fér. maj.'
    if 'privileg' in t: return 'fér. priv.'
    if 'feria' in t: return 'férie'
    if r>=6: return '1re cl.'
    if r>=5: return '2e cl.'
    if r>=4: return 'dbl maj.'
    if r>=3: return 'dbl'
    if r>=2: return 'semi-dbl'
    return 'simple' if not istemp else 'férie'
def color(lat,fr,d,istemp):
    n=fr
    if n.startswith('Vigile') or 'vigile' in n:
        if 'Nativité de Notre' in n: return 'violet'
        if 'Épiphanie' in n: return 'blanc'
        if 'Pentecôte' in n: return 'rouge'
        if 'Ascension' in n: return 'blanc'
        return 'violet'
    if 'Vendredi saint' in n or 'défunts' in n: return 'noir'
    if re.search(r'Gaudete|Laetare',n): return 'rose'
    if 'Jeudi saint' in n: return 'blanc'
    if istemp and re.search(r'Avent|Carême|Passion|Rameaux|Lundi saint|Mardi saint|Mercredi saint|Samedi saint|Cendres|gésime|Rogations|Quatre-Temps',n) and 'Pentecôte' not in n: return 'violet'
    if n=='Les Saints Innocents' and d.weekday()!=6: return 'violet'
    if re.search(r'Pentecôte',n) and istemp and not re.search(r'après la Pentecôte',n): return 'rouge'
    if re.search(r'Jean, Apôtre et Évangéliste|Conversion|Chaire|Dédicace|Pierre aux Liens|Stigmates',n): return 'blanc'
    if re.search(r'Martyr|Apôtre|Évangéliste|Croix|Précieux Sang|Pierre et Paul|Décollation|Innocents|Étienne',n): return 'rouge'
    if istemp and re.search(r'après la Pentecôte|après l’Épiphanie|^Férie$',n): return 'vert'
    return 'blanc'
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
SATBVM='Office de la Sainte Vierge le samedi'
def days():
    tr={}
    for y,E in [(2026,easter(2026)),(2027,easter(2027))]:
        l,T=transfers(y,E); tr[y]=T
    out=[]
    d=START
    while d<=END:
        md=f'{d.month:02d}-{d.day:02d}'
        T=tr[d.year]
        moved=set()
        for k,v in T.items():
            if not v.startswith('Tempora/'):
                for f in v.split('~'):
                    if f!=k: moved.add(f)
        cands=[]
        tk=temporal(d)
        E=easter(2027)
        sept_ember={D(2027,9,15):'Mercredi des Quatre-Temps de septembre',D(2027,9,17):'Vendredi des Quatre-Temps de septembre',D(2027,9,18):'Samedi des Quatre-Temps de septembre'}
        if d in sept_ember:
            cands.append([2.1,sept_ember[d],'',True,'Tempora/093-'+str((d.weekday()+1)%7)])
        elif tk:
            tn=tname2(tk,d); tr_=trank(tk,d)
            cands.append([tr_,tn,(title('Tempora/'+tk)[1] or ''),True,'Tempora/'+tk])
        files=None
        if md in T:
            val=T[md]
            if val.startswith('Tempora/'):
                k=val.split('/')[1]
                nm={'Nat1-0':'Dimanche dans l’octave de Noël','Nat2-0':'Très Saint Nom de Jésus','Epi3-0':'3e dimanche après l’Épiphanie (anticipé au samedi)'}.get(k,title(val)[0] or k)
                cands=[[rankof(val) or 5,nm,title(val)[1] or '',True,val]]
                files=[]
            else: files=val.split('~')
        else:
            files=[f for f in KAL.get(md,[]) if f not in moved]
        for i,f in enumerate(files):
            if f.startswith('X'): continue
            r=srank(f) if i==0 else min(srank(f),1.1)
            cands.append([r,fixname(frname(f)),latname(f),False,'Sancti/'+f])
        if not cands: cands=[[1.0,'Férie','',True,'']]
        cands.sort(key=lambda c:-c[0])
        win=cands[0]
        comms=[c[1] for c in cands[1:] if not (c[3] and c[0]<=1.0) and c[1] not in ('Férie','Férie du temps pascal')]
        holy=(E-TD(7)<=d<=E+TD(7)) or (E+TD(49)<=d<=E+TD(55))
        if holy and d.weekday()!=6: comms=[]
        if holy and d==E: comms=[]
        if md in ('12-29','12-31'): comms=comms+['Octave de Noël']
        if md=='12-24': comms=[]
        extra={'2027-04-18':'Octave de S. Joseph','2027-05-30':'Octave du Saint-Sacrement','2027-06-06':'Octave du Sacré-Cœur'}
        if d.isoformat() in extra: comms=comms+[extra[d.isoformat()]]
        comms=[fixname(c) for c in comms]
        name=win[1]
        if win[3] and win[0]<=1.0 and d.weekday()==5 and not cands[1:] :
            name=SATBVM; lab='simple'; col='blanc'
        else:
            lab=rlabel(win[4],win[3],name,win[0])
            col=color(win[2],name,d,win[3])
        if d.weekday()==6 and any(x in ('Octave du Saint-Sacrement','Octave du Sacré-Cœur') for x in comms): col='blanc'
        tempname=next((c[1] for c in cands if c[3]),None)
        out.append(dict(date=d.isoformat(),office=name,rank=lab,color=col,comms=comms,temporal=tempname,isfeast=not win[3],path=win[4]))
        d+=TD(1)
    return out
if __name__=='__main__':
    R=days()
    json.dump(R,open('days.json','w'),ensure_ascii=False,indent=0)
    for r in R:
        print(r['date'],dt.date.fromisoformat(r['date']).strftime('%a'),'|',r['office'],'|',r['rank'],'|',r['color'],'|',' ; '.join(r['comms']))
