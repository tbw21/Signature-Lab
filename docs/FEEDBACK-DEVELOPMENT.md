# Development record (separate from later frozen acceptance)

Baseline v0.18.4 rebuilt and matched its full manifest. Initial Chromium demo clicks at
390/1440 showed the expected native dialog/result with no page errors; no hidden-demo cause
was inferred. Reproduction screenshots and raw notes are external acceptance evidence inputs.

First new Node contract invocation exceeded the outer 45-second tool window after 10 passing
cases. It was incomplete and excluded. Subsequent disjoint complete jobs reran the cases.
First browser selection: 13 passed, 3 failed (queued modal close race, and two actual session
record downloads). Session download failure was separately reproduced on unchanged v0.18.4:
TypeError on JSON.stringify of a frozen reactive proxy. Corrections were tested on new
unfrozen development bytes. Native modal closed-event handler now ignores old close events
while the element is newly open. Public export is detached before deep freeze.

A diagnostic harness initially had the wrong __file__ anchor and looked for baseline files
in the working directory; corrected outside source. A static assertion used BeautifulSoup
get_text on inert template contents and could not see CHECK COMPLETE; corrected to inspect
its actual source, with separate real browser visibility checks still required. No application
acceptance was relaxed. Visual review replaced a colliding demo CSS class whose inherited
borders added unwanted separators; a no-border browser assertion was added.

The final report separately identifies full preflight and frozen-acceptance results. Development
passes are not added to acceptance totals. Source/test changes after this note (if any) must
be recorded in the external logs and final qualification, never hidden or patched after freeze.

## 21 September 2026 continuation (before candidate freeze)
The supplied dev-3 HTML and preflight-source.zip were recovered. All 207 manifest-listed
files matched; a build reproduced the HTML exactly. A fresh complete preflight ran all 98
canonical jobs: 1,075 named checks passed, none failed, four origin/engine checks unavailable.
No prior partial job or reported pass was used to fill a missing result. Current-run raw
logs accompany the external evidence; earlier development notes above are historical.

A separate exact-baseline/current-browser probe reproduced the old frozen-reactive-proxy
JSON export TypeError and successful current export. Short portrait/landscape views exposed
the recorded demo result. These supplemental observations are not additional named passes.

Handoff review found the README describing ancestor v0.18.2 as the current reconstruction,
and the general hardware checklist prescribed rollback to v0.14 by name. A new documentation
regression failed before correction (14 existing cases passed, 1 new case failed) and passed
after correction. Current README now names the recovered feedback preview and v0.18.4
baseline; rollback requires a separately approved identity or withdrawal. Historical addenda
are explicitly marked. This changes documentation and one static test, not application bytes.
The final complete frozen acceptance, including this new case, is reported separately.
