# Physical/browser acceptance for v0.16.1-rc1

Use the exact frozen HTML hash from the accompanying manifest. Save current results first;
close older versions and create a fresh disposable test wallet. Never import a real seed,
fund a generated address, broadcast these tests or weaken device protection. Test SS and
CCQ separately; identify firmware exactly, not as "latest". A blocker rejects those bytes.

Record app hash, signer hardware/firmware, browser/OS, device type, opening origin, camera,
QR format, word length, operator and date. Device labels/fingerprint are not attestation.
Start with one ordinary response and preserve its full Save result file. Then 3-6 cases,
then the intended longer run. Twenty per device is a practical target, not a confidence
threshold. Cover 12/24-word setup and all applicable six transaction scenarios.

Verify all output counts/amounts/full addresses, including a 20-output boundary case.
Compare individual and guided paths with the same test/policy. Exercise supported BC-UR,
BBQr, file and paste paths; mark unsupported/refused cases rather than inventing passes.
Verify a known good reduced response is not amber, and independently reviewed synthetic
negative fixtures remain visible/halt correctly. Do not install malicious firmware to test.

At 320/390 CSS px, landscape, native zoom and larger OS text, check Test/Advanced/Session,
keyboard/screen-reader focus, long addresses, custom-policy indicator and historical issue
badge. No hidden required review. Ask beginners what a match, difference and completed
session prove; reject misleading interpretation, not merely add more warnings.

Check actual camera permissions, cancellation before/after grant, late grant, failed/ended
camera, phone screen lock, background/return, reflections and long animated codes. The
camera must stop and never secretly restart. Repeated permission is controlled by browser;
record origin and one-time/per-site permission. Do not enable access for all sites.

Save result should contain original current response/public test, no deliberately exported
local secrets. Save session record is summaries, not every raw response. Verify reports
with tools/replay_evidence.py in a separate trusted environment. Record all failures, latency
and refused/skipped cases; do not scan until green and discard previous failures.

Reload/new-wallet loses in-memory state by design. Save first. Back/Forward restoration
must not start capture/advance. Upgrade/rollback uses fresh tabs/disposable tests, not seed
migration. Test OS interruption/storage faults safely and distinguish from API injections.

Physical acceptance is only compatibility/workflow evidence. It is not an independent code
audit, publisher authentication, or proof that firmware cannot recognize a test or leak later.
