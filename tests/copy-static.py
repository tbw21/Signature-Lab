#!/usr/bin/env python3
"""Scoped presentation contracts: no runtime changes or attack-coverage escalation."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,sys
from reference_projection import read
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2])
page=read('src/page.html');css=read('src/style.css');html=FILE.read_text();results=[]
INTRO='Compare test signatures with expected results to flag deviations such as the published Dark Skippy example; a match cannot rule out all attacks.'
OLD_INTRO='Check your hardware wallet’s test signatures against expected results using a disposable wallet.<br class="purpose-break" /> A match does not prove the firmware is safe.'
OLD_LINE='<p class="wallet-fingerprint-help">Master key · No passphrase</p>'
OLD_SCOPE='<strong>A match does not prove the firmware is safe.</strong> It applies to this transaction only.'
NEW_SCOPE='<strong>This match applies to this transaction only.</strong> It does not rule out seed leakage or other firmware attacks.'
OLD_CSS='.purpose-brief{color:#afbdc9;font-size:14px;line-height:1.65;margin:0 0 18px;max-width:92ch;overflow-wrap:anywhere}'
NEW_CSS='.purpose-brief{color:#e5b67d;font-size:14px;font-weight:500;line-height:1.65;margin:0 0 18px;max-width:100%;overflow-wrap:anywhere;white-space:normal}'
SUFFIX='\n/* v0.16.4: compact scope copy, natural reflow and system high-contrast colors. */\n@media(forced-colors:active){.purpose-brief{color:CanvasText}}\n'
sha=lambda b:hashlib.sha256(b).hexdigest()
def check(v,m='assertion failed'):
 if not v:raise AssertionError(m)
def test(name,fn):
 try:fn();results.append({'name':name,'status':'passed'})
 except Exception as e:results.append({'name':name,'status':'failed','error':repr(e)})
def intro():
 check(page.count('id="test-purpose"')==1);check(f'id="test-purpose">{INTRO}</p>' in page)
 check('purpose-break' not in page);check(html.count(INTRO)==1)
test('C-S01 exact scoped purpose copy is one canonical paragraph without a forced break',intro)
def color():
 check(NEW_CSS in css);check('purpose-break' not in css)
 rules=re.findall(r'\.purpose-brief\{([^}]+)\}',css)
 check(not any(re.search(r'(?:white-space\s*:\s*nowrap|overflow\s*:\s*(?:hidden|clip)|text-overflow\s*:\s*ellipsis|(?:^|;)height\s*:)',r) for r in rules))
 check('color:CanvasText' in rules[-1])
test('C-S02 gold purpose text retains natural reflow and forced-colour fallback',color)
def location():
 check(OLD_LINE not in page);check(page.count('id="wallet-technical-note"')==1)
 i=page.index('id="technical-help"');end=page.index('</div></details>',i)
 note=page[i:end];check('BIP32 master-key fingerprint' in note);check('uses no passphrase' in note)
 check('without adding one' in note);check('id="wallet-fingerprint-value"' in page)
test('C-S03 wallet note moves to technical Help while the live fingerprint remains',location)
def result_scope():
 check(page.count(NEW_SCOPE)==1);check(OLD_SCOPE not in page)
 check('<p class="result-limit" x-show="resultState === \'match\'"><span>'+NEW_SCOPE in page)
 check('Signatures matched. File changes need review.' in page)
test('C-S04 matching result explicitly retains transaction-specific and seed-leakage limits',result_scope)
def semantics():
 check(page.count('id="signature-scope-note"')==1)
 i=page.index('id="signature-check"');end=page.index('</div></details>',i);t=page[i:end]
 for text in ['not a search for an attacker’s secret watermark','cannot rule out a conditional Dark Skippy variant','later seed leakage']:
  check(text in t,text)
 for text in ['detects all Dark Skippy','Dark Skippy-free','guarantees safe']:check(text not in html,text)
test('C-S05 method explanation distinguishes reference comparison from universal attack detection',semantics)
def preservation():
 data=json.loads((ROOT/'fixtures/copy-unchanged.json').read_text())
 for name,value in data.items():check(sha(read(name).encode())==value,name)
 check(len(json.loads((ROOT/'fixtures/alignment-unchanged.json').read_text()))==29)
test('C-S06 retained runtime/build/input order preserved after exact declared startup projection',preservation)
def page_projection():
 t=page.replace(INTRO,OLD_INTRO,1).replace(NEW_SCOPE,OLD_SCOPE,1)
 t=re.sub(r'<p id="wallet-technical-note">.*?</p>','',t,count=1)
 t=re.sub(r'<p id="signature-scope-note">.*?</p>','',t,count=1)
 marker="x-text=\"walletFingerprint || 'Unavailable'\">Unavailable</code></div>"
 check(t.count(marker)==1);t=t.replace(marker,marker+OLD_LINE,1)
 check(sha(t.encode())==json.loads((ROOT/'fixtures/copy-projection.json').read_text())['pageSha256'])
test('C-S07 reversing current audit additions plus prior authorized copy restores original template',page_projection)
def css_projection():
 check(css.endswith(SUFFIX));t=css[:-len(SUFFIX)].replace(NEW_CSS,OLD_CSS,1)
 marker='@media(max-width:760px){.purpose-brief{font-size:13px;line-height:1.65;margin-bottom:14px}'
 check(t.count(marker)==1);t=t.replace(marker,marker+'.purpose-break{display:none}',1)
 check(sha(t.encode())==json.loads((ROOT/'fixtures/copy-projection.json').read_text())['cssSha256'])
test('C-S08 reversing authorized purpose styling restores every original CSS byte',css_projection)
def menu():
 expected=json.loads((ROOT/'fixtures/copy-projection.json').read_text())['questions']
 actual=[list(x) for x in re.findall(r'<details class="details" id="([^"]+)" data-help-group="([^"]+)"><summary>(.*?)</summary>',page)]
 check(actual==expected);check(len(actual)==22)
test('C-S09 FAQ headings, groups and IDs stay unchanged so the generated contents remain canonical',menu)
def architecture():
 p=ROOT/'docs/COPY-ARCHITECTURE-FROZEN.md';record=json.loads((ROOT/'fixtures/copy-projection.json').read_text())
 check(sha(p.read_bytes())==record['architectureSha256']);check(INTRO in p.read_text())
 check(json.loads((ROOT/'release.json').read_text())['version']=='0.20.3-rc1')
test('C-S10 architecture remains frozen and candidate version is unique to the refinement',architecture)
r={'suite':'Copy/scope static and preservation contracts','complete':True,'sha256':sha(FILE.read_bytes()),'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results}
OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
