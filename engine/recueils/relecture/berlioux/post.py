import json,re,sys
from functools import lru_cache
from spellchecker import SpellChecker
sp=SpellChecker(language='fr')
B='/tmp/claude-0/berl/'
e=json.load(open(B+'ent.json'))
def kn1(w): return w.lower() in sp or w.lower() in EXTRA
def kn(w):
    ps=[p for p in re.split(r"['\-]",w) if p]
    return bool(ps) and all(kn1(p) or len(p)==1 for p in ps)
SKIP=set('crucior recordaremur amici crucifié convers compasion acccueille connaisnaissance surabondamment ensanglante trouvasse cinquièmement quatrièmemement'.split())
NOHY={'et','dont','seulement','si','que','qui','lorsque','ou','mais','quoique'}
EXTRA=set('cœur cœurs sœur sœurs œuvre œuvres vœu vœux consolatrice consolateur expiatrices expiatrice satisfactoire satisfactoires austérités eût fût abjuré abjura mémoraison béatifique purgatoire ici-bas amertumes'.split())
ENCL=['leur','leurs','moi','toi','lui','nous','vous','même','mêmes','être','elle','elles','il','ils','on','en','y','aimé','aimée','aimés','aimées','là','ci']
log=[]
@lru_cache(None)
def seg(w):
    if not w: return []
    best=None
    for i in range(1,len(w)+1):
        a=w[:i]
        if (len(a)>1 or a.lower() in ('à','a','y')) and kn(a):
            r=seg(w[i:])
            if r is not None and (best is None or len(r)+1<len(best)): best=[a]+r
    return best
def fixword(m):
    pre,w,post=m.group(1),m.group(2),m.group(3)
    if not w or w.lower() in SKIP or kn(w) or "'" in w and all(kn(p) or len(p)==1 for p in w.split("'")): return m.group(0)
    lw=w
    # -t- inversions
    mm=re.fullmatch(r"(.+?)-?t-?(il|elle|on|ils|elles)",w)
    if mm and kn(mm.group(1)) and ('-' in w):
        r=f"{mm.group(1)}-t-{mm.group(2)}"; log.append((w,r)); return pre+r+post
    mm=re.fullmatch(r"(.+?)t-(il|elle|on)",w)
    if mm and kn(mm.group(1)): r=f"{mm.group(1)}-t-{mm.group(2)}"; log.append((w,r)); return pre+r+post
    for enc in sorted(ENCL,key=len,reverse=True):
        if w.lower().endswith(enc) and len(w)>len(enc)+1 and kn(w[:-len(enc)]) and w[:-len(enc)].lower() not in ('l','d','s','n') and w[:-len(enc)].lower() not in NOHY:
            r=w[:-len(enc)]+'-'+w[-len(enc):]
            log.append((w,r)); return pre+r+post
    if re.fullmatch(r"[a-zà-ÿœ]+",w) and len(w)>=7:
        s=seg(w)
        if s and len(s)<=4: r=' '.join(s); log.append((w,r)); return pre+r+post
    # F/T for l'
    mm=re.fullmatch(r"[FT]([a-zàâéèêîôûœ].+|[AEÉIOU][a-zé].+)",w)
    if mm and kn(mm.group(1)) and not kn(w): r="l'"+mm.group(1); log.append((w,r)); return pre+r+post
    return m.group(0)
def clean(t):
    t=t.replace('’',"'").replace('‘',"'")
    t=re.sub(r"[^\s]*\^*R[Ee]M[iI]ER\s+(POINT|point)",'PREMIER POINT',t)
    t=re.sub(r"(?i)(?<![\wÀ-ÿ])\^*premier\s+point",'PREMIER POINT',t)
    t=re.sub(r"\b([cdjlmnst]|qu)\^\s?(?=[a-zàâéèêîôûœA-ZÉ])",r"\1'",t)
    t=re.sub(r"(?<=\w)\^+(?=[\s,.;:!?])",'',t)
    t=re.sub(r"(?<!\S)\^+(?!\S)\s?",'',t)
    def hy(m):
        a,b=m.group(1),m.group(2)
        if kn(a+b): return a+b
        if kn(a+'-'+b) and a[0].isupper()==False: return a+'-'+b
        return m.group(0)
    t=re.sub(r"([\wÀ-ÿœ]+)- (?:— )?([a-zà-ÿœ]+)",hy,t)
    t=re.sub(r"(?<![\w°])0(?=\s+[A-ZÉa-zàâéèêîôû])",'O',t)
    t=re.sub(r"(?<!\S)([^\s\wÀ-ÿœ«»—(\"“]*)([\wÀ-ÿœŒæ'\-]+)([^\s\wÀ-ÿ]*)(?!\S)",fixword,t)
    def head(m):
        h=m.group(2)
        if h.isupper() or re.search(r"[A-ZÉ]{3,}",h): h=h[0]+h[1:].lower() if h[:2]!='IL' else 'Il'+h[2:].lower()
        for a,b in [('dieu','Dieu'),('purgatoire','Purgatoire'),('âmes','Ames'),('ames','Ames'),('ciel','Ciel'),('jésus','Jésus'),('christ','Christ'),('marie','Marie'),('nous','nous')]:
            h=re.sub(r"\b"+a+r"\b",b,h)
        h=re.sub(r"^Nous ([A-ZÉ]+)",lambda k:'Nous '+k.group(1).lower(),h)
        return m.group(1)+h
    def num(m):
        n=m.group(2); return m.group(1)+('1°' if n[0] in '14' else '2°')+' '
    t=re.sub(r"(^|\n|[.:] )(19|10|40|49|4°|1»|1<>|1\^|20|29|90|920|2<>|2\^|2o)\s+(?=[A-ZÉÈ]{2,}|Il |L'aum)",num,t)
    ps=t.split('\n\n'); out=[]
    for p in ps:
        p=p.strip()
        if not p: continue
        if out and not re.search(r"[.!?»:…]$",out[-1]) and re.match(r"[a-zàâçéèêîôûœ]",p): out[-1]+=' '+p
        else: out.append(p)
    return '\n\n'.join(out)
for x in e: x['corps']=clean(x['corps']); x['titre']=clean(x['titre'])
json.dump(e,open(B+'ent2.json','w'),ensure_ascii=False)
for a,b in log: print(a,'->',b)
