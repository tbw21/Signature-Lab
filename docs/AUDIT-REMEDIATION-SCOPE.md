# Disposition of 13 October independent audit, scoped to v0.20.11 development

This record distinguishes repaired software test behavior from hardware and public-release acceptance. Passing historical tests run on archived source are provenance checks only; live UI behavior requires current source/browser tests. No failure is waived.

1. **Frozen identity and handoff** — Source lock and expected-output file record the current artifact; deterministic source and handoff archives must have accurate manifests, no resource forks, and exact-byte independent rebuild.
2. **Historical static tests** — All eleven historical static jobs now use a hash-checked current-to-archived source provenance bridge, preserve their negative source checks, and separately evaluate current copy, version and architecture through the live current-assurance and current-release contracts.
3. **Historical layout and accessibility** — Replace obsolete exact coordinates and historical color/font strings with contrast, 320–1440px reflow, real 200% text, increased text spacing, 44px targets, high-contrast selection, keyboard/focus and no-clipping requirements. The v0.20.11 stylesheet contains narrowly scoped repairs.
4. **Behavioral browser races** — Test visible UI after a rendered/visible wait, not mere DOM attachment. Keep camera-denied and guided halted behavior terminal; no automatic camera permissions on Results.
5. **Canonical inclusion** — The single qualifier includes current release, UI, privacy, browser, assurance and accessibility tests in `stage=current` before all historical stages. Historical jobs remain present; exceptions and failed jobs are not silently hidden.
6. **Licensing** — The Bitcoin Way copyright line coexists with the original author's notices in the source, HTML and license.
7. **Release** — No RC, publisher signature or public release pointer is asserted by this development handoff. A complete uninterrupted qualification and external acceptance remain gates.
8. **User-reported physical tests** — Thirty SeedSigner 0.8.7 physical runs are prior-operator observations. The exact old HTML hash, run-by-run device/environment/transport/case evidence, and hardware tests on final candidate remain unverified here.

No new signing protocol, verifier, QR algorithm, capture subsystem, or session state controller is authorized by this scope.
