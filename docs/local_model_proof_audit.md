# Local redirection draft: proof dependencies and scope

This document records the mathematical dependencies and preparation checks for
`local_redirection_irrationality.tex`. It is a research draft, not a formal proof
assistant development or a report of external peer review.

## Claims and their proofs

| Claim | Location | Dependency |
| --- | --- | --- |
| Exact independent core-family representation | Section 2.1 | The three local transition rules; independent Poisson drivers and the strong Markov property |
| Excursion transform `h_l(s)` | Lemma 2.2 | Discounted backward recurrence, bounded stopping, nonexplosion, and the bound `h_l(s) <= 1/l!` |
| Exact reproduction transform and unique root | Theorem 2.1, Section 2.1 | Regeneration at zero, Poisson domination, and the first-child `Exp(1)` law |
| Almost-sure continuous-time core amplitude | Lemma 2.3 | The nonlattice CMJ law of large numbers in Iksanov–Kolesko–Meiners, Section 2.2 |
| Strict positivity of the CMJ martingale | Lemma 2.3 | A direct bounded-second-moment generation-martingale argument and its smoothing identity |
| Extension to every finite tree seed | Lemma 2.4 and Section 2.2 | Positive-probability preparation of a core with any positive leaf count, strong Markov inheritance, and a finite-family decomposition |
| Exact graph-size clock and discrete amplitude | Section 2.3 | The leaf rate `L + omega*C_0`, an integrable immigration drift, a square-integrable compensated martingale, and a Yule lower coupling |
| Effective root computation for computable `omega` | Section 2.4 | Explicit factorial series tail and `-m'(s) >= 1/(1+s)^2 >= 1/4` on `(0,1)` |
| Transcendence of `F(r)` for every rational `r > -1` | Theorem 3.1 | The verified E-function height conditions and the classical Siegel–Shidlovskii theorem |
| Irrationality of `alpha_omega` for finite algebraic `omega >= 0` | Theorem 3.2 | Theorem 3.1 and the exact characteristic equation from Theorem 2.1 |
| Transfer criterion for other exact reductions | Proposition 4.1 | Transcendence of rational specializations, together with an explicitly required nonvanishing polynomial specialization |

## Probability checks

1. A newborn core starts with one leaf. Its local leaf-count rates are upward
   `l`, downward `1` while `l > 0`, and activation `omega` at `l = 0`.
   Each downward move produces one newborn core. These rates are independent of
   adjacent core degrees; this is the fact that makes the CMJ representation exact.
2. The whole vertex process has rate at most `max(1, omega)*N`, and the core
   process has total core-birth rate at most its core count. Both are nonexplosive.
3. Eliminating the zero-state delay gives the reproduction transform
   `(s+omega)*(1-F)/(s*(s+omega-omega*F))`. Its denominators are positive for
   `s > 0`; the equivalent root equation has denominator
   `s + omega*(1-s) > 0` for `0 < s < 1`.
4. The first child arrives at an exponential age of rate one, and all child births
   are a thinning of a rate-one Poisson process. This proves nonlatticeness,
   strict monotonicity, a positive finite mean discounted childbearing age, and
   finite second moments of the discounted reproduction measure for every
   positive discount.
5. These moments imply the hypotheses in Iksanov–Kolesko–Meiners, Remark 2.1.
   The deterministic counting characteristic has integrable exponentially
   weighted local suprema, as required by their almost-sure upgrade of (2.13).
6. Lifetime offspring can be infinite. The draft therefore supplies a direct
   nondegeneracy proof: `Var(W_{j+1}) = m(2*alpha)*Var(W_j) + Var(Y)`, with
   `m(2*alpha) < 1`, gives a mean-one `L^2` limit; the smoothing equation and
   `K >= 1` almost surely, `P(K >= 2) >= 1/2`, give positivity. The equality
   of the generation and Nerman martingale limits is the standard result
   explicitly recalled in Iksanov–Kolesko–Meiners, Section 2.2.
7. The arbitrary-seed argument preserves the actual initial leaf counts. It does
   not replace an exceptional ancestor with an ordinary one by an unproved
   stochastic comparison.
