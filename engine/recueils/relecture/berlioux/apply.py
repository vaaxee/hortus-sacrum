import json,re,sys,html
sys.path.insert(0,'/home/user/hortus-sacrum/engine/recueils')
from pathlib import Path
B='/tmp/claude-0/berl/'
dj=json.load(open(B+'djvu_pages.json')); merged=json.load(open(B+'merged.json')); flags=json.load(open(B+'flags.json'))
dec={}
for l in open(B+'dec.txt',encoding='utf-8'):
    l=l.rstrip('\n')
    if not l: continue
    k,_,v=l.partition('\t'); dec[int(k)]=v
def key(w): return re.sub(r"[^\wÀ-ÿœŒ]|_","",w.replace('’',"'")).lower()
def res(f):
    v=dec.get(f['id'])
    if v is None or v=='A': return f['a']
    if v=='B': return f['b']
    if v=='B?':
        ck=key(f['ctxA'])
        return f['a'] if key(f['b']) in ck else f['b']
    return v
pages=[]
pe=json.load(open(B+'paraends.json'))
for i,p in enumerate(dj):
    ov=Path(f'{B}over/{i}.txt')
    if ov.exists(): pages.append(ov.read_text(encoding='utf-8').rstrip('\n')); continue
    if str(i) in merged:
        lines={}
        for w,li,fid in merged[str(i)]:
            if fid is not None: w=res(flags[fid])
            if w: lines.setdefault(li,[]).append(w)
        n=len(dj[i])
        pages.append('\n'.join(' '.join(lines.get(li,[]))+('\n' if li in pe[i] else '') for li in range(max([n]+[k+1 for k in lines]))))
    else:
        pages.append('\n'.join(' '.join(w for w,_ in l)+('\n' if li in pe[i] else '') for li,l in enumerate(p)))
txt='\n'.join(pages)
txt=re.sub(r'[ \t]+',' ',txt)
txt=re.sub(r'^([A-ZÈ-]+IÈME)\s*\nJOUR',r'\1 JOUR',txt,flags=re.M)
Path(B+'src').mkdir(exist_ok=True); Path(B+'src/moisdesamesdupur00berl.txt').write_text(txt,encoding='utf-8')
import mois
mois.SRC=Path(B+'src')
ent=mois.decouper('moisdesamesdupur00berl')
json.dump(ent,open(B+'ent.json','w'),ensure_ascii=False)
print(len(ent),[len(e['corps'])//1000 for e in ent])
