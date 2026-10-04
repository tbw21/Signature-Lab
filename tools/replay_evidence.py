#!/usr/bin/env python3
"""Independent, public-only replay of Signature Lab evidence.
Checks public transaction binding, keys, amounts, BIP143 digests, strict low-S
SIGHASH_ALL ECDSA signatures, and consistency with recorded public references.
Does NOT authenticate the reference file, derive secret-key nonces, rerun the
metadata policies other than psbt-envelope-v3, attest hardware origin, or certify firmware.
Requires Python 3.10+ and cryptography with secp256k1 support. No network used.
"""
from pathlib import Path
import argparse, hashlib, json, struct, sys
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
LIMIT=524288
N=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
POLICIES={'compatible','plain','grind-core','grind-embit'}
def require(test,message):
    if not test: raise ValueError(message)
def sha(data): return hashlib.sha256(data).digest()
def dsha(data): return sha(sha(data))
def le(n): return struct.pack('<I',n)
def compact(n):
    require(isinstance(n,int) and 0<=n<=LIMIT,'Size outside replay bounds')
    if n<253:return bytes([n])
    return b'\xfd'+n.to_bytes(2,'little') if n<65536 else b'\xfe'+le(n)
def blob(data):return compact(len(data))+data
class Reader:
    def __init__(self,data):self.data=data;self.pos=0;require(len(data)<=LIMIT,'Payload too large')
    def get(self,n):
        require(isinstance(n,int) and 0<=n<=len(self.data)-self.pos,'Truncated payload')
        out=self.data[self.pos:self.pos+n];self.pos+=n;return out
    def compact(self, maximum=LIMIT):
        first=self.get(1)[0]
        if first<253:return first
        n=int.from_bytes(self.get({253:2,254:4,255:8}[first]),'little')
        require({253:253,254:65536,255:4294967296}[first]<=n<=maximum,'Noncanonical/oversized length')
        return n
    def blob(self):return self.get(self.compact())
    def finish(self):require(self.pos==len(self.data),'Trailing payload')
def fromhex(text):
    require(isinstance(text,str) and len(text)<=LIMIT*2 and len(text)%2==0,'Invalid hex')
    require(all(c in '0123456789abcdefABCDEF' for c in text),'Nonhex character')
    return bytes.fromhex(text)
def parse_tx(data):
    r=Reader(data);version=r.get(4);segwit=r.data[r.pos:r.pos+2]==b'\0\1'
    if segwit:r.get(2)
    count=r.compact();require(1<=count<=20,'Unsupported input count');inputs=[]
    for _ in range(count):inputs.append((r.get(36),r.blob(),r.get(4)))
    count=r.compact();require(1<=count<=20,'Unsupported output count');outputs=[]
    for _ in range(count):outputs.append((r.get(8),r.blob()))
    witnesses=[]
    if segwit:
        for _ in inputs:
            n=r.compact();require(n==2,'Expected one signature and key per input')
            witnesses.append([r.blob() for _ in range(n)])
    lock=r.get(4);r.finish();return version,inputs,outputs,witnesses,lock

def unsigned(tx):
    v,ins,outs,_,lock=tx
    return v+compact(len(ins))+b''.join(a+blob(b)+c for a,b,c in ins)+compact(len(outs))+b''.join(a+blob(b) for a,b in outs)+lock

def signed_bytes(tx):
    v,ins,outs,witnesses,lock=tx
    require(len(witnesses)==len(ins),'Missing signatures')
    return v+b'\0\1'+compact(len(ins))+b''.join(a+blob(b)+c for a,b,c in ins)+compact(len(outs))+b''.join(a+blob(b) for a,b in outs)+b''.join(compact(len(w))+b''.join(blob(x) for x in w) for w in witnesses)+lock

def maps(data):
    r=Reader(data);require(r.get(5)==b'psbt\xff','Missing PSBT header');out=[];fields=0
    while r.pos<len(data):
        require(len(out)<41,'Too many maps');row={}
        while True:
            key=r.blob()
            if not key:break
            fields+=1;require(fields<=4096 and key not in row,'Duplicate key or too many fields');row[key]=r.blob()
        out.append(row)
    return out

