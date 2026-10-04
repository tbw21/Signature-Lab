"""Independent Python check of the public 20-output review/evidence fixture, not hardware."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent
namespace={'__file__':str(ROOT/'independent-structure.py')}
exec((ROOT/'independent-structure.py').read_text().split('results=[]')[0],namespace)
parse=namespace['parse'];address_script=namespace['address_script']
f=json.loads(Path(sys.argv[1]).read_text());rows=f['rows'];e=f['evidence'];public=e['publicTest'];results=[]
def case(name,fn):
 try:fn();results.append({'name':name,'status':'passed'})
 except Exception as exc:results.append({'name':name,'status':'failed','error':str(exc)})
def check_count():assert len(rows)==20==len(public['outputs'])
def check_amounts():assert all(int(r['amountSats'])==int(o['amountSats']) for r,o in zip(rows,public['outputs']))
def check_scripts():assert all(address_script(r['address']).hex()==r['scriptHex']==o['scriptHex'] for r,o in zip(rows,public['outputs']))
def check_order():assert [r['index'] for r in rows]==list(range(20))
def check_raw():
 tx=e['analysis']['txHex'];ver,ins,outs,wit,lock=parse(bytes.fromhex(tx))
 assert len(outs)==20
 for (amount,script),row in zip(outs,rows):
  assert int.from_bytes(amount,'little')==int(row['amountSats']) and script.hex()==row['scriptHex']
def check_binding():
 import hashlib
 raw=bytes.fromhex(e['returnedArtifact']['hex']);assert hashlib.sha256(raw).hexdigest()==e['returnedArtifact']['sha256']
 assert e['report']['result']=='match' and e['report']['deviceOrigin']=='not-attested'
for name,fn in [('20 outputs present',check_count),('amounts exact',check_amounts),('independent Bech32 destination decoding',check_scripts),('order complete',check_order),('verified signed transaction matches review',check_raw),('original response hash and scope',check_binding)]:case(name,fn)
out={'suite':'Independent 20-output review oracle','passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results};Path(sys.argv[2]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(1 if out['failed'] else 0)
