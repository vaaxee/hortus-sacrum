import json,glob,re,random,sys
from spellchecker import SpellChecker
sp=SpellChecker(language='fr'); LAT=set()
for b in json.load(open('/tmp/claude-0/vul/v.json'))['books']:
    for c in b['chapters']:
        for v in c['verses']: LAT.update(w.lower() for w in re.findall(r'[a-zæœA-ZÆŒ]+',v['text']))
W=lambda w: re.findall(r"[A-Za-zÀ-ÿœŒæÆ]+",w)
dico=lambda w: bool(W(w)) and all(x.lower() in sp or x.lower() in LAT for x in W(w))
def dist(x,y):
    d=list(range(len(y)+1))
    for i,cx in enumerate(x,1):
        p,d[0]=d[0],i
        for j,cy in enumerate(y,1): p,d[j]=d[j],min(d[j]+1,d[j-1]+1,p+(cx!=cy))
    return d[-1]
k=lambda w: re.sub(r"[^\wÀ-ÿœæ']",'',w.replace('’',"'")).lower()
COURTS=set()
for bb,aa in {'de':'ae àe âe cie cle dc ds ûe cîe cfe cte cce dv dj ue','et':'el ot','la':'ia îa ja ki','que':'gue aue cjue','où':'oii oit oîi oà','des':'cies','les':'ies jes','du':'ju clu dvi ciu dli dïi','un':'im','est':'esi','en':'eh eri','fit':'ht tit','fin':'hn rin','dès':'ciès'}.items():
    for x in aa.split(): COURTS.add((x,bb))
out=[]
for f in sorted(glob.glob('/tmp/claude-0/gu*/corrections*.json')):
    C=json.load(open(f)); dec=[]
    for i,c in enumerate(C):
        a,b=c['a'],c['b']
        if c['auto'] or dico(a) or not dico(b): continue
        if re.fullmatch(r"[A-ZÉ][a-zé]{1,5}\.",a) or re.search(r'\d',a+b): continue  # abréviations, chiffres
        if len(k(b))<2 or dist(k(a),k(b))>2 or len(W(a))!=len(W(b)): continue
        # mêmes signes de ponctuation autour
        if re.sub(r'[\wÀ-ÿœŒæÆ]','',a.replace('’',"'")).strip("'")!=re.sub(r'[\wÀ-ÿœŒæÆ]','',b.replace('’',"'")).strip("'"): continue
        if len(k(b))<=3 and (k(a),k(b)) not in COURTS: continue
        if a in ('Epoux','tète,','boure','rièrc','vni,','rerrcur',"'epuis",'ressentirai-jc'): continue
        dec.append(f'{i}\t{b}'); out.append((a,b))
    s=f.split('corrections')[1][:-5]
    open(f.replace(f'corrections{s}.json',f'dec{s}.txt'),'w').write('\n'.join(dec)+'\n')
print(len(out)); random.seed(1)
if '-v' in sys.argv: print(' | '.join(f'{a}→{b}' for a,b in random.sample(out,250)))
