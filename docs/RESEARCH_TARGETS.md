# Further research targets

The main draft's completed theorem is effective computation of the original
exponent, using an exact characteristic pressure and a uniform boundary
comparison. The local-model companion supplies a concrete irrationality
theorem. The arithmetic continuation proves first-promotion reductions and
coefficient-height asymptotics, full-critical certificate-polynomial
noncancellation, primitive-numerator growth, and several exact root and
derivative-ratio representations. The new critical-boundary theorem
also proves core-comparable eigenfunctions, the exact critical core-ring
equation, and mean core growth up to constant factors. The following
targets concern the remaining analytic, arithmetic, and computational gaps.

## 1. Make computation practical

The two-sided certificate algorithm terminates, but the proof supplies no
useful complexity estimate. Implementing it directly would enumerate large
finite environment profiles and histories. The useful next computational
step is a finite approximation with an explicit error on its critical
parameter, followed by a verified solver.

A successful reduction must preserve the evolving environment and justify
its tail bound uniformly. A good fit to simulations or a convergent sequence
without an effective outer error does not supply such a solver. The existing
boundary-leaf estimate is an analytic tool for controlling that error.

### What the new convergence statements provide

The exact-pressure iteration
`s_(n+1) = s_n + 63*log(r_infty(s_n))/(400*log(2))` contracts the distance
to `mu` by at least the factor `73/82` on the current enclosure. Its
remaining computational requirement is an efficient certified evaluation
of the pressure; the iteration does not supply an outer error bound for
the finite-generation approximation defining that pressure.

Equality-safe trisection gives a rational series with a geometric error
after each completed certificate stage, with endpoint denominators dividing
`Q*3^n` and width at most the initial width times `(2/3)^n`. A stage
dovetails strict lower and upper searches at two interior points, so it
does not need to decide equality with `mu`. This supplies no runtime bound
for obtaining the certificates. The implemented driver tests this scheduling
interface on exact demonstration roots; it does not implement the full
friend-tree upper search.

The generation series has an explicit geometric tail above any certified
upper bound `b >= mu`: for `b < s <= S`, `S > 1`, put
`theta = (S-s)/(S-b)` and `rho = S^(-(1-theta))`. Then

$$
A_m^\infty(s)\le[12(b+3)]^\theta\rho^m.
$$

This gives a stopping rule for the generation sum, with finite-history
errors handled separately. The rate deteriorates as `s` approaches `b`.
That tail estimate alone does not prove critical divergence. The new
directional comparison supplies a separate proof of fixed-seed
divergence and two-sided reciprocal-linear real-axis bounds.

The exact Yule population-tail helper also improves fixed-time finite-state
calculations to a geometric population cutoff bound. This identity is
restored from earlier project work. Spatial-profile and quadrature errors,
and the cost of the long-time critical limit, remain separate.

Eliminating every null ring now gives population-only lower sums
`L*_(m,N)`, with a proved error
`O_(s,m)(N^(-s)(log N)^(s+m-1))` for each fixed generation `m`.
The implemented bound uses rational root comparisons and a potential
genealogy second moment. This supplies an effective finite-population
approximation to each coefficient, but still leaves the outer generation
error for the pressure unresolved. An elementary envelope shows that any
threshold root of this family inside the current enclosure requires at
least 488 proper births; this is a necessary cost, not a sufficient budget.

The new fixed-discount formula

$$
\mu=2-\lim_{m\to\infty}\frac{B_m(2)}{B_{m+1}(2)},\qquad
B_m(s)=\frac1{m!}\int_0^\infty t^m e^{-st}F_2(t)\,dt,
$$

has positive rational coefficient expansions and explicit finite-population
tails for every fixed derivative. It uses no exact-pressure oracle.
The new estimate `F_2(t)=Theta(exp(mu*t))` now gives an
`O_s(m^(-1/2))` derivative-order bound, with a displayed constant in terms
of the core-comparison constants. Those constants have not been
numerically evaluated. The implemented finite-index ratio intervals
therefore still need this additional error input before enclosing `mu`.

## 2. Identify a usable arithmetic characteristic

For the local models, the root equation involves

$$
F(s)=\int_0^1 x^s e^{x-1}\,dx.
$$

The companion proves that `F(r)` is transcendental for every rational
`r > -1`. This yields the following useful conditional transfer principle:
if the original critical relation can be proved to imply

$$
P(\mu,F(\mu))=0,
$$

where the coefficients of `P(s,X)` are algebraic rational functions of `s`
and every rational candidate `r` in the relevant interval is a regular
specialization with `P(r,X)` nonzero, then `mu` is irrational. At a rational
candidate this would force the transcendental number `F(r)` to satisfy a
nonzero polynomial over the algebraic numbers.

No such exact finite reduction is known here for the original friend tree.
The independent-family derivation for the local models cannot be transferred
to the original interacting tree without a proof. Nonvanishing of a finite
truncation alone also does not establish the needed critical relation.

