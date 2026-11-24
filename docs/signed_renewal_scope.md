# A signed renewal reduction and its critical boundary theorem

This note records an exact reduction of the **original** environment kernel,
the newly proved fixed-seed boundary theorem, and the arithmetic step that
remains unproved. It does not prove irrationality of the friend-tree exponent.
The input kernel, comparison estimates, and
uniform resolvent bounds are those in the original manuscript and the
[arithmetic dependency audit](transcendence_proof_dependencies.md).

## 1. An exact signed scalar identity

Fix `s>0`, let `K=K_s` on bounded functions of full newborn environments,
and put

\[
\ell f=f(x_\infty),\qquad a=K\mathbf1,\qquad
D=K-a\otimes\ell,\qquad (a\otimes\ell)f=a\,\ell f.
\]

Here `x_infinity` is the inert newborn and `D 1=0`. Define

\[
F_s(z)=\ell(I-zK)^{-1}\mathbf1
      =\sum_{m\ge0}A_m^\infty(s)z^m,
\qquad A_0^\infty=1.
\]

For sufficiently small `|z|`,

\[
\boxed{F_s(z)=\frac1{1-B_s(z)},\qquad
B_s(z)=z\,\ell(I-zD)^{-1}a.}
\]

Indeed, with `u=(I-zK)^(-1)1`, the rank-one decomposition gives

\[
u=\mathbf1+z(I-zD)^{-1}a\,\ell u,
\]

because `(I-zD)^(-1)1=1`. Apply `ell`. The Neumann series justify all
operations, for example on `|z|<s/2`, since `||K||<=1/s` and `||D||<=2/s`.

The signed coefficients `B_s(z)=sum_(m>=1) b_m(s) z^m` satisfy

\[
b_m=\ell D^{m-1}a
=\sum_{j=1}^{m}(-1)^{j-1}
  \sum_{\substack{n_1+\cdots+n_j=m\\n_i\ge1}}
  A_{n_1}^\infty\cdots A_{n_j}^\infty.
\]

Equivalently,

\[
b_m=A_m^\infty-\sum_{j=1}^{m-1}b_jA_{m-j}^\infty.
\]

Thus

\[
b_1=A_1,\qquad b_2=A_2-A_1^2,\qquad
b_3=A_3-2A_1A_2+A_1^3.
\]

These formulas keep all original environment dependence. They do not
introduce independent descendant families. The `A_m` are exact kernel
values, and are not known to be rational merely because `s` is rational.

## 2. The critical boundary is now proved along the positive real axis

The [critical boundary section](../sections/transcendence/critical_resolvent_compactness.tex)
uses the actual friend dynamics to prove

\[
\frac1K\le A_m^\infty(\mu)\le48\qquad(m\ge0)
\]

for a fixed finite `K`. The earlier sharper upper bound below `43` also
remains valid. The proof uses directional infection estimates, prefix-free
cuts, finite inert profiles, and guardian events independent of the interior
drivers. It establishes divergence at the fixed inert seed, rather than
deducing that statement from divergence of a supremum.

For `0<=z<1` this gives

\[
\frac1{K(1-z)}\le F_\mu(z)\le\frac{48}{1-z}.
\]

Since `F_mu` is positive on this interval, the signed germ continues there
by `B_mu(z)=1-1/F_mu(z)`. Its critical boundary remainder satisfies

\[
\boxed{\frac{1-z}{48}\le1-B_\mu(z)\le K(1-z),\qquad
\lim_{z\uparrow1}B_\mu(z)=1.}
\]

This is a nonzero, controlled **analytic** remainder. The statement is
about continuation along the positive real axis. It does not assert that
the signed Taylor series has radius at least one, or that `sum_m b_m(mu)`
converges: complex zeros of `F_mu` still require separate analysis.

An arithmetic specialization is also still required. At rational `r`,
the exact values `A_j^infinity(r)` and `b_j(r)` are not known to be rational.
Rational finite-history approximations need error bounds after their
denominators are cleared. See the
[rational-specialization audit](rational_specialization_audit.md) for the
precise remaining integer-small-value condition.

## 3. A rational critical kernel with finite pointwise boundary values

The following positive weighted shift explains why the earlier operator
estimates alone could not prove the boundary theorem.
Choose any rational `eta` in the certified interval for `mu`, and set

\[
\alpha=\frac{1-\eta}{2},\qquad
c=\frac{1+\eta}{2},\qquad \rho(s)=\frac{c}{s+\alpha}.
\]

On `ell^infinity(N_0)`, define

