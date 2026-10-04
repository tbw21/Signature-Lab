# Recovery/development record — not acceptance evidence

The previous v0.18.3 source/test/archive checkpoint was not available in the runtime or in
searched conversation/Library results. Only screenshots and earlier response notes remained.
Exact v0.18.2 HTML and source archive hashes matched the published unsigned hash record;
188 source manifest files matched. New candidate v0.18.4-rc1 avoids name reuse.

Initial adaptations of historical source/copy assertions passed 99 targeted static cases.
New node contract runs completed their cases but exited nonzero because the new harness
assigned a boolean to Node process.exitCode. Corrected to numeric 0/1; these first process
executions are not successful completed jobs. A combined 20-second invocation then terminated
partway through a contract range (17 cases), excluded. Bounded independent subprocess jobs
subsequently ran the complete contract selection successfully.

The new static test initially searched literal && in serialized HTML rather than reading the
attribute decoded by the HTML parser. It was corrected to inspect the actual disabled binding.
New browser tests initially used Playwright is_disabled() on a fieldset, which returned false
while DOM disabled=true, matches(':disabled')=true, its first button was disabled and the
application canReceive was false. The probe confirmed no bypass. The assertion now checks the
native disabled fieldset and effective disabled child control. An explicit-scan test required
an arbitrary top<300 despite the whole camera already being visible and the page at maximum
scroll; corrected to require the camera area in the viewport, preserving the actual usability
requirement. Neither change relaxes a signing or camera rule.

A diagnostic helper initially used its own __file__ path for an inherited harness include and
failed before executing a test. It was corrected to the actual test directory. All original
logs, failed reports and corrected fresh runs are retained separately from frozen acceptance.
No final-candidate freeze has occurred at this document's preparation. Later final results
belong in an external report; never edit this record after candidate freeze to imply earlier
failures were passes.
