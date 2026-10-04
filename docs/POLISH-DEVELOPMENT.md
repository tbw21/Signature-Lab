# Development record before freeze

Baseline hashes and archive CRCs verified; 181 source-manifest entries present.
Architecture frozen before application edits. Application changes limited to page/CSS.

A measurement helper initially set __file__ outside the tests directory, so its inherited
harness looked for browser.py in the wrong folder. No application ran in that failed probe.
Correcting the helper path allowed exact baseline and new geometry measurements.

Initial targeted checks: 12/12 new static and 7/7 retained card viewport cases passed.
The first 10-case enlarged-text/Help range returned 8 passes and 2 test failures. Those two
programmatically focused Help after pointer-driven workspace selection and incorrectly
expected :focus-visible without keyboard input. The harness now enters keyboard modality
with Tab before focusing and activating Help; no application/style rule was relaxed.
The complete 18-case range (16-33) subsequently passed. Failed records remain outside the
source tree in the development evidence and are not counted as acceptance.

The retained full-width card geometry assertions were intentionally revised for the new
shared QR rail, preserving all state/pixel/safety assertions. Exact historical source
reversals were extended with only the documented page/CSS edits. No runtime file changed.

Full preflight and frozen-candidate acceptance are separate. Their exact completed results,
any subsequent failure and unavailable environments must be recorded in the external report.

The first complete development preflight passed 932 cases with 0 failures and 4 unavailable
origin/engine checks. A subsequent visual inspection identified avoidable 320px header
wrapping; a focused regression then deliberately reproduced it (0 passes, 1 failure).
Reducing only the smallest-screen inter-group gap keeps all original text/control sizes and
fits one header row. Long/enlarged version text is allowed to wrap instead of spilling outside
its label. New browser assertions require ordinary header height and non-overflowing labels.
No runtime behavior changed. A second complete preflight is required after this refinement.

One report-summary call was made before the last preflight job finished; its completeness
assertion rejected the partial dispatch. After completion the same read-only summarizer
verified the 932-case totals. No raw result or source was changed by report assembly.
Supplemental rendered QR screenshot inspection matched canvas content for 16 width/word/size
combinations; these observations are not added to the named pass totals or optical claims.

During the second preflight, a visual sweep found the outgoing QR-format selector was
20 CSS pixels narrower than its desktop QR. A targeted assertion reproduced it (1 pass,
1 failure across the mobile/desktop pair). The selector now shares the available width of
its QR and save/copy row, without changing callbacks or font/selection styling.

The second dispatch had already stopped automatically after an inherited browser assertion
failed (6 passes, 1 failure in sessions-browser-15-21; 26 of 83 jobs completed). An attempted
explicit stop for the selector correction came later and raised ProcessLookupError because
the dispatcher was already gone. Its initially written ABORTED receipt is preserved with a
separate correction; it does not establish the actual earlier stop cause.

The failed assertion synchronously counted an accessibility-role control immediately after
changing to the transaction step. A separate 40-session probe of those same dev-2 HTML bytes
observed six immediate zero role counts, followed by the expected count after two render
frames in all 40 observations; wallet/plan/transaction state remained unchanged and there
were no page errors. The step uses deferred x-show presentation. The inherited check now
waits at most six seconds for the same unique, visible, disabled Next control, and rechecks
the unchanged transaction state. This is a bounded UI assertion, not an application retry.
Its first external probe helper split a Python prefix at the wrong delimiter and raised
SyntaxError before executing an application; a corrected delimiter ran the complete probe.

The third preflight passed that inherited case, but was explicitly stopped before modifying
the test and these source notes; its partial jobs are excluded. The new independent probe
and earlier failure are retained. A full fresh preflight and then frozen acceptance are
required. No partial run may stand in for either, and no runtime rule has been changed.
