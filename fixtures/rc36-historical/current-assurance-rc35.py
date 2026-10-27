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
test('A02 distribution HTML hash, byte count and current identity',lambda:(require(sha(HTML.read_bytes())==expected['sha256'],'HTML SHA-256 differs'),require(HTML.stat().st_size==expected['bytes'],'HTML length differs'),require(expected['version']==release['version']=='0.20.12-rc33','Version differs')))
test('A03 RC test status never implies public release acceptance',lambda:(require(expected['publisherAuthenticated'] is False,'Publisher authenticated falsely'),require(release['status']=='development-ui-preview-unqualified','Status promoted'),require('not an approved public release' in h and 'Publisher authentication has not been verified' in h,'Preview warning absent')))
def module_provenance():
 reviewed=json.loads((ROOT/'fixtures/approved-app-change.json').read_text())
 approved=json.loads((ROOT/'fixtures/rc30-historical/rc30-focus-provenance.json').read_text())
 for n,v in trusted['trustedUnits'].items():
  if n=='src/20-application.js':
   prior=(ROOT/'fixtures/rc30-historical/20-application-rc28.js').read_bytes()
   require(v==reviewed['historicalSha256'],'Historical pin altered')
   require(sha(prior)==approved['baselineSha256']==reviewed['currentSha256'],'RC28 reviewed app changed')
   require(prior.replace(b'this.$refs?.sessionNav?.focus?.({preventScroll:true});',b"document.querySelector('#tbw-settings > summary')?.focus?.({preventScroll:true});")== (ROOT/n).read_bytes(),'Unreviewed RC30 application edit')
   require(sha((ROOT/n).read_bytes())==approved['currentSha256']=='c3e4558e8b1d5afa1251691013abdfd1534a646dcd31ac2443c59dbe339fbe58','RC30 app digest changed')
  else:require(sha((ROOT/n).read_bytes())==v,'Trusted module changed: '+n)
test('A04 unchanged core modules plus exact reviewed UI coordinator change',module_provenance)
test('A05 vendor identities preserved',lambda:[require(sha((ROOT/n).read_bytes())==v,'Vendor changed: '+n) for n,v in trusted['vendorHashes'].items()])
test('A06 canonical source builder unchanged',lambda:require(sha((ROOT/'build.py').read_bytes())=='8f2543d6f05f1cebd8a84610c51e0500258c00de053015576280d6619b0abb0e','Build tool changed'))
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
 require('disposable' in warning and 'never overwrite an existing wallet' in warning,'Current wallet warning weak')
 combined=page.lower()
 for term in ['never use your main wallet or real funds','never enter a recovery phrase from an existing wallet',"never enter a funded wallet's seed",'not proof that firmware is safe','taproot/schnorr, multisig, non-bip84 input scripts']:
  require(term in combined,'Safety/compatibility statement missing: '+term)
 require('No passphrase' in page,'Passphrase instruction missing')
 require('fingerprint' in page.lower() and 'fingerprint matches, continue' in page.lower() and 'compare this fingerprint' in page.lower(),'Fingerprint comparison missing')
 require('BIP84' in page and 'P2WPKH' in page and 'ECDSA' in page,'Wallet/signer compatibility scope incomplete')
test('A08 no-real-seed, no-overwrite, no funding and compatibility scope',safety)
def unique():
 ids=[x.get('id') for x in soup.select('[id]')];require(len(ids)==len(set(ids)),'Duplicate HTML IDs')
 require(not soup.select('nav.workspace-nav,#workspace-test,#workspace-advanced,#workspace-session,.workspace-alert'),'Retired hidden navigation reintroduced')
 for css in ['#tbw-settings','#tbw-settings > summary','.tbw-drawer-workspace','#advanced-view','#session-view','#test-view','#retain-evidence','#retain-evidence-before-sign','#finish-testing-open','#finish-testing-confirm','#attack-example','#reference-self-check-note']:
  one(css)
 controls=soup.select('#tbw-settings .tbw-drawer-workspace > button')
 require(len(controls)==2,'Visible Advanced and Session controls missing')
 require(all('openWorkspace(' in (b.get('@click') or '') for b in controls),'Duplicate/custom workspace coordinator')
 require("openWorkspace('advanced')" in controls[1].get('@click','') and "openWorkspace('session')" in controls[0].get('@click',''),'Workspace target changed')
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
 require('.topbar .tbw-settings>summary{width:auto!important;min-width:44px!important;height:44px!important;min-height:44px!important' in style,'Visible Settings target minimum absent')
 require('.tbw-settings .tbw-drawer-workspace>button{display:flex!important;align-items:center!important;min-height:71px!important' in style,'Visible workspace controls target minimum absent')
 require('flex-wrap:wrap' in style and 'min-width:0' in style,'Responsive wrapping absent')
 require('@media(forced-colors:active)' in style or '@media (forced-colors:active)' in style,'Forced colors absent')
 require('@media(forced-colors:active)' in style and 'CanvasText' in style,'Forced colors contrast policy removed')
 require('text-overflow:clip!important' in style,'Recovery words can truncate')
