# RC28 qualification architecture freeze

Baseline: frozen RC27 preflight; never modify its bytes.

Trusted runtime: unchanged application and vendor JavaScript; no verifier, signing, QR, camera, import, or session journal changes.
Presentation: 44px visible header navigation targets, first Help topic return link.
Test harness: accessibility navigates using visible Settings drawer and Back to test, asserts reflow, 44px targets, 200% font, spacing, forced colors, keyboard and focus return.
Provenance: historical snapshots/hashes retained. RC28 presentation bytes explicitly reviewed and pinned in tests/current_to_historical.py. Exact hashes: 
- src/page.html = cc24ed0d0de48de6ba9d0e2d73888201a56acd6b4385b63e418fa04c55988425
- src/style.css = 9a2c9a385a9082c5915e7ea2b5d252b3ee11775f4d47fcf875c2f06301f9111f
- src/20-application.js = 4ded7810831f8f841fdde9c9c3f3e94c808eb25605de995c53297c6ab8fcb26d

Privilege: offline tests only, no network, device or installer writes.
State: source-lock.json authoritative build source integrity; release.json authoritative release status; EXPECTED-OUTPUT.json authoritative output check; immutable candidate hash only after freeze.
Recovery/rollback: RC27 remains untouched, no auto retry or mutation of frozen candidate.
Retired: hidden workspace navigation is not a supported test path; archived tests remain available in frozen RC27.
Acceptance: full canonical 139 jobs required for software qualification; native file and hardware remain distinct gates.
