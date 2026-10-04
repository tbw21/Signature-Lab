"""Test-only exact reversal of declared delivery changes. Never used by build/runtime."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=json.loads((ROOT/'fixtures/delivery-changes.json').read_text())
def project(name,text):
 from audit_projection import project as audit
 text=audit(name,text)
 for edit in reversed(R['edits'].get(name,[])):
  assert edit['after'] and text.count(edit['after'])==1, 'Nonunique delivery reversal '+name
  text=text.replace(edit['after'],edit['before'],1)
 return text
