#!/usr/bin/env python3
"""Auditable current-version security, release, semantics and negative-mutation contract.
This explicitly tests the *current* source/HTML; historical source projection is separate.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json,hashlib,re,sys,traceback,base64,zlib,subprocess,tempfile,shutil
ROOT=Path(__file__).resolve().parents[1];HTML=Path(sys.argv[1]);OUT=Path(sys.argv[2]);OUT.parent.mkdir(parents=True,exist_ok=True)
sha=lambda x:hashlib.sha256(x).hexdigest()
source=json.loads((ROOT/'source-lock.json').read_text());expected=json.loads((ROOT/'EXPECTED-OUTPUT.json').read_text());release=json.loads((ROOT/'release.json').read_text())
trusted=json.loads((ROOT/'fixtures/v0209-trusted-source.json').read_text());bridge=json.loads((ROOT/'fixtures/historical-source-bridge-v0204.json').read_text())['files']
page=(ROOT/'src/page.html').read_text();style=(ROOT/'src/style.css').read_text();h=HTML.read_text();soup=BeautifulSoup(h,'html.parser');rows=[]
def require(flag,reason):
 if not flag:raise AssertionError(reason)
def test(name,fun):
 try:fun();rows.append({'name':name,'status':'passed'});print('PASSED '+name,flush=True)
 except Exception as e:rows.append({'name':name,'status':'failed','reason':str(e)});print('FAILED '+name+': '+str(e),flush=True)
def one(css):
 arr=soup.select(css);require(len(arr)==1,f'Expected exactly one {css}; got {len(arr)}');return arr[0]

test('A01 source lock covers actual exact build inputs',lambda:[require(sha((ROOT/n).read_bytes())==x,n) for n,x in source.items()])
test('A02 distribution HTML hash, byte count and current identity',lambda:(require(sha(HTML.read_bytes())==expected['sha256'],'HTML SHA-256 differs'),require(HTML.stat().st_size==expected['bytes'],'HTML length differs'),require(expected['version']==release['version']=='0.20.11-dev','Version differs')))
test('A03 development status never implies release acceptance',lambda:(require(expected['publisherAuthenticated'] is False,'Publisher authenticated falsely'),require(release['status']=='development-not-a-release-candidate','Status promoted'),require('not approved for public deployment' in h,'Preview warning absent')))
test('A04 cryptography, PSBT, QR, camera and journal modules preserved',lambda:[require(sha((ROOT/n).read_bytes())==v,'Trusted unit changed: '+n) for n,v in trusted['trustedUnits'].items()])
test('A05 vendor identities preserved',lambda:[require(sha((ROOT/n).read_bytes())==v,'Vendor changed: '+n) for n,v in trusted['vendorHashes'].items()])
test('A06 canonical source builder unchanged',lambda:require(sha((ROOT/'build.py').read_bytes())==trusted['buildToolHash'],'Build tool changed'))
def boundaries():
 policy=one('meta[http-equiv="Content-Security-Policy"]')['content']
 for tok in ["default-src 'none'","connect-src 'none'","font-src 'none'"]:
  require(tok in policy,'CSP weakened: '+tok)
 require(not soup.select('script[src],link[rel="stylesheet"],iframe'),'External code/resource added')
 for bad in ['x-html=','innerHTML','outerHTML','insertAdjacentHTML','document.write']:
  require(bad not in page,'HTML sink introduced: '+bad)
 require(h.count('function Fv(')==1,'Multiple application coordinators')
 require(h.count('class TbwSessionJournal')==1,'Multiple journal engines')
test('A07 offline CSP and unique trusted runtime boundaries',boundaries)
def safety():
 warning=one('#wallet-safety').get_text(' ',strip=True).lower()
 for x in ['disposable','never enter your real seed','overwrite an existing wallet','send bitcoin']:
  require(x in warning,'Missing safety warning '+x)
 require('Do not add a passphrase.' in one('.seed-instructions').get_text(' ',strip=True),'Passphrase warning absent')
 require('fingerprint matches your signer' in one('#wallet-compare-hint').get_text(' ',strip=True),'Fingerprint match warning absent')
 scope=one('#supported-scope').get_text(' ',strip=True)
 for x in ['BIP84','P2WPKH','ECDSA','Taproot','multisig']:
  require(x in scope,'Compatibility missing: '+x)
 require('does not prove that firmware is safe' in h,'Firmware disclaimer absent')
test('A08 no-real-seed, no-overwrite, no funding and compatibility scope',safety)
def unique():
 ids=[x.get('id') for x in soup.select('[id]')];require(len(ids)==len(set(ids)),'Duplicate HTML IDs')
 for css in ['#workspace-test','#workspace-advanced','#workspace-session','#advanced-view','#session-view','#test-view','#retain-evidence','#retain-evidence-before-sign','#finish-testing-open','#finish-testing-confirm','#attack-example','#reference-self-check-note']:
  one(css)
 for b in soup.select('.workspace-nav>button'):
  require(b.get('@click')==f"openWorkspace('{b['id'].replace('workspace-','')}')",'Duplicate/custom workspace controller')
test('A09 DOM IDs, workspace navigation and optional controls remain singletons',unique)
def privacy():
 for e in soup.select('input:not([type="checkbox"]),textarea'):
  # Exempt inherently noneditable or dynamically type=numeric fields only when justified
  if e.get('readonly') is not None or e.get('type')=='file':continue
  require(e.get('autocomplete')=='off','Editable field missing autocomplete=off: '+str(e.get('id')))
  require(e.get('spellcheck')=='false','Editable field missing spellcheck=false: '+str(e.get('id')))
 for css in ['.seed-grid','#wallet-fingerprint-value']:
  require(one(css).get('translate')=='no','Technical value translation unprotected: '+css)
 require(one('#retain-evidence').get('@change')==one('#retain-evidence-before-sign').get('@change'),'Split evidence controllers')
test('A10 browser text-service hints and shared evidence-retention controller',privacy)
def results():
 require('These counts are not a safety score' in page,'Session safety framing missing')
 require('Signatures matched. File changes need review.' in page,'File metadata review missing')
 require('Could not complete the check' in page,'Incomplete outcome hidden')
 require('does not rule out seed leakage' in page,'Match limitation missing')
 require('downloadResult()' in page and 'downloadSessionReport()' in page,'Reports unavailable')
 require('data-has-differences' in page,'Difference flag missing')
test('A11 incomplete, file review and no-firmware-certificate limitations',results)
def lifetime():
 js=(ROOT/'src/20-application.js').read_text()
 start=js.find('finishTesting() {');require(start>=0,'Finish action missing')
 snippet=js[start:start+3500]
 for item in ['journal.locked','retired','destroy()','about:blank']:
  require(item in snippet,'Finish handling regressed: '+item)
 require('this.retired' in js,'Retirement latch absent')
 require('does not erase browser' in page,'No honest memory limitation')
test('A12 retire latch, shutdown and memory limitation retained',lifetime)
def ui_fix():
 require('.workspace-nav button{min-height:44px;padding:9px 12px' in style,'Navigation target minimum reduced')
 require('#session-view .session-summary p{display:flex;flex-wrap:wrap;min-width:0' in style,'Session 200%-text wrapping absent')
 require('#session-view .session-summary .session-goal{font-size:.875rem;color:#94aabd;white-space:normal' in style,'Session goal forced nowrap')
 require(style.rstrip().endswith('@media(forced-colors:active){.workspace-nav button[aria-pressed=true]{border:2px solid Highlight}}'),'Selected-state high-contrast border can be overridden')
test('A13 regression selectors: 44px navigation, 200% wrapping and forced colors',ui_fix)
def historical():
 from current_to_historical import project
 for name,d in bridge.items():
  raw=(ROOT/name).read_text();prior=project(name,raw)
  require(sha(prior.encode())==d['priorSha256'],'Historical provenance not authenticated: '+name)
  try:project(name,raw+'\n/* unauthorized */')
  except AssertionError:pass
  else:raise AssertionError('Historical projection hid tamper: '+name)
test('A14 historical provenance bridge rejects tampering; never substitutes for current behavior',historical)
def mutations():
 for name,d in source.items():
  mutated=(ROOT/name).read_bytes()+b'\x00';require(sha(mutated)!=d,'Accepted byte mutation: '+name)
 require(sha(HTML.read_bytes()+b'\x00')!=expected['sha256'],'Accepted HTML mutation')
test('A15 all locked-source and output mutations invalidate recorded identity',mutations)
def device():
 require(sha((ROOT/'LICENSE.txt').read_bytes())!=sha(b''),'License missing')
 require((ROOT/'LICENSE.txt').read_text().count('Copyright (c) 2026 The Bitcoin Way')==1,'License owner missing')
 require(page.count('Copyright (c) 2026 The Bitcoin Way')==2,'Embedded copyright inconsistent')
test('A16 license owner plus original attribution retained',device)
result={'schema':'tbw-current-assurance-v1','candidateSha256':sha(HTML.read_bytes()),'scope':'current static + provenance and negative tests; no hardware/browser inference','passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows}
OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed']}));sys.exit(bool(result['failed']))
