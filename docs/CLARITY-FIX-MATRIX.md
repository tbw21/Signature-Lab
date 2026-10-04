# Clarity refinement traceability

| Request | Implementation | Regression evidence |
|---|---|---|
| One native font | One system-ui token, inherited across all text/control/data surfaces. No webfont/CSP changes. | CL-S05/06; clarity-browser 1–7, 11–18, 30 |
| No workspace bounce | Common navigation/identity/guided shell retained across views, preventScroll focus and stable scrollbar gutter. | CL-S07/08; CL-C15–17; browser 1–10 |
| Less wallet clutter | Concise title; redundant eyebrow/tag/demo-description removed; New wallet moved to Advanced. | CL-S09–11; CL-C18–20; browser 11–18, 28 |
| Concise warning | Visible no-real-seed/no-funding reminder above the words; technical detail stays in Help. | CL-S09; retained UX safety checks |
| Direct known attack | One native modal uses the existing recorded fixture and verifier; no active-wallet replacement, counter or evidence mixing. | CL-S12/13; CL-C01–14; browser 19–27 |
| Simplify consistently | Shared typography, panel-heading hierarchy, shorter load/acknowledgement prose, existing advanced spaces. | full retained UX/alignment/Help tests; new font and layout cases |
| Preserve security | Startup, crypto, metadata, QR/camera, evidence and journal units unchanged; actual candidate is executed by all runtime tests. | CL-S02–04/14; retained suites |

Historical preservation tests reverse declared UI changes to compare prior baselines. They do not
execute historical/projected code and do not establish behavior of the new UI. New current-DOM
and native-dialog cases cover intentional changes; unauthorized edits fail exact hash checks.
