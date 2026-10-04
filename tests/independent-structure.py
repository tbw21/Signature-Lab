"""Independent audit checks of six saved disposable fixtures, not application code.
Checks expected transaction serialization and PSBT v0/v2 maps without JS parsers.
"""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parent
FIXTURES=Path(sys.argv[1]);OUTPUT=Path(sys.argv[2])
# Reuse independent Python primitives, but not its top-level run or any JS code.
ns = {}
exec((ROOT/'independent-crypto.py').read_text().split('rows=[];inputs=0;')[0], ns)
derive, public, sha, dsha = (ns[k] for k in ('derive','public','sha','dsha'))
compact, le, Reader, parse = (ns[k] for k in ('compact','le','Reader','parse'))
import hashlib

def pkh(pub):
    return hashlib.new('ripemd160',sha(pub)).digest()

def path(row):
    return [0x80000054,0x80000000,0x80000000+row['account'],row['change'],row['addressIndex']]

def address_script(address):
    assert address == address.lower() or address == address.upper()
    text=address.lower(); hrp,data=text.rsplit('1',1); assert hrp=='bc'
    alphabet='qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    values=[alphabet.index(c) for c in data]
    check=1
    for value in [ord(c)>>5 for c in hrp]+[0]+[ord(c)&31 for c in hrp]+values:
        top=check>>25;check=((check&0x1ffffff)<<5)^value
        for bit,gen in enumerate((0x3b6a57b2,0x26508e6d,0x1ea119fa,0x3d4233dd,0x2a1462b3)):
            if (top>>bit)&1:check^=gen
    assert check==1 and values[0]==0
    acc=bits=0; program=bytearray()
    for value in values[1:-6]:
        acc=(acc<<5)|value;bits+=5
        while bits>=8:
            bits-=8;program.append((acc>>bits)&255)
    assert bits<5 and ((acc<<(8-bits))&255)==0 and len(program)==20
    return b'\x00\x14'+bytes(program)

def map_read(reader):
    result={}
    while True:
        n=reader.cv()
        if n==0:return result
        key=reader.get(n);assert key not in result
        result[key]=reader.blob()

results=[]
for fixture in json.loads(FIXTURES.read_text()):
    spec=fixture['spec']; words=spec['mnemonic']; rows=spec['inputs'];outputs=spec['outputs']
    input_bytes=b'';expected_input_maps=[];root_fp=pkh(public(derive(words,[])))[:4]
    for row in rows:
        pub=public(derive(words,path(row)))
        prev=bytes.fromhex(row['txid'])[::-1]+le(row['vout'])
        input_bytes+=prev+b'\x00'+le(row['sequence'])
        witness=int(row['amountSats']).to_bytes(8,'little')+b'\x16\x00\x14'+pkh(pub)
        expected_input_maps.append({b'\x01':witness,b'\x06'+pub:root_fp+b''.join(le(i) for i in path(row))})
    output_bytes=b'';expected_output_maps=[]
    for row in outputs:
        dest=row['dest']; output_map={}
        if dest['kind']=='change':
            pub=public(derive(words,path(dest)));script=b'\x00\x14'+pkh(pub)
            output_map[b'\x02'+pub]=root_fp+b''.join(le(i) for i in path(dest))
        else:
            assert dest['kind']=='address';script=address_script(dest['address'])
        output_bytes+=int(row['amountSats']).to_bytes(8,'little')+compact(len(script))+script
        expected_output_maps.append(output_map)
    unsigned=le(2)+compact(len(rows))+input_bytes+compact(len(outputs))+output_bytes+le(spec['lockTime'])
    assert unsigned.hex()==fixture['publicTest']['unsignedTransactionHex']
    assert sum(int(x['amountSats']) for x in rows)>=sum(int(x['amountSats']) for x in outputs)
    for variant in fixture['variants']:
        ver,ins,outs,witnesses,locktime=parse(bytes.fromhex(variant['txHex']))
        rebuilt=ver+compact(len(ins))+b''.join(a+compact(len(b))+b+c for a,b,c in ins)+compact(len(outs))+b''.join(a+compact(len(b))+b for a,b in outs)+locktime
        assert rebuilt==unsigned
    for version in (0,2):
        r=Reader(bytes.fromhex(fixture['psbt'+str(version)])); assert r.get(5)==b'psbt\xff'
        if version==0:
            expected_global={b'\x00':unsigned}
            imaps=expected_input_maps;omaps=expected_output_maps
        else:
            expected_global={b'\xfb':le(2),b'\x02':le(2),b'\x04':compact(len(rows)),b'\x05':compact(len(outputs))}
            if spec['lockTime']:expected_global[b'\x03']=le(spec['lockTime'])
            imaps=[]
            for row,original in zip(rows,expected_input_maps):
                imaps.append({**original,b'\x0e':bytes.fromhex(row['txid'])[::-1],b'\x0f':le(row['vout']),b'\x10':le(row['sequence'])})
            omaps=[]
            for row,original,public_row in zip(outputs,expected_output_maps,fixture['publicTest']['outputs']):
                omaps.append({**original,b'\x03':int(row['amountSats']).to_bytes(8,'little'),b'\x04':bytes.fromhex(public_row['scriptHex'])})
        assert map_read(r)==expected_global
        assert [map_read(r) for _ in rows]==imaps
        assert [map_read(r) for _ in outputs]==omaps
        assert r.p==len(r.b)
        results.append({'scenario':fixture['scenario'],'status':'passed','inputs':len(rows),'outputs':len(outputs),'psbtVersion':version,'checks':'transaction bytes; destinations; values; input UTXO maps; input/output derivations; no extra PSBT bytes'})
report={'suite':'Independent Python transaction and PSBT structure checks','passed':len(results),'failed':0,'scope':'Six saved fixtures, both PSBT v0 and v2. No physical signer, no consensus/chain verification.','results':results}
OUTPUT.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
