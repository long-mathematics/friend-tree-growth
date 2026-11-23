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

The root checker produces intervals of width `2**-90` using rational enclosures
for the exponential-integral series. Floating-point values printed elsewhere
are display conveniences; they are not used to certify inequalities.

Individual commands are also available:

```sh
python3 scripts/core_clock_kernel.py --check
python3 scripts/inert_growth_kernel.py --check
python3 scripts/verify_infection_kernel.py
python3 scripts/check_van_root.py --output build/verification/van_root_checks.json
```

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
   floating-point proposals. The binary's digest must match the pinned data
   before it is accepted by the downstream evaluator.
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
certificate constants are reused.

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
