# Erzeugt template_v2.html: Konfiguration und Aufmaß zusammengeführt (Test-Version)
s=open('template.html',encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a); assert c==n,(c,a[:90]); s=s.replace(a,b)
# --- Titel
rep('<title>Garagentor-Konfigurator</title>','<title>Garagentor-Konfigurator V2 (Test)</title>')
# --- Aufmaß-Tab entfernen
i=s.index('<button role="tab" id="tab-auf"'); j=s.index('</button>',i)+len('</button>'); s=s[:i]+s[j:]
# --- Aufmaß-Ansicht leeren, aufBody in den Abschnitt „Maße“ verschieben
rep('''<section class="view" id="v-auf" hidden>
 <div class="sec auf-sec"><h2>Aufmaß <span class="muted small" style="font-weight:400">Maße in mm · Skizze nicht maßstäblich</span></h2><div class="body" id="aufBody"></div></div>
</section>''','<section class="view" id="v-auf" hidden></section>')
rep('<span class="zg-t">Maße<small class="zg-s" id="sum_mass"></small></span>','<span class="zg-t">Maße &amp; Aufmaß<small class="zg-s" id="sum_mass"></small></span>')
i=s.index('aria-controls="zgb_mass"'); i=s.index('<div class="body">',i)+len('<div class="body">')
s=s[:i]+'''<div class="mmode" role="radiogroup" aria-label="Maße"><button type="button" data-mm="auf">Aufmaß vor Ort</button><button type="button" data-mm="direkt">Maße direkt eingeben</button></div>
     <div id="massAuf" class="auf-sec"><div class="muted small" style="margin:2px 0 8px">Maße in mm · Skizze nicht maßstäblich · Ergebnis wird sofort in die Konfiguration übernommen</div><div id="aufBody"></div></div>
     <div id="massDirect">'''+s[i:]
j=s.index('</div></div></div></div></section>',i)
s=s[:j]+'</div>'+s[j:]
# --- CSS
rep('.aufdot{display:none','''.mmode{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden;margin-bottom:12px}.mmode button{border:0;background:var(--panel);color:var(--ink);padding:7px 14px;font:600 14px var(--f-body);cursor:pointer}.mmode button.on{background:var(--ink);color:var(--panel)}
.auf-live{margin-top:10px;font-size:13px;padding:8px 10px;border-radius:6px;border-left:4px solid}.auf-live.ok{background:var(--accent-soft);border-color:var(--accent)}.auf-live.no{background:var(--warn-bg);border-color:var(--warn)}
.aufdot{display:none''')
# --- Modus
rep('function aufMatch(s){ const a=s&&s.auf; return','''function aufMode(c){ const a=c&&c.auf; if(!a) return "direkt"; return a.mode||(a.m&&+a.m.B1?"auf":"direkt"); }
function aufMatch(s){ const a=s&&s.auf; if(aufMode(s)==="direkt") return false; return''')
rep('function aufLocked(){ const a=CFG.auf; return !!(a&&a.oB&&aufMatch(CFG)&&a.lock!==false); }','function aufLocked(){ const a=CFG.auf; return !!(a&&a.oB&&aufMatch(CFG)); }')
# --- Live-Übernahme
rep('function aufApply(r,keepView){','''let LIVE_BUSY=false;
function aufLive(){ if(LIVE_BUSY||aufMode(CFG)!=="auf") return; const a=CFG.auf; if(!a||!a.m||!(+a.m.B1)) return; let r; try{ r=aufCalc(a,CFG); }catch(e){ return; }
 if(!r.B||!r.H||r.err.length) return; if(a.appliedSig===aufSig(a)&&aufMatch(CFG)&&!aufStale()) return;
 LIVE_BUSY=true; try{ aufApply(r,true,true); } finally { LIVE_BUSY=false; } }
function aufApply(r,keepView,silent){''')
rep('''if(!keepView) showView("v-cfg"); toast(''','''if(!keepView) showView("v-cfg"); if(!silent) toast(''')
# nach jeder Neuberechnung des Aufmaß-Ergebnisses live übernehmen
rep('''function renderAufRes(){
 const a=CFG.auf, r=aufCalc(a,CFG), el=$("aufRes"); if(!el) return;''','''function renderAufRes(){ renderAufRes0(); aufLive(); }
function renderAufRes0(){
 const a=CFG.auf, r=aufCalc(a,CFG), el=$("aufRes"); if(!el) return; AUF_RSIG=aufRSig();''')
