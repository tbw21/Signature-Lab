'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const assert=require('node:assert/strict'),cp=require('node:child_process'),zlib=require('node:zlib');
const file=process.argv[2]; if(!file) throw Error('Usage: node tests/unit.cjs artifact.html [results.json]');
const html=fs.readFileSync(file,'utf8');
const code=html.split('/* TBW_BBQR_CODEC_BEGIN */')[1]?.split('/* TBW_BBQR_CODEC_END */')[0];
assert(code,'codec markers present');
const context={Uint8Array};vm.createContext(context);vm.runInContext(code+'\nglobalThis.codec=tbwBBQrCodec();globalThis.factory=createTBWBBQrCodec;',context,{timeout:5000});
const C=context.codec, results=[];let testIndex=0;const range=(process.env.TEST_RANGE||'1:999').split(':').map(Number);
function test(name,fn){testIndex++;if(testIndex<range[0]||testIndex>range[1])return;console.log("RUN",testIndex,name);const started=performance.now();try{fn();results.push({name,status:'passed',ms:Math.round(performance.now()-started)})}catch(e){results.push({name,status:'failed',error:e.stack});}}
function rejects(fn,pattern){assert.throws(fn,pattern);}
function oracle(q){const p=cp.spawnSync('python',[path.join(__dirname,'oracle.py')],{input:JSON.stringify(q),encoding:'utf8',maxBuffer:20*1024*1024,timeout:30000});assert.equal(p.status,0,p.stderr);return JSON.parse(p.stdout);}
function encoded(bytes,encoding='Z',type='P',chunkBytes=75,packed){return oracle({op:'encode',base64:Buffer.from(bytes).toString('base64'),encoding,type,chunkBytes,...(packed?{packedBase64:Buffer.from(packed).toString('base64')}:{})}).frames;}
function receive(frames,codec=C){const s=codec.createSession();for(const f of frames)codec.apply(s,f);return {session:s,result:codec.verify(s)};}
function bytes(seed,n){let x=seed>>>0;return Uint8Array.from({length:n},()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return x&255});}
const patterns=[Uint8Array.of(0),Uint8Array.of(255,1),bytes(42,5),bytes(43,77),bytes(44,850),new Uint8Array(10000).fill(0x42)];
for(const encoding of ['H','2','Z'])for(const type of ['P','T']){
 test(`Python -> BBQr ${encoding}/${type}: six payload sizes, last-first + duplicates`,()=>{
  const vectors=oracle(patterns.map(raw=>({op:'encode',base64:Buffer.from(raw).toString('base64'),encoding,type,chunkBytes:75})));
  vectors.forEach((v,i)=>{const frames=[...v.frames].reverse();frames.splice(1,0,frames[0]);const {session,result}=receive(frames);assert.deepEqual(result.bytes,patterns[i]);assert.equal(result.fileType,type);assert.equal(C.status(session).progress,1);});
 });
}
for(const type of ['P','T'])test(`BBQr -> Python ${type}: compression and fallback round trips`,()=>{
 for(const raw of patterns){const plan=C.plan(raw,type),o=oracle({op:'decode',frames:[...plan.frames].reverse()});assert.equal(o.base64,Buffer.from(raw).toString('base64'));assert.equal(o.type,type);assert.equal(plan.encoding,raw.length<6?'2':plan.encoding);assert(plan.frames.every(f=>f.length<=168));}
});
test('fixed wbits=10 raw compression and level=9 contract',()=>{let seen;const c=context.factory(()=>({deflateRaw:(b,o)=>{seen=o;return b}}));c.plan(Uint8Array.of(1));assert.equal(seen.windowBits,10);assert.equal(seen.level,9);});
test('immutable plans and status snapshots; verify defensive copy',()=>{const p=C.plan(patterns[4]),s=receive(p.frames).session;assert(Object.isFrozen(p));assert(Object.isFrozen(p.frames));assert(Object.isFrozen(C.status(s)));const copy=C.verify(s).bytes;copy.fill(0);assert.deepEqual(C.verify(s).bytes,patterns[4]);});
test('inspect does not mutate an existing session',()=>{const s=C.createSession();C.inspect('B$HP0100AA');assert.equal(C.status(s).received,0);});
test('incomplete state is never verified',()=>{const s=C.createSession();C.apply(s,'B$HP0200AA');assert.equal(C.status(s).done,false);rejects(()=>C.verify(s),/incomplete/);});
test('matching duplicates are idempotent before and after completion',()=>{const s=C.createSession();for(let i=0;i<10;i++)C.apply(s,'B$HP0200AA');assert.equal(C.status(s).received,1);C.apply(s,'B$HP0201BB');for(let i=0;i<5;i++)C.apply(s,'B$HP0201BB');assert.deepEqual(C.verify(s).bytes,Uint8Array.of(170,187));});
test('base36 maximum 1295 parts supported out of order',()=>{const frames=encoded(new Uint8Array(1295).fill(42),'H','P',1);assert.equal(frames[0].slice(4,6),'ZZ');assert.equal(receive(frames.reverse()).result.bytes.length,1295);});
test('512 KiB decoded boundary accepted',()=>{const raw=new Uint8Array(524288).fill(0x31);assert.deepEqual(receive(encoded(raw)).result.bytes,raw);});
test('512 KiB incompressible export with large frame budget',()=>{const raw=bytes(51,524288);const p=C.plan(raw,'P',4288);assert(p.frames.length<=1295);const out=receive(p.frames).result.bytes;assert.deepEqual(out,raw);});
const malformed=[['lowercase header','b$HP0100AA'],['unknown encoding','B$QP0100AA'],['unsupported filetype','B$HJ01007B7D'],['executable filetype','B$HX010090'],['zero count','B$HP0000AA'],['index equal count','B$HP0101AA'],['bad base36','B$HP0!00AA'],['empty payload','B$HP0100'],['odd hex','B$HP0100A'],['lowercase hex','B$HP0100aa'],['invalid hex','B$HP0100GG'],['non-base32','B$2P010018'],['base32 padding','B$2P0100AA======'],['one character base32','B$2P0100A'],['three character base32','B$2P0100AAA'],['six character base32','B$2P0100AAAAAA'],['nonzero pad bits','B$2P0100AB'],['unaligned middle base32','B$2P0200AA'],['embedded whitespace','B$HP0100AA BB'],['embedded newline','B$HP0100AA\nBB'],['oversized QR','B$HP0100'+'AA'.repeat(2145)]];
for(const [label,value] of malformed)test(`reject ${label}`,()=>rejects(()=>C.apply(C.createSession(),value),/BBQr/));
for(const [label,a,b] of [
 ['conflicting encoding','B$HP0200AA','B$2P0201AA'],['conflicting type','B$HP0200AA','B$HT0201BB'],
 ['conflicting count','B$HP0200AA','B$HP0301BB'],['conflicting duplicate','B$HP0200AA','B$HP0200BB'],
 ['unequal middle parts','B$HP0300AA','B$HP0301BBBB'],['long final part','B$HP0200AA','B$HP0201BBBB'],
 ['long final seen first','B$HP0201AAAA','B$HP0200BB']])test(`reject ${label}, then terminal latch and explicit reset`,()=>{const s=C.createSession();C.apply(s,a);rejects(()=>C.apply(s,b),/BBQr/);assert.equal(C.status(s).failed,true);rejects(()=>C.apply(s,'B$HP0100AA'),/failed/);rejects(()=>C.verify(s),/failed/);C.rollback(s);C.apply(s,'B$HP0100AA');assert.equal(C.verify(s).bytes[0],170);});
