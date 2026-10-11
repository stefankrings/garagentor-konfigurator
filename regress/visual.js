// Bildvergleich der Oberfläche: node regress/visual.js [--update]
// Fotografiert alle Abschnitte, das Aufmaß, die Einstellungen und alle Angebotsformen
// bei 1300 px und 390 px Breite und vergleicht Pixel + sichtbaren Text mit dem Referenzstand.
const {chromium}=require('playwright'), fs=require('fs'), path=require('path'), {execFileSync}=require('child_process');
const CASES=require('./cases.js'), APP='file://'+path.join(__dirname,'..',process.env.APP||'Garagentor-Konfigurator-V3.html');
const DIR=path.join(__dirname,'visual'), REF=path.join(DIR,'ref'), CUR=path.join(DIR,'cur'), UPD=process.argv.includes('--update');
[REF,CUR].forEach(d=>fs.mkdirSync(d,{recursive:true}));
const SCEN=[["bsp",null],["auf","o02"]];
(async()=>{
 const b=await chromium.launch(), txt={}, errs=[]; let shots=[];
 for(const W of [1300,390]) for(const [sn,cid] of SCEN){
  const ctx=await b.newContext({viewport:{width:W,height:W>500?950:844},deviceScaleFactor:1}), p=await ctx.newPage();
  p.on('pageerror',e=>errs.push(`${W}/${sn}: ${e.message}`));
  await p.addInitScript(()=>{ const D=Date; const T=new D("2026-10-11T10:00:00").getTime(); window.Date=class extends D{ constructor(...a){ super(...(a.length?a:[T])); } static now(){ return T; } }; });
  await p.goto(APP,{waitUntil:'domcontentloaded'}); await p.waitForTimeout(1200);
  await p.addStyleTag({content:'*,*::before,*::after{transition:none!important;animation:none!important;caret-color:transparent!important} html.vshot .view.ov:not([hidden]),html.vshot #v-offer:not([hidden]){position:static!important;overflow:visible!important;inset:auto!important} html.vshot #v-cfg,html.vshot header .stage,html.vshot .stagewrap{display:none!important}'});
  const c=cid&&CASES.find(x=>x.id===cid);
  await p.evaluate(c=>{ const deep=(t,s)=>{ for(const k in s){ if(s[k]&&typeof s[k]==="object"&&!Array.isArray(s[k])&&t[k]&&typeof t[k]==="object") deep(t[k],s[k]); else t[k]=s[k]; } };
   S=Object.assign(JSON.parse(JSON.stringify(DEFAULT_SETTINGS)),(c&&c.set)||{}); CFG=defaultConfig(true); if(c&&c.cfg) deep(CFG,JSON.parse(JSON.stringify(c.cfg)));
   if(c&&c.auf){ CFG.auf=Object.assign(aufDefault(),JSON.parse(JSON.stringify(c.auf))); CFG.auf.mode="auf"; }
   normalize(CFG); CFG.a.nr="AN-TEST-001"; bindBasics(); renderAll(); },c);
  await p.waitForTimeout(500);
  const shot=async (nm,ov)=>{ await p.evaluate(ov=>document.documentElement.classList.toggle("vshot",!!ov),ov); await p.mouse.move(0,0); await p.evaluate(()=>document.activeElement&&document.activeElement.blur&&document.activeElement.blur()); await p.waitForTimeout(250); const f=`${W}_${sn}_${nm}.png`; await p.screenshot({path:path.join(UPD?REF:CUR,f),fullPage:true}); shots.push(f);
   txt[f]=await p.evaluate(()=>{ const v=[...document.querySelectorAll('.view')].filter(x=>!x.hidden); return v.map(x=>x.innerText).join("\n¦\n").replace(/[ \t]+/g," "); }); };
  const gs=await p.evaluate(()=>[...document.querySelectorAll('#torAcc > .zg')].map(s=>s.dataset.g));
  for(const g of gs){ await p.evaluate(g=>{ UI.torOpen=g; accApply("torAcc","torOpen"); window.scrollTo(0,0); },g); await shot("cfg_"+g); }
  if(sn==="bsp"){
   const ss=await p.evaluate(()=>{ showView("v-set"); return [...document.querySelectorAll("#v-set .settings.set-acc > .sec")].map(s=>s.dataset.s); });
   for(const [i,s] of ss.entries()){ await p.evaluate(s=>{ SET_OPEN=s; applySetAcc(); },s); await shot("set_"+i,1); }
   await p.evaluate(()=>showView("v-cfg"));
  }
  for(const f of (sn==="bsp"?["kr","std","mo"]:["kr","mo"])){ await p.evaluate(f=>{ CFG.a.stil=f==="mo"?"modern":"klassisch"; if(f!=="mo") S.brief=f==="kr"?"krings":"std"; update(false); showView("v-offer"); window.scrollTo(0,0); },f); await p.waitForTimeout(f==="mo"?1500:400); await shot("off_"+f,1); await p.evaluate(()=>showView("v-cfg")); }
  await ctx.close();
 }
 await b.close();
 const TF=path.join(DIR,'ref_text.json');
 if(UPD){ fs.writeFileSync(TF,JSON.stringify(txt,null,1)); console.log(`Referenz geschrieben: ${shots.length} Bilder`); if(errs.length) console.log("JS-FEHLER:",errs); return; }
 const rt=JSON.parse(fs.readFileSync(TF)); let bad=0;
 const res=JSON.parse(execFileSync('python3',[path.join(__dirname,'imgdiff.py'),REF,CUR,...shots]).toString());
 for(const f of shots){ const r=res[f], t=rt[f]!==txt[f];
  if(r.miss||r.px>0||t){ bad++; console.log(`✗ ${f}: ${r.miss?"keine Referenz":r.size?"Größe "+r.size:r.px+" Pixel anders"}${t?" · Text geändert":""}`); } }
 if(errs.length) console.log("JS-FEHLER:",errs);
 console.log(bad?`\n${bad} von ${shots.length} Ansichten weichen ab – Unterschiede in regress/visual/diff_*.png`:`✓ Alle ${shots.length} Ansichten pixelgleich.`);
 process.exitCode=bad||errs.length?1:0;
})();
