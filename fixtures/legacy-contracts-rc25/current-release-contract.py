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
case('release candidate identity exact',lambda:require(version['version']==expected['version']=='0.20.11-rc3' and version['status']=='release-candidate-device-testing-only','version or status'))
case('trusted module hashes unchanged from v0.20.9',lambda:require(all(sha((R/k).read_bytes())==v for k,v in old['trustedUnits'].items()),'trusted module edited'))
case('vendor module hashes unchanged',lambda:require(all(sha((R/k).read_bytes())==v for k,v in old['vendorHashes'].items()),'vendor edited'))
case('build tool unchanged',lambda:require(sha((R/'build.py').read_bytes())==old['buildToolHash'],'build altered'))
html=O.read_text()
case('offline CSP and limited matching warnings present',lambda:require("connect-src 'none'" in html and 'A match does not prove that firmware is safe.' in html and 'These counts are not a safety score' in html,'trust copy or CSP'))
case('one application coordinator and session journal',lambda:require(html.count('function Fv(')==1 and html.count('class TbwSessionJournal')==1,'duplicate controller'))
case('copyright statements match',lambda:require((R/'LICENSE.txt').read_text().count('Copyright (c) 2026 The Bitcoin Way')==1 and (R/'src/page.html').read_text().count('Copyright (c) 2026 The Bitcoin Way')==2,'copyright inconsistency'))
case('mutated source and output are rejected',lambda:require(all(sha((R/k).read_bytes()+b'\x00')!=v for k,v in lock.items()) and sha(O.read_bytes()+b'\x00')!=expected['sha256'],'tamper accepted'))
result={'schema':'tbw-v0210-current-release-contract-v1','passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'checks':rows}
dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed']}));sys.exit(bool(result['failed']))
