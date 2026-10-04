# Wallet card traceability and regression disposition

| Finding / requirement | Correction / scope | Evidence |
|---|---|---|
| W01-W03: fingerprint, enlargement, comparison and continuation fragmented | One wallet-confirmation region; old separate footer and fingerprint border retired | wallet-card-static S03-S08; browser 1-15 |
| W02: controls must not perform both actions | Original callbacks retained; explicit button type; primary action described by safety/comparison copy | static S05/S08; browser keyboard case |
| W04: preserve active wallet, QR pixels and result | All 29 ordered modules byte-identical to dev-4 | static S02; retained crypto/startup/QR/metadata tests; browser 8-15, completed test |
| W05: reproduced 438px uneven buttons | Allocate appropriate room to the longer label and stretch same-row controls; no font shrinking | wallet-card-browser case 26; old HTML reproduction failed, corrected HTML must pass |
| W05-W06: related layout fine tuning | Same trailing action alignment; readable wrap/stack, no nested border or clipped status | enlarged-text/spacing/high-contrast/optional-example cases |
| W07: unfinished clarity acceptance | Run all retained jobs on exact candidate; no inherited test-total reuse | qualify.py job receipts |
| Native-font copy wrapping | Require one line when measured glyph width fits, natural wrap otherwise; keep 14px desktop text | copy-browser responsive cases; Linux 1024px reproduction |
| Old copy-refinement expected version | Expect the newly assigned 0.18.1-rc1 instead of dev-4's 0.18.0-rc1; no runtime change | copy-static C-S10 |
| Superseded alignment assertion | Enlargement is now inside common card, not touching right QR edge; assert card containment instead | alignment-browser.py seed_geometry; new pixel/state tests |

No extra seed persistence, camera retention, new signing method, new state owner, dependency or
firmware profile. Source projections remain test-only exact reversals with negative tamper tests.
Full runtime/browser checks execute current candidate bytes, not source projections.
