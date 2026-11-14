import json,re,glob,collections
G='/tmp/claude-0/gu/'; R='/home/user/hortus-sacrum/data/recueils/gueranger/'
clean=json.load(open(G+'clean.json')); m=json.load(open(G+'match.json'))
def tidy(t):
    t=t.replace('’',"'").replace('’',"'")
    t=re.sub(r'\s*\n\s*',' ',t); t=re.sub(r' {2,}',' ',t).strip()
    return t
JUNK=re.compile(r'(Societas pro canonizatione|Publié le|Published on|Partager|Share this|abbe-pivert|Abbé Pivert|Lire la suite|Aller au contenu|Skip to content)',re.I)
out={}; n=0
for f in sorted(glob.glob(R+'v*.json')):
    v=json.load(open(f)); ch=False
    for ei,e in enumerate(v['entrees']):
        r=m.get(f"{v['tome']}:{ei}")
        if not r or r['cov']<0.5: continue
        ps=[]
        for k,t in clean[r['url']][r['a']:r['b']+1]:
            t=tidy(t)
            if not t or JUNK.search(t): continue
            ps.append(('## '+t) if k=='H' and len(t)<120 else t)
        if sum(len(p) for p in ps)<300: continue
        e['corps']='\n\n'.join(ps); e['source']=r['url']; ch=True; n+=1
    out[f]=v
print(n)
json.dump(out,open(G+'built.json','w'),ensure_ascii=False)
