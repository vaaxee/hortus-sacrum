import datetime as dt
D=dt.date; TD=dt.timedelta
PG={'stigmates':62,'berchmans':63,'gonzague':63,'thomas':64,'joseph7':64,'immaculee7':65,'camille':65,'ignace':66,'stanislas':66,
'antoine':68,'dominique':68,'mercredi':68,'heure':69,'vendredi1':69,'crucifix':71,'paule':72,'douleurs7':72,'samedi1':73,'douze':73,'rosaire':74,'merci':76,
'montfort':11,'gabriel':19,'joseph':34,'veni':56,'douleurs':32,'michel':28,'couronne':21,'mediatrice':17,'tejoseph':60}
def weekly(start,n,key,label):
    return [(start+TD(7*i),key,f'{label} — {i+1}/{n}') for i in range(n)]
SERIES=[]
SERIES+=weekly(D(2026,12,20),6,'thomas','Six dimanches de S. Thomas d’Aquin')
SERIES+=weekly(D(2027,1,31),7,'joseph7','Sept dimanches de S. Joseph')
SERIES+=weekly(D(2027,4,11),6,'gonzague','Six dimanches de S. Louis de Gonzague')
SERIES+=weekly(D(2027,5,23),10,'ignace','Dix dimanches de S. Ignace')
SERIES+=weekly(D(2027,8,15),5,'stigmates','Cinq dimanches des Stigmates de S. François')
SERIES+=weekly(D(2027,10,10),7,'immaculee7','Sept dimanches de l’Immaculée Conception')
SERIES+=weekly(D(2027,3,16),13,'antoine','Treize mardis de S. Antoine')
SERIES+=weekly(D(2027,6,15),15,'dominique','Quinze mardis de S. Dominique')
SERIES+=weekly(D(2027,1,8),13,'paule','Treize vendredis de S. François de Paule')
SERIES+=weekly(D(2027,7,30),7,'douleurs7','Sept vendredis des Douleurs')
SERIES+=weekly(D(2027,4,17),15,'rosaire','Quinze samedis du Rosaire')
SERIES+=weekly(D(2027,7,31),7,'merci','Sept samedis de N.-D. de la Merci')
SERIES+=weekly(D(2027,9,18),11,'douze','Douze samedis avant l’Immaculée Conception')
SERIES=[(d,k,l.replace('— 11/11','— 11/12 (le 12e : 4 déc.)').replace('/11','/12')) if k=='douze' else (d,k,l) for d,k,l in SERIES]
def firsts(start,end):
    out=[]
    d=start
    fri=0;sat=0
    while d<=end:
        if d.day<=7:
            if d.weekday()==2: out.append((d,'mercredi','Premier mercredi : S. Joseph'))
            if d.weekday()==4:
                fri+=1
                lab='Premier vendredi du mois'+(f' — {fri}/9' if fri<=9 else '')
                out.append((d,'vendredi1',lab))
                out.append((d-TD(1),'heure','Heure sainte (veille du premier vendredi)'))
            if d.weekday()==5:
                sat+=1
                lab='Premier samedi du mois'+(f' — {sat}/5' if sat<=5 else '')
                out.append((d,'samedi1',lab))
        d+=TD(1)
    return out
NOV=[('Neuvaine à l’Immaculée Conception',D(2026,11,29),None),('Neuvaine de Noël',D(2026,12,16),None),
('Neuvaine à S. Joseph',D(2027,3,10),'joseph'),('Neuvaine à S. Gabriel',D(2027,3,15),'gabriel'),
('Neuvaine à S. Louis-Marie Grignion de Montfort (28 avr.)',D(2027,4,19),None),
('Neuvaine au Saint-Esprit, avant la Pentecôte',D(2027,5,7),'veni'),('Neuvaine au Sacré-Cœur',D(2027,5,26),None),
('Neuvaine de l’Assomption',D(2027,8,6),None),('Neuvaine de la Nativité de Notre-Dame',D(2027,8,30),None),
('Neuvaine à S. Michel',D(2027,9,20),'michel'),('Neuvaine du Rosaire',D(2027,9,28),None),('Neuvaine de la Toussaint',D(2027,10,23),None)]
def novenas():
    out=[]
    for lab,s,k in NOV:
        for i in range(9): out.append((s+TD(i),k,f'{lab} — {('1er' if i==0 else str(i+1)+'e')} jour'))
    return out
def montfort():
    out=[];s=D(2027,3,3)
    for i in range(33):
        d=s+TD(i)
        if i<12: ph=f'douze jours : se vider de l’esprit du monde — {i+1}/12'
        elif i<19: ph=f'1re semaine : connaissance de soi — {i-11}/7'
        elif i<26: ph=f'2e semaine : connaissance de la sainte Vierge — {i-18}/7'
        else: ph=f'3e semaine : connaissance de Jésus-Christ — {i-25}/7'
        out.append((d,'montfort','Montfort, '+ph))
    out.append((D(2027,4,5),'montfort','Consécration (renouvellement) à Jésus par Marie — communion de ce jour'))
    return out
FIXED=[(D(2027,3,24),'gabriel','Prière à S. Gabriel'),(D(2027,3,19),'joseph','Douleurs et Allégresses de S. Joseph ; hymne Te, Joseph, celebrent (p. 60)'),
(D(2027,5,16),'veni','Veni Creator'),(D(2027,9,15),'douleurs','Les sept Douleurs de Marie')]
def all_items():
    L=SERIES+firsts(D(2026,11,29),D(2027,11,27))+montfort()+FIXED
    by={}
    for d,k,l in L: by.setdefault(d.isoformat(),[]).append(('dev',l,PG.get(k)))
    for d,k,l in novenas(): by.setdefault(d.isoformat(),[]).append(('nov',l,PG.get(k) if k else None))
    return by
# -------- fasting, CIC 1917
def fasting(d,office,isfeast):
    E=dt.date(2027,3,28)
    ash=E-TD(46)
    ember={D(2026,12,16),D(2026,12,18),D(2026,12,19),D(2027,2,17),D(2027,2,19),D(2027,2,20),D(2027,5,19),D(2027,5,21),D(2027,5,22),D(2027,9,15),D(2027,9,17),D(2027,9,18)}
    vig={D(2026,12,24),D(2027,5,15),D(2027,8,14)}  # All Saints vigil 31 Oct 2027 is Sunday: none
    oblig={D(2026,12,25),D(2027,5,6),D(2027,8,15),D(2027,11,1)}
    if d.weekday()==6: return None
    if d==E-TD(1): return ('JA','Jeûne et abstinence jusqu’à midi')
    lent=ash<=d<E
    if d==ash or (lent and d.weekday() in (4,5)) or d in ember or d in vig: return ('JA','Jeûne et abstinence')
    if lent: return ('J','Jeûne')
    if d.weekday()==4:
        if d in oblig: return None
        if d==D(2027,1,1): return ('A','Abstinence (sauf là où la Circoncision est fête de précepte)')
        return ('A','Abstinence')
    return None
