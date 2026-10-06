# Readability corrections and regression coverage

| Request/finding | Change | Regression |
|---|---|---|
| Default type too small / mixed family | Approved preview uses local Helvetica-first family, 18px body, generally 16px controls/instructions, >=14px supporting text | Readability full-view text metrics, both word lengths, enlarged text/spacing; existing rendered suites |
| Orange logo punctuation | Remove dot span only; wheel unchanged | R06/R07 and full-view DOM |
| Footer too far and too small | No content min-height spacer; static 16px footer follows active panel | Footer geometry across wallet/Advanced/Session/intake/results/Help |
| Scenario label zero-size | Override zero font-size on actual label | Reproduced 0px in development, full-view regression now >=14px |
| Unequal mobile result actions | Stretch all siblings including incomplete-result icon controls; use full-width text actions on narrow views | Strengthened pairwise vertical-overlap assertion reproduced 2 failures before fix |
| Possible two-digit output collisions | Retain full label/address/amount and assert text-range separation at 20 outputs | 320/390/1440 output review/editor cases |
| Older font/geometry assertions | Explicitly supersede system-ui, 14px description and undersized one-row header rules; preserve all safety predicates | New typography/flow cases plus retained live-browser suites |
| Preview/source history unreliable | Recover exact preview, verify script body against full v0.20.0 source, unique v0.20.3 identity | All 29 source hashes unchanged; no prior acceptance totals reused |

No extra camera operation, font download, security policy change, signing family or UI redesign.

## Content-relative footer and scrolling
An unchanged pre-fix development build at 1440×900 changes from a 1,142px wallet document to a 900px Advanced/Session document. Its scroll range changes from 242px to zero, necessarily clamping a prior 60px offset to zero. The navigation's document-space top remains exactly 139.375px. An inherited test incorrectly required the impossible old scroll offset after retiring the artificial height spacer. Its replacement preserves all representable offsets, requires unchanged document alignment/state, and rejects application-requested scrolling. No runtime scroll behavior or deadline changed.
