# v0.20.10 qualification harness stabilization — frozen scope

## Scope / requirement
Qualify the exact frozen v0.20.10-dev HTML and locked runtime from the 13 October audit. Repair only the qualification harness and its fixtures; no runtime, template, CSS, build-tool, or source-lock change. Do not promote to RC while any canonical job fails, times out, or remains unavailable. Keep original audits and failures intact.

## Authoritative sources
- Exactly one application build (`build.py`) and its `source-lock.json`, `EXPECTED-OUTPUT.json` and immutable external HTML checksum.
- One canonical test runner (`qualify.py`); no second release pointer or alternate verdict engine.
- Current-source semantic checks own assertions about current UI and behavior; historical source reversal tests are provenance-only, explicitly labeled and barred from substituting for current acceptance.
- Historical baseline bytes must originate in a verifiable archived source package and are checked on both input and output hashes. Every unknown or altered current source must fail closed.

## Boundaries
- Trusted core: unchanged cryptography, PSBT parsing, QR/camera, startup self-test, coordinator and session journal. Historical projection and test fixtures cannot execute or mutate this code.
- Optional: visual, browser and provenance tests must not affect application behavior.
- Ownership: operator decides release, publisher signing, hardware/optics, independent audit. Automated tests cannot claim hardware acceptance.

## Failure / state model
Each test produces an immutable per-hash result. Errors, timeouts, skipped tests and unavailable browsers are separately reported. No silent retries. A failed campaign is disqualified; fixes occur only in a new qualification-harness candidate followed by a fresh run. Before RC freeze, harness changes are allowed; after freeze neither bytes nor tests change.

## Test and acceptance contract
1. Source lock, build hashes and frozen HTML identity verified before any tests.
2. Current semantics, CSP, source trust boundaries and anti-tamper checks pass on exact current bytes.
3. Historical provenance tests may run for regression history but must not be promoted into current behavior claims.
4. Current reflow, doubled text, increased text spacing, forced colors, keyboard/focus, camera-denied and workflow checks pass in a bounded browser matrix.
5. Full canonical runner, followed by clean extraction and replay, must complete without unqualified assumptions or exceptions.
6. Real hardware, native browsers, publisher authentication and external review remain external gates; don't invent acceptance results.

## Explicitly retired behavior
Do not assert current source equals pre-0.20.4 bytes, current release is v0.20.3, or current copy exactly equals an older product label. Historical identities remain archived as provenance; their current security intent gets separately tested.