def psbt_tx(data,public_test,need_signed=True):
    rows=maps(data);count=len(public_test['inputs']);outcount=len(public_test['outputs'])
    require(len(rows)==1+count+outcount,'Incorrect map count');g=rows[0]
    version=int.from_bytes(g.get(b'\xfb',b'\0'*4),'little')
    require(version in (0,2),'Unsupported PSBT version')
    if version==0:
        require(b'\0' in g,'Missing unsigned transaction');tx=parse_tx(g[b'\0']);require(not tx[3],'Signed global transaction')
    else:
        def integer_field(key,expected):
            require(key in g,'Missing PSBT count');r=Reader(g[key]);actual=r.compact();r.finish();require(actual==expected,'Count mismatch')
        integer_field(b'\4',count);integer_field(b'\5',outcount)
        require(len(g.get(b'\2',b''))==4,'Missing version');lock=g.get(b'\3',b'\0'*4);require(len(lock)==4,'Invalid locktime')
        ins=[];outs=[]
        for row in rows[1:1+count]:
            require(len(row.get(b'\x0e',b''))==32 and len(row.get(b'\x0f',b''))==4,'Missing v2 input')
            sequence=row.get(b'\x10',b'\xff'*4);require(len(sequence)==4,'Invalid sequence')
            require(not any(k in row for k in [b'\x11',b'\x12']),'Required locktime fields outside replay scope')
            ins.append((row[b'\x0e']+row[b'\x0f'],b'',sequence))
        for row in rows[1+count:]:
            require(len(row.get(b'\3',b''))==8 and b'\4' in row,'Missing v2 output');outs.append((row[b'\3'],row[b'\4']))
        tx=(g[b'\2'],ins,outs,[],lock)
    require(len(tx[1])==count and len(tx[2])==outcount,'Transaction count mismatch')
    require(all(i[1]==b'' for i in tx[1]),'Unexpected input script')
    witnesses=[]
    for index,row in enumerate(rows[1:1+count]):
        p=public_test['inputs'][index];pub=fromhex(p['publicKeyHex']);sigkey=b'\2'+pub
        if b'\1' in row:
            r=Reader(row[b'\1']);amount=r.get(8);script=r.blob();r.finish()
            require(int.from_bytes(amount,'little')==int(p['amountSats']) and script==fromhex(p['previousScriptHex']),'Changed previous output')
        require(row.get(b'\3',le(1))==le(1),'Unsupported sighash')
        require(row.get(b'\7',b'')==b'','Unexpected final script')
        require(not any(k[:1] in [b'\4',b'\5'] or (k and 19<=k[0]<=24) for k in row),'Unsupported input scripts')
        partial=[(k[1:],v) for k,v in row.items() if k[:1]==b'\2']
        require(not partial or (len(partial)==1 and partial[0][0]==pub),'Wrong/extra partial signature key')
        if not need_signed:continue
        if b'\x08' in row:
            r=Reader(row[b'\x08']);n=r.compact();require(n==2,'Invalid final witness');w=[r.blob(),r.blob()];r.finish()
            if sigkey in row:require(row[sigkey]==w[0],'Conflicting signatures')
        else:require(sigkey in row,'Missing signature');w=[row[sigkey],pub]
        witnesses.append(w)
    return (tx[0],tx[1],tx[2],witnesses,tx[4])