8. The transfer to the vertex hitting times is pathwise. No expectation is
   interchanged with a random hitting time.

## Arithmetic checks

For rational `r > -1`, put `lambda = r+1 = a/b > 0` in lowest terms and
`f_lambda(z) = sum_{n>=0} z^n/(lambda+1)_n`.

- The beta-integral calculation gives `F(r) = f_lambda(-1)/lambda`.
- In E-function form the coefficients are
  `c_n = b^n*n! / product_{j=1}^n(a+b*j)`.
- The reduced denominators of **all** `c_0,...,c_n` divide
  `lcm(1,...,a+b*n)`. Prime powers dividing `b` cause no denominator;
  for every other prime power the arithmetic progression contains at most
  `floor(k/p^h)+1` multiples among its first `k` terms. Comparing with
  Legendre's formula proves the common-denominator bound.
- The elementary exponential bound for that least common multiple, together
  with `0 < c_n <= 1`, gives the required linear logarithmic height bound.
- The function is entire and nonpolynomial, hence transcendental over `C(z)`.
- The homogeneous system for `(1, f_lambda)` has its only finite pole at zero.
  The algebraic evaluation point `-1` is regular. Beukers's statement of the
  classical Siegel–Shidlovskii theorem (Theorem 1.1) applies directly.
- At a rational candidate root and algebraic `omega`, the right side of the
  characteristic equation is algebraic, while the left side is transcendental.
- The polynomial exponential-integral reduction is nonzero: for `r=p/q` in
  `(0,1)`, the amplitude `p*t^(p-1)` has degree at most `q-2`; a nonzero
  polynomial `R' + q*t^(q-1)*R` has degree at least `q-1`. Allowing rational
  `R` cannot remove this obstruction because a finite pole produces an
  uncancelled pole of one higher order in `R'`.

## Attribution and limits

The characteristic equation is already equation (25) of Hartle, Krapivsky,
Redner, and Zhang, *Anomalous scaling in redirection networks*, arXiv:2604.01540,
Physical Review E 114 (2026), 034314. The PAN and DAN equations are their
(22) and (17). The draft attributes them explicitly in its abstract,
introduction, and theorem discussion. The CMJ and E-function theorems are
classical inputs with precise primary references.

The results concern the local VAN family, including PAN and DAN. They do not
prove a root equation or irrationality theorem for the original friend-tree
exponent `mu`. They do not prove transcendence of `alpha_omega`, discrete-time
mean asymptotics, an `L^1` amplitude limit at graph size `n`, or a theorem for
the singular model `omega = infinity`.

The conditional transfer proposition is not applied to the original kernel.
A nonzero bivariate polynomial is insufficient: its specialization at a
rational parameter must remain a nonzero polynomial in the transform variable.

## Reproduction and preparation

- Numerical examples are reproduced by `scripts/check_van_root.py`, using only
  Python's standard library and exact `Fraction` arithmetic.
- `verification/van_root_checks.json` records exact root endpoints of width
  `2^-90`, strict sign margins, truncation orders, and finite denominator checks.
- The article displays rational decimal intervals of width `10^-24` that
  contain the recorded exact intervals.
- Numerical checks are not proofs of irrationality or substitutes for the
  infinite-population probability arguments.
- The draft was typeset with standard LaTeX packages, compiled in two passes,
  and checked for unresolved references and overfull boxes. Page renders were
  inspected for equation placement and legibility. The repository build command
  is the canonical way to reproduce the final PDF.

Primary references rechecked during preparation:

- [Hartle–Krapivsky–Redner–Zhang, equations (17), (22), (25)](https://arxiv.org/html/2604.01540v1)
- [Iksanov–Kolesko–Meiners, Section 2.2](https://arxiv.org/pdf/2109.00867v3)
- [Beukers, Theorem 1.1](https://annals.math.princeton.edu/wp-content/uploads/annals-v163-n1-p08.pdf)
- [Olofsson, the general `x log x` theorem](https://www.stat.rice.edu/~olofsson/xlogx.pdf)
