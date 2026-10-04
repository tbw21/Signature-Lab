#!/usr/bin/env python3
"""Current-byte boundaries for the supplied source audit; no historical runtime substitution."""
from pathlib import Path
import json,hashlib,sys,re,ast
from bs4 import BeautifulSoup
from audit_projection import project,RECORD
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);H=FILE.read_text();S=BeautifulSoup(H,'html.parser');rows=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m='assertion failed'):
 if not v:raise AssertionError(m)
def test(n,f):
 try:f();rows.append({'name':n,'status':'passed'})
 except Exception as e:rows.append({'name':n,'status':'failed','error':repr(e)})
def source(n):
 from evidence_projection import project as evidence
 return evidence(n,(ROOT/n).read_text()) # retained historical boundaries; new ES tests assert current bytes
test('SA-S01 requirements frozen before scoped edits and unique current identity',lambda:(require(sha((ROOT/'docs/SOURCE-AUDIT-ARCHITECTURE-FROZEN.md').read_bytes())==RECORD['architectureSha256']),require(json.loads(source('release.json'))['version']=='0.20.0-rc1')))
def boundaries():
 for n,old in RECORD['baselineHashes'].items():
  raw=source(n);require(sha(raw.encode())==RECORD['currentHashes'][n],n);require(sha(project(n,raw).encode())==old,n)
 require(set(RECORD['edits'])=={'src/metadata.js','src/06-session-download.js','src/session-journal.js','src/20-application.js','src/22-bootstrap.js','src/page.html'})
test('SA-S02 all application bytes mapped and only five runtime modules plus template changed',boundaries)
def negative():
 for n,old in RECORD['baselineHashes'].items():require(sha(project(n,source(n)+'\n// undeclared').encode())!=old,n)
test('SA-S03 projections cannot hide appended undeclared mutation',negative)
def protected():
 for n in ['src/04-bitcoin.js','src/evidence.js','src/reference-self-test.js','src/13-qr-session.js','src/17-camera.js','src/11-bbqr.js','src/19-import.js']:
  require(sha((ROOT/n).read_bytes())==RECORD['baselineHashes'][n],n)
 require(len(json.loads(source('sources.json')))==29)
test('SA-S04 verifier evidence QR camera startup core and source order remain byte-identical',protected)
test('SA-S05 reduced sighash exception is exact and policy version advances',lambda:(require("f.type === 3 && !f.keyData && f.value === '01000000'" in source('src/metadata.js')),require("'psbt-envelope-v3'" in source('src/metadata.js'))))
test('SA-S06 order observations retain positions and explicit conversion basis',lambda:[require(x in source('src/metadata.js'),x) for x in ['beforePosition: beforePositions.get(key)','afterPosition: afterPositions.get(key)','relativeOrderChanged: reordered','retainedBefore.some','same-version-local-reconstruction','fieldOrderAssessed: false']])
test('SA-S07 one shared worst-outcome calculation is used by journal and current report',lambda:(require('function tbwCheckOutcome(check)' in source('src/06-session-download.js')),require('const outcomes = em(checks)' in source('src/session-journal.js')),require('tbwCheckOutcome(entry)' in source('src/session-journal.js')),require('metadata:analysis?.metadata' in source('src/20-application.js')),require('metadataStatus:report.metadata?.status' in source('src/session-journal.js'))))
test('SA-S08 attacker-controlled preview is bounded with a short independent DOM identity',lambda:(require('.slice(0, 32)' in source('src/20-application.js')),require('field.key.slice(0, 128)' in source('src/20-application.js')),require('displayId:index' in source('src/20-application.js')),require(S.select_one('.metadata-fields template').get(':key')=='field.displayId'),require(S.select_one('.metadata-display-limit').get('x-text')=='metadataDetailNotice')))
def agent():
 first='\n'.join(p.read_text() for p in (ROOT/'src').glob('*.js'))
 require('document.modelContext' not in first and '.registerTool(' not in first)
 require('Browser-agent registration retired' in source('src/22-bootstrap.js'))
 require('inspect()' in source('src/20-application.js'))
