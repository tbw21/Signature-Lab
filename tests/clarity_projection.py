"""Test-only reversal of approved UI changes; never used in production/build.
Whole-template exact equality guards prevent unrelated edits being masked.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=json.loads((ROOT/'fixtures/clarity-projection.json').read_text())
def project(name,text):
 from audit_projection import project as audit
 text=audit(name,text)
 for edit in reversed(RECORD['edits'].get(name,[])):
  assert edit['after'] and text.count(edit['after'])==1, 'Nonunique clarity reversal: '+name
  text=text.replace(edit['after'],edit['before'],1)
 return text
