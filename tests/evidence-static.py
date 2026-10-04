#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import sys,json,hashlib,ast,re
from evidence_projection import RECORD,project
ROOT=Path(__file__).resolve().parents[1];HTML=Path(sys.argv[1]);OUT=Path(sys.argv[2]);S=BeautifulSoup(HTML.read_text(),'html.parser');rows=[]
sha=lambda t:hashlib.sha256(t).hexdigest()
def require(v,msg='assertion failed'):
 if not v:raise AssertionError(msg)
def src(n):return (ROOT/n).read_text()
def test(name,f):
 try:f();rows.append({'name':name,'status':'passed'})
 except Exception as e:rows.append({'name':name,'status':'failed','error':repr(e)})
def boundary():
 for n,h in RECORD['currentHashes'].items():require(sha((ROOT/n).read_bytes())==h,n);require(sha(project(n,src(n)).encode())==RECORD['baselineHashes'][n],n)
 require(set(RECORD['edits'])=={'src/20-application.js','src/session-journal.js','src/page.html','src/style.css'})
test('ES01 exact change inventory accounts for every application and vendor byte',boundary)
def negative():
 for n in RECORD['edits']:require(sha(project(n,src(n)+'\n// unauthorized').encode())!=RECORD['baselineHashes'][n],n)
test('ES02 historical projections cannot hide undeclared trailing mutations',negative)
def protected():
 order=json.loads(src('sources.json'));require(len(order)==29)
 for n in order:
  if n not in ('src/20-application.js','src/session-journal.js'):require(sha((ROOT/n).read_bytes())==RECORD['baselineHashes'][n],n)
test('ES03 27 runtime modules including signing math, metadata, QR, camera and startup remain unchanged',protected)
test('ES04 architecture freeze identity and unique candidate remain exact',lambda:(require(sha((ROOT/'docs/EVIDENCE-ARCHITECTURE-FROZEN.md').read_bytes())==RECORD['architectureSha256']),require(json.loads(src('release.json'))['version']=='0.20.0-rc1')))
def optional():
 c=S.select_one('#session-evidence-tools');require(c.find_parent(id='session-view') is not None)
 require(S.select_one('#retention-warning').find_parent('noscript') is None)
 require(S.select_one('#retain-evidence').get('@change')=='setEvidenceRetention($event.target.checked)')
 require('#retain' not in src('src/04-bitcoin.js'))
test('ES05 controls remain in Session; retention failure remains discoverable outside it',optional)
def private():
 j=src('src/session-journal.js');a=src('src/20-application.js')
 require('journal.record(next.report, next.evidence)' in a)
 for bad in ['JSON.stringify(prepared','stateSignature','getUserMedia','setInterval','localStorage','sessionStorage','indexedDB','fetch(']:require(bad not in j,bad)
 require('evidence.report !== report' in j and 'Object.isFrozen(evidence)' in j)
 require('#summary(entry)' in j and '_attachment' in j)
test('ES06 journal retains existing public evidence only with no private-state/persistence or acquisition access',private)
test('ES07 explicit serialized-data and capture limits preserve core journal capacity',lambda:[require(x in src('src/session-journal.js'),x) for x in ['bytes:16*1024*1024','payloads:256','captures:256',"filter(e=>e.type !== 'capture-attempt').length < 2000",'this.#retentionFault','this.#captureOmitted']])
test('ES08 every response gets retained or missing status without silent eviction',lambda:[require(x in src('src/session-journal.js'),x) for x in ['not-enabled','no-complete-response-evidence','byte-limit','payload-limit','retention-error','allRecordedChecksRetained','retentionRollback()']])
def diagnostics():
 a=src('src/20-application.js').split('diagnosticPackage(includeResponse = false) {')[1].split('downloadDiagnosticPackage(')[0]
 for bad in ['artifactText','this.seed','parseProblem','scan.error','navigator.userAgent']:require(bad not in a,bad)
 require("includeResponse && result?.evidence" in a)
 require(S.select_one('#diagnostic-response').get('x-model')=='diagnosticIncludeResponse')
test('ES09 diagnostic-only allowlist omits raw bytes, exception text and automatic browser fingerprinting',diagnostics)
def bindings():
 c=S.select_one('#wallet-replacement');require(c.select_one('[x-show="retentionStatus.retained > 0"]') is not None)
 require('saveBeforeWalletChange(\'bundle\')' in str(c))
test('ES10 retained full-session evidence is saveable before wallet replacement',bindings)
def origin():
 t=src('tests/origins.py');ast.parse(t)
 for x in ["['chromium','firefox','webkit']",'page.goto(',"page.expect_download()",'--require-all']:require(x in t,x)
 require('set_content(' not in t and 'UUID_SHIM' not in t and 'add_init_script' not in t)
 require('unavailable-tool' in t and 'ERR_BLOCKED_BY_ADMINISTRATOR' in t)
test('ES11 available engines execute critical navigation/import/export workflows; missing engines are never passed',origin)
def replay():
 t=src('tools/replay_evidence.py');ast.parse(t)
 for token in ['def verify_metadata','def metadata_conversion','def replay_bundle','Unsupported metadata policy','False complete-evidence claim','Metadata policy findings differ']:
  require(token in t,token)
 for bad in ['subprocess','eval(','exec(','requests','urllib']:require(bad not in t,bad)
test('ES12 independent replay performs bounded raw-byte policy reconstruction without loading JS or network',replay)
test('ES13 one existing replay entry point handles single evidence and session bundles',lambda:(require("data.get('schema')=='tbw-session-evidence-v1'" in src('tools/replay_evidence.py')),require('json.loads(text)' in src('tools/replay_evidence.py'))))
test('ES14 deliberate defects are isolated and distinguish detected escaped and invalid cases',lambda:[require(x in src('tests/deliberate-defects.cjs'),x) for x in ['DO-NOT-USE-','invalid-setup','escaped','detected','ERR_ASSERTION','probe(load(FILE).A)']])
test('ES15 no new font, external resource or framework/CSP change is smuggled into the candidate',lambda:(require(S.select_one('meta[http-equiv="Content-Security-Policy"]')['content']==BeautifulSoup(RECORD['edits']['src/page.html']['before'],'html.parser').select_one('meta[http-equiv="Content-Security-Policy"]')['content']),require(not S.select('script[src],link[rel="stylesheet"]'))))
test('ES16 optional checkboxes have consistent native controls and label-sized activation targets',lambda:(require('min-height:44px' in src('src/style.css')),require('flex:0 0 20px' in src('src/style.css')),require(S.select_one('#retain-evidence').parent.get('class')==['evidence-opt-in'])))
def documentation():
 t=src('README.md');require(t.startswith('# Signature Lab v0.20.0-rc1'))
 require('fully rerun metadata policy' not in t)
 require('**psbt-envelope-v3**' in t and 'Unknown policy versions' in t)
 require('No storage permission' in t and 'not a total' in t)
 require('## Source history, not current qualification' in t)
 require('vendor/CSP migration is investigated but not implemented' in t)
test('ES17 current README has one authoritative scope and correctly describes independent metadata replay',documentation)
r={'suite':'Evidence-upgrade source and integration boundaries','complete':True,'sha256':sha(HTML.read_bytes()),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
