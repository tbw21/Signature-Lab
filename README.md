# Signature Lab v0.20.0-rc1

Offline signature spot checker for disposable BIP84 P2WPKH single-signature wallets.
Never enter real wallet words, fund generated addresses or broadcast test transactions.
A matching response is not firmware certification or proof of a physical-device operation.

## Current scope

This candidate starts from the exact v0.19.0-rc1 HTML and source archive. It adds optional bounded
session evidence retention, diagnostic packages, independent psbt-envelope-v3 replay, critical browser
workflow automation and a targeted deliberate-defect campaign. The main layout, signing calculations,
metadata policy, QR codecs, camera controller and startup self-check are unchanged.

One coordinator, immutable result and session journal remain authoritative. Retention is off by default,
stays in the open tab and uses the existing public evidence exporter. No storage permission, upload,
network integration, new signing method or vendor replacement is introduced.

See docs/EVIDENCE-ARCHITECTURE-FROZEN.md, docs/EVIDENCE-SCOPED-REVIEW.md and
 docs/EVIDENCE-FIX-MATRIX.md. The separate qualification report identifies the exact accepted bytes,
completed checks, failures, unavailable environments and limits; old version totals are not current passes.

## Normal workflow

Load the displayed test words on the signer without an extra passphrase. Compare the fingerprint, then
choose Wallet confirmed. Review all destinations, amounts and fees on the actual signer before signing.
Scan, import or paste its response; all paths use the same verifier. Results exposes unfinished intake
but camera access requires Scan signed QR. Reselecting Results during capture preserves that scan;
navigating away stops it. Completed results are read-only and failures remain explicit.

The two navigation groups do not deliberately scroll the page downward. Wallet confirmed is a task
action and reveals transaction review after a long mobile wallet page. The Dark Skippy example checks
a recorded attack, not the user's device. It does not replace the wallet or increase test counts.

New test wallet is beside the word-length selector. Replacing a used wallet asks before clearing its
result and history. Cancel/Escape preserve them. Active guided sessions must be ended first. Ending a
session removes its active banner, not its history or unresolved findings.

## Save evidence without losing earlier responses

In **Session -> Session evidence & diagnostics**, enable **Keep result evidence in this tab** before
importing responses. **Save session evidence** contains the retained original public result envelopes,
immutable findings, attachment hashes and explicit completeness information. Turning it on later cannot
recover earlier responses; turning it off keeps existing attachments and marks future gaps.

The logical budget is 16 MiB of UTF-8 serialized payloads and 256 retained responses. It is not a total
browser-memory bound. There is no eviction. Budget or retention errors latch for the wallet lifetime,
remain visible, and do not weaken verification. Export existing data and use the normal confirmed
new-wallet flow to start again. A reload/new wallet resets the in-tab state. There is no crash-resume,
automatic disk save, remote backup or secure-erasure claim.

**Save result** continues to export the current result. **Save summary only** and **Save session record**
remain summaries, not original-response archives. Save each result before advancing when retention is
off or incomplete. Completeness means supplied recorded checks, not proof that every planned operation
occurred. A download event is not proof of a successful final OS write: open and verify the saved file.

Capture-attempt summaries are recorded only while retention is enabled, at most 256 diagnostic entries
with an omitted count. They do not consume the 2,000 core check/control slots or inflate signature counts.
A failed guided capture and its control-halt entry remain two history records for one stopped operation.
These records do not claim every raw optical observation or device-signing attempt was captured.

Diagnostic packages exclude raw frames, response bytes and exception messages by default. Including the
current response requires explicit choice. Operator notes are unverified. Runtime exports do not add the
locally held seed/private keys, but original returned data and human notes can contain hidden or sensitive
information. Review them before sharing. Nothing is uploaded automatically.

## Independent replay

```
python3 tools/replay_evidence.py saved-result-or-session.json --output replay.json
```

The one existing entry point checks transaction binding, signatures, consistency with saved public
references, and independently reconstructs **psbt-envelope-v3** metadata from original public bytes.
It covers the supported generated PSBT v0/v2 conversion shapes, field classification/hashes, positions
and retained-field order. Unknown policy versions or unsupported reconstructions are rejected.
Session bundles are checked for attachment identity, hashes, declared gaps and worst-observed counts.
Incomplete retained results are identified, not counted as cryptographically replayed.

