> Historical v0.14 record. For the consolidated candidate, apply
> CONSOLIDATION-ARCHITECTURE.md and CONSOLIDATION-FIX-MATRIX.md.

# Pre-freeze development executions and limitations

The architecture contract preceded implementation. All old supplied releases remain
unchanged. Development files were editable; no candidate acceptance began during these
iterations. This history is not folded into an inflated count of unique final passes.

- An initial UI-update script stopped at an unmatched source-string assertion before
  writing the page. The anchor was corrected against the actual source and rerun.
- A combined runtime/BBQr command timed out during the second suite. Completed runtime
  results were retained; the incomplete codec execution was not counted. The codec
  suite was rerun separately and completed.
- A streaming container execution was unavailable (StreamingExecNotEnabledContainerError).
  Subsequent commands used bounded synchronous execution.
- The independent structure harness initially requested an old fixture property. Its
  schema was updated to current-candidate generated fixtures and expanded to both
  PSBT versions; the complete rerun passed.
- The first static harness had a syntax error, then an overbroad regex counted an
  Alpine diagnostic string as a second script element. The harness syntax and
  script-element scope were corrected, without changing application behavior.
- New browser tests first had a Playwright function-return injection mistake and an
  immediate visibility assertion racing a reactive update. The injection was wrapped
  in an explicit function and the assertion waits for the visible state. Both complete
  ranges passed on rerun; no application fix was concealed by deleting a test.
- One progress message total said 256 instead of 236. It was immediately corrected.
  Individual test result files were not changed to support the mistaken total.
- Upstream download/DNS and registry/CDN metadata attempts failed. No unverified
  downloaded bytes were inserted. Publisher identity and pako provenance remain open.
- Genuine file and local HTTP navigation were blocked by administrator policy.
  Firefox/WebKit executables were not present. No policy bypass or hardware pass is claimed.

Final acceptance uses newly frozen files, fresh outputs and complete reruns. Prefreeze
reports are historical evidence, not additional final passes.

- A final combined development command reported an outer 30-second tool timeout after
  all three requested suites had written complete zero-failure JSON reports and printed
  their totals (19 static, 54 regression, 21 camera). No child process remained. Those
  files are development evidence only. Final acceptance reruns them in bounded separate
  commands and requires completed command status as well as complete result files.
