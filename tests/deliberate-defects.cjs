'use strict';
// Mutation testing on labelled temporary copies only. A mutant must parse and load,
// then violate a specific assertion. Syntax errors / setup failures do not count as detected defects.
const fs=require('fs'),path=require('path'),os=require('os'),assert=require('assert/strict'),crypto=require('crypto');
const {load}=require('./load.cjs'),FILE=process.argv[2],OUT=process.argv[3],base=fs.readFileSync(FILE,'utf8'),rows=[];
const range=(process.env.TEST_RANGE||'1:999').split(':').map(Number);let idx=0;
const sourceRoot=path.resolve(__dirname,'..');
function app(A){const a=A.Fv(),s=A.Hp(),f=v=>({value:String(v),error:null});a.$refs={};a.$nextTick=async()=>{};a.seed=f(s.mnemonic);a.lockTime=f(s.lockTime);a.psbtVersion='2';a.inputs=s.inputs.map((v,i)=>({id:i,utxoId:f(v.txid+':'+v.vout),amount:f(v.amountSats),pathSuffix:f('0h/'+v.change+'/'+v.addressIndex),sequence:f(v.sequence)}));a.outputs=[{id:9,amount:f(s.outputs[0].amountSats),dest:f('m/84h/0h/0h/0/18')}];a.acknowledged=true;a.recompute();return a}
function signed(A,s,root){let p=A.wp(s,root),raw=A.ap.fromRaw(A.K.decode(A.Np(s,root)[0].txHex));for(let i=0;i<s.inputs.length;i++){const w=raw.getInput(i).finalScriptWitness;p.updateInput(i,{partialSig:[[w[1],w[0]]]},true)}return p}
const tests=[
 ['transaction binding', 'if (K.encode(r.unsignedTx) !== K.encode(i.unsignedTx))\n    throw Error(`This signed transaction', 'if (false)\n    throw Error(`This signed transaction', A=>{const s=A.Hp(),root=A.up(s.mnemonic),raw=A.ap.fromRaw(A.K.decode(A.Np(s,root)[0].txHex));raw.outputs[0].amount+=1n;assert.throws(()=>A.Rp(s,raw.hex,root),/different test/)}],
 ['signature validity', '    if (!f)\n        throw Error(`${o}: signature verification failed.', '    if (false)\n        throw Error(`${o}: signature verification failed.',A=>{const s=A.Hp(),root=A.up(s.mnemonic),raw=A.ap.fromRaw(A.K.decode(A.Np(s,root)[0].txHex));raw.inputs[0].finalScriptWitness[0][12]^=1;assert.throws(()=>A.Rp(s,raw.hex,root),/signature verification failed/)}],
 ['reference comparison', 'references.find(reference => reference.txHex === txHex)', 'references.find(reference => true)',A=>assert.equal(!!A.Up().matched,false)],
 ['unknown metadata rejection', "classification = 'unexpected'; reason = 'Not an expected signing or finalization change'; unexpected++;", "classification = 'expected'; reason = 'Not an expected signing or finalization change'; accepted++;",A=>{const s=A.Hp(),root=A.up(s.mnemonic),p=signed(A,s,root);p.global.proprietary=[[Uint8Array.of(1,120,0),Uint8Array.of(65)]];const r=A.zp(s,{kind:'psbt',bytes:p.toPSBT(2)},A.Np(s,root),root);assert(r.ok);assert.equal(r.metadata.status,'unexpected')}],
 ['worst-observed review cannot be erased', 'rank[tbwCheckOutcome(next)] > rank[tbwCheckOutcome(previous)]','rank[tbwCheckOutcome(next)] < rank[tbwCheckOutcome(previous)]',A=>{const a=app(A);a.acceptArtifact(a.variants[0].txHex);const r=a.report(),j=new A.TbwSessionJournal();j.record(r);j.record({...r,metadata:{status:'unexpected'}});assert.equal(j.checks()[0].metadataStatus,'unexpected');a.destroy()}],
 ['missing evidence cannot claim complete coverage','allRecordedChecksRetained:checks.length>0 && checks.length===retained.length','allRecordedChecksRetained:checks.length>0',A=>{const a=app(A);a.acceptArtifact(a.variants[0].txHex);assert.equal(a.retentionStatus.allRecordedChecksRetained,false);a.destroy()}],
 ['returned-response hash binds exported bytes',"returnedArtifact: { kind: artifact.kind, hex: K.encode(artifact.bytes), sha256: K.encode(ns(artifact.bytes)) }", "returnedArtifact: { kind: artifact.kind, hex: K.encode(artifact.bytes), sha256: '0'.repeat(64) }",A=>{const a=app(A);a.acceptArtifact(a.variants[0].txHex);const e=a.exportEvidence();assert.equal(e.returnedArtifact.sha256,crypto.createHash('sha256').update(Buffer.from(e.returnedArtifact.hex,'hex')).digest('hex'));a.destroy()}],
 ['diagnostic-only export excludes response bytes', '...(includeResponse && result?.evidence ? {evidence:result.evidence} : {})','...(result?.evidence ? {evidence:result.evidence} : {})',A=>{const a=app(A);a.acceptArtifact(a.variants[0].txHex);assert.equal('evidence' in a.diagnosticPackage(),false);a.destroy()}]
];
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'tbw-labelled-mutants-'));
try{
 for(const [name,before,after,probe] of tests){idx++;if(idx<range[0]||idx>range[1])continue;let row={id:idx,name:'Deliberate defect: '+name,status:'failed',mutation:'not-run'};console.log('RUN',idx,name);
  try{
   assert.equal(base.split(before).length-1,1,'Mutation target must be unique');probe(load(FILE).A);
   const mutated=base.replace(before,after),p=path.join(dir,'DO-NOT-USE-'+idx+'.html');fs.writeFileSync(p,mutated);row.mutantSha256=crypto.createHash('sha256').update(mutated).digest('hex');
   const {A}=load(p); // Any loader/syntax failure is invalid, never counted as a killed behavioral mutation.
   try{probe(A);row.mutation='escaped';row.error='Required behavior did not detect deliberate defect';}
   catch(e){if(e.code==='ERR_ASSERTION'){row.status='passed';row.mutation='detected';row.assertion=e.message}else{row.mutation='invalid-test';row.error=e.stack}}
  }catch(e){row.mutation='invalid-setup';row.error=e.stack}
  rows.push(row);console.log(row.status,row.mutation);fs.writeFileSync(OUT,JSON.stringify({complete:false,results:rows},null,2));
 }
}finally{fs.rmSync(dir,{recursive:true,force:true})}
const r={suite:'Deliberate-defect campaign on labelled temporary copies',complete:true,total_defined:tests.length,test_range:range.join(':'),sha256:crypto.createHash('sha256').update(base).digest('hex'),passed:rows.filter(r=>r.status==='passed').length,failed:rows.filter(r=>r.status==='failed').length,detected:rows.filter(r=>r.mutation==='detected').length,escaped:rows.filter(r=>r.mutation==='escaped').length,invalid:rows.filter(r=>r.mutation.startsWith('invalid')).length,results:rows,scope:'Eight targeted mutations, not a global mutation score, firmware attack corpus or independent audit.'};fs.writeFileSync(OUT,JSON.stringify(r,null,2));process.exitCode=r.failed?1:0;
