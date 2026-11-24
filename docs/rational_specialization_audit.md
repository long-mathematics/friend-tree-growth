# Rational specialization after the critical boundary theorem

This is an arithmetic audit of the original friend-tree representations.
It does not classify the exponent. It uses the fixed-seed critical boundary theorem in the
[critical boundary section](../sections/transcendence/critical_resolvent_compactness.tex)
and records the arithmetic step that remains unproved.

## 1. A precise limit of discount-shift acceleration

For the actual free-tree expectations \(a_n=\mathbb EC_n\), write

\[
w_n(s)=\frac{(n-1)!}{(s+2)_{n-1}},\qquad
\mathcal M(s)=\sum_{n\ge2}a_nw_n(s).
\]

The exact rational identity

\[
\frac{w_n(s+j)}{w_n(s)}
=\frac{(s+2)_j}{(n+s+1)_j}\qquad(j\ge0)
\]

shows what a candidate-specific rational combination of discount shifts
can achieve. Fix a positive rational candidate \(r=p/q\), and rational
coefficients \(c_0,\ldots,c_J\), not all zero. Let \(j_0\) be the first
index with \(c_{j_0}\ne0\). Then its combined population summand is

\[
a_n\sum_{j=0}^J c_jw_n(r+j)
=a_nw_n(r)\left[
 c_{j_0}(r+2)_{j_0}n^{-j_0}
 +O(n^{-j_0-1})\right].
\]

This follows directly by expanding the finite rational functions in
\(1/n\); no asymptotic formula for \(a_n\) beyond the established
\(a_n=n^{\mu+o(1)}\) is being assumed.

Consequently:

- If \(c_0\ne0\), the combined summand is asymptotic to
  \(c_0a_nw_n(r)\). It retains the critical tail, including its eventual
  sign and convergence or divergence. Rational specialization does not
  change this endpoint obstruction.
- If \(c_0=0\), the combination improves the power of decay, but removes
  the original critical transform. Under \(r=\mu\), the new summand is
  \(n^{-j_0-1+o(1)}\) and is summable; there is no established identity
  evaluating this new convergent transform to a rational number.

The same point is visible before expanding the beta integral: a finite
combination of shifts multiplies its integrand by a polynomial in
\(1-z\). A nonzero constant term leaves the singular endpoint unchanged;
vanishing there discards the critical term.

This rules out that specific direct tail-cancellation mechanism. It does
not rule out population-dependent orders, approximation schemes using
additional analytic structure, or other signed constructions. Those
require a new, proved estimate.

## 2. What the new boundary theorem genuinely adds

The independently audited directional infection/guardian argument yields
a bounded positive eigenfunction on the inert-stub environment class and
constants \(K<\infty\) with

\[
\frac1K\le A_m^\infty(\mu)\le48\qquad(m\ge0).
\]

Therefore, for the actual scalar generation series,

\[
F_\mu(z)=\sum_{m\ge0}A_m^\infty(\mu)z^m,
\]

one has

\[
\frac1{K(1-z)}\le F_\mu(z)\le\frac{48}{1-z}
\qquad(0\le z<1).
\]

The signed renewal germ continued along the positive real interval is
\(B_\mu(z)=1-1/F_\mu(z)\). Thus there is now a genuine nonzero
boundary remainder, with a two-sided estimate:

\[
\boxed{\quad
\frac{1-z}{48}\le1-B_\mu(z)\le K(1-z),\qquad
\lim_{z\uparrow1}B_\mu(z)=1.
\quad}
\]

This closes a previously missing critical-boundary step. It does not
make the remainder a rational linear form under the assumption that
\(\mu\) is rational.

## 3. The exact arithmetic gap

The renewal coefficients are

\[
b_m(r)=A_m^\infty(r)
-\sum_{j=1}^{m-1}b_j(r)A_{m-j}^\infty(r).
\]

Even at a fixed rational \(r\), the values \(A_j^\infty(r)\) are
infinite full-history sums. Finite history entries and their truncations
are rational, but this does not establish rationality of their limits.
In particular, clearing the denominator of \(r\) does not clear the
unknown numbers \(A_j^\infty(r)\) or \(b_j(r)\).

Furthermore, positive-axis continuation does not establish that the
Taylor series \(\sum b_m(r)z^m\) converges throughout \(|z|<1\).
Complex zeros of \(F_r\) may obstruct that Taylor series even though
\(F_r(z)>0\) on the positive real interval. Accordingly, finite sums
of \(b_m(r)\) are not yet justified critical convergents.

A successful candidate-specific irrationality argument must produce
explicit rational finite expressions \(R_N(r)\), exact denominator
clearers \(D_N(r)\in\mathbb Z_{>0}\), and remainder estimates such that,
under \(r=\mu\),

\[
0<\left|D_N(r)\bigl(R_N(r)-1\bigr)\right|<1
\]

for some \(N\), or an equivalent nonzero integer small-value relation.
The new boundary theorem supplies neither the required denominator-
normalized approximation error nor a Taylor/Padé continuation estimate.
The polynomial-height criterion for transcendence is unnecessary for
this rational-only target, but these denominator and nonzero-remainder
requirements remain necessary for this particular approach.

Integer specializations of the auxiliary product parameter do not bridge
this gap: that parameter is independent of the critical discount \(r\).
The signed integer state observables have rational expectations, but the
transition-probability denominators remain. No identity identifying their
integer specializations with the new critical renewal boundary value has
been proved.

## 4. Why the new Pochhammer identity is not yet arithmetic

Normalize the selected free critical eigenfunction by \(H(S_3)=1\),
where \(S_3\) is the three-vertex star. Its exact embedded expectation is

\[
\mathbb E H(T_n)=\frac{(\mu+3)_{n-3}}{(3)_{n-3}}\qquad(n\ge3).
\]

The right-hand side would be rational if \(\mu\) were rational.
That does not make each state value of \(H\) rational. Already at the
first branching population, the original transition probabilities
from \(S_3\) to the four-vertex star \(S_4\) and the four-vertex path
\(P_4\) are \(2/3\) and \(1/3\). The eigenfunction equation is just

\[
2H(S_4)+H(P_4)=3+\mu.
\]

For a rational candidate \(\mu\), this gives one rational linear
combination of two selected state values. The normalized-resolvent
construction has not supplied rationality or controlled denominators
for those values. Uniform comparison with the core count constrains
their size, not their arithmetic nature.

Thus the Pochhammer expectation and its nonnegative martingale do
not yet give an integer-valued observable or an integer small form.
An arithmetic description of the critical eigenfunction, or another
construction avoiding its unknown state values, remains necessary
for this route.
