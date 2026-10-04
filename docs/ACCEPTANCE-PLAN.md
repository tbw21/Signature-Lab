# v0.15 consolidated candidate acceptance plan

The implementation contract is CONSOLIDATION-ARCHITECTURE.md (frozen before coding).
Inherited v0.14 contracts remain applicable except the historical writable sessionChecks
array is replaced with the new journal projection. Core signing/reference algorithms
and the sole camera controller remain unchanged. No device simulation is a runtime mode.

## Before candidate freeze

Finish development static/syntax, unit/contracts, integration and fault tests. Exercise
individual and guided workflows, orphan/stale callbacks, plan count/binding limits,
readiness/fingerprint states, optional planner absence and terminal failures. Independently
calculate BIP32 fingerprints and decode actual generated SeedQR pixels. Retain all legacy
crypto, transport, metadata, evidence and reconstruction tests.

Complete code and docs, update the development source lock, generate the internal manifest,
build one versioned HTML and deterministic source ZIP. Record both SHA-256 hashes and the
freeze timestamp outside the archive. Previous release files stay untouched.

## Exact-byte acceptance

Extract that ZIP into a new directory. Reject absolute/traversal/duplicate/non-regular
paths before extraction. Verify CRCs and every manifest entry. Use the exact separately
built HTML and source ZIP. Run qualify.py with results outside the clean extraction:

- static: syntax, assembly/no older-HTML input, single-implementation/source invariants;
- core: all retained BBQr cases, audit regressions and camera lifecycle contracts;
- browser: retained workflow, QR pixels, current evidence/metadata and lifecycle simulations;
- sessions: new plan/journal contracts and actual-HTML guided/fingerprint/browser cases;
- independent: six crypto scenarios, v0/v2 PSBT structure and public replay/tampering;
- tools: operator-owned release-signing/vendor-comparison utility tests using test material;
- package: exact clean builds/repack, tampered inputs, overwrite/concurrent/interrupted
  publication and filesystem-boundary failures;
- origins: attempt actual file/HTTP startup and installed alternate browsers, reporting
  unavailable cases separately rather than passing the harness as deployment acceptance.

The driver bounds subprocesses, refuses previous result paths, stops on failure and checks
candidate identities after each stage. A candidate blocker disqualifies those bytes. Do
not change tests, HTML, archive or sources during acceptance; fix a new candidate and restart.
Afterwards verify both candidate hashes and the entire clean-extraction manifest again.

## Scope and reporting

Treat fresh browser context as a fresh-install simulation; live transport/unit changes
as populated-session adoption; close/open version changes as upgrade/rollback; and page
loss/Back-Forward lifecycle as recovery simulation. No persistent wallet migration or
boot/node/Fulcrum/storage install exists. Real power loss, read-only mounted filesystems,
full disks and actual signer interruptions remain physical checks, not implied passes.

State completed named passes/failures, incomplete timeouts, unavailable checks and actual
physical operations separately. The 200-case journal test uses synthetic summaries, not
hardware. The six independent crypto cases include individual signature checks that are
not counted again. No software counter grants firmware confidence or hardware certification.

Outside trusted provenance, publisher signature, independent organizational review and
real device/browser/optical acceptance must be recorded through OPEN-GATES.md and
HARDWARE-ACCEPTANCE.md before broader promotion.
