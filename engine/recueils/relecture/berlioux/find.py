import json,sys,re
from PIL import Image,ImageDraw,ImageFont
B='/tmp/claude-0/berl/'
dj=json.load(open(B+'djvu_pages.json'))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
qs=[l.rstrip('\n') for l in open(B+'q.txt',encoding='utf-8') if l.strip()]
parts=[]
for q in qs:
    hit=None
    for i in range(18,306):
        for li,l in enumerate(dj[i]):
            s=' '.join(w for w,_ in l)
            if q in re.sub(r'\s+',' ',s): hit=(i,li); break
        if hit: break
    if not hit: print('NOT FOUND',q); continue
    i,li=hit; im=Image.open(f'{B}img/{i}.jpg').convert('L')
    ls=dj[i][max(0,li-1):li+2]
    cs=[list(map(int,c.split(','))) for l in ls for _,c in l]
    y0=min(c[3] for c in cs)-15; y1=max(c[1] for c in cs)+15
    cr=im.crop((0,y0,im.width,y1)); cr=cr.resize((1000,int(cr.height*1000/im.width)))
    lab=Image.new('L',(1000,24),255); ImageDraw.Draw(lab).text((4,2),f'p{i} «{q}»',font=font,fill=0)
    parts+=[lab,cr]
H=sum(p.height for p in parts); sh=Image.new('L',(1000,H),255); y=0
for p in parts: sh.paste(p,(0,y)); y+=p.height
sh.save(B+'q.png'); print(H)
