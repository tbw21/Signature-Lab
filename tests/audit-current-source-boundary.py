#!/usr/bin/env python3
"""Qualification-only invariant and negative-mutation checks for frozen v0.20.10.
Does not replace historical UI/accessibility cases or authenticate the publisher.
"""
from pathlib import Path
import hashlib,json,sys,subprocess
root=Path(__file__).resolve().parents[1]
html=Path(sys.argv[1]);out=Path(sys.argv[2]);checks=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def check(name,func):
 try:func();checks.append(dict(name=name,status='passed'))
 except Exception as e:checks.append(dict(name=name,status='failed',error=repr(e)))
def require(expr,msg):
 if not expr:raise AssertionError(msg)
lock=json.loads((root/'source-lock.json').read_text())
expected=json.loads((root/'EXPECTED-OUTPUT.json').read_text())
source=json.loads((root/'sources.json').read_text())
check('Exact HTML digest and size',lambda:require(sha(html.read_bytes())==expected['sha256'] and html.stat().st_size==expected['bytes'],'HTML identity'))
check('Every locked source input matches digest',lambda: [require(sha((root/p).read_bytes())==digest,p) for p,digest in lock.items()])
check('Authoritative runtime source inventory unique',lambda:require(len(source)==len(set(source)),'Duplicate source unit'))
check('All trusted modules included in source lock',lambda:[require(p in lock,'Missing source lock '+p) for p in source])
check('No source lock symlinks or traversals',lambda:[require(not Path(p).is_absolute() and '..' not in Path(p).parts and not (root/p).is_symlink(),p) for p in lock])
check('Offline CSP and network disallow',lambda:require("connect-src 'none'" in html.read_text() and "font-src 'none'" in html.read_text(),'Missing offline CSP'))
check('Single app coordinator and session journal',lambda:require(html.read_text().count('function Fv(')==1 and html.read_text().count('class TbwSessionJournal')==1,'Controller duplication'))
check('Seed and result safety caveats present',lambda:require('Never enter your real seed' in html.read_text() and 'A match does not prove that firmware is safe.' in html.read_text(),'Safety caveats'))
check('Version remains development-only',lambda:require(json.loads((root/'release.json').read_text())['status']=='development-not-a-release-candidate' and expected['publisherAuthenticated'] is False,'Release claim'))
def mutation_test():
 for p,digest in lock.items():
  original=(root/p).read_bytes();changed=original+b'\n# intentional negative-mutation'
  require(sha(changed)!=digest,'Mutation did not invalidate '+p)
check('All source input mutations invalidate identity',mutation_test)
result={'schema':'tbw-audit-boundary-v1','applicationSha256':sha(html.read_bytes()),'passed':sum(x['status']=='passed' for x in checks),'failed':sum(x['status']=='failed' for x in checks),'checks':checks}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed']}));sys.exit(bool(result['failed']))
