#!/usr/bin/env python3
"""Independent transport oracle using CPython base64 and native zlib.
This is a local specification-based oracle, not Coinkite's upstream test suite.
JSON stdin/stdout; no network and no wallet operations.
"""
import base64
import json
import sys
import zlib


def encode(raw, kind='P', encoding='Z', chunk_bytes=75, packed=None):
    if encoding == 'Z' and packed is None:
        z = zlib.compressobj(level=9, wbits=-10)
        packed = z.compress(raw) + z.flush()
    if packed is None:
        packed = raw
    if encoding != 'H':
        chunk_bytes = max(5, chunk_bytes // 5 * 5)
    chunks = [packed[i:i+chunk_bytes] for i in range(0, len(packed), chunk_bytes)]
    def b36(n):
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return chars[n // 36] + chars[n % 36]
    return ['B$'+encoding+kind+b36(len(chunks))+b36(i) +
            (part.hex().upper() if encoding == 'H' else
             base64.b32encode(part).decode().rstrip('=')) for i,part in enumerate(chunks)]


def decode(frames):
    assert frames and len({x[:6] for x in frames}) == 1
    header=frames[0][:6]; count=int(header[4:6],36)
    parts = {}
    for frame in frames:
        i=int(frame[6:8],36)
        assert i < count
        assert i not in parts or parts[i] == frame[8:]
        parts[i]=frame[8:]
    assert set(parts) == set(range(count))
    data=[]
    for i in range(count):
        text=parts[i]
        data.append(bytes.fromhex(text) if header[2]=='H' else
                    base64.b32decode(text+'='*((-len(text))%8)))
    packed=b''.join(data)
    if header[2]=='Z':
        z=zlib.decompressobj(wbits=-10)
        raw=z.decompress(packed)+z.flush()
        assert z.eof and not z.unused_data and not z.unconsumed_tail
    else:
        raw=packed
    return {'type':header[3], 'base64':base64.b64encode(raw).decode()}


def process(query):
    if query['op']=='decode': return decode(query['frames'])
    raw=base64.b64decode(query.get('base64',''))
    packed=base64.b64decode(query['packedBase64']) if 'packedBase64' in query else None
    return {'frames':encode(raw,query.get('type','P'),query.get('encoding','Z'),query.get('chunkBytes',75),packed)}

if __name__=='__main__':
    query=json.load(sys.stdin)
    print(json.dumps([process(x) for x in query] if isinstance(query,list) else process(query)))
