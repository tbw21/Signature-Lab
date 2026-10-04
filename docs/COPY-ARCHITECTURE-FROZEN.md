# Copy and scope refinement: frozen architecture and acceptance criteria

Frozen before implementation: 2026-09-17T20:01:34.779280+00:00.
Baseline: exact v0.16.3-rc1, HTML c2d52403e93af63dfd7e9bcd9798a5fe97050510548f4ba258ee5ca7d937b32a,
source ZIP 3f2eb32e61d5d105bb496bd8d5882deb16705d2c2314f1d5454b570df01190b6.
New candidate name: v0.16.4-rc1. Old names and artifacts must not be overwritten.

## Requirements and acceptance
1. Remove the secondary Master key / No passphrase line from the Test wallet surface.
   Keep the fingerprint, source, QR, words, paths and all original dynamic bindings unchanged.
   Retain master-fingerprint/no-passphrase information inside the existing technical FAQ.
2. Top introduction is one paragraph in the existing informational gold #e5b67d, 14px desktop,
   13px narrow layout, no forced line break, no fixed height, clipping, ellipsis, nowrap or
   shrinking type to fake a single line. Fit one line at the existing 1120px max-width desktop
   container at 100% text; reflow on smaller screens or enlarged text.
   Exact copy: Compare test signatures with expected results to flag deviations such as the published Dark Skippy example; a match cannot rule out all attacks.
3. Clarify inside the existing signature-check FAQ that this compares supported deterministic
   signatures, flags the published example, does not search for a secret attack watermark,
   and cannot rule out conditional variants or other channels. Do not claim detection of
   all Dark Skippy attacks or imply that only unrelated attacks remain possible.
4. The matching-result scope line also becomes: This match applies to this transaction only;
   it does not rule out seed leakage or other firmware attacks. Keep routine metadata under technical details; errors, amber review, immutable results,
   device-origin limits, demo isolation, Help contents, alignment and offline protections stay.
5. No runtime JavaScript, cryptographic algorithm, metadata policy, transport, seed generation,
   verification condition, session state or camera controller change.
6. Rerun all retained applicable checks from a clean extraction, plus new exact-copy/scope,
   color/contrast, desktop-one-line/mobile-reflow, enlarged-text, fingerprint and FAQ checks.
   Tests must preserve failure states, QR pixel bytes and wallet/transaction/policy identity.

## Architecture and module boundaries
Trusted runtime remains the one prepared test, one verifier, one QR session, one camera owner,
one immutable result and one session journal. src/page.html owns explanatory copy;
src/style.css owns its presentation. build.py remains the one source assembler and generates
Help contents from actual headings. No new runtime controller, modal, setter, API or dependency.
Optional Help is not installation/startup-critical and cannot approve or alter a result.

## Privilege, ownership and authoritative state
Browser permissions, CSP, no-network policy and local in-memory state are unchanged. No storage
of secret state, extra permissions, telemetry or authentication claims are added. The opened
HTML is the active release. release.json owns its version; source-lock.json covers assembly
inputs. Build/source identity and artifact hash are distinct; unsigned hashes are not identity.

## Reboot, resume, rollback, recovery, upgrades
No OS installation, service, bootloader or storage migration exists. Save result evidence first,
close the old page, open the new candidate and use a fresh disposable wallet. Reload starts
fresh; Back/Forward may restore memory but not restart capture or signing. Rollback means close
and open untouched v0.16.3 with a fresh test, never editing the new artifact or undoing hardware
signing. Existing terminal failures require explicit operator action. No automatic retry added.

## Explicitly retired presentation
Main-surface Master key / No passphrase line; forced purpose-break BR; gray two-line introductory
copy. Historical fixtures remain provenance, not alternate runtime paths. No security control
or underlying scope limitation is retired.

## Qualification and freeze
Before acceptance complete static/syntax and unit/contract development checks, retained and new
cross-module integration, faults and applicable lifecycle/build simulations. Freeze source
archive and HTML with SHA-256; run final acceptance in a fresh extraction without modifying
candidate, source, test or lock bytes. Any blocker disqualifies the candidate; fix under a new
candidate identity and restart. Skipped/unavailable checks and external gates stay separate.
Physical signer/optical acceptance, normal origins, publisher signing, dependency provenance and
outside review cannot be inferred from this presentation-only change. No bug-free, 100%-reliable
or fully-audited claim is authorized by this scope.
