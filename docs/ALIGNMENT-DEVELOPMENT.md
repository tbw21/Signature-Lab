# Alignment development history

- Baseline HTML/archive hashes verified against v0.16.1 release identity.
- An edit helper initially expected adjacent evidence buttons. That assertion stopped
  it before writing the template. The helper was corrected to wrap existing individual
  actions without changing their handlers. The first dev-1 build therefore reproduced
  the untouched baseline exactly, and is not a changed release or accepted candidate.
- dev-2: 38 retained static checks and all 22 new alignment browser cases passed.
  Normal and enlarged 12/24-word layouts, 320-1440px, doubled text, text spacing,
  keyboard focus, trailing actions, QR pixel stability and application-state equality.
- Source-presentation changes only. No runtime JavaScript edits.
- Hardware/real-optics, publisher signing and dependency provenance are not tested by
  these DOM checks. A new run of all retained suites follows before final freeze.

- The container does not provide streaming-exec sessions. That call failed before any
  command ran. No candidate or result files were created by it.
- An initial combined development static/core command hit the 60-second outer command
  limit during regression job 21-40. Its partial core attempt is excluded from completed
  development totals; it did not change the source or HTML. Final acceptance uses bounded
  individual job dispatch and waits for each job's explicit success receipt.
- Completed pre-freeze development selection: 43 static checks, 22 alignment browser cases,
  21 controlled-clock camera faults/contracts and 8 retained calm browser tests: 94 passed,
  0 failed. Candidate normal/enlarged desktop/mobile screenshots were visually inspected.
- No runtime changes were needed after the first successful presentation implementation.
  The exact retained complete suite is required again after candidate freeze before delivery.
