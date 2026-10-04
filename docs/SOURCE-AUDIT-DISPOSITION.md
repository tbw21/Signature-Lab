# Disposition of the 21 September 2026 source audit

Basis: the attached Independent audit: Signature Lab v0.18.5-rc2, SHA256
`d365f5a0470f03b80bdb31b14aad965236e48793dca22f52f08a566afd427908`.
This document separates its reported work from new source observations, synthetic reproductions,
implementation decisions and deferred requirements. It is not a new independent organizational audit.

## A — Reduced envelope plus SIGHASH_ALL — reproduced and corrected
The exact baseline reproduces the claimed contradiction for v0 and v2: full responses with
an added 01000000 sighash are expected, but otherwise uniformly reduced responses with the
same field are marked unexpected. The new rule mirrors the existing exact type/value/key-data
allowance in the reduced-envelope recognizer. Bp/Rp remain byte-identical: non-ALL, malformed
fields, foreign keys, invalid signatures or changed transactions do not become valid results.
Selective omissions, proprietary additions and finalized removal of the UTXO retain review.
This changes a metadata classification, not cryptographic signature acceptance or device trust.
No assumption that Foundation Prime behaves like Passport, and no original orange case is diagnosed.

## B — Ordered PSBT fields — reproduced and recorded, not rejected
Reversing maps in the exact baseline preserves a signature match and has no ordering record.
The new psbt-envelope-v3 evidence adds beforePosition/afterPosition (zero-based within each map)
to every field, a per-map relativeOrderChanged observation, the number of retained fields compared,
and fieldOrderChanged (number of changed maps). It also states the comparison basis: the actual
prepared PSBT, or a locally reconstructed same-version PSBT for version conversion.
The comparison uses the relative order of common keys. Comparing full key lists naïvely would
mislabel normal signature insertion and expected metadata removal as reordering. Absolute positions
retain the arrangement of added and removed fields too; their placement is not itself rejected or
reported as retained-key reordering. The full data remains available in original-response evidence.
Technical details explains the observation neutrally. Expected serializers can reorder fields.
This channel concerns recipients of the PSBT, not automatically the extracted on-chain transaction.
The lack of observed reordering cannot establish absence of hidden information, and no universal
capacity/detection claim is inferred from the audit's combinatorial examples.

## C — Session outcomes — reproduced and corrected consistently
The baseline's summary drops metadata and retains an old match if the same txid later needs review.
The journal now carries metadataStatus. One shared outcome helper produces mutually exclusive
matched, review and differed buckets, with checked = matched + review + differed. Missing/unknown
metadata is review, not a fabricated clean result. A raw transaction uses not-applicable file status
and can match its signatures without claiming PSBT coverage.
Deduplication retains the worst observed result: differed > review > matched. Old immutable entries
and evidence remain, so a later match cannot erase prior findings. Incomplete attempts remain outside
completed counts. Guided status and public result projections use the same helper; metadata is carried
into the provisional report before commit, avoiding a UI/export count discrepancy.
The additive countPolicy is distinct-transaction-worst-observed-v2. Saved older files are not rewritten
or silently migrated. Consumers must examine build and count-policy version rather than assuming the
old meaning of matched. Review is not a malware conviction.

## D — Untrusted metadata rendering — confirmed and bounded
The baseline getter exposes every unexpected field. The new display projection shows at most 32
unexpected rows and at most 128 key hex characters plus an ellipsis. A separate small integer identity
prevents key-prefix collisions after truncation. The visible shown/total note points to Save result.
All fields still undergo assessment, remain counted, and are preserved in the immutable evidence.
Limits are presentation only; no parsing, signature or envelope acceptance rule is loosened.

## E — Automatic browser-agent registration — removed
The previous status payload was not a seed export, as the audit correctly observes. Nevertheless,
unsolicited browser-agent registration is unnecessary for the manual offline testing path. This
candidate never reads document.modelContext or registers an agent tool. Internal inspect() stays.
No optional toggle/controller or new privilege was added. This does not prevent a browser or extension
with access to the page from reading the page. A local CSP does not authenticate the browser.

