# Dependency/CSP refresh: separate gate, not implemented in this candidate

The entire shipped vendor set is retained byte-for-byte from verified v0.19.0-rc1. The main visual design,
CSP, font stack and signing policy are unchanged. Reconstructed vendor chunks do not acquire authentic
provenance merely because regression comparisons pass.

## Investigation in this continuation
The raw GitHub download attempt failed DNS resolution. The current qualification environment contains
system Chromium but no managed Firefox or WebKit executable. No upstream component was downloaded,
updated, authenticated or replaced. Existing Python pins matched the installed environment.

Official Alpine CSP documentation describes an alternative evaluator without unsafe-eval, supporting
most ordinary Alpine expressions. This is not a drop-in promise for the current template: optional
chaining, event calls, templates, arithmetic and assignments must all be inventoried and qualified. The
inert Vite preload code remains in the inherited bundle. No claim of removal of every network primitive
or elimination of unsafe-eval is made.

## Acceptance for the separate refresh
1. Acquire exact authenticated/pinned upstream source and licence records for each component.
2. Inventory each original symbol, local modification, template expression and source-to-bundle step.
3. Build the CSP-compatible framework and remove unused preload functionality under a frozen scope.
4. Demonstrate the same native workflow, negative imports, privacy and reference results under the
   stricter CSP on supported real origins. No rule may be disabled merely to satisfy a framework.
5. Repeat complete qualification, independent review/rebuild and actual deployment acceptance on new
   candidate bytes. Keep one release pointer; do not silently replace this archive.

Primary documentation consulted: https://alpinejs.dev/advanced/csp and
https://playwright.dev/python/docs/browsers . These are explanatory references, not runtime downloads.
