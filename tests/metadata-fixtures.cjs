'use strict';
const {load}=require('./load.cjs'),fs=require('fs'),assert=require('assert/strict');
const {A}=load(process.argv[2]),OUT=process.argv[3],s=A.Hp(),root=A.up(s.mnemonic),refs=A.Np(s,root),raw=A.ap.fromRaw(A.K.decode(refs[0].txHex)),cases=[];
const range=(process.env.TEST_RANGE||'1:999').split(':').map(Number);let index=0;
const f=v=>({value:String(v),error:null});
function app(version){const a=A.Fv();a.$refs={};a.$nextTick=async()=>{};a.seed=f(s.mnemonic);a.lockTime=f(s.lockTime);a.psbtVersion=String(version);a.inputs=s.inputs.map((v,i)=>({id:i,utxoId:f(v.txid+':'+v.vout),amount:f(v.amountSats),pathSuffix:f('0h/'+v.change+'/'+v.addressIndex),sequence:f(v.sequence)}));a.outputs=[{id:9,amount:f(s.outputs[0].amountSats),dest:f('m/84h/0h/0h/0/18')}];a.acknowledged=true;a.recompute();assert(a.transactionReady);return a}
function signed(version){const p=A.wp({...s,psbtVersion:version},root);for(let i=0;i<s.inputs.length;i++){const w=raw.getInput(i).finalScriptWitness;p.updateInput(i,{partialSig:[[w[1],w[0]]]},true)}return p}
const cs=n=>n<253?Buffer.from([n]):n<65536?Buffer.from([253,n&255,n>>8]):Buffer.from([254,n&255,(n>>>8)&255,(n>>>16)&255,n>>>24]);
const pack=maps=>new Uint8Array(Buffer.concat([Buffer.from('70736274ff','hex'),...maps.flatMap(m=>[...Array.from(m.values()).flatMap(x=>{const k=Buffer.from(x.key,'hex'),v=Buffer.from(x.value,'hex');return[cs(k.length),k,cs(v.length),v]}),Buffer.from([0])])]));
for(const preparedVersion of [0,2])for(const returnedVersion of [0,2])for(const shape of ['partial','reduced','reduced-sighash','final','reordered','unknown','selective-removal','inserted-order']){
 index++;if(index<range[0]||index>range[1])continue;const started=Date.now();console.log('START',index,preparedVersion,returnedVersion,shape);
 const a=app(preparedVersion),p=signed(returnedVersion);
 if(shape==='final')p.finalize();
 let rows=A.tbwPsbtMaps(p.toPSBT(returnedVersion));
 if(shape.startsWith('reduced')){
  rows=rows.map((r,index)=>new Map([...r].filter(([k,v])=>index===0||index>s.inputs.length?v.type!==2||index===0:![1,6].includes(v.type))));
  if(shape==='reduced-sighash')for(let i=1;i<=s.inputs.length;i++)rows[i].set('03',{key:'03',value:'01000000'});
 }
 if(shape==='reordered')rows=rows.map(r=>new Map([...r].reverse()));
 if(shape==='unknown')rows[0].set('fa'+('00'.repeat(8)),{key:'fa'+('00'.repeat(8)),value:'abcd'});
 if(shape==='selective-removal'){const key=[...rows[1]].find(([k,v])=>v.type===6)[0];rows[1].delete(key)}
 if(shape==='inserted-order'){const pairs=[...rows[1]],i=pairs.findIndex(([k,v])=>v.type===2),sig=pairs.splice(i,1)[0];rows[1]=new Map([sig,...pairs])}
 a.acceptArtifact(A.K.encode(pack(rows)));assert(a.isTestComplete,shape+': '+a.parseProblem);
 cases.push({name:`prepared${preparedVersion}-returned${returnedVersion}-${shape}`,evidence:a.exportEvidence()});a.destroy();console.log('DONE',index,Date.now()-started);
}
fs.writeFileSync(OUT,JSON.stringify(cases));console.log('Generated',cases.length,'synthetic evidence fixtures');
