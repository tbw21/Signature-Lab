# Distribution recommendation — The Bitcoin Way Signature Lab

Status: design proposal, NOT a completed deployment. Do not publish a developmental or unsigned/hardware-unqualified candidate as an approved security tool.

## Topology

* Main thebitcoinway.com website: a concise introduction, what the tool checks and does not check, safety constraints, supported signer/firmware matrix based on observed hardware tests, FAQ and clear buttons: **Launch online**, **Download for offline use**, **View source / verify release**. No running the app in a WordPress or other CMS iframe.
* Independent, static HTTPS application origin: proposed `lab.thebitcoinway.com` subject to the owner verifying exact subdomain/cookie isolation. Build/deploy *the exact same qualified HTML file* as the immutable GitHub release asset. Avoid network scripts, analytics, GTM, support chat, external fonts, cookies, service workers and silently installed extensions. If main site sets cookies with Domain=.thebitcoinway.com, those can be sent to the lab subdomain; remove such cross-subdomain cookies or consider a different registrable application domain.
* GitHub public repository: original source provenance caveats, locked build inputs, tests, provenance, hardware acceptance, CHANGELOG/SECURITY.md, publisher-signed releases, hashes and verified, immutable release assets. One authoritative active release version and one release pointer. GitHub file is not a second build. An authenticated release-signing key must be established by TBW (not generated or impersonated here).

## Security and availability

* Preserve strict offline operation after the HTML has loaded: `connect-src 'none'`, no remote font/import/analytics. Explicit user-click outbound links may still navigate; server sees the initial IP/TLS connection. Explain this honestly.
* Do not inject any CMS assets into the HTML after build. Do not rewrite/minify at CDN level; compare deployed bytes with SHA-256 of signed immutable release before switching the current pointer.
* Keep cookies host-only, disable any shared main-site login state, no same-origin access to the CMS. Deploy the app on an independently permissioned static origin. Verify DNS ownership, HSTS and HTTPS cert renewal; GitHub Pages custom domains require domain verification and HTTPS enforcement.
* Plan HTTP response headers appropriate to the measured browser support. E.g., `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, a compatible restrictive CSP and minimally permissive `Permissions-Policy` that does not accidentally block requested camera access. The current HTML CSP requires `unsafe-inline`/`unsafe-eval`, so do not claim script CSP is strict until isolated migration qualification.
* Online app: human-facing evergreen landing link pointing to a checked versioned immutable HTML object; shorter `current` navigation pointer can change only after accepted new release. Download should have explicit version and checksum shown and point to independently signed immutable release; no mutable 'latest.zip' without a verifiable mapping.
* If hosting on GitHub Pages, log collection is governed by the provider; don't claim no web-server logs. The camera requires a secure context and explicit permission on the chosen origin; local file browser behavior must be measured, not assumed.

## Before switching a live pointer

1. Freeze acceptance candidate archive, record SHA-256; no edits during acceptance.
2. Verify source provenance and publisher signing; independently review supply-chain/cryptographic changes.
3. Rerun full software + negative + fault suite, real native-browser/file/HTTPS, offline reload, mobile camera and physical signer acceptance.
4. Verify clean extraction, locked rebuild and exact binary parity with the signed release.
5. Compare deployed response bytes, content type, restrictive headers and camera behavior from external devices; evaluate third-party cookie isolation.
6. Enable the new pointer only after sign-off; keep immutable prior version for rollback (fresh session, not in-place state migration).

## Landing page draft direction

**Signature Lab** — Check signatures. Question your assumptions.

Compare a disposable test wallet's signed transactions against expected deterministic signatures, inspect unexpected transaction metadata and save independent evidence. Entirely in your browser, with no account required and no signing inside the Lab.

**Not a firmware safety certificate.** A matching test cannot rule out conditional attacks or malicious firmware. Never enter a real seed, replace a real wallet or fund a test wallet.

Actions: Launch the Lab · Download offline · Verify on GitHub
