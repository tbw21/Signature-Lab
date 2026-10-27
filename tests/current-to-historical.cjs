'use strict';
// Test-only: historical source provenance, NOT acceptance of current behavior.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),zlib=require('zlib'),assert=require('node:assert/strict');
const files=JSON.parse(fs.readFileSync(path.join(__dirname,'../fixtures/historical-source-bridge-v0204.json'),'utf8')).files;
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const reviewedRC26=Object.freeze({"src/page.html":"5fb24284faa8822dfc53f40dd49107ce503698f4ceb5fbdb885afe8f2e5ef24b","src/style.css":"221e33ad63e0f214c53b44d831d6bec490273bac4fe88e2b89ed5f6492206ce3","src/20-application.js":"4ded7810831f8f841fdde9c9c3f3e94c808eb25605de995c53297c6ab8fcb26d"});
const reviewedRC28=Object.freeze({"src/page.html":"cc24ed0d0de48de6ba9d0e2d73888201a56acd6b4385b63e418fa04c55988425","src/style.css":"9a2c9a385a9082c5915e7ea2b5d252b3ee11775f4d47fcf875c2f06301f9111f","src/20-application.js":"4ded7810831f8f841fdde9c9c3f3e94c808eb25605de995c53297c6ab8fcb26d"});
const reviewedRC34=Object.freeze({"src/page.html":"bc4323fe9ca8f9fc7fe69c885b4c9c912de4d34f207dabbe4f5affb43d1a67f4","src/style.css":"9c4ef0365efdcce75c0411f3aacaba410a882b62f921ad4082b5c6a10fcd2218","src/20-application.js":"c3e4558e8b1d5afa1251691013abdfd1534a646dcd31ac2443c59dbe339fbe58"});
const witnessFiles=Object.freeze({"src/page.html":"page-rc28.html","src/style.css":"style-rc28.css","src/20-application.js":"20-application-rc28.js"});
function verifyReviewedCurrent(name,current){
 if(name==='src/style.css'){
   // Consolidated RC36: independently pin every current CSS byte, then verify
   // historical provenance with an independently pinned RC35 CSS witness.
   assert.equal(sha(current),'f6ad6246153ffbf8eeffbca408a578e1dd2c4a3714446de375ca4d4c522d5f37','Unreviewed RC36 stylesheet bytes');
   current=fs.readFileSync(path.join(__dirname,'../fixtures/rc36-historical/rc35-audit-style.css'),'utf8');
   assert.equal(sha(current),'2add29b1edd73854307e3aba021be193bf2463d5225610c7b2305f26ecf4a9bb','RC35 historical CSS witness altered');
   const auditMarker='\n/* Narrow-header correction:';
   assert.equal(current.split(auditMarker).length,2,'Missing/duplicate historical audit CSS correction');
   const auditAt=current.indexOf(auditMarker);
   assert.equal(sha(current.slice(auditAt)),'a76e39d6af2ad63495738d0d6a31d803acc6b34bf65c48b5da2250375de578e6','Historical audit CSS correction changed');
   current=current.slice(0,auditAt);
 }
 if(name==='src/style.css' && current.includes('\n/* Signature Lab RC35:')){
   const marker='\n/* Signature Lab RC35:';
   assert.equal(current.split(marker).length,2,'Duplicate/unreviewed CSS correction');
   const at=current.indexOf(marker), base=current.slice(0,at), suffix=current.slice(at);
   assert.equal(sha(base),reviewedRC34[name],'Historical RC34 CSS altered');
   assert.equal(sha(suffix),'37d333fece22fe22f96e10fcdb20403981c40abfee4c3e3e6cc1073a69f2bb23','Unreviewed RC35 CSS addition');
   current=base;
 }
 assert.equal(sha(current),reviewedRC34[name],'Unreviewed current source: '+name);
 const base=fs.readFileSync(path.join(__dirname,'../fixtures/rc30-historical/',witnessFiles[name]));
 assert.equal(sha(base),reviewedRC28[name],'RC28 historical witness tampered: '+name);
 if(name==='src/20-application.js'){
   const oldLine='this.$refs?.sessionNav?.focus?.({preventScroll:true});';
   const newLine="document.querySelector('#tbw-settings > summary')?.focus?.({preventScroll:true});";
   const before=base.toString('utf8');assert.equal(before.split(oldLine).length,2,'Historical focus line changed');
   assert.equal(current,before.replace(oldLine,newLine),'Unreviewed focus change to application runtime');
 }
 if(name==='src/style.css'){
   const prov=JSON.parse(fs.readFileSync(path.join(__dirname,'../fixtures/rc36-historical/rc34-css-provenance.json'),'utf8'));
   assert.equal(sha(prov.exactAppend),prov.appendSha256,'CSS append provenance tampered');
   assert(current.endsWith(prov.exactAppend),'Approved CSS tail missing');
   assert.equal(sha(current.slice(0,-prov.exactAppend.length)),prov.baselineSha256,'Pre-RC34 stylesheet altered');
   assert.equal(prov.currentSha256,reviewedRC34[name],'CSS provenance does not pin approved RC34');
 }
}
exports.project=(name,text)=>{
 const r=files[name];if(!r)return text;
 const approved=JSON.parse(fs.readFileSync(path.join(__dirname,'../fixtures/current-ui-provenance.json'),'utf8')).files;
 if(approved[name]){
   verifyReviewedCurrent(name,text);
   assert.equal(approved[name].rc26Sha256,reviewedRC26[name],'Historical RC26 pin changed');
   assert.equal(approved[name].archivedPriorSha256,r.priorSha256,'Historical prior digest was changed: '+name);
 }else assert.equal(sha(text),r.currentSha256,'Unauthorized unreviewed historical source: '+name);
 const prior=zlib.inflateSync(Buffer.from(r.priorB64Zlib,'base64'));
 assert.equal(prior.length,r.priorBytes,'Corrupt historical fixture bytes: '+name);
 assert.equal(sha(prior),r.priorSha256,'Corrupt historical fixture digest: '+name);
 return prior.toString('utf8');
};
