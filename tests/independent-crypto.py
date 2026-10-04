"""Audit-only independent BIP32/BIP143/RFC6979 oracle.
Uses Python hashlib/HMAC and cryptography/OpenSSL secp256k1, not the bundled JS libraries.
Input fixtures are browser-generated disposable wallets, never funded wallets.
"""
import hashlib,hmac,json,struct,unicodedata,time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ec,utils
from cryptography.hazmat.primitives import hashes,serialization
import sys
FIXTURES=Path(sys.argv[1]);OUTPUT=Path(sys.argv[2]);N=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
sha=lambda b:hashlib.sha256(b).digest()
dsha=lambda b:sha(sha(b))
mac=lambda k,d:hmac.new(k,d,hashlib.sha256).digest()
le=lambda x:struct.pack('<I',x)
ser=lambda x:x.to_bytes(32,'big')
def compact(x):
 if x<253:return bytes([x])
 for code,size in [(253,2),(254,4),(255,8)]:
  if x<1<<(size*8):return bytes([code])+x.to_bytes(size,'little')
def public(k):return ec.derive_private_key(k,ec.SECP256K1()).public_key().public_bytes(serialization.Encoding.X962,serialization.PublicFormat.CompressedPoint)
def derive(words,path):
 seed=hashlib.pbkdf2_hmac('sha512',unicodedata.normalize('NFKD',words).encode(),b'mnemonic',2048,64)
 m=hmac.new(b'Bitcoin seed',seed,hashlib.sha512).digest();k=int.from_bytes(m[:32],'big');chain=m[32:]
 for index in path:
  data=(b'\0'+ser(k) if index>=2**31 else public(k))+index.to_bytes(4,'big')
  m=hmac.new(chain,data,hashlib.sha512).digest();k=(k+int.from_bytes(m[:32],'big'))%N;chain=m[32:]
 return k
class Reader:
 def __init__(self,raw):self.b=raw;self.p=0
 def get(self,n):
  b=self.b[self.p:self.p+n];assert len(b)==n;self.p+=n;return b
 def cv(self):
  a=self.get(1)[0];return a if a<253 else int.from_bytes(self.get({253:2,254:4,255:8}[a]),'little')
 def blob(self):return self.get(self.cv())
def parse(raw):
 r=Reader(raw);version=r.get(4);segwit=r.get(2);assert segwit==b'\x00\x01'
 ins=[]
 for i in range(r.cv()):ins.append((r.get(36),r.blob(),r.get(4)))
 outs=[]
 for i in range(r.cv()):outs.append((r.get(8),r.blob()))
 witnesses=[]
 for i in range(len(ins)):witnesses.append([r.blob() for _ in range(r.cv())])
 locktime=r.get(4);assert r.p==len(raw)
 return version,ins,outs,witnesses,locktime
def sign(digest,key,extra=b''):
 data=ser(key)+ser(int.from_bytes(digest,'big')%N)+extra
 v=b'\x01'*32;k=b'\x00'*32
 k=mac(k,v+b'\x00'+data);v=mac(k,v);k=mac(k,v+b'\x01'+data);v=mac(k,v)
 while True:
  v=mac(k,v);nonce=int.from_bytes(v,'big')
  if 0<nonce<N:
   r=ec.derive_private_key(nonce,ec.SECP256K1()).public_key().public_numbers().x%N
   s=(pow(nonce,-1,N)*(int.from_bytes(digest,'big')+r*key))%N
   if r and s:return utils.encode_dss_signature(r,min(s,N-s))
  k=mac(k,v+b'\x00');v=mac(k,v)
def expected(digest,key,mode):
 sig=sign(digest,key);counter=1
 def valid(sig):
  if mode=='plain':return True
  if mode=='grind-embit':return len(sig)<=70
  return utils.decode_dss_signature(sig)[0]<1<<255
 while not valid(sig):
  sig=sign(digest,key,le(counter)+b'\x00'*28);counter+=1;assert counter<1000
 return sig
rows=[];inputs=0;variants=0;openssl_plain_crosschecks=0
for vector in json.loads(FIXTURES.read_text()):
 start=time.monotonic();spec=vector['spec'];cases=0
 for variant in vector['variants']:
  version,ins,outs,witnesses,locktime=parse(bytes.fromhex(variant['txHex']))
  assert version==le(2) and locktime==le(spec['lockTime'])
  hp=dsha(b''.join(x[0] for x in ins));hs=dsha(b''.join(x[2] for x in ins));ho=dsha(b''.join(a+compact(len(b))+b for a,b in outs))
  for index,source in enumerate(spec['inputs']):
   key=derive(spec['mnemonic'],[0x80000054,0x80000000,0x80000000+source['account'],source['change'],source['addressIndex']]);pub=public(key)
   assert ins[index][0]==bytes.fromhex(source['txid'])[::-1]+le(source['vout'])
   assert ins[index][1]==b'' and ins[index][2]==le(source['sequence'])
   assert witnesses[index][1]==pub
   script=b'\x76\xa9\x14'+hashlib.new('ripemd160',sha(pub)).digest()+b'\x88\xac'
   msg=dsha(version+hp+hs+ins[index][0]+compact(len(script))+script+int(source['amountSats']).to_bytes(8,'little')+ins[index][2]+ho+locktime+le(1))
   sig=witnesses[index][0];assert sig[-1]==1
   ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(),pub).verify(sig[:-1],msg,ec.ECDSA(utils.Prehashed(hashes.SHA256())))
   # OpenSSL is a second implementation of plain RFC6979, in addition to this Python oracle.
   op=ec.derive_private_key(key,ec.SECP256K1()).sign(msg,ec.ECDSA(utils.Prehashed(hashes.SHA256()),deterministic_signing=True))
   r,s=utils.decode_dss_signature(op);op=utils.encode_dss_signature(r,min(s,N-s));assert op==sign(msg,key)
   openssl_plain_crosschecks+=1
   for mode in variant['ids']:assert sig[:-1]==expected(msg,key,mode),(vector['scenario'],index,mode)
   cases+=1
  variants+=1
 inputs+=len(spec['inputs'])
 rows.append({'scenario':vector['scenario'],'inputCount':len(spec['inputs']),'uniqueVariants':len(vector['variants']),'signatureChecks':cases,'status':'passed','seconds':round(time.monotonic()-start,3)})
r={'oracle':'Python hashlib/HMAC + cryptography/OpenSSL; no JS signing/parsing libraries','scenarios':len(rows),'distinctTestInputs':inputs,'uniqueSignedTransactions':variants,'signatureChecks':openssl_plain_crosschecks,'passed':len(rows),'failed':0,'results':rows}
OUTPUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
