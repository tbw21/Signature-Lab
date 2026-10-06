# Readability delivery: frozen requirements and architecture

Scope fixed before applying this continuation's source edits.

## Requirements and acceptance criteria
Preserve the user's approved Helvetica-first, larger-text preview; remove only the orange wordmark dot, not the wheel. Body baseline 18px at normal 16px root; normal controls/instructions 16px and supporting text at least 14px except browser-native internal widgets. No licensed font binary or external font resource is distributed. Helvetica is preferred when locally available; local Arial/Liberation Sans/sans-serif fallback remains necessary. Footer is readable and follows the active content in normal flow, never fixed over controls or pushed below an artificial screen-height spacer. Licence and attribution stay visible.

Test 320/360/390/438/768/1024/1440 widths, 12/24 words, enlarged/reduced QR, all workspaces, results/review/incomplete states, dialogs, output 10-20 labels, keyboard, increased text/spacing and footer route. No clipped or overlapping critical text; natural wrapping is preferred to shrinking. Fix only reproduced readability regressions, with a named regression for each.

## Recovery and authoritative source
The v0.20.0 HTML/source hashes match the supplied qualification; all 241 manifest entries match and a fresh rebuild reproduces that HTML. The supplied readability-work/dev-1.html is recoverable. Its executable module body is identical to v0.20.0 after removing only the generated build header. No v0.20.2 HTML/source archive or acceptance receipts were recovered from the mounted runtime or Files searches. Screenshot/checkpoint claims are not acceptance evidence and are not reused. This work uses new identity v0.20.3-rc1, preserving the approved preview's template and stylesheet and all original runtime source.

## Modules and trusted core
The existing application coordinator, prepared transaction, immutable completed result, camera owner, self-check and single session journal remain authoritative. All 29 ordered JS source units and vendor bytes are unchanged; tests enforce hashes. Application edits allowed only in src/page.html and src/style.css. Optional Help/demo/retention stay optional and cannot alter verification. No new runtime controller, ledger, validator, parser, retry loop or UI business logic. One build.py, archive.py and qualify.py remain authoritative. Test-only reverse projections must match exact declared edits and may never erase an undeclared mutation. Behavioral tests execute current HTML.

## Privileges and ownership
Browser permissions, CSP, offline networking restrictions and storage behavior remain unchanged. No font downloads, persistence, network integrations, installed services or browser policy changes. Only working-container source/output paths are writable; prior supplied archives remain untouched.

## State, restart, rollback and upgrades
No data migration. A reload or confirmed replacement starts a new wallet lifetime under existing rules and can discard unsaved evidence; closing/reverting does not undo physical signatures. Save needed evidence before switching versions. Rollback means explicitly reopening a previously accepted exact artifact after closing the current tab; no automatic downgrade, resume or retries. OS recovery boot is not applicable to a standalone HTML application.

## Retirement
Retire orange wordmark punctuation, undersized default text and artificial footer spacer in presentation only. Preserve QR white quiet area, all-output review, warnings, original attribution/licences and evidence controls. No additional feature work during acceptance.

## Qualification
Run syntax/static, unit/contracts, integration, faults, fresh-start/adoption/upgrades/rollback/restoration/idempotence simulations and reproducible clean extraction as applicable. Negative cases stay terminal until explicit operator action. Complete a development preflight; freeze exact HTML, source archive and SHA-256; then run all canonical jobs from a fresh extraction. Any failed candidate is disqualified and never patched. Frozen jobs run without retries; unavailable environments, simulations and physical results are separate. Finish a reproducible handoff with one root HTML and one start guide plus source, evidence, reports and hardware instructions. Physical and outside organizational/publisher acceptance are not performed or invented.
