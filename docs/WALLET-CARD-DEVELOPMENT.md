# Development record (not frozen-candidate acceptance)

The supplied dev-4 source ZIP was extracted, CRC-checked and all 174 manifest entries verified.
Its source assembler reproduced the exact supplied dev-4 HTML. Initial metadata inspection
assumed an enclosing archive directory and raised StopIteration; direct root release.json
inspection corrected this without modifying source or running a product check.

The requested layout passed 10 direct new static checks and 25 new browser cases in targeted
runs. The retained static source suite passed 43, clarity-static passed 14 and the initial
browser sample passed 20. These are development cases, not acceptance of a frozen candidate.
A progress message misstated the retained static subtotal as 77; the correct subtotal is 57.
The 35 new card cases and 20 sampled browser cases were correct. Saved JSON counts were not
changed; acceptance totals must be computed from the final named reports, not messages.

The first complete development dispatch stopped on its first failed job, copy-static. Its
C-S10 assertion still expected the previous 0.18.0-rc1 version. At stop, 619 named cases passed
and 1 failed across 46 jobs. This was an outdated test expectation, not a signing/UI failure.
The expected version was updated to the newly assigned 0.18.1-rc1, without altering any
application validation condition. The corrected copy-static suite passed all 10 cases, and
all 22 alignment cases passed separately. The incomplete dispatch is retained and excluded
from final acceptance totals. A fresh full preflight and fresh frozen-byte acceptance follow.

The prior enlargement-alignment assertion was deliberately adapted: the action now belongs
inside the confirmation card, rather than being attached to the QR's right edge. Containment,
pixel preservation, independent QR decode and separate acknowledgement are checked directly.
No runtime file was edited. No automatic retries or hardware results are implied.

A second development dispatch was explicitly stopped before freeze when a supplemental
438px measurement found uneven action heights: Enlarge QR 44px versus Test wallet loaded
58.375px. Equal flex bases wrapped the longer label unnecessarily. The added regression
case failed on that exact development HTML (0 passed, 1 failed), establishing the defect.
The fix stretches siblings consistently and assigns space according to their text lengths.
At ordinary sizes, the row stays level where it fits; narrow screens stack full-width buttons.
This is W05's requested related fine tuning, not a verification or camera change. The complete
26-case card suite and fresh full qualification must be rerun after the correction.

Targeted remaining-range checks also found the retained copy-browser assertion required one
line at 1024px. With the previously requested native system-ui font, the unchanged 14px copy
needs two lines on this Linux platform. No overflow or missing text occurred. The assertion
was updated to compare actual measured text width with available width: a single line when
it fits, otherwise natural wrapping. Desktop text remains 14px. No application text/font was
shrunk or clipped to satisfy the old font's line count. The reproduction recorded 1 passed,
1 failed; the corrected test is rerun. This closes a pending clarity regression expectation.
