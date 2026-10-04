# v0.15.1 UX stabilization contract
Frozen before implementation: 2026-09-16. This is a UI/release-clarity change, not a new detector.

## Baseline and scope
Authoritative baseline: supplied v0.15.0-rc1 HTML SHA-256
3d5dc1835bc4841132f099e771f05ce5eac113c126d7a0abb783626d594c3811;
source ZIP 9c752b1f456053f755713d923bda8eee3f6b97a0dd995c6626f94fec6908dc3f.
The screenshot's 1-200 session planner belongs to this consolidated branch. The
simultaneously surfaced v0.12.2 attachment is NOT the implementation baseline.
Previous releases remain unchanged. A new unique release identity is mandatory.

## Requirements and acceptance criteria
UX-01: Session count, presets, labels, instructions and start/end controls reflow without
clipping at 320, 360, 390, 438, 768, 1024 and 1440 CSS pixels. Test enlarged fonts,
text spacing, keyboard interaction, narrow containers and active/halted/completed states.
Do not hide horizontal overflow to conceal a failed layout or shrink fonts to force fit.
UX-02: One discoverable Advanced tools disclosure, closed on fresh open, groups optional
session planning, transaction editing/signing policy and report labels. Default user can
complete the three-step test without opening it. Essential QR transport and import options
remain available. Power users retain every supported existing operation.
UX-03: Collapsing tools is presentation-only: it must not change seed, PSBT, references,
policy, prepared identity, session journal, results, or camera acquisition. Nondefault
policy/PSBT/custom transaction state remains explicitly visible outside disclosures.
UX-04: Safety instructions, comparison limitations, wrong/incomplete/mismatched results,
metadata status, active/halted guided state and exit/stop actions never depend on Advanced.
Evidence export may be collapsed, but its existence remains discoverable and per-response
retention limits remain clear before advancing. No green 'firmware safe' certificate.
UX-05: Native disclosure keyboard behavior, visible focus, logical labels, no hidden
focusable children, distinct headings, text status in addition to color. Check 200% text
size and 320px reflow as engineering targets, not a blanket WCAG conformance claim.
UX-06: Actual release version and accurately labelled assembly-source hash visible in
Help; release-candidate/hardware-pending state visible from the initial screen. A self-
reported identity is not self-authentication. No invented publisher signature, audit,
physical compatibility, scanning improvement or safety probability.
UX-07: Core scripts, keys, generator, verifier, metadata policy, codecs, scanner,
prepared cache, journal and export contents remain unchanged. Only Fv presentation
getters/actions may change. Full existing qualification plus new UX regressions must run.
UX-08: Document trust conditions and residual gates: immutable versioning, signed authentic
publication, dependency provenance, independent review/reproduction, real devices/browser
acceptance and nontechnical-user interpretation. No new firmware simulator or algorithms.

## Architecture / boundaries
Trusted runtime: existing transaction/key construction, verifier, metadata assessment and
result snapshot. Existing camera, QR transports and optional guided planner retain their
contracts/ownership. The page template and stylesheet own layout; native details elements
own disclosure state, with existing settingsOpen binding for the transaction editor.
Any added application methods are presentation-only. The same verifier serves all users.
No separate beginner/advanced verification policy, retry engine, ledger or state store.

## Privileges and authoritative state
Browser-local unprivileged HTML, unchanged CSP/connect-src none; camera only on explicit
Start. No account access, runtime downloads, persistence, telemetry, funded wallet data,
new dependency or release-signing key. No new network permissions.
Private prepared test, immutable current result and existing private session journal remain
the only corresponding state authorities. Native disclosure state is not security state.
One active release is the opened uniquely versioned HTML; older versions are archives.

## Lifecycle / apply / verify / recovery / rollback
inspect: existing read-only app inspect/status plus visible UI. plan/apply/verify/rollback:
existing contracts remain unchanged. Opening/collapsing tools applies no transaction action.
Fresh page defaults closed; switching steps doesn't reset nondefault settings. Back/Forward
may restore native disclosure state but must not restart capture or advance. Reload/crash
loses memory; no persistence or crash-resume claim. Save reports before closing.
Upgrade/rollback: close other pages, open chosen version and start a new disposable wallet.
No OS service, storage, Bitcoin/Fulcrum, bootloader or recovery-boot work applies.

## Retired UI
The standalone planner above the first wallet, duplicate customization placement, always-
visible optional report/evidence details, rigid 140px count column and nowrap action labels.
Their operations remain through one authoritative control each; no hidden old controller.
Do not reuse v0.15.0-rc1 for different bytes.

## Qualification
Development: static/contract/integration/faults, full previous suite, new disclosure/layout
suite, offline/browser lifecycle, optional absence, export/signature negative paths,
independent vectors, fresh/existing-data/rollback/idempotence and reproducible archive.
Freeze HTML and source ZIP only after development passes. Clean-extract and rerun all
applicable stages on those bytes, writing evidence outside the extraction. Any blocker
requires another identity/candidate and a complete new run. Hardware/external gates stay
separate. Three review dimensions: source preservation, behavioral/fault tests, visual and
accessibility-layout probes. No guarantee that all possible bugs have been eliminated.

## Trust-link clarification before candidate freeze
The standalone footer's relative LICENSE.txt navigation does not resolve inside the single
HTML download. UX-06/UX-08 include self-contained Help/status navigation; expose the exact
already-embedded MIT notice through an internal Help disclosure and test the footer target.
This changes presentation only, not the license or cryptographic/runtime contracts.
