#!/usr/bin/env python3
"""Single v0.20.5 developer source and UI truthfulness contract.
Only exact v0.20.4-to-v0.20.5 wording/version changes are authorized.
This is a provenance consistency check, NOT independent publisher authentication.
"""
from pathlib import Path
import hashlib, json, sys, re
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
FIX=json.loads((ROOT/'fixtures/v0205-current-contract.json').read_text())
EXPECTED=json.loads((ROOT/'EXPECTED-OUTPUT.json').read_text())
HTML=ROOT.parent/'TBW-Signature-Lab-v0.20.5-dev.html'
checks=[]

def sha(b):return hashlib.sha256(b).hexdigest()
def case(n,fun):
    try:fun();checks.append({'name':n,'status':'passed'})
    except Exception as e:checks.append({'name':n,'status':'failed','reason':str(e)})
def require(cond,why):
    if not cond:raise AssertionError(why)

def source_contract(blob_overrides=None):
    blob_overrides=blob_overrides or {}
    baseline=FIX['baselineSourceHashes'];current=FIX['candidateSourceHashes']
    require(set(current)==set(baseline),'Changed source inventory')
    require(FIX['allowedRuntimeChanges']==['release.json','src/page.html'],'Unapproved allowlist')
    changes=[k for k in current if current[k]!=baseline[k]]
    require(set(changes)==set(FIX['allowedRuntimeChanges']),'Unexpected modified build input')
    for p,digest in current.items():
        contents=blob_overrides.get(p,(ROOT/p).read_bytes())
        require(sha(contents)==digest,'Source mismatch: '+p)
    template=blob_overrides.get('src/page.html',(ROOT/'src/page.html').read_bytes()).decode()
    for change in reversed(FIX['exactReleaseWordingSubstitutions']):
        require(template.count(change['new'])==1,'Changed release wording delta')
        template=template.replace(change['new'],change['old'])
    require(sha(template.encode())==baseline['src/page.html'],'Source-template reconstruction mismatch')
    version=json.loads(blob_overrides.get('release.json',(ROOT/'release.json').read_bytes()))
    require(version['version']=='0.20.5-dev','Incorrect current release version')
    require(version['status']=='development-not-a-release-candidate','Incorrect development status')
    require(version['baseline']=='v0.20.4-dev frozen; release-status truthfulness correction only','Scope changed')
    require(current==json.loads((ROOT/'source-lock.json').read_text()),'Source lock is not authoritative')

def release_text():
    html=HTML.read_text()
    for item in ('v0.20.5-dev development preview: hardware acceptance pending; not approved for public deployment',
                 'title="Development preview. Not approved for public deployment; hardware acceptance pending."',
                 'is a development preview, not an approved release.',
                 'Publisher authentication and independent security review are not complete.',
                 'Physical signing-device and optical-scanning acceptance remain pending.',
                 'This page is not a firmware safety certificate.'):
        require(html.count(item)==1,'Missing or duplicated release statement: '+item)
    require('v0.20.5-dev release candidate' not in html,'Unapproved RC label')
    require('is a release candidate.' not in html,'Unapproved visible RC status')
    require('Release candidate. Hardware acceptance pending.' not in html,'Unapproved tooltip')
    require('This page is not an independent security audit' not in html,'Stale review wording')

def manifest_gate():
    require(EXPECTED['version']=='0.20.5-dev','Expected output version')
    require(EXPECTED['sha256']==sha(HTML.read_bytes()),'Expected html mismatch')
    require(EXPECTED['bytes']==HTML.stat().st_size,'Expected html length mismatch')
    require(EXPECTED['publisherAuthenticated'] is False,'Claimed publisher authentication')
    require(EXPECTED['status']=='development-not-qualified-for-public-use','Release grade mismatch')

def runtime_gate():
    html=HTML.read_text()
    require("connect-src 'none'" in html and "font-src 'none'" in html,'Offline CSP altered')
    require('No Taproot, multisig or real wallet tests.' in html,'Signing scope warning absent')
    require('A match does not prove that firmware is safe.' in html,'Safety limit warning absent')
    require('Never enter your real seed' in html,'Real seed prohibition missing')
    require('overwrite an existing wallet on your signer' in html.lower(),'Real wallet overwrite protection missing')
    require('autocomplete="off"' in html and 'translate="no"' in html,'Privacy hints disappeared')
    require(html.count('function Fv(')==1,'App coordinator duplicated')
    require(html.count('class TbwSessionJournal')==1,'Journal duplicated')
    require('End session and keep report' in html and 'Finish testing' in html,'Distinct lifecycle controls missing')

case('Q01 inventory exactly matches v0.20.4 frozen source',lambda:source_contract())
case('Q02 only two authorized build inputs changed',lambda:require(set(k for k,v in FIX['candidateSourceHashes'].items() if v!=FIX['baselineSourceHashes'][k])=={'release.json','src/page.html'},'Source boundary'))
case('Q03 current wording appears in built HTML, including accessibility and Help',release_text)
case('Q04 expected output, development grade and size consistent',manifest_gate)
case('Q05 offline policy, signing caveat, privacy and singleton architecture remain',runtime_gate)
# Unknown internal file names are not assumed; attack the actual allowlisted source identity instead.
def rejects(path,content):
    try:source_contract({path:content})
    except (AssertionError,ValueError,UnicodeDecodeError):return True
    return False
original=(ROOT/'src/page.html').read_bytes()
case('N02 appended script to approved page rejected',lambda:require(rejects('src/page.html',original+b'<!-- unauthorized -->'),'Tampered page accepted'))
case('N03 forged accessible status rejected',lambda:require(rejects('src/page.html',original.replace(b'development preview',b'release candidate',1)),'Forged release status accepted'))
release=(ROOT/'release.json').read_bytes()
case('N04 changing release version rejected',lambda:require(rejects('release.json',release.replace(b'0.20.5-dev',b'0.20.5-rc1')),'RC promotion accepted'))
other=next(x for x in FIX['candidateSourceHashes'] if x.startswith('src/') and x not in FIX['allowedRuntimeChanges'])
case('N05 changed trusted runtime rejected',lambda:require(rejects(other,(ROOT/other).read_bytes()+b'\nunauthorized'), 'Unapproved trusted runtime accepted'))
case('N06 change to stylesheet rejected',lambda:require(rejects('src/style.css',(ROOT/'src/style.css').read_bytes()+b'\n/* changed */'), 'Unapproved styling accepted'))
case('N07 tampered build tool rejected',lambda:require(rejects('build.py',(ROOT/'build.py').read_bytes()+b'\n# changed'), 'Unapproved builder accepted'))
result={'schema':'tbw-v0205-current-contract-results-v1','version':'0.20.5-dev','passed':sum(x['status']=='passed' for x in checks),'failed':sum(x['status']=='failed' for x in checks),'checks':checks}
print(json.dumps(result,indent=2))
if len(sys.argv)>1: Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
sys.exit(1 if result['failed'] else 0)
