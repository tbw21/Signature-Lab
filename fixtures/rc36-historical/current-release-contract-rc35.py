#!/usr/bin/env python3
"""Current source identity + trust boundary; reject tampering, not legacy wording."""
import json,hashlib,sys,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
O=Path(sys.argv[1]);dest=Path(sys.argv[2]);rows=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def case(name, fn):
 try: fn(); rows.append({'name':name,'status':'passed'})
 except Exception as e: rows.append({'name':name,'status':'failed','reason':str(e)})
def require(p,s):
 if not p: raise AssertionError(s)
lock=json.loads((R/'source-lock.json').read_text());expected=json.loads((R/'EXPECTED-OUTPUT.json').read_text());version=json.loads((R/'release.json').read_text())
old=json.loads((R/'fixtures/v0209-trusted-source.json').read_text())
case('current source lock matches every authoritative build input',lambda:require(all(sha((R/k).read_bytes())==v for k,v in lock.items()),'source lock mismatch'))
case('current build output matches recorded hash',lambda:require(sha(O.read_bytes())==expected['sha256'] and O.stat().st_size==expected['bytes'],'output mismatch'))
case('release candidate identity exact',lambda:require(version['version']==expected['version']=='0.20.12-rc33' and version['status']==expected['status']=='development-ui-preview-unqualified' and version.get('publisherAuthenticated') is False and expected.get('publisherAuthenticated') is False,'version or status'))
def reviewed_module_provenance():
    reviewed=json.loads((R/'fixtures/approved-app-change.json').read_text())
    for name,digest in old['trustedUnits'].items():
        if name=='src/20-application.js':
            require(digest==reviewed['historicalSha256'],'Historical pin drift')
            approved=json.loads((R/'fixtures/rc30-historical/rc30-focus-provenance.json').read_text())
            archived=(R/'fixtures/rc30-historical/20-application-rc28.js').read_bytes()
            patch=(R/'fixtures/rc30-historical/rc28-to-rc30-focus.patch').read_bytes()
            require(sha(archived)==reviewed['currentSha256']==approved['baselineSha256'],'Reviewed RC28 application baseline changed')
            require(sha(patch)==approved['patchSha256'],'RC30 approved focus patch changed')
            require(archived.replace(b'this.$refs?.sessionNav?.focus?.({preventScroll:true});',b"document.querySelector('#tbw-settings > summary')?.focus?.({preventScroll:true});")== (R/name).read_bytes(),'More than RC30 reviewed focus change')
            require(sha((R/name).read_bytes())==approved['currentSha256']=='c3e4558e8b1d5afa1251691013abdfd1534a646dcd31ac2443c59dbe339fbe58','Unapproved current runtime change')
        else:require(sha((R/name).read_bytes())==digest,'Unexpected trusted module edit: '+name)
    patch=(R/'fixtures/reviewed-application-delta.patch').read_bytes()
    require(sha(patch)==reviewed['reviewedDiffSha256'],'Reviewed provenance diff tampered')
    require(reviewed['currentSha256']=='4ded7810831f8f841fdde9c9c3f3e94c808eb25605de995c53297c6ab8fcb26d','Unknown application change')
case('historical pins plus exact reviewed application delta',reviewed_module_provenance)
case('vendor module hashes unchanged',lambda:require(all(sha((R/k).read_bytes())==v for k,v in old['vendorHashes'].items()),'vendor edited'))
case('reviewed deterministic build-tool pin',lambda:require(sha((R/'build.py').read_bytes())=='8f2543d6f05f1cebd8a84610c51e0500258c00de053015576280d6619b0abb0e','Unreviewed build-tool change'))
html=O.read_text()
case('offline CSP and limited matching warnings present',lambda:require("connect-src 'none'" in html and 'A matching result is not proof that firmware is safe.' in html and 'A match is not proof of firmware safety.' in html and 'These counts are not a safety score' in html,'trust copy or CSP'))
case('one application coordinator and session journal',lambda:require(html.count('function Fv(')==1 and html.count('class TbwSessionJournal')==1,'duplicate controller'))
case('copyright statements match',lambda:require((R/'LICENSE.txt').read_text().count('Copyright (c) 2026 The Bitcoin Way')==1 and (R/'src/page.html').read_text().count('Copyright (c) 2026 The Bitcoin Way')==2,'copyright inconsistency'))
case('mutated source and output are rejected',lambda:require(all(sha((R/k).read_bytes()+b'\x00')!=v for k,v in lock.items()) and sha(O.read_bytes()+b'\x00')!=expected['sha256'],'tamper accepted'))
result={'schema':'tbw-v0210-current-release-contract-v1','passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'checks':rows}
dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed']}));sys.exit(bool(result['failed']))
