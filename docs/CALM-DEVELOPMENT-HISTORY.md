# Development history, distinct from frozen acceptance

Existing accessible artifacts were hashed before work. The actual zen-work/dev-2.html
preview was recovered into the full v0.15.2 source assembly. Later calm-work source was
missing; its claimed 41/30 test passes were not reused. Architecture was recorded first.

Early static runs failed because test extraction assumed HTML attribute order and because
preservation allowlists still described the old UI. The new extractor requires a sole
inline module and exact CSP. Existing verification tokens are independently compared after
removing only the presentation's workspace reveal. Unchanged core module hashes remain.

New browser tests found duplicate Paste text, seed-word overflow under 200% text at 320px,
and Help returning to Test rather than the previous workspace. Corrected in preflight-4.
Other failures were stale assertions looking for metadata or guided controls before opening
the new disclosure; a hardcoded old version; keyboard modality setup; missing reactive
invalidation in an injected getter; an injected callback accidentally executed by Playwright;
and awaiting a disclosure's settled focus. These harness paths were corrected, not core rules.

An initial test module prefix split matched its own nested string and caused SyntaxError.
It now uses an anchored newline marker. A first screenshot helper lacked __file__. The
source-lock updater initially refused the absent explicit --development-update flag, and
a subsequent build lookup failed because no output had been created. Both are recorded
preflight errors, not passes. One tail command used invalid syntax after successful tests.

Several oversized combined development commands exceeded container execution windows,
including Node suites, combined browser suites, independent checks followed by release-tools,
and origins/browser grouping. Partial browser/core outputs were excluded. A killed browser
process recorded EPIPE after its parent was terminated. Small disjoint ranges completed
on rerun. There were no physical cameras or signing devices connected here.

All completed development failures and incomplete logs remain in the separate acceptance
support evidence. These do not count as successful final acceptance and are not erased.
Later final qualification is run only after candidate/archive hashes are frozen.
