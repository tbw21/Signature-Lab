# v0.17.0-rc1 reference-audit correction

See docs/REFERENCE-ARCHITECTURE-FROZEN.md, REFERENCE-AUDIT-DISPOSITION.md and REFERENCE-SOURCES.md.
A mandatory48-answer startup check gates wallet generation. Earlier qualification sections below
are historical scopes, not this release's current acceptance totals. The current driver lists
its authoritative jobs with `--list-jobs`. No source/runtime network downloads required.

# The Bitcoin Way Signature Lab v0.16.4-rc1

Calm workspace release candidate, based on the actual delivered 0.16.0 development
preview and the complete v0.15.2-rc1 source/test package. The subsequent claimed calm-work
source checkpoint was not available. This package recovers the concrete preview and
qualifies fresh changes; it does not claim those missing test outputs were recovered.
Historical documents and previous HTML fixtures are retained for traceability only.
The separate, exact-hash qualification report establishes which checks completed.

**Never use a real/funded seed, fund generated addresses, broadcast invented transactions
or weaken signer protections.** This checks supplied signatures for one BIP84 P2WPKH
transaction against supported deterministic references. It cannot certify firmware or
prove the origin of a response. This source contains no firmware simulator.

## Copy and scope refinement in 0.16.4

The introduction is one gold paragraph without a forced line break. It fits a normal-width
max-container desktop view and wraps naturally on mobile or enlarged text. The published
Dark Skippy example is named as an example of a signature deviation, never as a guarantee
that all variants are detected. The result limitation explicitly preserves the possibility
of seed leakage or other attacks after a matching spot check.

The master-key/no-passphrase note is moved from below the wallet fingerprint into the
existing **Technical details and expected signatures** FAQ. The fingerprint itself stays.
All 29 runtime JavaScript units and the builder are byte-preserved from 0.16.3. Scope,
regression requirements and unchanged lifecycle rules are in docs/COPY-ARCHITECTURE-FROZEN.md.

## Onboarding and Help in 0.16.3

The exact starting point is the frozen v0.16.2-rc1 source archive. All 29 runtime JavaScript
units remain unchanged. A two-sentence purpose statement describes the signature check
and its limits. Step 1 offers an optional **Try example** shortcut to the one existing,
isolated published-attack demonstration. Checking it does not run firmware, replace the
disposable test, change its history or become a physical-device test.

Help now has five native expandable Contents groups covering all 22 canonical questions.
The builder generates titles/targets from the FAQ source, so there is no second maintained
question list or runtime menu controller. **Back to contents** preserves current test state.
The two camera questions now distinguish permission retention from capture lifecycle.

**What does an orange result mean?** distinguishes a signature match with unresolved file
changes from incomplete verification and pre-verification scan failures. Secondhand feedback
about Foundation Prime does not supply the original orange-result data. No metadata,
cryptographic or device-name acceptance rule has been changed to suppress those findings.
See docs/ONBOARDING-ARCHITECTURE-FROZEN.md and docs/ONBOARDING-HARDWARE-ACCEPTANCE.md.

## Retained alignment refinement in 0.16.2

Workspace navigation stays right-aligned in Test, Advanced and Session. Panel action
rows use a consistent trailing edge. Mobile rows may fill available width without
reversing tab order or squeezing touch targets. Seed-loading instructions are left-aligned
beneath the words, while Enlarge/Reduce QR stays right-aligned beside its code. Normal and
enlarged QR use the same existing state/rendering; all runtime JavaScript is unchanged.
See docs/ALIGNMENT-ARCHITECTURE-FROZEN.md for exact scope and acceptance criteria.

## Retained workspace features

- Consistent labelled Test / Advanced / Session navigation, including equal-size mobile controls.
- A compact main workflow; editing, planning and device notes have their own Advanced space.
- Read-only review of every output's full destination, exact amount, role and order.
- Normal reduced-response explanations in technical details/FAQ; unresolved findings stay visible.
- Save result prioritizes full current public evidence; explicit summary-only export remains.
- Short content-derived export names; wallet/transaction/policy are unchanged by navigation.
- Historical review/incomplete findings stay discoverable after later matching checks.

