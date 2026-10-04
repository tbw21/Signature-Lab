#!/usr/bin/env python3
"""Sidecar/prerequisite negative tests; explicit synthetic faults, not hardware trials."""
from pathlib import Path
import importlib.util,json,tempfile,sys,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);rows=[]
def module(n):
 s=importlib.util.spec_from_file_location(n,ROOT/'tools'/f'{n}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=module('verify_output');env=module('qualification_environment')
def test(n,f):
 try:f();rows.append({'name':n,'status':'passed'})
 except Exception as e:rows.append({'name':n,'status':'failed','error':repr(e)})
def expect_error(f):
 try:f()
 except (ValueError,FileNotFoundError):return
 raise AssertionError('Expected rejection')
def yes(x):
 if not x:raise AssertionError('Expected true')
def expected_mutation(key,value):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'expected.json';r=json.loads((ROOT/'EXPECTED-OUTPUT.json').read_text());r[key]=value;p.write_text(json.dumps(r));expect_error(lambda:v.verify(FILE,p))
test('SA-P01 source-only verifier checks actual rebuilt candidate and labels unsigned provenance',lambda:(yes(v.verify(FILE)['verified']),yes(v.verify(FILE)['publisherAuthenticated'] is False)))
test('SA-P02 incorrect output checksum is rejected',lambda:expected_mutation('sha256','0'*64))
test('SA-P03 correct bytes cannot conceal mismatched build-input identity',lambda:expected_mutation('sourceSha256','1'*64))
test('SA-P04 unsupported output receipt schema rejected',lambda:expected_mutation('schema','invented'))
def tamper():
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'modified.html';p.write_bytes(FILE.read_bytes()+b' ');expect_error(lambda:v.verify(p))
test('SA-P05 modified rebuilt artifact rejected without changing reference',tamper)
def synthetic_environment(kind):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'requirements';p.write_text('qrcode==8.2\n')
  def version(n):
   if kind=='missing-package':raise env.importlib.metadata.PackageNotFoundError(n)
   return '0.0' if kind=='wrong-version' else '8.2'
  def importer(n):
   if kind=='missing-native-library':raise ImportError('synthetic missing shared library')
  def which(n):return None if kind=='missing-tool' and n=='node' else '/usr/bin/'+n
  def run(*a,**k):return subprocess.CompletedProcess(a,0,stdout='synthetic tool',stderr='')
  r=env.inspect_environment(p,version,importer,which,run)
  yes(r['status']=='unavailable-environment');yes(r['candidateFailure'] is False);yes(bool(r['blockers']))
for kind in ['missing-package','wrong-version','missing-native-library','missing-tool']:
 test('SA-P06 dependency fault is environment-unavailable, not a candidate failure: '+kind,lambda k=kind:synthetic_environment(k))
def driver():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);dummy=d/'source.zip';dummy.write_bytes(b'placeholder: no source test should run')
  r=subprocess.run([sys.executable,str(ROOT/'qualify.py'),str(FILE),str(dummy),str(d/'out'),'--job','static'],cwd=ROOT,text=True,capture_output=True,timeout=15)
  yes(r.returncode==3);yes('UNAVAILABLE-ENVIRONMENT' in r.stderr);yes(not (d/'out/static.json').exists())
test('SA-P07 driver refuses unprepared environment before executing any candidate case',driver)
def malformed():
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'r';p.write_text('qrcode>=8\n');expect_error(lambda:env.inspect_environment(p))
test('SA-P08 unpinned qualification requirement rejected',malformed)
r={'suite':'Source-audit delivery and prerequisite faults','complete':True,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows};OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
