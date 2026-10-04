# Development accounting: onboarding and Help

Baseline HTML and source ZIP matched their published SHA-256 values. Changes are scoped
by ONBOARDING-ARCHITECTURE-FROZEN.md. No runtime JavaScript file was edited.

Initial checks: 43 retained static/source checks, 12 contents build contracts and 10 demo
isolation/fault checks passed. The initial five Step-1 browser cases asserted visibility
immediately after an Alpine transition. They failed before awaiting the hidden state;
this test-observation race was corrected with an explicit wait, not a runtime change.
The five cases then passed.

A new 320px doubled-text Help test found a real pre-existing long-title overflow:
Help & methodology extended the scroll width to 344px although element boxes fit.
Added overflow-wrap:anywhere to Help/Contents headings and summary titles. The regression
then passed. A one-off probe first used the wrong __file__ location and failed to load
its harness; the probe path was corrected outside release source.

The additional Help menu groups share the existing FAQ router; all 22 links were exercised
at three widths with focus and return checks. The optional example is linked from Step 1,
not duplicated or made a mandatory gate. Button text says Check example rather than Run
known attack to avoid implying execution of malicious firmware.

Development results are not final acceptance. Complete final runs use a new clean extraction
of the uniquely named frozen candidate and reports outside that source. Historical partial
or failed development runs are retained separately, never added to final passed totals.

Final pre-freeze development selection on dev-4.html: 83 checks passed, 0 failed
(43 retained static/source, 12 build/contents, 10 demo isolation/fault, 18 new browser).
Earlier failed selections are not added to these passes. Current runtime remains unchanged.
