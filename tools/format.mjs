// Formatiert Haupt-Skript und Stylesheets des Templates einheitlich (Prettier). HTML-Markup bleibt unverändert.
import fs from 'fs'; import prettier from './node_modules/prettier/index.mjs';
const f=process.argv[2]; let src=fs.readFileSync(f,'utf8');
const opt={printWidth:110,tabWidth:2,semi:true,singleQuote:false,trailingComma:"none",arrowParens:"avoid",bracketSpacing:true};
// Stylesheets
const css=[...src.matchAll(/<style>([\s\S]*?)<\/style>/g)];
for(const m of css.reverse()){ const out=await prettier.format(m[1],{...opt,parser:"css"}); src=src.slice(0,m.index)+"<style>\n"+out+"</style>"+src.slice(m.index+m[0].length); }
// Haupt-Skript (das längste <script>)
const sc=[...src.matchAll(/<script>([\s\S]*?)<\/script>/g)].sort((a,b)=>b[1].length-a[1].length)[0];
const js=await prettier.format(sc[1],{...opt,parser:"babel"});
if(/<\/script/i.test(js)) throw new Error("</script im Ergebnis");
src=src.slice(0,sc.index)+"<script>\n"+js+"</script>"+src.slice(sc.index+sc[0].length);
fs.writeFileSync(f,src); console.log("formatiert:",f,src.length);
