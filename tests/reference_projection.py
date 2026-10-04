"""Reverse only declared startup/Help additions for historical preservation assertions.
This never changes build/runtime bytes. New reference-static tests verify every reversal
against the immutable baseline hashes before these historical projections are trusted.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=json.loads((ROOT/'fixtures/reference-projection.json').read_text())
def project(name,text):
 from clarity_projection import project as clarity
 text=clarity(name,text)
 for edit in reversed(RECORD['edits'].get(name,[])):
  assert text.count(edit['after'])==1, 'Declared reversal is not unique: '+name
  text=text.replace(edit['after'],edit['before'],1)
 return text
def read(name):return project(name,(ROOT/name).read_text())
