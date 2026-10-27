#!/usr/bin/env python3
from pathlib import Path
import re,sys,json
R=Path(__file__).resolve().parents[1]
css=(R/'src/style.css').read_text()
checks={'full word CSS final override': '.premium-test-step .seed-grid li strong, .tbw-wallet-panel .seed-grid li strong' in css and 'text-overflow:clip!important' in css and 'white-space:normal!important' in css,
        'narrow width grid': '@media(max-width:374px)' in css,
        'no recovery-word modification': 'src/07-wordlist.js' in json.loads((R/'fixtures/v0209-trusted-source.json').read_text())['trustedUnits']}
print(json.dumps(checks));sys.exit(0 if all(checks.values()) else 1)
