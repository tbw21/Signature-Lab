#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,sys,re,subprocess,ast
from bs4 import BeautifulSoup
from readability_projection import RECORD,project
R=Path(__file__).resolve().parents[1];H=Path(sys.argv[1]);O=Path(sys.argv[2]);rows=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
S=BeautifulSoup(H.read_text(),'html.parser');page=(R/'src/page.html').read_text();css=(R/'src/style.css').read_text()
def req(x,m='requirement'): 
 if not x:raise AssertionError(m)
def case(n,f):
 try:f();rows.append({'name':n,'status':'passed'})
 except Exception as e:rows.append({'name':n,'status':'failed','error':repr(e)})
case('R01 frozen readability scope identity',lambda:req(sha((R/'docs/READABILITY-DELIVERY-ARCHITECTURE.md').read_bytes())==RECORD['architectureSha256']))
case('R02 all 29 runtime module identities are authorized current inputs',lambda:[req(sha((R/n).read_bytes())==json.loads((R/'source-lock.json').read_text())[n],n) for n in json.loads((R/'sources.json').read_text())])
case('R03 exact current template and stylesheet identities',lambda:[req(sha((R/n).read_bytes())==json.loads((R/'source-lock.json').read_text())[n],n) for n in ['src/page.html','src/style.css']])
case('R04 exact authorized presentation reverses to baseline',lambda:[req(sha(project(n,(R/n).read_text()).encode())==RECORD['baselineHashes'][n],n) for n in RECORD['edits']])
def no_hidden_mutation():
 for n in RECORD['edits']:
  try:project(n,(R/n).read_text()+'\n// unexpected')
  except AssertionError:continue
  raise AssertionError('Historical projection accepted modified current bytes: '+n)
case('R05 projection cannot hide undeclared appended text',no_hidden_mutation)
case('R06 logo reads Signature Lab without orange punctuation',lambda:(req(S.select_one('.brand-name').get_text()=='Signature Lab'),req(S.select_one('.brand-name .accent') is None)))
def wheel_identity():
 # Keep historical witness unchanged while pinning the approved current brand
 # asset to the independently recovered frozen RC27 source identity.
 historical=BeautifulSoup(RECORD['edits']['src/page.html']['before'],'html.parser').select_one('.brand-mark')['src']
 req(sha(historical.encode())=='b51dac0131167a7f2d4ce887ba1a60312334cf8e6918f27e183c95f90c381320','Historical branding witness changed')
 req(sha(S.select_one('.brand-mark')['src'].encode())=='63f6b5aed77f2997a102158c7773b4c9bb39565c2f568d4b62cdf66f4e657352','Current approved brand logo changed')
case('R07 historical brand image and frozen RC27 current brand pin retained',wheel_identity)
case('R08 Helvetica-first local family without distributed font files',lambda:(req(re.search(r'--app-font\s*:\s*Helvetica',css)),req('@font-face' not in css),req(not any(p.suffix.lower() in ['.ttf','.woff','.woff2','.otf'] for p in R.rglob('*')))))
case('R09 all application text uses one family',lambda:req('body,body *,body *::before,body *::after{font-family:var(--app-font)!important}' in css))
case('R10 QR canvas and control bindings unchanged',lambda:[req(len(S.select(sel))==1,sel) for sel in ['[x-ref="seedQrCanvas"]','#wallet-fingerprint-value','#wallet-loaded','#test-purpose']])
case('R11 browser privileges and external-resource boundaries unchanged',lambda:(req(S.select_one('[http-equiv="Content-Security-Policy"]')['content']==BeautifulSoup(RECORD['edits']['src/page.html']['before'],'html.parser').select_one('[http-equiv="Content-Security-Policy"]')['content']),req(not S.select('script[src],link[rel="stylesheet"]'))))
case('R12 single normal-flow footer with original attribution and licence route',lambda:(req(len(S.select('footer'))==1),req(S.select_one('footer a[href="#license-help"]') is not None),req('oren-z0 / exfil-tester' in S.select_one('footer').get_text())))
case('R13 body and main controls have explicit larger default sizes',lambda:(req('body{font-size:1.125rem' in css),req('.button,.button.small{font-size:1rem' in css)))
def current_bindings():
 # The immutable current page is source-locked; compare its exact event/binding projection with the built HTML.
 original=BeautifulSoup((R/'src/page.html').read_text(),'html.parser')
 def pairs(doc):return sorted((e.name,a,str(v)) for e in doc.find_all() for a,v in e.attrs.items() if a.startswith(('@','x-')))
 req(pairs(S)==pairs(original),'Event bindings differ between source and distribution')
 req(S.select_one('#wallet-loaded').get('@click')=='confirmWalletLoaded()','Wallet confirmation callback changed')
 req(S.select_one('#try-example').get('@click')=='openExample()','Example callback changed')
 req(S.select_one('#retain-evidence-before-sign').get('@change')==S.select_one('#retain-evidence').get('@change'),'Evidence state owner changed')
case('R14 current event bindings match source exactly without a second state owner',current_bindings)
def current_release_caveat():
 release=json.loads((R/'release.json').read_text())
 expected=json.loads((R/'EXPECTED-OUTPUT.json').read_text())
 req(release['version']==expected['version']=='0.20.12-rc36', 'Current release identity changed')
 req(expected['sha256']=='c2c4ae702b966d25a2ecb020dc70190e5f56eb0290fc6295cf55def0bf72612b', 'Unexpected output digest')
 req(sha((R/'rc35.html').read_bytes())=='5c2c6e0293171f6f69147bb67557ec5d59d4783ac8cc7b07b3957ab59f510886', 'Original RC35 witness changed')
 req(expected['status']==release['status']=='development-ui-preview-unqualified', 'Claim of qualified release')
 req(release['publisherAuthenticated'] is False and expected['publisherAuthenticated'] is False,'False publisher authentication')
 req('Physical signing-device and optical-scanning acceptance remain pending' in page, 'Hardware qualification caveat missing')
case('R15 current exact release plus explicit no hardware/publisher claim',current_release_caveat)
case('R16 handoff distinguishes development from historical hardware checklists',lambda:(req('RC28' in (R/'RC28-ARCHITECTURE-FROZEN.md').read_text()),req('development-ui-preview-unqualified' in (R/'release.json').read_text()),req('checklist, not a record' in (R/'docs/READABILITY-HARDWARE-ACCEPTANCE.md').read_text()),req('not an approved public release' in H.read_text())))
r={'suite':'Readability static and preservation','complete':True,'sha256':sha(H.read_bytes()),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};O.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
