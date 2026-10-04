'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),cp=require('child_process'),crypto=require('crypto'),acorn=require('./vendor/acorn.cjs');
const FILE=process.argv[2],OUT=process.argv[3],ROOT=path.resolve(__dirname,'..');const html=fs.readFileSync(FILE,'utf8'),code=require('./html.cjs').moduleCode(html),ast=acorn.parse(code,{ecmaVersion:'latest',sourceType:'module'}),results=[];
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
function test(name,f){try{f();results.push({name,status:'passed'})}catch(e){results.push({name,status:'failed',error:e.stack})}}
function walk(n,fn){if(!n||typeof n!=='object')return;if(n.type)fn(n);for(const [k,v]of Object.entries(n)){if(k==='start'||k==='end')continue;if(Array.isArray(v))v.forEach(x=>walk(x,fn));else if(v&&typeof v==='object')walk(v,fn)}}
function tokens(s){return [...acorn.tokenizer(s,{ecmaVersion:'latest'})].map(t=>t.type.label+':'+String(t.value)).join('\n')}
function fn(ast,name){const n=ast.body.find(n=>n.type==='FunctionDeclaration'&&n.id.name===name);assert(n,name);return n}
function source(name){return require('./reference-projection.cjs').project(name,fs.readFileSync(path.join(ROOT,name),'utf8'))}
test('entire runtime parses as an ECMAScript module',()=>assert(ast.body.length>1000));
test('Node checks exact shipped runtime syntax',()=>{const r=cp.spawnSync(process.execPath,['--input-type=module','--check'],{input:code,encoding:'utf8'});assert.equal(r.status,0,r.stderr)});
test('one implementation for every runtime top-level symbol',()=>{const seen=new Set;for(const n of ast.body){const names=n.type==='FunctionDeclaration'||n.type==='ClassDeclaration'?[n.id.name]:n.type==='VariableDeclaration'?n.declarations.flatMap(d=>d.id.type==='Identifier'?[d.id.name]:d.id.type==='ArrayPattern'?d.id.elements.filter(Boolean).map(x=>x.name):[]):[];for(const name of names){assert(!seen.has(name),'Duplicate top-level '+name);seen.add(name)}}});
test('application has no duplicated or shadowed object properties',()=>{let obj;walk(fn(ast,'Fv'),n=>{if(n.type==='ReturnStatement'&&n.argument?.type==='ObjectExpression'&&n.argument.properties.some(p=>p.key?.name==='stateSignature'))obj=n.argument});assert(obj);const seen=new Set;for(const p of obj.properties){const key=p.key?.name??p.key?.value;assert(!seen.has(key),'Duplicate app property '+key);seen.add(key)}});
test('mathematical construction/key/signature implementations preserve baseline tokens',()=>{const baseline=source('fixtures/bitcoin-before.js'),old=acorn.parse(baseline,{ecmaVersion:'latest',sourceType:'module'});for(const name of ['up','dp','fp','pp','mp','hp','gp','_p','vp','yp','bp','xp','Sp','Cp','wp','Tp','Op','kp','jp','Mp','Np','Pp','Fp','Ip','Lp','Rp','Bp','Hp','Up']){const o=fn(old,name),n=fn(ast,name);assert.equal(tokens(code.slice(n.start,n.end)),tokens(baseline.slice(o.start,o.end))),name}});
test('new semantic wrapper uses one underlying transaction and signature verifier',()=>{const z=code.slice(fn(ast,'zp').start,fn(ast,'zp').end);assert(z.includes('tbwAssessMetadata'));assert(z.includes('Rp(')&&z.includes('Bp('));assert(!z.includes('sign('))});
test('Content Security Policy remains offline and denies connections',()=>{const csp=require('./html.cjs').csp(html);assert(csp.includes("connect-src 'none'")&&csp.includes("object-src 'none'")&&csp.includes("base-uri 'none'"));const old=require('./html.cjs').csp(source('baseline/TBW-Signature-Lab-v0.12.2.html'));assert.equal(csp,old)});
test('single inline executable and no external runtime scripts or resources',()=>{assert.equal((html.replace(code,'').match(/<script\b/g)||[]).length,1);assert(!/<script[^>]*\bsrc=/i.test(html));assert(!/<(?:img|link)[^>]*(?:src|href)="https?:\/\//i.test(html));assert(!/@@[A-Z_]+@@/.test(html))});
test('all static HTML IDs are unique',()=>{const ids=[...html.matchAll(/\s+id="([^"]+)"/g)].map(m=>m[1]);assert.equal(new Set(ids).size,ids.length)});
test('segmented BC-UR/BBQr controls retained and legacy dropdown absent',()=>{assert(html.includes('data-qr-mode="ur"')&&html.includes('data-qr-mode="bbqr"'));assert(!html.includes('<select id="qr-format"'));assert(html.includes(':aria-pressed='))});
test('metadata warning and explicit evidence export visible bindings exist',()=>{assert(html.includes('data-metadata-status'));assert(html.includes('metadataSummary?.label'));assert(html.includes('@click="downloadEvidence()"'));assert(html.includes('Review before sharing'))});
test('terminal camera lifecycle and finite-import rules have no retired early-break path',()=>{const text=source('src/19-import.js');assert(!/\bbreak\b/.test(text));const camera=source('src/17-camera.js');for(const event of ['ended','inactive','visibilitychange','CAMERA_START_TIMEOUT','CAMERA_STALLED'])assert(camera.includes(event));assert(!source('src/20-application.js').includes('120000'))});
test('no seed/raw application spread in public snapshot or exports', () => { const text = source('src/evidence.js'); for (const forbidden of ['...prepared', '...context', 'JSON.stringify(prepared']) { assert.equal(text.includes(forbidden), false); } assert(text.includes('publicKeyHex')); });
test('compression vendor bytes embedded verbatim with original MIT and zlib notices',()=>{assert(html.includes(source('vendor/pako-1.0.11.min.js')));for(const marker of ['This notice may not be removed','Vitaly Puzrin','Andrei Tuputcyn'])assert(html.includes(marker),marker)});
test('source lock covers every authoritative assembly input',()=>{const r=cp.spawnSync('python',['-c','import build; build.locked(); print("verified")'],{cwd:ROOT,encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});assert.equal(r.status,0,r.stderr)});
test('build no longer reads a previous HTML or downloads dependencies',()=>{const s=source('build.py');assert(!s.includes("read_text('baseline"));assert(!s.includes('urllib')&&!s.includes('requests.'));assert(s.includes('os.link(name,path)'))});
test('artifact matches deterministic source assembly exactly',()=>{const r=cp.spawnSync('python',['-c','import build,hashlib; print(hashlib.sha256(build.assemble()[0]).hexdigest())'],{cwd:ROOT,encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});assert.equal(r.status,0,r.stderr);assert.equal(r.stdout.trim(),sha(html))});
test('runtime has no persistence or broadcast operations',()=>{assert(!/localStorage|sessionStorage|indexedDB/.test(code));assert(!/sendrawtransaction/.test(code));assert(!/Math\.random\(/.test(source('src/reliability-common.js')))});
test('release identifier and embedded source build identity agree',()=>{const release=JSON.parse(source('release.json'));assert(code.includes('"version":"'+release.version+'"'));assert(html.includes('Signature Lab v'+release.version));assert(code.includes('publisherAuthenticated":false'))});
test('consolidated fingerprint uses the existing cached root with unavailable/zero guards',()=>{const app=source('src/20-application.js');assert(app.includes('get walletFingerprint()'));assert(app.includes("fingerprint.toString(16).padStart(8,'0').toUpperCase()"));assert(app.includes('seedRenderRequest'));assert(html.includes('wallet-fingerprint-value'));});
test('historical checks have one read-only journal projection, not a writable UI ledger',()=>{const app=source('src/20-application.js');assert(app.includes('get sessionChecks()'));assert(!/this\.sessionChecks\s*=|app\.sessionChecks\s*=/.test(app));assert.equal((app.match(/journal = new TbwSessionJournal/g)||[]).length,2);});
test('guided plan is optional, bounded and separate from the signing implementation',()=>{const s=source('src/guided-plan.js');assert(s.includes('> 200'));assert(!/\b(Np|Mp|Op|zp|up|signIdx)\(/.test(s));assert(html.includes('Start guided session'));assert(html.includes('not a safety guarantee'));});
test('guided controller has no camera acquisition, timer, signer or network engine',()=>{const s=source('src/session-journal.js');assert(!/getUserMedia|setTimeout|setInterval|fetch\(|XMLHttpRequest|signIdx/.test(s));assert(s.includes('halted'));assert(s.includes('2000'));});
test('remediation: all modules are identical after reversing declared startup additions to the accepted v0.15.2 baseline',()=>{
 const expected=JSON.parse(source('fixtures/calm-unchanged.json'));
 for(const [name,hash] of Object.entries(expected))assert.equal(sha(source(name)),hash,name);
 assert(Object.keys(expected).length>20);
});
test('remediation: no unintended application operations changed',()=>{
 const permitted=new Set(['scan','startScan','onScanHit','scanDiagnostics','downloadScanDiagnostics','invalidate',
   'resultDisplayState','metadataExplanation','metadataFieldLabel','completedScanNote',
   'workspaceView','workspaceRequest','outputsOpen','showFileDetails','openWorkspace','showAdvancedSettings','routineNotice','outputReview',
   'formatReviewAmount','sessionHistory','recordedReviewCount','recordedIncompleteCount','historyLabel','historyTone','scenarioName','exportHistory','downloadHistory','downloadResult',
   'focusSection','focusCurrentSection','goToStep','beginPreparedTest','acceptArtifact','verify','downloadReport','downloadEvidence','downloadSessionReport']);
 function normalized(text){
  const parsed=acorn.parse(text,{ecmaVersion:'latest'});let obj;
  walk(parsed,n=>{if(n.type==='ReturnStatement'&&n.argument?.type==='ObjectExpression'&&n.argument.properties.some(p=>p.key?.name==='stateSignature'))obj=n.argument});
  assert(obj);let out=text;
  for(const p of obj.properties.filter(p=>permitted.has(p.key?.name)).sort((a,b)=>b.start-a.start)){
   let end=p.end;while(/\s/.test(text[end]))end++;if(text[end]===',')end++;
   out=out.slice(0,p.start)+out.slice(end);
  }
  return tokens(out);
 }
 assert.equal(normalized(source('src/20-application.js')),normalized(source('fixtures/remediation-before/20-application.js')));
});
test('UX: disclosures exist once, are closed initially and leave required status outside',()=>{
 assert.equal((html.match(/id="advanced-tools"/g)||[]).length,1);
 assert(!/<details[^>]*id="advanced-tools"[^>]*\sopen(?:[\s>])/.test(html));
 assert(html.includes('class="guided-status"') && html.includes('guidedStatus.phase'));
 assert(html.includes('id="workspace-advanced"'));assert(html.includes('id="result-tools"'));assert(html.includes('Custom settings in use'));
 assert(html.includes('Hardware acceptance pending'));assert(html.includes('The release is unsigned'));
});
test('UX: required disclosure and source identity bindings are native, local and readonly',()=>{
 assert(html.includes('x-ref="advancedTools"'));assert(html.includes('releaseSourceHash'));
 assert(html.includes('@toggle="settingsOpen = $el.open"'));assert(!html.includes('beginnerVerifier'));
});
test('UX: rigid planner count width and nowrap button restriction are retired',()=>{
 const css=source('src/style.css');assert(!css.includes('.guided-plan-controls>div:first-child{width:140px}'));
 assert(css.includes('minmax(min(100%,12rem),1fr)'));assert(!css.includes('.button{white-space:nowrap;'));
 assert(!/(?:html|body)\s*\{[^}]*overflow-x\s*:\s*(?:hidden|clip)/.test(css));
});
test('remediation: raw input values and unknown fields are not allowlisted by device name',()=>{
 const m=source('src/metadata.js');assert(m.includes('tbwReducedResponse'));assert(!/SeedSigner|COLDCARD|firmware|device\s*===/.test(m));
 assert(m.includes("classification = 'unexpected'"));assert(m.includes('supportingFieldsRemoved'));
});
test('remediation: strict finite input and bounded pre-admission camera rejection remain distinct',()=>{
 const q=source('src/13-qr-session.js'),app=source('src/20-application.js');
 assert(q.includes("options.source ?? 'finite'"));assert(q.includes("this.source !== 'camera'"));
 assert(q.includes('this.consecutiveRejected >= 8 || this.rejectedFrames >= 24'));
 assert(app.includes("new E_({source:'camera'})"));assert(!source('src/19-import.js').includes("source:'camera'"));
});
test('remediation: internal decoder exceptions are not described as camera checksum noise',()=>{
 const q=source('src/13-qr-session.js');assert(q.includes("error?.message === 'Invalid Checksum'"));assert(q.includes("'UR_DECODER_INTERNAL'"));
 assert(!q.includes("catch { tbwFail('UR_FRAME_CHECKSUM'"));
});
test('remediation: one shared overall-finding rule drives report and presentation',()=>{
 assert(source('src/evidence.js').includes('report.overallStatus = tbwFindingState('));
 assert(source('src/20-application.js').includes('return tbwFindingState('));
 assert(html.includes(':data-result-state="resultDisplayState"'));assert(html.includes('Signatures matched. File changes need review.'));
});
test('remediation: diagnostical download excludes raw QR content by construction',()=>{
 const app=source('src/20-application.js');const a=app.indexOf('scanDiagnostics()'),b=app.indexOf('downloadScanDiagnostics()',a);
 const f=app.slice(a,b);assert(f.includes('tbw-scan-diagnostics-v1'));assert(!/artifactText|mnemonic|seed.value|privateKey|originalText/.test(f));
 assert(html.includes('Save scan diagnostics'));
});
test('calm: verification method differs only by revealing the test workspace',()=>{
 function method(text){let found;walk(acorn.parse(text,{ecmaVersion:'latest'}),n=>{if(n.type==='Property'&&n.key?.name==='verify')found=text.slice(n.start,n.end)});assert(found);return tokens(found.replace("this.workspaceView = 'test'; ",''));}
 assert.equal(method(source('src/20-application.js')),method(source('fixtures/calm-before/20-application.js')));
});
test('calm: output review and JSON filename helpers are single-purpose projections',()=>{
 const output=source('src/output-review.js');assert(!/signIdx|fetch\(|privateKey|setTimeout|new TbwSessionJournal/.test(output));
 assert(output.includes('item.amountSats'));assert(output.includes('publicTest.outputs.map'));
 const download=source('src/06-session-download.js');assert(download.includes("['record','detail','journal','notes']"));
 assert.equal((code.match(/function tbwSaveJson\(/g)||[]).length,1);
});
test('calm: three explicit workspace buttons and visible unresolved finding bindings',()=>{
 for(const id of ['workspace-test','workspace-advanced','workspace-session'])assert(html.includes('id="'+id+'"'));
 assert(html.includes('Recorded findings need review'));assert(html.includes('Inspect file changes'));
 assert(html.includes('@click="downloadResult()"'));assert(html.includes('Save summary only'));
});
test('calm: full read-only output review has no editing or shortened-address substitution',()=>{
 assert(html.includes('output.address'));assert(html.includes('output.amountSats'));assert(html.includes('output.role'));
 const output=source('src/output-review.js');assert(output.includes('scriptHex'));assert(!output.includes('slice('));
});
test('calm: asynchronous view focus has cancellation guards',()=>{
 const app=source('src/20-application.js');assert(app.includes('request !== this.workspaceRequest'));
 assert(app.includes('view !== this.workspaceView'));assert(app.includes('epoch !== this.epoch'));
});
test('alignment: retained 29-unit alignment baseline is preserved after declared startup additions',()=>{
 const expected=JSON.parse(source('fixtures/alignment-unchanged.json'));assert.equal(Object.keys(expected).length,29);
 for(const [name,value] of Object.entries(expected))assert.equal(sha(source(name)),value,name);
});
test('alignment: original interaction, data-display and canvas bindings preserved exactly',()=>{
 const script=`from html.parser import HTMLParser
import json
from pathlib import Path
class P(HTMLParser):
 def __init__(self):super().__init__();self.bindings=[];self.canvases=[]
 def handle_starttag(self,tag,attrs):
  for name,value in attrs:
   if name.startswith('@') or name in ['x-ref','x-text','x-for','x-show','x-model',':disabled',':aria-pressed',':aria-expanded']:self.bindings.append([name,value])
  if tag=='canvas':self.canvases.append(sorted(attrs))
import sys;sys.path.insert(0,'tests')
from reference_projection import read
p=P();p.feed(read('src/page.html'))
expected=json.loads(Path('fixtures/alignment-bindings.json').read_text())
assert sorted(p.bindings)==expected['bindings']
assert json.loads(json.dumps(p.canvases))==expected['canvases']
`;
 const r=cp.spawnSync('python',['-c',script],{cwd:ROOT,encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});assert.equal(r.status,0,r.stderr);
});
test('alignment: instructions occur once below the word grid, separate from QR controls',()=>{
 const page=source('src/page.html');assert.equal((page.match(/class="seed-instructions"/g)||[]).length,1);
 assert.equal((page.match(/id="seed-scan-title"/g)||[]).length,1);
 assert(page.indexOf('class="seed-instructions"')>page.indexOf('</ol>'));
 assert(page.indexOf('class="seed-instructions"')<page.indexOf('aria-label="Disposable wallet QR code"'));
 assert(!page.includes('class="seed-scan-copy"'));assert(page.includes('class="seed-qr-actions"'));
});
test('alignment: trailing actions preserve DOM order and retain mobile equal-size controls',()=>{
 const css=source('src/style.css');assert(css.includes('.workspace-heading .workspace-nav{margin-inline-start:auto}'));
 assert(css.includes('.button-group,.import-actions,.result-actions,.transaction-toolbar,.guided-start-row{justify-content:flex-end}'));
 assert(css.includes('.seed-qr-actions{display:flex'));assert(!/row-reverse|column-reverse/.test(css));
 assert(css.includes('repeat(3,minmax(0,1fr))'));
});
test('alignment: historical alignment introduces no dependency or build controller; declared startup addition separately checked',()=>{
 const order=JSON.parse(source('sources.json'));const fixed=JSON.parse(source('fixtures/alignment-unchanged.json'));
 assert(order.every(name=>name in fixed));assert.equal(order.length,28);
 assert(source('docs/ALIGNMENT-ARCHITECTURE-FROZEN.md').includes('No new features'));
});
const out={suite:'Static/syntax/architecture/source-preservation',artifact:path.basename(FILE),sha256:sha(html),passed:results.filter(r=>r.status==='passed').length,failed:results.filter(r=>r.status==='failed').length,results};if(OUT)fs.writeFileSync(OUT,JSON.stringify(out,null,2));console.log(JSON.stringify(out,null,2));process.exitCode=out.failed?1:0;
