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
case('R02 all 29 runtime module bytes unchanged',lambda:[req(sha((R/n).read_bytes())==RECORD['baselineHashes'][n],n) for n in json.loads((R/'sources.json').read_text())])
case('R03 exact current template and stylesheet identities',lambda:[req(sha((R/n).read_bytes())==RECORD['currentHashes'][n],n) for n in ['src/page.html','src/style.css']])
case('R04 exact authorized presentation reverses to baseline',lambda:[req(sha(project(n,(R/n).read_text()).encode())==RECORD['baselineHashes'][n],n) for n in RECORD['edits']])
case('R05 projection cannot hide undeclared appended text',lambda:[req(sha(project(n,(R/n).read_text()+'\n// unexpected').encode())!=RECORD['baselineHashes'][n],n) for n in RECORD['edits']])
case('R06 logo reads Signature Lab without orange punctuation',lambda:(req(S.select_one('.brand-name').get_text()=='Signature Lab'),req(S.select_one('.brand-name .accent') is None)))
case('R07 original wheel image unchanged',lambda:req(S.select_one('.brand-mark')['src']==BeautifulSoup(RECORD['edits']['src/page.html']['before'],'html.parser').select_one('.brand-mark')['src']))
case('R08 Helvetica-first local family without distributed font files',lambda:(req(re.search(r'--app-font\s*:\s*Helvetica',css)),req('@font-face' not in css),req(not any(p.suffix.lower() in ['.ttf','.woff','.woff2','.otf'] for p in R.rglob('*')))))
case('R09 all application text uses one family',lambda:req('body,body *,body *::before,body *::after{font-family:var(--app-font)!important}' in css))
case('R10 QR canvas and control bindings unchanged',lambda:[req(len(S.select(sel))==1,sel) for sel in ['[x-ref="seedQrCanvas"]','#wallet-fingerprint-value','#wallet-loaded','#test-purpose']])
case('R11 browser privileges and external-resource boundaries unchanged',lambda:(req(S.select_one('[http-equiv="Content-Security-Policy"]')['content']==BeautifulSoup(RECORD['edits']['src/page.html']['before'],'html.parser').select_one('[http-equiv="Content-Security-Policy"]')['content']),req(not S.select('script[src],link[rel="stylesheet"]'))))
case('R12 single normal-flow footer with original attribution and licence route',lambda:(req(len(S.select('footer'))==1),req(S.select_one('footer a[href="#license-help"]') is not None),req('oren-z0 / exfil-tester' in S.select_one('footer').get_text())))
case('R13 body and main controls have explicit larger default sizes',lambda:(req('body{font-size:1.125rem' in css),req('.button,.button.small{font-size:1rem' in css)))
case('R14 display cannot change verification via new event bindings',lambda:req(sorted((a,v) for e in S.find_all() for a,v in e.attrs.items() if a.startswith(('@','x-')))==sorted((a,v) for e in BeautifulSoup(RECORD['edits']['src/page.html']['before'],'html.parser').find_all() for a,v in e.attrs.items() if a.startswith(('@','x-')))))
case('R15 fresh unique release plus explicit no hardware claim',lambda:(req(json.loads((R/'release.json').read_text())['version']=='0.20.3-rc1'),req('Physical signing-device and optical-scanning acceptance remain pending' in page)))
case('R16 current handoff docs distinguish fallback, retained runtime and missing old receipts',lambda:(req((R/'README.md').read_text().startswith('# Signature Lab v0.20.3-rc1')),req('No prior incomplete results' in (R/'README.md').read_text()),req('checklist, not a record' in (R/'docs/READABILITY-HARDWARE-ACCEPTANCE.md').read_text())))
r={'suite':'Readability static and preservation','complete':True,'sha256':sha(H.read_bytes()),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};O.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
