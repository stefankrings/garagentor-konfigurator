// Aufruf: node regress/run.js            → vergleicht mit baseline.json
//         node regress/run.js --update   → schreibt baseline.json neu (nur nach bewusster Prüfung!)
const {chromium}=require('playwright'), fs=require('fs'), path=require('path');
const CASES=require('./cases.js'), BASE=path.join(__dirname,'baseline.json'), APP='file://'+path.join(__dirname,'..',process.env.APP||'Garagentor-Konfigurator.html');
(async()=>{
 const b=await chromium.launch(), p=await (await b.newContext({viewport:{width:1300,height:1000}})).newPage(), errs=[];
 p.on('pageerror',e=>errs.push(e.message));
 await p.goto(APP,{waitUntil:'domcontentloaded'}); await p.waitForTimeout(1200);
 const out={};
 for(const c of CASES){
  out[c.id]=await p.evaluate(async c=>{
   const r2=x=>Math.round(x*100)/100, deep=(t,s)=>{ for(const k in s){ if(s[k]&&typeof s[k]==="object"&&!Array.isArray(s[k])&&t[k]&&typeof t[k]==="object") deep(t[k],s[k]); else t[k]=s[k]; } };
   S=Object.assign(JSON.parse(JSON.stringify(DEFAULT_SETTINGS)),c.set||{});
   CFG=defaultConfig(!!c.example); if(c.cfg) deep(CFG,JSON.parse(JSON.stringify(c.cfg))); normalize(CFG);
   const o={t:c.t};
   if(c.auf){ CFG.auf=Object.assign(aufDefault(),JSON.parse(JSON.stringify(c.auf))); const r=aufCalc(CFG.auf,CFG);
    o.auf={B:r.B,H:r.H,beschlag:r.bSel||null,acc:r.acc,todo:r.todo,warn:r.warn,err:r.err,missing:r.missing};
    if(r.B&&r.H&&!r.err.length) aufApply(r); }
   R=compute(CFG);
   if(c.pxTest){ CFG.px={}; R.lines.forEach(l=>{ if(l.key) CFG.px[l.key]=l.ep; }); const n0=R.net; Object.assign(S,c.pxTest); R=compute(CFG); o.px={vorher:n0,gesperrt:R.net,geaendert:R.changed.length,neu:r2(R.lines.reduce((a,l)=>a+r2((l.curEp??l.ep)*l.qty),0))}; R.lines.forEach(l=>{ if(l.key) CFG.px[l.key]=l.curEp; }); R=compute(CFG); o.px.nachUebernahme=R.net; }
   o.cfg={line:CFG.line,b:CFG.b,h:CFG.h,beschlag:CFG.beschlag,zarge50:!!CFG.opts.zarge50,drv:CFG.drv,
    mount:Object.fromEntries(Object.entries(CFG.mount).filter(x=>+x[1]>0)),mountH:CFG.mountH||{},auff:CFG.svc.auff||0};
   o.preis={net:R.net,vat:R.vat,gross:R.gross,labor:R.labor};
   o.lines=R.lines.map(l=>[l.title,r2(+l.qty||0),l.unit,r2(l.gp)]);
   if(c.auf&&typeof renderAuf==="function"&&document.getElementById("aufBody")){ try{ CFG.auf.mode="auf"; renderAll(); UI.torOpen="mass"; accApply("torAcc","torOpen"); renderAuf(); await new Promise(r=>setTimeout(r,60)); /* nach der Verkaufspreis-Umrechnung lesen, wie angezeigt */
     o.mehrpreise=[...document.querySelectorAll('#aufBody ul')].map(u=>{ const h=u.closest('[id^="pk_"]'); return (h?h.id:"?")+": "+[...u.querySelectorAll('li')].map(li=>{ const c=li.querySelector('.pk-cost'); return (li.querySelector('.lbl b')||li).innerText.trim().slice(0,40)+" = "+(c?c.innerText.replace(/\s+/g," ").trim():"–"); }).join(" | "); });
     R=compute(CFG); }catch(e){ o.mehrpreise=["Fehler: "+e.message]; } }
   o.err=R.err; o.warn=R.warn; o.notes=aufNotes(CFG); o.onotes=typeof offerNotes==="function"?offerNotes(CFG):o.notes; o.strips=doorStrips(CFG);
   o.pos=offerPositions().map(x=>[x.pos,x.title,r2(x.gp)]);
   if(c.offer){ o.pages={}; for(const f of c.offer){ if(f==="mo"){ CFG.a.stil="modern"; } else { CFG.a.stil="klassisch"; S.brief=f==="kr"?"krings":"std"; }
     renderSheet(); o.pages[f]=f==="kr"?document.querySelectorAll('#sheet .kpage').length:f==="mo"?document.querySelectorAll('#sheet .mpage').length:1; } }
   return o; },c);
 }
 await b.close();
 if(errs.length) console.log("JS-FEHLER:",errs);
 if(process.argv.includes('--update')){ fs.writeFileSync(BASE,JSON.stringify(out,null,1)); console.log(`Baseline geschrieben: ${Object.keys(out).length} Fälle`); return; }
 const base=JSON.parse(fs.readFileSync(BASE)); let bad=0;
 const diff=(a,b,p,acc)=>{ if(JSON.stringify(a)===JSON.stringify(b)) return; if(a&&b&&typeof a==="object"&&typeof b==="object"&&!Array.isArray(a)){ new Set([...Object.keys(a),...Object.keys(b)]).forEach(k=>diff(a[k],b[k],p+"."+k,acc)); } else acc.push(`${p}: vorher ${JSON.stringify(a)} → jetzt ${JSON.stringify(b)}`); };
 for(const id of Object.keys(base)){ const acc=[]; diff(base[id],out[id],id,acc); if(acc.length){ bad++; console.log(`✗ ${id} ${base[id].t}\n   `+acc.slice(0,8).join("\n   ")+(acc.length>8?`\n   … ${acc.length-8} weitere`:"")); } }
 Object.keys(out).filter(k=>!base[k]).forEach(k=>console.log(`+ neu: ${k} (nicht in Baseline)`));
 console.log(bad?`\n${bad} von ${Object.keys(base).length} Fällen weichen ab.`:`✓ Alle ${Object.keys(base).length} Fälle unverändert.`);
 process.exitCode=bad?1:0;
})();