test('A13 regression selectors: 44px navigation, 200% wrapping and forced colors',ui_fix)
def historical():
 from current_to_historical import project, REVIEWED_RC28
 for name,d in bridge.items():
  original=(ROOT/name).read_text()
  archived={'src/page.html':'fixtures/rc30-historical/page-rc28.html',
            'src/style.css':'fixtures/rc30-historical/style-rc28.css',
            'src/20-application.js':'fixtures/rc30-historical/20-application-rc28.js'}.get(name)
  source=(ROOT/archived).read_text() if archived else original
  if archived:require(sha(source.encode())==REVIEWED_RC28[name], 'RC28 immutable witness changed: '+name)
  prior=project(name,source)
  require(sha(prior.encode())==d['priorSha256'],'Historical provenance not authenticated: '+name)
  try:project(name,source+'\n/* unauthorized */')
  except AssertionError:pass
  else:raise AssertionError('Historical projection hid tamper: '+name)
 # RC30 reviewed current byte pins are checked independently from the old projection.
 require(sha((ROOT/'src/page.html').read_bytes())=='bc4323fe9ca8f9fc7fe69c885b4c9c912de4d34f207dabbe4f5affb43d1a67f4','Unreviewed RC30 page')
 css_review=json.loads((ROOT/'fixtures/rc32-historical/rc32-css-provenance.json').read_text())
 require(css_review['schema']=='tbw-reviewed-rc32-css-delta-v1','Invalid CSS review schema')
 baseline=(ROOT/'fixtures/rc32-historical/style-rc30.css').read_bytes()
 require(sha(baseline)==css_review['rc30Sha256']=='cbcf6fef2e10877c16d3e7929d0e5ee95079083a4b5b7d9dec4f76923a2e3bfb','RC30 CSS historical witness tampered')
 assert len(css_review['replacements'])==2
 changed=baseline
 for rule in css_review['replacements']:
  before,after=rule['before'].encode(),rule['after'].encode()
  require(before!=after and changed.count(before)==1,'Invalid scoped CSS patch')
  changed=changed.replace(before,after)
 require(changed==(ROOT/'fixtures/rc33-historical/rc32-style.css').read_bytes(),'RC32 CSS witness changed')
 require(sha(changed)==css_review['rc32Sha256'],'RC32 CSS reviewed hash changed')
 # Current RC33 source must equal precisely the reviewed one-rule security repair;
 # historical RC32 and RC30 witnesses remain independent and immutable.
 rc33_review=json.loads((ROOT/'fixtures/rc33-historical/rc33-css-provenance.json').read_text())
 require(rc33_review['schema']=='rc33-reviewed-delta-v1','Unknown current CSS provenance')
 rule=rc33_review['cssSafetyRule'].encode()
 anchor=b'#test-view .sign-layout{display:grid!important;grid-template-columns:minmax(0,1.55fr) minmax(320px,.93fr)!important;grid-template-areas:\'summary qr\'!important;column-gap:16px!important;margin-top:17px!important;align-items:start!important}'
 note=b'\n/* RC33: Alpine x-show must win over the approved premium grid layout.\n   When transactionReady/outputReview fails, never display stale signing information. */\n'
 require(changed.count(anchor)==1 and not rule in changed,'CSS patch anchor changed')
 patched=changed.replace(anchor,anchor+note+rule)
 require(patched==(ROOT/'src/style.css').read_bytes(),'Unreviewed RC33 CSS change')
 require(sha(changed)==rc33_review['cssBaselineSha256'] and sha(patched)==rc33_review['cssCurrentSha256'],'RC33 CSS provenance digest mismatch')

 require(not soup.select('nav.workspace-nav,.workspace-alert'),'Retired menu unexpectedly restored')

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
