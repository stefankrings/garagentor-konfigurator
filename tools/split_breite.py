import sys
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
i=s.index('/* Breite: Zarge,'); j=s.index('\n}\n',s.index('function aufBreite(X){',i))+3; old=s[i:j]
L=old.split('\n')
def find(prefix): return next(k for k,l in enumerate(L) if l.startswith(prefix))
a=find('   // Tor in der Öffnung'); b=find('  else { const an=')
inO='\n'.join(L[a:b])   # endet mit '...lichten Öffnung`); }'
assert inO.rstrip().endswith('}'); inO=inO.rstrip()[:-1].rstrip()   # schließende Klammer des if-Zweigs weg
sd0=find('  else { const an='); sd1=find('   if(!R.probB&&side[0]')
seiten='\n'.join(L[sd0:sd1]).replace('  else { const an=','  const an=',1)
st0=sd1; st1=find(' }')
stdb='\n'.join(L[st0:st1])
assert stdb.rstrip().endswith('} } } } }'); stdb=stdb.rstrip()[:-2].rstrip()  # schließende Klammer des else-Zweigs weg
new='''/* Breite (Ablauf): Tor in der Öffnung oder Zarge auf Anschlag/Wand */
function aufBreite(X){
 if(X.B1==null) return;
 if(X.a.seite==="stumpf_in"){ aufBreiteInOeffnung(X); return; }
 aufBreiteSeiten(X); aufStandardbreite(X);
}
/* Tor in der Öffnung: Zarge in der Laibung, Durchfahrt wird kleiner; Sonderzarge 50 mm bringt je Seite 30 mm (nur 6.(NU), max. 3500 mm) */
function aufBreiteInOeffnung(X){
 const {a,R,B1,SP,z50ok,szvQ}=X; const c=X.c;
'''+'\n'.join(l for l in inO.split('\n')[1:])+'''
}
/* Zarge auf Anschlag/Wand: nutzbarer Seitenplatz je Seite; reicht er nicht → Sonderbreite (asym/sym) oder Sonderzarge 50 mm */
function aufBreiteSeiten(X){
 const {a,v,R,B1,V,SP,z50ok,szvQ}=X;
'''+seiten+''' X.side=side; X.an=an;
}
/* Standardbreite statt Sonderbreite, wenn die Öffnung bis 15 mm schmaler ist und der Seitenplatz die Überdeckung erlaubt */
function aufStandardbreite(X){
 const {a,R,B1,SP,side,an}=X;
'''+stdb+'''
}
'''
s=s[:i]+new+s[j:]; open(f,'w',encoding='utf-8').write(s); print('ok')
