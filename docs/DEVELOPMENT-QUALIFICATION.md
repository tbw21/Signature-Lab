# v0.20.4-dev — Development qualification (not an RC)

HTML SHA-256: `bb77243aff1530ec60a0f66aab10446913c065666ddb0a73436f0629f13cbead`
Original release handoff SHA-256: `16c183865a4c64d3761ac44a7299aeea89cde1f0cdc47c4b9ea9698cfab52cc9`

## Completed on exact development HTML
* Privacy/UX regressions: **9 passed, 0 failed**
* Optional demo isolation: **10 passed, 0 failed**
* Session-state contracts: **38 passed, 0 failed**
* Controlled Chromium setContent 1440px/390px: **6 passed, 0 failed** — not native file/HTTP(S) or actual camera
* Synthetic metadata matrix fixture generation: **32 passed, 0 failed** — successful generation and completed response check, not an independent full replay or hardware test

Total **95 completed pass, 0 completed fail**. Static structural checks: 16 fields, 9 code elements, 136 unique IDs, zero duplicates. These counts are deliberately not the inherited 1,356 checks.

## Not executed / blocking public release
* full baseline 1356-case requalification not executed on this version
* real signer signing / optical QR tests not available
* native file:// and HTTPS hosting acceptance not executed
* Firefox/Safari/WebKit cross-engine tests not executed
* actual mobile camera permission not tested
* publisher key identity, signatures, upstream vendor provenance and independent external code audit not completed
* site deployment and cookie/header/DNS validation not executed
* true memory erasure unprovable for JS strings and browser or OS memory
* power-loss/read-only-full-disk/restart/native installation/recovery scenarios not exhaustively tested

## Historical interruptions
* An earlier metadata-fixture run was interrupted at 45 seconds; the final-byte full 32-case generation completed successfully.

## Release policy
The original v0.20.3-rc1 archive was neither modified nor replaced. This development snapshot is unsigned and has not entered frozen release-candidate acceptance. A future RC must restart the 10-gate qualification, freeze its final archive SHA-256 before hardware acceptance, and never be patched in place after that.
