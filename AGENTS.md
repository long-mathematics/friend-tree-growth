# Research and implementation instructions

This repository contains mathematical research drafts by Christopher D. Long
and reproducible exact-arithmetic calculations. Read `README.md` and the
relevant proof-dependency document before changing a theorem or a checker.

## Mathematical fidelity

- Keep the original random friend tree and the modified local redirection
  models distinct. The original exponent is denoted by `mu`; the local-model
  exponent is `alpha_omega`.
- Do not claim irrationality or transcendence of the original exponent.
  The arithmetic theorem in the companion paper applies to the local models.
- Do not replace a uniform estimate by an estimate for each fixed environment,
  or interchange a supremum and an integral without proof.
- The proof of effective computability is a terminating certificate search.
  The repository does not implement an efficient arbitrary-precision solver
  for the original exponent. Preserve this distinction.
- The original exponent's existence and published upstream certificates are
  external inputs. Maintain immutable references and accurate attribution.
- Computer checks verify the stated finite inequalities. The analytic tail
  arguments, stochastic couplings, and limiting theorems require their written
  proofs; a passing program does not replace them.
- Any proposed strengthening must include its proof and a dependency audit.
  Mark conjectures and unresolved steps explicitly. Do not add placeholder
  proofs, axioms, or numerical evidence described as a theorem.

## Repository conventions

- Canonical manuscript sources and compiled PDFs are at the repository root.
  Supporting LaTeX sections are in `sections/`; executable tools are in
  `scripts/`; exact reference reports are in `verification/`.
- Preserve sole manuscript authorship as recorded in `CITATION.cff` unless the
  author explicitly changes it. Credit prior work and external code separately.
- Use exact integer or rational arithmetic for certificate decisions. Floating
  point may be used for exploratory calculations or displayed approximations,
  but it must not decide a rigorous inequality.
- Keep fetched upstream files and binaries in ignored `.cache/`. Preserve their
  licenses and validate the pinned hashes before using them.
- Keep generated build logs and temporary output in ignored `build/`.
- Do not commit credentials, personal correspondence, external full-text papers,
  historical chat transcripts, or unrelated research material.

## Validation

- Run `python3 scripts/run_checks.py` after changing exact checkers or constants.
- Run `python3 scripts/verify_bound.py` after changing the original upper-bound
  certificate or its imported dependencies.
- Run `python3 scripts/build_papers.py` after editing either manuscript, then
  inspect the affected rendered pages. Resolve undefined references and
  overfull boxes before treating the PDFs as final outputs.
- Record which checks actually ran; do not describe unexecuted remote CI as
  passing. No formal proof-assistant verification is currently claimed.