def verify_signatures(tx,public_test):
    v,ins,outs,witnesses,lock=tx;require(v==le(public_test['version']) and lock==le(public_test['lockTime']),'Version/lock mismatch')
    require(len(ins)==len(public_test['inputs']) and len(outs)==len(public_test['outputs']),'Count mismatch')
    for (amount,script),expected in zip(outs,public_test['outputs']):
        require(int.from_bytes(amount,'little')==int(expected['amountSats']) and script==fromhex(expected['scriptHex']),'Output mismatch')
    require(len(witnesses)==len(ins),'Missing witnesses')
    hp=dsha(b''.join(i[0] for i in ins));hs=dsha(b''.join(i[2] for i in ins));ho=dsha(b''.join(a+blob(s) for a,s in outs))
    for index,(op,script,sequence) in enumerate(ins):
        source=public_test['inputs'][index];pub=fromhex(source['publicKeyHex']);w=witnesses[index]
        require(op==fromhex(source['txid'])[::-1]+le(source['vout']) and sequence==le(source['sequence']) and not script,'Input mismatch')
        require(len(pub)==33 and len(w)==2 and w[1]==pub,'Witness key mismatch')
        pkh=hashlib.new('ripemd160',sha(pub)).digest();require(fromhex(source['previousScriptHex'])==b'\0\x14'+pkh,'Previous script/key mismatch')
        script_code=b'\x76\xa9\x14'+pkh+b'\x88\xac';amount=int(source['amountSats']);require(600<=amount<=2100000000000000,'Invalid input amount')
        digest=dsha(v+hp+hs+op+blob(script_code)+amount.to_bytes(8,'little')+sequence+ho+lock+le(1))
        require(digest==fromhex(source['digestHex']),'Recorded digest mismatch')
        sig=w[0];require(len(sig)>=9 and sig[-1]==1,'Expected SIGHASH_ALL signature')
        r,s=utils.decode_dss_signature(sig[:-1]);require(0<r<N and 0<s<=N//2 and utils.encode_dss_signature(r,s)==sig[:-1],'Noncanonical/high-S signature')
        ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(),pub).verify(sig[:-1],digest,ec.ECDSA(utils.Prehashed(hashes.SHA256())))
    return len(ins)

# Independent reconstruction of the documented psbt-envelope-v3 policy. This code
# reads public raw PSBT maps; it does not import or execute the application's JavaScript.
METADATA_POLICY='psbt-envelope-v3'
METADATA_LIMITATION='Field values and positions are recorded, not every hidden-information channel. Relative order compares retained keys; added-field placement is preserved in positions but not classified as reordering. Ordering can change legitimately and does not prove leakage. Reduced responses may omit supporting fields. Choices of order or retained data can carry information to a recipient of the PSBT, not necessarily to the blockchain. Unknown fields are not automatically malicious.'
FIELD_NAMES={
 'global':{0:'unsignedTx',1:'xpub',2:'txVersion',3:'fallbackLocktime',4:'inputCount',5:'outputCount',6:'txModifiable',251:'version',252:'proprietary'},
 'input':{0:'nonWitnessUtxo',1:'witnessUtxo',2:'partialSig',3:'sighashType',4:'redeemScript',5:'witnessScript',6:'bip32Derivation',7:'finalScriptSig',8:'finalScriptWitness',9:'porCommitment',10:'ripemd160',11:'sha256',12:'hash160',13:'hash256',14:'txid',15:'index',16:'sequence',17:'requiredTimeLocktime',18:'requiredHeightLocktime',19:'tapKeySig',20:'tapScriptSig',21:'tapLeafScript',22:'tapBip32Derivation',23:'tapInternalKey',24:'tapMerkleRoot',252:'proprietary'},
 'output':{0:'redeemScript',1:'witnessScript',2:'bip32Derivation',3:'amount',4:'script',5:'tapInternalKey',6:'tapTree',7:'tapBip32Derivation',252:'proprietary'}}
def field_type(key):
    r=Reader(key);n=r.compact(maximum=2**53-1);return n,key[r.pos:]
def metadata_version(rows):
    v=rows[0].get(b'\xfb',b'\0'*4)
    require(v in (b'\0'*4,b'\2\0\0\0'),'Unsupported PSBT metadata version')
    return int.from_bytes(v,'little')
