# v0.16.4 development record

The exact 0.16.3 HTML and source archive matched their published checksum record. All 138
baseline source-manifest entries and archive CRCs verified. Before source edits, the scoped
architecture/acceptance document was frozen and recorded by hash.

Targeted development: 43 retained static, 10 copy/static contracts and 18 new browser cases
passed; 0 failed. Real rendered text at 1440 and 1024px used one line, at 390 and 320px three
natural lines, without horizontal overflow. Gold was RGB(229,182,125), original 14px desktop
and 13px mobile text, not shrunken to force fitting.

One environment-discovery shell returned status 1 only because the optional executable alias
chromium-browser was absent; /usr/bin/chromium is present and used. This was not a product
or regression-test failure. No prior alleged tool outage is assumed to persist in this run.

Full preflight and frozen acceptance are recorded in the separate final qualification report.
This historical development record is not a substitute for either and never certifies hardware.

Full preflight subsequently completed: 710 named checks passed, 0 failed, 4 origin/engine checks unavailable, 61 jobs, no job failure or timeout. Full preflight results are in the separate evidence archive. No runtime or test change was made after this preflight.
