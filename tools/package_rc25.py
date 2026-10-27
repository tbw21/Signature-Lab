"""Create reproducible RC25 development handoff. Run before candidate freeze only."""
from pathlib import Path
import hashlib, json, zipfile, shutil, tempfile, subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=Path('/mnt/data')
NAME='TBW-Signature-Lab-v0.20.12-rc25'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
art=OUT/(NAME+'.html')
source=OUT/(NAME+'-source.zip')
outer=OUT/(NAME+'-UI-PREVIEW-Handoff.zip')
qual=OUT/(NAME+'-QUALIFICATION-RECEIPT.json')
receipt=json.loads((ROOT/'RC25-SEEDQR-BROWSER-RECEIPT.json').read_text())
assert receipt['passed']==8 and receipt['failed']==0
assert art.exists()
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.is_symlink():continue
    relative=p.relative_to(ROOT)
    if any(seg in {'__pycache__','.git','.pytest_cache'} for seg in relative.parts):continue
    if p.suffix in {'.pyc','.png'}:continue
    if str(relative).startswith('rc24-'):continue
    if relative.name.startswith('probe-'):continue
    files.append((relative.as_posix(),p))
assert 'src/style.css' in [k for k,_ in files]
manifest=''.join(f'{sha(p)}  {name}\n' for name,p in files).encode()
def add(z,name,data):
    info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_STORED;info.external_attr=0o100644<<16
    z.writestr(info,data)
with zipfile.ZipFile(source,'w') as z:
    for name,path in files:add(z,name,path.read_bytes())
    add(z,'SOURCE-SHA256SUMS.txt',manifest)
qualification={
 'version':'0.20.12-rc25','grade':'DEVELOPMENT_UI_PREVIEW_PUBLIC_RELEASE_BLOCKED',
 'browser_scope':'real standalone application inserted as document via Playwright/Chromium; not native file://',
 'browser_cases_passed':8,'browser_cases_failed':0,'javascript_modules_unchanged':29,'javascript_syntax_passed':29,
 'css_parse':'PASS','fault_source_tamper':'PASS','fault_no_overwrite':'PASS',
 'core_logic_changes':0,'hardware_acceptance':'NOT_RUN','native_file_origin':'BLOCKED_BY_POLICY_NOT_RUN',
 'historical_suite':'NOT_RUN','publisher_authenticated':False,
 'source_zip_sha256':sha(source),'standalone_sha256':sha(art),
 'baseline':'v0.20.12-rc24 unchanged'
}
qual.write_text(json.dumps(qualification,indent=2,sort_keys=True)+'\n')
readme=(
 '# Signature Lab v0.20.12-rc25 — scoped SeedQR enlarge repair\n\n'
 'Open the standalone HTML locally to review. The existing SeedQR button now opens a centered, enlarged QR and collapses with Reduce, Escape, or outside click. QR canvas content is unchanged. No Bitcoin, signer, or QR-generation logic changed.\n\n'
 'This is a development UI preview, not a signed or fully qualified release. Read the qualification receipt and docs/rc25 in the source zip. RC24 is the unchanged rollback baseline.\n'
).encode()
checks=''.join(f'{sha(p)}  {n}\n' for n,p in [('standalone.html',art),('source.zip',source),('qualification.json',qual)]).encode()
with zipfile.ZipFile(outer,'w') as z:
    add(z,NAME+'.html',art.read_bytes())
    add(z,NAME+'-source.zip',source.read_bytes())
    add(z,'RC25-QUALIFICATION-RECEIPT.json',qual.read_bytes())
    add(z,'RC25-SEEDQR-BROWSER-RECEIPT.json',(ROOT/'RC25-SEEDQR-BROWSER-RECEIPT.json').read_bytes())
    add(z,'README.md',readme)
    add(z,'SHA256SUMS.txt',checks)
# Independent extraction, rebuild and both ZIP CRCs
with tempfile.TemporaryDirectory(prefix='rc25-extract-') as td:
    d=Path(td)
    with zipfile.ZipFile(outer) as z:
        assert z.testzip() is None
        z.extractall(d)
    q=d/'source'
    with zipfile.ZipFile(d/(NAME+'-source.zip')) as z:
        assert z.testzip() is None
        z.extractall(q)
    for line in (q/'SOURCE-SHA256SUMS.txt').read_text().splitlines():
        h,f=line.split('  ',1);assert sha(q/f)==h,f
    subprocess.run(['python',str(q/'build.py'),str(d/'rebuilt.html')],check=True,stdout=subprocess.PIPE,timeout=30)
    assert (d/'rebuilt.html').read_bytes()==art.read_bytes()
    # Repack separately from a clean extraction.
    repack=d/'repack-source.zip'
    with zipfile.ZipFile(repack,'w') as z:
        for name,_ in files:add(z,name,(q/name).read_bytes())
        add(z,'SOURCE-SHA256SUMS.txt',(q/'SOURCE-SHA256SUMS.txt').read_bytes())
    assert repack.read_bytes()==source.read_bytes()
    repack2=d/'repack-outer.zip'
    with zipfile.ZipFile(repack2,'w') as z:
        for name in [NAME+'.html',NAME+'-source.zip','RC25-QUALIFICATION-RECEIPT.json','RC25-SEEDQR-BROWSER-RECEIPT.json','README.md','SHA256SUMS.txt']:
            add(z,name,(d/name).read_bytes())
    assert repack2.read_bytes()==outer.read_bytes()
print(json.dumps({'source_files':len(files),'outer_sha256':sha(outer),'outer_bytes':outer.stat().st_size,'html_sha256':sha(art),'manifest_entries':len(files),'clean_extraction':'PASS','source_and_outer_reproducible':True}))
