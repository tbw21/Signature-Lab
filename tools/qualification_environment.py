#!/usr/bin/env python3
"""Read-only prerequisite inspection. Never installs, patches, retries, or tests a signer."""
from pathlib import Path
import argparse, importlib, importlib.metadata, json, os, platform, re, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
MODULES={'beautifulsoup4':'bs4','Pillow':'PIL','playwright':'playwright.sync_api',
         'pyzbar':'pyzbar.pyzbar','cryptography':'cryptography.hazmat.primitives.asymmetric.ec',
         'typing_extensions':'typing_extensions','pyee':'pyee','greenlet':'greenlet',
         'soupsieve':'soupsieve','cffi':'cffi','pycparser':'pycparser','qrcode':'qrcode'}
def inspect_environment(requirements=ROOT/'qualification-requirements.txt', version=importlib.metadata.version,
                        importer=importlib.import_module, which=shutil.which, run=subprocess.run):
    records=[]; blockers=[]
    for line in Path(requirements).read_text().splitlines():
        line=line.strip()
        if not line or line.startswith('#'):continue
        match=re.fullmatch(r'([A-Za-z0-9_-]+)==([A-Za-z0-9_.+-]+)',line)
        if not match:raise ValueError('Every qualification requirement must have an exact version')
        name,wanted=match.groups();row={'package':name,'required':wanted}
        try:
            actual=version(name);row['installed']=actual
            if actual!=wanted:raise ValueError('Version differs from the qualified environment pin')
            importer(MODULES.get(name,name));row['status']='available'
        except Exception as exc:
            row.update(status='unavailable-environment',reason=str(exc));blockers.append(name)
        records.append(row)
    tools=[]
    for name,args in [('python',['--version']),('node',['--version']),('openssl',['version']),('chromium',['--version'])]:
        binary=which(name);row={'tool':name,'path':binary}
        try:
            if not binary:raise FileNotFoundError(name+' executable not found')
            result=run([binary,*args],capture_output=True,text=True,timeout=10,check=True)
            row.update(status='available',version=(result.stdout or result.stderr).strip())
            if name=='chromium' and not Path('/usr/bin/chromium').exists():raise FileNotFoundError('Retained browser harness requires /usr/bin/chromium')
        except Exception as exc:row.update(status='unavailable-environment',reason=str(exc));blockers.append(name)
        tools.append(row)
    return {'schema':'tbw-qualification-environment-v1','complete':True,
        'status':'ready' if not blockers else 'unavailable-environment','candidateFailure':False,
        'python':sys.version,'platform':platform.platform(),'packages':records,'tools':tools,'blockers':blockers,
        'scope':'Tool prerequisites only. Not candidate behavior, native browser or hardware acceptance.'}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path)
    args=parser.parse_args();result=inspect_environment()
    with args.output.open('x') as file:json.dump(result,file,indent=2)
    print(json.dumps(result,indent=2));return 0 if result['status']=='ready' else 3
if __name__=='__main__':raise SystemExit(main())
