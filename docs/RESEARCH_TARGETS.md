# Further research targets

The main draft's completed theorem is effective computation of the original
exponent, using an exact characteristic pressure and a uniform boundary
comparison. The local-model companion supplies a concrete irrationality
theorem. The following targets concern additional results.

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

## 3. Resolve the critical resolvent boundary term

Separate exploratory work constructs a critical generator eigenfunction
and identifies an escape term when converting it to a first-core-event
kernel equation. Eliminating that term requires a growth bound or an
appropriate nonescape theorem for the transformed process. A sufficient
fixed-skeleton polynomial-growth condition has been identified, but the
required condition is not established in the general critical case.

This is a route toward a sharper critical operator description. It is not
an unresolved prerequisite of the effective computability theorem in the
main draft, which uses finite-time upper certificates and the uniform
growth equality.

## 4. Strengthen growth asymptotics

For the original tree, determine whether normalized core counts have a
positive finite limit, and obtain sharp mean asymptotics. The bounded-input
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

For the original tree, even irrationality remains open. Neither the
computable character of the root nor the presence of Mellin integrals is
evidence strong enough to classify its arithmetic nature.
