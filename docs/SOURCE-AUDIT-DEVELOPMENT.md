# Source audit remediation: development log

Baseline: exact supplied v0.18.5-rc2 source and HTML, with independently checked manifest
and reproduced output. Architecture recorded before application edits. No old artifact is modified.

## Findings independently exercised before edits
The baseline synthetic trigger matrix reproduced a reduced response retaining exact SIGHASH_ALL
as unexpected in PSBT v0/v2; reversing field order retained a match with no ordering evidence;
match/review/match summaries remained optimistic. Source inspection confirmed uncapped metadata
projection and unconditional optional browser-agent registration. Full original Foundation case
bytes and the auditor's differential corpus/runner are absent; those claims are not relabelled as
newly reproduced hardware or complete upstream-provenance evidence.

## Development corrections and failed checks (not acceptance passes)
- A read-only inspection initially referenced a nonexistent tests/harness.py; the existing harness
  is in tests/browser.py. No application code was executed or modified by that failed inspection.
- An initial lock-source invocation omitted the required explicit development-update flag. It
  refused the operation; the following build correctly refused the stale source lock. No candidate
  was published. The documented development command was then used.
- The first new Node contract run recorded 47 passes and two failures caused by strict comparison
  of arrays from distinct VM realms. Assertions now compare the same ordered JSON values, not
  different prototypes. The complete subsequent run passed all 49 cases on the exact dev HTML.
- An inherited static suite initially recorded 12 passes and two failures because its historical
  byte-boundary assertions did not reverse the newly authorized edits at two read_bytes sites.
  They now use the same exact, negative-tested audit projection as the rest of the historical
  assertions. All 14 then passed. New source-audit cases check every current byte and reject any
  undeclared change. Runtime/browser tests execute the current application, never projected code.
- Visual inspection found '1 need review'. It was corrected before freeze to '1 needs review';
  the plural case remains 'N need review'. The direct DOM regression uses the singular label.

## Targeted checks before full preflight
New suites completed 49 contract, 18 source/static, 11 delivery/prerequisite, and 21 exact-DOM
browser cases on development revisions; retained static suites completed 124 current selections.
These are development observations, not frozen-candidate acceptance or additional final case totals.
Raw failed and successful reports are preserved outside the source tree for the handoff.

## Qualification plan
Run all canonical jobs from qualify.py, with an explicit prerequisite stage first. The existing
single driver remains the test implementation. An external supervised dispatcher may execute one
sequential browser queue and one sequential nonbrowser queue; no application retry engine is added.
Each job is bounded and failures stop that run. Producers precede their independent consumers.
The candidate is not frozen until full preflight and source review finish. Any blocker after freeze
requires a new candidate and acceptance restarted from the beginning, not patching frozen bytes.
