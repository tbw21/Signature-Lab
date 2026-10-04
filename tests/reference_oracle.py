"""Independent RFC6979/strict-low-r/DER-length oracle, Python HMAC + OpenSSL points."""
import hashlib,hmac
from cryptography.hazmat.primitives.asymmetric import ec,utils
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
methods={'plain':'plain_der','grind-core':'grind_core_der','grind-embit':'grind_embit_der'}
def mac(k,m):return hmac.new(k,m,hashlib.sha256).digest()
def signature(sk,digest,method,first_extra=None):
 d=int.from_bytes(sk,'big');z=int.from_bytes(digest,'big')%N
 assert 1<=d<N and len(sk)==len(digest)==32
 for ctr in range(100000):
  extra=(first_extra or b'') if ctr==0 else ctr.to_bytes(4,'little')+bytes(28)
  seed=sk+z.to_bytes(32,'big')+extra;k=bytes(32);w=b'\x01'*32
  k=mac(k,w+b'\0'+seed);w=mac(k,w);k=mac(k,w+b'\1'+seed);w=mac(k,w)
  for _ in range(1000):
   w=mac(k,w); nonce=int.from_bytes(w,'big')
   if 1<=nonce<N:
    r=ec.derive_private_key(nonce,ec.SECP256K1()).public_key().public_numbers().x%N
    s=pow(nonce,-1,N)*(z+r*d)%N
    if r and s:break
   k=mac(k,w+b'\0');w=mac(k,w)
  else:raise RuntimeError('nonce exhaustion')
  s=min(s,N-s);der=utils.encode_dss_signature(r,s)
  if method=='plain' or (method=='grind-core' and r<2**255) or (method=='grind-embit' and len(der)<=70):return der,ctr
 raise RuntimeError('grind exhaustion')