rep('let LINE_ITEMS=null;','''let LINE_ITEMS=null, AUF_RSIG="";
function aufRSig(){ return JSON.stringify([aufSig(CFG.auf||{}),CFG.drv,CFG.door&&CFG.door.on,CFG.opts&&CFG.opts.dach,CFG.color,CFG.ral,CFG.line,CFG.surface]); }''')
# Statuszeile statt „beim Wechsel übernommen“
rep('''<div class="auf-auto ${r.B&&r.H&&!r.err.length?"ok":"no"}">${r.B&&r.H&&!r.err.length?"Wird beim Wechsel in Konfiguration oder Angebot automatisch übernommen.":"Wird erst übernommen, wenn die Maße vollständig und widerspruchsfrei sind."}</div>''',
'''<div class="auf-live ${r.B&&r.H&&!r.err.length?"ok":"no"}">${r.B&&r.H&&!r.err.length?`In der Konfiguration: ${r.B} × ${r.H} mm, Beschlag ${esc(bnmG(r.bSel||CFG.beschlag).replace(/\\.$/,""))}${r.missing.length?" – es fehlen noch Maße":""}`:(+a.m.B1?"Noch nicht übernommen – Maße unvollständig oder widersprüchlich. Die Konfiguration behält die letzten gültigen Werte.":"Noch kein Aufmaß erfasst.")}</div>''')
# Tortyp-Auswahl im Aufmaß entfällt (steht direkt darüber im Abschnitt Tortyp)
rep('''  <div class="f auf-typ"><span class="flabel" id="lb_aline">Tortyp</span><div id="pk_aline"></div><span class="hint">bestimmt die möglichen Beschläge und Zargen – deshalb schon hier wählen</span></div>
''','')
# --- Sperren/Anzeige in der Konfiguration
rep('''const hosts=["pk_line","pk_beschlag","pk_b","pk_h","pk_hf","pk_zarge"];''','''const hosts=["pk_beschlag","pk_hf","pk_zarge"];''')
rep('''<span>aus dem Aufmaß</span> · <button type="button" data-goauf>im Aufmaß ändern</button>''','''<span>festgelegt im Aufmaß</span> · <button type="button" data-goauf>zum Aufmaß</button>''')
rep('''function applyAufLock(){ aufTabState(); const bar=$("aufLockBar"); if(!bar) return; const on=aufLocked();''','''function applyAufLock(){ const bar=$("aufLockBar"); if(!bar) return; const on=aufLocked();
 { const m=aufMode(CFG); document.querySelectorAll(".mmode button").forEach(b=>{ b.classList.toggle("on",b.dataset.mm===m); b.setAttribute("aria-checked",b.dataset.mm===m); }); const ma=$("massAuf"), md=$("massDirect"); if(ma) ma.hidden=m!=="auf"; if(md) md.hidden=m==="auf";
   if(m==="auf"&&ma&&!$("aufRes")) renderAuf(); else if(m==="auf"&&AUF_RSIG!==aufRSig()) renderAufRes(); }''')
