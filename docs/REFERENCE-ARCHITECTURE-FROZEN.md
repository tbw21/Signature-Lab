# Reference audit correction: frozen implementation contract
Version: 0.17.0-rc1. Baseline: exact v0.16.4-rc1, SHA256 3042da6b7ea353054b49c0bd4329989e25c62a9c7cf7303df333924d68d4f3e2.

## Requirements and acceptance
1. Independently reproduce every supplied vector (16 keys/digests, three methods each) before using it as an expected result. Expected bytes are literals, never generated from the implementation under test at runtime.
2. Before constructing the first disposable wallet/application state, run one mandatory known-answer check: all 48 signatures, valid-signature checks and wrong-message rejection. Use only published disposable vector keys. No network, randomness, filesystem, camera or wallet access is needed by this check.
3. Any mismatch, exception, reentrant execution or exhausted cooperative time budget latches a terminal startup failure. No application or camera starts; no normal result can be issued. No in-page retry/reset. Explicit reload of verified bytes starts a new lifetime.
4. A successful gate runs once per page lifetime, not per transaction. An immutable status is available in existing technical Help; no new default-view reassurance badge or green firmware certification.
5. Preserve exact signing math, accepted method IDs/defaults, transaction generator, metadata rules, QR/camera, session journal, evidence contents and offline permissions. Clarify DER-length versus strict low-R in Help. Keep compatibility-channel and conditional-attack limitations.
6. Record BIP 461 as a Draft whose publication/merge were verified; do not assert full conformance or automatic device qualification without the complete pinned specification/firmware chain. Do not change defaults or rename IDs.
7. No Taproot implementation, device-name exceptions, two-input minimum, automatic signing retry, upload/external submission or camera keepalive in this stabilization change.
8. Retain the calm UX, one-line desktop gold purpose copy, all warning visibility, read-only output review, evidence exports, Help contents and optional example. Run all retained tests plus new startup/fault/independent/boundary cases. Assert exact authorized changes by reversible projection against baseline, not by replacing old golden hashes.

## Architecture and authority
One source module src/reference-self-test.js owns one private immutable lifecycle and fixed literal vector set. It calls the existing Op/qc implementation; it is not a second production verifier. Fv invokes apply/verify before any application seed, journal or random transaction is created. Existing startup-error rendering projects its terminal status. An application getter reads that same status for technical Help; there is no separately mutable status field. One existing build.py, qualify.py, source lock, module order and release.json remain authoritative.
Inspect/status are read-only snapshots. Plan describes fixed operations/budget, apply is once-only synchronous work, verify requires success, rollback explicitly does not reset a failed test. This is startup fault detection, not code/publisher authentication, continuous runtime monitoring, entropy testing or proof against a malicious browser that can replace the checker.

## Privilege, ownership, optionality
Local browser execution only. No added dependencies, permissions, persistent storage, user-key exports or external connections. Public known-answer keys never replace the generated wallet. Help and demonstration stay optional and cannot reset or satisfy the startup gate. Publisher keys remain operator-owned and unavailable here.

## Lifecycle/recovery/upgrade
Failure stays terminal; no automatic retry. Fixed finite 48 comparisons; existing signing loop has a finite counter bound. A cooperative 10-second elapsed-time check occurs between operations, not a hard preemptive timeout for a hung JS engine. Reload constructs a fresh module lifetime. Closing/rollback does not undo a device signature. Upgrade/rollback uses untouched versioned files and fresh disposable wallets; no seed/session migration. OS boot, installed services and storage migration are not applicable.

## Retired behavior
Starting wallet generation without exercising literal reference vectors. No existing verification or transport path is retired or replaced. Historical preservation tests project only the authorized startup/Help additions; independent new preservation tests require every other original source byte to match.

## Release qualification
Freeze HTML/source ZIP/manifest before acceptance. No edits during acceptance. A candidate product/test blocker disqualifies that candidate; restart on new bytes/version. External missing hardware, publisher signing, complete dependency provenance, full exact-version firmware/source verification and independent organizational audit remain separately reported. Source-only review is not device acceptance. Preserve all prior releases.
