# Reproducing the exact checks

The repository contains two different kinds of verification: small exact checks
of formulas used in the proofs, and a complete rerun of the finite motif
certificate supporting the improved numerical upper bound. Neither is a formal
verification of the manuscripts. The probabilistic comparison arguments and the
reductions from infinitely many states to finite inequalities remain mathematical
proofs in the main paper.

All commands below run from the repository root. Use Python 3.10 or later,
without `-O` or `PYTHONOPTIMIZE`: the scripts deliberately use assertions for
mathematical checks. Python dependencies are from the standard library.

## Fast checks

```sh
python3 scripts/run_checks.py
```

The default output directory is `build/verification/`. To write reports elsewhere,
add `--output-dir PATH`. The committed reports in `verification/` record a
successful run, with source hashes in `quick_check_run.json`.

| Script | Checks | Scope |
| --- | --- | --- |
| `core_clock_kernel.py --check` | 210 exact comparisons with ordered leaf-event histories; mass identities; burst tails; first-promotion truncations; finite profiles | Checks the eliminated waiting-event kernel, including silent inert-boundary choices |
| `inert_growth_kernel.py --check` | 180 comparisons with individual-clock recursion; null-ring accounting; generation-profile and reward tails | Checks finite approximations to the inert generation coefficients |
| `verify_infection_kernel.py` | 16 exact occupation terms at each degree 2 through 63; the large-degree numerical inequality; absorption constant | Supplies the finite arithmetic part of the boundary-disagreement estimate |
| `check_van_root.py` | Rational root brackets for PAN, DAN, and VAN with parameter 2; 1,100 coefficient denominator checks | Supports the companion paper's root computation and examples; the irrationality proof is analytic |
| `check_first_promotion.py --check` | 106,865 exact finite checks of null-event elimination, independent backward recursion, reduction boundaries, tail signs and widths, and good-prime valuations | Supports the original inert newborn's first-promotion formulas; the infinite tails and height asymptotics require the written proofs |
| `check_critical_root_forms.py` | Finite signed certificate-polynomial construction and exact arithmetic checks | Supports the full-critical noncancellation and algebraic-root construction; the infinite limit and arithmetic scope require the written proofs |
| `rapid_root_tools.py` | Exact Yule-tail identities, cutoff selection, and equality-safe trisection on demonstration roots | Implements computational helpers; it does not implement the full friend-tree certificate search or produce new digits of `mu` |
| `full_tree_recurrence.py --check` | Exact free-tree coefficients and two independent transition calculations; core and promotion-rate drift identities; the six-vertex closure diagnostic | Checks the first two levels of the full-model recurrence hierarchy; it does not prove a finite scalar closure or an asymptotic error bound |
| `primitive_population_tools.py --check` | 1,340 exact checks of proper-birth sums, all reachable poles through five births, primitive numerator/content arithmetic, independent recursions, omitted histories, and rational population tails | Supports the population-only hierarchy; the all-budget residue signs, primitive-growth asymptotic, and infinite error theorem require their written proofs |
| `laplace_derivative_tools.py --check` | 3,686 exact checks of complete homogeneous polynomials, independent Newton identities, and beta-derivative tail telescoping | Gives rational enclosures for fixed derivatives; no effective derivative-order rate or certified bracket for `mu` |
| `check_generator_obstructions.py --check` | 29 exact checks of star formulas, edge-start derivatives, a negative Hankel determinant, a negative-square certificate, and a prime-cancellation example | Supports the stated generator and spectral obstructions; the all-order star-pole theorem is analytic |
| `check_bipartite_products.py --check` | Whole-polynomial generator and expectation identities through population 10 in both free and inert models, harmonic coefficients, second moments, integer binomial values, and star probabilities | Supports the signed product and variance identities; true-martingale and exponent statements require the written proofs |
| `check_product_insertions.py --check` | 1,167 exact checks of entire bivariate polynomials on all free trees through population 9 and their finite-population recurrences | Checks the core, color, and core-count-generating insertions; it does not close their remaining neighbor-dependent expectations |
| `check_product_countermodel.py` | 944 exact checks on all 94 unlabelled trees through population 9 and the uniform-color expectation bound | Checks a distinct rational-growth comparison process, not the original exponent |

The root checker produces intervals of width `2**-90` using rational enclosures
for the exponential-integral series. Floating-point values printed elsewhere
are display conveniences; they are not used to certify inequalities.

