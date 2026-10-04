"""Test-only reversal of explicit source-audit edits. Never used by runtime/build.
Unknown bytes outside a hunk survive reversal and fail older hashes. This is not
execution of a substitute implementation: all behavioral tests use current HTML.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RECORD=json.loads((ROOT/'fixtures/source-audit-changes.json').read_text())
def project(name,text):
 from evidence_projection import project as evidence
 text=evidence(name,text)
 for edit in reversed(RECORD['edits'].get(name,[])):
  if text.count(edit['after'])==1:text=text.replace(edit['after'],edit['before'],1)
  elif text.count(edit['before'])==1:continue  # already projected by another historical layer
  else:raise AssertionError('Nonunique or modified source-audit hunk: '+name)
 return text
def read(name):return project(name,(ROOT/name).read_text())
