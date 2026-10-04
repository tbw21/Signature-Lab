# v0.15.2-rc1: QR acquisition and returned-file interpretation
Architecture/requirements frozen before implementation, 16 September 2026.

## Exact basis and non-goals
Authoritative implementation base: supplied UX source archive (SHA256
17ceb20c3ae58e59e6b3e9bb779ffb0862aecad39f19c9cc8d7deb14c85a4267).
It rebuilds the exact dev-2.html (cee33c352cd226fad2ef7ec5764355655dec64a2f07388541327e23800f72e8e).
The current v0.12.2 attachment is a retained reference, NOT the implementation base.
Retain all UX progressive disclosure, guided-session, fingerprint and reliability work.
The actual failed QR payload and expanded metadata details were not supplied. Correct
reproduced software limitations; do not claim diagnosis of the exact hardware incident.
No new firmware runner, signing algorithm, bypass of signature checks, secret persistence,
network permission, device-name allowlist or claim of hardware certification.

## Requirements and acceptance
R1: Classify malformed Bytewords, checksum rejection and internal decoder errors separately.
Official Bytewords vectors, independently produced frames and corrupted vectors must verify
expected behavior. Checksums, sizes, transfer identities, equations and semantic verification
remain enforced. Never repair, guess or normalize corrupt bytes into acceptance.
R2: Camera-only frame acquisition may reject a damaged frame before admission and continue
in the SAME scan. This is the only new explicitly retryable operation: at most 7 consecutive
and 23 total rejections, followed by terminal failure at 8/24. Every rejected observation
counts against existing frame/text/time budgets. Surface rejection counts while scanning,
in completed evidence/reports and in downloadable diagnostics. A checksum-valid but
conflicting frame, message checksum failure, internal error, limit, malformed fountain header,
mixed transfer or signature failure remains terminal until explicit operator action.
Finite paste/file imports remain strict; no content is dropped. No camera reacquisition.
R3: Recognize only a narrow fully reduced signature-only PSBT envelope, with all required
transaction fields and signature fields retained, no unknown/proprietary additions and
uniform supporting-field removal. This is field accounting, not proof removals carry no
information. Only a successful existing semantic/signature verifier can produce a completed
result. Modified supporting fields and selective removals remain review findings.
R4: Expected cleanup gets neutral language; unexpected additions/changes get a visible amber
review result even when signatures match. Reports distinguish signature result from overall
review status. Raw transactions explicitly have no PSBT metadata comparison. No global
suppression of metadata, device-name exemptions or clean-bill-of-health wording.
R5: Preserve beginner default, discoverable advanced tools, responsive reflow, keyboard
access, essential visible warnings, immutable result and same-key fingerprint. No unrelated UI.
R6: Include complete retained regression suite plus new transport, metadata, guided-session,
report, source-preservation, browser and corruption cases. All completed/failed/unavailable
runs recorded separately. Final candidate frozen before clean-extraction acceptance; any
candidate blocker requires a new candidate and restart.

## Boundaries, state, privilege and lifecycle
Trusted core is src/04-bitcoin.js plus its pinned primitive dependencies. It remains unchanged.
One QR session owns admission, counters, transfer identity and terminal errors; one camera
controller owns capture and deadlines. UI projects state, never generates another verdict.
One prepared test, one immutable result, one existing attempt journal; no new persistent
ledger. A shared finding-status function supplies UI/report scope, not cryptographic logic.
Diagnostics contain counts/codes and build ID, not raw QR strings, seeds or private keys.
Camera permission remains explicit; no privileges beyond the existing offline file.
One release.json defines identity. No former release bytes are edited or replaced.
Reload begins fresh. Pagehide/back-forward and late callbacks retain existing no-restart
behavior. Upgrade/rollback means closing the old file and opening a retained/new one with
a fresh disposable test; no seed/session migration. There is no OS installer/boot recovery.
Optional evidence export failure cannot change a verdict. No automatic retries of signing,
verification, failed sessions, dependency failures or camera startup.

## Explicit retirement
Retire the catch-all frame-checksum label, first-corrupt-camera-frame terminal policy and
large green combined result for unresolved file findings. Keep strict finite-import and
message-error latches. Preserve historical implementations only as immutable test fixtures.
Retire the UX-only no-change assertion for the explicitly changed modules, replace with
change-allowlist and token-level preservation for every unaffected operation.

## Remaining gates
No physical SS/CCQ, original failing response, authentic upstream vendor bytes, publisher
key or external reviewer is supplied. Normal-origin tests attempted without bypassing
policy; unavailable platforms cannot be counted as passes. Complete software tests are not
hardware acceptance. Diagnostic UI/manual tests cannot attest a physical signer.