def metadata_conversion(prepared,p,target):
    """Recreate this generator's other-version unsigned PSBT from public data only.
    Refuse prepared envelopes outside the supported generator contract; never assume
    that arbitrary third-party PSBT conversion follows the Lab's ordering policy.
    """
    tx=parse_tx(fromhex(p['unsignedTransactionHex']));v,ins,outs,_,lock=tx;n=len(ins)
    if target==0:glob={b'\0':unsigned(tx)}
    else:
        glob={b'\2':v}
        if lock!=b'\0'*4:glob[b'\3']=lock
        glob.update({b'\4':compact(n),b'\5':compact(len(outs)),b'\xfb':le(2)})
    allow_global={0,2,3,4,5,251}
    require(all(field_type(k)[0] in allow_global and not field_type(k)[1] for k in prepared[0]),'Prepared global fields outside conversion replay scope')
    converted=[glob]
    for i,(op,script,seq) in enumerate(ins):
        original=prepared[i+1];pub=fromhex(p['inputs'][i]['publicKeyHex']);out={}
        require(set(original)<={b'\1',b'\6'+pub,b'\x0e',b'\x0f',b'\x10'},'Prepared input outside conversion replay scope')
        require(b'\1' in original and b'\6'+pub in original,'Missing prepared input support')
        out[b'\1']=original[b'\1'];out[b'\6'+pub]=original[b'\6'+pub]
        if target==2:out.update({b'\x0e':op[:32],b'\x0f':op[32:],b'\x10':seq})
        converted.append(out)
    for i,(amount,script) in enumerate(outs):
        original=prepared[1+n+i];out={}
        require(all(field_type(k)[0] in (2,3,4) for k in original),'Prepared output outside conversion replay scope')
        for k,val in original.items():
            if field_type(k)[0]==2:out[k]=val
        # Library orders derivations by key bytes within their field type.
        out=dict(sorted(out.items(),key=lambda x:x[0]))
        if target==2:out.update({b'\3':amount,b'\4':script})
        converted.append(out)
    return converted

def reduced_envelope(rows,inputs,version):
    allowed_global={0,251} if version==0 else {2,3,4,5,251}
    for key in rows[0]:
        typ,extra=field_type(key)
        if typ not in allowed_global or extra:return False
    shape=None
    for row in rows[1:1+inputs]:
        types=[(field_type(k)[0],field_type(k)[1],v) for k,v in row.items()]
        partial=sum(t==2 for t,k,v in types);final=sum(t==8 and not k for t,k,v in types)
        current='partial' if partial==1 and final==0 else 'final' if final==1 and partial==0 else None
        if not current or (shape is not None and shape!=current):return False
        shape=current
        for typ,extra,value in types:
            structural=version==2 and typ in (14,15,16) and not extra
            sighash=typ==3 and not extra and value==le(1)
            signature=current=='partial' and typ==2
            witness=current=='final' and not extra and (typ==8 or (typ==7 and value==b''))
            if not (structural or sighash or signature or witness):return False
    allowed_output=set() if version==0 else {3,4}
    return all(field_type(k)[0] in allowed_output and not field_type(k)[1] for row in rows[1+inputs:] for k in row)

