# Third-party materials and attribution

## Can Uzay's friend-tree exponent project

The original-model upper certificate extends the rational motif potential
from [uzay-eth/friend-tree-exponent](https://github.com/uzay-eth/friend-tree-exponent).
The original exponent's existence and coarse bounds are also explicit
mathematical inputs to the main draft.

The verification scripts retrieve only the specified immutable source files
and the upstream license into the ignored `.cache/` directory, verify their
SHA-256 hashes, and build the certificate locally. Exact revisions, individual
hashes, and the byte-level provenance are in [docs/UPSTREAM.md](docs/UPSTREAM.md).

The upstream verification code is MIT licensed, copyright 2026 Can Uzay.
Its notices are preserved in the fetched source and license. Upstream prose
and proofs are CC BY 4.0; the present repository cites them and does not bundle
their full text. The repository's MIT license does not change either
upstream license.

## Published mathematical sources

The papers cite the original sources of the network models, the local-model
root equation, branching-process limit theorems, and the Siegel–Shidlovskii
theorem. The bibliography gives primary source URLs and publication details.
External journal articles and arXiv full-text files are not distributed in
this repository.

## Verification scope

The full bound workflow reproduces the upstream checker and adds exact
corrected-row comparisons. It is not a separately implemented verification
of every upstream inequality. The written analytic proofs are separate from
the finite program output.
