import json,re,unicodedata,collections,glob
G='/tmp/claude-0/gu/'; R='/home/user/hortus-sacrum/data/recueils/gueranger/'
clean=json.load(open(G+'clean.json'))
def norm(t):
    t=unicodedata.normalize('NFD',t.lower()); t=''.join(c for c in t if not unicodedata.combining(c))
    return re.findall(r'[a-z]{2,}',t.replace('œ','oe').replace('æ','ae'))
K=5
idx=collections.defaultdict(list)
urls=list(clean)
for ui,u in enumerate(urls):
    for pi,(k,t) in enumerate(clean[u]):
        w=norm(t)
        for i in range(len(w)-K+1): idx[' '.join(w[i:i+K])].append((ui,pi))
res={}
stats=collections.Counter()
for f in sorted(glob.glob(R+'v*.json')):
    v=json.load(open(f))
    for ei,e in enumerate(v['entrees']):
        w=norm(e['corps']); sh=[' '.join(w[i:i+K]) for i in range(0,max(0,len(w)-K+1))]
        if not sh: continue
        votes=collections.Counter(); hits=collections.defaultdict(list)
        for s in sh:
            for ui,pi in set(idx.get(s,[])): votes[ui]+=1; hits[ui].append(pi)
        if not votes: stats['none']+=1; continue
        best=None
        for ui,_ in votes.most_common(3):
            c=collections.Counter(hits[ui]); ps=sorted(c)
            # grappes de paragraphes consécutifs (écart <= 4)
            cl=[[ps[0]]]
            for p in ps[1:]:
                if p-cl[-1][-1]<=4: cl[-1].append(p)
                else: cl.append([p])
            g=max(cl,key=lambda k:sum(c[p] for p in k))
            sc=sum(c[p] for p in g)
            if not best or sc>best[0]: best=(sc,ui,g[0],g[-1])
        sc,ui,a,b=best
        # bornes précises : paragraphe propre correspondant au début et à la fin de la lecture OCR
        U=urls[ui]; maps=[]
        for op in e['corps'].split('\n\n'):
            w3=norm(op); s3={' '.join(w3[i:i+K]) for i in range(len(w3)-K+1)}
            if len(s3)<3: continue
            vv=collections.Counter(pi for x in s3 for (u2,pi) in idx.get(x,[]) if u2==ui and a-40<=pi<=b+40)
            if vv:
                pi,nv=vv.most_common(1)[0]
                if nv>=max(2,0.3*len(s3)): maps.append(pi)
        if maps:
            a=min(maps[:3]); b=max(maps[-3:])
            if b<a: a,b=min(maps),max(maps)
        span=set()
        for pi in range(a,b+1):
            w2=norm(clean[urls[ui]][pi][1]); span|={' '.join(w2[i:i+K]) for i in range(len(w2)-K+1)}
        cov=len(set(sh)&span)/len(set(sh))
        res[f"{v['tome']}:{ei}"]=dict(titre=e['titre'],cle=e['cle'],url=urls[ui],a=a,b=b,cov=round(cov,2),nocr=len(e['corps']),nclean=sum(len(t) for _,t in clean[urls[ui]][a:b+1]))
        stats['ok' if cov>=0.5 else 'low']+=1
json.dump(res,open(G+'match.json','w'),ensure_ascii=False,indent=0)
print(stats)
import statistics
ok=[r for r in res.values() if r['cov']>=0.5]
print('ratio clean/ocr median',statistics.median(r['nclean']/r['nocr'] for r in ok))
for r in sorted(ok,key=lambda r:r['nclean']/r['nocr'])[:8]+sorted(ok,key=lambda r:r['nclean']/r['nocr'])[-8:]: print(r['cle'],r['cov'],r['nocr'],r['nclean'],r['url'][-50:],r['a'],r['b'])
