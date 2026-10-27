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
reviewed=json.loads((ROOT/'fixtures/approved-app-change.json').read_text())
for file,digest in F['trustedUnits'].items():
 def unit(file=file,digest=digest):
  req(sha(ROOT/file)==(reviewed['currentSha256'] if file=='src/20-application.js' else digest),file)
  if file=='src/20-application.js':
   req(digest==reviewed['historicalSha256'],'historical baseline drift')
   import hashlib
   req(hashlib.sha256((ROOT/'fixtures/reviewed-application-delta.patch').read_bytes()).hexdigest()==reviewed['reviewedDiffSha256'],'reviewed diff integrity')
 check('trusted runtime pin + reviewed app delta '+file,unit)
for file,digest in F['vendorHashes'].items():
 check('vendor unchanged '+file,lambda file=file,digest=digest:req(sha(ROOT/file)==digest,file))
check('reviewed build tool pin',lambda:req(sha(ROOT/'build.py')=='8f2543d6f05f1cebd8a84610c51e0500258c00de053015576280d6619b0abb0e','unreviewed build tool'))
check('version truthful',lambda:req(json.loads((ROOT/'release.json').read_text())['version']=='0.20.12-rc28' and json.loads((ROOT/'release.json').read_text())['status']=='development-ui-preview-unqualified','version'))
page=(ROOT/'src/page.html').read_text()
def critical():
 for text in ['How to read this record','These counts are not a safety score','No checks completed yet','Finish testing','Never enter a recovery phrase from an existing wallet','A matching result is not proof that firmware is safe.','id="advanced-view"','id="session-view"','id="transaction-editor"','id="guided-setup"','id="save-history"','id="session-checked"','id="finish-testing-open"']:
  req(text in page,text)
 req(page.count('id="session-interpretation"')==1,'one interpretation disclosure')
 req(page.count('id="session-evidence-tools"')==1,'one evidence block')
check('critical flow and caveats retained',critical)
report={'schema':'tbw-v0209-ui-contract-v1','passed':sum(c['status']=='passed' for c in checks),'failed':sum(c['status']=='failed' for c in checks),'results':checks}
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'failures':[x for x in checks if x['status']=='failed']},indent=2))
sys.exit(bool(report['failed']))
