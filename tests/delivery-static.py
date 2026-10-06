#!/usr/bin/env python3
"""Actual source/HTML checks and exact before-after boundaries for the delivery refinement."""
from pathlib import Path
from audit_projection import read as audit_read
from bs4 import BeautifulSoup
import json,hashlib,sys
from delivery_projection import project,R
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);H=FILE.read_text();S=BeautifulSoup(H,'html.parser');rows=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m='assertion failed'):
 if not v:raise AssertionError(m)
def case(n,f):
 try:f();rows.append({'name':n,'status':'passed'})
 except Exception as e:rows.append({'name':n,'status':'failed','error':repr(e)})
def one(s):
 e=S.select(s);require(len(e)==1,s);return e[0]
case('D-S01 scope was frozen before edits and uniquely identifies reconstructed candidate',lambda:(require(sha((ROOT/'docs/DELIVERY-ARCHITECTURE-FROZEN.md').read_bytes())==R['architectureSha256']),require(json.loads((ROOT/'release.json').read_text())['version']=='0.20.3-rc1')))
def preserve():
 require(len(R['runtime'])==29)
 for name,digest in R['runtime'].items():
  raw=audit_read(name);require(sha(project(name,raw).encode())==digest,name)
  if name!='src/20-application.js':require(sha(raw.encode())==digest,name)
case('D-S02 28 runtime modules unchanged; only declared app navigation reversed to exact baseline',preserve)
def reverse():
 for name,digest in R['before'].items():
  raw=audit_read(name);require(sha(raw.encode())==R['after'][name],name);require(sha(project(name,raw).encode())==digest,name)
case('D-S03 every application edit reverses to exact v0.18.2 bytes',reverse)
def mutations():
 for name,digest in R['before'].items():require(sha(project(name,audit_read(name)+'\n/* undeclared */').encode())!=digest,name)
case('D-S04 undeclared edits cannot be masked by historical projections',mutations)
def helper():
 w=one('#word-count');p=one('#word-count-help');require(p.previous_sibling==w or p.find_previous_sibling()==w)
 require(w.parent==p.parent);require(p.get_text()=='Changing length creates a new test wallet.')
 require('word-count-help' in w['aria-describedby'])
case('D-S05 helper is directly under its selector and programmatically associated',helper)
def copy():
 require('Wallet confirmed' in one('#wallet-loaded').get_text())
 require('Dark Skippy example'==one('#try-example').get_text());require(one('#try-example').get('@click')=='openExample()')
 require("'Import the signed response.'" in one('#verify-title').get('x-text'))
 require(S.select_one('.intake .intro').get_text()=='Scan, import or paste the signed response from your signer.')
case('D-S06 exact approved labels and single existing demo callback',copy)
def safety():
 require('Never enter a real seed' in one('#wallet-safety').get_text());require('Do not add a passphrase.' in one('.seed-instructions').get_text())
 require('Check that the fingerprint matches your signer.'==one('#wallet-compare-hint').get_text())
 require(one('#wallet-loaded').get('@click')=='confirmWalletLoaded()');require(one('#wallet-loaded').get('x-show')=='!isTestComplete')
case('D-S07 wallet safety and explicit operator confirmation remain visible',safety)
def structure():
 for s in ['#seed-qr-display','[x-ref="seedQrCanvas"]','#wallet-fingerprint-value','.seed-grid','#attack-example']:one(s)
 require(one('#seed-qr-display').find('button') is None)
 require('x-data' not in one('#wallet-load-card').attrs)
 require("connect-src 'none'" in one('meta[http-equiv="Content-Security-Policy"]')['content'])
case('D-S08 no duplicated wallet or verifier, no permission or external runtime addition',structure)
def routes():
 for e in S.select('.stepper>button'):require(e.get('@click','').startswith('goToStep('))
 require('scanSignedTransaction' not in str(one('.stepper')))
 app=audit_read('src/20-application.js');nav=app.split('goToStep(e,')[1].split('get resultState()')[0]
 for s in ['getUserMedia(', 'startScan(', 'clearResult(', 'journal.', 'acceptArtifact(']:require(s not in nav,s)
 require("this.intakeOpen = !this.isTestComplete" in nav)
case('D-S09 navigation cannot sign acquire camera reset evidence or bypass journal',routes)
def findings():
 for text in ['Signatures matched. File changes need review.','Could not complete the check','output.address','@click="downloadResult()"','does not rule out seed leakage']:require(text in H,text)
 require('guidedLocked && !guidedStatus.canReceive' in one('.intake fieldset')[':disabled']);require(one('.help-control').get('aria-label')=='Help');require(one('.help-control').find_parent(class_='workspace-nav') is None)
case('D-S10 all critical result branches output review evidence and global Help preserved',findings)
r={'suite':'Delivery scope and source checks','complete':True,'sha256':sha(FILE.read_bytes()),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};OUT.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
