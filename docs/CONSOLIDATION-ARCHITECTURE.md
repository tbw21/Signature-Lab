# Consolidation and guided physical-device sessions: frozen scope

2026-09-16. Baseline v0.14.0-rc1 plus the behavior of v0.12.3-fingerprint-rc1.
Baseline hashes verified before implementation (recorded outside the source tree).
This is a software implementation milestone. Hardware and outside publisher/source
acceptance cannot be performed or asserted by this milestone.

## Requirements and acceptance criteria
C1. One assembled HTML retains v0.14 QR/camera/metadata/evidence/fixed-policy logic and
adds the root fingerprint below SeedQR, with leading zeroes and stale-state guards.
C2. Optional guided physical-device session: 1-200 distinct prepared cases, presets
20/50/100, fixed public plan and signing policy, same wallet throughout. Generate case
shapes with the existing scenario generator; do not pre-sign or return references as
hardware output. Freeze the whole public plan before the first session transaction.
C3. A user reviews/approves every transaction on the real signer. Page advancement and
camera initiation require explicit clicks. No simulator, firmware uploader, automatic
signing, background network, unattended approval, repeat signing or implicit retries.
C4. Only the current planned transaction can receive a result. Signature differences,
metadata warnings, incomplete submissions and camera failures halt guided advancement.
Operator can explicitly end the session; its existing findings remain exportable until
new-wallet reset/reload. No button turns a halted case into a matching result.
C5. One authoritative in-memory event ledger provides historical summaries and guided
results. Existing same-wallet unique checks are projections, not another writable ledger.
Current result snapshot remains immutable; each event stores public summary only, never
private prepared state. Save current evidence before advancing when raw replay is needed.
C6. Session report includes fixed plan/hash, requested/completed/not-completed counts,
matching/differing/metadata/incomplete counts, per-case summaries, stop reason, exact
build identity, and a no-device-attestation/no-safety-certificate limitation.
C7. Repeated Next/Start/import, late callbacks, editing, new wallet and changed policy
cannot silently change an active plan, duplicate progress, skip a case or revive a
halt. Manual tests continue without creating a guided plan; optional setup failures
leave the current test unchanged. No actual firmware profiles are inferred or certified.
C8. Desktop/mobile controls have accessible labels, visible selection/focus, and no
horizontal overflow. Real scanning speed and nontechnical comprehension are not claimed.

## Architecture and authoritative state
Core retained: existing transaction generator/key functions and sole signature verifier.
Transport retained: BC-UR, BBQr, Specter/static import and sole camera lifecycle controller.
New session bookkeeping is a synchronous private owner inside the app. It owns one
immutable plan, cursor/control phase and one append-only public event ledger. The UI is
only a projection and sends explicit commands; there is no independent UI verifier.
The existing prepared cache remains the only prepared transaction; the existing result
snapshot remains the only current verification finding. History stores bounded summaries
of that snapshot, not a second editable result. Max 200 planned cases, 2000 ledger events.
Fingerprint is read from the same cached HD root and guarded by normalized seed/SeedQR
state. No second key derivation, fingerprint state cache or clipboard persistence.
Session contracts: inspect/status, plan (no published mutation), apply/start, verify
(current-case identity), record, explicit advance and rollback/end. Core verification
is reused unchanged. Only the current case is rendered/prepared cryptographically.

## Privilege / ownership / optional boundary
Browser-only; disposable data in this tab. Same CSP, no connections or new permissions.
Camera permission is still operator initiated. No install/service/boot/storage or
Bitcoin/Fulcrum operation. Software does not flash firmware or control device buttons.
Guided session and export are optional. Failure creating a plan cannot mutate core test
state. Failed active runs require explicit end before manual work can resume.

## Lifecycle, upgrade, recovery and rollback
Previous release files are immutable archives, not alternative current builds. The
explicitly opened new HTML is the single active version. Save reports, close old tab,
open new HTML and create a fresh disposable wallet. No migration/persistent seed store.
Page reload/crash loses the run; do not claim crash resume. Back/Forward restoration
may retain the same in-memory run but never restarts capture or advances a transaction.
Explicit End session stops capture, preserves its log and permits manual work; a new
wallet resets the in-memory ledger only after the operator chooses that action. There
is no rollback of device signing and no retry of an uncertain hardware operation.
Build/archive rollback: reopen untouched baseline, fresh wallet. Frozen candidates are
never edited; any failure disqualifies them and requires a new candidate/full rerun.

## Retired components / deferred external gates
The fingerprint-only build is no longer the recommended runtime alternative; its
feature is incorporated, not its old QR/camera implementation. The writable public
sessionChecks array is retired in favor of an immutable projection of one ledger.
No public firmware simulator, new wallet types, device-specific profiles or speculative
QR speed/density changes. Repeat-signing diagnostics and physical scan tuning are held
until target-hardware qualification and measured workflow observations. Publisher key,
upstream dependency authentication and independent organizational review remain open.

## Qualification
Before freeze: static/syntax, legacy/unit/contracts, integration, fault injection,
fresh-page/adoption/rollback/recovery/idempotence simulations, source/archive rebuilds.
After freeze: repeat entire applicable suite from clean extraction; record SHA-256,
passed/failed/unavailable separately. Include independent fingerprint and cryptographic
oracles, plan limits/tampering, cancelled/late camera/file operations and optional
setup failure. Actual origins/browsers and physical hardware are separate gates.
No production, hardware compatibility or safety-rate claim is authorized by this scope.
