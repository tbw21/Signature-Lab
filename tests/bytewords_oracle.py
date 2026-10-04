"""Test-only independent Bytewords/CBOR systematic-frame oracle.
Dictionary and published vector: Blockchain Commons BCR-2020-012.
https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-012-bytewords.md
CRC uses Python zlib, not the shipped JS. Does not implement fountain redundancy.
"""
import zlib, math, hashlib, json, sys
from pathlib import Path
WORDS='''able acid also apex aqua arch atom aunt
away axis back bald barn belt beta bias
blue body brag brew bulb buzz calm cash
cats chef city claw code cola cook cost
crux curl cusp cyan dark data days deli
dice diet door down draw drop drum dull
duty each easy echo edge epic even exam
exit eyes fact fair fern figs film fish
fizz flap flew flux foxy free frog fuel
fund gala game gear gems gift girl glow
good gray grim guru gush gyro half hang
hard hawk heat help high hill holy hope
horn huts iced idea idle inch inky into
iris iron item jade jazz join jolt jowl
judo jugs jump junk jury keep keno kept
keys kick kiln king kite kiwi knob lamb
lava lazy leaf legs liar limp lion list
logo loud love luau luck lung main many
math maze memo menu meow mild mint miss
monk nail navy need news next noon note
numb obey oboe omit onyx open oval owls
paid part peck play plus poem pool pose
puff puma purr quad quiz race ramp real
redo rich road rock roof ruby ruin runs
rust safe saga scar sets silk skew slot
soap solo song stub surf swan taco task
taxi tent tied time tiny toil tomb toys
trip tuna twin ugly undo unit urge user
vast very veto vial vibe view visa void
vows wall wand warm wasp wave waxy webs
what when whiz wolf work yank yawn yell
yoga yurt zaps zero zest zinc zone zoom'''.split()
PAIRS=[w[0]+w[-1] for w in WORDS];LOOKUP={p:i for i,p in enumerate(PAIRS)}
assert len(WORDS)==len(LOOKUP)==256

def encode(data):
    data=bytes(data);data+=zlib.crc32(data).to_bytes(4,'big')
    return ''.join(PAIRS[x] for x in data)

def decode(text):
    if len(text)%2 or len(text)<8:raise ValueError('encoding')
    data=bytes(LOOKUP[text[i:i+2].lower()] for i in range(0,len(text),2))
    if data[-4:]!=zlib.crc32(data[:-4]).to_bytes(4,'big'):raise ValueError('checksum')
    return data[:-4]

def cbor(n,major=0):
    if n<24:return bytes([major*32+n])
    for ai,size in [(24,1),(25,2),(26,4)]:
        if n<1<<(8*size):return bytes([major*32+ai])+n.to_bytes(size,'big')
    raise ValueError('integer too large')

def frames(payload,fragment_size=90,kind='crypto-psbt',force_multi=False):
    """First N systematic frames from standard UR framing. No runtime JS is used."""
    msg=cbor(len(payload),2)+payload
    if len(msg)<=fragment_size and not force_multi:return ['ur:'+kind+'/'+encode(msg)]
    count=math.ceil(len(msg)/fragment_size);size=math.ceil(len(msg)/count)
    crc=zlib.crc32(msg);out=[]
    for i in range(count):
        part=msg[i*size:(i+1)*size].ljust(size,b'\0')
        packed=b'\x85'+cbor(i+1)+cbor(count)+cbor(len(msg))+cbor(crc)+cbor(size,2)+part
        out.append(f'ur:{kind}/{i+1}-{count}/'+encode(packed))
    return out

def corrupt_frame(frame):
    parts=frame.split('/');body=parts[-1]
    # Substitute one data byte but deliberately retain the old Bytewords checksum.
    i=2 if len(body)>12 else 0
    before=body[i:i+2];after=PAIRS[(LOOKUP[before]+1)%256]
    parts[-1]=body[:i]+after+body[i+2:];return '/'.join(parts)

def fixtures():
    published_hex='d99d6ca20150c7098580125e2ab0981253468b2dbc5202c11947da'
    published_minimal='tantjzoeadgdstaslplabghydrpfmkbggufgludprfgmaosecffltnsoaawkbd'
    assert encode(bytes.fromhex(published_hex))==published_minimal
    assert decode(published_minimal).hex()==published_hex
    cases=[{'name':'published BCR vector','hex':published_hex,'minimal':published_minimal}]
    for n in [1,2,3,16,31,64,127,128,255,256,513,4096]:
        b=bytes((i*37+n)%256 for i in range(n));cases.append({'name':f'{n} bytes','hex':b.hex(),'minimal':encode(b)})
    for label,predicate in [('leading-zero CRC',lambda x:x<1<<24),('high-bit CRC',lambda x:x>=1<<31)]:
        for i in range(100000):
            b=b'crc-test'+i.to_bytes(4,'big')
            if predicate(zlib.crc32(b)):
                cases.append({'name':label,'hex':b.hex(),'minimal':encode(b)});break
        else:raise AssertionError(label)
    multipart=[]
    for kind in ['crypto-psbt','bytes','psbt']:
        for size in [1,24,90,255,512,2048]:
            payload=bytes((i*11+size)%256 for i in range(size));encoded=frames(payload,90,kind)
            multipart.append({'name':f'{kind}/{size}','hex':payload.hex(),'frames':encoded})
    return {'source':'BCR-2020-012 dictionary and vector; test-only Python zlib and explicit CBOR; no JavaScript codec',
            'bytewords':cases,'systematic':multipart}
if __name__=='__main__':
    data=fixtures()
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(data,indent=2))
    else:print(json.dumps(data))
