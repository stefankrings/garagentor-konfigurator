// CSS-Übersicht: mehrfach definierte Selektoren, Klassen ohne Verwendung
const fs=require('fs'), postcss=require('postcss');
const src=fs.readFileSync(process.argv[2],'utf8'), css=[...src.matchAll(/<style>([\s\S]*?)<\/style>/g)].map(m=>m[1]).join('\n');
const root=postcss.parse(css), seen={}; let n=0;
root.walkRules(r=>{ n++; const ctx=r.parent.type==='atrule'?'@'+r.parent.name+' '+r.parent.params:''; const k=ctx+'|'+r.selector; (seen[k]=seen[k]||[]).push(r.nodes.length); });
const dup=Object.entries(seen).filter(([k,v])=>v.length>1);
console.log(`${n} Regeln, ${dup.length} Selektoren mehrfach definiert`); dup.slice(0,400).forEach(([k,v])=>console.log('  '+v.length+'× '+k.slice(0,110)));
// Klassen ohne Vorkommen außerhalb des CSS
const rest=src.replace(/<style>[\s\S]*?<\/style>/g,''); const cls=new Set(); root.walkRules(r=>(r.selector.match(/\.[A-Za-z][\w-]*/g)||[]).forEach(c=>cls.add(c.slice(1))));
const un=[...cls].filter(c=>!new RegExp('(?<![\\w-])'+c+'(?![\\w-])').test(rest));
console.log(`\n${un.length} Klassen im CSS ohne Vorkommen im HTML/JS:`); console.log('  '+un.join(' '));
