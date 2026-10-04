#!/usr/bin/env python3
"""Exact source boundary and real rendered-markup checks for feedback remediation."""
from pathlib import Path
from audit_projection import read as audit_read
from bs4 import BeautifulSoup
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);H=FILE.read_text();S=BeautifulSoup(H,'html.parser');R=json.loads((ROOT/'fixtures/feedback-changes.json').read_text());rows=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m='assertion failed'):
 if not v:raise AssertionError(m)
def case(n,f):
 try:f();rows.append({'name':n,'status':'passed'})
 except Exception as e:rows.append({'name':n,'status':'failed','error':repr(e)})
def one(s):
 x=S.select(s);require(len(x)==1,s);return x[0]
def reverse(name,t):
 for e in reversed(R['edits'].get(name,[])):
  require(e['after'] and t.count(e['after'])==1,name);t=t.replace(e['after'],e['before'],1)
 return t
case('FB-S01 requirement/architecture identity fixed before edits and new release identity unique',lambda:(require(sha((ROOT/'docs/FEEDBACK-ARCHITECTURE-FROZEN.md').read_bytes())==R['architectureSha256']),require(json.loads((ROOT/'release.json').read_text())['version']=='0.20.0-rc1')))
def runtime():
 require(len(R['runtime'])==29)
 for n,d in R['runtime'].items():
  b=audit_read(n);require(sha(reverse(n,b).encode())==d,n)
  if n!='src/20-application.js':require(sha(b.encode())==d,n)
case('FB-S02 28 runtime modules unchanged and all coordinator edits reverse exactly',runtime)
def boundaries():
 for n,d in R['before'].items():
  b=audit_read(n);require(sha(b.encode())==R['after'][n],n);require(sha(reverse(n,b).encode())==d,n)
case('FB-S03 every application byte is accounted for against the exact v0.18.4 baseline',boundaries)
def tamper():
 for n,d in R['before'].items():require(sha(reverse(n,audit_read(n)+'\n// unexpected').encode())!=d,n)
case('FB-S04 historical projections cannot erase an undeclared extra edit',tamper)
def wallet():
 w=one('#new-test-wallet');require(w.find_parent(class_='seed-toolbar') is not None);require(w.get('@click')=='requestWalletChange()');require(not S.select('#wallet-options'))
 require(w.get(':disabled')=='guidedLocked || scan.active');require(w.get_text()=='New test wallet')
 for i,b in enumerate(S.select('#word-count button')):require(b.get('@click')==f'requestWalletChange({[12,24][i]}, false)')
case('FB-S05 wallet and word length share one guarded request path with no duplicate Advanced reset',wallet)
def confirm():
 d=one('#wallet-replacement');require(d.name=='dialog');require(d.get('@cancel.prevent')=='cancelWalletChange()');require(d.get('@close')=='if (!$el.open) cancelWalletChange()')
 require('clears this tab' in one('#wallet-change-warning').get_text());require('Nothing is saved automatically.' in d.get_text())
 require(one('[x-ref="keepWallet"]').has_attr('autofocus'));require(one('#confirm-new-wallet').get('@click')=='confirmWalletChange()')
case('FB-S06 destructive intent is explicit with safe initial focus and stale-close guard',confirm)
def exports():
 d=one('#wallet-replacement');t=str(d);require("saveBeforeWalletChange('result')" in t);require("saveBeforeWalletChange('session')" in t);require('walletChangeError' in t)
 a=audit_read('src/20-application.js').split('exportHistory() {')[1].split('downloadHistory()')[0]
 require('tbwFreeze(JSON.parse(JSON.stringify({' in a);require('...this' not in a and 'seed.value' not in a)
case('FB-S07 public export detaches reactive data before freezing and prompt retains export errors',exports)
def ended():
 require(one('.guided-status').get('x-show')=="hasGuidedSession && (guidedLocked || workspaceView === 'session')")
 require("guidedStatus.phase === 'ended'" in one('.guided-status-heading .tag').get('x-text'))
 require('CHECKED' in one('.guided-status-heading .tag').get('x-text'));require(one('.ended-session-next').find('button') is not None)
case('FB-S08 ended plan is visible in Session only and not labelled an active case',ended)
def warnings():
 require('recordedOperationFailureCount' in one('#workspace-session .workspace-alert').get('x-show'))
 require('recordedOperationFailureCount' in str(one('.tracker-session')));require("=== 1 ? ' file review'" in str(one('.tracker-session')))
 require('File changes need review' in H and 'Could not complete the check' in H)
case('FB-S09 genuine historical findings remain visible and one review is singular',warnings)
def demo():
 b=one('#try-example');require(b.get('@click')=='openExample()');require(b.get_text()=='Dark Skippy example');require(b.get('aria-describedby')=='example-entry-help')
 require('does not run malicious firmware' in one('#example-operation').get_text());require('not a device test' in one('#example-scope').get_text())
 require('CHECK COMPLETE' in str(one('#attack-example')));require(one('#example-raw').has_attr('readonly'))
case('FB-S10 demo is labelled as a recorded calculation with visible outcome and inspectable bytes',demo)
def isolation():
 a=audit_read('src/20-application.js').split('openExample() {')[1].split('runDemonstration() {')[0]
 for n in ['randomizeAll(', 'beginPreparedTest(', 'acceptArtifact(', 'journal.', 'fetch(', 'getUserMedia(', 'setTimeout(']:require(n not in a,n)
 require('this.runDemonstration()' in a and 'dialog.scrollTop = 0' in a)
case('FB-S11 demo uses existing isolated verifier and has no hidden wallet or camera path',isolation)
def core():
 for s in ['#seed-qr-display','[x-ref="seedQrCanvas"]','#wallet-fingerprint-value','.seed-grid']:one(s)
 require('output.address' in H);require('@click="downloadResult()"' in H);require('does not rule out seed leakage' in H)
 require("connect-src 'none'" in one('meta[http-equiv="Content-Security-Policy"]')['content'])
case('FB-S12 QR identity review evidence scopes and offline CSP remain unchanged',core)
def one_reset():
 a=audit_read('src/20-application.js');require(a.count('randomizeAll(e =')==1);require(a.count('pendingWalletChange = Object.freeze(')==1)
 require('intent.resultRevision === this.resultRevision' in a);require('intent.fileRequest === this.fileRequest' in a)
 require('this.cancelWalletChange();\n    if (!unchanged)' in a);require('pause() { this.cancelWalletChange();' in a)
case('FB-S13 confirmation is consumed before the sole reset and guards stale revisions',one_reset)
def style():
 c=audit_read('src/style.css');require('system-ui' in c and '@font-face' not in c);require('@media(forced-colors:active)' in c)
 require('wallet-replacement-actions' in c);require('min-height:44px' in c)
case('FB-S14 no external font, stable touch targets and reflow/forced-color rules retained',style)
def current_docs():
 text=(ROOT/'README.md').read_text();hardware=(ROOT/'docs/HARDWARE-ACCEPTANCE.md').read_text()
 require('recovered feedback-refinement dev-3 preview' in text)
 require('docs/FEEDBACK-ARCHITECTURE-FROZEN.md' in text)
 require('Never choose an older release as an automatic' in text)
 require('opening untouched v0.14' not in hardware)
 require('Historical v0.15.1' in hardware)
case('FB-S15 handoff names the current baseline and never prescribes an unapproved downgrade',current_docs)
r={'suite':'Feedback static/source boundary','complete':True,'sha256':sha(FILE.read_bytes()),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