\[
(T_sf)(n)=\rho(s)\left(\frac{n+5}{n+6}\right)^2 f(n+1).
\]

Every entry at rational `s` is rational. The nonzero entry is the
positive Laplace transform

\[
\int_0^\infty e^{-st}
c\left(\frac{n+5}{n+6}\right)^2e^{-\alpha t}\,dt.
\]

Finite compressions are nilpotent. The exact generation coefficients are

\[
A_m(s;n)=\rho(s)^m\left(\frac{n+5}{n+m+5}\right)^2,
\]

so

\[
u_m(s)=\rho(s)^m\left(\frac5{m+5}\right)^2,
\qquad v_m(s)=\rho(s)^m.
\]

State zero attains the infimum, so the reference-state comparison holds
with constant one. Also `u_m` is supermultiplicative, since
`(5+m)(5+n)>=5(5+m+n)`. The elementary original-kernel bounds hold:

\[
\|T_s\|=\rho(s)\le\frac1s,\qquad
[2(s+2)]^{-m}\le A_m(s;n)\le s^{-m}.
\]

For the lower bound, each weight is at least `rho(s)(5/6)^2`.
Throughout the indicated interval `2c(5/6)^2>1` and `alpha<1/2`, so

\[
2c(5/6)^2(s+2)\ge s+\alpha.
\]

The pressure is exactly `rho(s)`, whose critical root is `s=eta`.
For `s>eta`, monotone convergence in the starting state gives

\[
\sup_n\sum_{m\ge0}A_m(s;n)
=\frac1{1-\rho(s)}=\frac{s+\alpha}{s-\eta}.
\]

Thus the uniform resolvent diverges at least at reciprocal-linear rate.
Nevertheless, at every **fixed** state,

\[
\sum_{m\ge0}A_m(\eta;n)
=(n+5)^2\sum_{j=n+5}^{\infty}\frac1{j^2}<\infty.
\]

The critical supremum over `n` is infinite. At the reference state,

\[
F_\eta(z)
=25z^{-5}\left(\operatorname{Li}_2(z)
                    -\sum_{j=1}^{4}\frac{z^j}{j^2}\right),
\]

with a removable singularity at zero. Its boundary value is

\[
F_\eta(1)=25\bigl(\zeta(2)-H_4^{(2)}\bigr)<\infty.
\]

Here the signed renewal series even has nonnegative coefficients and
converges at one. To see this, write `A_m=25/(m+5)^2` and
`r_m=A_(m+1)/A_m=((m+5)/(m+6))^2`. These ratios increase, and the renewal
recurrence gives

\[
b_{m+1}=\sum_{j=1}^{m}
b_jA_{m-j}\bigl(r_m-r_{m-j}\bigr)\ge0
\]

inductively from `b_1=A_1>0`. Tonelli applied to `F=1+BF` at one, using
`F_eta(1)<infinity`, now proves ordinary convergence and

\[
B_\eta(1)=\sum_{m\ge1}b_m
=1-\frac1{F_\eta(1)}<1.
\]

This is a comparison **operator**, not another realization of the friend
rule. It proves that the listed operator estimates, rational entries,
and a rational critical root within the numerical interval can coexist.
The directional and guardian arguments now supply additional information
for the actual friend dynamics. This comparison lacks their resulting
uniformly positive critical generation coefficients. It remains useful
for separating the earlier operator estimates from that stronger theorem.

## 4. What a local-environment reduction still has to prove

The original locality theorem approximates each fixed reward
`K_s^m 1` uniformly from finite local information. This is useful but does
not prove that `K_s` contracts a norm on *arbitrary* local observables,
or that it is compact on a space which retains the critical exponent.
The new essential-radius theorem rules out such compactness on the
original full supremum-norm space.
The new relative approximation of resolvent rewards does not contradict
this result: it applies to a particular normalized family, not arbitrary
bounded observables.

Retagging at a child moves a fixed old vertex one edge farther away.
Discrepancies can also propagate inward before that birth. A successful
local-space construction must control both effects and unbounded degrees,
with constants uniform over the observables and number of transfers.

A direct decorated finite-radius projection is not an exact Markov
quotient. Take a core path from the newborn tag to a vertex `v` on the
radius-`R` boundary. Keep the entire decorated ball and all its full
degree labels fixed. Give `v` a core neighbor `w` outside the ball, of
degree two in one environment and degree three in another, by adding a
leaf outside the ball. The rate of a new leaf attaching to `v` differs
by `1/2-1/3=1/6`. Thus the generator does not close on that projection.
This example does not exclude another quotient or a suitable space of
local observables.
