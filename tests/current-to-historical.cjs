'use strict';
// Test-only: historical source provenance, NOT acceptance of current behavior.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),zlib=require('zlib'),assert=require('node:assert/strict');
const files=JSON.parse(fs.readFileSync(path.join(__dirname,'../fixtures/historical-source-bridge-v0204.json'),'utf8')).files;
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
exports.project=(name,text)=>{
 const r=files[name];if(!r)return text;
 assert.equal(sha(text),r.currentSha256,'Unauthorized current source in historical projection: '+name);
 const prior=zlib.inflateSync(Buffer.from(r.priorB64Zlib,'base64'));
 assert.equal(prior.length,r.priorBytes,'Corrupt historical fixture bytes: '+name);
 assert.equal(sha(prior),r.priorSha256,'Corrupt historical fixture digest: '+name);
 return prior.toString('utf8');
};
