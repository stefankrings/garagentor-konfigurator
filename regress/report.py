import json,html,sys
d=json.load(open('regress/baseline.json'))
e=lambda s:html.escape(str(s))
eur=lambda v:f"{v:,.2f} €".replace(",","X").replace(".",",").replace("X",".")
NM={"blende":"Blende 45 mm","sturzbl":"Sturzblende","szv":"Seitenzargenverkleidung","vblech":"Verkleidungsblech","lboden":"L-Bodenprofil","zboden":"Z-Bodenprofil","bodenbohr":"Bodenprofil gebohrt"}
U={"blende":"m","sturzbl":"m","vblech":"lfm","szv":"Paar","lboden":"Stk","zboden":"Stk"}
groups=[("k","Konfiguration ohne Aufmaß"),("a","Aufmaß-Fälle"),("o","Angebote")]
rows=""
for g,gt in groups:
    rows+=f'<tr class="g"><td colspan="6">{gt}</td></tr>'
    for k,o in d.items():
        if not k.startswith(g): continue
        c=o['cfg'];p=o['preis']
        res=[f"<b>{c['b']} × {c['h']} mm</b> · {({'s15':'Comfort Sonderpreisliste','auto':'Comfort Automatik','prem':'Premium'})[c['line']]} · Beschlag {e(c['beschlag'])}"+(" · Sonderzarge 50" if c['zarge50'] else "")]
        if c['mount']: res.append("Zubehör aus Aufmaß/Auswahl: "+", ".join(f"{NM.get(i,i)} {str(q).replace('.',',')} {U.get(i,'')}"+(f" ({c['mountH'][i]} mm hoch)" if i in c['mountH'] else "") for i,q in c['mount'].items()))
        if c['auff']: res.append(f"Auffüttern {str(c['auff']).replace('.',',')} m²")
        if o.get('strips'): s=o['strips']; res.append("Fotomontage/Zeichnung: "+", ".join(x for x in [f"links {s['l']:g} mm" if s['l'] else "",f"rechts {s['r']:g} mm" if s['r'] else "",f"oben {s['t']:g} mm ({'Blende' if s['blende'] else 'Sturzblende/Spalt'})" if s['t'] else ""] if x)+" sichtbar (Außenansicht)")
        if 'auf' in o and o['auf']['err']: res.append('<span class="er">Aufmaß nicht übernommen: '+e("; ".join(o['auf']['err']))+'</span>')
        if 'auf' in o and o['auf']['todo']: res.append("Zusätzlich nötig: "+e("; ".join(o['auf']['todo'])))
        if o['notes']: res.append("Angebotshinweise: "+"<br>– ".join([""]+[e(n) for n in o['notes']]))
        if o['err']: res.append('<span class="er">Fehler: '+e("; ".join(o['err']))+'</span>')
        if o['warn']: res.append('<span class="wa">Warnung: '+e("; ".join(o['warn']))+'</span>')
        if o.get('pages'): res.append("Seiten: "+", ".join(f"{({'kr':'KRINGS-Briefpapier','std':'neutral','mo':'modern'})[f]} {n}" for f,n in o['pages'].items()))
        pos="<br>".join(f"{e(x[0])} {e(x[1])} – {eur(x[2])}" for x in o['pos'])
        rows+=f'<tr><td class="id">{k}</td><td>{e(o["t"])}</td><td>{"<br>".join(res)}<details><summary>Positionen</summary>{pos}</details></td><td class="r">{eur(p["net"])}</td><td class="r">{eur(p["labor"])}</td><td class="ck"></td></tr>'
doc=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Prüfliste Konfigurator</title><style>
body{{font:13px/1.45 system-ui,Segoe UI,Arial,sans-serif;color:#222;margin:24px}}h1{{font-size:20px;margin:0 0 4px}}p{{max-width:900px}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #ddd;padding:6px 8px;vertical-align:top;text-align:left}}th{{background:#f3f1ee;position:sticky;top:0}}
tr.g td{{background:#2b2829;color:#fff;font-weight:700}}.id{{font-weight:700;white-space:nowrap}}.r{{text-align:right;white-space:nowrap}}.ck{{width:70px;border-left:1px solid #ddd}}
.er{{color:#a32020}}.wa{{color:#8a5a00}}details{{margin-top:4px;color:#555}}.box{{border:2px solid #c77700;background:#fff7e6;padding:10px 14px;border-radius:8px;max-width:900px;margin:12px 0}}
@media print{{details{{display:none}}th{{position:static}}}}</style></head><body>
<h1>Prüfliste – Garagentor-Konfigurator</h1>
<p>Diese {len(d)} Fälle laufen ab jetzt bei jeder Änderung automatisch mit. Weicht danach auch nur ein Cent oder Millimeter ab, fällt es sofort auf. Bitte prüfe stichprobenartig, ob die Ergebnisse fachlich stimmen – vor allem Preise, Bestellmaße, Beschlag und Zubehör. Was falsch ist, bitte mit Fallnummer melden; sonst schreibe ich einen Fehler als „richtig“ fest. Preise netto mit Standard-Einstellungen (8 % TZ, kein Aufschlag).</p>
<div class="box"><b>Mir ist beim Erstellen aufgefallen (bitte beurteilen):</b><ul>
<li><b>a09:</b> Bei „eine Größe kleiner“ (Torhöhe 2250 mm) wählt das Aufmaß Beschlag 6.(NU), obwohl Beschlag 8 bei 2250 mm zulässig wäre. Ursache: Die Zulässigkeit von Beschlag 8 wird mit der größtmöglichen Höhe (2370 mm) geprüft statt mit der gewählten Standardhöhe. Das halte ich für einen Fehler.</li>
<li><b>k06, k07, k17:</b> Bei 5000/4500 mm Breite bzw. Dachfolge bleibt Beschlag 8 eingestellt, mit Fehlermeldung. Das ist gewollt (der Nutzer muss umstellen) – nur zur Info.</li>
<li><b>Neu, a54:</b> Bodenversatz 15 mm → Z-Profil (L-Profil gilt nur für 20–30 mm). Ist ein Z-Profil bei so wenig Versatz praktikabel, oder wäre hier „bauseits“ bzw. ein anderes Profil richtig?</li>
<li><b>Neu, a40:</b> Lichte Höhe 2135 mm → Sonderhöhe 2135 mm. Standardhöhe 2250 wäre 115 mm höher und wird nur bis 15 mm Überdeckung vorgeschlagen. Ist die 15-mm-Grenze für euch richtig?</li>
<li><b>Neu, a64/a65:</b> Premium mit 100 mm Anschlag oben → Beschlag 6.(NU) statt Standard 5., weil 5. nur bis 2115 mm reicht. Fachlich so gewollt?</li>
<li><b>Neu, a44/a63:</b> Anschlag oben 0 mm, Decke knapp: Beschlag 8. und 6.(NU) erreichen hier beide nur dieselbe Höhe (2065 bzw. 2105 mm) – der Niedrigsturzbeschlag bringt also nichts. Stimmt das mit euren Unterlagen überein?</li>
<li><b>a07:</b> Sonderhöhe 2145 mm aus 2250-mm-Torblatt: Warnung zur gekürzten Sicke beim Motiv medio. Fachlich korrekt?</li>
</ul></div>
<table><thead><tr><th>Nr.</th><th>Fall</th><th>Ergebnis</th><th class="r">Netto</th><th class="r">davon Arbeit</th><th>OK?</th></tr></thead><tbody>{rows}</tbody></table></body></html>'''
open('Pruefliste-Konfigurator.html','w').write(doc)
print("ok")
