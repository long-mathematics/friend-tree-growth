# Uniform growth and effective computation: dependency crosscheck

## Scope and conclusion

This is a focused mathematical review of the bridge from the original finite-seed
mean exponent `mu` to the uniform newborn exponent `lambda`, and of the resulting
two-sided certificate algorithm. It checks the hybrid truncation argument,
its moment and change-of-measure dependencies, the boundary resolvent
absorption, and the computability of each fixed-time upper bound `H(T)`.
No gap or circular dependency was found in these arguments as reviewed.

The conclusion uses the explicitly imported original-model mean-exponent
and weighted planting results, together with the certified lower bound
`mu >= 113/200 > 11/20`. It is not a fresh independent proof of every upstream
certificate, an audit of all source code, or a proof-assistant verification.
The proof establishes computability and the stated analytic characterizations;
it does not establish an arithmetic classification of `mu`.

The source arguments correspond to the manuscript sections in
`sections/original/finite_window.tex`, `controlled_moments.tex`,
`likelihood.tex`, `hybrid_gap.tex`, `boundary_gradient.tex`,
`finite_time_computation.tex`, and `computability.tex`. The supporting
locality, stabilization, inert-growth, and scalar-pressure arguments were
also checked for the particular uses below.

## 1. The hypotheses needed before the closure are available independently

The future-child decomposition gives the old-state estimate
`E_y C(t) <= C(y) H(t)`, where `H(t) = 1 + integral_0^t G(u) du` and
`G` is the supremum of newborn means over admissible finite environments.
It also gives submultiplicativity of `H` and `G <= H <= 1+tG`, so the
uniform exponent exists without assuming `lambda = mu`.

For every discount above `lambda`, the finite-window potential is bounded
above and below by positive multiples of the core count. Its increment is
uniformly bounded for **every ordinary vertex addition**, including a
promotion caused by attaching a new leaf to an existing leaf. The
connected-common-tree coupling proves this increment estimate at finite
horizon, independently of the later boundary infection argument.

Applying the generator to powers of the shifted potential gives controlled
moment bounds with rate `p*a` for every `a > lambda`. The quadratic
remainder is controlled by the total population moment of order `p/2`;
`a > 1/2` makes this contribution strictly subcritical. Thus the moment
bounds used in the likelihood argument do not presume the equality they
help prove.

The allowed boundary controls here have the specified predictable
Poisson-input construction, equivalently the stated conditional generator.
The argument does not authorize additional simultaneous compound jumps
merely because their separate event counts have bounded intensities.

## 2. The bounded-parent reference law is autonomous and has the right density

Replacing only the parent's degree-gain channel by `h(t)=(1+t)^(-2)`
makes the pair consisting of the retained component and parent degree
autonomous before the threshold crossing. The retained input remains
`1/D_parent <= 1/2`. For initial degree at most `M`, at most `M` parent
degree gains occur before crossing, and their actual intensity is at most
`M`. The actual-to-reference density is therefore bounded above by a
fixed polynomial in the observation time, uniformly over the original
exterior.

For the reverse comparison on a fixed finite completion, the actual
parent-gain intensity is at least `1/D_root >= 1/N`. If all these gains
occur before `epsilon*t`, the inverse density is bounded by
`exp(I_M) * N(epsilon*t)^M`. The stopped inverse-degree occupation has a
uniform conditional remaining-mean bound `B_M = 3*M^2*(1+3*M)`.
Ordered-time integration gives the required exponential moment for
`a*B_M < 1`. This bound applies also to neighbours born later: there are
at most `M` contributing neighbour labels before the crossing, and each
receives a permanent-slot input of rate at least `1/M` while the bound is
in force.

Three-factor Hölder is used with the correct density direction. Its
weighted factor is an expectation under a genuine finite-seed law, hence
has upper exponent at most `mu`. Its other two factors are the controlled
moment bound and the inverse-density moment. No independence of realized
neighbour processes or of the occupation and population factors is assumed.

## 3. The hybrid truncation handles the old component at a crossing

Under a hypothetical gap `g=lambda-mu>0`, bounded-parent histories have a
strict growth gap. Late changes have an exponentially small probability
by the local stabilization bound, which becomes a weighted smallness
estimate through the controlled second moment. Histories with no late
change are treated by the preceding likelihood calculation.

For the hybrid which deletes parent-to-root arrivals after the parent first
exceeds `M`, late crossings are bounded by the exit intensity times the
pre-crossing retained mean, followed by the old-state factor `H`.
Early crossings are treated by the same fixed completion. The extra
inverse-likelihood cost is at most `exp(t/(M+1))`, because the deleted
channel's intensity is bounded by `1/(M+1)`.

