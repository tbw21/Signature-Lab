#!/usr/bin/env python3
"""Direct current-source/HTML checks. Does not execute historical projections."""
from pathlib import Path
from rc29_static_contract import release_identity,archive_original_tests,pin_input,shared_wallet,wallet_safety
from audit_projection import read as audit_read
from rc35_style_pin import pinned_historical_css
from bs4 import BeautifulSoup
import hashlib,json,re,sys
from delivery_projection import project as delivery_project
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);rows=[]
R=json.loads((ROOT/'fixtures/wallet-card-changes.json').read_text())
H=FILE.read_text();soup=BeautifulSoup(H,'html.parser');sha=lambda b:hashlib.sha256(b).hexdigest()
def check(ok,why='assertion failed'):
 if not ok:raise AssertionError(why)
def test(name,fn):
 try:fn();rows.append({'name':name,'status':'passed'})
 except Exception as e:rows.append({'name':name,'status':'failed','error':repr(e)})
def unique(selector):
 es=soup.select(selector);check(len(es)==1,selector);return es[0]
test('WC-S01 architecture has not changed after scope freeze',lambda:check(sha((ROOT/'docs/WALLET-CARD-ARCHITECTURE-FROZEN.md').read_bytes())==R['architectureSha256']))
def runtime():
 for name,digest in R['runtime'].items():check(sha((delivery_project(name,(ROOT/name).read_text()) if name=='src/20-application.js' else audit_read(name)).encode())==digest,name)
 check(len(R['runtime'])==len(json.loads((ROOT/'sources.json').read_text())))
test('WC-S02 runtime units preserve dev-4 after exact declared navigation reversal',runtime)
def exactchanges():
 for name,digest in R['before'].items():
  text=pinned_historical_css() if name=='src/style.css' else audit_read(name);check(sha(text.encode())==R['after'][name],name)
  for edit in reversed(R['edits'][name]):
   check(text.count(edit['after'])==1,name);text=text.replace(edit['after'],edit['before'],1)
  check(sha(text.encode())==digest,name)
test('WC-S03 entire page/style changes reverse to exact supplied baseline',exactchanges)
def card():
 shared_wallet(soup)
 c=unique('#wallet-load-card');check(c.name=='section');check(c.get('aria-labelledby')=='wallet-fingerprint-label')
 for selector in ['#wallet-fingerprint-value','#wallet-fingerprint-label','#wallet-compare-hint']:
  check(c in unique(selector).parents,selector)
 check(unique('#wallet-loaded').find_parent(class_='premium-wallet-continue') is not None)
 check(unique('.seed-qr-actions>button').find_parent(class_='seed-scan') is not None)
 check(not c.has_attr('x-data'))
test('WC-S04 all four related pieces live once in one card inside the wallet panel',card)
def binding():
 check(unique('#wallet-fingerprint-value').get('x-text')=="walletFingerprint || 'Unavailable'")
 b=unique('#wallet-loaded');check(b.get('@click')=='confirmWalletLoaded()');check(b.get('x-show')=='!isTestComplete')
 check('wallet-compare-hint' in b.get('aria-describedby','').split())
 e=unique('.seed-qr-actions>button');check(e.get('@click')=='seedQrExpanded = !seedQrExpanded')
 check(e.get(':aria-expanded')=='seedQrExpanded');check(e.get('aria-controls')=='seed-qr-display')
 check(e not in unique('#seed-qr-display').descendants)
test('WC-S05 fingerprint, enlargement and acknowledgement retain their distinct bindings',binding)
test('WC-S06 one original seed canvas and word list with no duplicated wallet surface',lambda:(unique('[x-ref="seedQrCanvas"]'),unique('.seed-grid'),unique('.premium-passphrase'),check(not soup.select('.panel-actions.acknowledgement'))))
def safety():
 wallet_safety(soup)
 check('wallet-safety' in unique('#wallet-loaded').get('aria-describedby','').split())
test('WC-S07 disposal, no-passphrase and fingerprint-comparison guidance remain',safety)
def actions():
 for b in soup.select('#wallet-load-card button'):check(b.get('type')=='button');check(not b.find_parent('button'))
 check(unique('#wallet-loaded').get('class')==['button','primary']);check('secondary' in unique('.seed-qr-actions>button').get('class'))
 check('x-data' not in unique('#wallet-load-card').attrs)
test('WC-S08 no combined operation, extra state owner or implicit form submission',actions)
def present():
 css=audit_read('src/style.css')
 for x in ['.wallet-confirmation-actions{display:flex','justify-content:flex-end','min-height:44px','@media(forced-colors:active)'] :check(x in css,x)
 check(not re.search(r'\.wallet-confirmation[^{}]*\{[^}]*overflow\s*:\s*(hidden|clip)',css))
 check('body,body *,body *::before,body *::after{font-family:var(--app-font)!important}' in css)
test('WC-S09 shared typography and responsive layout use no cropping or font downloads',present)
test('WC-S10 signature/file review, incomplete states, outputs and evidence remain available',lambda:check(all(x in H for x in ['Signatures matched. File changes need review.','Could not complete the check','output.address','@click="downloadResult()"','id="result-tools"','id="help-contents-title"'])))
r={'suite':'Wallet confirmation current-source checks','complete':True,'sha256':sha(FILE.read_bytes()),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};OUT.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
