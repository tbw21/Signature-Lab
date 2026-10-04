// Test-only exact authorized edit reversal; never imported by application/build.
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const R=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../fixtures/source-audit-changes.json'),'utf8'));
exports.project=(name,text)=>{text=require("./evidence-projection.cjs").project(name,text);for(const e of [...(R.edits[name]||[])].reverse()){
 const count=s=>text.split(s).length-1;
 if(count(e.after)===1)text=text.replace(e.after,e.before);
 else assert.equal(count(e.before),1,'Modified source-audit hunk '+name);
}return text;};
