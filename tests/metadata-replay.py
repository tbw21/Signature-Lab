#!/usr/bin/env python3
"""Independent public-byte metadata replay and adversarial bundle tests."""
from pathlib import Path
import importlib.util,json,copy,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];HTML=Path(sys.argv[1]);DIR=Path(sys.argv[2]);OUT=Path(sys.argv[3]);rows=[]
sp=importlib.util.spec_from_file_location('independent_replay',ROOT/'tools/replay_evidence.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def test(name,f):
 try:f();rows.append({'name':name,'status':'passed'})
 except Exception as e:rows.append({'name':name,'status':'failed','error':repr(e)})
def reject(fn):
 try:fn()
 except (ValueError,KeyError,TypeError,AssertionError):return
 raise AssertionError('Tampered or unsupported evidence was accepted')
def require(v,msg='assertion failed'):
 if not v:raise AssertionError(msg)
cases=[]
for path in sorted(DIR.glob('metadata-fixtures-*.json')):cases+=json.loads(path.read_text())
require(len(cases)==32 and len({x['name'] for x in cases})==32,'All 32 independently supplied current fixtures required')
for c in cases:test('Metadata replay '+c['name'],lambda c=c:m.replay(c['evidence']))
base=cases[0]['evidence']
for name,path,value in [
 ('policy',['report','metadata','policy'],'future-policy'),('status',['report','metadata','status'],'unchanged'),
 ('count',['report','metadata','unexpected'],900),('field order count',['report','metadata','fieldOrderChanged'],100),
 ('conversion',['report','metadata','versionConversion'],True),('field position',['report','metadata','fields',0,'afterPosition'],88),
 ('value digest',['report','metadata','fields',0,'afterSha256'],'0'*64),('field classification',['report','metadata','fields',0,'classification'],'expected'),
 ('ordering observation',['report','metadata','fieldOrder',0,'relativeOrderChanged'],True),('overall verdict',['report','overallStatus'],'review'),
 ('analysis disagreement',['analysis','metadata','status'],'unexpected')]:
 def change(path=path,value=value):
  e=copy.deepcopy(base);p=e
  for k in path[:-1]:p=p[k]
  p[path[-1]]=value;reject(lambda:m.replay(e))
 test('Metadata replay rejects tampered '+name,change)
bundle=json.loads((DIR/'retention-7-10-session.json').read_text())
test('Twenty saved responses independently replay with honest scope',lambda:(require(m.replay_bundle(bundle)['replayed']==20),require(m.replay_bundle(bundle)['missing']==0)))
for name,mutate in [
 ('wrong slot hash',lambda b:b['events'][0].update(sha256='0'*64)),
 ('missing attachment',lambda b:b['events'][0].pop('evidenceJson')),
 ('duplicate index',lambda b:b['events'][1].update(index=1)),
 ('wrong wallet',lambda b:b.update(walletSession='different')),
 ('wrong retained count',lambda b:b['coverage'].update(retained=0)),
 ('wrong byte budget',lambda b:b['coverage'].update(bytes=1)),
 ('false clean aggregate',lambda b:b['history']['summary'].update(review=99)),
 ('unsupported counting policy',lambda b:b['history']['summary'].update(countPolicy='invented')),
 ('changed journal summary',lambda b:b['history']['events'][0].update(test=999))]:
 def tamper(mutate=mutate):
  b=copy.deepcopy(bundle);mutate(b);reject(lambda:m.replay_bundle(b))
 test('Bundle replay rejects '+name,tamper)
def incomplete():
 b=copy.deepcopy(bundle);slot=b['events'][0];size=slot['bytes'];b['events'][0]={'index':1,'type':'check','test':slot['test'],'retention':'not-enabled'}
 b['coverage'].update(retained=19,missing=1,bytes=b['coverage']['bytes']-size,allRecordedChecksRetained=False)
 r=m.replay_bundle(b);require(r['missing']==1 and r['replayed']==19);b['coverage']['allRecordedChecksRetained']=True;reject(lambda:m.replay_bundle(b))
test('Partial bundle declares missing response instead of claiming a complete replay',incomplete)
def keyencoding():
 r=m.Reader(b'\xfd\x01\x00');reject(lambda:r.compact(maximum=2**53-1))
test('Independent metadata type parser rejects noncanonical compact encoding',keyencoding)
for label,change in [
 ('too many references',lambda e:e['publicTest'].update(references=e['publicTest']['references']*4)),
 ('no references',lambda e:e['publicTest'].update(references=[])),
 ('empty method identifiers',lambda e:e['publicTest']['references'][0].update(ids=[])),
 ('duplicate reference method',lambda e:e['publicTest']['references'][0]['ids'].append(e['publicTest']['references'][0]['ids'][0])),
 ('incomplete report',lambda e:e['report'].update(completed=False)),
 ('unverified analysis',lambda e:e['analysis'].update(ok=False))]:
 def bad(change=change):
  e=copy.deepcopy(base);change(e);reject(lambda:m.replay(e))
 test('Independent replay rejects '+label,bad)
r={'suite':'Independent metadata and session-evidence replay','complete':True,'sha256':hashlib.sha256(HTML.read_bytes()).hexdigest(),'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows}
OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