## F — Vendored preload polyfill — deferred to next vendor refresh
Confirmed inert in the shipped template: no modulepreload links; first-party code creates none;
connect-src remains none. Vendor bytes are preserved in this correction. The fetch primitive still
exists in the bundle: no statement that every network primitive has been removed is made.
A pinned vendor refresh should remove the unused polyfill and assess an Alpine CSP build. Removing
unsafe-eval requires a framework migration, not just editing CSP. These are separate reviewed changes.

## G — Visibility race — structural test correction
The reported test waited on reactive psbtQrAvailable before measuring an x-show element. All three
visible-layout box/rect helpers (polish, alignment, wallet-card) now wait for actual visible geometry.
Their normal interaction deadline is unchanged. A controlled test reproduces a zero rectangle despite
a true readiness flag, then proves the corrected helper waits for display. A never-visible fixture
still fails at its bounded deadline. This is test synchronization, not retrying application actions.
It does not establish that the earlier rc1 document-load timeout had the same cause.

## Rebuild and source-only delivery
A new clean baseline rebuild matched the published rc2 HTML exactly and all 210 manifest entries
verified. The audit's statement of no expected output hash applies to the source-only ZIP: the
previous Handoff and separate SHA256SUMS already carried artifact identity. This source package now
also contains EXPECTED-OUTPUT.json and tools/verify_output.py, allowing a one-command comparison.
The sidecar is deliberately outside build.inputs(), avoiding a self-referential output hash. It is
inside the frozen source manifest/archive. Checksums establish consistency, not publisher identity.
Qualification Python requirements are pinned, including active transitive packages. An environment
stage identifies missing/mismatched prerequisites before candidate tests and reports an unavailable
environment, never an invented candidate pass/failure. Native dependencies and observed versions are
recorded too. These pins are not wheel authentication or a complete hermetic OS/toolchain lock.

## Audit corroboration and limits
The supplied audit reports 1,200 signer comparisons and 400 verification comparisons against npm
@noble/curves 2.4.0, plus correct BIP84 vectors and a fail-closed startup-gate experiment. The 400-key
corpus, runner, package-acquisition evidence and raw logs were not supplied. The reported differential
work is retained, explicitly attributed, in DEPENDENCIES.json; upstreamAuthenticated remains false.
The three literal BIP84 addresses are rerun locally in tests/audit.cjs. Existing independent
Python/HMAC/OpenSSL reference and transaction tests are rerun as part of full qualification.

The audit reports 83 qualification jobs. The actual frozen rc2 source defines 99 canonical jobs.
The audit's exact invocation/run inventory was not supplied, so its 82/83 statement cannot be treated
as completion of all 99. The new run uses qualify.py's actual complete inventory, not a copied count.

The positive transaction binding, seed-containment, parser and bounded-work observations are valuable
scope-specific evidence. They do not establish all possible inputs, full provenance, hardware origin,
security of a user's firmware/browser, or organizational approval. Foundation Prime responses remain
not diagnosed because no full original orange-response evidence was provided.

## Primary-source cross-checks (external to the supplied audit)
BIP174 source (bitcoin/bips bip-0174.mediawiki, retrieved 2026-09-30) defines the sighash field as a
four-byte little-endian value with no key data and requires finalizers to retain UTXO data. The
new exception is narrower than general PSBT permissiveness: only the Lab's SIGHASH_ALL flow.
Playwright's Python actionability documentation defines visible elements by a nonempty bounding box
and absence of visibility:hidden; this supports waiting on the rendered element rather than a
reactive property. BIP84 source confirms the three supplied address vectors. These are source checks,
not pinned full firmware review or evidence of any named device's installed code.
Sources: https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki
https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki
https://playwright.dev/python/docs/actionability#visible

## Still open
Physical signer/optical/native browser and deployment acceptance; authenticated publication;
inherited dependency provenance/security review; independently reproducible complete test environment;
independent organizational review/rebuild; user-comprehension testing; original Foundation reports.
No automatic reset/downgrade, hidden warning, firmware profile or new signing family is introduced.
