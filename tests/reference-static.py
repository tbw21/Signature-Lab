#!/usr/bin/env python3
"""Current-byte audit gate preservation; historical projections cannot excuse other edits."""
from pathlib import Path
from audit_projection import read as audit_read
import hashlib,json,sys,re
from reference_projection import project, RECORD
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);rows=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def check(v,m='assertion failed'):
 if not v:raise AssertionError(m)
def case(name,f):
 try:f();rows.append(dict(name=name,status='passed'))
 except Exception as e:rows.append(dict(name=name,status='failed',error=repr(e)))
page=audit_read('src/page.html');code=audit_read('src/reference-self-test.js');app=audit_read('src/20-application.js')
def preservation():
 for name,digest in RECORD['baselineInputs'].items():
  text=audit_read(name);check(sha(project(name,text).encode())==digest,name)
 check(set(RECORD['edits'])=={'sources.json','src/20-application.js','src/21-navigation.js','src/page.html'})
case('R-S01 exact authorized reversals restore every baseline source/vendor/template/style/build byte',preservation)
def gate_order():
 start=app.index('function Fv() {');gate=app.index('tbwReferenceSelfTest.apply();',start)
 check(start<gate<app.index("let e = ''",start)<app.index('new TbwSessionJournal()',start))
 check(app.index('tbwReferenceSelfTest.verify();',start)<app.index("let e = ''",start))
case('R-S02 startup gate precedes wallet, journal and generated-transaction construction',gate_order)
def source_order():
 actual=json.loads((ROOT/'sources.json').read_text());old=json.loads(project('sources.json',(ROOT/'sources.json').read_text()))
 check(actual.count('src/reference-self-test.js')==1);check([n for n in actual if n!='src/reference-self-test.js']==old)
 check(actual.index('src/04-bitcoin.js')<actual.index('src/reference-self-test.js')<actual.index('src/20-application.js'))
case('R-S03 exactly one new gate module between authoritative crypto and application',source_order)
def vector_source():
 v=json.loads(re.search(r'Object.freeze\((\[.*\])\.map\(row',code).group(1))
 check(v==json.loads((ROOT/'fixtures/reference-audit-vectors.json').read_text()));check(len(v)==16)
case('R-S04 all 16 vector inputs and 48 expected answers are literal supplied values',vector_source)
def scope():
 for forbidden in ['getRandomValues','Math.random','fetch(','document.','navigator.','setTimeout','setInterval','localStorage','mnemonic','new TbwSessionJournal']:
  check(forbidden not in code,forbidden)
 check('Op(digest, key, method)' in code);check('qc.verify(expected, wrong' in code)
case('R-S05 known-answer gate uses existing signer and verifier with no wallet, RNG, network or timer engine',scope)
def immutable():
 check('get referenceSelfCheck() { return tbwReferenceSelfTest.status(); }' in app)
 check('Object.freeze({inspect:status, plan, apply, verify, status, rollback})' in code)
 check('reset:false' in code);check('state.phase === \'failed\'' in code)
case('R-S06 status is read-only and rollback cannot revive a failed gate',immutable)
def claims():
 for phrase in ['BIP 461 (Draft)','not claim full conformance','does not remove the information channel','does not prove that a device used fresh randomness','not inherently impossible over optical QR']:
  check(phrase in page,phrase)
 check('Taproot remains outside this release' in page)
 check('does not authenticate this file' in page)
case('R-S07 audit-related Help preserves uncertain-source and conditional-attack limitations',claims)
def calm():
 check(page.count('id="reference-self-check-note"')==1)
 start=page.index('id="technical-help"');end=page.index('</div></details>',start)
 check(start<page.index('id="reference-self-check-note"')<end)
 check(page.count('id="test-purpose"')==1)
case('R-S08 successful self-check status is confined to existing technical Help',calm)
case('R-S09 mandatory architecture receipt is unchanged',lambda:check(sha((ROOT/'docs/REFERENCE-ARCHITECTURE-FROZEN.md').read_bytes())==RECORD['architectureSha256']))
def projection_negative():
 text=audit_read('src/20-application.js').replace('this.epoch++','this.epoch--',1)
 check(sha(project('src/20-application.js',text).encode())!=RECORD['baselineInputs']['src/20-application.js'])
 text=audit_read('src/20-application.js').replace('tbwReferenceSelfTest.apply();','',1)
 try:project('src/20-application.js',text)
 except AssertionError:return
 raise AssertionError('Missing gate was hidden by projection')
case('R-S10 unauthorized math/state edits or missing gate cannot be masked by preservation projection',projection_negative)
r=dict(suite='Reference audit static/preservation',sha256=sha(FILE.read_bytes()),complete=True,passed=sum(x['status']=='passed' for x in rows),failed=sum(x['status']=='failed' for x in rows),results=rows)
OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
