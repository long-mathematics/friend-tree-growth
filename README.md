# Friend-tree growth

Research drafts and exact verification programs by **Christopher D. Long**.

This project studies the growth exponent of the original random friend tree
and the arithmetic of exponents in a related family of local redirection
trees. It contains two manuscripts with different scopes.

## Manuscripts

| Draft | Main results | Files |
| --- | --- | --- |
| **Effective computation and boundary robustness of the random friend-tree exponent** | An exact pressure characterization, a terminating two-sided computation theorem, a uniform boundary-leaf resolvent estimate, robustness under bounded predictable boundary input, and a sharper rational upper bound for the original exponent. | [PDF](friend_tree_growth.pdf) · [LaTeX](friend_tree_growth.tex) |
| **Growth and irrationality in local redirection trees** | An exact CMJ representation, almost-sure power-law growth from every finite tree seed, effective root isolation, and irrationality for every finite algebraic activation parameter. | [PDF](local_redirection_irrationality.pdf) · [LaTeX](local_redirection_irrationality.tex) |

These are research drafts dated November 23, 2026. The repository includes
written proofs, internal dependency audits, and reproducible finite
calculations. It does not claim external peer review or proof-assistant
formalization.

## Original random friend tree

At each step, choose an existing vertex uniformly, choose one of its
neighbours uniformly, and attach a new vertex to that neighbour. Let `C_n`
be the number of nonleaf vertices. The existence of the deterministic
exponent `mu`, and the initial bracket `0.5650 <= mu <= 0.5665`, are inputs
from [Can Uzay's proof and certificate repository](https://github.com/uzay-eth/friend-tree-exponent).
The model originates in [Krapivsky and Redner (2017)](https://arxiv.org/abs/1706.01514).

The first manuscript establishes the following results using those explicit
inputs.

1. **Exact characterization.** In the inert-parent newborn process, let
   `A_m(s)` be the expected sum of `exp(-s * birth_time)` over genealogical
   generation `m`. The limit `r(s) = lim_m A_m(s)^(1/m)` exists, is positive,
   continuous and strictly decreasing, and has its unique crossing at
   `r(mu) = 1`.
2. **Uniform boundary control.** For the discounted core-count resolvent,
   adding one leaf at the retained root has a bound independent of the size
   and shape of the existing finite component. A subcritical disagreement
   exploration proves this bound.
3. **Effective computability.** A dovetailed search of finite rational lower
   and upper certificates terminates with a bracket of any prescribed
   positive rational width. A rational series for `mu` follows, with a
   certified remainder after each completed stage. No useful running-time
   bound or implemented high-precision solver for this search is claimed.
4. **Boundary robustness.** For each fixed finite bound `Q`, the uniform
   infimum and supremum of continuous-time mean growth over the specified
   predictable root-leaf input policies `0 <= q_t <= Q` both have exponent
   `mu`. This statement is about the explicitly defined boundary policies.
5. **Sharper certificate.** A constant-per-core correction to the upstream
   potential proves

   ```text
   0.5650 <= mu <= 2832242711 / 5000000000 = 0.5664485422.
   ```

   This narrows the upstream interval by about 3.43%. The finite rational
   inequalities and their analytic all-degree extensions are both documented.

The precise proof dependencies are in
[the original-model audit](docs/original_proof_dependencies.md). The numerical
improvement reuses and credits the upstream potential tables; it does not
claim a new independent construction of those tables.

## Local redirection models

The companion paper studies `VAN(omega)`, including `PAN = VAN(0)` and
`DAN = VAN(1)`, for finite `omega >= 0`. These are the models introduced by
[Hartle, Krapivsky, Redner, and Zhang](https://arxiv.org/abs/2604.01540).
Their characteristic equation is

$$
F(s)=\int_0^1 x^s e^{x-1}\,dx
=\frac{(1-s)(s+\omega)}{\omega+(1-\omega)s},\qquad 0<s<1.
$$

The manuscript proves the exact probabilistic identification of the unique
root `alpha_omega`, the almost-sure limit
`C_n / n^alpha_omega -> Z` with `0 < Z < infinity` for every finite tree seed with at least two vertices,
and computability for computable `omega`. For algebraic `omega`, a
Siegel–Shidlovskii specialization proves that `alpha_omega` is irrational.
The characteristic equation is credited to Hartle and coauthors; its
appearance here is not a priority claim.

The [local-model audit](docs/local_model_proof_audit.md) records the
branching-process and arithmetic inputs. The exact example brackets are in
[verification/van_root_checks.json](verification/van_root_checks.json).

## Questions still open in this work

- Irrationality or transcendence of the **original** exponent `mu`.
- Transcendence of the local-model exponents `alpha_omega`.
- A practical, certified arbitrary-precision solver for the original exponent.
- A finite special-function equation for the original exponent with the
  specialization and nonvanishing properties required for an arithmetic proof.
- Sharp mean asymptotics or a positive almost-sure power-law amplitude for the
  original process.

The [research targets](docs/RESEARCH_TARGETS.md) distinguish these goals from
the completed arguments. In particular, computability and a positive Mellin
kernel do not by themselves imply irrationality.

## Reproduce the calculations

The quick suite uses Python 3.10 or later and the standard library:

```bash
python3 scripts/run_checks.py
```

The full original-model certificate check also needs a C compiler with
OpenMP and GMP development headers. It fetches hash-pinned upstream files,
builds the certificate in an ignored cache, verifies the upstream
inequalities, and checks the corrected vertex rows:

```bash
python3 scripts/verify_bound.py
```

See [verification instructions](docs/verification.md) for the scope, commands,
dependencies, and reference reports. See [upstream provenance](docs/UPSTREAM.md)
for immutable revisions and file hashes. Re-running the same upstream
checker is described as reproduction, not as an independent implementation.

Build both manuscripts with a standard LaTeX installation:

```bash
python3 scripts/build_papers.py
```

The build tool writes the PDFs at the repository root and keeps temporary
files in `build/papers/`. It rejects unresolved references and overfull boxes.
The GitHub workflows run these commands when the repository is hosted there;
their presence is not a claim that a remote run has occurred.

## Citation, attribution, and license

Use [CITATION.cff](CITATION.cff) for project metadata and cite the appropriate
manuscript for its mathematical results. Original materials in this project
are under the [MIT license](LICENSE). Downloaded upstream verification code
retains Can Uzay's MIT notice; upstream proof text has its own CC BY 4.0
license and is cited rather than bundled. See
[third-party notices](THIRD_PARTY_NOTICES.md).

AI tools assisted with proof exploration, literature checking, code, and
manuscript preparation. The papers present the arguments and dependencies
explicitly so they can be checked independently.