# Leiste oben entfällt
rep('''  $("aufUnlock").onclick=()=>{''','''  if($("aufUnlock")) $("aufUnlock").onclick=()=>{''')
rep(''' if(on){ const st=aufStale();''',''' bar.hidden=true; if(false){ const st=aufStale();''')
rep('''document.querySelectorAll("[data-goauf]").forEach(b=>b.onclick=e=>{ e.preventDefault(); e.stopPropagation(); showView("v-auf"); });''','''document.querySelectorAll("[data-goauf]").forEach(b=>b.onclick=e=>{ e.preventDefault(); e.stopPropagation(); goAuf(); });''')
rep('function aufLocked(){','''function goAuf(){ showView("v-cfg"); UI.torOpen="mass"; accApply("torAcc","torOpen"); setTimeout(()=>{ const s=document.querySelector('#torAcc [data-g="mass"]'); if(s) s.scrollIntoView({behavior:"smooth",block:"start"}); },280); }
function aufLocked(){''')
# Nach Konfigurationsänderungen (Antrieb, Tortyp …) Aufmaß-Ergebnis live nachziehen
rep(''' if(aufLocked()){ const st=aufStale(); if(st) R.warn.unshift(''',''' if(aufMode(CFG)==="auf"&&!LIVE_BUSY&&aufLocked()&&aufStale()){ aufLive(); return; }
 if(false){ const st=aufStale(); if(st) R.warn.unshift(''')
# Ansicht „Aufmaß“ gibt es nicht mehr
rep('''function showView(id){ if(CUR_VIEW==="v-auf"&&id!=="v-auf") aufAutoApply(); CUR_VIEW=id;''','''function showView(id){ if(id==="v-auf"){ goAuf(); return; } CUR_VIEW=id;''')
# Modus-Schalter binden
rep('function bindBasics(){','''function bindMode(){ document.querySelectorAll(".mmode button").forEach(b=>b.onclick=()=>{ if(!CFG.auf) CFG.auf=aufDefault(); CFG.auf.mode=b.dataset.mm; if(b.dataset.mm==="auf"){ renderAuf(); } renderAll(); }); }
function bindBasics(){ bindMode();''')
rep('''set("mass",`${CFG.b} × ${CFG.h} mm${CFG.bSonder||CFG.hSonder?" (Sondermaß)":""}`);''','''set("mass",`${CFG.b} × ${CFG.h} mm${CFG.bSonder||CFG.hSonder?" (Sondermaß)":""}${aufMode(CFG)==="auf"?(aufMatch(CFG)?" · aus dem Aufmaß":" · Aufmaß unvollständig"):""}`);''')
open('template_v2.html','w',encoding='utf-8').write(s)
print("ok")
s=open('template_v2.html',encoding='utf-8').read()
def rep2(a,b):
    global s
    assert s.count(a)==1,a[:80]; s=s.replace(a,b)
rep2('<div class="brand">Garagentor-Konfigurator<small>','<div class="brand">Garagentor-Konfigurator <span class="v2tag">V2 Test</span><small>')
rep2('.mmode{display:inline-flex;','.v2tag{font:700 11px var(--f-body);background:#c77700;color:#fff;border-radius:4px;padding:2px 6px;vertical-align:middle;letter-spacing:.03em}\n.mmode{display:flex;width:max-content;max-width:100%;')
open('template_v2.html','w',encoding='utf-8').write(s)
print("ok2")
# --- Kundendaten als oberster Abschnitt der Konfiguration; im Angebot bleibt nur die Angebotsform
s=open('template_v2.html',encoding='utf-8').read()
i=s.index('   <div class="sec" style="max-width:210mm;margin:0 auto 14px"><h2>Kunde &amp; Angebot</h2>')
j=s.index('     <div class="ostil">',i); k=s.index('    </div>\n   </div>\n',j)
fields=s[s.index('<div class="body">',i)+len('<div class="body">'):j]
ostil=s[j:k]
s=s[:i]+'''   <div class="sec ostil-sec" style="max-width:210mm;margin:0 auto 14px"><div class="body">
'''+ostil+'''    </div></div>
'''+s[k+len('    </div>\n   </div>\n'):]
sec='''<section class="zg" data-g="kunde"><button type="button" class="zg-h" aria-expanded="false" aria-controls="zgb_kunde"><span class="zg-t">Kunde &amp; Angebot<small class="zg-s" id="sum_kunde"></small></span><svg class="zg-c" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button><div class="zg-b" id="zgb_kunde" role="region" inert><div class="zg-in"><div class="zg-pad"><div class="body">'''+fields+'''</div></div></div></div></section>
'''
a='<section class="zg" data-g="typ">'; assert s.count(a)==1; s=s.replace(a,sec+a)
a=' const set=(g,txt)=>{ const el=$("sum_"+g); if(el) el.textContent=txt; };'; assert s.count(a)==1
s=s.replace(a,a+'''
 { const k=CFG.k||{}, nm=kName(k), kd=[[k.anrede&&k.anrede!=="Firma"?k.anrede:"",nm].filter(Boolean).join(" "),[kOrt(k),k.teilort].filter(Boolean).join(" – "),CFG.a&&CFG.a.nr?`Angebot ${CFG.a.nr}`:""].filter(Boolean).join(" · "); set("kunde",kd||"noch keine Kundendaten"); }''')
