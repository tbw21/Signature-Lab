#!/usr/bin/env python3
"""Pure contents generation and editorial-input fault contracts. No browser or hardware."""
from pathlib import Path
from html.parser import HTMLParser
import sys,json,hashlib,re,importlib.util
from reference_projection import read
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);results=[]
spec=importlib.util.spec_from_file_location('build',ROOT/'build.py');build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
source=(ROOT/'src/page.html').read_text();html=FILE.read_text()
def check(v,msg='assertion failed'):
 if not v:raise AssertionError(msg)
def test(name,f):
 try:f();results.append({'name':name,'status':'passed'})
 except Exception as e:results.append({'name':name,'status':'failed','error':repr(e)})
def rejects(s):
 try:build.help_contents(s)
 except ValueError:return
 raise AssertionError('Invalid help source accepted')
class Menu(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.current=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a':self.current=[a.get('href'), '']
 def handle_data(self,s):
  if self.current:self.current[1]+=s
 def handle_endtag(self,t):
  if t=='a' and self.current:self.links.append(self.current);self.current=None
menu=build.help_contents(source)
def identity():
 a=Menu();a.feed(menu)
 items=re.findall(r'<details class="details" id="([^"]+)" data-help-group="[^"]+"><summary>(.*?)</summary>',source,re.S)
 check(len(items)==22);check(set(h for h,t in a.links)=={'#'+i for i,t in items});check(len(a.links)==len(items))
 from html import unescape
 check(dict(a.links)=={'#'+i:unescape(t) for i,t in items})
test('O-B01 every canonical FAQ has exactly one same-title contents link',identity)
test('O-B02 contents output is deterministic and embedded once',lambda:(check(menu==build.help_contents(source)),check(html.count(menu)==1)))
test('O-B03 missing FAQ id is a terminal build error',lambda:rejects(source.replace('id="known-example"','',1)))
test('O-B04 unknown group is a terminal build error',lambda:rejects(source.replace('data-help-group="Start here"','data-help-group="Unknown"',1)))
test('O-B05 duplicate ID is rejected instead of ambiguous navigation',lambda:rejects(source.replace('id="known-example"','id="test-view"',1)))
test('O-B06 unsafe target syntax is rejected',lambda:rejects(source.replace('id="known-example"','id="a/b"',1)))
test('O-B07 missing question title is rejected',lambda:rejects(source.replace('<summary>Try a known malicious-signature example</summary>','<summary> </summary>',1)))
test('O-B08 incomplete taxonomy group is rejected',lambda:rejects(source.replace('data-help-group="Method &amp; trust"','data-help-group="Start here"')))
test('O-B09 empty optional Help cannot silently generate misleading contents',lambda:rejects('<html><body></body></html>'))
test('O-B10 unbalanced template fails deterministically',lambda:rejects(source.replace('</body>','</div></body>',1)))
def escape_test():
 changed=source.replace('Try a known malicious-signature example','Example &lt;untrusted&gt; &amp; <em>italic</em>',1)
 m=build.help_contents(changed)
 check('Example &lt;untrusted&gt; &amp; italic' in m);check('<untrusted>' not in m);check('<em>' not in m)
test('O-B11 generated titles are escaped plain text, never markup',escape_test)
def unchanged():
 record=json.loads((ROOT/'fixtures/alignment-unchanged.json').read_text())
 for name,digest in record.items():check(hashlib.sha256(read(name).encode()).hexdigest()==digest,name)
 check(len(record)==29)
test('O-B12 retained 29-unit baseline preserved after exact declared startup projection',unchanged)
result={'suite':'Onboarding build/contents contracts and faults','complete':True,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'results':results}
OUT.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));sys.exit(bool(result['failed']))
