import json,re,csv,difflib,unicodedata,collections,sys
from spellchecker import SpellChecker
B='/tmp/claude-0/berl/'
sp=SpellChecker(language='fr')
dj=json.load(open(B+'djvu_pages.json'))
def tess(i):
    ws=[];
    with open(f'{B}tess/{i}.tsv',encoding='utf-8') as f:
        for r in csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE):
            if r['level']=='5' and r['text'].strip():
                ws.append((r['text'],(int(r['left']),int(r['top']),int(r['width']),int(r['height'])),(r['block_num'],r['par_num'],r['line_num'])))
    return ws
def key(w):
    w=unicodedata.normalize('NFC',w).replace('’',"'").replace('‘',"'")
    w=re.sub(r"'+","'",w)
    return re.sub(r"[^\wÀ-ÿœŒ']|_","",w).lower()
agree=collections.Counter()
def known(w):
    k=key(w)
    if not k: return True
    parts=[p for p in re.split(r"['\-]",k) if p]
    return all(p in sp or p.isdigit() or agree[p]>=1 for p in parts) and not re.search(r"[\^\d]",k.replace('1','') if False else k) or k.isdigit()
res={}
first=True
for phase in (0,1):
  flags=[]
  for i in range(18,306):
    A=[(w,li) for li,l in enumerate(dj[i]) for w,_ in l]
    AC=[c for li,l in enumerate(dj[i]) for _,c in l]
    T=tess(i)
    ka=[key(w) for w,_ in A]; kb=[key(w) for w,*_ in T]
    sm=difflib.SequenceMatcher(None,ka,kb,autojunk=False)
    ops=sm.get_opcodes()
    if phase==0:
        for tag,a1,a2,b1,b2 in ops:
            if tag=='equal':
                for k in ka[a1:a2]:
                    for p in re.split(r"['\-]",k):
                        if p: agree[p]+=1
        continue
    # build corrected word list for page with A line indices
    out=[]  # (word, line, flag or None)
    for tag,a1,a2,b1,b2 in ops:
        if tag=='equal':
            for k,kb_ in zip(range(a1,a2),range(b1,b2)):
                aw_=A[k][0]; bw_=T[kb_][0].replace('’',"'")
                bad=lambda w: re.search(r"[\^£<>|\[\]{}~*#@&$]|^'|'$",w)
                out.append((bw_ if bad(aw_) and not bad(bw_) else aw_,A[k][1],None))
            continue
        aw=[A[k][0] for k in range(a1,a2)]; bw=[T[k][0] for k in range(b1,b2)]
        while bw and (not key(bw[0]) or (len(key(bw[0]))==1 and not aw[:1]==bw[:1] and len(bw)>1)): bw=bw[1:]
        ja0=None
        line=A[a1][1] if a1<len(A) else (A[-1][1] if A else 0)
        ak=all(known(w) for w in aw); bk=all(known(w) for w in bw)
        ja=''.join(key(w) for w in aw); jb=''.join(key(w) for w in bw)
        if ja==jb and not bw==aw:  # same letters, punctuation/spacing difference
            bad=lambda w: re.search(r"[\^£<>|\[\]{}~*#@&$]|^'|'$",w)
            if any(bad(w) for w in aw) and not any(bad(w) for w in bw):
                out+=[(w.replace('’',"'"),line,None) for w in bw]
            else: out+=[(w,A[k][1],None) for w,k in zip(aw,range(a1,a2))]
            continue
        if not aw and all(not key(w) for w in bw): continue  # tess extra punctuation noise
        if all(re.fullmatch(r"[\d—–\-| ]*",w) for w in aw) and any(re.search(r"\d",w) for w in aw):
            out+=[(w,A[k][1],None) for w,k in zip(aw,range(a1,a2))]; continue
        if not bw:
            out+=[(w,A[k][1],None) for w,k in zip(aw,range(a1,a2))]; continue
        if not aw:
            if all(known(w) and len(key(w))>=2 and key(w).replace("'","").replace('-','').isalpha() for w in bw) and len(''.join(bw))>=3: pass
            else: continue
        if ja.lower()==jb.lower() or (ja.replace('â','a')==jb.replace('â','a')):
            out+=[(w,A[k][1],None) for w,k in zip(aw,range(a1,a2))]; continue
        if not bw and ak and all(len(key(w))<=1 for w in aw):
            out+=[(w,A[k][1],None) for w,k in zip(aw,range(a1,a2))]; continue
        if bk and not ak and bw:
            out+=[(w,line,None) for w in bw]; continue
        if ak and not bk and aw:
            out+=[(w,A[k][1],None) for w,k in zip(aw,range(a1,a2))]; continue
        # unresolved
        box=None
        if b1<b2:
            xs=[T[k][1] for k in range(b1,b2)]
            box=(min(x[0] for x in xs),min(x[1] for x in xs),max(x[0]+x[2] for x in xs),max(x[1]+x[3] for x in xs))
        fid=len(flags)
        flags.append({'id':fid,'page':i,'a':' '.join(aw),'b':' '.join(bw),'box':box,'boxA':[AC[k] for k in range(a1,min(a2+1,len(AC)))][:1]+[AC[k] for k in range(max(a1,a2-1),min(a2,len(AC)))],'ctxA':' '.join(x[0] for x in A[max(0,a1-4):a2+4])})
        out.append(('⟦%d⟧'%fid,line,fid))
    res[i]=out
json.dump(flags,open(B+'flags.json','w'),ensure_ascii=False,indent=0)
json.dump(res,open(B+'merged.json','w'),ensure_ascii=False)
print(len(flags))
