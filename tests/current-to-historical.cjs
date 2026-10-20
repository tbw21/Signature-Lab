'use strict';
// Test-only: historical source provenance, NOT acceptance of current behavior.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),zlib=require('zlib'),assert=require('node:assert/strict');
const files=JSON.parse(fs.readFileSync(path.join(__dirname,'../fixtures/historical-source-bridge-v0204.json'),'utf8')).files;
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
exports.project=(name,text)=>{
 const r=files[name];if(!r)return text;
 if(sha(text)!==r.currentSha256){
   const release=JSON.parse(fs.readFileSync(path.join(__dirname,'../release.json'),'utf8'));
   assert.equal(name,'src/page.html','Unauthorized current source in historical projection: '+name);
   assert.equal(release.version,'0.20.11-rc3','Historical projection candidate version changed');
   const pairs=[
     ['v@@VERSION@@ release candidate: hardware acceptance pending; not approved for public deployment','v@@VERSION@@ development preview: hardware acceptance pending; not approved for public deployment'],
     ['title="Release candidate for disposable-wallet testing. Not approved for public deployment; hardware acceptance pending."','title="Development preview. Not approved for public deployment; hardware acceptance pending."'],
     ['<span class="release-label">RC3</span>','<span class="release-label">Preview</span>'],
     ['is a release candidate for disposable-wallet testing, not an approved public release.','is a development preview, not an approved release.'],
   ];
   let restored=text;
   for(const [current,dev] of pairs){
     assert.equal(restored.split(current).length-1,1,'Missing/duplicated RC3 release change');
     restored=restored.replace(current,dev);
   }
   assert.equal(sha(restored),r.currentSha256,'Unauthorized current source in historical projection: '+name);
 }
 const prior=zlib.inflateSync(Buffer.from(r.priorB64Zlib,'base64'));
 assert.equal(prior.length,r.priorBytes,'Corrupt historical fixture bytes: '+name);
 assert.equal(sha(prior),r.priorSha256,'Corrupt historical fixture digest: '+name);
 return prior.toString('utf8');
};
