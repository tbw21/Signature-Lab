# Scoped read-only/security review of calm-workspace changes

Reviewed boundaries: prepared transaction to visible output review; workspace and deferred
focus; metadata/result scope; event history; public evidence serialization and download;
retention of crypto/codec/camera invariants. Tests are authored in this workflow, not an
independent organizational audit. No new runtime dependency or network permission was added.

Output-review data comes from the existing prepared public PSBT; full address decoding uses
the existing library. An independent Python Bech32/raw-transaction oracle checks 20 outputs.
No extra wallet keys, signatures, transaction construction or second journal are introduced.
An unavailable projection blocks the signing presentation; it cannot rewrite a test to fit.

Display changes do not hide unresolved errors. History is an immutable projection of the
one existing journal, with earlier review/incomplete findings surfaced across views. Export
uses a single serialization and content hash; failures preserve the result. Filename suffixes
are convenience, not authenticated provenance or anti-detection. Public returned data is
untrusted. Browser known disposable seeds are never valid for savings.

The release is unsigned. Vendor provenance, original source/lockfile recovery, public
repository publication, outside code review and independent rebuild remain outstanding.
Inline/eval CSP permissions remain inherited: no exploitable injection is claimed or ruled
out. No complete dependency or long-running coverage-guided fuzz audit was performed.
Normal-origin and other browser-engine availability are attempted and reported separately.

The user-reported 21 SeedSigner results concern v0.15.2 only. The uploaded final summary
contains no raw signatures for independent replay and has empty device/firmware labels.
Do not convert its counts into reliability percentages or this candidate's hardware grade.
