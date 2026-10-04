'use strict';
const fs=require('fs'),{load}=require('./load.cjs'),{A}=load(process.argv[2]),spec=A.Hp(),root=A.up(spec.mnemonic),refs=A.Np(spec,root),out=[];
for(const policy of ['compatible','plain','grind-core','grind-embit'])for(const kind of ['raw','partial0','partial2','final0','final2']){
 const version=kind.endsWith('0')?0:2,s={...spec,psbtVersion:version},reference=refs[0];
 let bytes=A.K.decode(reference.txHex),type='tx';
 if(kind!=='raw'){
  type='psbt';const p=A.wp(s,root),r=A.ap.fromRaw(bytes,{allowUnknownInputs:true,allowUnknownOutputs:true,disableScriptCheck:true});
  for(let i=0;i<s.inputs.length;i++){const w=r.getInput(i).finalScriptWitness;p.updateInput(i,{partialSig:[[w[1],w[0]]]},true)}
  if(kind.startsWith('final'))p.finalize();bytes=p.toPSBT(version);
 }
 const artifact={kind:type,bytes},analysis=A.zp(s,artifact,A.tbwPolicyReferences(refs,policy),root);
 const publicTest=A.tbwPublicTest(s,root,A.K.encode(A.Tp(s,root)),refs);
 const snapshot=A.tbwResultSnapshot({stateKey:'private-test-state',artifactText:A.K.encode(bytes),analysis,error:null,prepared:{spec:s},publicTest,intake:{method:'text',artifact},context:{test:1,walletSession:'public-evidence-fixture',session:{checked:1},sessionChecks:[],scenario:'fixture',scenarioCoverage:[],step:3,inputs:s.inputs.length,outputs:s.outputs.length,device:'fixture, not real hardware',firmware:'not-qualified',signingPolicy:policy}});
 out.push({name:kind+'/'+policy,evidence:snapshot.evidence});
}
fs.writeFileSync(process.argv[3],JSON.stringify(out,null,2));
