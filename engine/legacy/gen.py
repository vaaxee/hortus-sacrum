import json,datetime as dt,re
import devo,enrich,stations
D=dt.date;TD=dt.timedelta
R={r['date']:r for r in json.load(open('days.json'))}
by=devo.all_items()
MOIS=['','janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']
JR=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
GRANDS=('1re cl.','2e cl.')
def tex(s):
    s=s.replace('&','\\&').replace('%','\\%')
    s=re.sub(r'(\d+)e\b',r'\1\\textsuperscript{e}',s)
    s=re.sub(r'\b1er\b',r'1\\textsuperscript{er}',s)
    s=re.sub(r'\b1re\b',r'1\\textsuperscript{re}',s)
    s=s.replace('Ier','I\\textsuperscript{er}')
    return s
ORIG={'2027-04-05':'03-25','2027-06-05':'05-31'}
def notice_for(d,r):
    if not r['isfeast'] or r['rank'] not in ('1re cl.','2e cl.','dbl maj.'): return None
    if r['office'].startswith('Octave') or 'jour dans' in r['office']: return None
    md=ORIG.get(d.isoformat(),d.isoformat()[5:])
    name=r['office'].replace('Toussaint','tous les Saints')
    t=enrich.notice2(md,name)
    if not t or t.startswith('Le lendemain'): return None
    return enrich.short(t,210)
def incip(r):
    p=r['path']
    if r['office'].startswith('Office de la Sainte Vierge'): return 'Salve, sancta Parens'
    inc=enrich.incipit(p) if p else None
    if not inc and p and p.startswith('Tempora/'): inc=enrich.incipit(p.rsplit('-',1)[0]+'-0')
    return inc
def info(d):
    r=R[d.isoformat()]
    f=devo.fasting(d,r['office'],r['isfeast'])
    return r,f
def day(d):
    r,f=info(d)
    big= d.weekday()==6 or r['rank'] in GRANDS
    off=tex(r['office'])
    if r['rank'] in ('1re cl.','2e cl.','dim. 1re cl.','dim. 2e cl.','dbl maj.') or d.weekday()==6: off='\\offgrand{'+off+'}'
    else: off='\\offpetit{'+off+'}'
    body=''
    if r['comms']: body+='\\comm{'+' ; '.join(tex(c) for c in r['comms'])+'}'
    lit=[]
    inc=incip(r)
    if inc: lit.append('Intr. \\textit{'+inc+'}')
    st=stations.ST.get(d)
    if st: lit.append('\\textit{'+st+'}')
    if lit: body+='\\liturgie{'+' \\enspace·\\enspace '.join(lit)+'}'
    n=notice_for(d,r)
    if n: body+='\\noticesaint{'+tex(n)+'}'
    if f: body+='\\jeune{'+tex(f[1])+'}'
    for kind,lab,pg in by.get(d.isoformat(),[]):
        ref=f'\\pg{{{pg}}}' if pg else ''
        body+=('\\dev' if kind=='dev' else '\\nov')+'{'+tex(lab)+'}{'+ref+'}'
    cmd='\\jourfete' if (r['rank'] in GRANDS and d.weekday()!=6) or r['rank'] in ('dim. 1re cl.',) and r['isfeast'] else '\\jourcal'
    if r['rank'] in GRANDS and r['isfeast']: cmd='\\jourfete'
    return f"{cmd}{{{JR[d.weekday()]}}}{{{d.day}}}{{{'1' if big else '0'}}}{{{r['color']}}}{{{off}}}{{{tex(r['rank'])}}}{{{body}}}\n"
def span(a,b):
    if a.month==b.month: return f'du {a.day} au {b.day} {MOIS[b.month]} {b.year}'
    if a.year==b.year: return f'du {a.day} {MOIS[a.month]} au {b.day} {MOIS[b.month]} {b.year}'
    return f'du {a.day} {MOIS[a.month]} {a.year} au {b.day} {MOIS[b.month]} {b.year}'
