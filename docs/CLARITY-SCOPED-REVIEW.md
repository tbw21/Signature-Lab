# Scoped security/UX review

The user requested a simpler interface, not weaker verification. The source delta is restricted
to src/page.html, src/style.css and two presentation entry points in src/20-application.js.
The existing runDemonstration/Up signature path is unchanged. The modal has one native visibility
state and one existing example result, not a duplicate test wallet or verifier. It cannot write
to the private prepared/result/journal closures. Existing trust boundaries remain.

The isolated example deliberately does not replace the active wallet: re-signing the public
fixture on honest hardware would not reproduce the malicious recorded signature. Mixing a
recorded response into an ordinary result could falsely suggest a user's device was tested.
One-click access is implemented without that ambiguity. A labelled recorded-example modal
loads and checks the known response directly. It is not exported as a physical-device result.

Wallet replacement remains a distinct action because changing 12 to 24 words is not a way to
create another wallet of the same length. Its placement is quiet; its destructive consequence
is explicit. Existing generator and reset semantics are unchanged. Do not fund any generated
address or weaken signer safeguards.

Native font selection does not promise identical glyphs or OS rendering. A single native-family
stack with tabular digits/no ligatures on technical fields preserves strings. External fonts
and runtime network access remain prohibited by the unchanged CSP. Real OS legibility and
optical tests remain outstanding.

Changing workspaces no longer invokes scrollIntoView; focus stays keyboard-accessible using
preventScroll. Shared navigation/identity rows remain present so the active panel's top stays
consistent. Focus/scroll for deliberate step transitions and Help still works as before.

No broad security audit or higher attack-detection probability is claimed. Dependency origins,
authenticated release signing, independent organizational review and actual platform/signer
acceptance remain open. Orange Foundation observations are not diagnosed by these UI changes.

Primary platform references reviewed: W3C CSS Fonts Level4 system-ui, CSS Overflow Level3
scrollbar-gutter, and WHATWG HTML focus preventScroll. The direct standards pages were retrieved;
an initial search returned irrelevant results which were not relied on.
https://www.w3.org/TR/css-fonts-4/
https://www.w3.org/TR/css-overflow-3/
https://html.spec.whatwg.org/multipage/interaction.html
