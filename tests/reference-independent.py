#!/usr/bin/env python3
"""Independent comparison of shipped signatures, supplied constants and digest/order boundaries."""
import sys,json,hashlib
from pathlib import Path
from reference_oracle import signature,N,methods
from cryptography.hazmat.primitives.asymmetric import ec,utils
from cryptography.hazmat.primitives import hashes
vectors=json.loads(Path(sys.argv[1]).read_text());out=Path(sys.argv[2]);rows=[]
for item in vectors:
 try:
  sk=bytes.fromhex(item['sk']);digest=bytes.fromhex(item['msghash']);private=ec.derive_private_key(int.from_bytes(sk,'big'),ec.SECP256K1());counters={}
  for mode,field in methods.items():
   calculated,counter=signature(sk,digest,mode);actual=bytes.fromhex(item['actual'][mode]);assert calculated==actual
   if item['source']=='supplied-audit':assert actual.hex()==item[field]
   private.public_key().verify(actual,digest,ec.ECDSA(utils.Prehashed(hashes.SHA256())))
   r,s=utils.decode_dss_signature(actual);assert s<=N//2;counters[mode]=counter
  # OpenSSL's RFC6979 is separate again from the Python HMAC nonce calculation.
  der=private.sign(digest,ec.ECDSA(utils.Prehashed(hashes.SHA256()),deterministic_signing=True));r,s=utils.decode_dss_signature(der)
  assert utils.encode_dss_signature(r,min(s,N-s)).hex()==item['actual']['plain']
  rows.append({'name':'Independent reference vector '+str(item['id']),'source':item['source'],'status':'passed','signatures':3,'counters':counters})
 except Exception as e:rows.append({'name':'Independent reference vector '+str(item['id']),'status':'failed','error':repr(e)})
try:
 item=vectors[0];sk=bytes.fromhex(item['sk']);digest=bytes.fromhex(item['msghash'])
 normal,_=signature(sk,digest,'plain');zeros,_=signature(sk,digest,'plain',first_extra=bytes(32));assert normal!=zeros
 rows.append({'name':'Absent nonce auxiliary data differs from 32 zero bytes','status':'passed'})
except Exception as e:rows.append({'name':'Absent nonce auxiliary data differs from 32 zero bytes','status':'failed','error':repr(e)})
r={'suite':'Independent PDF reference and digest-boundary oracle','complete':True,'oracle':'Python HMAC/integers/OpenSSL points plus OpenSSL deterministic-signature crosscheck; not BIP461 conformance or physical hardware','passed':sum(r['status']=='passed' for r in rows),'failed':sum(r['status']=='failed' for r in rows),'signatures':len(vectors)*3,'suppliedSignatures':48,'results':rows};out.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
