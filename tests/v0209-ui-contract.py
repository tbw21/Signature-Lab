#!/usr/bin/env python3
"""v0.20.9 exact trusted-unit, version and safety copy contract; no older source required."""
from pathlib import Path
import json,hashlib,re,sys
ROOT=Path(__file__).resolve().parents[1]
F=json.loads((ROOT/'fixtures/v0209-trusted-source.json').read_text())
checks=[]
def check(label,work):
 try:work();checks.append({'name':label,'status':'passed'})
 except Exception as e:checks.append({'name':label,'status':'failed','detail':str(e)})
def req(condition,label):
 if not condition:raise AssertionError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for file,digest in F['trustedUnits'].items():
 check('trusted runtime unchanged '+file,lambda file=file,digest=digest:req(sha(ROOT/file)==digest,file))
for file,digest in F['vendorHashes'].items():
 check('vendor unchanged '+file,lambda file=file,digest=digest:req(sha(ROOT/file)==digest,file))
check('build tool unchanged',lambda:req(sha(ROOT/'build.py')==F['buildToolHash'],'build tool'))
check('version truthful',lambda:req(json.loads((ROOT/'release.json').read_text())['version']=='0.20.9-dev','version'))
page=(ROOT/'src/page.html').read_text()
def critical():
 for text in ['How to read this record','These counts are not a safety score','No responses have been checked yet.','Finish testing','Never enter your real seed','A match does not prove that firmware is safe.','id="advanced-view"','id="session-view"','id="transaction-editor"','id="guided-setup"','id="save-history"','id="session-checked"','id="finish-testing-open"']:
  req(text in page,text)
 req(page.count('id="session-interpretation"')==1,'one interpretation disclosure')
 req(page.count('id="session-evidence-tools"')==1,'one evidence block')
check('critical flow and caveats retained',critical)
report={'schema':'tbw-v0209-ui-contract-v1','passed':sum(c['status']=='passed' for c in checks),'failed':sum(c['status']=='failed' for c in checks),'results':checks}
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'failures':[x for x in checks if x['status']=='failed']},indent=2))
sys.exit(bool(report['failed']))
