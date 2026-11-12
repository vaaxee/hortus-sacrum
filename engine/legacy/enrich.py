import re,os,unicodedata
from engine import _parse
B='/home/claude/do/web/www'
def msec(lang,path,sec,d=0):
    p=f'{B}/missa/{lang}/{path}.txt'
    if path.startswith('Commune/') and not os.path.exists(p): p=f'{B}/horas/{lang}/{path}.txt'
    if d>5 or not os.path.exists(p): return None
    head,secs=_parse(p)
    pick=[x for x in secs if x[0]==sec and not x[1]] or [x for x in secs if x[0]==sec and 'divino' in x[1].lower()]
    if pick:
        body=[l for l in pick[0][2] if l.strip()]
        if body and body[0].startswith('@'):
            ref=body[0][1:]; tgt,_,s2=ref.partition(':')
            return msec(lang,tgt or path,s2 or sec,d+1)
        return body
    if head.startswith('@'):
        return msec(lang,head[1:].split(':')[0],sec,d+1)
    return None
def _vide(path):
    for sec in ('Rule','Rank'):
        b=msec('Latin',path,sec) or []
        for l in b:
            m=re.search(r'(?:vide|ex)\s+([A-Za-z0-9/\-]+)',l)
            if m:
                t=m.group(1)
                return t if '/' in t else 'Commune/'+t
    return None
def incipit(path,d=0):
    if path=='Sancti/12-25': path='Sancti/12-25m3'
    b=msec('Latin',path,'Introitus')
    if not b:
        v=_vide(path)
        if v and d<3 and v!=path: return incipit(v,d+1)
        return None
    for l in b:
        if l.startswith('v. '):
            t=re.split(r'[:,;.!?]',l[3:])[0].strip()
            w=t.split()
            return ' '.join(w[:5])+('…' if len(w)>5 else '')
    return None
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); return ''.join(c for c in s if unicodedata.category(c)!='Mn')
MOIS={'janvier':1,'février':2,'mars':3,'avril':4,'mai':5,'juin':6,'juillet':7,'août':8,'septembre':9,'octobre':10,'novembre':11,'décembre':12}
def martsecs(md):
    p=f'{B}/horas/Francais/Martyrologium/{md}.txt'
    if not os.path.exists(p): return []
    head,secs=_parse(p)
    return [(k,' '.join(l.strip() for l in b if l.strip())) for k,c,b in secs if k!='Titulus']
def keyname(fr):
    m=re.match(r'^(?:S\.|Ste|Ss\.|Stes)\s+([^,]+)',fr)
    if not m: return None
    n=re.split(r'\s+(?:et|de|d’|Ier|II|VII|le|la)\b',m.group(1))[0]
    return n.strip()
def notice(md,fr,depth=0):
    kn=keyname(fr)
    if not kn or depth>1: return None
    kk=norm(kn)
    for k,t in martsecs(md):
        if kk in norm(t):
            m=re.search(r'dont il est fait mention le [^()]*\((\d+)\s+(\w+)\)',t)
            if m and depth==0 and m.group(2) in MOIS:
                r=notice(f'{MOIS[m.group(2)]:02d}-{int(m.group(1)):02d}',fr,1)
                if r: return r
            return t
    return None
def short(t,lim=230):
    if len(t)<=lim: return t
    out=''
    for s in re.split(r'(?<=[.;])\s+',t):
        if len(out)+len(s)>lim and out: break
        out+=(' ' if out else '')+s
    if len(out)>lim+80: out=out[:lim].rsplit(' ',1)[0]
    return out+(' […]' if out!=t else '')
STOP=set('bienheureuse vierge marie notre seigneur jesus christ octave saints saint sainte fete commemoraison apotre apotres confesseur martyr eveque docteur eglise pape apparition les des de la du le et'.split())
def kw(fr):
    w=re.findall(r"[\w’-]+",norm(fr).replace('-',' '))
    return [x for x in w if len(x)>3 and x not in STOP]
def notice2(md,fr):
    r=notice(md,fr.replace('-',' '))
    if r: return r
    ks=kw(fr)
    if not ks: return None
    best=None;bs=0
    for i,(k,t) in enumerate(martsecs(md)):
        nt=norm(t).replace('-',' ')
        if all(x in nt for x in ks): return t
    return None