An alternative is an arithmetic theorem for the actual infinite kernel:
construct nonzero approximation witnesses and prove denominator or height
bounds strong enough that the critical relation would force an impossible
nonzero integer of absolute value below one. Both the nonvanishing and the
arithmetic growth estimates are necessary; numerical smallness alone is
insufficient.

### Established first-promotion arithmetic

The [transcendence continuation](../friend_tree_transcendence_progress.pdf)
now gives an exact hypergeometric transform for the full waiting phase
before the inert newborn's first promotion. It proves a positive residual
identity and excludes a rational telescope at every parameter in the
current enclosure for `mu`.

For positive algebraic `s`, with
`D = [Q((s + sqrt(s^2+4))/2):Q]`, its coefficients satisfy
`h(t_n(s)) = (2 - 2/D)*n*log(n) + O_s(n)`. At rational discounts, it also
determines the leading growth of primitive denominators and their least
common denominator. The exceptional rational parameters with `s^2+4` a
rational square are dense, including examples inside the enclosure.

These statements identify the arithmetic cost of the natural series; they
do not classify the arithmetic nature of its evaluated sum. The positive
residual and rational nonsummability do not themselves transfer that class
through all environments. Its accelerated rational enclosures concern the
first-promotion transform, not improved bounds for `mu`.

### Full-critical noncancellation is now available for certificate polynomials

For the actual finite-history lower sums `L_(m,R,N)(s)`, the continuation
clears the signed residual `12(s+3)-L_(m,R,N)(s)` to an integer polynomial.
An explicitly omitted history gives a strictly positive value at `mu`,
with explicit degree, height, and nonzero root-gap bounds. The increasing
largest nonnegative roots of the resulting product polynomials converge
to `mu`. Normalizing the finite lower sums also gives continuous residuals
decreasing to `1-r_infty(s)`, strictly positive at `mu` before tending to
zero. Their convergence is uniform on compact positive intervals, but
no effective rate in the history budget is proved.

Thus noncancellation for this full-model certificate construction is
established. The arithmetic target is now a sufficiently small value
relative to degree and height. For the literal clearers used in the note,
the critical values grow rather than tend to zero.

The stronger population-only hierarchy now resolves the primitive
normalization question for its entire family. All reachable poles have
nonzero residues of known sign. After removing every common polynomial
factor and dividing all integer content, its primitive numerators obey

$$
p_{m,N}(\mu)>1,\qquad
\min_{1\le m\le N}\log p_{m,N}(\mu)=N\log N+O(N).
$$

Simply reducing this family therefore cannot produce small arithmetic
forms. A remaining concrete target is a controlled signed combination or
another characteristic that cancels enough of the now-explicit poles,
while retaining a proof of nonvanishing and a usable height/error bound.
The theorem does not rule out such constructions.

The restored full-tree beta/Mellin representation is another exact
organization: its rational coefficients are `a_n=E C_n`, and its convergence
abscissa is `mu`. It does not yet provide a finite special-function equation,
a fixed-order recurrence for `a_n`, or a rapidly computable critical root.

There is now an explicit full-model recurrence hierarchy. For the generator
`L`, put `u_(r,n)=E[(L^r C)(T_n)]`; then
`u_(r,n+1)=u_(r,n)+u_(r+1,n)/n`. Its first two levels expose the
inverse-degree and neighbour correlations needed beyond `a_n` itself.
The corresponding generating functions satisfy
`(1-z)G_r'(z)-2G_r(z)=G_(r+1)(z)`, and each `a_n` has a finite
operator rising-factorial expression. This is an exact countable system.
The new star-pole theorem shows that `C, LC, L^2 C, ...` are linearly
independent on finite trees: no finite-dimensional invariant linear
observable space containing `C` exists. This still does not rule out
a more useful finite recurrence for the edge-start expectations or a
nonlinear reduction. A negative Hankel determinant also excludes a
positive real exponential-mixture representation for `F_2'/2`.
A characteristic relation in the discount parameter and a fixed-order
ODE for the population generating function are distinct reduction targets.

Statewise pole noncancellation must not be transferred to arithmetic of
the averaged coefficients without proof. The sixth edge-start generator
derivative has denominator 432, even though a natural star-history
subcollection contributes 72/5. This explicit cancellation identifies a
specific obstacle to deriving denominator lower bounds from stars alone.

The [dependency audit](transcendence_proof_dependencies.md) records the
proved components, the classical arithmetic inputs, and the remaining
transfer problem.

### A signed product route and its exact remaining gap

For the full original process, the bipartite product
`P_z(T) = product_v (1+sigma_v*z)_(d_v-1)/(d_v-1)!` is annihilated by the
generator. Its coefficients give a signed harmonic-number martingale `J`
with `E J^2 = E sum_v H^(2)_(d_v-1)`, between `E C` and `zeta(2) E C`.
At integer `z=k` the product is a signed integer binomial observable;
negative vertices of degree greater than `k` contribute zero.

