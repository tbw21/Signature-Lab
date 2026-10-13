'use strict';
// Only historical *source comparison* helpers import this module.
// Live behavioral tests and the authoritative build always use the v0.20.4 HTML.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('node:assert/strict');
const record=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../fixtures/privacy-ux-qualification-projection.json'),'utf8')).files;
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
exports.project=(name,text)=>{
 const r=record[name]; if(!r)return text;
 assert.equal(sha(text),r.newSha256,'Unauthorized change to v0.20.4 source: '+name);
 for(const e of [...r.edits].reverse()){
  assert(e.after&&text.split(e.after).length-1===1,'Non-unique exact privacy/UX reversal: '+name);
  text=text.replace(e.after,e.before);
 }
 assert.equal(sha(text),r.oldSha256,'v0.20.3 source identity mismatch: '+name);
 return text;
};
