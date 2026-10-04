# Change-to-test traceability

| Requirement | Change | Regression evidence |
|---|---|---|
| R1 | Same bordered three-button controls on every viewport; long text reflows | calm-browser 1-13, 28-30; retained UX reflow/keyboard suites |
| R2 | Main review/QR/actions together; Advanced and Session separate | calm-browser 1-8,18-20,25-27; calm contracts |
| R3 | One read-only output projection from prepared public PSBT | calm contracts 12-18; calm-browser 14-17,30; independent output-oracle (6 checks) |
| R4 | Expected file detail collapsed; amber findings and history indicators visible | calm-browser 18-20,26; retained remediation/UX and journal tests |
| R5 | Single JSON download helper; full evidence primary, summary explicit; short names | calm contracts 19-27; calm-browser 21-24,31; public replay/tampering |
| R6 | Generation/epoch/view guarded focus; no capture side effect; Help returns workspace | calm contracts 1-11,30-39; calm-browser 25,27,32; lifecycle suites |
| R7 | Core, metadata, codecs, camera, vendors preserved byte-for-byte | static preserved-module map and cryptographic token checks |
| R8 | Retained all named test cases, adapting only obsolete UI paths | frozen disjoint reports from qualify.py; independent core/structure/replay |
| R9 | Unique release.json, lock, manifest, no overwrite, exact source assembly | static and package suite; outside freeze/final-integrity receipts |

Development corrections: duplicate Paste label, enlarged seed-word reflow, Help returning
to the wrong workspace. Test-harness changes are separately documented. No live signing
algorithm, metadata exception or terminal-error rule was relaxed to satisfy tests.