## Beginner and power-user workflow

Start in Test. Load a generated disposable wallet on the actual signer and compare its
master fingerprint. In Transaction, compare amounts and **Review all outputs** with
the physical device before signing. The QR and review share the same prepared test.
BC-UR/BBQr are transport choices only. File/paste/Specter/static import paths remain.

Advanced holds the guided-session planner, transaction settings and optional report
labels. Selecting Advanced does not create a different verifier. Nondefault policy,
PSBT or edited-transaction indicators remain visible. Session shows the existing journal,
scenario counts and earlier findings. Merely switching view does not change the wallet,
transaction, locked policy, completed result or history. Stop capture before switching.

A guided session fixes 1-200 public cases (20/50/100 shortcuts) before its first attempt.
You must operate the physical signing device for every case. No hidden automatic signing,
retry, skip, advancement or camera start occurs. Differences, unexplained file findings,
incomplete data and terminal camera failures halt progression until explicit End. End
preserves its record, does not undo device signing and permits manual investigation.

## Save useful evidence

**Save result** uses the existing current-result evidence exporter when evidence exists;
it otherwise saves an explicitly incomplete summary, never a fabricated success. The
technical disclosure also offers **Save summary only** and **Save evidence**. Examples:
`detail-7a83c9d04e12.json`, `record-5f276bc810a3.json`, `journal-481c7fd209ba.json`.
The suffix is the first 12 hex characters of the full file SHA-256. This is a short name,
not an authenticity signature, collision-proof identity or stealth defence. Full build
identity and findings stay inside. The browser download name is not added to a signer QR.

The evidence export deliberately excludes locally held seed/private/root keys. Returned
bytes are untrusted and could themselves contain hidden information. Review before
sharing. **Save each result before advancing**: session export is a history of summaries,
not a complete archive of earlier responses. Nothing persists automatically. Reload/new
wallet loses the tab's state; no secret crash recovery is provided.

## Preserved QR, camera and returned-file rules

Known invalid Bytewords camera observations are excluded before decoder admission within
8-consecutive/24-total and time/resource limits. Corrupt complete messages, mixed/conflicting
transfers and internal errors stay terminal. Finite file/paste imports consume all data
strictly. A narrow uniformly reduced PSBT remains expected only after full existing
transaction/key/signature checks. Unknown additions or unexplained alterations stay amber.
No wallet brand/name exempts data. One metadata policy, verifier and camera controller remain.

The camera is released after a response or stop. Browser permission retention is outside
the page's control. No quiet persistent camera or global permission workaround was added.

## Evidence and qualification limits

The user's final report records 21 matches with v0.15.2-rc1, reported as physical SeedSigner
0.8.7 use. It contains summaries, not 21 original responses. That is not acceptance of this
new build, independently replayed cryptographic evidence or a measured detection rate.
Actual SS/CCQ optical/browser acceptance, outside review, publisher signing and complete
upstream dependency authentication remain separate gates. See docs/CALM-HARDWARE-ACCEPTANCE.md.

## What this source package is

The build directly assembles checked-in JavaScript modules, template, stylesheet and
pinned vendor bytes. It does not patch an older HTML or use test fixtures as runtime
fallbacks. The inherited application/vendor sources were reconstructed from rc2, not
recovered as the original TypeScript, dependency lockfile or upstream build pipeline.
Complete dependency provenance and independent organizational review remain outstanding.
See `docs/OPEN-GATES.md`, `docs/DEPENDENCIES.json` and `docs/CONSOLIDATION-ARCHITECTURE.md`.

## Rebuild without network access

Use Python 3.10+ on a filesystem supporting atomic hard links and directory fsync.
Linux is the recorded qualification environment; other build platforms need acceptance.
No npm installation, network, old HTML or build-time JavaScript bundler is required.

```sh
python build.py /absolute/path/to/a-new-output.html
```

The destination must not exist. The build verifies `source-lock.json`. The embedded
source identity identifies locked assembly inputs; the final HTML digest is separate.
Unsigned hashes show consistency, not publisher authenticity. Only an unfrozen development
candidate may update its source lock explicitly:

