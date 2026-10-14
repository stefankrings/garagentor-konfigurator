import sys
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
i=s.index('/* Höhe und Beschlag:'); j=s.index('/* Verstärktes Tor:',i); old=s[i:j]
def cut(a,b):  # Text zwischen a (inkl.) und b (exkl.)
    x=old.index(a); y=old.index(b,x); return old[x:y]
p_mass=cut('  const DH=v("DH"),','  const rtReq=')
p_wahl=cut('  const rtReq=','  // Hinweise zur Sturztiefe')
p_hinw=cut('  // Hinweise zur Sturztiefe','  if(a.sturz==="stumpf_in"){ if(dep2')
p_loes=cut('  if(a.sturz==="stumpf_in"){ if(dep2','  // Höherführung:')
p_hf=cut('  // Höherführung:','  c=Object.assign({},c,{beschlag:sel.k});')
# Sturz-Hinweise und Höhen-Lösung brauchen nF/dep2/nB aus der Beschlagswahl
p_hinw=p_hinw.replace('  // Hinweise zur Sturztiefe für den gewählten Beschlag\n','')
new='''/* Sturzmaße: größte mögliche Torhöhe je Beschlag (hmaxFor) aus Sturz, Anschlag oben, Decke und Bodenversatz */
function aufSturzmass(X){
 const {a,v,H1,V}=X; const c=X.c;
'''+p_mass+''' Object.assign(X,{DH,DVh,STe,rest,hmaxFor});
}
/* Beschlag: alle Beschläge bewerten (Höhe, Grenzen Beschlag 8, Sonderzarge, Raumtiefe) und den passenden wählen */
function aufBeschlagwahl(X){
 const {a,v,R,B1,H1,hmaxFor}=X; const c=X.c;
'''+p_wahl+''' X.sel=sel; X.nF=nF; X.dep2=dep2; X.nB=nB;
}
/* Hinweise zur Sturztiefe für den gewählten Beschlag */
function aufSturzhinweise(X){
 const {a,R,V,STe,nF,dep2,nB}=X;
'''+p_hinw+'''}
/* Torhöhe: in der Öffnung, Sonderhöhe mit Sturzblende, eine Größe kleiner mit Blende, Standardhöhe mit Überdeckung */
function aufHoehenloesung(X){
 const {a,R,B1,H1,rest,sel,nF,dep2,nB}=X;
'''+p_loes+'''}
/* Höherführung 60/110 mm: möglich, wenn sie die Torhöhe nicht verringert. Rückgabe "neu", wenn die gewählte nicht passt */
function aufHoeherfuehrung(X){
 const {a,R,H1,hfOn,hmaxFor,sel}=X; const c=X.c;
'''+p_hf+'''}
/* Höhe und Beschlag (Ablauf). Rückgabe "neu", wenn die gewählte Höherführung nicht passt */
function aufHoehe(X){
 if(X.H1==null) return;
 aufSturzmass(X); aufBeschlagwahl(X); aufSturzhinweise(X); aufHoehenloesung(X);
 if(aufHoeherfuehrung(X)==="neu") return "neu";
 X.c=Object.assign({},X.c,{beschlag:X.sel.k}); /* folgende Teile rechnen mit dem gewählten Beschlag */
}
'''
s=s[:i]+new+s[j:]; open(f,'w',encoding='utf-8').write(s); print("ok")
