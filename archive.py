#!/usr/bin/env python3
"""Deterministic, atomic source archive. No overwrite, no symlinks, no network."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_STORED
import io,hashlib,sys
from build import atomic_create
EXCLUDE={'__pycache__','.DS_Store'}
def entries(root):
    out=[]
    for path in root.rglob('*'):
        if any(x in EXCLUDE for x in path.relative_to(root).parts) or path.suffix=='.pyc':continue
        if path.is_symlink():raise ValueError('Refusing symlink in source archive')
        if path.is_file():out.append(path)
    return sorted(out)
def archive_bytes(root,output):
    root,output=Path(root),Path(output)
    if output.exists():raise ValueError('Refusing to overwrite frozen/archive bytes: '+str(output))
    if output.resolve().is_relative_to(root.resolve()):raise ValueError('Archive output must be outside source directory')
    buffer=io.BytesIO()
    with ZipFile(buffer,'w',compression=ZIP_STORED) as z:
        for path in entries(root):
            info=ZipInfo(path.relative_to(root).as_posix(),(1980,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=ZIP_STORED
            z.writestr(info,path.read_bytes())
    data=buffer.getvalue();atomic_create(output,data);return hashlib.sha256(data).hexdigest()
if __name__=='__main__':
    try:
        if len(sys.argv)!=3:raise ValueError('Usage: python archive.py SOURCE_DIRECTORY NEW_ARCHIVE.zip')
        print(archive_bytes(sys.argv[1],sys.argv[2]))
    except Exception as exc:print('ARCHIVE FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
