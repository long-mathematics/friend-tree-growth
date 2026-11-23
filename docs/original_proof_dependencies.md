# Original-model proof dependencies

This document records the mathematical scope of `friend_tree_growth.tex`.
It is a dependency map for the current research draft, not a claim of
external peer review or proof-assistant certification.

## Imported inputs

| Input | Exact source | Use |
| --- | --- | --- |
| Existence of a common continuous-time mean exponent and discrete power exponent; `0.5650 <= mu <= 0.5665` | Can Uzay, `friend-tree-exponent`, existence and bracket proofs; proof revision `88f2f9c8c3ebc1b4e0c980db6afd97d29f3df176` | Identifies the exponent under study; `mu > 11/20` is needed for the uniformity closure. |
| Weighted planted-branch comparison, good-history root selection, and finite-seed comparison | Same revision, `proofs/existence.md`, Lemma 4.1(c), Corollary 5.3, Lemma 6.1 | Identifies the inert newborn mean exponent with the original exponent. The unweighted planted-versus-free ordering is neither imported nor asserted. |
| Upper motif arrays, extrapolation rules, and drift decomposition | Numerical revision `ba2ec2e1935e0858e6bae2b40a9ee07c9b5665aa`, `verify/motif-bracket/` | Supplies the unchanged potential to which the exact correction is applied. Source and binary hashes are in `verification/upstream_manifest.json`. |

The almost-sure logarithmic exponent theorem is cited for context. It is
not used to prove a new almost-sure amplitude or a new boundary-control
almost-sure statement.

## Internal analytic chain

| Stage | Source section | Main dependency and conclusion |
| --- | --- | --- |
| Exact model and kernel | `sections/original/model_kernel.tex` | Full core state includes leaf counts, real core neighbours, and inert stubs. Independent Yule bursts give explicit beta weights. Null stub choices are included. The tagged-child kernel retains the entire environment. |
| Permanent inert comparison | `inert_comparison.tex` | An exterior-only no-return construction has probability at least `1/6`; newborn preparation contributes `1/[2(s+3)]`. This proves `A_m(s;x) >= A_m^infty(s)/[12(s+3)]` uniformly in environment and generation. |
| Actual generation limit | `inert_comparison.tex` | Positivity and supermultiplicativity give the genuine limit `r_infty(s)`, rather than a limsup. |
| Inert mean exponent | `inert_growth.tex` | Uniform finite preparation and the imported weighted planting estimate give the lower exponent. A genuine high-degree-parent embedding gives the upper exponent. Thus the inert newborn has mean exponent `mu`. |
| Exact pressure crossing | `pressure.tex` | Tonelli identifies the discounted generation sum with the mean Laplace transform. Finite convexity and the bound `log r_infty(s) <= -log s` give strict decrease and the unique root `r_infty(mu)=1`. |
| Effective coefficients | `coefficient_computation.tex` | The potential-Yule core-ring tail and first-discard real-birth errors produce finite rational intervals for every fixed `A_m^infty(s)`. Positive lower histories give complete strict lower certificates. |
| Uniform mean exponent | `uniform_means.tex` | Future-child decomposition yields the old-core bound and submultiplicativity of `H(t)=1+integral G`. This constructs `lambda >= mu` without assuming equality. |
| Finite environment reduction | `locality.tex`, `finite_time_computation.tex` | Potential arrows use only initial exterior clocks and are independent of the tagged potential genealogy. Finite depth/degree profiles have an explicit uniform error. Yule population cutoff and rational uniformization compute every fixed `H(T)`. |
| Finite-window potential | `finite_window.tex` | A common-vertex coupling proves ordinary-birth sensitivity `exp(2t)`. A block with `exp(-sT) H(T)<1` gives a supersolution with bounded ordinary-birth increments whenever `s>lambda`. |
| Controlled moments | `controlled_moments.tex` | The finite-window potential and shifted-Yule population moments give every fixed controlled core moment with normalized exponent `lambda`. This does not use `lambda=mu`, and the controlled processes are not silently treated as genuine finite exteriors. |
| Bounded-parent stabilization | `parent_stabilization.tex` | A birth-death immigration comparison and permanent neighbour slots bound late changes before a parent-degree cutoff. |
| Reference-law likelihood | `likelihood.tex` | Only the parent degree-gain channel is changed to `(1+t)^(-2)`. There are finitely many such changes before cutoff, so the forward loss is polynomial. Conditional inverse-degree occupation bounds control the inverse likelihood. |
| Hybrid gap under a hypothetical exponent gap | `hybrid_gap.tex` | Controlled moments, stabilization, and finite-seed likelihood comparisons give strict subcriticality of bounded-parent histories when `mu<lambda`. Early/late crossing decomposition proves the same for the process deleting arrivals after a sufficiently high-degree crossing. No new root-leaf gradient is used here. |
| Uniform boundary-leaf estimate | `boundary_gradient.tex` | Maximal coupling of aggregate gain and promotion channels; a dynamically explored common core tree; full charging of every family born after its parent's first disagreement. The local reservoir is dominated by a pure-birth process with rate `n+5/2`. Its outward discounted reproduction mass is at most `19/20` at `s=11/20`. |
| Uniformity closure | `boundary_gradient.tex` | The finite-horizon bound is proportional to finite `W_T(s)`, so no uniform resolvent finiteness is assumed. Dynkin's identity and absorption with `M>=132` contradict a hypothetical `mu<lambda`. Hence `lambda=mu`. |
| Effective two-sided computation | `computability.tex` | Complete lower and upper strict-certificate searches are dovetailed. Density of rational endpoints gives termination at every positive rational tolerance, without deciding equality of any proposed rational and `mu`. A positive rational series with a prescribed remainder follows. |
| Canonical resolvent | `canonical_resolvent.tex` | Uniformity supplies finiteness above `mu`. Time-block tails compute `V_s` effectively; first-step decomposition gives the exact nonnegative eliminated-kernel series. The boundary-leaf estimate passes to infinite time. |
| Uniform bounded-input robustness | `boundary_robustness.tex` | The resolvent yields the upper rate for every bounded predictable root-leaf input. Finite preparation of an arbitrarily high parent and an independent no-candidate event give the uniform lower rate. Includes horizon-dependent policies with a common bound. |

