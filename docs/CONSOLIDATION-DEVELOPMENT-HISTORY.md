# Consolidation development record (before candidate freeze)

2026-09-16. The v0.14 reliability HTML/source archive and the separate fingerprint
HTML/source archive were identified and checked against their supplied SHA-256 values.
All four matched. The architecture/acceptance scope was written before implementation;
its initial SHA-256 is d15596128c01371519b44c2db7d8492020c4ab37957541c1783163e129bd1337.
Existing released files were left unchanged; development operates in a separate source tree.

## Reason-linked changes

- Incorporate the fingerprint into v0.14 instead of making the older fingerprint-only
  branch the active release. Its cached-root and zero-preserving behavior is retained;
  asynchronous SeedQR completion is bound to the current wallet/render request to avoid
  advertising an old or unfinished QR. Independent fingerprint/QR-pixel tests cover it.
- Add an optional public-plan generator and a sole historical journal. Replace the old
  writable sessionChecks array with a read-only derived projection so guided and manual
  histories do not become competing stores. Keep one prepared test and current result.
- Bind guided responses to wallet session, full root public key, case identity/number,
  policy and PSBT version. Halt on differences/incomplete/capture/metadata findings.
  No automatic signing, camera start, advancement or uncertain-operation retry exists.
- Add labeled count/preset/start/end/report controls and consistent fingerprint visibility.
  Session summaries intentionally do not retain every original response in memory;
  per-result Save evidence is explicit, and the limitation is described in UI/README.
- Update tests for the retired writable ledger and add the matching contract, browser,
  independent fingerprint and failure cases. Existing cryptographic function tokens and
  all original applicable test assertions are preserved. New tests use generated public
  disposable material, never a real wallet or a purported physical-device execution.

## Incomplete tool runs, not acceptance passes

This execution environment repeatedly ended long directly invoked commands at about
30 seconds despite longer requested timeouts. Initial standalone legacy-unit/regression
and new-browser attempts therefore produced partial logs; a browser range 1-10 stopped
after six passing observations. Those partial runs are excluded from final counts.
Some diagnostic output described completion optimistically in its filename; only an
actual complete JSON result and zero exit code is evidence of completion.

A requested interactive container session returned StreamingExecNotEnabledContainerError.
No interactive session or service was installed. The test suites were split into bounded,
non-overlapping ranges before freeze. A single bounded stage supervisor was then launched
and actively polled during the current response. It invokes the one qualification driver
sequentially, writes outside source, stops on failure and has no automatic retry. The
supervisor is execution bookkeeping, not another runtime controller or build pipeline.

The new application tests use small, explicit disposable transaction fixtures where
transaction size is unrelated to the assertion. Existing six-scenario cryptographic and
PSBT v0/v2 independent tests retain wide transaction-shape coverage. An isolated large
BBQr diagnostic completed encoding/decoding successfully; the earlier direct-command
limit was not a demonstrated application failure. Fixture/probe runs are not counted
again in qualification totals.

## External authentication attempt

An attempt to fetch the pako 1.0.11 npm tarball was unavailable: the download tool required
an opened source URL, and the associated web URL opens were refused. No restriction was
bypassed, no unverified replacement was introduced and the inherited bytes remain pinned.
This does not establish upstream authentication or a vulnerability finding. Publisher
signing keys, external organizational review and actual hardware are not available through
these tests and remain explicit open gates.

## Evidence separation

Development observations are not frozen-candidate acceptance. The qualification record
supplied beside the final candidate must state the actual completed run, hashes, clean
extraction results and unavailable tests. Do not sum development reruns, fixture generation,
QR screenshots or individual signatures already inside named oracle cases as extra passes.

## Final pre-freeze presentation correction

The first complete development run recorded 391 named passes, zero failures and four
unavailable origin/browser cases. Visual review then found the inherited incomplete-result
text suggesting a retry without mentioning a guided session must first be ended. That
text is now conditional on guided state. The transaction toolbar also says Next planned
transaction rather than implying a new random case. Existing browser cases gained explicit
wording assertions; no runtime JavaScript changed in this presentation correction. Static
and affected browser checks are rerun before freeze, followed by full frozen acceptance.
These development rechecks are not added twice to the final count.

The initial release packaging preflight stopped before creating any release artifact
because two development interpreter cache files were present (build.cpython-313.pyc
and tests/oracle.cpython-313.pyc). These generated caches were removed from the unfrozen
working tree. No runtime/test source was changed. The final clean-source preflight and
manifest checks were restarted; no frozen candidate was patched.