The first-promotion checker records its reference results in
[`first_promotion_checks.json`](../verification/first_promotion_checks.json).
Its default finite grid has 14 rational parameters, indices through 80,
and primes through 251. Transform intervals use exact rational endpoints
with decimal endpoints rounded outwards. The report separately labels
floating denominator-growth diagnostics as exploratory; they establish no
asymptotic or arithmetic classification. These intervals evaluate the
first-promotion transform and are not new estimates of `mu`.

The critical-root and rapid-root reports distinguish finite checks from
the limiting theorems. In particular, the exact-pressure iteration's
factor `73/82` is an analytic result that assumes exact or certified
pressure evaluations. The trisection scheduler's geometric rate counts
completed certificate stages, and its demonstration roots do not replace
the missing full-model strict-certificate search implementation.

The full-tree recurrence calculator starts from the edge, with `a_2=0`
and promotion rate `Lambda(edge)=2`. Its reference report
[`full_tree_recurrence_checks.json`](../verification/full_tree_recurrence_checks.json)
records exact coefficients through population 10 and retains every target
multiplicity when merging isomorphic trees. The written countable
recurrence, differential hierarchy, and operator-factorial representation
remain analytic statements; finite coefficient checks do not classify
the growth exponent or establish convergence of normalized promotion rates.

The population-only checker removes all null rings before applying its
proper-birth cutoff. The resulting rational functions are reduced in
`Q(s)`, and their integer numerators are divided by content. Its reference
report is
[`primitive_population_checks.json`](../verification/primitive_population_checks.json).
The exact `487/488` comparison is a necessary budget for reaching the
current exponent enclosure, not an assertion that 488 births suffice.
Its public tail helper uses rational upper root bounds, so returned
outer errors make no floating-point proof decisions.

The derivative helper's
[reference report](../verification/laplace_derivative_tool_checks.json)
encloses derivatives at a fixed discount using exact full-tree coefficients.
The caller must supply the actual coefficients; elementary size-bound
validation alone does not prove their provenance. These intervals enclose
the fixed-index ratios, while the limit in derivative order has no
certified rate. The
[generator obstruction report](../verification/generator_obstruction_checks.json)
records exact identities; its negative generator-moment Hankel matrix is
different from the positive time-tilted moment matrices in the manuscript.

The Yule helper evaluates an exact finite binomial-tail expression at a
rational survival parameter. Using a rational lower bound for `exp(-T)`
gives a rigorous upper bound on the population-discard error at time `T`.
Spatial-profile and quadrature errors must still be controlled separately.
The written generation-tail theorem similarly gives a geometric bound
only above a certified upper bound on `mu`, not at the critical point.

Individual commands are also available:

```sh
python3 scripts/core_clock_kernel.py --check
python3 scripts/inert_growth_kernel.py --check
python3 scripts/verify_infection_kernel.py
python3 scripts/check_van_root.py --output build/verification/van_root_checks.json
python3 scripts/check_first_promotion.py --check --output build/verification/first_promotion_checks.json
python3 scripts/check_critical_root_forms.py
python3 scripts/rapid_root_tools.py
python3 scripts/full_tree_recurrence.py --check --output build/verification/full_tree_recurrence_checks.json
python3 scripts/primitive_population_tools.py --check --output build/verification/primitive_population_checks.json
python3 scripts/laplace_derivative_tools.py --check --output build/verification/laplace_derivative_tool_checks.json
python3 scripts/check_generator_obstructions.py --check --output build/verification/generator_obstruction_checks.json
```

To compute a different finite prefix of the full-tree coefficients, use
`python3 scripts/full_tree_recurrence.py --max-population N`. Its JSON output
includes the rational means and the final unlabelled-tree distribution.
The number of states grows quickly; this coefficient enumeration is not a
critical-exponent solver.

To compute a proper-birth lower coefficient and its primitive polynomial,
for example, run:

```sh
python3 scripts/primitive_population_tools.py --generation 2 --s 1/2 --max-births 3 --polynomial
```

The module also provides a rational fixed-generation population-tail
helper. The derivative module provides `beta_derivative_weights`,
`derivative_tail`, and `enclose_derivatives` for use with the full-tree
calculator's exact coefficients. Enumeration remains costly, and these
helpers do not implement the missing outer critical-limit error.

## Manuscripts

Build all three research drafts with a standard LaTeX installation:

```sh
python3 scripts/build_papers.py
```

