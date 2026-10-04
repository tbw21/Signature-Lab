# Development record (pre-freeze)
- Verified exact v0.16.4 HTML/source hashes and extracted baseline unchanged.
- Supplied 16 vectors:48/48 independent HMAC/OpenSSL and48/48 shipped-reference matches.
- Additional12 digest/key boundary combinations reproduce36 further signatures; OpenSSL
  deterministic signing separately agrees with the Python plain-RFC6979 computation.
- Extraction helper initially assumed an unindented JSON brace and stopped. Whitespace-only
  extraction corrected; dependent Node probe initially lacked the JSON. No vectors guessed.
- Three browser fault tests initially returned the RNG-hook function as page.evaluate's
  completion value; Playwright invoked it without a buffer. Corrected only the test wrapper
  to a no-return arrow; all three fault scenarios then executed and passed. No runtime
  protection was relaxed. Entire complete preflight/acceptance follows separately.
- A streaming exec request was unsupported and executed no command; normal execution used.
- First development dispatcher was explicitly stopped after detecting that its development
  archive still contained the previous manifest. That partial run is excluded; generate the
  current manifest before restarting complete preflight. No candidate was frozen or edited.
- Historical exact-byte tests now reverse only the declared, literal startup/Help additions
  before testing older scoped preservation contracts. New R-S01/R-S10 separately require
  exact baseline hashes and reject undeclared edits/missing gate. No old golden hash replaced.
- Successful status stays inside existing Help; no new top-screen badge. All signing math,
  policy IDs/defaults, transaction/metadata/QR/camera/evidence behavior preserved.

- Standalone full reference contract selection exposed a test-isolation error: replacing
  getRandomValues on the shared Node WebCrypto instance leaked into a later case. The
  stub now replaces only its VM-local crypto object. The affected development dispatch was
  explicitly stopped; final full preflight starts from scratch. This was not a wallet RNG bug.
- Missing startup module inspection showed the error renderer could itself reference an
  absent gate. Added a typeof guard, retaining fail-closed behavior and producing an explicit
  startup failure instead of leaving the initial loading message. Browser fault injection
  now removes the actual gate binding, rather than substituting an early test exception.
