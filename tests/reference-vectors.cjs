'use strict';
const fs=require('fs'),path=require('path'),{load}=require('./load.cjs');const A=load(process.argv[2]).A;
const rows=JSON.parse(fs.readFileSync(path.join(__dirname,'../fixtures/reference-audit-vectors.json')));
const n=A.qc.Point.Fn.ORDER,ser=x=>x.toString(16).padStart(64,'0');
const boundaries=[];for(const key of [1n,n-1n])for(const hash of [0n,1n,n-1n,n,n+1n,2n**256n-1n])boundaries.push({sk:ser(key),msghash:ser(hash)});
const all=rows.concat(boundaries).map((row,i)=>({id:i+1,source:i<16?'supplied-audit':'independent-boundary',...row,actual:Object.fromEntries(['plain','grind-core','grind-embit'].map(mode=>[mode,A.K.encode(A.Op(A.K.decode(row.msghash),A.K.decode(row.sk),mode))]))}));
fs.writeFileSync(process.argv[3],JSON.stringify(all,null,2));console.log('Exported '+all.length+' public test vectors for independent replay');
