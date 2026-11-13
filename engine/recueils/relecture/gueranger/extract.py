import re,html,json
G='/tmp/claude-0/gu/'
out={}
for l in open(G+'map.txt'):
    u,f=l.split()
    if u in out: continue
    s=open(G+f,encoding='utf-8',errors='ignore').read()
    m=re.search(r'<div[^>]+class="[^"]*(entry-content|post-content|elementor-widget-theme-post-content)[^"]*"',s)
    body=s[m.start():] if m else s
    body=re.split(r'<footer|class="[^"]*(sharedaddy|post-navigation|comments-area|jp-relatedposts)',body)[0]
    body=re.sub(r'<sup[^>]*>.*?</sup>','',body,flags=re.S)
    body=re.sub(r'<(script|style)[^>]*>.*?</\1>','',body,flags=re.S)
    paras=[]
    for tag,inner in re.findall(r'<(p|h[1-6]|li|blockquote)[^>]*>(.*?)</\1>',body,flags=re.S):
        t=html.unescape(re.sub(r'<br\s*/?>','\n',inner)); t=re.sub(r'<[^>]+>','',t)
        t=re.sub(r'[ \t ]+',' ',t).strip()
        if t: paras.append(('H' if tag[0]=='h' else 'P',t))
    out[u]=paras
json.dump(out,open(G+'clean.json','w'),ensure_ascii=False)
print(sum(len(v) for v in out.values()), sum(len(t) for v in out.values() for _,t in v)//1000,'k chars')
for u,v in list(out.items())[:3]: print(u,len(v),v[:3])
