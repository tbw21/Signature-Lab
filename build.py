#!/usr/bin/env python3
"""Single offline source-to-HTML build. No baseline HTML and no network required.
The explicit source lock is checked before reading inputs. Output is never overwritten.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, sys, tempfile
from html import escape
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent
LOCK='source-lock.json'

def sha(data): return hashlib.sha256(data).hexdigest()
def inputs():
    order=json.loads((ROOT/'sources.json').read_text())
    if len(order)!=len(set(order)): raise ValueError('Duplicate source unit')
    paths=['build.py','sources.json','release.json','src/page.html','src/style.css',*order,
           'vendor/pako-1.0.11.min.js','vendor/pako-LICENSE.txt','vendor/pako-zlib-NOTICE.txt']
    for name in paths:
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or not (ROOT/p).is_file() or (ROOT/p).is_symlink():
            raise ValueError('Invalid source path: '+name)
    return paths,order

def manifest(): return {name:sha((ROOT/name).read_bytes()) for name in sorted(inputs()[0])}
def locked():
    expected=json.loads((ROOT/LOCK).read_text())
    actual=manifest()
    if expected != actual: raise ValueError('Source lock mismatch. Refusing changed or missing build inputs.')
    return actual


HELP_GROUPS = ('Start here', 'Understand a result', 'Scan & transfer', 'Repeat & customize', 'Method & trust')

def help_contents(template):
    """Pure presentation projection: canonical FAQ ids/titles/groups live in page.html.
    Malformed editorial input stops the build; never invent a missing target or render HTML
    found inside a heading. No new runtime dependency or navigation controller is involved.
    """
    class Questions(HTMLParser):
        VOID = frozenset(('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'))
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack=[]; self.items=[]; self.ids=set(); self.current=None; self.summary=False
        def handle_starttag(self, tag, attrs):
            a=dict(attrs)
            if a.get('id'):
                if a['id'] in self.ids: raise ValueError('Duplicate page id: '+a['id'])
                self.ids.add(a['id'])
            parent=self.stack[-1] if self.stack else None
            if tag=='details' and parent and parent[1].get('id')=='help':
                key=a.get('id',''); group=a.get('data-help-group','')
                if not re.fullmatch(r'[a-z][a-z0-9-]*',key): raise ValueError('Every FAQ requires a stable id')
                if group not in HELP_GROUPS: raise ValueError('Every FAQ requires a recognized contents group')
                self.current={'id':key,'group':group,'title':'','summaries':0}
                self.items.append(self.current)
            if tag=='summary' and self.current and parent and parent[1].get('id')==self.current['id']:
                self.summary=True; self.current['summaries']+=1
            if tag not in self.VOID:self.stack.append((tag,a))
        def handle_endtag(self,tag):
            if tag=='summary':self.summary=False
            if not self.stack:return
            if self.stack[-1][0]!=tag: raise ValueError('Unbalanced help template element: '+tag)
            _,attrs=self.stack.pop()
            if self.current and tag=='details' and attrs.get('id')==self.current['id']:self.current=None
        def handle_startendtag(self,tag,attrs):
            self.handle_starttag(tag,attrs)
            if tag not in self.VOID:self.handle_endtag(tag)
        def handle_data(self,data):
            if self.summary and self.current:self.current['title']+=data
    parser=Questions();parser.feed(template);parser.close()
    if parser.stack:raise ValueError('Unclosed template element')
    if not parser.items: raise ValueError('Help contains no questions')
    groups={g:[] for g in HELP_GROUPS}
    for item in parser.items:
        title=' '.join(item['title'].split())
        if not title or item['summaries']!=1:raise ValueError('Every FAQ requires one nonempty summary')
        groups[item['group']].append((item['id'],title))
    sections=[]
    for group,items in groups.items():
        if not items:raise ValueError('Empty help contents group: '+group)
        links=''.join('<li><a href="#'+escape(key,quote=True)+'" data-faq-link="">'+escape(title)+'</a></li>' for key,title in items)
        sections.append('<details class="help-topic"><summary>'+escape(group)+'</summary><ul>'+links+'</ul></details>')
    return '<nav class="help-contents" aria-labelledby="help-contents-title"><h3 id="help-contents-title">Contents</h3><div class="help-contents-grid">'+''.join(sections)+'</div></nav>'

def assemble():
    hashes=locked();identity=sha(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode())
    version=json.loads((ROOT/'release.json').read_text())['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-(?:dev|rc\d+))?',version): raise ValueError('Invalid release version')
    chunks=['const TBW_BUILD = Object.freeze('+json.dumps({'version':version,'sourceSha256':identity,'publisherAuthenticated':False},separators=(',',':'))+');\n']
    for name in inputs()[1]:
        text=(ROOT/name).read_text()
        if name=='src/11-bbqr.js':chunks.append('/* TBW_BBQR_CODEC_BEGIN */\n')
        if name=='vendor/12-compression.js':
            notices='/*\n'+(ROOT/'vendor/pako-LICENSE.txt').read_text()+'\n'+(ROOT/'vendor/pako-zlib-NOTICE.txt').read_text()+'\n*/'
            text=text.replace('/*@@PAKO_NOTICES@@*/',notices).replace('/*@@PAKO_BYTES@@*/',(ROOT/'vendor/pako-1.0.11.min.js').read_text())
        if name=='src/22-bootstrap.js': chunks.append('/* TBW_BOOTSTRAP_BEGIN */\n')
        chunks.append(text+'\n')
        if name=='vendor/12-compression.js':chunks.append('/* TBW_BBQR_CODEC_END */\n')
    script='\n'.join(chunks)
    if re.search('</script',script,re.I): raise ValueError('Unsafe closing script text')
    html=(ROOT/'src/page.html').read_text()
    for marker in ['@@SCRIPT@@','@@STYLE@@','@@HELP_CONTENTS@@']:
        if html.count(marker)!=1: raise ValueError('Template marker count')
    html=html.replace('@@HELP_CONTENTS@@',help_contents(html))
    html=html.replace('@@SCRIPT@@',script).replace('@@STYLE@@',(ROOT/'src/style.css').read_text()).replace('@@VERSION@@',version)
    if '@@' in html and re.search(r'@@[A-Z_]+@@',html):raise ValueError('Unresolved template marker')
    return html.encode(),identity

def atomic_create(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise FileExistsError('Refusing to overwrite existing output: '+str(path))
    # Fully written temporary file is linked atomically with no replacement permitted.
    name=None
    try:
        with tempfile.NamedTemporaryFile(prefix='.'+path.name+'.',dir=path.parent,delete=False) as temp:
            name=temp.name;temp.write(data);temp.flush();os.fsync(temp.fileno())
        os.link(name,path)
        d=os.open(path.parent,os.O_RDONLY)
        try:os.fsync(d)
        finally:os.close(d)
    finally:
        if name is not None:Path(name).unlink(missing_ok=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('output',type=Path)
    args=ap.parse_args();data,identity=assemble();atomic_create(args.output,data)
    print(json.dumps({'output':str(args.output),'sha256':sha(data),'bytes':len(data),'sourceSha256':identity}))
if __name__=='__main__':
    try:main()
    except Exception as exc:print('BUILD FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