The individual selectors are `--paper original`, `--paper local`, and
`--paper transcendence`. PDFs are written at the repository root; logs and
the build report go to ignored `build/papers/`. The build rejects unresolved
references and overfull boxes. Inspect affected page renders after changes
to manuscript content. The
[transcendence audit](transcendence_proof_dependencies.md) separates finite
checks from the analytic and number-theoretic arguments they support.

## Full corrected motif certificate

The full check needs a C compiler named `gcc`, OpenMP, and the GMP development
headers and library. On Debian or Ubuntu, the corresponding packages are
`build-essential` and `libgmp-dev`.

```sh
python3 scripts/verify_bound.py
```

The runner performs the following steps:

1. Fetch five small inputs from the immutable upstream revision in
   `verification/upstream_manifest.json`. Every downloaded file must match its
   SHA-256 digest. The complete upstream license is included.
2. Compile the upstream builder and construct `upper_5665.bin`. The builder uses
   floating-point proposals. Compilation disables fused multiply-add contraction
   with `-ffp-contract=off` so that multiply/add rounding reproduces the pinned
   coefficient bytes on newer processor targets. The binary's digest must
   match the pinned data before it is accepted by the downstream evaluator.
3. Compile and run the upstream GMP checker, with a patch that records the
   minimum vertex slack. Its original inequality tests remain in place. Require
   **17,329,108 exact inequalities with zero failures** and the original tree
   checks to pass.
4. Check all **484,138** corrected vertex rows in Python `Fraction` arithmetic,
   including the tail endpoint rows, at the fixed rational values
   
   \[
   \beta=\frac{2832242711}{5000000000},\qquad
   \tau=\frac{5294970481}{100000000000000}.
   \]
   
   The verified minimum margin must equal
   
   \[
   \zeta=\frac{199752266575452391}
   {1200500000000000000000000000}>0.
   \]
5. Compare the evaluator with the upstream independently written Python
   evaluator on selected finite trees and boundary limits, and check selected
   corrected drift, jump, and kernel intervals.

The full rerun checks the inherited edge, vertical-motif, and cherry inequalities
as well as the new vertex inequalities. A run of only
`continuation_certificate_bounds.py` is **not** a substitute for step 3.
Likewise, the finite evaluator comparisons are useful implementation checks but
do not replace the full certificate or the all-degree tail proof.

The proof in the main paper explains how the tail endpoints cover every degree,
how the corrected vertex reserve combines with the unchanged motif inequalities,
and how the resulting drift inequality gives
`mu <= 0.5664485422`. No claim of an independent second implementation of the
complete GMP verifier is made.

### Cache, offline use, and resources

Downloaded files go to `.cache/upstream/`. Compiled programs, the approximately
139 MB certificate, and build logs go to `.cache/motif-certificate/`. Neither
directory belongs in version control. Keep roughly 1 GB of free memory and
several hundred MB of disk space available; runtime depends on the machine.

To fetch only the pinned sources:

```sh
python3 scripts/fetch_upstream.py
```

After a successful build, all decisive checks can be repeated without network
access or rebuilding the binary:

```sh
python3 scripts/verify_bound.py --offline --reuse-binary
```

`--source-dir`, `--work-dir`, and `--output-dir` allow alternative locations.
An explicitly supplied source directory is still checked against the same
manifest. A mismatching existing source is rejected rather than silently
overwritten. A builder output with a different digest also fails closed;
platform-dependent numerical proposals must be investigated before the
certificate constants are reused. The exact checker and its source/data pins
are unchanged by the builder's floating-point compilation setting. A controlled
`x86-64-v3` experiment is recorded in
`verification/compiler_reproducibility.json`.

If a child verifier fails, the runner prints the diagnostic log tail and copies
available builder and GMP logs into the report directory before exiting. CI
therefore retains the underlying failure, even when no final JSON report can
be written.

## What the implementation does not claim

The main paper proves termination of an arbitrarily accurate rational bracketing
algorithm for the original exponent. This repository currently implements the
exact finite waiting-event kernels, selected lower-witness computations, the
concrete improved upper certificate, and supporting arithmetic checks. It does
not implement an efficient general arbitrary-precision solver for the original
exponent, supply a useful complexity bound, or numerically prove irrationality.

The companion paper concerns different local redirection models. Its root
brackets and irrationality theorem do not transfer to the original exponent
without an additional mathematical argument.
