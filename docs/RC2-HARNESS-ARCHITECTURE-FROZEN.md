# v0.18.5-rc2 acceptance-harness repair — scope frozen before implementation

Date: 2026-09-21T10:57:45.585249+00:00

The rc1 acceptance stopped at Page.set_content, waiting for load, with its inherited
6000ms default timeout. The 1440px layout assertions had not run. The exact reason for
that one slow load is not established; it is not evidence that a UI assertion failed.
rc1 is disqualified and remains unchanged. Its actual failure/partial logs are retained.

## Requirements and acceptance
The harness must permit the existing startup reference gate's 10-second cooperative budget
plus bounded document parsing/setup, without changing runtime gate behavior or accepting an
unready page. Set an explicit 15000ms document-load setup budget; keep the 6000ms interaction
budget and 10000ms app-ready check unchanged. Never retry set_content or a failed case.
Demonstrate the old 6000ms budget rejecting a deliberately delayed but otherwise ready test
fixture, the new budget handling it, and an unready page remaining a terminal timeout.
Test the exact candidate normally. Fault fixtures are separate labelled copies, not release
bytes or physical-device operations. Do not claim an application performance improvement
or a conclusive diagnosis of the user's earlier invisible demo.

## Boundaries, state, privileges and retirement
Only test setup, current version identity and associated documentation/qualification inputs
may change. No application module, cryptographic rule, journal, reset controller, permission,
network access, dependency, retry engine or UI feature is changed. Existing one coordinator,
source lock, source order, verifier and session journal remain authoritative. Retire only the
implicit six-second document-setup deadline; interactive checks remain at six seconds.
Historical rc1 notes/identities stay intact and are not promoted to rc2 acceptance.

## Recovery and qualification
A failed setup remains failed; no automatic retry or successful-status rewrite is allowed.
Run targeted startup/harness and preserved-source checks before freeze, then freeze a new
HTML/source archive and restart ALL canonical qualification jobs from fresh extraction.
No rc1 partial pass fills a missing rc2 case. Any further blocker again disqualifies its
candidate. Source/ZIP/publication failure, clean rebuild, upgrade/rollback and idempotence
cases remain in the full suite; OS boot/installer tests are not applicable to this HTML app.
Hardware, native browsers, dependency provenance, publisher signing and outside review remain
open. Every exported result retains its original qualified-build identity.
