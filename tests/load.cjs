'use strict';
const fs=require('fs'),vm=require('vm'),crypto=require('crypto');
function load(file=process.env.TBW_HTML, overrides={}){
 if(!file)throw Error('Set TBW_HTML or supply the candidate HTML path');
 const exact=fs.readFileSync(file,'utf8');
 const code=require('./html.cjs').moduleCode(exact);
 const no=()=>{};
 class Target {constructor(){this.events={};}addEventListener(k,f){(this.events[k]??=new Set).add(f)}removeEventListener(k,f){this.events[k]?.delete(f)}emit(k){for(const f of [...(this.events[k]??[])])f({type:k})}}
 const document=Object.assign(new Target,{createElement:()=>({relList:{supports:()=>true},getContext:()=>null}),querySelectorAll:()=>[],visibilityState:'visible'});
 class Element{};class MutationObserver{observe(){} disconnect(){} takeRecords(){return []}}
 const context={console,Uint8Array,ArrayBuffer,DataView,Buffer,TextEncoder,TextDecoder,crypto:crypto.webcrypto,performance,document,Element,MutationObserver,navigator:{},setTimeout,clearTimeout,setInterval,clearInterval,queueMicrotask,URL,Blob,AbortController,DOMException,requestAnimationFrame:f=>setTimeout(f,16),cancelAnimationFrame:clearTimeout,...overrides};
 context.window=context;context.addEventListener=no;context.removeEventListener=no;
 vm.createContext(context);
 let end=code.indexOf('/* TBW_BOOTSTRAP_BEGIN */');if(end<0)end=code.lastIndexOf('sa.data(`app`');if(end<0)throw Error('Cannot find bootstrap boundary');
 const exports='tbwOutputReview,tbwSaveJson,TbwSessionJournal,tbwSessionCount,tbwMakeGuidedPlan,tbwFormCase,tbwCaseIdentity,tbwRestoreCase,Fv,E_,Pv,iv,nv,w_,S_,C_,up,fp,wp,Tp,Op,kp,Mp,Np,Fp,Ip,Lp,Rp,zp,Bp,Up,Hp,Vp,ap,Ra,K,ns,qc,x_,g_,kg,__,h_,tbwUUID,tbwInspectUr,tbwPsbtMaps,tbwAssessMetadata,tbwReducedResponse,tbwFindingState,tbwPublicTest,tbwResultSnapshot,tbwPolicyReferences,tbwFreeze,TBW_LIMITS,TBW_BUILD,tbwBBQrCodec,tbwBBQrCompression,pp,Af,_d,Cp,Sp,df,tf,nf,of';
 vm.runInContext(code.slice(0,end)+'\nglobalThis.A={'+exports+'};',context,{timeout:10000});
 return {A:context.A,ctx:context,Target};
}
module.exports={load};
if(require.main===module){const {A}=load(process.argv[2]);console.log('demo',A.Up().ok,!!A.Up().matched);const x=A.Fv();x.$refs={};x.$nextTick=async()=>{};x.recompute();console.log('app',x.buildProblem,x.psbtBase64.length,x.variants.length);const b=A.K.decode(A.Vp);console.log('UR',A.Pv(A.w_(b,90).join('\n')).kind);x.destroy();}
