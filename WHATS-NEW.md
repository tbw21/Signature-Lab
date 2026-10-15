# What's New — TBW Signature Lab

## Testing and wallet safety

- Start with a straightforward payment test before progressing through varied scenarios.
- Show supported BIP84 native SegWit, single-signature ECDSA scope before testing.
- Warn against entering real seed words, overwriting an existing signer wallet, or funding a disposable test wallet.
- Keep the recorded Dark Skippy example accessible without competing with the main signing workflow.

## Privacy and session controls

- Add cooperative browser spellcheck, autocomplete, autocorrect, and writing-assistance opt-outs on editable fields, including fields added dynamically.
- Mark seed words and technical identifiers to discourage automatic browser translation.
- Offer optional, bounded evidence retention before signed-response intake, disabled by default.
- Add a separately confirmed **Finish testing** action that stops capture, retires app-owned wallet/session state, and leaves the active workflow.
- Keep **End guided session** separate from **Finish testing**, preserving the distinction between recording a session and retiring the wallet.

## Interface and navigation

- Simplify the Test wallet heading, progress navigation, controls, and spacing.
- Move the three-step progress indicator into the Test workflow only.
- Improve visual hierarchy, alignment, typography, action-button sizing, and disclosure panels throughout Test, Transaction, Results, Advanced, Session, and Help.
- Use quieter safety notices and custom-settings warnings while retaining their text.
- Improve QR-transfer layout, response intake, result presentation, and mobile reflow.
- Standardize modal dialogs, confirmation actions, error/empty states, footer, and Help navigation.
- Restore a minimum 44-pixel workspace-navigation target height.
- Correct Session overview wrapping at 200% text enlargement on narrow screens.
- Restore a visible selected workspace border in high-contrast/forced-colors mode.

## Advanced tools

- Reorganize guided-session planning, transaction controls, and device notes into cleaner expandable sections.
- Reduce redundant nested borders, labels, and cards.
- Improve transaction editor spacing, input/output rows, and settings alignment.

## Session records

- Emphasize completed checks with supporting match, review, and difference counts.
- Move detailed count explanations into **How to read this record**.
- Clarify the session empty state, evidence controls, and record exports.
- Visually separate the **Finish testing** action and its unsaved-data warning.
- Improve session-history entries, responsive layouts, and evidence disclosures.

## Other corrections

- Correct the optional firmware-version input markup.
- Update Help and accessible release labels to distinguish development previews from approved releases.
- Align The Bitcoin Way and original-author copyright notices across the license and application.
