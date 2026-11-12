import re,os,datetime as dt,json
B='/home/claude/do/web/www'
D=dt.date
def _parse(p):
    secs=[];cur=None
    lines=open(p,encoding='utf-8').read().split('\n')
    head=lines[0].strip() if lines else ''
    for ln in lines:
        m=re.match(r'^\[([^\]]+)\]\s*(?:\(([^)]*)\))?\s*$',ln)
        if m: cur=[m.group(1),m.group(2) or '',[]]; secs.append(cur); continue
        if cur is not None: cur[2].append(ln)
    return head,secs
def _ok(c):
    c=c.lower()
    if 'nisi' in c: return False
    return ('divino' in c) or ('1930' in c)
def readsec(lang,path,sec,_d=0):
    p=f'{B}/horas/{lang}/{path}.txt'
    if not os.path.exists(p) or _d>4: return None
    head,secs=_parse(p)
    plain=[x for x in secs if x[0]==sec and not x[1]]
    cond=[x for x in secs if x[0]==sec and x[1] and _ok(x[1])]
    pick=cond[0] if cond else (plain[0] if plain else None)
    if pick:
        body=[l for l in pick[2] if l.strip()]
        return body[0].strip() if body else None
    if head.startswith('@'):
        return readsec(lang,head[1:].split(':')[0],sec,_d+1)
    return None
def ranktext(path):
    r=readsec('Latin',path,'Rank')
    if not r: return ''
    if r.startswith('@'): return ranktext(r[1:].split(':')[0])
    f=r.split(';;'); return f[1] if len(f)>1 else ''
def title(path):
    fr=readsec('Francais',path,'Officium'); la=readsec('Latin',path,'Officium')
    fr=fr.split(';;')[0].strip() if fr else None; la=la.split(';;')[0].strip() if la else None
    return fr,la
def rankof(path):
    r=readsec('Latin',path,'Rank')
    if not r: return None
    if r.startswith('@'): 
        tgt=r[1:].split(':')[0]; return rankof(tgt)
    f=r.split(';;')
    try: return float(f[2])
    except: 
        try: return float(f[1])
        except: return None
# ---------- kalendarium
def merge():
    K={}
    for v in ['1570','1888','1906','1939','1954']:
        for line in open(f'{B}/Tabulae/Kalendaria/{v}.txt',encoding='utf-8'):
            line=line.strip()
            if not line or line[0] in '#*': continue
            parts=line.split('=')
            K[parts[0]]=parts[1].split('~')
    return K
KAL=merge()
def transfers(year,easter):
    letter='abcdefg'[(D(year,1,1)-D(year,1,1)).days]  # placeholder
    # dominical letter: first Sunday of year: Jan1=A..Jan7=G
    j=D(year,1,1); off=(6-j.weekday())%7  # days to Sunday
    letter='abcdefg'[off]
    T={}
    for fn in [f'{letter}.txt', f'{easter.month}{easter.day:02d}.txt']:
        p=f'{B}/Tabulae/Transfer/{fn}'
        if not os.path.exists(p): continue
        for line in open(p,encoding='utf-8'):
            line=line.strip()
            if not line or line[0]=='#' or not re.match(r'^\d\d-\d\d=',line): continue
            k,rest=line.split('=',1)
            val,_,vers=rest.partition(';;')
            vs=vers.split()
            if '1954' in vs: T[k]=('1954',val)
            elif 'DA' in vs and not (k in T and T[k][0]=='1954'): T[k]=('DA',val)
    return letter,{k:v[1] for k,v in T.items()}
def easter(y):
    a=y%19;b=y//100;c=y%100;d=b//4;e=b%4;f=(b+8)//25;g=(b-f+1)//3;h=(19*a+b-d-g+15)%30;i=c//4;k=c%4;l=(32+2*e+2*i-h-k)%7;m=(a+11*h+22*l)//451;mo=(h+l-7*m+114)//31;da=((h+l-7*m+114)%31)+1
    return D(y,mo,da)
