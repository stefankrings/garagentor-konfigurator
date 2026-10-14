# Mutationstest: baut absichtlich kleine Fehler ein und prüft, ob die Rechentests sie finden.
import subprocess,os,sys,re
M=[("Hn-H1<=15","Hn-H1<=9","Toleranz Standardhöhe 15→9 mm"),
   ("Wn-B1<=15","Wn-B1<=9","Toleranz Standardbreite 15→9 mm"),
   ("dv>=20&&dv<=30","dv>=21&&dv<=30","L-Profil ab 21 statt 20 mm"),
   ("VERST_PLUS = 60","VERST_PLUS = 50","Verstärkungsprofil 50 statt 60 mm"),
   ("if(RT<req)","if(RT<req-20)","Raumtiefe 20 mm großzügiger"),
   ('sym=a.symB==="sym"',"sym=false","Symmetrie ignoriert"),
   ('["zboden","Z-Bodenprofil Edelstahl 3 mm, 3000 mm","Maße x1 (max. 100), h1 (max. 50), x2 (max. 80 mm)",173,','["zboden","Z-Bodenprofil Edelstahl 3 mm, 3000 mm","Maße x1 (max. 100), h1 (max. 50), x2 (max. 80 mm)",174,',"Preis Z-Profil 173→174 €"),
   ('sturz==="stumpf_in"','sturz==="stumpf_inX"',"eine Sturz-Abfrage (in der Öffnung) kaputt"),
   ("list:drv===\"tiga\"?320:650","list:drv===\"tiga\"?321:650","Preis Steuerung tiga 320→321"),
   ("list:p*0.1,","list:p*0.11,","Milchglas 10 → 11 %"),
   ("qty:mB/10,unit:\"cm\"","qty:mB/10+1,unit:\"cm\"","Montage 1 cm zu viel"),
   ("s.b<=3000?1936:2027","s.b<=3000?1937:2027","Schlupftür 1936→1937"),
   ("unit:\"m²\",list:61,","unit:\"m²\",list:62,","RAL-Mehrpreis 61→62 €/m²"),
   ("Math.max(0,n-side[i])","Math.max(0,n-side[i]+1)","Seitenplatz 1 mm falsch gerechnet"),
   ('${q} × Edelstahl-${pz?"Z":"L"}-Bodenprofil','${q} × Edelstahl-${pz?"L":"Z"}-Bodenprofil',"Text Bodenprofil vertauscht")]
src=open(sys.argv[1] if len(sys.argv)>1 else 'template_v4.html',encoding='utf-8').read(); hit=0
only=sys.argv[2:] 
for a,b,t in M:
    if only and not any(o in t for o in only): continue
    rx=re.compile(r'\s*'.join(re.escape(ch) for ch in a.replace(' ','')))  # unabhängig von Leerzeichen/Zeilenumbrüchen
    mo=rx.search(src)
    if not mo: print("?? nicht gefunden:",t); continue
    open('/tmp/mut.html','w',encoding='utf-8').write(src[:mo.start()]+b+src[mo.end():])
    subprocess.run(['python3','build.py','/tmp/mut.html','_mut.html'],check=True)
    r=subprocess.run(['node','regress/run.js'],env=dict(os.environ,APP='_mut.html'),capture_output=True,text=True)
    n=[l for l in r.stdout.split('\n') if l.startswith('✗')]
    hit+=bool(n); print(("✓ erkannt " if n else "✗ NICHT erkannt ")+f"{t}: {len(n)} Fälle")
os.remove('_mut.html'); print(f"\n{hit} von {len(M)} eingebauten Fehlern erkannt")
