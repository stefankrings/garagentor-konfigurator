# GeoNames DE.txt -> teilorte-deutschland.json (Dörfer, Stadt- und Ortsteile je Gemeinde)
import sys,json,re
F=sys.argv[1]; rows=[l.rstrip('\n').split('\t') for l in open(F,encoding='utf-8')]
def gname(n):
    n=re.sub(r',.*','',n).strip()
    n=re.sub(r'\ba\.d\.\s*','an der ',n); n=re.sub(r'\bi\.d\.\s*','in der ',n); n=re.sub(r'\bb\.\s*','bei ',n)
    return re.sub(r'\s+',' ',n)
G={r[13]:[gname(r[1]),round(float(r[4]),3),round(float(r[5]),3),set()] for r in rows if r[7]=='ADM4' and r[13]}
BAD=re.compile(r'(stra(ß|ss)e|ufer|platz|park|damm|allee|bahnhof|\btor$|\s{2})',re.I)
for r in rows:
    if r[6]!='P' or r[7] not in ('PPL','PPLX','PPLA4','PPLA3','PPLA2','PPLA','PPLC'): continue
    g=G.get(r[13]); n=r[1].strip()
    if not g or n==g[0] or '/' in n or BAD.search(n): continue
    if re.match(re.escape(g[0])+r'[\s-]',n) and not re.match(re.escape(g[0])+r'-\w+$',n): continue   # "Berlin Köpenick", "Berlin - …"
    g[3].add(n)
out={"v":1,"quelle":"GeoNames (CC BY 4.0)","g":[[g[0],g[1],g[2],sorted(g[3])] for g in G.values() if g[3]]}
json.dump(out,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(len(out['g']),'Gemeinden',sum(len(g[3]) for g in out['g']),'Teilorte')
