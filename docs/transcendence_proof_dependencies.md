# Arithmetic and root representations: proof dependencies and scope

This document records the claims in
[`friend_tree_transcendence_progress.tex`](../friend_tree_transcendence_progress.tex),
*Transcendence targets for the friend-tree exponent: exact first-promotion
reduction and arithmetic obstructions*, by Christopher D. Long. It is a
research continuation, not external peer review or proof-assistant
verification. Neither irrationality nor transcendence of the original
exponent `mu` is proved.

## Contextual inputs

The continuation uses the original inert newborn: one real core, one real
leaf, and one inert parent stub. The stub contributes to degree but has no
source clock. Its null events must be eliminated explicitly. This is not a
free-star initial state or a local VAN family.

The original exponent's existence, enclosure, and full generation-pressure
characterization `r_infty(mu)=1` are contextual inputs from the existing
project at revision
[`6ee9d6e6402699e02860eb02dde319d28a6df385`](https://github.com/long-mathematics/friend-tree-growth/tree/6ee9d6e6402699e02860eb02dde319d28a6df385).
Their upstream and internal dependencies remain those recorded in the
[original-model audit](original_proof_dependencies.md). The new arithmetic
arguments do not alter the improved upper-bound certificate or reprove
existence of the exponent.

The local root equation, uniqueness, and irrationality at finite algebraic
activation parameters are inputs from the companion manuscript, with
dependencies recorded in the [local-model audit](local_model_proof_audit.md).

The full-critical sections additionally use the pressure supremum formula
and complete strict lower/upper certificate searches from that original
proof chain. The beta/Mellin section uses the original free tree started
from an edge, with `a_2=E C_2=0`; it does not identify these free-tree
coefficients with the inert-newborn generation coefficients. The scalar
beta identity and exact Yule tail restore earlier exploratory derivations;
they are not presented as newly discovered identities.

## Proved statements

The theorem numbers below refer to the continuation.

| Statement | Location | Dependencies and scope |
| --- | --- | --- |
| Exact joint first-promotion weights and hypergeometric transform | Theorem 2.1 | Original rates `j`, `j/(j+1)`, and `1/(j+1)`; exact null-event elimination; multiplication of discounted channels; gamma-ratio asymptotics |
| Positive residual identity | Theorem 3.1 | A rational difference identity and its explicit finite terminal term; the terminal term vanishes at every positive discount |
| Complete classification of rational telescopes | Theorem 3.2 | Pole-orbit exclusion, polynomial degree comparison, and invertibility at positive integer discounts; no rational telescope exists anywhere in the current enclosure for `mu` |
| Nonzero boundary at `s=1` | Proposition 3.3 | The explicit polynomial telescope, the gamma-ratio limit, and reflection; this evaluation gives no arithmetic classification |
| Accelerated rational enclosures | Theorem 4.1 | Exact lower/upper residual signs, summation with a vanishing terminal term, and the coefficient asymptotic; enclosure width is `O_s(M^(-s-5))` |
| Primitive rational denominators and common denominators | Theorem 5.1 | Exact split/inert prime valuations, Hensel lifting, Legendre's formula, and the classical weighted quadratic Mertens estimate |
| Algebraic coefficient-height asymptotic | Theorem 6.1 | Exact good-prime ideal valuations, exclusion of finitely many bad primes, unconditional number-field Mertens, and polynomial bounds for every conjugate |
| Exact arithmetic class of the two natural generating functions | Corollary 6.2 | Their differential equations, the denominator dichotomy, and Theorem 6.1; the ordinary series is a `G`-function and its Borel transform an `E`-function exactly when `s` is rational and `s^2+4` is a rational square |
| Equivalent target for transcendence of the entire local family | Proposition 7.1 | Solving the established local root equation for its activation parameter, monotonicity, and uniqueness of the local root |
| Positive integer clearer and explicit degree/height bounds | Signed-certificate section, `scp:clearer` | Unnormalized beta entries, finite ring and population budgets, and a least-common-multiple degree clearer |
| Full-critical noncancellation | Signed-certificate section, `scp:nonvanishing` | The pressure supremum formula gives `A_m(mu) <= 12(mu+3)`; an explicit prefix of null rings and chain promotions supplies a strictly positive omitted reward |
| Increasing algebraic-root representation of `mu` | Signed-certificate section, `scp:roots` | Completeness of the finite lower-certificate hierarchy and monotonicity; no error rate in the common history budget is proved |
| Signed normalized residuals converging to `1-r_infty(s)` | Signed-certificate section, `scp:pressure-residual` | Cofinal finite-history lower sums and the pressure supremum formula; positive residuals at `mu`, with qualitative compact convergence but no effective budget modulus |
| Geometric iteration using the exact pressure | Pressure-iteration section, `pci:contraction` | Convex secant bounds for `log r_infty`, the known enclosure, and `r_infty(s) <= 1/s`; anchored contraction factor `73/82` |
| Full-tree beta/Mellin series and convergence abscissa | Scalar beta-series section, `hfk:mellin` and `hfk:abscissa` | Independence of Yule holding times and the embedded tree chain, Tonelli, and the established mean exponent; restores an earlier exploratory identity |
| Geometric tail at a fixed interior generating-function argument | Scalar beta-series section, `hfk:fixed-z` | The bound `E C_n <= n-2` and explicit sums of quadratic coefficients times a geometric sequence |
| Exact countable recurrence and differential hierarchy | Scalar beta-series section, `hfk:hierarchy` | The original one-step operator `I+L/n`, finite generator powers, and polynomial observable bounds; includes a finite operator rising-factorial formula, not a finite scalar closure |
| First moment drifts and logarithmic-average formula for `mu` | Scalar beta-series section, `hfk:second-level` and `hfk:logarithmic-average` | Exact changes under leaf addition/promotion and the known mean exponent; no pointwise limit of the normalized promotion rates is asserted |
| Equality-safe rational series | Certificate-series section, `rr:trisection` | Complete strict searches at two distinct trisection points, fair scheduling, and a strict starting bracket; counts completed stages rather than runtime |
| Explicit geometric generation tail above a certified upper bound | Certificate-series section, `rr:generation-tail` | The critical coefficient bound, potential genealogy at `S>1`, and Hölder interpolation |
| Exact Yule population-tail helper | Certificate-series section, `rr:yule-tail` | Negative-binomial size bias and its finite binomial-tail identity; earlier project identity applied to fixed-time cutoff computation |
| Exact reduced poles for the population-only hierarchy | Population section, `pop:poles` | Elimination of every null ring, strict ordering of holding-rate pole intervals by population, same-sign residues, and an explicit reachability classification |
| Primitive numerators never small at criticality | Population section, `pop:primitive-growth` | Minimal scalar clearer, integer-content divisibility, an omitted proper-birth history, and Stirling; all `p_(m,N)(mu)>1`, with minimum logarithm `N log N+O(N)` after all polynomial and content cancellation |
| Stronger algebraic-root hierarchy | Population section, `pop:roots` | Domination of the earlier lower sums and completeness; exact product degree, but no effective root-error rate |
| Explicit fixed-generation population error | Population section, `pop:tail` | Rate-one potential genealogy, exact second moment, Yule two-founder hitting probability, and Cauchy–Schwarz without independence; rate `O_(s,m)(N^(-s)(log N)^(s+m-1))` for fixed `s,m` |
| Fixed-discount Laplace derivative-ratio limit | Derivative section, `tl:ratio` | The established free-tree mean exponent and gamma concentration, with a separate first-moment tail argument; requires no limiting amplitude or generation-ratio limit |
| Rational derivative series and finite tails | Derivative section, `tl:beta-jet` and `tl:rational-tail` | Positive beta-product coefficients, complete homogeneous polynomials, and an exactly telescoping dominant tail for `s>1`; finite-index ratio enclosures do not enclose `mu` |
| Positive population modes at every discount | Population-eigenfunction section, `pm:all-discounts` | Proper-birth coupling between rates `n-1/2` and `n`, positive gamma-bounded population limits, Markov scaling, finite first-step equations, and a conservative Doob transform; marked core hazard proves no escape |
| Core-growth variational characterization | Population-eigenfunction section, `pm:variational` | Uniform comparability with `C`, localized Dynkin/Fatou, and the inherited canonical resolvent; no attainment of the infimum is asserted |
| Uniform critical resolvent divergence | Population-eigenfunction section, `pm:uniform-pole` | Variational growth comparison and the original bound `V_s <= (1+W(s))C/s`; no exchange of supremum and integral and no claim of a pointwise critical pole |
| No finite invariant linear closure containing the core count | Generator section, `fgo:star-pole` and `fgo:independence` | Finite history patterns on stars, increasing pole orders, and two elementary seed comparisons; does not exclude an edge-start scalar equation or a nonlinear closure |
| Failure of a positive scalar spectral representation | Generator section | Exact edge-start generator derivatives, negative Hankel determinant, and an explicit negative-square certificate; specific to `F_2'/2` and positive measures with exponential moments near zero |
| Sufficient polynomial small-value criterion | Final arithmetic audit | The nonzero integer resultant for an algebraic candidate; signed nonzero polynomials are now available, but the required small-value estimate relative to height remains unproved |

The height theorem uses absolute logarithmic Weil height. If
`vartheta = (s + sqrt(s^2+4))/2` and `D = [Q(vartheta):Q]`, then

$$
h(t_n(s))=\left(2-\frac2D\right)n\log n+O_s(n).
$$

The rational-square exceptions have only exponential common-denominator
growth and are dense in the positive reals. They cannot be excluded by the
current enclosure for `mu`. Rational nonsummability still holds at those
parameters inside that enclosure.

## Classical arithmetic inputs

- [Zhao, Section 1.2](https://doi.org/10.1007/s40993-025-00640-y)
  records the unconditional character-sum form used in the rational
  denominator argument.
- [Garcia and Lee, Theorem 1, (A1)--(A2)](https://arxiv.org/abs/2007.10313v4)
  supplies the unconditional number-field Mertens estimate used in the
  prime-ideal height argument.
- [Beukers, Theorem 1.1 and the surrounding definitions](https://annals.math.princeton.edu/wp-content/uploads/annals-v163-n1-p08.pdf)
  records the `E`-function arithmetic conditions and classical
  Siegel--Shidlovskii theorem. The new coefficient-height theorem obstructs
  direct use of that framework outside the stated rational-square case.
- [Sprindzuk, Theorems 1 and 3](https://doi.org/10.1070/IM1968v002n01ABEH000632)
  applies to the local function family through the broader `E*` class. For
  fixed algebraic irrational parameter and fixed degree bounds, it gives
  finiteness of algebraic points with algebraic values of those degrees.
  It does not exclude the required point `-1`, and its exceptional set
  varies with the parameter.

These cited theorems supply inputs to the written arguments. No RH or GRH
assumption is used in the coefficient-height or denominator theorems.

## Remaining arithmetic gaps

The first-promotion transform `Phi(s) = E exp(-s*tau)` is one component of
the original kernel. It is strictly less than one for positive `s`, so
`Phi(mu)=1` is not the original critical equation. Its formal nonzero
rational-summation class does not imply that its value is irrational, or
that the class survives a signed reduction involving every environment.

The full-model finite lower sums now give signed integer polynomials
`P_(m,R,N)` with rigorously positive values at `mu`. This is a separate
construction from transferring the first-promotion rational-summation
class. Its coarse height bound is explicit, but its literal cleared
critical values grow: on the diagonal budgets,
`P_(m,h,h)(mu) > (3/2)^h` for `1 <= m <= h`. They therefore do not supply
the small values required for the stated resultant criterion. That
coarse-clearer observation alone did not settle primitive normalization.
The stronger population-only family `L*_(m,N)` now does: every reachable
pole survives, its residual is put in reduced polynomial form, and all
integer content is divided out. The resulting `p_(m,N)` always satisfies
`p_(m,N)(mu)>1`, with uniform minimum logarithmic growth `N log N+O(N)`.
This closes the primitive-normalization loophole for this precise family.
It does not rule out linear combinations, other signed characteristics,
or arithmetic cancellations after a fixed rational specialization.

The exact-pressure iteration has a proved rate only for exact or certified
pressure queries. An effective outer error for finite-generation pressure
evaluations is still absent. The algebraic-root supremum has no asserted
rate in its finite-history budget. Its normalized residuals converge to
`1-r_infty(s)` uniformly on compact positive intervals, but this qualitative
uniform convergence supplies no effective modulus. Equality-safe trisection has a geometric
rate in completed certificate stages, but the full strict-certificate
searches have no useful runtime bound and are not implemented by the
generic scheduling helper.

The full-tree beta/Mellin formula identifies a convergence abscissa, not a
finite special-function equation. The recurrence and differential hierarchy
is countable; its first drift already needs observables beyond the core
count. The growing star-pole theorem now rules out every finite-dimensional
invariant linear observable space containing `C`, a stronger statement
than the earlier six-vertex example. It still does not rule out every
possible finite scalar equation for the edge-start expectations.
The operator-factorial representation uses finite polynomial operations
on the generator and assumes no bounded-operator functional calculus.
The explicit generation-resolvent tail
applies above a certified upper bound and deteriorates toward it. Bounded
critical coefficients and pressure one do not establish divergence of the
critical generation sum, so no reciprocal-resolvent zero or pointwise
critical pole is asserted. Uniform resolvent suprema do diverge at least
as `1/(s-mu)`; this does not imply divergence at any prescribed finite seed.

The derivative-ratio formula provides a genuine stronger limit relation
at one fixed rational discount, and every fixed derivative has certified
rational series enclosures. The proof uses only a qualitative mean
exponent, however, and supplies no effective rate in derivative order.
Moment positivity concerns the unnormalized time-tilted integrals `Z_m`;
their values are not known to be rational. It therefore does not supply
a rational continued-fraction proof of irrationality. The negative
generator-moment Hankel certificate concerns a different sequence.

The all-discount population eigenfunctions show that exact positivity and
even no-escape harmonicity for the full kernel do not identify the critical
parameter. Uniform comparability with the core count does identify it.
These population modes do not resolve the escape term of the separately
constructed core-reward-normalized critical eigenfunction. Likewise the
statewise star-pole theorem does not prove edge-start numerical denominator
noncancellation: the explicit fifth-prime cancellation in the sixth
generator derivative demonstrates the missing transfer.

The arithmetic function classification concerns the two specific natural
generating functions. A Borel transform changes the evaluation: the actual
first-promotion value is `H_s(1)-1`, not an asserted `E_s` specialization.
The local-family equivalence likewise proves neither its transcendence
assertions nor a transfer to the original model.

## Reproduction and finite verification

The reference run of `scripts/check_first_promotion.py` contains 106,865
exact finite checks at 14 rational parameters, with indices through 80
and primes through 251. It checks the original null-event recursion,
independent backward equations, the finite reduction boundary, tail
residuals and widths, and good-prime numerator valuations. Exact fractions
give the transform enclosures; their decimal endpoints are rounded
outwards. Floating denominator diagnostics are separately labelled as
exploratory and make no proof decisions.

Run the full quick suite with `python3 scripts/run_checks.py`, or run this
checker separately:

```sh
python3 scripts/check_first_promotion.py --check --output build/verification/first_promotion_checks.json
python3 scripts/check_critical_root_forms.py
python3 scripts/rapid_root_tools.py
python3 scripts/full_tree_recurrence.py --check --output build/verification/full_tree_recurrence_checks.json
python3 scripts/primitive_population_tools.py --check
python3 scripts/laplace_derivative_tools.py --check
python3 scripts/check_generator_obstructions.py --check
```

The committed reference report is
[`verification/first_promotion_checks.json`](../verification/first_promotion_checks.json).
Build the note with `python3 scripts/build_papers.py --paper transcendence`.

The critical-root checker audits finite signed-polynomial construction and
its exact arithmetic. The rapid-root helper checks Yule-tail identities and
cutoff selection, plus the equality-safe scheduler on exact demonstration
roots. Its demonstrations are not new evaluations or brackets for `mu`.
Both are included in the quick suite; the generated reports state the
checks actually performed. The infinite noncancellation, root-limit, and
contraction statements require their written proofs.

The full-tree recurrence calculator additionally checks the first two
levels of the new hierarchy by comparing source/neighbour choices with
aggregated attachment probabilities and by testing the drift at each
retained tree. Its
[reference report](../verification/full_tree_recurrence_checks.json)
uses the original edge-start free tree, records the edge exception, and
includes the six-vertex diagnostic for closure in the core count alone.
It does not test every level of the countable hierarchy or supply an
asymptotic error estimate for recovering `mu` from the finite coefficients.

The new population checker records 1,340 exact checks through five proper
births, using independent source-choice and aggregate-state recursions,
reduced polynomial arithmetic, content bounds, omitted histories, and
rational tail comparisons. Its `N=487,488` envelope comparison proves a
necessary birth budget only, not that a witness at budget 488 exists.
The derivative helper records 3,686 exact checks of the complete homogeneous
recurrence, independent Newton identities, and tail telescoping. The
generator-obstruction checker records 29 exact checks of star formulas,
the seven derivatives, the two negative-moment certificates, and the
explicit cancellation example. Reports are committed in `verification/`.

The finite checks do not establish an infinite tail limit, prime-density
estimate, denominator asymptotic, or transcendence assertion. Those limits
and asymptotics require the written analytic and number-theoretic proofs;
the desired arithmetic classification of the exponents remains open.
