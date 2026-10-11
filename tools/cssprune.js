// Entfernt CSS-Selektoren mit Klassen, die im HTML/JS nirgends vorkommen. node tools/cssprune.js datei.html
const fs=require('fs'), postcss=require('postcss'); const f=process.argv[2]; let src=fs.readFileSync(f,'utf8');
const rest=src.replace(/<style>[\s\S]*?<\/style>/g,''); const used=c=>new RegExp('(?<![\\w-])'+c+'(?![\\w-])').test(rest);
let removed=[];
src=src.replace(/<style>([\s\S]*?)<\/style>/g,(m,css)=>{ const root=postcss.parse(css);
 root.walkRules(r=>{ const keep=r.selectors.filter(s=>(s.match(/\.[A-Za-z][\w-]*/g)||[]).every(c=>used(c.slice(1))));
  if(keep.length===r.selectors.length) return; removed.push(...r.selectors.filter(s=>!keep.includes(s))); if(!keep.length) r.remove(); else r.selector=keep.join(','); });
 root.walkAtRules(a=>{ if(a.nodes&&!a.nodes.length) a.remove(); });
 return '<style>'+root.toString()+'</style>'; });
fs.writeFileSync(f,src); console.log(removed.length+' Selektoren entfernt:\n  '+removed.join('\n  '));
