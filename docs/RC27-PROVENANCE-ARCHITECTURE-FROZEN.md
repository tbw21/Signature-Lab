# RC27: separate historical and current provenance

Historical fixture payloads and original trusted-code SHA-256s are unchanged.
Current UI lineage is pinned to RC26 frozen source for exactly the three changed units (coordinator, page, stylesheet).
The prior archive hash and size are verified independently. Current mutations are rejected. Historical projection output cannot be used as evidence that the current redesigned UI behaves identically.
No signer, verifier, QR, wallet, camera, or journal production code is modified.
No automatic retry or historical assertion deletion is permitted. This change requalifies provenance checks but does not establish independent publisher signing or full prior/current behavior equivalence.
Acceptance: current-assurance A14 passes; negative mutation fails; all old pins survive; other tests still run without relaxed assertions.