def assess_metadata(public_test,artifact):
    if artifact['kind']=='tx':
        return {'policy':METADATA_POLICY,'status':'not-applicable','label':'No PSBT metadata',
                'unexpected':0,'unchanged':0,'expected':0,'fields':[], 'fieldOrderAssessed':False,
                'fieldOrderChanged':0,'fieldOrder':[], 'limitation':'The returned artifact is a raw transaction, not a PSBT.'}
    require(artifact['kind']=='psbt','Unsupported artifact type for metadata replay')
    original=maps(fromhex(public_test['psbtHex']));after=maps(fromhex(artifact['hex']))
    inputs=len(public_test['inputs']);outputs=len(public_test['outputs']);wanted=1+inputs+outputs
    require(len(original)==len(after)==wanted,'Metadata map count mismatch')
    requested=metadata_version(original);returned=metadata_version(after)
    require(public_test['psbtVersion']==requested,'Prepared PSBT version mismatch')
    converted=returned!=requested
    before=metadata_conversion(original,public_test,returned) if converted else original
    reduced=reduced_envelope(after,inputs,returned)
    records=[];ordering=[];unchanged=accepted=unexpected=removed_support=0
    for m,(old,new) in enumerate(zip(before,after)):
        scope='global' if m==0 else 'input' if m<=inputs else 'output'
        index=None if scope=='global' else m-1 if scope=='input' else m-inputs-1
        old_pos={k:i for i,k in enumerate(old)};new_pos={k:i for i,k in enumerate(new)}
        common_old=[k for k in old if k in new];common_new=[k for k in new if k in old]
        ordering.append({'scope':scope,'index':index,'beforeCount':len(old),'afterCount':len(new),
                         'comparedFields':len(common_old),'relativeOrderChanged':common_old!=common_new})
        for key in dict.fromkeys([*old,*new]):
            typ,extra=field_type(key);was=key in old;now=key in new;value=new[key] if now else old[key]
            removed=False
            if was and now and old[key]==new[key]:
                change='unchanged';classification='unchanged';reason='Preserved';unchanged+=1
            else:
                change='added' if not was else 'removed' if not now else 'changed'
                sign=scope=='input' and not was and now and (typ==2 or (typ==8 and not extra) or
                    (typ==7 and not extra and not value) or (typ==3 and not extra and value==le(1)))
                final=scope=='input' and b'\x08' in new and not now and typ in (3,6)
                removed=reduced and was and not now and (typ in (1,3,6) if scope=='input' else scope=='output' and typ==2)
                explicit=m==0 and key==b'\xfb' and now and value==le(0) and returned==0
                if sign or final or removed or explicit:
                    classification='expected';accepted+=1
                    reason='Signing data checked by the signature verifier' if sign else (
                        'Supporting field omitted from a complete signature-only response; checked using the original prepared test' if removed else
                        'Input signing metadata removed during finalization' if final else 'Explicit PSBT version zero')
                    removed_support+=int(bool(removed))
                else:classification='unexpected';reason='Not an expected signing or finalization change';unexpected+=1
            records.append({'scope':scope,'index':index,'field':FIELD_NAMES[scope].get(typ,f'unknown type {typ}'),
                'key':key.hex(),'type':typ,'change':change,'classification':classification,'reason':reason,
                'beforePosition':old_pos.get(key),'afterPosition':new_pos.get(key),
                'beforeSha256':sha(old[key]).hex() if was else None,'afterSha256':sha(new[key]).hex() if now else None,
                'beforeBytes':len(old[key]) if was else None,'afterBytes':len(new[key]) if now else None})
    return {'policy':METADATA_POLICY,'status':'unexpected' if unexpected else 'expected' if accepted or converted else 'unchanged',
            'label':'File changes need review' if unexpected else 'Reduced signing response' if removed_support else 'Only expected signing changes',
            'unexpected':unexpected,'unchanged':unchanged,'expected':accepted,'reducedResponse':bool(removed_support),
            'supportingFieldsRemoved':removed_support,'requestedVersion':requested,'returnedVersion':returned,
            'versionConversion':converted,'fields':records,'fieldOrderAssessed':True,
            'fieldOrderChanged':sum(x['relativeOrderChanged'] for x in ordering),'fieldOrder':ordering,
            'fieldOrderBasis':'same-version-local-reconstruction' if converted else 'original-prepared-psbt',
            'limitation':METADATA_LIMITATION}

def verify_metadata(evidence):
    report=evidence['report'];recorded=report.get('metadata')
    require(isinstance(recorded,dict) and recorded.get('policy')==METADATA_POLICY,'Unsupported metadata policy; no replay approval')
    actual=assess_metadata(evidence['publicTest'],evidence['returnedArtifact'])
    require(recorded==actual,'Metadata policy findings differ from original bytes')
    require(evidence['analysis'].get('metadata')==actual,'Analysis/report metadata disagree')
    overall='review' if report['result']=='match' and actual['status']=='unexpected' else report['result']
    require(report.get('overallStatus')==overall,'Overall status disagrees with metadata/signature finding')
    return {'policy':METADATA_POLICY,'status':actual['status'],'fieldOrderChanged':actual['fieldOrderChanged'],
            'fieldsVerified':len(actual['fields']),'overallStatus':overall,'result':'reproduced-from-public-bytes'}

