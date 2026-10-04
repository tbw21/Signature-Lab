#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json,copy,sys
root=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('replay',root/'tools/replay_evidence.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
cases=json.loads(Path(sys.argv[1]).read_text());results=[]
def test(name,f):
    try:f();results.append({'name':name,'status':'passed'})
    except Exception as e:results.append({'name':name,'status':'failed','error':repr(e)})
for case in cases:test('public-only replay '+case['name'],lambda c=case:m.replay(c['evidence']))
base=cases[0]['evidence']
def mutation(path,value):
    def action():
        data=copy.deepcopy(base);parent=data
        for item in path[:-1]:parent=parent[item]
        parent[path[-1]]=value
        try:m.replay(data)
        except Exception:return
        raise AssertionError('Altered evidence was accepted')
    return action
for name,path,value in [
 ('artifact bytes',['returnedArtifact','hex'],'00'),('artifact hash',['returnedArtifact','sha256'],'0'*64),
 ('public input amount',['publicTest','inputs',0,'amountSats'],'1'),('public digest',['publicTest','inputs',0,'digestHex'],'0'*64),
 ('public input key',['publicTest','inputs',0,'publicKeyHex'],'02'+'0'*64),('public output amount',['publicTest','outputs',0,'amountSats'],'123'),
 ('unsigned transaction',['publicTest','unsignedTransactionHex'],'00'),('prepared PSBT',['publicTest','psbtHex'],'00'),
 ('policy version',['report','signingPolicy','version'],'future'),('policy ID',['report','signingPolicy','id'],'auto'),
 ('reported verdict',['report','result'],'mismatch'),('reported transaction ID',['report','evidence','transactionId'],'0'*64),
 ('reference bytes',['publicTest','references',0,'txHex'],'00'),('signature count',['report','evidence','signaturesVerified'],999),
 ('reported signed bytes',['analysis','txHex'],'00'),('matched labels',['report','matchedAlgorithms'],[])]:
    test('replay rejects changed '+name,mutation(path,value))
r={'suite':'Independent public evidence replay and tampering checks','passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results};Path(sys.argv[2]).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(1 if r['failed'] else 0)
