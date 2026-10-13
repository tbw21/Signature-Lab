# Signature Lab v0.20.5-dev — pre-implementation scope freeze and acceptance contract

**Status:** developmental. Not a release candidate. Original v0.20.4-dev application (SHA-256 `bb77243aff1530ec60a0f66aab10446913c065666ddb0a73436f0629f13cbead`) is frozen and preserved.

## Requirements, scope and measurable acceptance
1. Correct a demonstrably inaccurate public-release claim in the v0.20.4-dev header accessibility label, tooltip and visible Help. Say **development preview**, no public approval, no hardware acceptance, no independent publisher authentication or audit, and no firmware certification.
2. Advance the embedded and source version to `0.20.5-dev`, preserving the established 0.20.4 application behavior, verification results and privacy UX without a new feature.
3. Exact source-pinned allowlist: `release.json` and `src/page.html` are the only changes among all build inputs. Three unique HTML-template string substitutions must reverse to byte-for-byte verified 0.20.4 template. Release metadata changes are explicit and hash-locked.
4. Validate real browser rendering and accessibility labels, not just source copy. Ensure missing/forged approval text is detected by negative tests.
5. Produce a deterministic, independently reproducible single HTML and source handoff with **WHAT'S NEW**, raw tests, SHA manifest and clean-extraction receipt. Keep the release pointer unset.
6. Report every failure, timeout, unavailable tool, skipped gate and unfinished hardware/security acceptance separately.

## Trusted core and module boundaries
Only the `src/page.html` description and `release.json` identity change among build inputs. Unchanged: Bitcoin crypto, reference evaluator, signature verifier, PSBT parser/policy, QR transports, camera, immutable result model, session journal, application coordinator, style, vendor libraries and build tool. No new modules or controllers; one verifier, one journal, one app state. No optional component can change outcomes.

## Authority, privilege and state
The local operator initiates test-wallet generation, signs on an external signer, decides evidence opt-in, exports evidence and explicitly retires the session. The app has no persistent authoritative ledger and no web account. The one in-tab coordinator and one journal remain the only owners of ongoing state. This change adds no network requests, new privilege or persistence.

## Recovery, interruption, upgrade and rollback
No automatic resumptions, hidden retries or migrations. New sessions begin from an explicit reopen. `Finish testing` remains distinct from ending the guided journal. Cleanup remains best-effort for application-reachable memory only. Rollback is selection of the unchanged previous complete file by the release operator, not a hot patch or silent swap; previous test wallets cannot be adopted into the new state. Failed build must leave no authoritative output. Full clean-extraction and second-run checks are required. No public active-release pointer is set.

## Retired/deferred
No live patch of old snapshots, new signing algorithms, wallet.dat, dynamic entropic inputs, WASM rewrite, memory-certification badges, auto upload, telemetric reporting, new retry engine, second verifier or extra UI business-state controller. The historical 24 failed static assertions are retained as open qualification debt; do not waive them in response to a passing new source-delta contract.

## Release gates
Static/syntax, unit/contract, integration, fault injection, installation simulation, existing session/data behavior, upgrade/rollback, interrupted reopen/recovery, repeat run, clean extraction/reproducibility; native browser camera and signer acceptance, security/dependency provenance and publisher signing remain separate external gates. Any blocker prevents RC promotion. A frozen RC SHA may be declared only after a complete single-campaign qualification, which has not occurred.
