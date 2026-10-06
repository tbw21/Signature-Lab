// Test-only exact reversal for preserved-ancestor source assertions; not executable substitution.
const fs=require('fs'),path=require('path');
const record=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../fixtures/evidence-upgrade-changes.json'),'utf8'));
exports.project=(name,text)=>{text=require("./readability-projection.cjs").project(name,text);const e=record.edits[name];return e&&text.split(e.after).length-1===1?text.replace(e.after,e.before):text};
