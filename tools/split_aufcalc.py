# Zerlegt aufCalc in Teilfunktionen – rein mechanisch, Reihenfolge und Logik bleiben unverändert.
import re,sys
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
start=s.index('function aufCalc(a,c){ const c0=c;\n'); end=s.index(' return R;\n}\n',start)+len(' return R;\n}\n')
body=s[start+len('function aufCalc(a,c){ const c0=c;\n'):end-len(' return R;\n}\n')]
marks=[(' // Plausibilität','check'),(' // Breite\n','breite'),(' // Höhe + Beschlagsentscheidung','hoehe'),(' // Verstärktes Tor','verst'),(' // Versatz: Aufdopplung','versatz'),(' // Raumtiefe','raum'),(' // Boden\n','boden'),(' // Hinweise für den Angebots-Nachtext','texte'),(' // Höhenkürzung','kuerzung')]
pos=[(body.index(mk),nm) for mk,nm in marks]
assert pos==sorted(pos)
segs={'ctx':body[:pos[0][0]]}
for i,(p,nm) in enumerate(pos): segs[nm]=body[p:(pos[i+1][0] if i+1<len(pos) else len(body))]
for k,v in segs.items(): print(k,len(v))
# Kontext: alles, was mehrere Teile brauchen
ctx=segs['ctx']
HEAD=' const {a,m,v,R,B1,H1,V,SP,z50ok,szvQ,hfOn}=X; let c=X.c;\n'
# Höhe: Rücksprung bei unpassender Höherführung + aktualisierter Beschlag
h=segs['hoehe']
a1='if(cur&&!cur.ok) return aufCalc(Object.assign({},a,{solHf:"0"}),c0);'; assert h.count(a1)==1; h=h.replace(a1,'if(cur&&!cur.ok) return "neu"; /* gewählte Höherführung passt nicht → ohne neu rechnen */')
a2='c=Object.assign({},c,{beschlag:sel.k});'; assert h.count(a2)==1; h=h.replace(a2,'c=Object.assign({},c,{beschlag:sel.k}); X.c=c; /* folgende Teile rechnen mit dem gewählten Beschlag */')
segs['hoehe']=h
DOC={'check':'Plausibilität: widersprüchliche Maße als Fehler melden',
 'breite':'Breite: Zarge, Sonderbreite, Symmetrie, Standardbreite mit Überdeckung, Tor in der Öffnung',
 'hoehe':'Höhe und Beschlag: größte Torhöhe je Beschlag, Auswahl, Sturzhinweise, Sonder-/Standardhöhe, Blenden, Höherführung. Rückgabe "neu", wenn die gewählte Höherführung nicht passt',
 'verst':'Verstärktes Tor: Durchfahrtsverlust und Hinweise (auch „evtl. verstärkt“ bei heller Farbe)',
 'versatz':'Versetzter Anschlag: Auffüttern und Alublech',
 'raum':'Raumtiefe prüfen',
 'boden':'Höhenversatz im Boden: L-/Z-Profil oder bauseits',
 'texte':'Hinweistexte für den Angebots-Nachtext (alle bewusst getroffenen Entscheidungen)',
 'kuerzung':'Sonderhöhe: Kürzung der untersten Lamelle und Folgen für das Motiv'}
NAME={'check':'aufPruefen','breite':'aufBreite','hoehe':'aufHoehe','verst':'aufVerstaerkung','versatz':'aufVersatz','raum':'aufRaumtiefe','boden':'aufBoden','texte':'aufTexte','kuerzung':'aufKuerzung'}
out=['/* ================= AUFMASS-BERECHNUNG =================\n   aufCalc(a,c) wertet das Aufmaß a für die Konfiguration c aus und liefert R (Bestellmaß, Beschlag, Zubehör, Hinweise).\n   Die Teile laufen in fester Reihenfolge und teilen sich den Kontext X; X.c ist ab aufHoehe die Konfiguration mit gewähltem Beschlag. */\n']
out.append('function aufKontext(a,c){\n'+ctx.replace('\n',' \n',0)+' return {a,c,m,v,R,B1,H1,V,SP,z50ok,szvQ,hfOn};\n}\n')
for k in ['check','breite','hoehe','verst','versatz','raum','boden','texte','kuerzung']:
    seg=segs[k]
    out.append(f'/* {DOC[k]} */\nfunction {NAME[k]}(X){{\n'+HEAD+seg+('' if k!='hoehe' else '')+'}\n')
out.append('''function aufCalc(a,c){
 const X=aufKontext(a,c);
 aufPruefen(X); aufBreite(X);
 if(aufHoehe(X)==="neu") return aufCalc(Object.assign({},a,{solHf:"0"}),c);
 aufVerstaerkung(X); aufVersatz(X); aufRaumtiefe(X); aufBoden(X); aufTexte(X); aufKuerzung(X);
 return X.R;
}
''')
s=s[:start]+''.join(out)+s[end:]
open(f,'w',encoding='utf-8').write(s)
