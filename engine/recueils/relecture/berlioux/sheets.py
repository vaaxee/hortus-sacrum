import json
from PIL import Image,ImageDraw,ImageFont
B='/tmp/claude-0/berl/'
F=json.load(open(B+'flags.json'))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
W=1100;per=14
def band(f):
    im=Image.open(f"{B}img/{f['page']}.jpg")
    if f['box']: y0,y1=f['box'][1],f['box'][3]; x0,x1=f['box'][0],f['box'][2]
    else:
        cs=[list(map(int,c.split(','))) for c in f['boxA']]
        y0=min(c[3] for c in cs); y1=max(c[1] for c in cs); x0=min(c[0] for c in cs); x1=max(c[2] for c in cs)
    h=y1-y0
    y0=max(0,y0-40-max(0,110-h)//2); y1=min(im.height,y1+40+max(0,110-h)//2)
    if y1-y0>380: y1=y0+380
    cr=im.crop((0,y0,im.width,y1)).convert('L')
    d=ImageDraw.Draw(cr); d.rectangle((x0-8,max(0,(f['box'] or [0,0])[1]-y0-6) if f['box'] else 2,x1+8,cr.height-3),outline=0,width=3)
    s=W/cr.width; return cr.resize((W,int(cr.height*s)))
for n in range(0,len(F),per):
    parts=[]
    for f in F[n:n+per]:
        b=band(f); lab=Image.new('L',(W,26),255); ImageDraw.Draw(lab).text((4,2),f"#{f['id']} p{f['page']}  A=«{f['a']}»  B=«{f['b']}»"[:110],font=font,fill=0)
        parts+=[lab,b]
    H=sum(p.height for p in parts); sh=Image.new('L',(W,H),255); y=0
    for p in parts: sh.paste(p,(0,y)); y+=p.height
    sh.save(f"{B}sheets/s{n//per:02d}.png")
print(len(F)//per+1)