s=s.replace('.ostil{display:flex;','.ostil-sec .body{padding:10px 16px}.ostil-sec .ostil{margin-top:0}\n.ostil{display:flex;',1)
open('template_v2.html','w',encoding='utf-8').write(s)
print("ok3")
# --- Kunde & Baustelle: Datum/Gültigkeit automatisch, Ansprechpartner-Auswahl
s=open('template_v2.html',encoding='utf-8').read()
def rep3(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
rep3('<span class="zg-t">Kunde &amp; Angebot<small class="zg-s" id="sum_kunde">','<span class="zg-t">Kunde &amp; Baustelle<small class="zg-s" id="sum_kunde">')
rep3('''      <label class="f">Datum<input type="date" id="a_datum"></label>
      <label class="f">Gültig bis<input type="date" id="a_gueltig"></label>''','''      <label class="f" style="grid-column:span 2">Ansprechpartner<select id="a_ap"></select></label>''')
rep3('Auswahl je Angebot in den Kundendaten (Testversion V2).','Auswahl je Angebot unter „Kunde &amp; Baustelle“ in der Konfiguration.')
rep3('''function update(redrawSide=true){''','''function update(redrawSide=true){ if(CFG&&CFG.a){ CFG.a.datum=today(); CFG.a.gueltig=today(+S.gueltigTage||14); } /* Angebotsdatum = heute, Gültigkeit lt. Einstellungen */''')
open('template_v2.html','w',encoding='utf-8').write(s)
print("ok4")
# --- Kopf: kein Konfiguration-Tab; Export-Icon neben Einstellungen; Export als Popup
s=open('template_v2.html',encoding='utf-8').read()
def rep5(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
i=s.index('  <nav class="tabs" role="tablist">'); j=s.index('</nav>',i)+len('</nav>')
s=s[:i]+'  <nav class="tabs" role="tablist" hidden><button role="tab" id="tab-cfg" aria-selected="true" data-view="v-cfg" hidden>Konfiguration</button></nav>'+s[j:]
EXP='<button role="tab" id="tab-offer" aria-selected="false" data-view="v-offer" class="ico" aria-label="Export" data-tip="Export"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V3M7.5 7.5 12 3l4.5 4.5"/><path d="M8 10H6a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2h-2"/></svg></button>'
rep5('<nav class="tabs setnav" aria-label="Einstellungen"><button role="tab" id="tab-set"','<nav class="tabs setnav" aria-label="Export und Einstellungen">'+EXP+'<button role="tab" id="tab-set"')
# Export-Ansicht als Popup
i=s.index('<section class="view" id="v-offer" hidden>')+len('<section class="view" id="v-offer" hidden>'); j=s.index('</section>',i)
s=s[:i]+'<div class="exp-panel" role="dialog" aria-modal="true" aria-labelledby="expT"><div class="exp-hd"><b id="expT">Export</b><button type="button" class="info-x" id="expClose" aria-label="Schließen">×</button></div>'+s[i:j]+'</div>'+s[j:]
rep5('#v-offer>.toolbar,#v-offer>.sec,.toast{display:none!important}','#v-offer .toolbar,#v-offer .ostil-sec,.exp-hd,.toast{display:none!important}')
rep5('  #v-offer{display:block!important}','  #v-offer{display:block!important;position:static!important;background:none!important;padding:0!important;overflow:visible!important} .exp-panel{max-width:none!important;margin:0!important;padding:0!important;background:none!important;box-shadow:none!important;border-radius:0!important}')
rep5('.v2tag{','''#v-offer:not([hidden]){position:fixed;inset:0;z-index:60;background:rgba(15,20,25,.55);overflow:auto;padding:24px 16px;overscroll-behavior:contain}
.exp-panel{max-width:1000px;margin:0 auto;background:var(--bg);border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.35);padding:0 16px 20px}
.exp-hd{display:flex;align-items:center;justify-content:space-between;padding:12px 0 10px;position:sticky;top:-24px;background:var(--bg);z-index:2;border-bottom:1px solid var(--line);margin-bottom:12px}.exp-hd b{font:600 18px var(--f-display)}
.exp-panel .toolbar{position:static}
html.exp-open,html.exp-open body{overflow:hidden}
.setnav{display:flex;gap:4px}
.set-back{margin-bottom:12px}
@media (max-width:600px){#v-offer:not([hidden]){padding:0}.exp-panel{border-radius:0;min-height:100%}}
.v2tag{''')
# Ansichtswechsel: Export als Overlay über der Konfiguration, Rückweg aus Einstellungen
rep5('''function showView(id){ if(id==="v-auf"){ goAuf(); return; } CUR_VIEW=id;''','''let PREV_VIEW="v-cfg";
function showView(id){ if(id==="v-auf"){ goAuf(); return; } if(id==="v-offer"&&CUR_VIEW==="v-offer") id=PREV_VIEW||"v-cfg"; else if(id==="v-set"&&CUR_VIEW==="v-set") id="v-cfg";
 if(id==="v-offer"){ if(CUR_VIEW&&CUR_VIEW!=="v-offer") PREV_VIEW=CUR_VIEW; document.documentElement.classList.add("exp-open"); $("v-offer").hidden=false; document.querySelectorAll(".tabs button").forEach(b=>b.setAttribute("aria-selected",b.dataset.view==="v-offer")); CUR_VIEW=id; setTimeout(()=>{ const c=$("expClose"); if(c) c.focus(); },0); return; }
 document.documentElement.classList.remove("exp-open"); CUR_VIEW=id;''')
rep5('<section class="view" id="v-set" hidden>','<section class="view" id="v-set" hidden><div class="settings set-back"><button type="button" class="btn" id="setBack">← Zurück zur Konfiguration</button></div>')
rep5('function bindMode(){','''function bindExport(){ const c=$("expClose"); if(c) c.onclick=()=>showView(PREV_VIEW||"v-cfg"); const ov=$("v-offer"); if(ov) ov.addEventListener("click",e=>{ if(e.target===ov) showView(PREV_VIEW||"v-cfg"); });
 document.addEventListener("keydown",e=>{ if(e.key==="Escape"&&CUR_VIEW==="v-offer"&&!PK_OPEN&&!( $("infoDlg")&&!$("infoDlg").hidden)) showView(PREV_VIEW||"v-cfg"); });
 const sb=$("setBack"); if(sb) sb.onclick=()=>showView("v-cfg"); const br=document.querySelector(".brand"); if(br){ br.style.cursor="pointer"; br.onclick=()=>showView("v-cfg"); } }
function bindMode(){ bindExport();''')
open('template_v2.html','w',encoding='utf-8').write(s)
print("ok5")
# --- Einstellungen ebenfalls als Popup (wie Export)
s=open('template_v2.html',encoding='utf-8').read()
def rep6(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
rep6('<section class="view" id="v-set" hidden><div class="settings set-back"><button type="button" class="btn" id="setBack">← Zurück zur Konfiguration</button></div>','<section class="view ov" id="v-set" hidden><div class="exp-panel" role="dialog" aria-modal="true" aria-labelledby="setT"><div class="exp-hd"><b id="setT">Einstellungen</b><button type="button" class="info-x" id="setClose" aria-label="Schließen">×</button></div>')
i=s.index('<section class="view ov" id="v-set" hidden>'); j=s.index('</section>',i); s=s[:i]+s[i:j]+'</div>'+s[j:]
rep6('<section class="view" id="v-offer" hidden>','<section class="view ov" id="v-offer" hidden>')
rep6('#v-offer:not([hidden]){position:fixed;','.view.ov:not([hidden]){position:fixed;')
rep6('@media (max-width:600px){#v-offer:not([hidden]){padding:0}','@media (max-width:600px){.view.ov:not([hidden]){padding:0}')
rep6('''let PREV_VIEW="v-cfg";
function showView(id){ if(id==="v-auf"){ goAuf(); return; } if(id==="v-offer"&&CUR_VIEW==="v-offer") id=PREV_VIEW||"v-cfg"; else if(id==="v-set"&&CUR_VIEW==="v-set") id="v-cfg";
 if(id==="v-offer"){ if(CUR_VIEW&&CUR_VIEW!=="v-offer") PREV_VIEW=CUR_VIEW; document.documentElement.classList.add("exp-open"); $("v-offer").hidden=false; document.querySelectorAll(".tabs button").forEach(b=>b.setAttribute("aria-selected",b.dataset.view==="v-offer")); CUR_VIEW=id; setTimeout(()=>{ const c=$("expClose"); if(c) c.focus(); },0); return; }
 document.documentElement.classList.remove("exp-open"); CUR_VIEW=id;''','''let PREV_VIEW="v-cfg"; const OVS=["v-offer","v-set"];
function showView(id){ if(id==="v-auf"){ goAuf(); return; } if(OVS.includes(id)&&CUR_VIEW===id) id="v-cfg";
 if(OVS.includes(id)){ OVS.forEach(o=>{ $(o).hidden=o!==id; }); if(id==="v-set") renderSaved&&renderSaved(); document.documentElement.classList.add("exp-open"); const cf=$("v-cfg"); if(cf) cf.hidden=false; document.querySelectorAll(".tabs button").forEach(b=>b.setAttribute("aria-selected",b.dataset.view===id)); CUR_VIEW=id; try{localStorage.setItem("gtk_tab","v-cfg")}catch(e){} setTimeout(()=>{ const c=$(id==="v-offer"?"expClose":"setClose"); if(c) c.focus(); },0); return; }
 document.documentElement.classList.remove("exp-open"); CUR_VIEW=id;''')
rep6('''function bindExport(){ const c=$("expClose"); if(c) c.onclick=()=>showView(PREV_VIEW||"v-cfg"); const ov=$("v-offer"); if(ov) ov.addEventListener("click",e=>{ if(e.target===ov) showView(PREV_VIEW||"v-cfg"); });
 document.addEventListener("keydown",e=>{ if(e.key==="Escape"&&CUR_VIEW==="v-offer"&&!PK_OPEN&&!( $("infoDlg")&&!$("infoDlg").hidden)) showView(PREV_VIEW||"v-cfg"); });
 const sb=$("setBack"); if(sb) sb.onclick=()=>showView("v-cfg");''','''let EXP_BOUND=false;
function bindExport(){ if(EXP_BOUND) return; EXP_BOUND=true; [["expClose","v-offer"],["setClose","v-set"]].forEach(([b,v])=>{ const c=$(b); if(c) c.onclick=()=>showView("v-cfg"); const ov=$(v); if(ov) ov.addEventListener("click",e=>{ if(e.target===ov) showView("v-cfg"); }); });
 document.addEventListener("keydown",e=>{ if(e.key==="Escape"&&OVS.includes(CUR_VIEW)&&!PK_OPEN&&!( $("infoDlg")&&!$("infoDlg").hidden)){ e.stopPropagation(); showView("v-cfg"); } });''')
open('template_v2.html','w',encoding='utf-8').write(s)
print("ok6")
