# v0.15.1-rc1: uncluttered default, explicit power-user controls

Baseline is the 1-200 guided-session v0.15.0-rc1 with HTML SHA-256
3d5dc1835bc4841132f099e771f05ce5eac113c126d7a0abb783626d594c3811.
The old v0.12.2 upload and alternative v0.15.0 artifact are not runtime inputs.

- One Advanced tools disclosure is closed on fresh open. It groups the existing guided
  planner, transaction editor/signing policy and optional device/firmware notes.
- Essential SeedQR, fingerprint, 12/24-word choice, BC-UR/BBQr, physical-device review,
  file/paste/camera intake and Save report remain available without Advanced tools.
- Nondefault signing policy, PSBT version and edited transaction are shown outside the
  disclosure. Review settings reveals existing controls without resetting anything.
- Completed result state, metadata findings, errors, active/halted session status and
  explicit End remain outside Advanced tools. No easier mode weakens the verifier.
- Evidence & technical details is a separate consistent disclosure on Results. Its
  summary reminds users to save original data before advancing. Existing exports and
  their contents are unchanged. A session summary is not an original-response archive.
- Empty progress/20-test goal is hidden before a first completed check or guided plan.
  Real progress returns when there is something to record; no findings are erased.
- Count input/presets use responsive intrinsic grid tracks. Long labels/actions wrap,
  while required fonts stay readable. No body overflow clipping conceals a layout fault.
- Small-screen seed grid and step navigation accommodate enlarged text. Existing QR
  quiet zones, pixels, transport and signature bytes remain unchanged.
- Release-candidate status and actual version are visible from the first screen. Help
  labels the assembly-source hash accurately and lists authentication/acceptance gaps.
- The single-file footer licence now opens the exact already-embedded MIT notice in Help
  rather than requiring a separate LICENSE.txt next to the standalone HTML.

Production source changes: src/page.html, src/style.css, three presentation properties
in src/20-application.js, release.json and source-lock.json. No generator, verifier,
metadata, codec, journal, export, prepared-cache or camera code changes.
Tests: existing browser actions now explicitly open the corresponding disclosure; test
assertions are retained. New 48-case UX suite and five static preservation tests. The
qualification driver adds an explicit ux stage. Documentation and baseline fixtures added.

This is not certified bug-free software. Hardware, OS, browser-origin, publisher signing,
dependency provenance and outside review gates remain separate from local test evidence.