The constructive target is to convert these generator cancellations into
a characteristic relation that depends on the actual critical discount.
The exact insertion identity
`L(x^C P_z)=(x-1)x^C P_z(Lambda+z Lambda_sigma)` removes the nonleaf terms
and leaves the original neighbor-dependent promotion rates. Closing or
estimating their tilted resolvent is a concrete version of this target.
The [product-polynomial note](product_polynomial_targets.md) records a
more specific structural candidate: after `q=1-z^2`, the averaged core
insertions and their promotion increments have nonnegative coefficients
in the exact data through population 9. The equivalent gamma-basis
positivity remains unproved. An exact positive recurrence in a Möbius
variable is available, but a seven-vertex example shows that it cannot
close on colored degree data alone.
The normalization `E P_z=1` holds for every auxiliary `z` and does not locate
`mu`. Statewise integrality does not remove probability denominators.
This limitation is substantive: the comparison rates
`lambda_v=N_opposite*d_v/(n-1)` preserve the product identities and exact
color Yule process while producing rational exponent `1`; the switch to
these rates may be delayed past any specified finite original prefix.
This comparison does not preserve the original exponent bracket.

For irrationality alone, a simpler sufficient target than transcendence
is available: nonzero integer polynomials with
`-log|P_N(mu)| / max(1,deg P_N) -> infinity`. If `mu=p/q`, integrality
gives `|P_N(mu)| >= q^(-deg P_N)`. Polynomial height does not enter this
rational-candidate argument. No current construction meets this target.

## 3. Use the now-proved critical boundary in an arithmetic construction

The [critical-boundary section](../sections/transcendence/critical_resolvent_compactness.tex)
resolves the fixed-seed divergence and core-ring escape questions.
Directional infection weights give a uniform relative approximation
by finitely many stub profiles. Independent permanent guardian events
compare those profiles to the inert seed. A root-input Dynkin comparison
then extends the common resolvent scale to all newborn environments.

In particular, for a fixed finite `K`,

$$
\frac1K\le A_m^\infty(\mu)<43,\qquad
\int_0^\infty e^{-\mu t}F_\infty(t)\,dt=\infty.
$$

Normalized core resolvents yield positive eigenfunctions uniformly
comparable with `C`. Thus the variational equation

$$
\mu=\inf_{C\le f\le K_f C}\sup_y\frac{L_\infty f(y)}{f(y)}.
$$

is now attained. For the selected one-stub eigenfunction,
`Q_mu H=H` has no escape term; before the first core ring the omitted
boundary is at most `A_* C exp(-(mu+C)t)`.
The population modes that exist at every discount remain outside this
core-comparable class.

The [signed renewal germ](signed_renewal_scope.md) consequently has a
genuine positive-real boundary value `B_mu(1)=1`, interpreted by
continuation. Its signed Taylor radius, an arithmetic description of its
infinite kernel coefficients, and a denominator-normalized nonzero
small-value estimate remain unresolved. The
[rational-specialization audit](rational_specialization_audit.md) makes
that next requirement precise. Real-axis reciprocal-linear bounds do
not themselves give a meromorphic pole or a limiting residue.

The full-environment operator on `ell^infinity` has
`r_ess(K_mu)=r(K_mu)=1`. Its finite compressions are nilpotent because
every genealogical step strictly increases population. Finite inert
proper-birth and core-ring determinants are also nonzero for positive
discounts. Thus a Fredholm determinant or finite regeneration reduction
needs a new invariant space, an exact environment quotient, or a proved
boundary contribution from infinite population. Existing finite-time
locality estimates do not by themselves establish such a reduction.

## 4. Strengthen growth asymptotics

For the original tree, determine whether normalized core counts have a
positive finite limit, and obtain a limiting mean amplitude. The new
core-comparable eigenfunctions prove
`F_2(t)=Theta(exp(mu*t))` and `E C_n=Theta(n^mu)`. They also give an
exact Pochhammer expectation for the selected eigenfunction and a
nonnegative normalized martingale; neither alone proves a positive
limiting core amplitude. The bounded-input
theorem currently identifies continuous-time mean exponents uniformly over
the stated policies. It does not assert arbitrary boundary perturbation
invariance, pathwise robustness, or a limiting amplitude.

## 5. Separate irrationality from transcendence

The proved arithmetic theorem for the local models excludes rational
exponents for algebraic activation parameters. It does not exclude
algebraic irrational exponents. Extending the argument to all algebraic
candidate exponents requires a further specialization theorem; the
rational-parameter E-function denominator argument is not automatically
valid at an algebraic irrational parameter.

The continuation makes this local target exact: transcendence of
`alpha_omega` for every finite algebraic `omega >= 0` is equivalent to
transcendence of `F(x)` for every algebraic real `x` in `[alpha_0,1)`, where
`alpha_0` is the PAN root. Sprindzuk's applicable `E*`-function theorem
gives finiteness under fixed degree bounds for fixed algebraic irrational
function parameter. It does not exclude the required evaluation point
`-1`; its exceptional set also varies with that parameter. Resolving this
specialization remains a local-model goal, with no automatic transfer to
the original exponent.

For the original tree, even irrationality remains open. Neither the
computable character of the root nor the presence of Mellin integrals is
evidence strong enough to classify its arithmetic nature.
