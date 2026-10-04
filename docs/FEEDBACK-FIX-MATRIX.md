# Feedback disposition and regression map

| Finding | Evidence / disposition | Change / coverage |
|---|---|---|
| Demo seems to do nothing | Exact v0.18.4 real button clicks open native modal at 390/1440 in Chromium. Complete invisibility not reproduced; recorded raw transaction gives 2 valid signatures and no reference match. | Button no longer says Run; recorded-attack hint, explicit calculation/scope, check-complete result, original transaction text, reopen scroll reset. FB-C01–03; FB-B02/B12/B13; retained clarity/reference suites. |
| Ended banner keeps occupying active page | hasGuidedSession remains true because plan is historical; old banner uses it in all views. | Ended banner only in Session; completed/requested badge, same saved plan/report; active/halted/complete locks unchanged. FB-B05/B06/B16; FB-C23–26. |
| New wallet hidden in Advanced | Prior progressive disclosure moved routine operation into technical options. | One New test wallet control by word selector; same low-level reset; active locks preserved. Confirmation for used state and word-count changes; empty unused wallet remains quick. FB-C04–22/C27; FB-B01/B03/B04/B07–B11. |
| Ended findings could be overlooked after banner removed | Journal contains capture/control failure events not counted by old compact review badges. | Read-only stopped-operation projection drives existing tracker and Session alert; no journal mutation. Ordinary end neutral; earlier failures preserved. FB-C24–26, FB-B06. |
| Save session record fails in real reactive browser | Reproduced on exact v0.18.4: JSON.stringify fails due to frozen reactive array proxy invariant. Node-only tests lacked reactivity. | Detach the existing public snapshot with JSON before freezing it; no seed, field policy, ledger or second exporter added. Real downloads checked in FB-B05/B07 and retained exporters. |
| Stale native close event cancels newly opened reset dialog | Reproduced in first development browser run, never released. | A queued close event cancels intent only if the dialog is still closed. FB-B04. |
| "1 file reviews" and routine end styled as fault | Baseline documented copy issue; normal end is not a cryptographic failure. | Singular/plural correct; normal end neutral; halted end and fault history remain amber. FB-S09/FB-C24–25 and UI assertions. |
| Decorative border collision | Visual review found reused .example-entry inherited old onboarding separators. | New scoped .demo-launch name; border-free trigger and consistent adjacent wallet controls. FB-B01 regression. |

All key/signature/transaction/metadata/QR/camera algorithms and journal source remain unchanged.
The application coordinator is the sole changed runtime module. Artifacts before this candidate
are retained untouched. Historical projection tests reverse exact declared changes; runtime tests
execute current candidate bytes, not a historical projection.
