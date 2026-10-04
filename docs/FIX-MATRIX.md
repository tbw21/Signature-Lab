> Historical v0.14 record. For the consolidated candidate, apply
> CONSOLIDATION-ARCHITECTURE.md and CONSOLIDATION-FIX-MATRIX.md.

# Audit-to-implementation traceability

| Audit item | Implemented change | Required regression / remaining gate |
|---|---|---|
| R1 | Terminal BC-UR checksum/fountain error state, cleared partial result | Corrupt complete-message checksum, no revival, explicit new session succeeds |
| R2 | Entire finite submission fed before commit; no early-break parser | Junk/mixed/other-transfer/conflicting tails fail; duplicates and valid fountain redundancy pass |
| R3 | Sole camera controller with 30-second permission/play deadline | Unanswered/late grant, stalled play, cancellation, repeated Start; no leaked stream |
| R4 | Track/stream/video failure handlers; hidden-page stop; bounded stall | Ended/inactive/error, missing frames, mute/unmute, hidden-page and no auto-restart |
| D1 | Lossless bounded PSBT map inventory and independent metadata status | Proprietary/unknown fields, wrong output derivation/script, finalization, v0/v2 conversion, trailing maps |
| D2 | One immutable result snapshot; optional original-byte public evidence | Report/export identity, no local seed/private key serialization, changed-state guard, independent public replay/tampering |
| D3 | One prepared-test cache plus failed-preparation latch | Unchanged revision, units/format/navigation reuse, edit invalidation, explicit retry of failure |
| D4 | Explicit compatibility or fixed-method selection, locked on attempt | Selected method, different valid method, coincident references, new-test unlock; certified device profiles remain unavailable |
| D5 | UR type/size/geometry/identity/equation/work admission | Giant declarations, wrong CBOR/sequence/identity, conflicting duplicate, redundant equation, session/work budgets |
| Q1 build | Standalone source assembly with lock and atomic output; inherited code labelled reconstructed | Token preservation, no old-HTML input, two clean rebuilds, exact repack, source tampering/concurrency/interruption |
| Q1 provenance | Inventory, pinned pako bytes and operator comparison/signing tools | Tool simulations pass independently of upstream/publisher authentication, which remains open |
| Q2 software | Native secure-random UUIDv4 implementation removes candidate harness-shim dependency | Missing randomUUID works; missing/failed secure RNG fails; genuine origin attempts remain environment-blocked |
| Q2 external | Versioned physical/browser acceptance checklist | Not simulated as passed; see OPEN-GATES.md |

No direct firmware inspection, detection-rate guarantee, hidden-channel proof, funded
wallet testing, automatic retries/reacquisition, extra signing algorithm or automatic
update service was added. The original three deterministic methods and core
transaction/key/signature verification functions retain their original token streams.

Retired runtime paths: early finite-import acceptance, swallowed terminal UR failures,
app-owned duplicate camera timer, mutable verification ledgers and unconditional
reference regeneration. Previous implementations survive only as testing fixtures,
not runtime fallbacks. The former HTML-patching build is not included as an alternative.

The runtime version is read from the single release.json build identity through TBW_BUILD.version; no independently maintained JavaScript version literal remains.
