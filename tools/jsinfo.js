// Übersicht über das Haupt-Skript: unbenutzte Top-Level-Deklarationen (Funktionen, Konstanten, Variablen)
// node tools/jsinfo.js template_v3.html  |  node tools/jsinfo.js template_v3.html --rm name1,name2  (entfernt Funktionen)
const fs=require('fs'), acorn=require('acorn'), walk=require('acorn-walk');
const file=process.argv[2], src=fs.readFileSync(file,'utf8');
const m=[...src.matchAll(/<script>([\s\S]*?)<\/script>/g)].sort((a,b)=>b[1].length-a[1].length)[0];
const off=m.index+'<script>'.length, js=m[1].replace(/__[A-Z]+__/g,'null');
const ast=acorn.parse(js,{ecmaVersion:'latest',sourceType:'script'});
const decl=[];
ast.body.forEach(n=>{ if(n.type==='FunctionDeclaration') decl.push({name:n.id.name,kind:'function',start:n.start,end:n.end});
 else if(n.type==='VariableDeclaration') n.declarations.forEach(d=>{ if(d.id.type==='Identifier') decl.push({name:d.id.name,kind:n.kind,start:n.start,end:n.end,multi:n.declarations.length>1}); }); });
const refs={}; walk.full(ast,n=>{ if(n.type==='Identifier') refs[n.name]=(refs[n.name]||0)+1; });
const html=src.slice(0,m.index)+src.slice(off+m[1].length);
const used=d=>{ let r=refs[d.name]||0; return r-1+(new RegExp('\\b'+d.name.replace(/\$/g,'\\$')+'\\b').test(html)?1:0); };
const rm=process.argv.indexOf('--rm');
if(rm<0){ const un=decl.filter(d=>used(d)<=0); console.log(`${decl.length} Deklarationen, ${un.length} unbenutzt:`); un.forEach(d=>console.log(`  ${d.kind} ${d.name}  (${d.end-d.start} Zeichen)`)); return; }
const names=process.argv[rm+1].split(','); let out=js, list=decl.filter(d=>names.includes(d.name)&&!d.multi).sort((a,b)=>b.start-a.start);
if(list.length!==names.length){ console.error('nicht gefunden/mehrfach:',names.filter(n=>!list.some(d=>d.name===n))); process.exit(1); }
let s2=m[1]; list.forEach(d=>{ let e=d.end; while(s2[e]===';'||s2[e]===' ') e++; if(s2[e]==='\n') e++; let st=d.start; while(st>0&&s2[st-1]===' ') st--; s2=s2.slice(0,st)+s2.slice(e); });
fs.writeFileSync(file,src.slice(0,off)+s2+src.slice(off+m[1].length)); console.log('entfernt:',list.map(d=>d.name).join(', '));