test('completed transfer rejects a conflicting appended frame',()=>{const s=receive(['B$HP0100AA']).session;rejects(()=>C.apply(s,'B$HP0100BB'),/conflicting/);rejects(()=>C.verify(s),/failed/);});
test('decompression bomb stopped at 512 KiB',()=>{const packed=zlib.deflateRawSync(Buffer.alloc(4*1024*1024,65),{windowBits:10});const frames=encoded(Uint8Array.of(1),'Z','P',75,packed);rejects(()=>receive(frames),/decompressed payload exceeds/);});
test('valid decoded payload at 512 KiB + 1 rejected',()=>rejects(()=>receive(encoded(new Uint8Array(524289).fill(42))),/512 KiB/));
test('raw DEFLATE truncation at every byte position rejected',()=>{const packed=zlib.deflateRawSync(Buffer.from(patterns[4]),{windowBits:10});for(const cut of [1,2,3,5,Math.floor(packed.length/2),packed.length-1]){const f=encoded(Uint8Array.of(1),'Z','P',75,packed.subarray(0,cut));rejects(()=>receive(f),/invalid|truncated/);}});
for(const [name,packed] of [['trailing junk',Buffer.concat([zlib.deflateRawSync(Buffer.from('hello')),Buffer.of(0)])],['concatenated streams',Buffer.concat([zlib.deflateRawSync(Buffer.from('hello')),zlib.deflateRawSync(Buffer.from('world'))])],['zlib wrapper',zlib.deflateSync(Buffer.from('hello'))],['gzip wrapper',zlib.gzipSync(Buffer.from('hello'))],['invalid block',Buffer.of(7)],['empty inflated file',zlib.deflateRawSync(Buffer.alloc(0))]])test(`reject compressed ${name}`,()=>rejects(()=>receive(encoded(Uint8Array.of(1),'Z','P',75,packed)),/BBQr/));
test('input implied by part size exceeds cap: reject before allocation',()=>rejects(()=>C.apply(C.createSession(),'B$HPZZ00'+'AA'.repeat(500)),/512 KiB/));
test('assembled compressed bytes cap before inflate',()=>{const packed=bytes(123,524289);const f=encoded(Uint8Array.of(1),'Z','P',2600,packed);rejects(()=>receive(f),/512 KiB/);});
test('4096-frame budget including duplicate frames',()=>{const s=C.createSession();for(let i=0;i<4096;i++)C.apply(s,'B$HP0200AA');rejects(()=>C.apply(s,'B$HP0201AA'),/session limit/);});
test('4 MiB session character budget including duplicates',()=>{const s=C.createSession(),frame='B$HP0200'+'AA'.repeat(2144);for(let i=0;i<Math.floor(4194304/frame.length);i++)C.apply(s,frame);rejects(()=>C.apply(s,frame),/session limit/);});
test('invalid plan arguments and excess part counts rejected',()=>{for(const input of [null,[],new Uint8Array(0),new Uint8Array(524289)])rejects(()=>C.plan(input),/BBQr/);for(const cap of [0,7,8.5,4289,Infinity])rejects(()=>C.plan(Uint8Array.of(1),'P',cap),/BBQr/);rejects(()=>C.plan(Uint8Array.of(1),'U'),/BBQr/);rejects(()=>C.plan(bytes(77,10000),'P',8),/too many parts/);});
test('compression dependency unavailable: explicit error, Hex/Base32 still work',()=>{const c=context.factory(()=>{throw Error('injected unavailable dependency')});rejects(()=>c.plan(Uint8Array.of(1)),/unavailable/);assert.equal(receive(['B$HP0100AA'],c).result.bytes[0],170);assert.equal(receive(['B$2P0100VI'],c).result.bytes[0],170);rejects(()=>receive(encoded(patterns[4]),c),/unavailable/);});
test('1000 deterministic malformed/random frames cannot complete accidentally',()=>{for(let i=1;i<=1000;i++){const f=String.fromCharCode(...bytes(i,30));const s=C.createSession();rejects(()=>C.apply(s,f),/BBQr/);assert.equal(C.status(s).done,false);}});
test('100 deterministic payload round trips and frame-size invariants',()=>{for(let i=1;i<=100;i++){const raw=bytes(i,i*17),p=C.plan(raw,'P',8*(1+i%30));assert.deepEqual(receive([...p.frames].reverse()).result.bytes,raw);const len=p.frames[0].length;assert(p.frames.slice(0,-1).every(f=>f.length===len));assert(p.frames.at(-1).length<=len);}});
const output={suite:'BBQr unit/contract/fault injection',testRange:range,totalDefined:testIndex,artifact:path.basename(file),passed:results.filter(x=>x.status==='passed').length,failed:results.filter(x=>x.status==='failed').length,results};
if(process.argv[3])fs.writeFileSync(process.argv[3],JSON.stringify(output,null,2));console.log(JSON.stringify({suite:output.suite,passed:output.passed,failed:output.failed,failures:results.filter(x=>x.status==='failed')},null,2));
process.exitCode=output.failed?1:0;
