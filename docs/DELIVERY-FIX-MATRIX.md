# Approved changes to v0.18.4-rc1

| Requirement | Implementation | Regression coverage |
|---|---|---|
| Borderless wallet rail; aligned QR/actions | CSS removes border color/background only; one canvas, no overlays | D-S03/08, browser helper/QR geometry and inherited polish/card cases |
| Helper under 12/24 selector | Same hint ID moved immediately after selector, grid reflow | D-S05, browser 8–15, 12/24/large text |
| Clear wording | Wallet confirmed / Run Dark Skippy demo / Import the signed response | D-S06/07 and browser 16/17/24 |
| Stationary left step navigation | Existing focusSection accepts scroll choice, existing stale-focus guard | D-C03/11–14/22, browser 1–7/25/28 |
| Explicit task focus | Wallet confirmation intentionally reveals transaction review | D-C15/16/24, browser 16/26 |
| Reopen unfinished Results intake | Presentation flag only; no result reset | D-C04/05/18/20, browser 17/20/21 |
| Completed result immutable | Existing result/journal and evidence, no intake reopened | D-C06/19/24, browser 22/23 |
| Current active Results stays scanning | No-op before camera-stop for same active step | D-C07/08/21, browser 18 |
| Leaving camera stops, never auto restarts | Existing sole stopScan/controller | D-C09/10, browser 19/29 |
| Demo stays isolated | Existing openExample/runDemonstration unchanged | D-C23, browser 24 and retained clarity/onboarding |

28 of 29 runtime modules remain byte-identical to v0.18.2. Only declared coordinator
navigation/focus/acknowledgement changes occur. The exact diff and before/after hashes are
fixtures/delivery-changes.json. No verification rule, signing method, metadata acceptance,
QR decoder, startup gate, export schema, storage rule or camera controller was changed.

Historical test adaptations: literal version and approved copy assertions updated; existing
exact-source projection records extended with reversible approved edits. Runtime preservation
checks for the old wallet/polish stages reverse only this release's declared app changes before
checking their original hashes. The independent current stage checks the exact changes and
rejects unrelated mutations. No runtime result is derived from a historical projection.