def replay_bundle(bundle):
    require(bundle.get('schema')=='tbw-session-evidence-v1','Unsupported session-evidence schema')
    history=bundle['history'];coverage=bundle['coverage'];events=bundle['events'];rows=history['events']
    require(history['schema']=='tbw-session-history-v1','Unsupported history schema')
    require(history['summary']['countPolicy']=='distinct-transaction-worst-observed-v2','Unsupported session count policy')
    require(bundle['build']==history['build'] and bundle['walletSession']==history['walletSession'],'Bundle identity differs from history')
    require(isinstance(events,list) and len(events)==len(rows)<=2256,'Missing or excessive history entries')
    details=[];retained=bytecount=checks=captures=0;worst={}
    rank={'matched':0,'review':1,'differed':2}
    for index,(slot,row) in enumerate(zip(events,rows),1):
        require(slot['index']==row['index']==index,'Reordered, duplicate or missing journal index')
        require(slot['type']==row['type'] and slot.get('test')==row.get('test'),'Journal attachment binding differs')
        if row['type']=='capture-attempt':captures+=1
        if row['type']!='check':
            require('evidenceJson' not in slot,'Non-result event has an evidence attachment');continue
        checks+=1
        require(type(row.get('completed')) is bool,'Invalid completed flag')
        if row['completed']:
            require(row.get('result') in ('match','mismatch'),'Unsupported completed outcome')
            outcome='differed' if row['result']!='match' else 'matched' if row.get('metadataStatus') in ['expected','unchanged','not-applicable'] else 'review'
            txid=row['transactionId'];require(isinstance(txid,str) and len(txid)==64 and all(c in '0123456789abcdef' for c in txid),'Missing completed transaction identity')
            if txid not in worst or rank[outcome]>rank[worst[txid]]:worst[txid]=outcome
        if slot['retention']!='retained':
            require('evidenceJson' not in slot and slot['retention'] in ['not-enabled','no-complete-response-evidence','byte-limit','payload-limit','retention-error'],'Invalid missing-evidence declaration')
            details.append({'index':index,'status':'missing-evidence','reason':slot['retention']});continue
        text=slot['evidenceJson'];require(isinstance(text,str),'Evidence JSON must be text')
        raw=text.encode('utf-8');bytecount+=len(raw);retained+=1
        require(len(raw)==slot['bytes'] and sha(raw).hex()==slot['sha256'],'Retained evidence hash/length mismatch')
        require(bytecount<=16*1024*1024 and retained<=256,'Retention limits exceeded')
        e=json.loads(text);r=e['report']
        require(r['walletSession']==bundle['walletSession'] and r['build']==bundle['build'],'Response belongs to another build/wallet')
        for key in ['test','createdAt','result','completed']:
            require(r[key]==row[key],'Response summary binding mismatch: '+key)
        require((r.get('metadata') or {}).get('status')==row.get('metadataStatus'),'Metadata summary binding mismatch')
        ev=r.get('evidence') or {}
        require(ev.get('artifactSha256')==row.get('artifactSha256') and ev.get('transactionId')==row.get('transactionId'),'Response hash/txid differs from history')
        if r['completed']:details.append({'index':index,'status':'replayed','finding':replay(e)})
        else:details.append({'index':index,'status':'retained-incomplete-not-cryptographically-replayed'})
    require(coverage['checks']==checks and coverage['retained']==retained and coverage['missing']==checks-retained and coverage['bytes']==bytecount,'Evidence completeness claim differs from attachments')
    require(coverage['allRecordedChecksRetained']==bool(checks and checks==retained),'False complete-evidence claim')
    require(coverage['captures']==captures and captures<=256,'Capture coverage mismatch')
    summary=history['summary'];require(summary['checked']==len(worst),'Distinct transaction count differs')
    for name in rank:require(summary[name]==list(worst.values()).count(name),'Worst-observed outcome count differs: '+name)
    return {'status':'consistent-session-evidence','recordedChecks':checks,'retained':retained,'missing':checks-retained,
            'replayed':sum(d['status']=='replayed' for d in details),'entries':details,
            'notEstablished':['complete history beyond supplied bundle','all requested physical operations','publisher/reference authenticity','hardware origin','firmware safety']}


