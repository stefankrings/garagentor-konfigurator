// Fasst mehrfach definierte Selektoren (gleicher @media-Kontext) in der letzten Regel zusammen
const fs=require('fs'), postcss=require('postcss'); const f=process.argv[2]; let src=fs.readFileSync(f,'utf8'); const log=[];
src=src.replace(/<style>([\s\S]*?)<\/style>/g,(m,css)=>{ const root=postcss.parse(css), g={};
 root.walkRules(r=>{ const k=(r.parent.type==='atrule'?'@'+r.parent.params:'')+'|'+r.selector; (g[k]=g[k]||[]).push(r); });
 Object.entries(g).filter(([k,v])=>v.length>1).forEach(([k,v])=>{ const last=v[v.length-1], decl=new Map();
  v.forEach(r=>r.walkDecls(d=>{ decl.delete(d.prop); decl.set(d.prop,d.clone()); }));
  last.removeAll(); decl.forEach(d=>last.append(d)); v.slice(0,-1).forEach(r=>r.remove()); log.push(k); });
 return '<style>'+root.toString()+'</style>'; });
fs.writeFileSync(f,src); console.log(log.length+' zusammengefasst: '+log.join(' · '));
