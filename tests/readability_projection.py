"""Test-only exact reversal of the authorized presentation delta; never imported by runtime/build."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RECORD=json.loads((ROOT/'fixtures/readability-changes.json').read_text())
def project(name,text):
 e=RECORD['edits'].get(name)
 if e and text.count(e['after'])==1:return text.replace(e['after'],e['before'],1)
 return text
