"""Exact, test-only reversal for historical preservation checks. Never imported by runtime/build.
New tests assert current hashes independently. Mutation outside the exact authorized text remains
and fails the older hashes; behavioural tests always execute current HTML, never projections.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RECORD=json.loads((ROOT/'fixtures/evidence-upgrade-changes.json').read_text())
def project(name,text):
 e=RECORD['edits'].get(name)
 if e and text.count(e['after'])==1:return text.replace(e['after'],e['before'],1)
 return text
