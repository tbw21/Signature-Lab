> Historical v0.14 record. For the consolidated candidate, apply
> CONSOLIDATION-ARCHITECTURE.md and CONSOLIDATION-FIX-MATRIX.md.

# Reliability release architecture and acceptance contract

Frozen before implementation: 2026-09-15. Target family: v0.14.0.
Baseline: v0.13.0-rc2, HTML SHA-256 d3c1793100e2bdb8e1450104c32b1aff54be3bb6fe3917686b6b8a54278bddb7.
Reason: correct audit R1-R4, D1-D5, and improve Q1/Q2 qualification. No unrelated features.

## Requirements and acceptance

R1: failed BC-UR checksum/decoder errors are terminal, visible and discard partial results.
An explicitly new session works; repeated frames cannot revive a failed session.
R2: every character/frame in a finite import is accounted for before verification.
Identical duplicates and verified fountain redundancy are permitted. Conflicts, malformed
trailing data, different transfers and mixed formats are rejected. Camera completion is
separate from finite-input completion and may stop once a valid complete artifact arrives.
R3: one lifecycle controller owns camera permission, playback and capture deadlines.
Permission/playback gets a combined 30-second deadline; capture gets a 120-second deadline.
Explicit cancellation or timeout wins against late success. Late streams are stopped.
R4: track ended, stream inactive, video error, or page hiding terminates capture. Temporary
mute/stall may recover only inside a 10-second bounded stall window; no automatic reacquire.
The controller releases all streams/listeners/timers/animation callbacks on every exit.
D5: UR preflight checks types, declared sizes, fragment geometry and transfer identity before
fountain decoding. Bound 512 KiB payload, 1024 source fragments, 4096 received frames, 4 MiB
scan text. UR sequence numbers are unsigned 32-bit identifiers, not a source-fragment count.
D1: inventory all PSBT raw key/value maps separately from signature verification. Compare
with the prepared PSBT. Classify unchanged, expected signing/finalization, removed, added,
and changed data with a versioned policy. Unexpected metadata is visible and recorded,
not silently green and not called proof of malware. Raw tx has no PSBT metadata to compare.
D2: a completed result is one immutable public snapshot. UI/report/evidence read that same
snapshot. Optional evidence export contains exact imported artifact bytes, full finite text
when applicable, prepared public PSBT, unsigned tx, public keys/input amounts/scripts/digests,
reference transactions, analysis, policy/version and operator labels. No mnemonic/private
key/xprv in export. Public evidence replay verifies mathematical validity and binding, not
secret-key nonce derivation or physical device origin.
D3: one private prepared-test cache keyed by all canonical form/signing-policy state. Changing
presentation does not regenerate signatures. Transaction changes invalidate readiness
immediately. Optional QR re-render can occur independently. Failure stays latched until an
explicit apply/new test/state change; no repeated automatic rebuild of failed state.
D4: compatibility default retained. Explicit optional fixed algorithm selection is possible
before importing a response, invalidates prior work, and is locked on completed tests. No
unverified automatic device-to-algorithm mapping or learning from first signature. Equivalent
reference methods remain visible. Unqualified device/firmware profile certification is absent.
Q1: one offline build from standalone readable application sources and pinned vendor inputs,
not patching an old HTML on each build. Reconstructed sources must be labelled reconstructed;
original author symbols/build metadata cannot be invented. Include inventory, licenses,
source hashes and provenance gaps. Provide explicit operator-owned release signing and
verification tools; no new key may be portrayed as an authenticated TBW publisher key.
Q2: rerun all applicable prior behavior tests, new regressions, independent Python/OpenSSL
oracles, clean builds/extraction/repack, and attempt genuine file/HTTP startup without shims.
Actual signers/cameras, independent organizational reproduction and publisher key custody
require external acceptance. They may not be marked passed by simulation.

## Authoritative modules and boundaries

- src/bitcoin*: trusted BIP84 construction, deterministic references and mathematical verifier.
  Keep the underlying signing algorithms unchanged; use one verifier in all paths.
- src/metadata*: bounded raw-map accounting and expected-change policy, not another signer.
- src/evidence*: public immutable snapshot and export/replay schema; no persistence by default.
- src/qr*: one incoming session dispatcher, protocol preflight, optional BBQr and animation.
- src/camera*: sole camera lifecycle owner; emits data/state, never computes signature verdicts.
- src/application*: one private prepared object, one verified snapshot and existing one-session
  transaction tracker. Alpine fields are projections, not competing ledgers/controllers.
- src/index.html/style: display bindings only. BC-UR/BBQr segmented control retained.
- tools/build.py: one deterministic source assembly path with pinned manifest; no network.
- tests: independent oracles and fault harnesses, excluded from application runtime.

## Trust, privileges and ownership

The browser necessarily knows the disposable test seed. Treat it and the OS as trusted for
this spot check, not as secure storage for savings. No real seeds, funding or broadcast.
Core needs local JavaScript and cryptographic randomness. Camera needs explicit user action
and browser permission; downloads need explicit action. No admin/root, backend, node,
installation service, network fetch, wallet migration, persistent secret store or updater.
Optional transports, camera and evidence downloads cannot change a prepared transaction or
skip signature verification. Failed optional facilities leave file/paste paths available.
Keep existing CSP network prohibition; replacing Alpine/eval is not justified without a
complete equivalent implementation. Do not claim CSP eliminates browser compromise.

## State, reboot, resume, recovery, upgrade and rollback

One HTML page selected by the operator is the active release. Older archives are inactive
rollback material. Close old version, open new version, create a fresh disposable wallet.
There is no persisted wallet migration. Reload or browser loss creates a new wallet. BFCache
restoration may retain the same test but never restarts capture automatically. Hiding the
page stops capture and drops partial responses; restart is explicit. Failed result/import
requires explicit correction/import. Completed snapshot read-only until a new test.
Rollback closes new page and reopens unchanged old HTML with a fresh test. Bootloader,
Bitcoin/Fulcrum, OS service and recovery-boot operations are not applicable.

## Retired operations

Early-break finite import; decoder-error swallowing; app-owned duplicate camera run timer;
indefinite getUserMedia/play pending state; ended-stream active display; unconditional
cryptographic recomputation; mutable completed report composition; build-time HTML patching.
No duplicate legacy parser/controller remains reachable as a fallback.

## Qualification gates and grades

Q0: architecture frozen, unqualified development. Q1: static/contracts complete.
Q2: unit/integration/fault checks complete. Q3: frozen-byte software/browser simulations and
clean reconstruction complete. Q4: actual supported-origin/browser/hardware acceptance,
publisher authentication/provenance and independent reproduction completed. These are local
labels, not industry certifications. External blockers remain individually recorded at Q3.
Development edits precede freeze. A candidate-blocking failure after freeze rejects that
candidate; changes require a new candidate and full fresh acceptance. Results are outside the
frozen archive. Do not edit it to insert postfreeze evidence.
