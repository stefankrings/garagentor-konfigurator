import sys,re
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
start=s.index('function aufSvg(a){\n'); end=s.index('\n return h+v;\n}\n',start)+len('\n return h+v;\n}\n')
body=s[start+len('function aufSvg(a){\n'):end-len(' return h+v;\n}\n')]
i1=body.index(' // ───────── Draufsicht'); i2=body.index(' // ───────── Seitenschnitt')
ctx=body[:i1]; top=body[i1:i2]; cut=body[i2:]
# W und DPX in den Kontext
a1=' const DPX=.25;\n'; assert top.count(a1)==1; top=top.replace(a1,'')
a2=' const W=440, c=220,'; assert top.count(a2)==1; top=top.replace(a2,' const c=220,')
ctx=ctx+' const DPX=.25, W=440; /* Tiefenmaßstab (beide Ansichten) und Zeichnungsbreite */\n'
# Detail Bodenprofil herauslösen
d0=cut.index(' if(DET){ // Detail Bodenprofil'); d1=cut.index(' v+=`</svg>`;',d0)
det=cut[d0:d1]; cut=cut[:d0]+' if(DET) v+=aufSvgBodenDetail(Z,FLOOR);\n'+cut[d1:]
det=det.replace(' if(DET){ // Detail Bodenprofil (vergrößert, ca. 1,6 px/mm)',' {',1)
names=['a','MC','wall','door','K','FL','val','lw','lbl','gl','ln','ext','tick','txtOf','lab','hchain','vchain','zz','poly','defs','PX','num','cl','RC','PB','SOLB','SPmm','zW','SHIFT','DPX','W']
def head(b):
    used=[x for x in names if re.search(r'(?:(?<![\w$.])|(?<=\.\.\.))'+re.escape(x)+r'(?![\w$])',b)]
    return ' const {'+','.join(used)+'}=Z;\n'
out='''/* ================= AUFMASS-ZEICHNUNG =================
   aufSvg(a): Draufsicht + Seitenschnitt (nicht maßstäblich) mit Maßketten; Kürzel-Beschriftungen sind antippbar (data-k). */
/* Zeichenwerkzeuge, Maßstab und das Aufmaß-Ergebnis, das beide Ansichten brauchen */
function aufSvgKontext(a){
'''+ctx+' return {a,MC,wall,door,K,FL,val,lw,lbl,gl,ln,ext,tick,txtOf,lab,hchain,vchain,zz,poly,defs,PX,num,cl,RC,PB,SOLB,SPmm,zW,SHIFT,DPX,W};\n}\n'
out+='/* Draufsicht: Laibungen/Anschläge, Zarge (rot, wenn sie nicht passt), Tor und Maßketten B1, AL/AR, SL/SR, T/V */\nfunction aufSvgDraufsicht(Z){\n'+head(top)+top+' return h;\n}\n'
out+='/* Seitenschnitt: Sturz, Decke, Boden, Platzbedarf des Beschlags, Schiene, Federn, Antrieb und Maßketten */\nfunction aufSvgSchnitt(Z){\n'+head(cut)+cut+' return v;\n}\n'
out+='/* Detail Bodenprofil (vergrößert, ca. 1,6 px/mm): L-/Z-Profil oder bauseitiger Ausgleich */\nfunction aufSvgBodenDetail(Z,FLOOR){\n'+head(det)+' let v="";\n'+det+' return v;\n}\n'
out+='function aufSvg(a){ const Z=aufSvgKontext(a); return aufSvgDraufsicht(Z)+aufSvgSchnitt(Z); }\n'
s=s[:start]+out+s[end:]; open(f,'w',encoding='utf-8').write(s); print('ok',len(ctx),len(top),len(cut),len(det))
