# v0.16.3-rc1: scope and architecture freeze

## Scope and reason
User feedback: the published malicious-signature example is hard to discover; Help needs
contents; the first screen does not explain the test. A secondhand Foundation Prime report
mentions 21 checks, some orange, most green, without returned evidence or release/firmware
identity. Treat that report as unresolved operator feedback, not a reproducible defect or
signer qualification. Never relax an acceptance rule on account of a brand or colour.

## Requirements and acceptance criteria
1. Add a compact two-sentence purpose statement above the workspace controls. It must describe
disposable-wallet signature comparison and explicitly limit the conclusion. Reflow normally.
2. Step 1 has an obvious, optional, right-aligned link to the existing known-attack example.
One canonical demo remains; it is not automatic, mandatory, a real-device test or counted.
3. Help has a native, keyboard-accessible, grouped contents menu. Generate titles and targets
from the canonical FAQ headings at build time. No second manually maintained question list.
Every FAQ has a stable unique ID. All links open/focus the existing FAQ and return without
changing the wallet, transaction, policy, result, history or guided lock.
4. Add a generic orange-result explanation that distinguishes matching signatures with file
findings from incomplete/failed transfers, requires actual evidence, and makes no device
exception. Improve the two overlapping camera questions by separating permissions from
lifecycle without breaking their existing anchors.
5. Preserve calm mobile/desktop alignment, all output review, warnings and current exports.
All 29 runtime JavaScript files, vendor bytes, CSP and all original reactive bindings remain
unchanged. No networking, permissions, storage or dependency added.

## Architecture and authority
- Trusted runtime: unchanged sole transaction generator/verifier, QR decoder/session, camera
controller, immutable result, public-evidence export and authoritative attempt journal.
- Optional presentation: one purpose paragraph, one demo link, FAQ content and build-generated
contents. Their absence must not prevent normal testing. Demo data is already isolated.
- Build: existing build.py remains the one assembler. A pure standard-library parser derives
contents from src/page.html after checking the existing source lock, before embedding code.
- Authoritative release: release.json. Authoritative question titles/ids/groups: src/page.html.
No runtime TOC controller, alternate verifier, secondary seed or new journal.
- Ownership/privilege: local unprivileged browser operation; no server or signer control.
Publisher key/dependency authentication remain external gates, not simulated successes.

## Lifecycle and recovery
Help navigation uses the existing router and its explicit camera stop. Returning does not
restart capture. Demo success/failure affects only demo state, not the active test. Closing
or reloading starts fresh; no secret-state resume or migration. Upgrade/rollback: save current
evidence, close old page, open the exact selected release and use a fresh disposable wallet.
Build interruption/concurrency/tampering must fail without overwriting a published artifact.
No OS boot/recovery services apply to this standalone browser application.

## Contracts
Existing runtime inspect/plan/apply/verify/status/rollback contracts are retained unchanged.
Contents generation: inspect canonical headings, plan grouped links, apply pure escaped HTML,
verify unique/complete ids/headings, status as build success/error, rollback by using unchanged
prior release. No persistent state or retries. Invalid help sources stop publication only;
optional help/demo never gates an already loaded runtime test.

## Retired behavior
Undiscoverable Step-1 demo; absent Help contents; duplicate camera-permission prose. Old
anchors are preserved and a lifecycle-specific question replaces the redundant explanation.
No existing cryptographic or metadata rule is retired.

## Qualification plan
Retain complete baseline suite; add contents-generation static/contract/fault tests,
demo isolation under success/failure/repeat/absent optional content, initial/no autorun,
all-topic navigation and return, review/incomplete FAQ and unchanged warnings/evidence,
12/24 words and normal/enlarged QR, 320/390/438/768/1440px, increased text and keyboard tests.
Then freeze uniquely named HTML and archive, record SHA-256, clean-extract and execute all
applicable suites. Any blocker disqualifies candidate bytes; fix in a new candidate and
restart. Report simulations, unavailable origins/engines and actual hardware separately.

## Current grade at freeze of architecture
Design frozen; no implementation or acceptance completed. Runtime changes permitted: none.
