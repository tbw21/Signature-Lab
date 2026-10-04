# Evidence upgrade: scoped engineering review
This is internal review of new source, not independent organizational approval.

## Trusted boundaries
The application passes the existing immutable **public** evidence envelope to the sole session journal.
The journal checks object identity against its report, requires the public evidence schema and a frozen
object, and serializes it into an immutable string. It never receives prepared secret state. The existing
current-result exporter stays authoritative. Summary exports strip internal attachments.

Retention is off by default and volatile. It does not enable storage, upload, camera access or automatic
signing. Disabling retains existing payloads; it does not clear a latched failure. New-wallet confirmation
and reload are the only reset boundaries. Browser crashes/power loss lose unexported in-tab data. A
browser download event is not proof of a successful final OS write or operator retention.

Limits are 16 MiB of UTF-8 serialized evidence and 256 payloads. These are logical data limits, not a bound
on total JavaScript heap use: strings, decoded data, DOM and export copies require additional memory.
There is no eviction. Later missing payloads and the latched reason remain visible. Verification continues
under the existing rules. Exporting all evidence can use additional transient memory. Physical low-memory
browser acceptance remains required.

Capture diagnostics are optional, on only while retention is enabled, at most 256 records in the same
journal with an explicit omitted count. They do not occupy the 2,000 core result/control slots. One
terminal record is attached to an explicitly started capture. They do not claim every camera frame,
permission dialog, attempted device signature or optical transfer was observed. Signature counts and
capture counts are distinct. Untrusted error strings, raw frames and automatic user-agent fingerprints
are excluded from the diagnostic-only allowlist. Operator notes are unverified and can contain whatever
the operator types; raw returned artifacts included by explicit choice remain untrusted.

## Independent replay
The existing Python entry point is extended, not embedded as another application verifier. It recomputes
psbt-envelope-v3 from raw public PSBT bytes, including supported generated-v0/v2 conversions, field
classification, hashes, positions and order. Unknown policy versions or unsupported reconstruction
shapes are rejected. It cannot assert publisher, reference or physical device authenticity, derive secret
nonces from seed-free reports, or determine that omitted history never existed. Supplied session history
is checked for internal bindings and worst-observed counts only. Retained incomplete responses are
identified and not reported as cryptographically replayed.

Bundle CLI input is capped at 32 MiB to accommodate 16 MiB of quoted evidence JSON plus the summary and
metadata wrapper. Raw PSBT/transaction limits remain 512 KiB; canonical CompactSize checks apply.
No Python eval, JS execution, subprocess or network request is involved in replay.

## Browser and mutation evidence
The existing origin runner now actually navigates each available engine, exercises startup, workflow,
recorded example, synthetic import, and real download events. Missing engines and administrator-blocked
origins remain unavailable. No setContent, permission shim or reference UUID shim is used by this runner.
WebKit is not branded Safari. Synthetic responses and headless downloads are not hardware or optics.

Eight deliberate source defects are tested on separately labelled temporary copies. Clean controls must
pass. A malformed/nonloading mutant is invalid setup, not a detected vulnerability. Counts mean these
specific defects were detected, not a global mutation score or attack-detection percentage.
