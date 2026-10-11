import json,sys,os
def teil():
    f='teilorte/teilorte-deutschland.json'
    if not os.path.exists(f): return '""'
    d=json.load(open(f,encoding='utf-8'))
    return json.dumps('\n'.join(f"{n}@{la};{lo}="+'/'.join(x for x in t if '/' not in x) for n,la,lo,t in d['g'] if t and '=' not in n and '@' not in n),ensure_ascii=False)

SRC=sys.argv[1] if len(sys.argv)>1 else 'template.html'; OUT=sys.argv[2] if len(sys.argv)>2 else 'Garagentor-Konfigurator.html'
t=open(SRC,encoding='utf-8').read()
pr=json.load(open('prices.json')); ral={}
for l in open('ral.txt',encoding='utf-8'):
    l=l.strip()
    if l: k,h,n=l.split('|'); ral[k]=[h,n]
wi=json.load(open('win_thumbs.json'))
out=t.replace('__PRICES__',json.dumps(pr,separators=(',',':'))).replace('__RAL__',json.dumps(ral,ensure_ascii=False,separators=(',',':'))).replace('__WINIMG__',json.dumps(wi,separators=(',',':'))).replace('__BRIEF__',open('brief.json').read()).replace('__BESCH__',open('besch.json').read()).replace('__ZUBIMG__',open('zubimg.json').read()).replace('__TEILORTE__',teil()).replace('__PLZ__',json.dumps(open('plz.txt',encoding='utf-8').read(),ensure_ascii=False)).replace('__FASSADEN__',open('fassaden.json').read()).replace('__PDFLIBS__',(open('libs/html2canvas.min.js').read()+'\n'+open('libs/jspdf.umd.min.js').read()).replace('</script','<\\/script'))
open(OUT,'w',encoding='utf-8').write(out)
