# Public disposable fixtures

The mnemonic phrases in `crypto-vectors.json` and the published Dark Skippy example
are deliberately public test material. Never fund or reuse them for real savings.
`bitcoin-before.js` and the baseline HTML files are preservation/rollback fixtures,
not active runtime implementations or build inputs. Independent tests regenerate
public references from the current candidate before checking them with Python/OpenSSL.
