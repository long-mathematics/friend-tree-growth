# Upstream sources and attribution

The original-model numerical certificate builds on Can Uzay's
[`friend-tree-exponent`](https://github.com/uzay-eth/friend-tree-exponent)
project. The new contribution checked here is a constant per-core correction
of its upper motif potential and an exact re-evaluation of the corresponding
vertex reserves, together with the analytic arguments in the main manuscript.

## Reproducible numerical inputs

The numerical inputs are pinned to commit
[`ba2ec2e1935e0858e6bae2b40a9ee07c9b5665aa`](https://github.com/uzay-eth/friend-tree-exponent/tree/ba2ec2e1935e0858e6bae2b40a9ee07c9b5665aa).
They are fetched on demand, not embedded in the source distribution. The exact
file hashes are recorded in `verification/upstream_manifest.json`.

| Input | Use |
| --- | --- |
| `verify/motif-bracket/cert_format.h` | Certificate layout shared by builder and verifier |
| `verify/motif-bracket/cert_build.c` | Generates the proposed rational coefficient arrays |
| `verify/motif-bracket/cert_verify_gmp.c` | Performs the complete exact GMP verification |
| `verify/motif-bracket/verify_python_cross.py` | Supplies an independently written finite-tree evaluator for comparison |
| `LICENSE` | Preserves the complete upstream license and attribution |

The recorded certificate binary has SHA-256
`3a4aef888a5b567a8ada05f9546f98c979d361da9f9b33ba6e794eb91fb30abe`.
It is generated locally and is not committed. The patch applied to the GMP
checker only adds an exact minimum-slack recorder in the existing vertex checks;
`verification_patch.diff` is written with each full run so that this modification
can be inspected.

The floating-point proposal builder is compiled with `-ffp-contract=off`.
Fused multiply-add contraction on `x86-64-v3` can change the proposed rational
coefficient bytes even when the exact inequalities pass. Disabling contraction
reproduces the pinned binary in the controlled compiler experiment recorded in
`verification/compiler_reproducibility.json`. The upstream source files, GMP
checks, rational constants, and certificate hash remain unchanged.

The original exponent-existence proof is cited separately at the more recent
immutable revision
[`88f2f9c8c3ebc1b4e0c980db6afd97d29f3df176`](https://github.com/uzay-eth/friend-tree-exponent/tree/88f2f9c8c3ebc1b4e0c980db6afd97d29f3df176).
The two revisions serve different purposes; the older numerical pin does not
identify the version of the existence argument used by the manuscript.

## Licensing

Upstream files under `verify/` are licensed under the MIT License, copyright
2026 Can Uzay. The fetcher includes the complete original `LICENSE`, and the
upstream copyright and permission notice must accompany any redistributed copy
or substantial portion of that code.

Upstream prose, proofs, and reports are licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
The verification runner does not fetch or redistribute those texts. References
in the manuscripts credit the mathematical input. Licensing of this repository's
own material does not replace or alter the upstream licenses.

The full exact checker remains Uzay's implementation. Running it again with a
slack recorder is reproducibility evidence, not an independently authored proof
checker. The separate Python finite-tree comparisons have their stated limited
scope.
