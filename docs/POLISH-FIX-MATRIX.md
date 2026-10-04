# Header / QR polish traceability

| Requirement | Implementation | Regression |
|---|---|---|
| Larger wheel / slightly smaller wordmark | One final header scale rule; existing image unchanged | P-S02/P-S03; 7 viewport scale cases |
| Quiet right version + question-mark Help | Existing links/routes, 44px Help with accessible name/title | P-S05-P-S07; Help roundtrip/version/focus/reflow cases |
| QR-aligned wallet card | Existing card moved once below canvas inside same QR rail | P-S08/P-S09; widths, both lengths, enlarge/pixels/state tests |
| No cramped action row | Natural flex wrap; full-width stacked actions when needed | Intermediate widths, doubled text, spacing |
| Transaction save/copy alignment | Same-width row; 44px controls | Both QR formats at mobile/desktop |
| No security or demo behavior changes | All 29 runtime files unchanged | Byte hashes + complete retained contract/fault/browser/oracle suite |
| No concealed warnings/history | Existing bindings and projections intact | Retained amber/incomplete/guided regressions plus new review check |

Only superseded full-width card geometry in tests/wallet-card-browser.py is changed: the
card now aligns to the QR's inner edges rather than spanning from seed words to panel edge.
The test still checks every action, normal/enlarged QR pixels, keyboard separation, completed
and unavailable states. Historical exact byte projections include only declared edits and
still reject unrelated changes. Candidate-version assertion updated to v0.18.2-rc1.
