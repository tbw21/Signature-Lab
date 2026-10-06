// Test-only exact presentation reversal for retained static checks. No runtime substitution.
const fs=require('fs'),path=require('path');
const record=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../fixtures/readability-changes.json'),'utf8'));
exports.project=(name,text)=>{const e=record.edits[name];return e&&text.split(e.after).length-1===1?text.replace(e.after,e.before):text};
