'use strict';
// Recorded disposable fixtures are input-only. Recreate every reference and PSBT
// using the current candidate, then send the resulting bytes to Python/OpenSSL.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{load}=require('./load.cjs');
const file=process.argv[2],out=process.argv[3],{A}=load(file);
const fixtures=JSON.parse(fs.readFileSync(path.join(__dirname,'../fixtures/crypto-vectors.json')));
const results=fixtures.map(f=>{const spec={...f.spec,inputs:f.spec.inputs.map(i=>({...i,amountSats:BigInt(i.amountSats)})),outputs:f.spec.outputs.map(o=>({...o,amountSats:BigInt(o.amountSats)}))},root=A.up(spec.mnemonic);
 const variants=A.Np(spec,root);assert.equal(JSON.stringify(variants),JSON.stringify(f.variants),'inherited signing results changed');
 return {scenario:f.scenario,spec,variants,psbt0:A.K.encode(A.Tp({...spec,psbtVersion:0},root)),psbt2:A.K.encode(A.Tp({...spec,psbtVersion:2},root)),publicTest:A.tbwPublicTest(spec,root,A.K.encode(A.Tp(spec,root)),variants)};
});
fs.writeFileSync(out,JSON.stringify(results,(k,v)=>typeof v==='bigint'?v.toString():v,2));console.log('Rebuilt '+results.length+' current-candidate fixtures');