Replay does not authenticate a reference or publisher, reproduce secret-key nonces from seed-free data,
attest hardware origin, establish that omitted history never existed, or certify firmware. Input is
bounded to 32 MiB of bundle JSON; raw transaction/PSBT limits remain 512 KiB. The tool runs offline and
does not execute the application or any embedded input code.

## Rebuild and compare

Python 3.10+ is required for the build. All runtime inputs are bundled; no npm/runtime download is needed.
Outputs must not already exist.

```
python3 build.py /absolute/path/new-rebuild.html
python3 tools/verify_output.py /absolute/path/new-rebuild.html
python3 archive.py /absolute/path/source /absolute/path/new-source.zip
```

EXPECTED-OUTPUT.json records the version, size, HTML hash and build-input identity. It is included in the
source archive but excluded from HTML build inputs to avoid circular hashing. One source list, lock,
assembler and archive tool remain authoritative. Only during editable development, before freezing:

```
python3 tools/lock-source.py --development-update
```

Hashes establish consistency, not publisher identity. The release remains unsigned unless separately
authenticated by the publisher. Inherited vendor chunks remain unauthenticated against upstream.

## Prepare and run qualification

Use a dedicated environment without real wallet secrets. Install the exact versions in
qualification-requirements.txt. The retained suite also needs Node, system Chromium, OpenSSL and libzbar.
Record the actual OS/tool versions. Python aliases must resolve to the same prepared environment.
Neither test setup nor the application silently installs prerequisites.

```
python3 -m pip install -r qualification-requirements.txt
python3 qualify.py HTML SOURCE_ARCHIVE RESULTS --list-jobs
python3 qualify.py HTML SOURCE_ARCHIVE FRESH_RESULTS --stage all
```

For bounded execution, run the environment job once, then each canonical job exactly once in order with
--job NAME. Keep fixture producers before consumers. Results must be outside the source tree; existing
reports are never overwritten. Do not run --stage all over a previously used result directory. Failed
or unavailable environments are not passes; no operation is retried automatically. Prerequisite pins
are not authenticated wheels or a hermetic OS image.

```
python3 tests/origins.py HTML FRESH_ORIGINS_JSON --require-all
```

The origin runner actually executes critical workflows on installed engines via normal file/loopback
navigation. Missing engines and administrator-blocked modes are unavailable. It is not the entire
retained suite on every engine, branded Safari, mobile OS, actual permission/optical or signer acceptance.
The additional eight-mutant campaign records detected, escaped and invalid cases separately; malformed
mutants are not successes. Historical source projections check declared preservation only; behavioral
tests execute the actual current HTML. No test count is an attack-detection probability.

## Delivery, lifecycle and remaining gates

Freeze HTML, source and tests before acceptance; a blocker requiring changed bytes means a new candidate
and a complete restarted qualification. Never choose an older release as an automatic
fallback: use a separately accepted rollback release and exact identity, or withdraw the affected copy.
Reload starts fresh and cannot undo an operation already performed on a signing device.

Use docs/EVIDENCE-HARDWARE-ACCEPTANCE.md with docs/HARDWARE-ACCEPTANCE.md. Physical/native-browser
acceptance, publisher signing, dependency provenance/security review, independent organizational review/
rebuild, comprehension studies and original Foundation orange-response evidence remain separate gates.
The vendor/CSP migration is investigated but not implemented; see docs/DEPENDENCY-REFRESH-GATE.md.
There is no new website deployment or publisher key. The startup gate cannot authenticate a hostile
page/browser or prove later firmware behavior.

## Source history, not current qualification

v0.18.5 continued the recovered feedback-refinement dev-3 preview; see
 docs/FEEDBACK-ARCHITECTURE-FROZEN.md and docs/RC2-HARNESS-ARCHITECTURE-FROZEN.md for that history.
v0.19 addressed the independent source audit; see docs/SOURCE-AUDIT-DISPOSITION.md. Historical versioned
addenda and fixtures are retained for traceability, not instructions to install their old candidates.