def replay(evidence):
    require(evidence.get('schema')=='tbw-signature-evidence-v1','Unsupported evidence schema')
    report=evidence['report'];require(report['result'] in ['match','mismatch'],'Only completed results are replayable automatically')
    require(report.get('completed') is True and evidence['analysis'].get('ok') is True,'Incomplete result is not a completed replay')
    p=evidence['publicTest'];references=p.get('references')
    require(isinstance(references,list) and 1<=len(references)<=3,'Reference count outside replay scope')
    method_ids=[]
    for reference in references:
        ids=reference.get('ids');require(isinstance(ids,list) and 1<=len(ids)<=3 and all(isinstance(x,str) for x in ids),'Invalid reference identifiers')
        method_ids+=ids
    require(len(method_ids)==3 and set(method_ids)==POLICIES-{'compatible'},'Missing, duplicate or unsupported reference method')
    artifact=evidence['returnedArtifact'];raw=fromhex(artifact['hex'])
    require(sha(raw).hex()==artifact['sha256']==report['evidence']['artifactSha256'],'Artifact hash mismatch')
    prepared=psbt_tx(fromhex(p['psbtHex']),p,False)
    tx=psbt_tx(raw,p) if artifact['kind']=='psbt' else parse_tx(raw)
    require(artifact['kind'] in ('psbt','tx') and artifact['kind']==report['evidence']['artifactKind'],'Artifact kind mismatch')
    expected_unsigned=fromhex(p['unsignedTransactionHex'])
    require(unsigned(tx)==unsigned(prepared)==expected_unsigned,'Unsigned transaction binding failed')
    count=verify_signatures(tx,p);final=signed_bytes(tx).hex()
    require(final==evidence['analysis']['txHex'],'Recorded signed transaction mismatch')
    require(dsha(expected_unsigned)[::-1].hex()==report['evidence']['transactionId'],'Transaction ID mismatch')
    require(count==report['evidence']['signaturesVerified'],'Signature count mismatch')
    policy=report['signingPolicy'];require(policy['version']=='deterministic-ecdsa-v1' and policy['id'] in POLICIES,'Unknown policy')
    matching=[]
    for reference in p['references']:
        require(set(reference['ids'])<=POLICIES-{'compatible'},'Unknown reference method')
        verify_signatures(parse_tx(fromhex(reference['txHex'])),p)
        if reference['txHex']==final and (policy['id']=='compatible' or policy['id'] in reference['ids']):matching+=reference['ids']
    require(bool(matching)==(report['result']=='match'),'Reported comparison does not agree with public references')
    require(set(matching)==set(report['matchedAlgorithms']),'Matched algorithm labels differ')
    metadata=verify_metadata(evidence)
    return {'metadataReplay':metadata,'status':'consistent-public-evidence','signaturesVerified':count,'result':report['result'],
            'signingPolicy':policy['id'],'artifactSha256':artifact['sha256'],'build':report['build'],
            'notEstablished':['publisher/reference authenticity','secret-key-derived nonce reproduction','hardware origin','firmware safety']}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('evidence',type=Path);ap.add_argument('--output',type=Path);args=ap.parse_args()
    require(args.evidence.stat().st_size<=32*1024*1024,'Evidence JSON too large')
    data=json.loads(args.evidence.read_text());result=replay_bundle(data) if data.get('schema')=='tbw-session-evidence-v1' else replay(data);text=json.dumps(result,indent=2)
    if args.output:
        with args.output.open('x') as f:f.write(text+'\n')
    print(text)
if __name__=='__main__':
    try:main()
    except Exception as exc:print('EVIDENCE CHECK FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
