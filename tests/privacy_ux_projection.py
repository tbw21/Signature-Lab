"""Test-only historical source projection with both exact source hashes asserted."""
import hashlib,json
from pathlib import Path
REC=json.loads((Path(__file__).resolve().parents[1]/'fixtures/privacy-ux-qualification-projection.json').read_text())['files']
def sha(text):return hashlib.sha256(text.encode()).hexdigest()
def project(name,text):
 r=REC.get(name)
 if not r:return text
 assert sha(text)==r['newSha256'],'Unauthorized privacy/UX source change: '+name
 for e in reversed(r['edits']):
  assert e['after'] and text.count(e['after'])==1,'Non-unique test-only reversal: '+name
  text=text.replace(e['after'],e['before'],1)
 assert sha(text)==r['oldSha256'],'Historical source identity mismatch: '+name
 return text
