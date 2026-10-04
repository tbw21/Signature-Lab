#!/usr/bin/env python3
"""Clean extraction, deterministic reconstruction and filesystem failure contracts."""
from pathlib import Path
from zipfile import ZipFile,BadZipFile
import tempfile,subprocess,hashlib,json,sys,os,shutil,errno
ROOT=Path(__file__).resolve().parents[1];HTML=Path(sys.argv[1]);ZIP=Path(sys.argv[2]);OUT=Path(sys.argv[3]);results=[]
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(condition,message='assertion failed'):
    if not condition:raise AssertionError(message)
def test(name,fn):
    try:fn();results.append({'name':name,'status':'passed'})
    except Exception as e:results.append({'name':name,'status':'failed','error':repr(e)})
def run(root,*args,**kwargs):return subprocess.run([sys.executable,*map(str,args)],cwd=root,env=env,capture_output=True,text=True,timeout=30,**kwargs)
with tempfile.TemporaryDirectory(prefix='tbw-qualification-') as directory:
    work=Path(directory);extract=work/'clean';extract.mkdir()
    with ZipFile(ZIP) as z:
        def paths():
            names=z.namelist();check(len(names)==len(set(names)))
            for info in z.infolist():
                p=Path(info.filename);check(not p.is_absolute() and '..' not in p.parts);check((info.external_attr>>16)&0o170000==0o100000)
        paths()  # Never extract a candidate with unsafe paths, even if the test report would record failure.
        test('archive paths unique, relative and regular files only',paths)
        test('all ZIP CRCs verify',lambda:check(z.testzip() is None))
        z.extractall(extract)
    def manifest():
        listed={line.split('  ',1)[1]:line.split('  ',1)[0] for line in (extract/'MANIFEST.sha256').read_text().splitlines()}
        actual={p.relative_to(extract).as_posix():sha(p) for p in extract.rglob('*') if p.is_file() and p.relative_to(extract).as_posix()!='MANIFEST.sha256'}
        check(actual==listed,'Extra/missing/changed archive file')
    test('clean extraction matches every internal manifest entry',manifest)
    def buildtwice():
        for i in range(2):
            output=work/f'build{i}.html';r=run(extract,'build.py',output);check(r.returncode==0,r.stderr);check(output.read_bytes()==HTML.read_bytes())
    test('two offline builds from clean source recreate exact candidate HTML',buildtwice)
    def repack():
        out=work/'repacked.zip';r=run(extract,'archive.py',extract,out);check(r.returncode==0,r.stderr);check(out.read_bytes()==ZIP.read_bytes())
    test('deterministic repack reproduces the exact candidate ZIP',repack)
    def nooverwrite():
        target=work/'existing.html';target.write_text('preserve me');r=run(extract,'build.py',target);check(r.returncode!=0);check(target.read_text()=='preserve me')
    test('existing output is never overwritten',nooverwrite)
    def concurrent():
        target=work/'concurrent.html';command=[sys.executable,str(extract/'build.py'),str(target)]
        a=subprocess.Popen(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b=subprocess.Popen(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        a.communicate(timeout=30);b.communicate(timeout=30);check(sorted([a.returncode,b.returncode])==[0,1]);check(target.read_bytes()==HTML.read_bytes());check(not list(work.glob('.concurrent.html.*')))
    test('concurrent builders produce one complete output and one explicit failure',concurrent)
    def tamper():
        root=work/'tampered';shutil.copytree(extract,root);p=root/'src/20-application.js';p.write_text(p.read_text()+'\n//tampered\n');r=run(root,'build.py',work/'tampered.html');check(r.returncode!=0 and 'lock mismatch' in r.stderr);check(not (work/'tampered.html').exists())
    test('altered source cannot build with the frozen lock',tamper)
    def symlink():
        root=work/'symlink';shutil.copytree(extract,root);p=root/'src/20-application.js';p.unlink();p.symlink_to(extract/'src/20-application.js');r=run(root,'build.py',work/'linked.html');check(r.returncode!=0);r=run(root,'archive.py',root,work/'linked.zip');check(r.returncode!=0);check(not (work/'linked.zip').exists())
    test('symlink build and archive inputs are rejected',symlink)
    def truncated():
        p=work/'cut.zip';p.write_bytes(ZIP.read_bytes()[:len(ZIP.read_bytes())//2]);
        try:ZipFile(p).testzip()
        except BadZipFile:return
        raise AssertionError('Truncated archive accepted')
    test('truncated archive is rejected',truncated)
    def diskfull():
        code="import build,os,errno;\n"+"def fail(*a):raise OSError(errno.ENOSPC,'injected full disk')\n"+"build.os.fsync=fail\n"+f"build.atomic_create({str(work/'full.html')!r},b'payload')"
        r=run(extract,'-c',code);check(r.returncode!=0 and 'full disk' in r.stderr);check(not (work/'full.html').exists());check(not list(work.glob('.full.html.*')))
    test('ENOSPC at fsync boundary leaves no published or partial output (injected)',diskfull)
    def readonly():
        work.chmod(0o755);extract.chmod(0o755);out=work/'readonly';out.mkdir();out.chmod(0o555)
        code=f"import sys;sys.path.insert(0,{str(extract)!r});import build;build.atomic_create({str(out/'app.html')!r},b'test')"
        def drop():os.setgroups([]);os.setgid(65534);os.setuid(65534)
        r=run(extract,'-c',code,preexec_fn=drop if os.geteuid()==0 else None);check(r.returncode!=0);check(not (out/'app.html').exists())
    test('unprivileged write to real read-only directory fails without publication (not read-only mount)',readonly)
    def interruption():
        target=work/'interrupted.html';code=f"import build,os;build.os.link=lambda *a:os._exit(23);build.atomic_create({str(target)!r},b'partial')"
        r=run(extract,'-c',code);check(r.returncode==23);check(not target.exists());orphans=list(work.glob('.interrupted.html.*'));check(bool(orphans))
        r=run(extract,'build.py',target);check(r.returncode==0,r.stderr);check(target.read_bytes()==HTML.read_bytes())
    test('abrupt builder exit before publish leaves output absent; explicit second run succeeds (not power loss)',interruption)
    def baseline_free():
        root=work/'runtime-source-only';shutil.copytree(extract,root)
        for name in ['baseline','fixtures','tests','docs','tools']:
            shutil.rmtree(root/name,ignore_errors=True)
        target=work/'without-baseline.html';r=run(root,'build.py',target);check(r.returncode==0,r.stderr);check(target.read_bytes()==HTML.read_bytes())
    test('source assembly rebuilds identically after all previous-HTML/test fixtures are removed',baseline_free)
    test('qualification did not modify clean-extracted manifest files',manifest)
result={'suite':'Archive/reconstruction/filesystem qualification','sha256':sha(HTML),'archiveSha256':sha(ZIP),'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'results':results};OUT.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));sys.exit(1 if result['failed'] else 0)
