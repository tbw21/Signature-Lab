#!/usr/bin/env python3
"""Actual current UI/input boundary checks plus exact declared source-change accounting."""
from pathlib import Path
from audit_projection import read as audit_read
from html.parser import HTMLParser
import sys,json,hashlib,re
from clarity_projection import project,RECORD
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);rows=[]
page=audit_read('src/page.html');css=audit_read('src/style.css');app=audit_read('src/20-application.js');html=FILE.read_text();sha=lambda x:hashlib.sha256(x).hexdigest()
def check(v,m='assertion failed'):
 if not v:raise AssertionError(m)
def case(name,f):
 try:f();rows.append(dict(name=name,status='passed'))
 except Exception as e:rows.append(dict(name=name,status='failed',error=repr(e)))
case('CL-S01 frozen architecture identity preserved',lambda:check(sha((ROOT/'docs/CLARITY-ARCHITECTURE-FROZEN.md').read_bytes())==RECORD['architectureSha256']))
def preservation():
 for name,digest in RECORD['runtimeBefore'].items():
  check(sha(project(name,audit_read(name)).encode())==digest,name)
  if name!='src/20-application.js':check(sha(audit_read(name).encode())==digest,name)
case('CL-S02 every crypto, vendor, startup, transport, result and journal byte unchanged; only declared app navigation differs',preservation)
def reversals():
 for name,digest in RECORD['baselineHashes'].items():
  check(sha(project(name,audit_read(name)).encode())==digest,name)
  check(sha(audit_read(name).encode())==RECORD['currentHashes'][name],name)
case('CL-S03 complete template/style/app reversals restore exact verified baseline hashes',reversals)
def mutation():
 for name in ['src/page.html','src/style.css','src/20-application.js']:
  t=audit_read(name);changed=t+'\n/* unauthorized */'
  try:result=project(name,changed)
  except AssertionError:continue
  check(sha(result.encode())!=RECORD['baselineHashes'][name],name)
case('CL-S04 unauthorized edits cannot be hidden by historical preservation projection',mutation)
case('CL-S05 one native font token applied to all visible text with no webfont request',lambda:(check('--app-font:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif' in css),check('body,body *,body *::before,body *::after{font-family:var(--app-font)!important}' in css),check('@font-face' not in css),check("font-src 'none'" in html)))
case('CL-S06 technical strings retain tabular numerals and disabled ligatures',lambda:check('font-variant-ligatures:none;font-variant-numeric:tabular-nums' in css))
case('CL-S07 workspace shell no longer conditionally removes progress or identity row',lambda:(check('class="stepper" x-show=' not in page),check('class="session-tracker" x-show="acknowledged"' in page),check('guidedLocked || workspaceView' in page),check('scrollbar-gutter:stable' in css)))
def no_scroll():
 t=app.split('async openWorkspace(view) {')[1].split('async showAdvancedSettings()')[0]
 check('preventScroll:true' in t);check('scrollIntoView' not in t);check('this.focusSection(' not in t);check('request !== this.workspaceRequest' in t)
case('CL-S08 workspace focus remains cancellable without automatic scrolling',no_scroll)
case('CL-S09 compact safety statement remains before exposed words',lambda:(check(page.index('id="wallet-safety"')<page.index('<ol class="seed-grid">')),check('Never enter a real seed or send bitcoin to this wallet.' in page),check('YOUR DISPOSABLE WALLET' not in page),check('See a known attack.' not in page)))
case('CL-S10 same-length reset is visible in Wallet and uses guarded confirmation, not duplicate Advanced logic',lambda:(check(page.count('id="new-test-wallet"')==1),check(page.index('id="new-test-wallet"')<page.index('id="advanced-view"')),check('id="wallet-options"' not in page),check('@click="requestWalletChange()"' in page),check('Nothing is saved automatically.' in page)))
case('CL-S11 concise loading instruction includes no-passphrase rule',lambda:(check(page.count('class="seed-instructions"')==1),check('Scan the QR or enter these words on your signer. Do not add a passphrase.' in page),check('Check that the fingerprint matches your signer' in page)))
case('CL-S12 one canonical example dialog and one demonstration result surface',lambda:(check(page.count('id="attack-example"')==1),check(page.count('class="demo-result"')==1),check(page.count('@click="openExample()"')==2),check('not a device test' in page),check('not added to your results' in page)))
def optional_boundary():
 t=app.split('openExample() {')[1].split('runDemonstration() {')[0]
 for forbidden in ['randomizeAll(', 'beginPreparedTest(', 'acceptArtifact(', 'journal.', 'new Tbw', 'getUserMedia(', 'verify(', 'setTimeout(', 'fetch(']:check(forbidden not in t,forbidden)
 check('this.runDemonstration()' in t);check('this.scan.active' in t);check('dialog.showModal' in t)
case('CL-S13 optional example calls existing verifier path without mutating or creating test state',optional_boundary)
case('CL-S14 failed/incomplete/review findings and full evidence actions remain present',lambda:(check('Signatures matched. File changes need review.' in page),check('Could not complete the check' in page),check('output.address' in page),check('@click="downloadResult()"' in page),check('does not rule out seed leakage' in page)))
r={'suite':'Clarity static and approved-change contracts','complete':True,'sha256':sha(FILE.read_bytes()),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