The reference density after deletion represents the genuine law restricted
to histories with no event in that channel. Its weighted core expectation
is consequently bounded by the unrestricted genuine mean. It is not an
assertion that deleting boundary arrivals monotonically lowers core means.
Choosing `1/(M+1) < g`, then a sufficiently small crossing-time fraction,
and finally a moment exponent sufficiently close to `lambda`, makes
both early and late crossing contributions strictly subcritical. This
argument does not restart a newborn estimate from an arbitrary old state.

## 4. The boundary estimate and absorption remain finite-horizon arguments

The boundary coupling uses aggregate leaf-gain and promotion channels.
An eligible uninfected core has identical local state in both copies; an
unmatched incoming leaf gain is its first possible discrepancy. Infection
therefore spreads along a connected portion of the eligible common core
tree. A charged family attaches only to an already infected eligible core.

At an infected core of smaller degree `d`, the discrepancy reservoir
`Q = degree_difference + union_promotions + infected_outward_neighbours`
has unit upward jumps at total rate at most `Q+5/2`. The separate aggregate
channels prevent an unaccounted simultaneous promotion and neighbour
infection. Previously grown common fringes and later feedback from charged
families are included in the rate estimate.

The resulting reproduction estimate is below `19/20` at discount `11/20`,
using the stated finite rational inequalities and the analytic bound for
`d >= 64`. Summing infection generations gives the uniform finite-horizon
boundary increment `40*W_T(s)/s`. The charged families start in admissible
newborn environments. Finite profiles with inert stubs lie in the same
finite-horizon closure, by completing each stub with a sufficiently
high-degree genuine parent and taking a limit.

The discounted Dynkin identity after the threshold crossing consequently
gives

`W_T(s) <= integral_0^T exp(-s*t) A_M(t) dt + 40*W_T(s)/(s^2*(M+1))`.

Every `W_T(s)` here is finite by core-count Yule domination. Division occurs
before sending `T` to infinity, so the argument does not assume its desired
uniform resolvent finiteness. For `M >= 132`, the contraction coefficient
at `s=11/20` is `16000/16093 < 1`. The hybrid gap then gives a discount
strictly between its exponent and `lambda`, contradicting the definition
of `lambda`. This proves `lambda=mu`.

## 5. The fixed-time upper calculation is effective

For fixed rational `T`, pruning at depth `R` or the first initial degree
at least `M` gives an explicitly finite profile set. Each retained degree
and leaf count is bounded and the retained depth is bounded. The potential
exterior-arrow event is independent of the potential tagged core genealogy;
this gives the uniform mean error

`exp(T) * (T^R/R! + (exp(T)-1)/M)`.

Profiles with inert stubs are admissible finite-horizon limits, so their
maximum supplies both sides of the supremum approximation. The use of
inert profiles therefore does not introduce an unproved enlargement of the
supremum.

For a profile with `n` real initial vertices, killing above population `N`
leaves a finite rational generator, including the finite genealogical marks
needed to identify the tag's family. Uniformization computes its mean. The
Yule second moment bounds the discarded mean by

`(n*(n+1)*exp(2*T) - n*exp(T))/N`.

Finally, all newborn means and their supremum are `exp(T)`-Lipschitz on
`[0,T]`. Rational quadrature therefore computes `H(T)` to any prescribed
rational accuracy. This calculation needs no convergence assertion for
finite-matrix Perron eigenvalues.

Once `lambda=mu`, enumerating strict certificates `H(T)<exp(s*T)` is
complete for every rational `s>mu`. The positive rational finite-history
sums for the inert generation coefficients are complete lower searches
for `s<mu`, by the exact pressure crossing and the uniform minorization.
Dovetailing pairs of these strict certificates halts at every requested
interval width; it never has to decide equality at a rational trial value.
No effective estimate for the hypothetical hybrid gap is required by this
algorithm, and no useful running-time bound is claimed.

## Imported planting input

The inert-growth argument uses the weighted planted-branch comparison,
not unweighted planted/free monotonicity. Its stated input was compared
with `proofs/existence.md` at upstream commit
`88f2f9c8c3ebc1b4e0c980db6afd97d29f3df176`: Lemma 4.1(c), Corollary 5.3,
and Lemma 6.1 give the required weighted expectation, root averaging,
and finite-seed reduction. The acceptance product remains inside the
reference expectation. This is consistent with the recorded counterexample
to an unweighted boundary-ordering assertion.
