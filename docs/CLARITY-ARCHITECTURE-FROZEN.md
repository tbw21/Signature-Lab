# Clarity refinement — architecture and acceptance frozen
Date: 2026-09-18. Baseline: exact v0.17.0-rc1 HTML and source archive.
Proposed candidate: v0.18.0-rc1. Scope is presentation/navigation and one-click access to
an existing recorded attack; no signing, metadata, QR, evidence, RNG or startup-gate changes.

## Requirements and acceptance
C01 One native system sans family throughout headings, prose, controls, words, data and Help.
No remote/bundled font, no changed data strings, no ligature substitutions in technical data.
Native system-ui means platform-native fonts, not identical font files on all operating systems.
C02 The Test/Advanced/Session navigation and active panel top retain their geometry across views.
Keep progress navigation and acknowledged wallet identity in the common shell. Navigation
focus uses preventScroll, no scrollIntoView on these workspace buttons; step/Help focus remains.
No page-width jump when a scrollbar appears. No clipping, fixed viewport content heights or
inaccessible internal scrolling. Deep page content may require deliberate user scrolling.
C03 Wallet heading is concise; remove duplicated eyebrow/tag/demo-description row. One compact
safety statement remains above exposed words, explicitly never real seed / never fund this wallet.
New-wallet same-length regeneration remains accessible in Advanced; word-length controls remain.
C04 Single concise loading instruction beneath words includes no added passphrase. Keep QR,
fingerprint, enlargement and wallet acknowledgement distinct and usable; no extra fingerprint claim.
C05 One click opens a native modal and evaluates the existing published Dark Skippy fixture using
runDemonstration/Up. It loads the recorded signed transaction for an example, NOT a new active
hardware wallet. The example is visibly identified, never increments counts, never changes the
active wallet/transaction/policy/result/journal, and does not start/retain/acquire the camera.
One canonical example dialog/result surface; Help opens the same action. Close/Escape restores
focus and the active test. Missing dialog support or active capture gives an explicit no-op notice.
C06 Simplify redundant headings/instructions across Test/Advanced/Session while keeping full-output
review, true warnings, fixed-policy indications, progress history, evidence exports and Help.
C07 Narrow 320/360/390/438px, tablet768/1024, desktop1440, 12/24 words, larger text, keyboard,
forced colors, reduced motion, all result states, missing optional demo, rapid navigation tested.
C08 Retain and rerun applicable baseline tests; adapt only superseded presentation expectations.
New tests prove actual current bindings and core-state preservation. Historical projection reverses
only documented edits with hash checks and negative tampering probes. Never execute projected code.

## Architecture, trust and ownership
Existing application Fv remains sole owner of prepared test, result and session journal. Add no
controller/state ledger. Existing modal DOM holds visibility only; existing demonstration holds
its separate result. The production verifier and startup gate are unchanged. Modal is optional.
The page needs only the existing explicit camera/browser-download permissions, no persistence,
network access, dependencies, font files or privileges. User controls signer and files.

## State, recovery and retirement
Workspace selection/focus is presentation state only. Existing terminal failures and explicit
operator recovery remain. Reload creates fresh disposable state; no seed/crash-state migration.
Close older copy after saving evidence, open new release as a fresh lifetime. Rollback opens an
older uniquely identified HTML; it cannot undo a device signature. Existing auto-generated seed
reset rules stay unchanged. No OS installer, reboot services or recovery boot apply.
Retire multiple type-family overrides on visible surfaces, workspace-only stepper removal,
workspace-induced scrollIntoView, prominent redundant new-wallet CTA, multi-step Help-only demo
entry and duplicate example result markup. Do not retire same-length wallet regeneration.

## Qualification and change control
Static/syntax, contract/unit, cross-module, negative/fault injection, synthetic camera/browser,
clean build/adoption, fresh-version upgrade/rollback, page restoration and idempotence checks.
Freeze HTML and source ZIP SHA-256 before acceptance; extract fresh and run all driver jobs.
No acceptance byte/source edits; any blocker requires a new candidate and restart. Injected
failures and synthetic signatures are labelled, never counted as physical tests. Network/dependency
failure must not fetch alternatives; existing bounded inputs/signatures remain. No hard-timeout or
hardware performance claims. Actual Mac/Windows/iOS/Android typography not inferred from Linux.
External publisher/dependency authentication, independent outside review, full physical/browser
acceptance and Foundation findings remain open. No detection probability or firmware certificate.