# ---------------- mois
DEVM={1:('Mois du saint Nom de Jésus',118,True),3:('Mois de saint Joseph',466,False),5:('Mois de Marie',325,True),
6:('Mois du Sacré-Cœur de Jésus',253,True),7:('Mois du Précieux Sang',217,True),8:('Mois du Cœur Immaculé de Marie',389,True),
9:('Mois de Notre-Dame des Sept Douleurs',381,True),10:('Mois du saint Rosaire',398,False),11:('Mois des fidèles trépassés',589,True),
12:('Mois de l’Immaculée Conception',364,True)}
EPI={12:('Tempora/Adv4-0','4\\textsuperscript{e} dimanche de l’Avent'),1:('Sancti/01-06','Épiphanie'),2:('Sancti/02-02','Purification'),
3:('Sancti/03-19','S. Joseph'),4:('Tempora/Pasc0-0','Pâques'),5:('Tempora/Pasc7-0','Pentecôte'),6:('Tempora/Pent02-5','Sacré-Cœur'),
7:('Sancti/07-01','Précieux Sang'),8:('Sancti/08-15','Assomption'),9:('Sancti/09-08','Nativité de Notre-Dame'),
10:('Sancti/10-07','Saint Rosaire'),11:('Sancti/11-01','Toussaint')}
def introit_fr(path):
    b=enrich.msec('Francais',path,'Introitus') or []
    ref=''; txt=''
    for l in b:
        if l.startswith('!') and not ref: ref=l[1:].strip().rstrip('.')
        if l.startswith('v. ') and not txt: txt=l[3:].strip()
    txt=re.sub(r'\s*\((Allé|Alle)[^)]*\)\.?$','',txt).replace('fasssent','fassent')
    return txt,ref
def moispages(y,m):
    first=D(y,m,1); last=(D(y+(m==12),m%12+1,1)-TD(1))
    out=[]
    out.append('\\moisgauche{'+MOIS[m].capitalize()+'}{'+str(y)+'}{')
    if m in DEVM:
        t,n,pl=DEVM[m]
        out.append('\\devmois{'+tex(t)+'}{'+str(n)+'}{'+('1' if pl else '0')+'}')
    txt,ref=introit_fr(EPI[m][0])
    out.append('}{'+tex(txt)+'}{'+ref+'}{'+EPI[m][1]+'}\n')
    # page droite
    fetes=[];ja=[];j=[];a=[];starts=[]
    d=max(first,D(2026,11,29))
    while d<=min(last,D(2027,11,27)):
        r,f=info(d)
        if r['rank'] in GRANDS or (r['rank']=='dbl maj.' and r['isfeast']):
            fetes.append((d.day,tex(r['office'])))
        if f:
            {'JA':ja,'J':j,'A':a}[f[0]].append(str(d.day))
        for kind,lab,pg in by.get(d.isoformat(),[]):
            if kind=='nov' and lab.endswith('1er jour'):
                starts.append((d.day,tex(lab.split(' — ')[0]),pg))
            if kind=='dev' and re.search(r'— 1/\d+',lab):
                starts.append((d.day,tex(lab.split(' — ')[0]),pg))
            if kind=='dev' and 'Montfort, douze jours' in lab and '1/12' in lab:
                starts.append((d.day,'Préparation à la consécration de Montfort',11))
        d+=TD(1)
    s='\\moisdroite{'+MOIS[m].capitalize()+' '+str(y)+'}{'
    s+='\\rubmois{Fêtes principales}'+''.join(f'\\lignemois{{{a_}}}{{{b_}}}' for a_,b_ in fetes)
    if starts:
        s+='\\rubmois{Dévotions et neuvaines qui commencent}'+''.join(f'\\lignemois{{{a_}}}{{{b_}'+(f'\\pg{{{p_}}}' if p_ else '')+'}' for a_,b_,p_ in starts)
    if ja or j or a:
        s+='\\rubmois{Pénitence}'
        if ja: s+='\\lignemoislong{Jeûne et abstinence}{'+', '.join(ja)+'}'
        if j: s+='\\lignemoislong{Jeûne}{'+', '.join(j)+'}'
        if a: s+='\\lignemoislong{Abstinence}{'+', '.join(a)+'}'
    s+='}\n'
    out.append(s)
    return ''.join(out)
out=[]
s=D(2026,11,29)
while s<=D(2027,11,27):
    e=s+TD(6)
    for k in range(7):
        dd=s+TD(k)
        if dd.day==1:
            out.append(moispages(dd.year,dd.month))
    sun=R[s.isoformat()]
    head=tex(sun['temporal'] if sun['temporal'] and 'imanche' in (sun['temporal'] or '') else sun['office'])
    out.append(f"\\semainegauche{{{tex(span(s,e))}}}{{{head}}}\n")
    for i in range(4): out.append(day(s+TD(i)))
    out.append("\\semainedroite{"+tex(span(s,e))+"}\n")
    for i in range(4,7): out.append(day(s+TD(i)))
    out.append("\\notes\n")
    s+=TD(7)
open('weeks.tex','w').write(''.join(out))
print(sum(1 for x in out if x.startswith('\\moisgauche')),'mois')
