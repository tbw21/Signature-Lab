#!/usr/bin/env python3
"""Explicit development-only source lock update. Never use on a frozen candidate."""
from pathlib import Path
import sys,json,importlib.util
root=Path(__file__).resolve().parents[1]
if sys.argv[1:]!=['--development-update']:raise SystemExit('Use --development-update only BEFORE candidate freeze.')
spec=importlib.util.spec_from_file_location('build',root/'build.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
(root/'source-lock.json').write_text(json.dumps(m.manifest(),indent=2,sort_keys=True)+'\n')