```sh
python tools/lock-source.py --development-update
```

Any blocker during acceptance disqualifies that candidate. Fix under a new release
identity, freeze new bytes and restart qualification. Never edit a frozen candidate.

## Reproduce the applicable software qualification

Python packages: playwright, Pillow, qrcode, pyzbar/libzbar, cryptography. Node.js 22+ and
Chromium at `/usr/bin/chromium` are used by the test harness. Acorn is test-only vendor
code. `docs/TEST-ENVIRONMENT.json` is an inventory, not an authenticated dependency lock.
No tools are installed automatically.

```sh
python qualify.py /absolute/path/to/candidate.html /absolute/path/to/source.zip /absolute/path/to/new-results
```

The single qualification driver runs bounded stages and refuses to replace previous
results. It can also run each stage separately with `--stage static`, `core`, `browser`,
`sessions`, `ux`, `remediation`, `calm`, `alignment`, `independent`, `tools`, `package` or `origins`. It does not patch/retry candidates.
Tests write outside the clean source extraction. Inspect failed, incomplete, skipped and
unavailable observations separately. Disjoint test ranges are not additional reruns. In a tool environment with a short
command limit, select one named job, for example:

```sh
python qualify.py /path/candidate.html /path/source.zip /path/new-results --stage browser --job browser-1-20
```

A job receipt explicitly says it does not certify its entire stage. Reuse the results
folder for different jobs, never overwrite a result. Fixture-producing jobs must precede
their independent replay/structure jobs. Invalid job names fail rather than recording a pass.

The Chromium harness loads exact HTML using about:blank/document.setContent and synthetic
camera streams. New code needs no UUID shim. An old rollback fixture uses a shim only in
that restricted harness. Browser simulations, public reference-response fixtures and
controlled-clock tests are not actual device or optical acceptance. The 200-case journal
simulation is a controller test, not 200 physical signing operations.

## Inspect current-result public evidence independently

```sh
python tools/replay_evidence.py saved-evidence.json
```

This Python/OpenSSL tool checks public data, transaction binding, signature validity and
consistency with saved public references. It does not authenticate the evidence or those
references, recreate secret-key nonces from public data, rerun the metadata policy, attest
hardware origin or certify firmware. The compact session-summary format is not an input
to this per-result replay tool. Unexpected metadata remains available for inspection in
the separate original-response evidence.

## Authenticate releases and dependencies

An authorized publisher must sign the final checksum manifest with its own trusted key.
No TBW signing key is invented or included here.

```sh
python tools/release_auth.py sign SHA256SUMS.txt --fingerprint FULL_TRUSTED_FINGERPRINT --signature SHA256SUMS.asc
python tools/release_auth.py verify SHA256SUMS.txt --fingerprint FULL_TRUSTED_FINGERPRINT --signature SHA256SUMS.asc
python tools/verify_vendor.py independently-authenticated-pako-1.0.11.tgz
```

Obtain the signing-key fingerprint through an independently trusted channel. A matching
key beside an untrusted download is insufficient. The vendor tool compares an authenticated
upstream tarball without executing it; a fabricated matching tarball only tests the utility.
Release-tool tests use throwaway keys/synthetic archives, not TBW or upstream authentication.

## Upgrade, rollback and recovery

Save needed reports, close older pages, open the consolidated HTML and create a fresh
wallet. The opened HTML is the active release; old files are retained archives, not
competing controllers. This release supersedes the separate fingerprint branch for
consolidation testing, without importing that branch's older camera/QR implementation.

Reload/crash loses memory. No crash-resume or persistent wallet migration is claimed.
Explicit End stops page capture but cannot undo an operation already performed by the
signing device. Never automatically repeat an operation whose hardware outcome is unknown.
Rollback is close-and-open of the untouched baseline with a fresh disposable test, not a
rollback of device signing. An interrupted build may leave an unpublished temporary file;
explicit execution to an absent destination is safe, with no partial publication.

See `docs/HARDWARE-ACCEPTANCE.md` before any broader promotion. Real scan-speed tuning,
repeat-signing diagnostics and certified device/firmware profiles are deliberately deferred
until physical qualification and measured workflow evidence justify them.
