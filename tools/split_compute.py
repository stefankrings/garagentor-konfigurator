import sys,re
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
start=s.index('function compute(c){\n'); endm=' return finish(applyPx(out,s));\n}\n'; end=s.index(endm,start)+len(endm)
body=s[start+len('function compute(c){\n'):end-len(endm)]
M=[(' const surfTxt=','tor'),(' { const mm=hfMM(s);','hf'),(' // Beschlag-Mehrpreis','beschlag'),(' // Fenster\n','fenster'),(' // Design\n','design'),(' // Schlupftür\n','tuer'),(' // Sonderausführungen','sonder'),(' // Antrieb & Zubehör','zubehoer'),(' // Eigene Leistungen','montage')]
pos=[(body.index(a),n) for a,n in M]; assert pos==sorted(pos)
seg={'ctx':body[:pos[0][0]]}
for i,(p,n) in enumerate(pos): seg[n]=body[p:(pos[i+1][0] if i+1<len(pos) else len(body))]
ctx=seg['ctx']
a='return finish(applyPx(out,s))}'; assert ctx.count(a)==1; ctx=ctx.replace(a,'return {fertig:finish(applyPx(out,s))}}')
NAME={'tor':'preisTor','hf':'preisHoeherfuehrung','beschlag':'preisBeschlag','fenster':'preisFenster','design':'preisDesign','tuer':'preisSchlupftuer','sonder':'preisSonderausfuehrung','zubehoer':'preisZubehoer','montage':'preisMontage'}
DOC={'tor':'Torposition: Grundpreis lt. Tabelle, Positionstext (Paneel, Oberfläche, Farbe, Beschlag, Antrieb, Dichtung), Antrieb/MKA/Griff, Dekor, RAL-Mehrpreis',
 'hf':'Zargenhöherführung 60/110 mm','beschlag':'Beschlag: Einsatzgrenzen Beschlag 8, Mehrpreis 6.(NU)/Comfort Plus, Hinweis Schlupftür',
 'fenster':'Fenster und Lichtbänder inkl. Zusatzfelder, RAL-Rahmen, Milchglas','design':'Designapplikationen (Highlight, Exklusiv) und Designsockelblende – nur glatt senso',
 'tuer':'Schlupftür mit Optionen; Fenster im Türbereich','sonder':'Sonderausführungen (OPTIONS) und zugehörige Hinweise',
 'zubehoer':'Antriebszubehör, Montagezubehör (Blenden, Profile …), eigene Positionen','montage':'Montageleistungen: Montage, Ausbau, Fuge, Auffüttern, eigene Montagepositionen (Arbeitskosten)'}
names=['s','out','L','lk','grp','sq']
def head(b):
    used=[x for x in names if re.search(r'(?<![\w$.])'+x+r'(?![\w$])',b)]
    return ' const {'+','.join(used)+'}=P;\n'
out=['/* ================= PREISBERECHNUNG =================\n   compute(c) liefert alle Angebotszeilen mit Preisen. Die Teile hängen über L() Zeilen an P.out an;\n   Reihenfolge = Reihenfolge im Angebot. Preise: kind "h" = Herstellerliste × (TZ, Aufschlag), "l" = eigene Leistung. */\n']
out.append('/* Grundlagen: Faktor, Zeilen-Helfer L(), Prüfungen Motiv/Farbe/Tabelle. Ohne Maße: {fertig} */\nfunction preisKontext(c){\n'+ctx+' return {s,out,L,lk,grp,sq};\n}\n')
for k,n in NAME.items():
    b=seg[k]; out.append(f'/* {DOC[k]} */\nfunction {n}(P){{\n'+head(b)+b+'}\n')
out.append('function compute(c){\n const P=preisKontext(c); if(P.fertig) return P.fertig;\n '+' '.join(f'{n}(P);' for n in NAME.values())+'\n return finish(applyPx(P.out,P.s));\n}\n')
s=s[:start]+''.join(out)+s[end:]; open(f,'w',encoding='utf-8').write(s); print('ok',{k:len(v) for k,v in seg.items()})
