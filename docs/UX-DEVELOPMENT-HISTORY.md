# UX development observations
- Verified baseline HTML/ZIP hashes against the latest 391-case v0.15.0 qualification.
- Initial baseline-probe harness used the wrong __file__ and failed before a browser test.
  Corrected the probe path outside release source; no application was changed.
- Baseline Chromium normal-size 320/438/768/1440 layouts did not reproduce the exact
  cropped user screenshot. At doubled computed font sizes the fixed 140px count label
  overflowed; 320px page scroll width reached 371px. This is a related reproducible reflow
  defect, not proof of the user's exact browser/zoom settings. Its remedy is responsive
  intrinsic sizing and wrapping, not hiding overflow.

- An exploratory Python screenshot probe had an unquoted dictionary key and stopped with
  NameError; corrected in the probe outside candidate code and rerun.
- The first UX focus test asserted before the asynchronous next-tick focus completed.
  It failed, was changed to await the documented focus transition, and passed on rerun.
- The initial forced-color assertion expected :focus-visible after mouse interaction.
  The test now enters keyboard modality explicitly before checking the keyboard focus
  outline. The revised test passed; no application suppression was added.
- Initial 45 UX cases and 28 static checks passed in disjoint completed development runs.
- Added a self-contained licence Help target and original-response retention reminder,
  plus result-heading/sticky-tracker overlap checks. The three added cases passed.
- Default and enlarged-text planner renders were inspected at 320/438/768/1440 widths.
  Full-page captures made while scrolled can reposition sticky elements; separate real
  viewport focus checks and an unscrolled capture verify that headings are not obscured.