## Numerical refinement

`sections/original/numerical_certificate.tex` uses the original full-tree
potential, groups edge/vertical contributions using a common endpoint,
and adds `tau C` with

```text
beta = 2832242711 / 5000000000
tau  = 5294970481 / 100000000000000
zeta = 199752266575452391 / 1200500000000000000000000000
```

The corrected inequality is `L Phi_tau <= beta Phi_tau - zeta C`.
The exact check covers all 484,138 vertex rows. Affine incoming-rate
interpolation and bilinear tail rectangles extend the check to every
degree. The unchanged edge, vertical, and cherry residuals are covered
by the complete original GMP verification (17,329,108 inequalities).
The numerical input is therefore a finite certificate together with
an analytic all-degree argument, not a simulation.

The numerical result is independent of the new uniformity proof. It
does not require the inert motif-potential cancellation construction,
which is consequently omitted from this focused manuscript.

## Claims deliberately not made

- No irrationality or transcendence of the original `mu` is proved.
- No identification of the original exponent with a modified
  PAN/DAN/VAN exponent is made.
- No exact finite-dimensional determinant or finite polynomial
  Mellin equation for the original exponent is claimed.
- The universal two-sided algorithm is proved terminating; it is not
  packaged as an efficient high-precision numerical solver.
- No sharp mean amplitude or positive almost-sure normalized amplitude
  is asserted for the original model.
- Boundary robustness concerns the continuous-time mean exponent for
  the precisely specified root-leaf input policies. It does not assert
  invariance under arbitrary graph perturbations.
- Equality of the uniform upper generation pressure and inert pressure
  away from their critical parameter is not assumed or proved.
- Critical escape/nonvanishing and arithmetic specialization problems
  remain separate and are not hidden hypotheses of computability.

## Draft audit

The consolidation removed references to unavailable earlier notes,
included each analytic prerequisite used by the uniformity closure,
and separated the proof revision from the numerical-data revision.
The core-kernel definitions explicitly handle the one-leaf inert
singleton and the two-leaf full-tree singleton. Zero total leaf count
has its own degenerate burst rule. All theorem references and labels
are checked during manuscript compilation.

The reproducibility scripts certify finite arithmetic statements.
Their successful execution does not, by itself, certify the
infinite-state coupling proofs or the full computability theorem.
