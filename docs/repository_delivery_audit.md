# Repository delivery audit

Audit date: November 23, 2026.

**Result:** the source distribution is ready for draft review. This was a
read-only consistency and packaging audit, apart from this report. It does not
replace the mathematical proof audits, certify the infinite-state arguments by
software, or claim that remote continuous integration has run.

## Manuscripts and local references

Both manuscript PDFs were present and matched the successful build report:

| Manuscript | Pages | SHA-256 |
| --- | ---: | --- |
| `friend_tree_growth.pdf` | 45 | `7db37e0453712d754ecb41ed9e7c8bfe32464ddad15367717b9360a677036233` |
| `local_redirection_irrationality.pdf` | 11 | `79f52368b1e6b38942886699995f203c4689f71feaecc060eacd14dc572c26bc` |

The build report records three compilation passes for each manuscript and no
unresolved references or overfull boxes. All 14 local Markdown links and all
22 LaTeX section inputs in the candidate distribution resolve to existing
files. Both title pages identify Christopher D. Long and the research-draft
date. This audit checked the PDFs and their build metadata; rendered-page
inspection is a separate part of manuscript preparation.

## Reproducibility evidence

The recorded source hashes in `quick_check_run.json` and
`bound_verification_run.json` match the corresponding current Python files.
Cross-report consistency checks confirm the following:

- The original certificate report records 17,329,108 exact GMP inequalities
  and 37 finite-tree checks.
- The corrected report records 484,138 vertex rows. Its beta, correction, and
  positive minimum margin agree exactly with the aggregate run report.
- The original, corrected, and aggregate reports identify the same certificate
  binary hash.
- The aggregate report records a fresh binary build, not binary reuse.
- Every recorded local-model bracket has exact width `2^-90`, with positive
  rational sign margins at both endpoints.

The expensive numerical checks were not repeated during this packaging audit:
their completed run and matching code hashes supplied the relevant evidence.
The JSON reports and instrumentation diff are part of the source distribution.
The original GMP verification log is deliberately retained by a narrow
exception to the log exclusion rule. Other transient logs remain excluded;
a fresh verification run regenerates them in its output directory.

## Commands and continuous integration

The README commands name existing portable entry points:

```sh
python3 scripts/run_checks.py
python3 scripts/verify_bound.py
python3 scripts/build_papers.py
```

Python file locations are derived from the repository layout, not a particular
host's workspace. The full verifier downloads only the hash-pinned upstream
inputs and preserves their license. Compiler and GMP requirements match the
full-certificate workflow; the LaTeX packages installed by the manuscript
workflow cover the manuscript preambles.

The three pinned GitHub Actions commits were checked against their official
repositories: `actions/checkout`, `actions/setup-python`, and
`actions/upload-artifact`. Each requested commit hash resolved exactly. Both
workflows request only read access to repository contents. Their presence and
configuration are not described as a successful remote run.

## Distribution and attribution

The Git candidate inventory excludes the downloaded upstream cache, the large
certificate binary, compiled executables, build output, external full-text
papers, and unrelated files. A targeted scan found no host-specific workspace
paths, credential patterns, private-key blocks, or chat attachment paths in
the candidate text files. The only PDF files are the two project manuscripts.

The license, citation metadata, third-party notice, and upstream provenance
document consistently identify authorship and attribution. Numerical inputs
are pinned separately from the newer upstream exponent-existence proof.
Upstream verification code and proof text retain their distinct licenses.

## Mathematical claim boundaries

The README, proof-dependency documents, and research targets consistently
separate the original exponent from the local-model exponents. They state the
implemented numerical certificate and finite-kernel calculations, while
identifying the general original-model computation theorem as a termination
result rather than a practical arbitrary-precision implementation.

Original-model irrationality and transcendence remain open. The local-model
irrationality statement is restricted to finite algebraic activation
parameters, and no transcendence classification of those exponents is claimed.
The original boundary-robustness statement concerns the specified bounded
predictable root-leaf inputs and continuous-time mean exponents. No general
graph-perturbation invariance or original-model normalized amplitude theorem is
advertised. These boundaries agree with the current proof-status documents.