test('SA-S09 default agent API surface removed without deleting internal inspect contract',agent)
def vendor():
 for n in RECORD['baselineHashes']:
  if n.startswith('vendor/'):require(sha((ROOT/n).read_bytes())==RECORD['baselineHashes'][n],n)
 require(not S.select('link[rel="modulepreload"]'))
 require("connect-src 'none'" in S.select_one('meta[http-equiv="Content-Security-Policy"]')['content'])
 require('fetch(' in source('vendor/01-foundation.js'))
test('SA-S10 inert vendor polyfill retained honestly with no preload links and same offline CSP',vendor)
def visibility():
 for n in ['polish-browser.py','wallet-card-browser.py','alignment-browser.py']:
  t=source('tests/'+n);require('wait_for(state="visible")' in t,n)
 require('timeout=15000' in source('tests/browser.py'))
 require('set_default_timeout(6000)' in source('tests/browser.py'))
test('SA-S11 visible-box helpers synchronize rendering without lengthening interaction budget',visibility)
def pins():
 req=[s for s in source('qualification-requirements.txt').splitlines() if s and not s.startswith('#')]
 require(len(req)==12);require(all(re.fullmatch(r'[A-Za-z0-9_-]+==[0-9.]+',s) for s in req))
 t=source('tools/qualification_environment.py');require('unavailable-environment' in t and "'candidateFailure':False" in t)
 require('pip install' not in t)
test('SA-S12 complete pinned qualification package set and explicit unavailable prerequisite outcome',pins)
def output():
 sys.path.insert(0,str(ROOT));import build
 require('EXPECTED-OUTPUT.json' not in build.inputs()[0])
 expected=json.loads(source('EXPECTED-OUTPUT.json'));require(expected['sha256']==sha(FILE.read_bytes()))
 require(expected['bytes']==FILE.stat().st_size)
 require(expected['sourceSha256']==build.assemble()[1])
test('SA-S13 source-package output receipt matches actual HTML without self-hash recursion',output)
def deps():
 d=json.loads(source('docs/DEPENDENCIES.json'));r=d['auditReportedBehavioralValidation']
 require(r['reportedSignatureComparisons']==1200 and r['reportedVerificationComparisons']==400)
 require(r['rawCorpusOrRunnerSupplied'] is False and r['upstreamComparisonReproducedInThisRemediation'] is False)
 require(all(v['upstreamAuthenticated'] is False for v in d['runtimeSources']))
test('SA-S14 external differential claim attributed, not converted into upstream authentication',deps)
def display():
 require("sessionSummary.review" in H and "guidedStatus.review" in H)
 require('Matched excludes checks needing file review' in H)
 require('Signatures matched. File changes need review.' in H)
 require('Could not complete the check' in H and 'does not rule out seed leakage' in H)
 require(S.select_one('.metadata-order-note').get('x-text')=='metadataOrderExplanation')
test('SA-S15 review totals and retained-field order are discoverable without hiding main warnings',display)
def syntax():
 for p in [ROOT/'qualify.py',ROOT/'tools/qualification_environment.py',ROOT/'tools/verify_output.py']:
  ast.parse(p.read_text(),filename=str(p))
test('SA-S16 new qualification and verification utilities have valid Python syntax',syntax)
def privacy():
 for n in ['src/metadata.js','src/06-session-download.js','src/session-journal.js','src/22-bootstrap.js']:
  t=source(n);require(not re.search(r'getUserMedia|fetch\(|localStorage|setInterval\(',t),n)
 require(".slice(0, 32)" not in source('src/evidence.js'))
 require('x-html' not in source('src/page.html'))
test('SA-S17 UI bounds do not truncate evidence or introduce new acquisition or HTML sinks',privacy)
def docs():
 t=source('docs/SOURCE-AUDIT-DISPOSITION.md');require('99' in t and '83' in t and 'not supplied' in t)
 require('Foundation Prime' in t and 'not diagnosed' in t)
 require('next vendor refresh' in t)
test('SA-S18 audit run-count discrepancy, unprovided evidence and deferred work remain explicit',docs)
r={'suite':'Source-audit current-byte static boundaries','complete':True,'sha256':sha(FILE.read_bytes()),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
