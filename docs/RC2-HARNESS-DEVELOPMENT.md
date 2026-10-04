# rc2 repair and development accounting

The frozen v0.18.5-rc1 acceptance was stopped, not retried: 768 named cases passed,
1 failed in Page.set_content waiting for load at its inherited 6000ms default. The
1440px layout assertions were not reached. 59 of 98 jobs completed/executed before
stopping; remaining jobs are unrun. Its frozen source/archive/HTML remain unchanged,
with disqualification and raw failure evidence retained outside this candidate.

RC2-HARNESS-ARCHITECTURE-FROZEN.md fixed the repair scope before implementation.
The common harness now explicitly permits 15000ms for document setup, leaving the
6000ms interaction deadline and 10000ms app-ready wait intact. Application source
and runtime reference-gate policy are unchanged. No automatic retry was introduced.
The old setup budget did not cover the runtime gate's own cooperative time allowance
plus parsing/setup. The cause of the isolated slow rc1 load remains unestablished;
this correction is not evidence of a speed improvement or a firmware finding.

Three new checks passed: exact candidate readiness with no network requests/errors;
an old-budget timeout on a finite 6500ms prelude fixture followed by genuine readiness
under the new budget on a separate fixture context; and a never-ready fixture still
failing the 10000ms readiness check. The labelled faults are not release-byte edits.
Both old/new fixture executions are specified comparisons, not retries of a failure.
Observed targeted delayed setup: old timeout after 6.135s, new ready after 8.055s.
Those are harness observations, not native-platform benchmark or performance claims.

All selected targeted checks completed before freezing: 124 static/source cases,
37 feedback contracts/faults, 8 calm browser cases (including the prior failure's
layout requirement) and 3 harness regressions: 172 passed, none failed.
Direct comparison also confirmed all 29 runtime files, page template and stylesheet
remain byte-identical to the recovered feedback preview. Only version/build identity,
test harness/driver/assertions and documentation/manifest changed in this repair.

Development execution issues, excluded from completed counts:
- An initial build invocation supplied the unsupported --output option; it produced
  no application file. The documented positional command succeeded afterward.
- A combined targeted invocation exceeded its outer 40-second execution window while
  feedback contracts were incomplete. Its partial report remains in evidence and is
  excluded. Complete bounded, disjoint selections then reran all 37 cases.
The original full 1075-case preview preflight and the pre-fix documentation regression
are retained as separate historical/development records, not added to rc2 acceptance.

Frozen rc2 acceptance must start all canonical jobs from a new clean extraction.
No prior pass fills an unrun current job. Any current blocker requires another new
candidate and full restart. Do not edit any frozen source, test, HTML or source ZIP.
