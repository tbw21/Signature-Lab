#!/usr/bin/env python3
"""Exact current-template/state boundary checks for the header/QR polish."""
from pathlib import Path
from rc29_static_contract import release_identity,archive_original_tests,pin_input,shared_wallet,wallet_safety
from audit_projection import read as audit_read
from rc35_style_pin import pinned_historical_css
from bs4 import BeautifulSoup
import json,hashlib,re,sys
from delivery_projection import project as delivery_project
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);rows=[]
R=json.loads((ROOT/'fixtures/polish-changes.json').read_text());H=FILE.read_text();S=BeautifulSoup(H,'html.parser')
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m='assertion failed'):
 if not v:raise AssertionError(m)
def case(name,fn):
 try:fn();rows.append({'name':name,'status':'passed'})
 except Exception as e:rows.append({'name':name,'status':'failed','error':repr(e)})
def one(s):
 es=S.select(s);require(len(es)==1,s);return es[0]
case('P-S01 architecture remains exactly frozen',lambda:require(sha((ROOT/'docs/POLISH-ARCHITECTURE-FROZEN.md').read_bytes())==R['architectureSha256']))
def preservation():
 for name,digest in R['runtime'].items():require(sha((delivery_project(name,(ROOT/name).read_text()) if name=='src/20-application.js' else audit_read(name)).encode())==digest,name)
 require(len(R['runtime'])==len(json.loads((ROOT/'sources.json').read_text()))==29)
case('P-S02 28 runtime units identical; declared navigation changes reverse exactly to v0.18.1',preservation)
def reverse():
 for name,digest in R['before'].items():
  text=pinned_historical_css() if name=='src/style.css' else audit_read(name);require(sha(text.encode())==R['after'][name],name)
  for e in reversed(R['edits'][name]):require(e['after'] and text.count(e['after'])==1,name);text=text.replace(e['after'],e['before'],1)
  require(sha(text.encode())==digest,name)
case('P-S03 complete page and stylesheet reverse exactly to baseline bytes',reverse)
def mutation():
 for name,digest in R['before'].items():
  text=(pinned_historical_css() if name=='src/style.css' else audit_read(name))+'\n/* unrelated mutation */'
  for e in reversed(R['edits'][name]):text=text.replace(e['after'],e['before'],1)
  require(sha(text.encode())!=digest,name)
case('P-S04 preservation check does not hide an unrelated appended change',mutation)
def help_control():
 e=one('.help-control');require(e.get('aria-label')=='Help');require(e.get('title')=='Help');require(e.get('href')=='#help')
 require(e.has_attr('data-help-home') and e.has_attr('data-help-link'))
 require(e.find_parent(class_='header-actions') is not None)
 require(e.find_parent(class_='workspace-nav') is None)
 require(e.get_text().strip()=='Help');require(not e.select('script'))
case('P-S05 one named Help control uses existing header navigation route',help_control)
def active_navigation():
 require(not S.select('nav.workspace-nav,#workspace-test,#workspace-advanced,#workspace-session,.workspace-alert'),'Retired hidden tabs returned')
 drawer=one('#tbw-settings');require(drawer.name=='details' and drawer.find('summary') is not None)
 routes=one('#tbw-settings .tbw-drawer-workspace')
 for target in ['advanced','session']:
  require(len([b for b in routes.select('button') if "openWorkspace('"+target+"')" in b.get('@click','')])==1,'Visible route missing: '+target)
 require(len(S.select('#advanced-view .aux-heading button'))>=1 and len(S.select('#session-view .aux-heading button'))>=1)
case('P-S06 retired tabs absent; visible Settings routes preserve single workspace',active_navigation)
def release():
 release_identity()
 require('v'+json.loads((ROOT/'release.json').read_text())['version'] in str(one('.tbw-drawer-about')))
 require('Session data is not uploaded or saved automatically.' in str(one('.tbw-drawer-about')))
 require('not an approved public release' in one('#release-status-help').get_text())
 require('Publisher authentication' in one('#release-status-help').get_text())
 require(one('.tbw-settings').find_parent(class_='header-actions') is not None)
case('P-S07 unique version and release caveat stay accessible in header',release)
def structure():
 shared_wallet(S)
 card=one('#wallet-load-card');qr=one('#seed-qr-display')
 require(card != qr and card.find_parent(class_='premium-wallet-panel') == qr.find_parent(class_='premium-wallet-panel'))
 require(not qr.find('button') and not qr.find(id='wallet-fingerprint-value'))
 require(not card.has_attr('x-data'))
case('P-S08 QR fingerprint and actions share one group without controls in the quiet zone',structure)
def callbacks():
 require(one('#wallet-loaded').get('@click')=='confirmWalletLoaded()')
 e=one('.seed-qr-actions>button');require(e.get('@click')=='seedQrExpanded = !seedQrExpanded')
 require(e.get('aria-controls')=='seed-qr-display');require(e.get(':aria-expanded')=='seedQrExpanded')
 require(one('#wallet-fingerprint-value').get('x-text')=="walletFingerprint || 'Unavailable'")
 one('[x-ref="seedQrCanvas"]');one('.seed-grid')
case('P-S09 original distinct callbacks and canvas/identity bindings preserved',callbacks)
def safety():
 wallet_safety(S)
 require('Signatures matched. File changes need review.' in H)
 require('Could not complete the check' in H);require('does not rule out seed leakage' in H)
 require('@click="downloadResult()"' in H and 'output.address' in H)
case('P-S10 safety scope warning results and evidence stay present',safety)
def no_new_paths():
 require(len(S.select('#attack-example'))==1);require(H.count('@click="openExample()"')==2)
 require('not a device test' in H)
 require("connect-src 'none'" in S.select_one('meta[http-equiv="Content-Security-Policy"]')['content'])
 require('@font-face' not in audit_read('src/style.css'))
case('P-S11 no demo wallet replacement or new network/font dependency',no_new_paths)
def action_policy():
 c=audit_read('src/style.css');require('.header-actions .help-control{display:grid' in c)
 require('min-height:44px' in c);require('@media(forced-colors:active)' in c)
 require('body,body *,body *::before,body *::after{font-family:var(--app-font)!important}' in c)
 for b in S.select('#wallet-load-card button'):require(b.get('type')=='button')
 require(not re.search(r'\.(?:wallet-confirmation|help-control)[^{}]*\{[^}]*overflow\s*:\s*(hidden|clip)',c))
case('P-S12 native typography reflow and explicit actions remain no-clipping',action_policy)
r={'suite':'Header and QR polish static checks','complete':True,'sha256':sha(FILE.read_bytes()),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};OUT.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
